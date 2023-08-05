import numpy as np
import bilby
import astropy.cosmology
import copy

def get_weights_mass_transfo(old_priors, new_priors, samples, prior_name = None):
    """
    Function computing the weights when going from a prior
    sampling upon Mc and q to a prior where we sample 
    upon m1 and m2. This is a modification to bilby 
    so that we also correct the likelihood

    ARGS:
    -----
    - old_piors: the old prior dictionary that was used
                 during the run 
    - new_priors: the new prior, which is the targeted 
                  prior
    - samples: dictionary with the samples used to computed
               the weights and quantities
    - prior_name: list of parameter names for which 
                  the prior needs to be modified

    RETURNS:
    --------
    - weigths: the weights related to the transformation   
               from the (Mc, q) space to (m1, m2) space
    """

    weights = []

    if prior_name is not None:
        shared_parameters = {key : samples[key] for key in new_priors if key in 
                             old_priors and key in prior_name}
    else:
        shared_parameters = {key : samples[key] for key in new_priors if key in 
                             old_priors}

    parameters = [{key : samples[key][i] for key in shared_parameters.keys()}
                  for i in range(len(samples['mass_1']))]

    for i in range(len(parameters)):
        w = 1

        for key in shared_parameters.keys():
            val = samples[key][i]
            w *= new_priors.evaluate_constraints(parameters[i])
            w *= new_priors[key].prob(val)/old_priors[key].prob(val)

        weights.append(w)

    return weights

def convert_Mc_q_prior_to_component_masses_priors(old_priors, old_likelihood,
                                                  samples, fraction = 0.5,
                                                  prior_name = None):
    """
    Function converting the results with priors in Mc and q
    into priors in M1 and M2 and also adapts the likelihood
    accordingly (difference with Bilby equivalent)

    NOTE: this works only if there is an explicit prior
          given on q, Mc, m1 and m2


    ARGS:
    -----
    - old_priors: the priors that have been used in 
                  the runs, where we sampled upon Mc and q
    - old_likelihood: the old likelihood value, which will 
                      be adapted to match the new prior space
    - samples: the samples from the first run which will be 
               used to compute the weights in the transformation
    - fraction: (default is 0.5) the fraction of all the samples
                 that will be used to perform the transformation
    - prior_name: list of nales of priors that should be common
                  to the two sets of priors, notably those
                  for which the modifications should be done

    RETURNS:
    --------
    - new_priors: the new prior dictionary
    - new_samples: the reweighed samples, modified according 
                   to the transformation
    - new_likelihood: the new value of the likelihood, adapted to 
                      follow the transformation
    """

    new_priors = copy.copy(old_priors)
    old_priors = copy.copy(old_priors)
    samples = copy.copy(samples)

    for key in ['chirp_mass', 'mass_ratio']:
        new_priors[key] = bilby.core.prior.base.Constraint(minimum = new_priors[key].minimum,
                                                           maximum = new_priors[key].maximum,
                                                           name = key, latex_label = None)
    for key in ['mass_1', 'mass_2']:
        new_priors[key] = bilby.core.prior.Uniform(minimum = new_priors[key].minimum,
                                                   maximum = new_priors[key].maximum,
                                                   name = new_priors[key].name,
                                                   latex_label = None)

    # get the weights for the mass transfo
    weights = np.array(get_weights_mass_transfo(old_priors, new_priors, samples,
                                                prior_name = ['mass_1', 'mass_2',
                                                              'mass_ratio',
                                                              'chirp_mass']))
    Jacobian = np.array([(samples['mass_1'][i]**2)/samples['chirp_mass'][i]
                         for i in range(len(samples['mass_1']))])

    weights = Jacobian * weights

    # make the new samples
    size = int(fraction*len(samples['mass_1']))
    inds = len(samples['mass_1'])
    idxs = np.random.choice(inds, size = size, p = weights/np.sum(weights))
    new_samples = dict()
    for key in samples.keys():
        new_samples[key] = [samples[key][ind] for ind in idxs]

    # adapt the likelihood 
    new_likelihood = old_likelihood + np.log(np.mean(weights))

    return new_priors, new_samples, new_likelihood

def convert_Dl1_Mu_prior_to_Dl1_Dl2_prior(old_priors, old_log_likelihood, samples, n_samps = int(1e5)):
    """
    Function converting the Dl1, Mu prior used in GOLUM to 
    an adapted prior in Dl1, Dl2 for the population effects.
    Here, we assume that m1, m2, Dl1 priors remain the same
    and we just change the mu_rel prior into a 
    UniformInComovingVolume prior for the second 
    luminosity distance

    ARGS:
    -----
    - old_priors: the old priors used in during 
                  the GOLUM run 
    - old_log_likelihood: the joint likelihood coming out
                          of the GOLUM analysis.
    - samples: dict with the samples that need to be reweighed
    - n_samps: int, the number of sample point to use to do 
               the change in variable

    RETURNS:
    --------
    - ln_probs: the natural log of the probabilities for
                the m1, m2, Dl1, Dl2 samples
    - new_log_likelihood: the new value for the log
                        likelihood after the change of variable
    - new_samples: the new samples produced by the reweighing 
                   process
    """

    # setup the new priors
    old_priors = copy.copy(old_priors)
    new_priors = copy.copy(old_priors)
    samples = copy.copy(samples)

    # remove mu_rel from new priors and add dl2
    new_priors.pop('relative_magnification')
    new_priors['luminosity_distance^(2)'] = bilby.gw.prior.UniformComovingVolume(name = 'luminosity_distance',
                                                                               minimum = 100,
                                                                               maximum = 5e4)

    # make resampling to get dl2 and weights
    idxs = np.random.choice(len(samples['luminosity_distance^(1)']), size = n_samps)
    resamps = dict()
    for key in samples.keys():
        resamps[key] = np.array(samples[key])[idxs]
    resamps['luminosity_distance^(2)'] = np.sqrt(resamps['relative_magnification'])*\
                                       resamps['luminosity_distance^(1)']

    # compute the weights for the change in variable
    Js = 2*np.sqrt(resamps['relative_magnification'])/resamps['luminosity_distance^(1)']
    pDl2s = np.exp(new_priors['luminosity_distance^(2)'].ln_prob(resamps['luminosity_distance^(2)']))
    pMus = np.exp(old_priors['relative_magnification'].ln_prob(resamps['relative_magnification']))
    Weights = Js*pDl2s/pMus

    # make the new samples with the adapted weights
    # take their prob too
    new_samples = dict()
    inds = np.random.choice(len(resamps['luminosity_distance^(1)']), size = n_samps,
                            p = Weights/np.sum(Weights))
    for key in new_priors.keys():
        new_samples[key] = resamps[key][inds]

    ln_probs = new_priors.ln_prob(new_samples, axis = 0)
    new_log_likelihood = old_log_likelihood + np.log(np.mean(Weights))

    return ln_probs, new_log_likelihood, new_samples
