import numpy as np
import bilby
import logging
from hanabi.hierarchical.utils import get_ln_weights_for_reweighting, downsample
from hanabi.inference.utils import ParameterSuffix
from hanabi.hierarchical.cupy_utils import _GPU_ENABLED, PriorDict, logsumexp 
from bilby.core.likelihood import Likelihood 
from bilby.core.prior import Prior
from hanabi.hierarchical.marginalized_likelihood import LuminosityDistanceJointPriorFromMagnificationJointDist, DetectorFrameComponentMassesFromSourceFrame
from .golum_to_hanabi import convert_Dl1_Mu_prior_to_Dl1_Dl2_prior
from .lensing_models import (LuminosityDistanceJointPriorFromJointMagnificationCatalog, 
                             LuminosityDistanceJointPriorFromJointMagnificationJAX)

    

if _GPU_ENABLED:
    import cupy as xp
else:
    import numpy as xp

class MonteCarloMarginalizedLikelihood(Likelihood):
    """
    This is a copy of the function with the same name in 
    hanabi.hierarchical with as only modification that the
    function does not take a bilby.result object as input
    but takes the samples and the joint evidence as 
    individual inputs (for GOLUM compatibility)
    """
    def __init__(self, samples, joint_evidence, mass_src_pop_model, spin_src_pop_model, magnification_joint_distribution, sampling_priors=None, sep_char="^", suffix=None, n_samples=None, kde = False, use_jax = False):
        # The likelihood is a function of the source redshift only
        # Might as well do this marginalization deterministically
        self.parameters = {'redshift': 0.0}
        self._meta_data = None
        self._marginalized_parameters = []
        self.samples = samples
        self.joint_evidence = joint_evidence
        self.mass_src_pop_model = mass_src_pop_model
        self.spin_src_pop_model = spin_src_pop_model

        self.sep_char = sep_char
        if suffix is None:
            self.suffix = ParameterSuffix(self.sep_char)
        else:
            self.suffix = suffix

        if kde == False:
            # we use the analytical model for each magnification
            self.fct_prob_luminosity_distance = self.compute_ln_prob_for_luminosity_distances_sis_analytical
            # Backward compatibility: previously we expect the 4th argument to be a list of absolute magnification distributions
            if type(magnification_joint_distribution) is list:
                magnification_joint_distribution = {"absolute_magnification" + "_{}".format(i+1): magnification_joint_distribution[i] for i in range(len(magnification_joint_distribution))}
                # NOTE The default suffix ^(_) is not compatible with variable naming rules in python
        
            for k in list(magnification_joint_distribution.keys()):
                # Check if the default suffix is in the keys
                if not k.isidentifier():
                    raise NameError("{} is not a valid variable name in python. Please rename the parameter (e.g. absolute_magnification_1 instead)".format(k))
            self.magnification_joint_distribution = PriorDict(magnification_joint_distribution)

        else:
            if use_jax == True:
                self.fct_prob_luminosity_distance = self.compute_ln_prob_for_luminosity_distances_jax
                # in this case, we can only consider two images for the moment
                self.magnification_joint_distribution = {"absolute_magnification" + "_{}".format(i+1): None for i in range(2)}
                self.magnification_kde = magnification_joint_distribution


            else:
                 # we use a model based on a usual kde
                self.fct_prob_luminosity_distance = self.compute_ln_prob_for_luminosity_distances_kde

                # in this case, we can only consider two images for the moment
                self.magnification_joint_distribution = {"absolute_magnification" + "_{}".format(i+1): None for i in range(2)}
                self.magnification_kde = magnification_joint_distribution
                        

        
        # Downsample if n_samples is given
        self.keep_idxs = downsample(len(self.samples['mass_1']), n_samples)
        assert sampling_priors is not None, "Sampling priors have to be specified when using effective lensing parameters are used!"
        if 'relative_magnification' in samples.keys():
            parameters_to_extract = ["luminosity_distance" + self.suffix(0)]
            parameters_to_extract += ["mass_1", "mass_2", "relative_magnification"]
            samps = dict()
            prior_dict = bilby.core.prior.PriorDict()
            for par in parameters_to_extract:
                samps[par] = np.array(self.samples[par])
                prior_dict[par] = sampling_priors[par]
            # pass everything to the conversion function 
            sampling_prior_ln_prob, self.joint_evidence, samples = convert_Dl1_Mu_prior_to_Dl1_Dl2_prior(prior_dict,
                                                                                                         self.joint_evidence,
                                                                                                         samps,
                                                                                                         n_samps = int(1e6))
            parameters_to_extract = ["luminosity_distance" + self.suffix(trigger_idx) for trigger_idx, _ in enumerate(self.magnification_joint_distribution.keys())]
            parameters_to_extract += ["mass_1", "mass_2"]
            # do the downsampling on the correct correct samples
            self.keep_idxs = downsample(len(sampling_prior_ln_prob), n_samples)
            self.sampling_prior_ln_prob = sampling_prior_ln_prob[self.keep_idxs]
            self.data = {p : np.array(samples[p])[self.keep_idxs] for p in parameters_to_extract}

        else:
            # Extract only the relevant parameters
            parameters_to_extract = ["luminosity_distance" + self.suffix(trigger_idx) for trigger_idx, _ in enumerate(self.magnification_joint_distribution.keys())]
            parameters_to_extract += ["mass_1", "mass_2"]
            self.data = {p: np.array(self.samples[p])[self.keep_idxs] for p in parameters_to_extract}

            # Evaluate the pdf of the sampling prior once and only once using numpy
            self.sampling_prior_ln_prob = sampling_priors.ln_prob(self.data, axis=0)

        logger = logging.getLogger("hanabi_hierarchical_analysis")
        if _GPU_ENABLED:
            # NOTE gwpopulation will automatically use GPU for computation (no way to disable that)
            self.use_gpu = True
            logger.info("Using GPU for likelihood evaluation")
            import cupy as cp
            # Move data to GPU
            self.sampling_prior_ln_prob = cp.asarray(self.sampling_prior_ln_prob)
            for k in self.data.keys():
                self.data[k] = cp.asarray(self.data[k])
        else:
            # Fall back to numpy
            self.use_gpu = False
            logger.info("Using CPU for likelihood evaluation")

    def compute_ln_prob_for_luminosity_distances_sis_analytical(self, z_src):
        parameters = ["luminosity_distance" + self.suffix(trigger_idx) for trigger_idx, _ in enumerate(self.magnification_joint_distribution.keys())]
        new_priors = LuminosityDistanceJointPriorFromMagnificationJointDist(
            self.magnification_joint_distribution,
            z_src,
            sep_char=self.sep_char,
            suffix=self.suffix
        )

        return new_priors.ln_prob({p: self.data[p] for p in parameters}, axis=0)

    def compute_ln_prob_for_luminosity_distances_kde(self, z_src):
        # works only for two images
        # in this case, we assume that magnification_joint_dsitribution corresponds to the kde
        # version of the magnification
        parameters = ["luminosity_distance"+self.suffix(trigger_idx) for trigger_idx in range(2)]
        new_priors = LuminosityDistanceJointPriorFromJointMagnificationCatalog(self.magnification_kde,
                                                                               z_src,
                                                                               sep_char = self.sep_char,
                                                                               suffix = self.suffix)
        return new_priors.ln_prob({p : self.data[p] for p in parameters})
    def compute_ln_prob_for_luminosity_distances_jax(self, z_src):
        """
        works only for two image. Function 
        to compute the information using jax
        """
        parameters = ['luminosity_distance'+self.suffix(trigger_idx) for trigger_idx in range(2)]
        new_priors = LuminosityDistanceJointPriorFromJointMagnificationJAX(self.magnification_kde,
                                                                           z_src, sep_char = self.sep_char,
                                                                           suffix = self.suffix)
        return new_priors.ln_prob({p : self.data[p] for p in parameters})

    def compute_ln_prob_for_component_masses(self, z_src):
        det_frame_priors = DetectorFrameComponentMassesFromSourceFrame(
            self.mass_src_pop_model,
            z_src=z_src
        )

        return det_frame_priors.ln_prob({p: self.data[p] for p in ["mass_1", "mass_2"]}, axis=0)

    def log_likelihood(self):
        z_src = float(self.parameters["redshift"])
        ln_weights = self.compute_ln_prob_for_component_masses(z_src) + \
            self.fct_prob_luminosity_distance(z_src) - \
            self.sampling_prior_ln_prob
        ln_Z = self.joint_evidence + logsumexp(ln_weights) - np.log(len(ln_weights))
        return np.nan_to_num(ln_Z, nan=-np.inf)
