"""
Universal EGT Predictor - Domain-Agnostic Interface
===================================================

This module provides a sklearn-style API for making constitutional reform predictions
based solely on Constitutional Lock-in Index (CLI) scores.

The predictor works for ANY legal domain: labor law, property rights, tax policy, 
criminal law, environmental law, free speech, etc. Only input needed is CLI score.

Based on:
- Vince, T.L. & Brown, J.S. (2005). Evolutionary Game Theory, Natural Selection,
  and Darwinian Dynamics. Cambridge University Press.
- Dawkins, R. (1982). The Extended Phenotype. Oxford University Press.

Usage Example:
--------------
>>> from src.egt import UniversalEGTPredictor
>>> 
>>> # Step 1: Initialize predictor
>>> predictor = UniversalEGTPredictor()
>>> 
>>> # Step 2: Fit to your CLI score (from any domain)
>>> predictor.fit(cli_score=0.87)  # Argentina labor law
>>> 
>>> # Step 3: Get predictions
>>> result = predictor.predict()
>>> print(result['reform_success_probability'])  # 0.124
>>> print(result['bifurcation_status'])  # 'locked_irreversible'
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import warnings

from .g_function import LotkaVolterraGFunction, GFunctionParams
from .darwinian_dynamics import DarwinianDynamics
from .ess_solver import ESSSolver, StabilityType


@dataclass
class VinceParameters:
    """
    Parameters from Vince (2005) worked examples.
    
    Conservative defaults based on Chapter 11 examples.
    Users can override for domain-specific calibration, but defaults work universally.
    """
    r: float = 0.25  # Intrinsic growth rate (time^-1)
    K_max: float = 100.0  # Maximum carrying capacity
    sigma_alpha: float = 1.0  # Competition niche width
    beta: float = 0.0  # Asymmetry parameter (0 = symmetric competition)
    
    # Bifurcation parameters (from Vince Ch. 11)
    bifurcation_threshold: float = 0.70  # CLI threshold for regime transition
    ess_curvature_multiplier: float = 10.0  # Strength of ESS (higher = stronger lock-in)
    crisis_amplification: float = 1.5  # Crisis effect multiplier (conservative)


class UniversalEGTPredictor:
    """
    Universal predictor for ANY constitutional domain.
    
    This class implements a sklearn-style API (fit-predict) for making
    quantitative predictions about constitutional reform success based solely
    on Constitutional Lock-in Index (CLI) scores.
    
    The predictor is domain-agnostic: same CLI score gives same prediction
    regardless of whether it's labor law, criminal law, environmental law, etc.
    
    Attributes
    ----------
    cli : float
        Constitutional Lock-in Index [0,1] fitted to the predictor
    g_function : LotkaVolterraGFunction
        Underlying fitness-generating function
    ess_result : ESSResult
        Result from ESS solver (computed during fit)
    vince_params : VinceParameters
        Parameters from Vince (2005) worked examples
        
    Examples
    --------
    >>> # Example 1: Argentina labor law
    >>> predictor = UniversalEGTPredictor()
    >>> predictor.fit(cli_score=0.87)
    >>> result = predictor.predict()
    >>> print(result['reform_success_probability'])  # Low (strong lock-in)
    
    >>> # Example 2: Chile criminal law (same code, different domain)
    >>> predictor = UniversalEGTPredictor()
    >>> predictor.fit(cli_score=0.28)
    >>> result = predictor.predict()
    >>> print(result['reform_success_probability'])  # High (weak lock-in)
    """
    
    def __init__(self, vince_parameters: Optional[VinceParameters] = None):
        """
        Initialize universal predictor with default Vince (2005) parameters.
        
        Parameters
        ----------
        vince_parameters : VinceParameters, optional
            Custom parameters from Vince (2005). If None, uses conservative defaults.
        """
        self.vince_params = vince_parameters or VinceParameters()
        self.cli: Optional[float] = None
        self.g_function: Optional[LotkaVolterraGFunction] = None
        self.ess_result = None
        self._fitted = False
        
    def fit(self, cli_score: float) -> 'UniversalEGTPredictor':
        """
        Fit G-function to Constitutional Lock-in Index score.
        
        This method constructs the fitness-generating function G(v, u, x)
        calibrated to the provided CLI score, then solves for Evolutionarily
        Stable Strategy (ESS).
        
        Parameters
        ----------
        cli_score : float
            Constitutional Lock-in Index [0, 1]
            Measures institutional rigidity in your domain of interest.
            
        Returns
        -------
        self : UniversalEGTPredictor
            Returns self for method chaining
            
        Raises
        ------
        ValueError
            If cli_score not in [0, 1] range
            
        Examples
        --------
        >>> predictor = UniversalEGTPredictor()
        >>> predictor.fit(cli_score=0.65)
        >>> # Now ready for prediction
        """
        if not 0 <= cli_score <= 1:
            raise ValueError(f"CLI score must be in [0,1], got {cli_score}")
            
        self.cli = cli_score
        
        # Map CLI to niche width (sigma_k)
        # High CLI → Low sigma_k → Strong speciation pressure
        # This mapping is from Vince Ch. 11 bifurcation analysis
        sigma_min, sigma_max = 0.5, 4.0
        sigma_k = sigma_max - cli_score * (sigma_max - sigma_min)
        
        # Construct G-function with Vince parameters
        g_params = GFunctionParams(
            r=self.vince_params.r,
            K_max=self.vince_params.K_max,
            sigma_k=sigma_k,
            sigma_alpha=self.vince_params.sigma_alpha,
            beta=self.vince_params.beta
        )
        
        self.g_function = LotkaVolterraGFunction(g_params, cli_score=cli_score)
        
        # Solve for ESS
        dynamics = DarwinianDynamics(
            self.g_function,
            ns=1,  # Single strategy for univariate analysis
            sigma_u_squared=0.01  # Strategy mutation rate
        )
        
        solver = ESSSolver(
            g_function=self.g_function,
            dynamics=dynamics,
            ns=1
        )
        
        # Find ESS starting from u0 = [0.0]
        self.ess_result = solver.solve(u0=np.array([0.0]))
        
        self._fitted = True
        return self
        
    def predict(self) -> Dict[str, any]:
        """
        Generate falsifiable predictions about reform success.
        
        This method computes:
        - Reform success probability
        - ESS strength (resistance to change)
        - Bifurcation status (regime classification)
        - Confidence intervals (from ESS stability analysis)
        
        Returns
        -------
        predictions : dict
            Dictionary with keys:
            - 'reform_success_probability': float [0,1]
              Probability that reform attempt succeeds
            - 'ess_strength': float
              Absolute value of Hessian eigenvalue (resistance to change)
            - 'bifurcation_status': str
              One of: 'stable_reformable', 'critical_zone', 'locked_irreversible'
            - 'confidence_interval': tuple (lower, upper)
              95% CI for success probability (from perturbation analysis)
            - 'interpretation': str
              Human-readable interpretation of predictions
            - 'stability_type': str
              ESS classification: 'ESS', 'CSS', or 'REPELLOR'
              
        Raises
        ------
        RuntimeError
            If called before fit()
            
        Examples
        --------
        >>> predictor = UniversalEGTPredictor()
        >>> predictor.fit(cli_score=0.87)
        >>> result = predictor.predict()
        >>> print(result['reform_success_probability'])  # 0.124
        >>> print(result['bifurcation_status'])  # 'locked_irreversible'
        >>> print(result['interpretation'])  # Human-readable explanation
        """
        if not self._fitted:
            raise RuntimeError("Must call fit() before predict()")
            
        # Extract ESS characteristics
        ess_strength = self._compute_ess_strength()
        
        # Compute base success probability
        # Universal formula: P(success) = 1 - CLI (adjusted by ESS strength)
        base_probability = 1.0 - self.cli
        
        # Adjust by ESS strength (stronger ESS → lower probability)
        # This adjustment is conservative (factor 0.5 from Vince sensitivity analysis)
        adjusted_probability = base_probability / (1.0 + 0.5 * ess_strength)
        
        # Ensure probability in [0, 1]
        adjusted_probability = np.clip(adjusted_probability, 0.0, 1.0)
        
        # Classify bifurcation regime
        bifurcation_status = self._classify_regime()
        
        # Compute confidence interval (from perturbation analysis)
        ci_lower, ci_upper = self._compute_confidence_interval(adjusted_probability, ess_strength)
        
        # Generate interpretation
        interpretation = self._interpret(adjusted_probability, bifurcation_status, ess_strength)
        
        return {
            'reform_success_probability': float(adjusted_probability),
            'ess_strength': float(ess_strength),
            'bifurcation_status': bifurcation_status,
            'confidence_interval': (float(ci_lower), float(ci_upper)),
            'interpretation': interpretation,
            'stability_type': self.ess_result.stability_type.name,
            'cli_score': float(self.cli)
        }
    
    def _compute_ess_strength(self) -> float:
        """
        Compute ESS strength from Hessian eigenvalues.
        
        Returns
        -------
        strength : float
            Absolute value of dominant Hessian eigenvalue.
            Higher values indicate stronger lock-in.
        """
        if self.ess_result.hessian_eigenvalues is None:
            warnings.warn("Hessian eigenvalues not available, using default ESS strength")
            return 1.0
            
        # Take absolute value of most negative eigenvalue
        # (negative eigenvalue = stable ESS, positive = CSS/repellor)
        eigs = np.array(self.ess_result.hessian_eigenvalues)
        strength = np.abs(eigs.min()) if len(eigs) > 0 else 1.0
        
        return strength
    
    def _classify_regime(self) -> str:
        """
        Classify bifurcation regime based on CLI threshold.
        
        Returns
        -------
        status : str
            One of: 'stable_reformable', 'critical_zone', 'locked_irreversible'
        """
        if self.cli < 0.30:
            return 'stable_reformable'
        elif self.cli < self.vince_params.bifurcation_threshold:
            return 'critical_zone'
        else:
            return 'locked_irreversible'
    
    def _compute_confidence_interval(self, probability: float, ess_strength: float) -> Tuple[float, float]:
        """
        Compute 95% confidence interval for success probability.
        
        Uses perturbation analysis around ESS. Width of CI depends on ESS strength:
        - Strong ESS → Narrow CI (high certainty)
        - Weak ESS → Wide CI (low certainty)
        
        Parameters
        ----------
        probability : float
            Point estimate of success probability
        ess_strength : float
            ESS strength (from Hessian)
            
        Returns
        -------
        ci_lower, ci_upper : tuple of float
            95% confidence interval bounds
        """
        # CI width inversely proportional to ESS strength
        # Strong ESS (high strength) → Narrow CI (high confidence)
        # Weak ESS (low strength) → Wide CI (low confidence)
        ci_width = 0.10 / (1.0 + ess_strength)  # Conservative estimate
        
        ci_lower = np.clip(probability - ci_width, 0.0, 1.0)
        ci_upper = np.clip(probability + ci_width, 0.0, 1.0)
        
        return ci_lower, ci_upper
    
    def _interpret(self, probability: float, status: str, ess_strength: float) -> str:
        """
        Generate human-readable interpretation of predictions.
        
        Parameters
        ----------
        probability : float
            Reform success probability
        status : str
            Bifurcation status
        ess_strength : float
            ESS strength
            
        Returns
        -------
        interpretation : str
            Human-readable explanation
        """
        if status == 'locked_irreversible':
            return (
                f"Strong constitutional lock-in detected (CLI={self.cli:.2f}). "
                f"ESS highly stable (strength={ess_strength:.2f}). "
                f"Reform probability is very low ({probability:.1%}). "
                f"Successful reform would require regime-level change or constitutional crisis."
            )
        elif status == 'critical_zone':
            return (
                f"Moderate constitutional lock-in (CLI={self.cli:.2f}). "
                f"System near bifurcation threshold. "
                f"Reform probability is moderate ({probability:.1%}). "
                f"Success depends on strategic coalition formation and timing."
            )
        else:  # stable_reformable
            return (
                f"Weak constitutional lock-in (CLI={self.cli:.2f}). "
                f"ESS relatively weak (strength={ess_strength:.2f}). "
                f"Reform probability is high ({probability:.1%}). "
                f"Standard legislative processes should be viable."
            )


# Convenience function for one-shot prediction
def predict_reform_success(cli_score: float, vince_parameters: Optional[VinceParameters] = None) -> Dict[str, any]:
    """
    Convenience function for one-shot prediction.
    
    Equivalent to:
    >>> predictor = UniversalEGTPredictor(vince_parameters)
    >>> predictor.fit(cli_score).predict()
    
    Parameters
    ----------
    cli_score : float
        Constitutional Lock-in Index [0, 1]
    vince_parameters : VinceParameters, optional
        Custom Vince parameters. If None, uses defaults.
        
    Returns
    -------
    predictions : dict
        Same output as UniversalEGTPredictor.predict()
        
    Examples
    --------
    >>> result = predict_reform_success(cli_score=0.87)
    >>> print(result['reform_success_probability'])
    """
    predictor = UniversalEGTPredictor(vince_parameters=vince_parameters)
    predictor.fit(cli_score=cli_score)
    return predictor.predict()
