"""
Darwinian Dynamics: Coupled Population-Strategy Evolution
==========================================================

Implements the Darwinian Dynamics framework from Vince (2005), Chapter 5.

Core Concept:
-------------
Darwinian Dynamics couples TWO timescales:
1. FAST (Ecological): Population dynamics dx/dt = x * H(u, x)
2. SLOW (Evolutionary): Strategy dynamics du/dt = sigma² * ∂G/∂v|_{v=u}

Timescale Separation (T_evo >> T_eco):
--------------------------------------
The evolutionary timescale is MUCH SLOWER than ecological:
- Ecological equilibrium x* reached "instantly" (quasi-equilibrium assumption)
- Strategies u evolve slowly on the FIXED adaptive landscape G*(v) = G(v, u, x*)
- This separation allows ESS analysis via G* instead of coupled dynamics

Key Insight from Report 3:
---------------------------
"ESS immune to fast ecological chaos"
- Even if x(t) fluctuates chaotically at ecological timescale
- The ESS u* remains stable at evolutionary timescale
- Reforms (fast) cannot dislodge judicial ESS (slow)

This is CRITICAL for constitutional law:
- Legislative reforms happen FAST (months/years)
- Judicial doctrine evolves SLOW (decades/centuries)
- Lock-in emerges from timescale separation

Mathematical Framework:
-----------------------
Population Dynamics (Fast):
    dx_i/dt = x_i * H_i(u, x) = x_i * G(v, u, x)|_{v=u_i}
    
Strategy Dynamics (Slow):
    du_i/dt = sigma_i² * ∂G(v, u, x*)/∂v|_{v=u_i}
    
Quasi-Equilibrium:
    x ≈ x*(u) for all time (ecological equilibrium tracks strategy changes)

References:
-----------
Vince (2005), Chapter 5: "Darwinian Dynamics"
Vince (2005), Section 5.7: "Timescale Separation"
"""

import numpy as np
from typing import Callable, Optional, Tuple, List
from dataclasses import dataclass
import warnings

from .g_function import GFunction, GFunctionParams


@dataclass
class TimescaleParams:
    """
    Parameters controlling timescale separation.
    
    Attributes
    ----------
    sigma_sq : float or np.ndarray
        Evolutionary variance sigma² (determines strategy evolution rate)
        Units: strategy²/time
        
    tau_eco : float
        Ecological timescale (time to reach x*)
        Units: time
        
    tau_evo : float
        Evolutionary timescale (time for u to change significantly)
        Units: time
        
    separation_ratio : float
        Ratio tau_evo / tau_eco (should be >> 1 for separation)
        Vince suggests ratio > 10 for quasi-equilibrium assumption
    """
    sigma_sq: float = 1.0
    tau_eco: float = 10.0
    tau_evo: float = 1000.0
    
    @property
    def separation_ratio(self) -> float:
        """Compute timescale separation ratio."""
        return self.tau_evo / self.tau_eco
    
    def validate(self) -> None:
        """Validate timescale separation assumption."""
        if self.separation_ratio < 10:
            warnings.warn(
                f"Timescale separation ratio {self.separation_ratio:.1f} < 10. "
                "Quasi-equilibrium assumption may be violated. "
                "ESS analysis may be inaccurate."
            )
        
        if self.sigma_sq <= 0:
            raise ValueError("sigma_sq (evolutionary variance) must be positive")


class PopulationDynamics:
    """
    Population dynamics (FAST timescale): dx/dt = x * H(u, x).
    
    This is the ecological layer where populations reach equilibrium x*
    given current strategies u.
    """
    
    def __init__(self, g_function: GFunction):
        """
        Initialize population dynamics.
        
        Parameters
        ----------
        g_function : GFunction
            G-function defining fitness H_i = G(u_i, u, x)
        """
        self.g_function = g_function
    
    def growth_rate(self, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """
        Compute per capita growth rates H_i(u, x) for all species.
        
        H_i = G(v, u, x)|_{v=u_i}
        
        Parameters
        ----------
        u : np.ndarray
            Resident strategies (ns,) or (ns, dim)
        x : np.ndarray
            Population densities (ns,)
            
        Returns
        -------
        np.ndarray
            Growth rates H (ns,)
        """
        ns = len(u)
        H = np.zeros(ns)
        
        for i in range(ns):
            if x[i] > 1e-10:  # Only compute for non-extinct populations
                H[i] = self.g_function.evaluate(u[i], u, x)
        
        return H
    
    def step(self, u: np.ndarray, x: np.ndarray, dt: float) -> np.ndarray:
        """
        Integrate one time step: x(t+dt) = x(t) * exp(H * dt).
        
        Uses exponential integrator (exact for constant H).
        
        Parameters
        ----------
        u : np.ndarray
            Current strategies
        x : np.ndarray
            Current densities
        dt : float
            Time step
            
        Returns
        -------
        np.ndarray
            Updated densities
        """
        H = self.growth_rate(u, x)
        x_new = x * np.exp(H * dt)
        
        # Remove extinct species
        x_new[x_new < 1e-10] = 0
        
        return x_new
    
    def integrate(self, u: np.ndarray, x0: np.ndarray, 
                  t_max: float, dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
        """
        Integrate population dynamics to equilibrium.
        
        Parameters
        ----------
        u : np.ndarray
            Fixed strategies
        x0 : np.ndarray
            Initial densities
        t_max : float
            Maximum integration time
        dt : float
            Time step
            
        Returns
        -------
        t : np.ndarray
            Time points
        x : np.ndarray
            Density trajectories (nt, ns)
        """
        nt = int(t_max / dt)
        ns = len(u)
        
        t = np.linspace(0, t_max, nt)
        x_trajectory = np.zeros((nt, ns))
        x_trajectory[0] = x0
        
        x = x0.copy()
        for i in range(1, nt):
            x = self.step(u, x, dt)
            x_trajectory[i] = x
            
            # Check for equilibrium
            if i > 100 and np.allclose(x_trajectory[i], x_trajectory[i-10], rtol=1e-6):
                # Equilibrium reached, truncate
                return t[:i+1], x_trajectory[:i+1]
        
        return t, x_trajectory
    
    def equilibrium(self, u: np.ndarray, x0: Optional[np.ndarray] = None,
                   tol: float = 1e-6, max_iter: int = 10000) -> np.ndarray:
        """
        Find ecological equilibrium x* for given strategies u.
        
        This is the FAST process that we assume reaches equilibrium
        before strategies change (quasi-equilibrium).
        
        Parameters
        ----------
        u : np.ndarray
            Resident strategies
        x0 : np.ndarray, optional
            Initial guess
        tol : float
            Convergence tolerance
        max_iter : int
            Maximum iterations
            
        Returns
        -------
        np.ndarray
            Equilibrium densities x*
        """
        return self.g_function.ecological_equilibrium(u, x0, tol, max_iter)


class StrategyDynamics:
    """
    Strategy dynamics (SLOW timescale): du/dt = sigma² * ∂G/∂v|_{v=u}.
    
    This is the evolutionary layer where strategies climb the adaptive
    landscape via natural selection.
    
    Key Equation (First-Order Strategy Dynamics, Eq 5.25):
    -------------------------------------------------------
    du_i/dt = sigma_i² * ∂G(v, u, x*)/∂v|_{v=u_i}
    
    where x* = x*(u) is the ecological equilibrium (quasi-equilibrium).
    """
    
    def __init__(self, g_function: GFunction, sigma_sq: float = 1.0):
        """
        Initialize strategy dynamics.
        
        Parameters
        ----------
        g_function : GFunction
            G-function defining fitness landscape
        sigma_sq : float
            Evolutionary variance (rate of strategy change)
        """
        self.g_function = g_function
        self.sigma_sq = sigma_sq
    
    def selection_gradient(self, u: np.ndarray, x: np.ndarray) -> np.ndarray:
        """
        Compute selection gradient ∂G/∂v|_{v=u_i} for all species.
        
        This is the direction of natural selection on the adaptive landscape.
        - Positive gradient → strategy increases
        - Negative gradient → strategy decreases
        - Zero gradient → stationary point (candidate ESS)
        
        Parameters
        ----------
        u : np.ndarray
            Current strategies (ns,) or (ns, dim)
        x : np.ndarray
            Population densities (ns,)
            
        Returns
        -------
        np.ndarray
            Selection gradients (ns, dim)
        """
        ns = len(u)
        
        # Handle scalar vs vector strategies
        if u.ndim == 1:
            grad = np.zeros(ns)
            for i in range(ns):
                if x[i] > 1e-10:
                    grad[i] = self.g_function.gradient(u[i], u, x)[0]
        else:
            dim = u.shape[1]
            grad = np.zeros((ns, dim))
            for i in range(ns):
                if x[i] > 1e-10:
                    grad[i] = self.g_function.gradient(u[i], u, x)
        
        return grad
    
    def step(self, u: np.ndarray, x: np.ndarray, dt: float) -> np.ndarray:
        """
        Integrate one time step: u(t+dt) = u(t) + du/dt * dt.
        
        du/dt = sigma² * ∂G/∂v|_{v=u}
        
        Parameters
        ----------
        u : np.ndarray
            Current strategies
        x : np.ndarray
            Current densities (at quasi-equilibrium)
        dt : float
            Time step
            
        Returns
        -------
        np.ndarray
            Updated strategies
        """
        grad = self.selection_gradient(u, x)
        du_dt = self.sigma_sq * grad
        
        u_new = u + du_dt * dt
        
        return u_new


class DarwinianDynamics:
    """
    Coupled Darwinian Dynamics with timescale separation.
    
    Integrates both population (fast) and strategy (slow) dynamics:
    
    Population (fast):  dx_i/dt = x_i * G(u_i, u, x)
    Strategy (slow):    du_i/dt = sigma_i² * ∂G/∂v|_{v=u_i}
    
    Quasi-Equilibrium Assumption:
    ------------------------------
    If tau_evo >> tau_eco, then x ≈ x*(u) at all times.
    
    This allows us to:
    1. Fix x = x*(u) for each u
    2. Evolve u on fixed adaptive landscape G*(v) = G(v, u, x*(u))
    3. Validate ESS via G* instead of full coupled dynamics
    
    LEGAL INTERPRETATION:
    ---------------------
    - Fast (dx/dt): Legislative activity responds quickly to judicial doctrine
    - Slow (du/dt): Judicial doctrine evolves slowly via precedent accumulation
    - Quasi-equilibrium: Reforms reach "steady state" before doctrine changes
    - ESS stability: Lock-in persists even if reform intensity fluctuates wildly
    """
    
    def __init__(self, g_function: GFunction, timescale_params: TimescaleParams):
        """
        Initialize coupled Darwinian Dynamics.
        
        Parameters
        ----------
        g_function : GFunction
            G-function defining fitness
        timescale_params : TimescaleParams
            Timescale parameters (sigma², tau_eco, tau_evo)
        """
        timescale_params.validate()
        
        self.g_function = g_function
        self.params = timescale_params
        
        self.pop_dynamics = PopulationDynamics(g_function)
        self.strat_dynamics = StrategyDynamics(g_function, timescale_params.sigma_sq)
    
    def integrate_coupled(self, u0: np.ndarray, x0: np.ndarray,
                         t_max: float, dt_pop: float = 0.01, 
                         dt_strat: float = 1.0,
                         use_quasi_equilibrium: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Integrate coupled population-strategy dynamics.
        
        Parameters
        ----------
        u0 : np.ndarray
            Initial strategies (ns,) or (ns, dim)
        x0 : np.ndarray
            Initial densities (ns,)
        t_max : float
            Maximum integration time
        dt_pop : float
            Population time step (fast timescale)
        dt_strat : float
            Strategy time step (slow timescale)
        use_quasi_equilibrium : bool
            If True, use quasi-equilibrium assumption (x ≈ x* always)
            If False, integrate full coupled system (much slower)
            
        Returns
        -------
        t : np.ndarray
            Time points
        u_trajectory : np.ndarray
            Strategy trajectories
        x_trajectory : np.ndarray
            Density trajectories
        """
        nt_strat = int(t_max / dt_strat)
        ns = len(u0)
        
        t = np.linspace(0, t_max, nt_strat)
        u_trajectory = np.zeros((nt_strat, *u0.shape))
        x_trajectory = np.zeros((nt_strat, ns))
        
        u_trajectory[0] = u0
        x_trajectory[0] = x0
        
        u = u0.copy()
        x = x0.copy()
        
        for i in range(1, nt_strat):
            if use_quasi_equilibrium:
                # FAST: Jump to ecological equilibrium instantly
                x = self.pop_dynamics.equilibrium(u, x0=x)
            else:
                # SLOW: Integrate population dynamics for one strategy step
                steps_per_strat = int(dt_strat / dt_pop)
                for _ in range(steps_per_strat):
                    x = self.pop_dynamics.step(u, x, dt_pop)
            
            # SLOW: Update strategies
            u = self.strat_dynamics.step(u, x, dt_strat)
            
            u_trajectory[i] = u
            x_trajectory[i] = x
            
            # Check for convergence to ESS
            if i > 10:
                du = np.linalg.norm(u_trajectory[i] - u_trajectory[i-10])
                if du < 1e-6:
                    # Converged to ESS
                    return t[:i+1], u_trajectory[:i+1], x_trajectory[:i+1]
        
        return t, u_trajectory, x_trajectory
    
    def find_ess(self, u0: np.ndarray, x0: Optional[np.ndarray] = None,
                 t_max: float = 10000.0, dt_strat: float = 1.0,
                 tol: float = 1e-6) -> Tuple[np.ndarray, np.ndarray, bool]:
        """
        Find ESS by integrating Darwinian Dynamics until convergence.
        
        This is the primary method for DEMONSTRATING convergent stability.
        
        Parameters
        ----------
        u0 : np.ndarray
            Initial strategies
        x0 : np.ndarray, optional
            Initial densities (if None, use K_max/ns)
        t_max : float
            Maximum integration time
        dt_strat : float
            Strategy time step
        tol : float
            Convergence tolerance
            
        Returns
        -------
        u_ess : np.ndarray
            ESS strategies (if converged)
        x_ess : np.ndarray
            ESS densities
        converged : bool
            True if converged to ESS
        """
        if x0 is None:
            x0 = np.ones(len(u0)) * self.g_function.params.K_max / len(u0)
        
        t, u_traj, x_traj = self.integrate_coupled(
            u0, x0, t_max, dt_strat=dt_strat, use_quasi_equilibrium=True
        )
        
        # Check if converged
        if len(t) < t_max / dt_strat - 1:
            # Early termination due to convergence
            u_ess = u_traj[-1]
            x_ess = x_traj[-1]
            converged = True
        else:
            # Did not converge
            u_ess = u_traj[-1]
            x_ess = x_traj[-1]
            
            # Check if close to stationary
            du_final = np.linalg.norm(u_traj[-1] - u_traj[-100])
            converged = du_final < tol
        
        return u_ess, x_ess, converged


class TimescaleSeparation:
    """
    Utility class for analyzing timescale separation.
    
    Validates the quasi-equilibrium assumption and warns if violated.
    """
    
    @staticmethod
    def estimate_ecological_timescale(g_function: GFunction, u: np.ndarray,
                                     x0: np.ndarray) -> float:
        """
        Estimate ecological relaxation time tau_eco.
        
        Integrates population dynamics and measures time to reach x*.
        
        Parameters
        ----------
        g_function : GFunction
            G-function
        u : np.ndarray
            Fixed strategies
        x0 : np.ndarray
            Initial densities
            
        Returns
        -------
        float
            Ecological timescale tau_eco
        """
        pop_dyn = PopulationDynamics(g_function)
        
        # Integrate until equilibrium
        t, x_traj = pop_dyn.integrate(u, x0, t_max=1000.0, dt=0.01)
        
        # Find 95% convergence time
        x_final = x_traj[-1]
        
        for i in range(len(t)):
            if np.allclose(x_traj[i], x_final, rtol=0.05):
                return t[i]
        
        return t[-1]
    
    @staticmethod
    def estimate_evolutionary_timescale(g_function: GFunction, u: np.ndarray,
                                       x: np.ndarray, sigma_sq: float) -> float:
        """
        Estimate evolutionary timescale tau_evo.
        
        Based on: tau_evo ~ Delta_u / (sigma² * |∂G/∂v|)
        
        where Delta_u is characteristic strategy change.
        
        Parameters
        ----------
        g_function : GFunction
            G-function
        u : np.ndarray
            Current strategies
        x : np.ndarray
            Current densities
        sigma_sq : float
            Evolutionary variance
            
        Returns
        -------
        float
            Evolutionary timescale tau_evo
        """
        strat_dyn = StrategyDynamics(g_function, sigma_sq)
        grad = strat_dyn.selection_gradient(u, x)
        
        grad_norm = np.linalg.norm(grad)
        
        if grad_norm < 1e-10:
            # At stationary point
            return np.inf
        
        # Characteristic strategy change (10% of current value or 1.0)
        Delta_u = max(np.linalg.norm(u) * 0.1, 1.0)
        
        tau_evo = Delta_u / (sigma_sq * grad_norm)
        
        return tau_evo
    
    @staticmethod
    def validate_separation(g_function: GFunction, u: np.ndarray, x: np.ndarray,
                           sigma_sq: float, min_ratio: float = 10.0) -> bool:
        """
        Validate timescale separation assumption.
        
        Parameters
        ----------
        g_function : GFunction
            G-function
        u : np.ndarray
            Strategies
        x : np.ndarray
            Densities
        sigma_sq : float
            Evolutionary variance
        min_ratio : float
            Minimum required ratio tau_evo / tau_eco
            
        Returns
        -------
        bool
            True if separation is valid
        """
        tau_eco = TimescaleSeparation.estimate_ecological_timescale(g_function, u, x)
        tau_evo = TimescaleSeparation.estimate_evolutionary_timescale(g_function, u, x, sigma_sq)
        
        ratio = tau_evo / tau_eco
        
        if ratio < min_ratio:
            warnings.warn(
                f"Timescale separation VIOLATED: tau_evo/tau_eco = {ratio:.2f} < {min_ratio}. "
                "Quasi-equilibrium assumption may not hold. ESS analysis may be invalid."
            )
            return False
        
        return True


# Export main classes
__all__ = [
    'DarwinianDynamics',
    'PopulationDynamics',
    'StrategyDynamics',
    'TimescaleParams',
    'TimescaleSeparation',
]
