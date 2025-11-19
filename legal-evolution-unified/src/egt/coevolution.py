"""
Coevolution: Legislative-Judicial Coupled Dynamics
===================================================

Implements multi-bauplan coevolution from Vince (2005), Chapter 10 & Example 4.6.1.

Key Insight from Report 5:
---------------------------
Constitutional lock-in is COEVOLUTIONARY:
- Population 1 (Legislative): Reform strategies
- Population 2 (Judicial): Defensive strategies
- Each evolves in response to the other

Hypothesis: Reforms push → Doctrine hardens → Stronger lock-in emerges
This is modeled as coevolution converging to more extreme ESS.

Red Queen Dynamics:
-------------------
If tau_evo ≈ tau_eco (timescales not separated), system may exhibit:
- Cycles (strategies chase each other)
- Arms races (escalating rigidity)
- Chaos (no equilibrium)

References:
-----------
Vince (2005), Example 4.6.1: "Predator-Prey Coevolution"
Vince (2005), Chapter 10: "Evolutionary Ecology"
"""

import numpy as np
from typing import Tuple, List
from .g_function import GFunction, GFunctionParams


class CoupledGFunctions:
    """
    Coupled G-functions for Legislative-Judicial coevolution.
    
    G_leg(v_leg, u_leg, u_jud, x_leg, x_jud): Legislative fitness
    G_jud(v_jud, u_jud, u_leg, x_jud, x_leg): Judicial fitness
    
    Analogy to Predator-Prey (Vince Example 4.6.1):
    ------------------------------------------------
    Legislative (Prey): Grows unless blocked by Judicial
    Judicial (Predator): Depends on Legislative activity for "sustenance"
    """
    
    def __init__(self, params_leg: GFunctionParams, params_jud: GFunctionParams):
        self.params_leg = params_leg
        self.params_jud = params_jud
    
    def K(self, v: float, K_max: float, sigma_k: float) -> float:
        """Carrying capacity."""
        return K_max * np.exp(-v**2 / (2 * sigma_k**2))
    
    def b(self, v_leg: float, u_jud: float, sigma_b: float) -> float:
        """
        Blocking coefficient: How effectively judicial strategy u_jud blocks reform v_leg.
        
        Analogy: Predation rate in Vince's model.
        """
        return np.exp(-(v_leg - u_jud)**2 / (2 * sigma_b**2))
    
    def G_legislative(self, v_leg: float, u_leg: np.ndarray, u_jud: np.ndarray,
                     x_leg: np.ndarray, x_jud: np.ndarray) -> float:
        """
        Legislative G-function (analogous to Prey).
        
        G_leg = r * [K(v_leg) - sum_j x_leg_j * a(v, u_j) - sum_k x_jud_k * b(v, u_k)] / K(v_leg)
        
        Interpretation:
        - Grows with carrying capacity K(v_leg)
        - Reduced by competition with other reforms (a term)
        - Reduced by judicial blocking (b term) ← KEY COUPLING
        """
        r = self.params_leg.r
        K_max = self.params_leg.K_max
        sigma_k = self.params_leg.sigma_k
        sigma_alpha = self.params_leg.sigma_alpha
        sigma_b = 0.5  # Blocking niche width (narrow = specific defense)
        
        K_v = self.K(v_leg, K_max, sigma_k)
        if K_v < 1e-12:
            return -np.inf
        
        # Intra-legislative competition
        competition = np.sum([x_leg[j] * np.exp(-(v_leg - u_leg[j])**2 / (2 * sigma_alpha**2)) 
                             for j in range(len(u_leg))])
        
        # Judicial blocking (predation)
        blocking = np.sum([x_jud[k] * self.b(v_leg, u_jud[k], sigma_b) 
                          for k in range(len(u_jud))])
        
        return r * (K_v - competition - blocking) / K_v
    
    def G_judicial(self, v_jud: float, u_jud: np.ndarray, u_leg: np.ndarray,
                  x_jud: np.ndarray, x_leg: np.ndarray) -> float:
        """
        Judicial G-function (analogous to Predator).
        
        G_jud = r * [1 - sum_k x_jud_k / (c * sum_j x_leg_j * b(v_jud, u_leg_j))]
        
        Interpretation:
        - Depends positively on legislative activity (prey availability)
        - Competes with other judicial strategies
        - More effective blocking (higher b) → higher fitness
        """
        r_jud = 0.25  # Judicial evolution rate (SLOW compared to legislative)
        c = 2.0  # Conversion efficiency (how much blocking sustains doctrine)
        sigma_b = 0.5
        
        # Predation efficiency (how well v_jud blocks existing reforms)
        efficiency = np.sum([x_leg[j] * self.b(u_leg[j], v_jud, sigma_b) 
                            for j in range(len(u_leg))])
        
        if efficiency < 1e-12:
            return -np.inf  # No reforms to block → doctrine cannot sustain
        
        # Intra-judicial competition
        competition_denom = c * efficiency
        competition = np.sum(x_jud) / competition_denom if competition_denom > 0 else np.inf
        
        return r_jud * (1 - competition)


class CoevolutionSystem:
    """
    Coupled Legislative-Judicial coevolution system.
    
    Integrates both populations simultaneously under coupled G-functions.
    """
    
    def __init__(self, coupled_g: CoupledGFunctions):
        self.coupled_g = coupled_g
    
    def integrate(self, u_leg0: np.ndarray, u_jud0: np.ndarray,
                 x_leg0: np.ndarray, x_jud0: np.ndarray,
                 t_max: float = 5000.0, dt: float = 0.1,
                 sigma_sq_leg: float = 1.0, sigma_sq_jud: float = 0.1) -> dict:
        """
        Integrate coupled coevolution.
        
        Parameters
        ----------
        u_leg0 : np.ndarray
            Initial legislative strategies
        u_jud0 : np.ndarray
            Initial judicial strategies
        x_leg0 : np.ndarray
            Initial legislative densities
        x_jud0 : np.ndarray
            Initial judicial densities
        t_max : float
            Integration time
        dt : float
            Time step
        sigma_sq_leg : float
            Legislative evolutionary variance (FAST)
        sigma_sq_jud : float
            Judicial evolutionary variance (SLOW) ← KEY: slower than legislative
            
        Returns
        -------
        dict
            Trajectories of strategies and densities
        """
        nt = int(t_max / dt)
        
        u_leg = u_leg0.copy()
        u_jud = u_jud0.copy()
        x_leg = x_leg0.copy()
        x_jud = x_jud0.copy()
        
        u_leg_traj = np.zeros((nt, len(u_leg0)))
        u_jud_traj = np.zeros((nt, len(u_jud0)))
        x_leg_traj = np.zeros((nt, len(x_leg0)))
        x_jud_traj = np.zeros((nt, len(x_jud0)))
        
        for t in range(nt):
            u_leg_traj[t] = u_leg
            u_jud_traj[t] = u_jud
            x_leg_traj[t] = x_leg
            x_jud_traj[t] = x_jud
            
            # Population dynamics (fast)
            H_leg = np.array([self.coupled_g.G_legislative(u_leg[i], u_leg, u_jud, x_leg, x_jud) 
                             for i in range(len(u_leg))])
            H_jud = np.array([self.coupled_g.G_judicial(u_jud[i], u_jud, u_leg, x_jud, x_leg) 
                             for i in range(len(u_jud))])
            
            x_leg = x_leg * np.exp(H_leg * dt)
            x_jud = x_jud * np.exp(H_jud * dt)
            
            # Remove extinct
            x_leg[x_leg < 1e-10] = 0
            x_jud[x_jud < 1e-10] = 0
            
            # Strategy dynamics (slow) - simplified gradient
            # (Full implementation requires numerical gradient)
            epsilon = 1e-4
            
            for i in range(len(u_leg)):
                if x_leg[i] > 1e-10:
                    G_plus = self.coupled_g.G_legislative(u_leg[i] + epsilon, u_leg, u_jud, x_leg, x_jud)
                    G_minus = self.coupled_g.G_legislative(u_leg[i] - epsilon, u_leg, u_jud, x_leg, x_jud)
                    grad = (G_plus - G_minus) / (2 * epsilon)
                    u_leg[i] += sigma_sq_leg * grad * dt
            
            for i in range(len(u_jud)):
                if x_jud[i] > 1e-10:
                    G_plus = self.coupled_g.G_judicial(u_jud[i] + epsilon, u_jud, u_leg, x_jud, x_leg)
                    G_minus = self.coupled_g.G_judicial(u_jud[i] - epsilon, u_jud, u_leg, x_jud, x_leg)
                    grad = (G_plus - G_minus) / (2 * epsilon)
                    u_jud[i] += sigma_sq_jud * grad * dt  # SLOWER evolution
        
        return {
            't': np.linspace(0, t_max, nt),
            'u_leg': u_leg_traj,
            'u_jud': u_jud_traj,
            'x_leg': x_leg_traj,
            'x_jud': x_jud_traj,
        }


class RedQueenDynamics:
    """
    Red Queen dynamics analysis: Do strategies chase each other endlessly?
    
    Indicators:
    -----------
    - Periodic orbits in (u_leg, u_jud) space
    - Non-converging strategy evolution
    - Fitness remains non-zero (no ESS reached)
    """
    
    @staticmethod
    def detect_cycles(trajectory: dict, threshold: float = 0.01) -> bool:
        """
        Detect if coevolution exhibits cycles instead of convergence.
        
        Returns True if strategies oscillate rather than converge.
        """
        u_leg = trajectory['u_leg']
        u_jud = trajectory['u_jud']
        
        # Check if strategies are still changing in last 20% of simulation
        n = len(u_leg)
        final_20pct = int(0.2 * n)
        
        u_leg_change = np.std(u_leg[-final_20pct:, 0])
        u_jud_change = np.std(u_jud[-final_20pct:, 0])
        
        return (u_leg_change > threshold) or (u_jud_change > threshold)


__all__ = ['CoupledGFunctions', 'CoevolutionSystem', 'RedQueenDynamics']
