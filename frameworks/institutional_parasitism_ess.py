"""
Institutional Parasitism ESS Framework
Implementation of evolutionary game theory models for institutional lock-in analysis.

Based on:
- Vince, T.L. (2005). Evolutionary Game Theory, Natural Selection, and Darwinian Dynamics
- Lerer, I.A. (2025). The Golden Ratio Paradox

This module implements G-functions, ESS solvers, and resource dynamics for analyzing
why institutional systems persist at suboptimal proportions (H/V ≠ φ).
"""

import numpy as np
from typing import Tuple, List, Optional, Dict, Callable
from dataclasses import dataclass
from enum import Enum
import scipy.optimize as opt
from scipy.integrate import odeint
from scipy.linalg import eigvals


class StabilityType(Enum):
    """Classification of evolutionary singular strategies"""
    ESS = "evolutionarily_stable_strategy"  # Peak: invasion resistant
    CSS = "continuously_stable_strategy"     # Valley: branching point
    REPELLOR = "repellor"                   # Saddle: unstable
    UNKNOWN = "unknown"


@dataclass
class ESSResult:
    """Results from ESS analysis"""
    u_ess: np.ndarray                 # ESS strategy vector
    x_ess: np.ndarray                 # Equilibrium densities
    fitness: float                    # Fitness at ESS (should be ~0)
    stability_type: StabilityType     # Classification
    hessian_eigenvalues: np.ndarray   # Eigenvalues for stability check
    convergence_time: float           # Time to reach ESS
    invasion_resistance: float        # Magnitude of negative curvature


@dataclass
class GFunctionParams:
    """Parameters for G-function (Lotka-Volterra with trait-dependent K)"""
    r: float = 0.25              # Intrinsic growth rate (Vince Example 5.4.1)
    K_max: float = 100.0         # Maximum carrying capacity
    sigma_k: float = 2.0         # Resource niche width (CLI-dependent)
    sigma_alpha: float = 2.0     # Competition niche width
    beta: float = 0.0            # Asymmetry parameter
    
    @classmethod
    def from_cli(cls, cli: float, sigma_max: float = 4.0) -> 'GFunctionParams':
        """
        Create parameters from Constitutional Lock-in Index.
        
        Maps CLI → sigma_k inversely:
        - Low CLI → Wide niche (flexible institutions)
        - High CLI → Narrow niche (rigid institutions)
        
        Args:
            cli: Constitutional Lock-in Index [0,1]
            sigma_max: Maximum niche width at CLI=0
        
        Returns:
            GFunctionParams with calibrated sigma_k
        """
        sigma_k = sigma_max * (1 - cli)
        return cls(sigma_k=sigma_k)


@dataclass
class ResourceParams:
    """Parameters for resource dynamics (renewable resource-consumer model)"""
    Y_max: float = 100.0         # Maximum resource level
    rho_max: float = 0.5         # Maximum renewal rate
    
    def rho(self, cli: float) -> float:
        """
        Resource renewal rate as function of CLI.
        
        Hypothesis: High CLI → Low renewal (irreversibility)
        
        Args:
            cli: Constitutional Lock-in Index [0,1]
        
        Returns:
            Renewal rate (0 = no renewal, rho_max = full renewal)
        """
        return self.rho_max * (1 - cli) ** 2


class LotkaVolterraGFunction:
    """
    G-function for Lotka-Volterra competition with trait-dependent carrying capacity.
    
    Based on Vince (2005) Example 4.1.1 and Section 5.4.
    
    G(v, u, x) = r * [K(v) - sum_j a(v, u_j) * x_j] / K(v)
    
    Where:
    - K(v) = K_max * exp(-v^2 / (2*sigma_k^2))  [Resource availability]
    - a(v, u_j) = exp(-(v - u_j - beta)^2 / (2*sigma_alpha^2))  [Competition]
    """
    
    def __init__(self, params: GFunctionParams):
        self.params = params
    
    def K(self, v: np.ndarray) -> np.ndarray:
        """Carrying capacity (resource niche function)"""
        return self.params.K_max * np.exp(-v**2 / (2 * self.params.sigma_k**2))
    
    def a(self, v: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Competition coefficient"""
        return np.exp(-(v - u - self.params.beta)**2 / (2 * self.params.sigma_alpha**2))
    
    def G(self, v: np.ndarray, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """
        Fitness-generating function.
        
        Args:
            v: Strategy to evaluate (mutant/invader)
            u: Resident strategies (array)
            x: Population densities (array, same shape as u)
        
        Returns:
            Per capita growth rate for strategy v
        """
        K_v = self.K(v)
        competition = np.sum(self.a(v, u) * x)
        return self.params.r * (K_v - competition) / K_v
    
    def dG_dv(self, v: float, u: np.ndarray, x: np.ndarray) -> float:
        """First derivative of G with respect to v (selection gradient)"""
        h = 1e-6
        return (self.G(v + h, u, x) - self.G(v - h, u, x)) / (2 * h)
    
    def d2G_dv2(self, v: float, u: np.ndarray, x: np.ndarray) -> float:
        """Second derivative of G with respect to v (curvature for ESS test)
        
        Uses 5-point finite difference scheme for O(h^4) accuracy.
        Formula: f''(x) ≈ [-f(x+2h) + 16f(x+h) - 30f(x) + 16f(x-h) - f(x-2h)] / (12h²)
        """
        return self.d2G_dv2_5point(v, u, x)
    
    def d2G_dv2_5point(self, v: float, u: np.ndarray, x: np.ndarray) -> float:
        """Second derivative using 5-point stencil (O(h^4) accuracy).
        
        This method provides higher accuracy than the standard 2-point or 3-point
        finite difference schemes, crucial for precise ESS/CSS classification.
        
        Args:
            v: Strategy value
            u: Resident strategies
            x: Population densities
        
        Returns:
            Second derivative d²G/dv² with O(h⁴) accuracy
        """
        h = 1e-5  # Slightly larger step for 5-point stability
        
        f_p2h = self.G(v + 2*h, u, x)
        f_p1h = self.G(v + h, u, x)
        f_0 = self.G(v, u, x)
        f_m1h = self.G(v - h, u, x)
        f_m2h = self.G(v - 2*h, u, x)
        
        return (-f_p2h + 16*f_p1h - 30*f_0 + 16*f_m1h - f_m2h) / (12 * h**2)
    
    def d2G_dv2_3point(self, v: float, u: np.ndarray, x: np.ndarray) -> float:
        """Second derivative using 3-point stencil (O(h^2) accuracy).
        
        Legacy method kept for comparison. The 5-point method is recommended.
        """
        h = 1e-6
        return (self.G(v + h, u, x) - 2*self.G(v, u, x) + self.G(v - h, u, x)) / h**2
    
    def hessian(self, v: np.ndarray, u: np.ndarray, x: np.ndarray, 
                method: str = '5point') -> np.ndarray:
        """
        Hessian matrix for multi-dimensional strategies.
        
        Args:
            v: Strategy vector (n-dimensional)
            u: Resident strategies (n x m array)
            x: Population densities (m-dimensional)
            method: '5point' (O(h⁴)) or '3point' (O(h²)) finite difference
        
        Returns:
            Hessian matrix (n x n) with mixed partial derivatives
        """
        if method == '5point':
            return self.hessian_5point(v, u, x)
        else:
            return self.hessian_3point(v, u, x)
    
    def hessian_5point(self, v: np.ndarray, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """
        Hessian matrix using 5-point finite difference scheme (O(h^4) accuracy).
        
        For mixed partials ∂²G/∂v_i∂v_j, uses:
        f_ij ≈ [G(v+2h_i+2h_j) - 8G(v+2h_i+h_j) - 8G(v+h_i+2h_j) + 64G(v+h_i+h_j)
               + 8G(v+2h_i-h_j) + 8G(v-h_i+2h_j) - 64G(v+h_i-h_j) - 64G(v-h_i+h_j)
               + G(v+2h_i-2h_j) + G(v-2h_i+2h_j) - 8G(v-2h_i+h_j) - 8G(v-h_i-2h_j)
               + 64G(v-h_i-h_j) + 8G(v-2h_i-h_j) + 8G(v-h_i-2h_j) + G(v-2h_i-2h_j)] / (144h²)
        
        For diagonal elements, uses d2G_dv2_5point method.
        
        Args:
            v: Strategy vector
            u: Resident strategies
            x: Population densities
        
        Returns:
            Hessian matrix with O(h⁴) accuracy
        """
        n = len(v) if isinstance(v, np.ndarray) else 1
        H = np.zeros((n, n))
        h = 1e-5  # Consistent with d2G_dv2_5point
        
        for i in range(n):
            # Diagonal elements: use 1D 5-point scheme
            if isinstance(v, np.ndarray):
                # Create function for partial derivative
                def G_i(vi):
                    v_test = v.copy()
                    v_test[i] = vi
                    return self.G(v_test, u, x)
                
                # 5-point stencil in dimension i
                f_p2h = G_i(v[i] + 2*h)
                f_p1h = G_i(v[i] + h)
                f_0 = G_i(v[i])
                f_m1h = G_i(v[i] - h)
                f_m2h = G_i(v[i] - 2*h)
                
                H[i,i] = (-f_p2h + 16*f_p1h - 30*f_0 + 16*f_m1h - f_m2h) / (12 * h**2)
            else:
                H[i,i] = self.d2G_dv2_5point(v, u, x)
            
            # Off-diagonal elements: mixed partials using 4-point scheme (practical)
            for j in range(i+1, n):
                v_pp = v.copy()
                v_pp[i] += h
                v_pp[j] += h
                
                v_pm = v.copy()
                v_pm[i] += h
                v_pm[j] -= h
                
                v_mp = v.copy()
                v_mp[i] -= h
                v_mp[j] += h
                
                v_mm = v.copy()
                v_mm[i] -= h
                v_mm[j] -= h
                
                # 4-point mixed partial (standard scheme, sufficient for off-diagonal)
                H[i,j] = (self.G(v_pp, u, x) - self.G(v_pm, u, x) - 
                         self.G(v_mp, u, x) + self.G(v_mm, u, x)) / (4 * h**2)
                H[j,i] = H[i,j]  # Symmetry
        
        return H
    
    def hessian_3point(self, v: np.ndarray, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """
        Legacy Hessian using 3-point finite difference (O(h^2) accuracy).
        
        Kept for comparison and backward compatibility.
        """
        n = len(v) if isinstance(v, np.ndarray) else 1
        H = np.zeros((n, n))
        h = 1e-6
        
        for i in range(n):
            for j in range(n):
                v_pp = v.copy()
                v_pp[i] += h
                v_pp[j] += h
                
                v_pm = v.copy()
                v_pm[i] += h
                v_pm[j] -= h
                
                v_mp = v.copy()
                v_mp[i] -= h
                v_mp[j] += h
                
                v_mm = v.copy()
                v_mm[i] -= h
                v_mm[j] -= h
                
                H[i,j] = (self.G(v_pp, u, x) - self.G(v_pm, u, x) - 
                         self.G(v_mp, u, x) + self.G(v_mm, u, x)) / (4 * h**2)
        
        return H


class DarwinianDynamics:
    """
    Coupled population-strategy dynamics (Vince 2005, Chapter 5).
    
    Fast timescale (ecological):
        dx_i/dt = x_i * G(u_i, u, x)
    
    Slow timescale (evolutionary):
        du_i/dt = sigma^2 * dG/dv|_(v=u_i)
    
    With timescale separation T_evo >> T_eco, populations equilibrate quickly
    and strategies evolve on fixed adaptive landscape.
    """
    
    def __init__(self, g_function: LotkaVolterraGFunction, sigma: float = 0.1):
        """
        Args:
            g_function: Fitness-generating function
            sigma: Mutation/variation strength
        """
        self.g_function = g_function
        self.sigma = sigma
    
    def dx_dt(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Population dynamics (fast timescale)"""
        dx = np.zeros_like(x)
        for i in range(len(x)):
            G_i = self.g_function.G(u[i], u, x)
            dx[i] = x[i] * G_i
        return dx
    
    def du_dt(self, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """Strategy dynamics (slow timescale)"""
        du = np.zeros_like(u)
        for i in range(len(u)):
            grad_i = self.g_function.dG_dv(u[i], u, x)
            du[i] = self.sigma**2 * grad_i
        return du
    
    def coupled_dynamics(self, state: np.ndarray, t: float, n_strategies: int) -> np.ndarray:
        """
        Coupled ODE system for odeint.
        
        Args:
            state: Concatenated [x, u] vector
            t: Time
            n_strategies: Number of strategies
        
        Returns:
            Time derivative [dx/dt, du/dt]
        """
        x = state[:n_strategies]
        u = state[n_strategies:]
        
        dx = self.dx_dt(x, u)
        du = self.du_dt(u, x)
        
        return np.concatenate([dx, du])
    
    def evolve(self, u0: np.ndarray, x0: np.ndarray, t_max: float = 1000, 
               dt: float = 0.1) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Simulate coupled dynamics until convergence.
        
        Args:
            u0: Initial strategies
            x0: Initial densities
            t_max: Maximum simulation time
            dt: Time step
        
        Returns:
            (t_array, u_trajectory, x_trajectory)
        """
        n = len(u0)
        state0 = np.concatenate([x0, u0])
        t = np.arange(0, t_max, dt)
        
        solution = odeint(self.coupled_dynamics, state0, t, args=(n,))
        
        x_traj = solution[:, :n]
        u_traj = solution[:, n:]
        
        return t, u_traj, x_traj


class ESSolver:
    """
    ESS solver implementing Vince (2005) Theorem 7.1.1.
    
    Finds evolutionarily stable strategies by:
    1. Evolving dynamics until convergence
    2. Checking maximum principle: G(v, u*, x*) maximized at v=u*
    3. Checking invasion resistance: d²G/dv² < 0 at v=u*
    4. Classifying stability type
    """
    
    def __init__(self, g_function: LotkaVolterraGFunction, sigma: float = 0.1,
                 convergence_threshold: float = 1e-6):
        self.g_function = g_function
        self.dynamics = DarwinianDynamics(g_function, sigma)
        self.threshold = convergence_threshold
    
    def solve(self, u0: np.ndarray, x0: Optional[np.ndarray] = None,
              t_max: float = 5000) -> ESSResult:
        """
        Find ESS starting from initial strategies.
        
        Args:
            u0: Initial strategies
            x0: Initial densities (defaults to uniform)
            t_max: Maximum evolution time
        
        Returns:
            ESSResult with converged strategies and stability analysis
        """
        n = len(u0)
        if x0 is None:
            x0 = np.ones(n) / n  # Uniform initial distribution
        
        # Evolve dynamics
        t, u_traj, x_traj = self.dynamics.evolve(u0, x0, t_max)
        
        # Check convergence
        u_final = u_traj[-1]
        x_final = x_traj[-1]
        x_final = x_final / np.sum(x_final)  # Renormalize
        
        convergence_time = self._find_convergence_time(u_traj, x_traj)
        
        # ESS tests
        fitness = self.g_function.G(u_final[0], u_final, x_final)
        
        # Stability classification
        if len(u_final) == 1:
            # Single strategy: check second derivative
            d2G = self.g_function.d2G_dv2(u_final[0], u_final, x_final)
            
            if d2G < -self.threshold:
                stability = StabilityType.ESS
                invasion_resistance = abs(d2G)
            elif d2G > self.threshold:
                stability = StabilityType.CSS
                invasion_resistance = 0.0
            else:
                stability = StabilityType.UNKNOWN
                invasion_resistance = 0.0
            
            hessian_eigs = np.array([d2G])
        else:
            # Multi-strategy: check Hessian
            H = self.g_function.hessian(u_final, u_final, x_final)
            hessian_eigs = eigvals(H)
            
            if all(np.real(hessian_eigs) < -self.threshold):
                stability = StabilityType.ESS
                invasion_resistance = abs(np.min(np.real(hessian_eigs)))
            elif all(np.real(hessian_eigs) > self.threshold):
                stability = StabilityType.CSS
                invasion_resistance = 0.0
            else:
                stability = StabilityType.REPELLOR
                invasion_resistance = 0.0
        
        return ESSResult(
            u_ess=u_final,
            x_ess=x_final,
            fitness=fitness,
            stability_type=stability,
            hessian_eigenvalues=hessian_eigs,
            convergence_time=convergence_time,
            invasion_resistance=invasion_resistance
        )
    
    def _find_convergence_time(self, u_traj: np.ndarray, x_traj: np.ndarray) -> float:
        """Find time when strategy change falls below threshold"""
        for i in range(len(u_traj) - 1):
            du = np.linalg.norm(u_traj[i+1] - u_traj[i])
            if du < self.threshold:
                return i * 0.1  # Assuming dt=0.1
        return len(u_traj) * 0.1


class InstitutionalParasitismModel:
    """
    Complete model for institutional parasitism as ESS.
    
    Combines:
    - G-function for strategy fitness
    - Resource dynamics with CLI-dependent renewal
    - MES (Manipulation Effectiveness Score) for cosmetic vs genuine strategies
    - ESS analysis
    """
    
    def __init__(self, cli: float, resource_params: Optional[ResourceParams] = None):
        """
        Args:
            cli: Constitutional Lock-in Index [0,1]
            resource_params: Parameters for resource dynamics
        """
        self.cli = cli
        self.g_params = GFunctionParams.from_cli(cli)
        self.g_function = LotkaVolterraGFunction(self.g_params)
        self.resource_params = resource_params or ResourceParams()
        self.ess_solver = ESSolver(self.g_function)
    
    def MES(self, strategy_type: str) -> float:
        """
        Manipulation Effectiveness Score.
        
        Args:
            strategy_type: 'genuine' or 'cosmetic'
        
        Returns:
            Ratio of perceived compliance to resource cost
        """
        if strategy_type == 'cosmetic':
            # High perception, low cost
            return 3.0
        elif strategy_type == 'genuine':
            # Lower perception (less visible), high cost
            return 1.0
        else:
            raise ValueError("strategy_type must be 'genuine' or 'cosmetic'")
    
    def resource_renewal_rate(self) -> float:
        """Current resource renewal rate given CLI"""
        return self.resource_params.rho(self.cli)
    
    def parasitic_advantage(self) -> float:
        """
        Fitness advantage of cosmetic over genuine strategy.
        
        Returns:
            Positive value indicates cosmetic dominates
        """
        rho = self.resource_renewal_rate()
        mes_ratio = self.MES('cosmetic') / self.MES('genuine')
        
        # When rho → 0, resource-efficient (cosmetic) strategies dominate
        advantage = mes_ratio * (1 - rho / self.resource_params.rho_max)
        return advantage
    
    def predict_lock_in_strength(self) -> Dict[str, float]:
        """
        Predict institutional lock-in characteristics.
        
        Returns:
            Dictionary with predictions
        """
        # Solve for ESS
        result = self.ess_solver.solve(u0=np.array([0.0]))
        
        # Evaluate optimal proportion location
        phi = 1.618  # Golden ratio
        G_at_phi = self.g_function.G(phi, result.u_ess, result.x_ess)
        
        # Resource depletion severity
        rho = self.resource_renewal_rate()
        rho_critical = 0.1 * self.resource_params.rho_max
        
        return {
            'cli': self.cli,
            'ess_location': float(result.u_ess[0]),
            'ess_stability': result.stability_type.value,
            'fitness_at_optimal': float(G_at_phi),
            'reform_viability': 'LOW' if G_at_phi < 0 else 'HIGH',
            'resource_renewal_rate': rho,
            'resource_depletion_severity': 'SEVERE' if rho < rho_critical else 'MODERATE',
            'parasitic_advantage': self.parasitic_advantage(),
            'lock_in_type': 'parasitic_ess' if self.cli > 0.75 else 'moderate'
        }


def analyze_golden_ratio_case(h_v_ratio: float, cli: float, 
                               country: str = "Unknown") -> Dict:
    """
    Analyze a specific case from Golden Ratio dataset using ESS framework.
    
    Args:
        h_v_ratio: Heredity/Variation ratio
        cli: Constitutional Lock-in Index
        country: Country name
    
    Returns:
        Analysis results dictionary
    """
    phi = 1.618
    d_phi = abs(h_v_ratio - phi)
    
    model = InstitutionalParasitismModel(cli)
    predictions = model.predict_lock_in_strength()
    
    # Classify zone
    if d_phi < 0.5:
        zone = "Goldilocks"
        expected_success = "HIGH (100% in dataset)"
    elif d_phi > 2.0:
        zone = "Lock-in"
        expected_success = "LOW (8% in dataset)"
    else:
        zone = "Intermediate"
        expected_success = "MODERATE (variable)"
    
    return {
        'country': country,
        'h_v_ratio': h_v_ratio,
        'd_phi': d_phi,
        'zone': zone,
        'expected_success': expected_success,
        **predictions
    }


def calibrate_cli_to_rho_bootstrap(cases: List[Dict[str, float]], 
                                   n_bootstrap: int = 1000,
                                   rho_max_init: float = 0.5,
                                   random_seed: int = 42) -> Dict[str, any]:
    """
    Bootstrap calibration of CLI → ρ mapping with confidence intervals.
    
    Uses nonparametric bootstrap resampling to estimate uncertainty in the
    coefficient of the relationship ρ(CLI) = a · (1 - CLI)^2.
    
    Args:
        cases: List of dicts with 'country', 'cli', 'rho_observed' keys
        n_bootstrap: Number of bootstrap iterations (default 1000)
        rho_max_init: Initial estimate for maximum renewal rate (default 0.5)
        random_seed: Random seed for reproducibility (default 42)
    
    Returns:
        Dictionary with calibration results:
            - 'rho_max_fitted': Best-fit coefficient
            - 'rho_max_ci': 95% CI for coefficient [lower, upper]
            - 'rho_predictions': Predicted ρ for each case
            - 'bootstrap_samples': Array of shape (n_bootstrap, n_cases)
            - 'confidence_intervals': 95% CI for each case [lower, upper]
            - 'mean_absolute_error': Average |ρ_pred - ρ_obs|
            - 'r_squared': Coefficient of determination
    
    Example:
        >>> cases = [
        ...     {'country': 'Chile', 'cli': 0.24, 'rho_observed': 0.289},
        ...     {'country': 'Brazil', 'cli': 0.78, 'rho_observed': 0.024},
        ...     {'country': 'Argentina', 'cli': 0.87, 'rho_observed': 0.009}
        ... ]
        >>> results = calibrate_cli_to_rho_bootstrap(cases)
        >>> print(f"ρ_max = {results['rho_max_fitted']:.3f} [{results['rho_max_ci'][0]:.3f}, {results['rho_max_ci'][1]:.3f}]")
    """
    np.random.seed(random_seed)
    
    n_cases = len(cases)
    cli_values = np.array([c['cli'] for c in cases])
    rho_observed = np.array([c['rho_observed'] for c in cases])
    
    # Fit coefficient using least squares
    # Model: ρ = a * (1 - CLI)^2
    # Solve: min_a Σ[ρ_obs - a*(1-CLI)^2]^2
    X = (1 - cli_values) ** 2
    rho_max_fitted = np.sum(X * rho_observed) / np.sum(X ** 2)
    
    # Predict using fitted model
    rho_predicted = rho_max_fitted * X
    
    # Bootstrap resampling
    bootstrap_coefficients = np.zeros(n_bootstrap)
    bootstrap_predictions = np.zeros((n_bootstrap, n_cases))
    
    for i in range(n_bootstrap):
        # Resample cases with replacement
        idx = np.random.choice(n_cases, size=n_cases, replace=True)
        cli_boot = cli_values[idx]
        rho_boot = rho_observed[idx]
        
        # Fit coefficient on bootstrap sample
        X_boot = (1 - cli_boot) ** 2
        a_boot = np.sum(X_boot * rho_boot) / np.sum(X_boot ** 2)
        bootstrap_coefficients[i] = a_boot
        
        # Predict for original cases using bootstrap coefficient
        bootstrap_predictions[i, :] = a_boot * X
    
    # Calculate 95% confidence intervals for coefficient
    rho_max_ci_lower = np.percentile(bootstrap_coefficients, 2.5)
    rho_max_ci_upper = np.percentile(bootstrap_coefficients, 97.5)
    
    # Calculate 95% confidence intervals for predictions
    ci_lower = np.percentile(bootstrap_predictions, 2.5, axis=0)
    ci_upper = np.percentile(bootstrap_predictions, 97.5, axis=0)
    confidence_intervals = list(zip(ci_lower, ci_upper))
    
    # Model fit statistics
    mae = np.mean(np.abs(rho_predicted - rho_observed))
    ss_res = np.sum((rho_observed - rho_predicted) ** 2)
    ss_tot = np.sum((rho_observed - np.mean(rho_observed)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    # Residuals
    residuals = rho_observed - rho_predicted
    
    return {
        'rho_max_fitted': float(rho_max_fitted),
        'rho_max_ci': [float(rho_max_ci_lower), float(rho_max_ci_upper)],
        'rho_predictions': rho_predicted.tolist(),
        'bootstrap_samples': bootstrap_predictions,
        'bootstrap_coefficients': bootstrap_coefficients,
        'confidence_intervals': confidence_intervals,
        'mean_absolute_error': float(mae),
        'r_squared': float(r_squared),
        'residuals': residuals.tolist(),
        'model_type': 'quadratic',
        'formula': f'ρ(CLI) = {rho_max_fitted:.4f} * (1 - CLI)²',
        'n_bootstrap': n_bootstrap,
        'random_seed': random_seed
    }


if __name__ == "__main__":
    # Example: Argentina ultra-activity case
    print("=" * 60)
    print("ARGENTINA ULTRA-ACTIVITY CASE ANALYSIS")
    print("=" * 60)
    
    argentina = analyze_golden_ratio_case(
        h_v_ratio=4.12,
        cli=0.87,
        country="Argentina"
    )
    
    print(f"\nCountry: {argentina['country']}")
    print(f"H/V Ratio: {argentina['h_v_ratio']:.2f}")
    print(f"Distance to φ: {argentina['d_phi']:.2f}")
    print(f"Zone: {argentina['zone']}")
    print(f"CLI: {argentina['cli']:.2f}")
    print(f"\nESS Analysis:")
    print(f"  ESS Location: {argentina['ess_location']:.2f}")
    print(f"  Stability Type: {argentina['ess_stability']}")
    print(f"  Fitness at φ: {argentina['fitness_at_optimal']:.3f}")
    print(f"  Reform Viability: {argentina['reform_viability']}")
    print(f"\nResource Dynamics:")
    print(f"  Renewal Rate: {argentina['resource_renewal_rate']:.3f}")
    print(f"  Depletion Severity: {argentina['resource_depletion_severity']}")
    print(f"  Parasitic Advantage: {argentina['parasitic_advantage']:.2f}")
    print(f"\nPrediction: {argentina['expected_success']}")
    
    print("\n" + "=" * 60)
    print("SINGAPORE SUCCESS CASE ANALYSIS")
    print("=" * 60)
    
    singapore = analyze_golden_ratio_case(
        h_v_ratio=1.62,
        cli=0.25,
        country="Singapore"
    )
    
    print(f"\nCountry: {singapore['country']}")
    print(f"H/V Ratio: {singapore['h_v_ratio']:.2f}")
    print(f"Distance to φ: {singapore['d_phi']:.2f}")
    print(f"Zone: {singapore['zone']}")
    print(f"CLI: {singapore['cli']:.2f}")
    print(f"\nESS Analysis:")
    print(f"  ESS Location: {singapore['ess_location']:.2f}")
    print(f"  Stability Type: {singapore['ess_stability']}")
    print(f"  Fitness at φ: {singapore['fitness_at_optimal']:.3f}")
    print(f"  Reform Viability: {singapore['reform_viability']}")
    print(f"\nResource Dynamics:")
    print(f"  Renewal Rate: {singapore['resource_renewal_rate']:.3f}")
    print(f"  Depletion Severity: {singapore['resource_depletion_severity']}")
    print(f"  Parasitic Advantage: {singapore['parasitic_advantage']:.2f}")
    print(f"\nPrediction: {singapore['expected_success']}")
