"""
Causal Inference Module for IusMorfos V6.0
Propensity Score Matching and Related Methods
"""

from .psm import (
    run_complete_psm,
    estimate_propensity_scores,
    perform_matching,
    check_balance,
    estimate_att,
    rosenbaum_sensitivity
)

__all__ = [
    'run_complete_psm',
    'estimate_propensity_scores',
    'perform_matching',
    'check_balance',
    'estimate_att',
    'rosenbaum_sensitivity'
]

__version__ = '1.0.0'
__author__ = 'IusMorfos V6.0 Development Team'
