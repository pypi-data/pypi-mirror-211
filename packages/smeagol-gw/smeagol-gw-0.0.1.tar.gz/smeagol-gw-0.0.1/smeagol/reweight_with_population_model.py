import numpy as np
import logging
from scipy.special import logsumexp
from astropy.cosmology import Planck15
import bilby
import pandas as pd
from bilby.core.prior import Prior
from hanabi.hierarchical.utils import get_ln_weights_for_reweighting, downsample, setup_logger
from hanabi.hierarchical.cupy_utils import _GPU_ENABLED, PriorDict
from hanabi.hierarchical.marginalized_likelihood import DetectorFrameComponentMassesFromSourceFrame
from hanabi.hierarchical.reweight_with_population_model import LuminosityDistancePriorFromRedshift

class ReweightWithPopulationModel(object):
    """
    Copy of the function with the same name in Hanabi but 
    changing the way in whih the information is read.
    Instead of taking as input a biby.result object
    we take the posteriors, log_evidence and priors
    indicidually.
    """
    def __init__(self, posteriors, log_evidence, priors, mass_src_pop_model, spin_src_pop_model, z_src_prob_dist, n_samples=None):
        #self.result = result
        self.posteriors = posteriors
        self.log_evidence = log_evidence
        self.priors = priors

        # Check if redshift is calculated and stored in result.posterior
        if not "redshift" in self.posteriors.keys():
            self.posteriors = bilby.gw.conversion.generate_source_frame_parameters(self.posteriors)

        # Downsample if n_samples is given
        self.keep_idxs = downsample(len(self.posteriors['mass_1']), n_samples)
        # Extract only the relevant parameters
        parameters_to_extract = ["luminosity_distance", "mass_1", "mass_2"]
        self.data = {p: np.array(self.posteriors[p])[self.keep_idxs] for p in parameters_to_extract}

        # Evaluate the pdf of the sampling prior once and only once using numpy
        sampling_priors = PriorDict(dictionary={p: self.priors[p] for p in parameters_to_extract})
        self.sampling_prior_ln_prob = sampling_priors.ln_prob(self.data, axis=0)
        self.data["redshift"] = np.array(self.posteriors["redshift"])[self.keep_idxs]
         
        logger = logging.getLogger("hanabi_hierarchical_analysis")
        if _GPU_ENABLED:
            # NOTE gwpopulation will automatically use GPU for computation (no way to disable that)
            self.use_gpu = True
            logger.info("Using GPU for reweighting")
            import cupy as cp
            # Move data to GPU
            self.sampling_prior_ln_prob = cp.asarray(self.sampling_prior_ln_prob)
            for k in self.data.keys():
                self.data[k] = cp.asarray(self.data[k])
        else:
            # Fall back to numpy
            self.use_gpu = False
            logger.info("Using CPU for reweighting")

        self.mass_src_pop_model = mass_src_pop_model
        self.spin_src_pop_model = spin_src_pop_model
        self.z_src_prob_dist = z_src_prob_dist
        self.ln_weights = self.compute_ln_weights()

    def compute_ln_prob_for_component_masses(self, z_src):
        det_frame_priors = DetectorFrameComponentMassesFromSourceFrame(
            self.mass_src_pop_model,
            z_src=z_src
        )
        
        new_prior_pdf = det_frame_priors.ln_prob({k: self.data[k] for k in ["mass_1", "mass_2"]}, axis=0)
        return new_prior_pdf

    def compute_ln_prob_for_luminosity_distances_from_redshift(self, z_src):
        if self.use_gpu:
            import cupy as cp
            # Use CPU instead
            z_src = cp.asnumpy(z_src)

        new_prior_pdf = np.log(LuminosityDistancePriorFromRedshift(self.z_src_prob_dist).prob_from_z_src(z_src))

        if self.use_gpu:
            new_prior_pdf = cp.asarray(new_prior_pdf)

        return new_prior_pdf

    def compute_ln_weights(self):
        ln_weights = self.compute_ln_prob_for_component_masses(self.data["redshift"]) + \
            self.compute_ln_prob_for_luminosity_distances_from_redshift(self.data["redshift"]) - \
            self.sampling_prior_ln_prob
        
        if self.use_gpu:
            import cupy as cp
            ln_weights = cp.asnumpy(ln_weights)
        return ln_weights

    def reweight_ln_evidence(self):
        ln_Z = self.log_evidence + logsumexp(self.ln_weights) - np.log(len(self.ln_weights))
        return ln_Z

    def reweight_samples(self):
        if isinstance(self.posteriors, dict):
            # make it to the correct format
            self.posteriors = pd.DataFrame().from_dict(self.posteriors)
        reweighted_samples = bilby.result.rejection_sample(self.posteriors.iloc[self.keep_idxs], np.exp(self.ln_weights))
        
        return reweighted_samples
