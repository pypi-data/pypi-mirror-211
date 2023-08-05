"""
Script with additional models compared to the ones
used in Hanabi
"""

import bilby 
import numpy as np
import astropy.cosmology as astro_cosmo
from scipy.stats import gaussian_kde
from scipy.special import logsumexp
from hanabi.inference.utils import ParameterSuffix
from hanabi.hierarchical.cupy_utils import _GPU_ENABLED

if _GPU_ENABLED:
    import cupy as xp
else:
    import numpy as xp

try:
    import jax
    import jax.numpy as jnp
    from jax import jit, vmap
except:
    print("Jax cannot be imported. Therefore, you cannot use it to seep kde up")


@jit
def kde_jax(x, data, bandwidth):
    """
    Function to make a gaussian kde in jax

    ARGUMENTS:
    ----------
    - x: the values for which the KDE should be evaluated
    - data: the data used to make the kde
    - bandwidth: the width to make the Gaussian kde

    RETURNS:
    --------
    - the gaussian kde
    """
    kernel = jnp.exp(-jnp.sum((x - data) ** 2, axis=1) / (2 * bandwidth ** 2)) / (bandwidth ** 2 * (2 * jnp.pi))
    return jnp.mean(kernel)

def make_jax_kde(data, bandwidth = 5):
    """
    Function to make a 2 JAX kde when doing the analysis

    ARGUMENTS:
    ----------
    - data: the data we should use to make the kde (assumed to be a
            dictionary with entries ['mu1', 'mu2'])
    - bandwidth: the width of the Gaussian kde. The default
                 value is 5 and matched the gaussian_kde

    RETURNS:
    --------
    - jax_kde: a jax_kde object
    """
    samples = jnp.array([[data['mu1'][i], data['mu2'][i]] for i in range(len(data['mu1']))])
    jax_kde = jit(vmap(lambda x : kde_jax(x, samples, bandwidth)))

    return jax_kde

class LuminosityDistanceJointPriorFromJointMagnificationCatalog(object):
    """
    Class encoding the probability to observed given luminosity
    distances given a catalog model including models
    """

    def __init__(self, magnification_kde, z, cosmology = None, sep_char="^", suffix = None):
        """
        Initialization of the class

        ARGUMENTS:
        ----------
        - magnification_kde: the gaussian kde with the probability
                             distribution for the magnifications
        - z: the redshift under consideration
        - sep_char: the character to split the name of the parameter
                     and the label of the image
        - suffix: the suffix to use to distinguish the different images
        - cosmology: the cosmology under which we work. The default
                     is astropy.cosmology.Planck15
        """

        self.magnification_kde = magnification_kde
        self.z = z
        self.sep_char = sep_char
        if suffix is None:
            self.suffix = ParameterSuffix(self.sep_char)
        else:
            self.suffix = suffix

        if cosmology is not None:
            self.cosmo = astro_cosmo.cosmology
        else:
            self.cosmo = astro_cosmo.Planck15

        # make the intrinsic luminosity distance
        self.intrinsic_luminosity_distance = bilby.gw.conversion.redshift_to_luminosity_distance(self.z,
                                                                                                 cosmology = self.cosmo)


    def jacobian(self, magnification):
        """
        Function computing the Jacobian for the change in 
        variable

        ARGUMENTS:
        ----------
        - magnification: the magnification for which the Jacobian
                         needs to be computed

        RETURNS:
        --------
        - J: the jacobian for the change in variable
        """

        J = 2*(magnification**1.5)/self.intrinsic_luminosity_distance

        return J

    def prob(self, joint_parameter):
        """
        Function computing the probability for the given joint parameters. 
        They should at least contain the luminosity distance for the 
        two images

        ARGUMENTS:
        ----------
        - joint_parameters: the joint parameters for the two 
                            observed data streams. Should at 
                            least contain the two luminosity 
                            distances

        RETURNS:
        --------
        - the probability to observe these luminosity distances
          given the magnification model
        """

        # make the corresponding magnifications
        mags_1 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(0)])**2
        mags_2 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(1)])**2

        # compute the probabilities to observes the magnification
        prob_mus = self.magnification_kde(np.vstack([mags_1, mags_2]))

        # compute the Jacobian
        J1 = self.jacobian(mags_1)
        J2 = self.jacobian(mags_2)

        return (J1*J2*prob_mus)

    def ln_prob(self, joint_parameter):
        """
        Function computing the log value of the probability 
        to observe given luminosity distances bases on the 
        magnification model.

        ARGUMENTS:
        ----------
        - joint_parameter: the parameters describing the two
                           observed data stream. Should at least
                           contain the two luminosity distances

        RETURNS:
        --------
        - the log of the probability to observe the luminosity 
          distances given the magnification model

        """

        return xp.log(self.prob(joint_parameter))


class LuminosityDistanceJointPriorFromJointMagnificationNFs(LuminosityDistanceJointPriorFromJointMagnificationCatalog):
    """
    Function implementing the probability to observe given
    magnifications given that we are using normalizing flow models.
    Here, the magnification KDE is expected to be a denmarf DensityEstimate
    object
    """

    def prob(self, joint_parameter):
        """
        Function computing the probability for the given joint parameters. 
        They should at least contain the luminosity distance for the 
        two images

        ARGUMENTS:
        ----------
        - joint_parameters: the joint parameters for the two 
                            observed data streams. Should at 
                            least contain the two luminosity 
                            distances

        RETURNS:
        --------
        - the probability to observe these luminosity distances
          given the magnification model
        """

        # make the magnifications
        mags_1 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(0)])**2
        mags_2 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(1)])**2

        # get the weights
        data = np.array([[mags_1[i], mags_2[i]] for i in range(len(mags_1))])
        logls = self.magnification_kde.score_samples(data)
        prob_mus = np.exp(logls - logsumexp(logls))

        # get the Jacobians
        J1 = self.jacobian(mags_1)
        J2 = self.jacobian(mags_2)

        return (J1*J2*prob_mus)


class LuminosityDistanceJointPriorFromJointMagnificationDPGMM(LuminosityDistanceJointPriorFromJointMagnificationCatalog):
    """
    Function implementing the probability to observe a given magnification 
    given that we are using the DPGMM method (https://ui.adsabs.harvard.edu/abs/2022MNRAS.509.5454R/abstract).
    Here, the magnification de is expected to be a DPGMM figaro object
    """

    def prob(self, joint_parameter):
        """
        Function computing the probability for the given joint parameters. 
        They should at least contain the luminosity distance for the 
        two images

        ARGUMENTS:
        ----------
        - joint_parameters: the joint parameters for the two 
                            observed data streams. Should at 
                            least contain the two luminosity 
                            distances

        RETURNS:
        --------
        - the probability to observe these luminosity distances
          given the magnification model
        """

        # make the magnifications
        mags_1 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(0)])**2
        mags_2 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(1)])**2

        # make the data as it should be input to the model
        data = np.array([[mags_1[i], mags_2[i]] for i in range(len(mags_1))])
        prob_mus = self.magnification_kde.pdf(data)

        # compute the jacobians
        J1 = self.jacobian(mags_1)
        J2 = self.jacobian(mags_2)

        return (J1*J2*prob_mus)

class LuminosityDistanceJointPriorFromJointMagnificationJAX(LuminosityDistanceJointPriorFromJointMagnificationCatalog):
    """
    Function implementing the probability to observe a given magnification 
    using jax
    """

    def prob(self, joint_parameter):
        """
        Function computing the probability for the given joint parameters. 
        They should at least contain the luminosity distance for the 
        two images

        ARGUMENTS:
        ----------
        - joint_parameters: the joint parameters for the two 
                            observed data streams. Should at 
                            least contain the two luminosity 
                            distances

        RETURNS:
        --------
        - the probability to observe these luminosity distances
          given the magnification model
        """

        # make the magnifications
        mags_1 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(0)])**2
        mags_2 = (self.intrinsic_luminosity_distance/joint_parameter["luminosity_distance"+self.suffix(1)])**2

        # make the data as it should be input to the model
        data = jnp.array([[mags_1[i], mags_2[i]] for i in range(len(mags_1))])
        prob_mus = self.magnification_kde(data)

        # compute the jacobians
        J1 = self.jacobian(mags_1)
        J2 = self.jacobian(mags_2)

        return (J1*J2*prob_mus)