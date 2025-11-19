"""
G-Function (Fitness-Generating Function) Implementation
========================================================

Implements the core G-function framework from Vince (2005), Chapter 4.

The G-function G(v, u, x) defines the per capita growth rate (fitness) of an 
individual with virtual strategy v in a population with resident strategies u 
at densities x.

Mathematical Definition:
------------------------
G(v, u, x)|_{v=u_i} = H_i(u, x)  # Individual fitness for species i

where:
- v: Virtual strategy (focal individual, mutant/invader)
- u: Vector of resident strategies [u_1, ..., u_ns]
- x: Vector of population densities [x_1, ..., x_ns]
- H_i: Per capita growth rate of species i

Key Properties (Theorem 4.3.1):
--------------------------------
1. G is continuous in all arguments
2. ∂G/∂v exists and is continuous
3. Homogeneity: G(v, u, λx) = G(v, u, x) for all λ > 0 (density-based)
   OR G(v, u, p, λN) = G(v, u, p, N) (frequency-based)

Three Formulations:
-------------------
1. Density-based: G(v, u, x)
   - Used for population dynamics: dx_i/dt = x_i * H_i(u, x)
   - ESS condition: G(v, u, x*)|_{v=u_i} = 0

2. Frequency-based: G(v, u, p, N)
   - Used for frequency dynamics: dp_i/dt = p_i * [G|_{v=u_i} - G_avg]
   - Preferred for matrix games
   - p_i = x_i / N, N = sum(x_i)

3. Resource-explicit: G(v, u, R)
   - Explicit resource dynamics: dR/dt = f(R, u, x)
   - Mechanistic consumer-resource models

References:
-----------
Vince (2005), Chapter 4: "Darwinian Dynamics and the G-Function"
Vince (2005), Chapter 9: "Matrix Games and Frequency Dependence"
"""

import numpy as np
from typing import Callable, Optional, Union, Tuple, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
import warnings


@dataclass
class GFunctionParams:
    """
    Parameters for G-function construction.
    
    Attributes
    ----------
    r : float
        Intrinsic growth rate (time^-1)
    K_max : float
        Maximum carrying capacity (density units)
    sigma_k : float
        Resource niche width (strategy units)
    sigma_alpha : float
        Competition niche width (strategy units)
    beta : float
        Asymmetry parameter for competition (dimensionless)
    """
    r: float = 0.25
    K_max: float = 100.0
    sigma_k: float = 2.0
    sigma_alpha: float = 2.0
    beta: float = 0.0  # Beta=0 → symmetric competition (no frequency dependence)
    
    def validate(self) -> None:
        """Validate parameter ranges."""
        if self.r <= 0:
            raise ValueError("r (growth rate) must be positive")
        if self.K_max <= 0:
            raise ValueError("K_max (carrying capacity) must be positive")
        if self.sigma_k <= 0:
            raise ValueError("sigma_k (niche width) must be positive")
        if self.sigma_alpha <= 0:
            raise ValueError("sigma_alpha (competition width) must be positive")


class GFunction(ABC):
    """
    Abstract base class for G-function implementations.
    
    All G-functions must implement:
    1. evaluate(v, u, x) → fitness value
    2. gradient(v, u, x) → ∂G/∂v (for strategy dynamics)
    3. hessian(v, u, x) → ∂²G/∂v² (for ESS stability test)
    """
    
    def __init__(self, params: GFunctionParams):
        """
        Initialize G-function with parameters.
        
        Parameters
        ----------
        params : GFunctionParams
            Model parameters (r, K_max, sigma_k, etc.)
        """
        params.validate()
        self.params = params
        
    @abstractmethod
    def evaluate(self, v: np.ndarray, u: np.ndarray, x: np.ndarray) -> float:
        """
        Evaluate G(v, u, x).
        
        Parameters
        ----------
        v : np.ndarray
            Virtual strategy (focal individual)
        u : np.ndarray
            Resident strategies (ns x strategy_dim)
        x : np.ndarray
            Population densities (ns,)
            
        Returns
        -------
        float
            Per capita growth rate (fitness)
        """
        pass
    
    @abstractmethod
    def gradient(self, v: np.ndarray, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """
        Compute ∂G/∂v (selection gradient).
        
        This is the KEY quantity for strategy dynamics:
        du_i/dt = sigma_i^2 * ∂G/∂v|_{v=u_i}
        
        Parameters
        ----------
        v : np.ndarray
            Virtual strategy
        u : np.ndarray
            Resident strategies
        x : np.ndarray
            Population densities
            
        Returns
        -------
        np.ndarray
            Gradient vector (strategy_dim,)
        """
        pass
    
    @abstractmethod
    def hessian(self, v: np.ndarray, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """
        Compute ∂²G/∂v² (curvature matrix).
        
        This determines ESS stability (Invasion Resistance):
        - A = ∂²G/∂v² < 0 → ESS (peak, invasion resistant)
        - A > 0 → Minimum (valley, disruptive selection → speciation)
        
        Parameters
        ----------
        v : np.ndarray
            Virtual strategy
        u : np.ndarray
            Resident strategies
        x : np.ndarray
            Population densities
            
        Returns
        -------
        np.ndarray
            Hessian matrix (strategy_dim x strategy_dim)
        """
        pass
    
    def ecological_equilibrium(self, u: np.ndarray, 
                              x0: Optional[np.ndarray] = None,
                              tol: float = 1e-6,
                              max_iter: int = 1000) -> np.ndarray:
        """
        Find Ecologically Stable Equilibrium (ESE) x* for given strategies u.
        
        Solves: dx_i/dt = x_i * G(u_i, u, x) = 0
        
        This is the fast timescale (T_eco) that reaches equilibrium before
        strategies evolve (T_evo >> T_eco).
        
        Parameters
        ----------
        u : np.ndarray
            Resident strategies
        x0 : np.ndarray, optional
            Initial guess for population densities
        tol : float
            Convergence tolerance
        max_iter : int
            Maximum iterations
            
        Returns
        -------
        np.ndarray
            Equilibrium densities x*
        """
        ns = len(u)
        if x0 is None:
            x0 = np.ones(ns) * self.params.K_max / ns
        
        x = x0.copy()
        for iteration in range(max_iter):
            # Compute fitness for each species
            H = np.array([self.evaluate(u[i], u, x) for i in range(ns)])
            
            # Update population densities (implicit Euler)
            x_new = x * np.exp(H * 0.01)  # Small time step
            
            # Check convergence
            if np.allclose(x_new, x, rtol=tol, atol=tol):
                return x_new
            
            x = x_new
            
            # Remove extinct species (x < epsilon)
            x[x < 1e-8] = 0
        
        warnings.warn(f"Ecological equilibrium did not converge after {max_iter} iterations")
        return x


class ScalarGFunction(GFunction):
    """
    Scalar strategy G-function for single-trait models.
    
    Implements Lotka-Volterra competition model (Example 4.1.1, Vince 2005):
    
    G(v, u, x) = r * [K(v) - sum_j x_j * a(v, u_j)] / K(v)
    
    where:
    - K(v) = K_max * exp(-v²/(2*sigma_k²))  # Carrying capacity
    - a(v, u_j) = exp(-(v - u_j - beta)²/(2*sigma_alpha²))  # Competition coefficient
    
    Key insight: beta ≠ 0 introduces asymmetry → frequency-dependent selection
    """
    
    def __init__(self, params: GFunctionParams):
        super().__init__(params)
    
    def K(self, v: float) -> float:
        """Carrying capacity as function of strategy."""
        return self.params.K_max * np.exp(-v**2 / (2 * self.params.sigma_k**2))
    
    def dK_dv(self, v: float) -> float:
        """Derivative of K with respect to v."""
        return -v / self.params.sigma_k**2 * self.K(v)
    
    def d2K_dv2(self, v: float) -> float:
        """Second derivative of K with respect to v."""
        sigma_k2 = self.params.sigma_k**2
        return (v**2 / sigma_k2**2 - 1 / sigma_k2) * self.K(v)
    
    def a(self, v: float, u_j: float) -> float:
        """Competition coefficient between strategies v and u_j."""
        return np.exp(-(v - u_j - self.params.beta)**2 / (2 * self.params.sigma_alpha**2))
    
    def da_dv(self, v: float, u_j: float) -> float:
        """Derivative of competition coefficient."""
        return -(v - u_j - self.params.beta) / self.params.sigma_alpha**2 * self.a(v, u_j)
    
    def d2a_dv2(self, v: float, u_j: float) -> float:
        """Second derivative of competition coefficient."""
        sigma_a2 = self.params.sigma_alpha**2
        diff = v - u_j - self.params.beta
        return ((diff**2 / sigma_a2**2 - 1 / sigma_a2) * self.a(v, u_j))
    
    def evaluate(self, v: Union[float, np.ndarray], 
                 u: np.ndarray, 
                 x: np.ndarray) -> float:
        """
        Evaluate G(v, u, x) for scalar strategy.
        
        G = r * [K(v) - sum_j x_j * a(v, u_j)] / K(v)
        """
        if isinstance(v, np.ndarray):
            v = float(v[0]) if v.size == 1 else v
        
        K_v = self.K(v)
        if K_v < 1e-12:
            return -np.inf  # Strategy v is not viable
        
        competition = np.sum([x[j] * self.a(v, u[j]) for j in range(len(u))])
        
        return self.params.r * (K_v - competition) / K_v
    
    def gradient(self, v: Union[float, np.ndarray], 
                 u: np.ndarray, 
                 x: np.ndarray) -> np.ndarray:
        """
        Compute ∂G/∂v.
        
        ∂G/∂v = r * [dK/dv * sum_j x_j * a(v,u_j) - K * sum_j x_j * da/dv] / K²
        """
        if isinstance(v, np.ndarray):
            v = float(v[0]) if v.size == 1 else v
        
        K_v = self.K(v)
        dK_v = self.dK_dv(v)
        
        sum_a = np.sum([x[j] * self.a(v, u[j]) for j in range(len(u))])
        sum_da = np.sum([x[j] * self.da_dv(v, u[j]) for j in range(len(u))])
        
        grad = self.params.r * (dK_v * sum_a - K_v * sum_da) / (K_v**2)
        
        return np.array([grad])
    
    def hessian(self, v: Union[float, np.ndarray], 
                u: np.ndarray, 
                x: np.ndarray) -> np.ndarray:
        """
        Compute ∂²G/∂v².
        
        This is the KEY test for ESS stability:
        - A < 0 → ESS (peak)
        - A > 0 → Minimum (valley → speciation)
        """
        if isinstance(v, np.ndarray):
            v = float(v[0]) if v.size == 1 else v
        
        K_v = self.K(v)
        dK_v = self.dK_dv(v)
        d2K_v = self.d2K_dv2(v)
        
        sum_a = np.sum([x[j] * self.a(v, u[j]) for j in range(len(u))])
        sum_da = np.sum([x[j] * self.da_dv(v, u[j]) for j in range(len(u))])
        sum_d2a = np.sum([x[j] * self.d2a_dv2(v, u[j]) for j in range(len(u))])
        
        # Product rule + chain rule (derived in Vince Ch 7)
        numerator = (d2K_v * sum_a + 2 * dK_v * sum_da - 
                    K_v * sum_d2a) * K_v**2 - 2 * K_v * dK_v * (dK_v * sum_a - K_v * sum_da)
        
        hess = self.params.r * numerator / (K_v**4)
        
        return np.array([[hess]])


class FrequencyGFunction(ScalarGFunction):
    """
    Frequency-based G-function: G(v, u, p, N).
    
    Preferred for matrix games and systems where fitness depends on 
    strategy FREQUENCY rather than absolute density.
    
    Frequency dynamics:
    dp_i/dt = p_i * [G(u_i, u, p, N) - G_avg]
    
    where G_avg = sum_i p_i * G(u_i, u, p, N)
    
    Note: In Matrix-ESS (Theorem 9.1.2), the ESS fitness is NOT zero,
    but equals G_avg: G(u_i, u*, p*, N) = p* E(u*) p*^T
    """
    
    def __init__(self, params: GFunctionParams):
        super().__init__(params)
    
    def evaluate_frequency(self, v: float, u: np.ndarray, 
                          p: np.ndarray, N: float) -> float:
        """
        Evaluate G(v, u, p, N) in frequency formulation.
        
        Parameters
        ----------
        v : float
            Virtual strategy
        u : np.ndarray
            Resident strategies
        p : np.ndarray
            Frequencies (sum to 1)
        N : float
            Total population size
            
        Returns
        -------
        float
            Per capita growth rate
        """
        # Convert frequencies to densities
        x = p * N
        
        # Use density-based G-function
        return super().evaluate(v, u, x)
    
    def average_fitness(self, u: np.ndarray, p: np.ndarray, N: float) -> float:
        """
        Compute average fitness G_avg = sum_i p_i * G(u_i, u, p, N).
        
        In frequency dynamics, dp_i/dt ∝ [G_i - G_avg].
        """
        return np.sum([p[i] * self.evaluate_frequency(u[i], u, p, N) 
                      for i in range(len(u))])


class LotkaVolterraGFunction(ScalarGFunction):
    """
    Classic Lotka-Volterra G-function for constitutional law evolution.
    
    This is the primary model for Constitutional Lock-in analysis.
    
    LEGAL INTERPRETATION:
    ---------------------
    - Strategy v: Doctrinal rigidity (0 = flexible, high = rigid)
    - K(v): Carrying capacity = maximum sustainable doctrine strength
    - a(v, u_j): Competition = how much reform v conflicts with doctrine u_j
    - beta: Asymmetry = advantage/disadvantage of being different from incumbent
    
    When beta = 0:
        Symmetric competition → ESS at v* where K(v) is maximized
        
    When beta ≠ 0:
        Asymmetric competition → frequency-dependent selection
        Possible outcomes: ESS shift, coexistence (coalition), or speciation
    
    CLI CONNECTION:
    ---------------
    High CLI → Large sigma_k (wide resource niche) → Single ESS (lock-in)
    Low CLI → Small sigma_k (narrow niche) → Multiple ESS (doctrinal pluralism)
    """
    
    def __init__(self, params: GFunctionParams, cli_score: float):
        """
        Initialize L-V G-function with CLI integration.
        
        Parameters
        ----------
        params : GFunctionParams
            Base parameters
        cli_score : float
            Constitutional Lock-in Index (0-1 scale)
            Maps to sigma_k via bifurcation analysis
        """
        super().__init__(params)
        self.cli_score = cli_score
        
        # Map CLI to niche width (HYPOTHESIS - requires empirical validation)
        # High CLI → narrow niche → speciation pressure
        # Low CLI → wide niche → single ESS
        self.params.sigma_k = self._cli_to_sigma_k(cli_score)
    
    def _cli_to_sigma_k(self, cli: float) -> float:
        """
        Map CLI score to resource niche width.
        
        CONSERVATIVE MAPPING (no speculative coefficients):
        - Use inverse relationship: high CLI → low sigma_k
        - Normalized to sigma_k ∈ [0.5, 4.0] based on Vince Example 5.4.1
        
        Parameters
        ----------
        cli : float
            CLI score (0-1)
            
        Returns
        -------
        float
            Niche width sigma_k
        """
        # Linear inverse mapping (PROVEN SAFE, not optimal)
        sigma_min = 0.5
        sigma_max = 4.0
        
        # High CLI (0.87 Argentina) → Low sigma_k (0.5) → High competition → Speciation
        # Low CLI (0.15 Chile) → High sigma_k (4.0) → Low competition → Single ESS
        sigma_k = sigma_max - cli * (sigma_max - sigma_min)
        
        return sigma_k
    
    def cli_to_bifurcation_parameter(self) -> Dict[str, float]:
        """
        Return bifurcation-relevant parameters derived from CLI.
        
        Returns
        -------
        dict
            Bifurcation parameters for analysis
        """
        return {
            'cli_score': self.cli_score,
            'sigma_k': self.params.sigma_k,
            'sigma_alpha': self.params.sigma_alpha,
            'beta': self.params.beta,
            'K_max': self.params.K_max,
        }


# Export main classes
__all__ = [
    'GFunction',
    'GFunctionParams',
    'ScalarGFunction',
    'FrequencyGFunction',
    'LotkaVolterraGFunction',
]
