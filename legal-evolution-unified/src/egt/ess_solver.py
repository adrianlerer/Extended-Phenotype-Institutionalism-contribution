"""
ESS (Evolutionarily Stable Strategy) Solver
============================================

Implements ESS Maximum Principle and stability tests from Vince (2005), Chapter 7.

ESS Definition (Definition 6.2.4):
-----------------------------------
A coalition of strategies u_c is an ESS if it is RESISTANT TO INVASION by
rare alternative strategies u_m.

Invasion resistance requires:
1. Ecological equilibrium x* remains stable (ESE)
2. Fitness of invaders is negative: G(v, u_c, x*) < 0 for all v ≠ u_c

ESS Maximum Principle (Theorem 7.1.1):
---------------------------------------
If u_c is an ESS, then:

    max_{v ∈ U} G(v, u, x*) = G(v, u, x*)|_{v=u_i} = 0

That is:
1. Each strategy u_i in the coalition is a GLOBAL MAXIMUM of G*(v)
2. The fitness at ESS is ZERO: G(u_i, u, x*) = 0

TWO Required Conditions for ESS:
---------------------------------
1. INVASION RESISTANCE (IR):
   ∂²G/∂v² < 0 at v = u_i (negative curvature = peak)
   
2. CONVERGENT STABILITY (CS):
   Darwinian Dynamics converges to u* from nearby initial conditions
   Verified by eigenvalue analysis or direct simulation

Disruptive Selection (A > 0):
------------------------------
If ∂²G/∂v² > 0 (positive curvature = valley), the strategy is:
- Convergently Stable (CS): dynamics converge to it
- NOT Invasion Resistant: mutants have higher fitness
- Result: SPECIATION (Evolutionary Branching)

This is the KEY mechanism for doctrinal subdivision.

LEGAL INTERPRETATION:
---------------------
ESS = Constitutional Lock-in (doctrine resistant to legislative reforms)
IR = Núcleo irreductible strength (reform attempts have negative "fitness")
CS = Historical convergence (doctrine emerged from precedent accumulation)
A > 0 = Speciation pressure (doctrine splits into subdoctrines)

References:
-----------
Vince (2005), Chapter 7: "The ESS Maximum Principle"
Vince (2005), Section 8.2: "Disruptive Selection and Evolutionary Branching"
"""

import numpy as np
from typing import Tuple, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum
import warnings

from .g_function import GFunction
from .darwinian_dynamics import DarwinianDynamics, TimescaleParams


class StabilityType(Enum):
    """Classification of strategy equilibria."""
    ESS = "ESS"  # Invasion resistant + Convergent stable (PEAK)
    CSS = "CSS"  # Convergent stable but not IR (VALLEY → speciation)
    REPELLOR = "REPELLOR"  # Not convergent stable (saddle point)
    UNKNOWN = "UNKNOWN"


@dataclass
class ESSResult:
    """
    Result of ESS analysis.
    
    Attributes
    ----------
    u_ess : np.ndarray
        ESS strategies
    x_ess : np.ndarray
        ESS densities
    stability_type : StabilityType
        Classification (ESS, CSS, REPELLOR)
    invasion_resistant : bool
        True if ∂²G/∂v² < 0 (peak)
    convergent_stable : bool
        True if dynamics converge
    fitness : np.ndarray
        Fitness values at ESS (should be ≈ 0)
    hessian_eigenvalues : np.ndarray
        Eigenvalues of Hessian (stability test)
    converged : bool
        True if solver converged
    """
    u_ess: np.ndarray
    x_ess: np.ndarray
    stability_type: StabilityType
    invasion_resistant: bool
    convergent_stable: bool
    fitness: np.ndarray
    hessian_eigenvalues: np.ndarray
    converged: bool
    
    def __str__(self) -> str:
        """Pretty print ESS result."""
        lines = [
            "=" * 60,
            "ESS ANALYSIS RESULT",
            "=" * 60,
            f"Stability Type: {self.stability_type.value}",
            f"Invasion Resistant: {self.invasion_resistant}",
            f"Convergent Stable: {self.convergent_stable}",
            f"Converged: {self.converged}",
            "",
            "ESS Strategies:",
            str(self.u_ess),
            "",
            "ESS Densities:",
            str(self.x_ess),
            "",
            f"Fitness (should be ≈ 0): {self.fitness}",
            "",
            f"Hessian Eigenvalues: {self.hessian_eigenvalues}",
            "  (All negative → ESS)",
            "  (Any positive → CSS/Speciation)",
            "=" * 60,
        ]
        return "\n".join(lines)


class InvasionResistance:
    """
    Tests for Invasion Resistance (IR) via Hessian analysis.
    
    IR Condition (Theorem 7.1.1):
    -----------------------------
    A strategy u is invasion resistant if:
    
        A = ∂²G/∂v² |_{v=u} < 0  (negative definite)
    
    Interpretation:
    ---------------
    - A < 0: PEAK (ESS if also CS)
    - A > 0: VALLEY (CSS → speciation if CS)
    - A = 0: Neutral (requires higher-order analysis)
    """
    
    @staticmethod
    def test(g_function: GFunction, u: np.ndarray, x: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Test invasion resistance for all strategies in coalition.
        
        Parameters
        ----------
        g_function : GFunction
            G-function
        u : np.ndarray
            Candidate ESS strategies
        x : np.ndarray
            Equilibrium densities
            
        Returns
        -------
        invasion_resistant : bool
            True if all strategies have A < 0
        eigenvalues : np.ndarray
            Eigenvalues of Hessian for each strategy
        """
        ns = len(u)
        eigenvalues = []
        
        for i in range(ns):
            if x[i] < 1e-10:
                # Extinct species, skip
                eigenvalues.append(np.array([np.nan]))
                continue
            
            # Compute Hessian at u_i
            H = g_function.hessian(u[i], u, x)
            
            # Extract eigenvalues
            if H.ndim == 0:
                # Scalar
                eigs = np.array([H])
            elif H.ndim == 1:
                # 1D
                eigs = np.array([H[0]])
            else:
                # Matrix
                eigs = np.linalg.eigvals(H)
            
            eigenvalues.append(eigs)
        
        eigenvalues = np.concatenate(eigenvalues)
        
        # IR requires ALL eigenvalues < 0 (negative definite)
        invasion_resistant = np.all(eigenvalues < 0)
        
        return invasion_resistant, eigenvalues
    
    @staticmethod
    def classify_curvature(eigenvalues: np.ndarray) -> str:
        """
        Classify adaptive landscape curvature.
        
        Parameters
        ----------
        eigenvalues : np.ndarray
            Hessian eigenvalues
            
        Returns
        -------
        str
            Classification: "PEAK", "VALLEY", "SADDLE", "NEUTRAL"
        """
        eigenvalues = eigenvalues[~np.isnan(eigenvalues)]
        
        if len(eigenvalues) == 0:
            return "UNKNOWN"
        
        if np.all(eigenvalues < -1e-8):
            return "PEAK"  # All negative → ESS candidate
        elif np.all(eigenvalues > 1e-8):
            return "VALLEY"  # All positive → CSS/Speciation
        elif np.any(eigenvalues > 1e-8) and np.any(eigenvalues < -1e-8):
            return "SADDLE"  # Mixed → Unstable
        else:
            return "NEUTRAL"  # Near zero → Higher-order test needed


class ConvergentStability:
    """
    Tests for Convergent Stability (CS) via Darwinian Dynamics simulation.
    
    CS Condition:
    -------------
    A strategy u* is convergently stable if Darwinian Dynamics starting
    from nearby initial conditions converges to u*.
    
    Vince notes: "For horrendous stability conditions for coalitions, 
    see Theorem 5.5.1. In practice, we verify CS by simulation."
    
    Method:
    -------
    1. Initialize u(0) near candidate ESS u*
    2. Integrate Darwinian Dynamics
    3. Check if u(t) → u* as t → ∞
    """
    
    @staticmethod
    def test(g_function: GFunction, u_candidate: np.ndarray, 
             x_candidate: np.ndarray, timescale_params: TimescaleParams,
             n_trials: int = 5, perturbation: float = 0.1,
             t_max: float = 5000.0) -> Tuple[bool, List[np.ndarray]]:
        """
        Test convergent stability by perturbed simulations.
        
        Parameters
        ----------
        g_function : GFunction
            G-function
        u_candidate : np.ndarray
            Candidate ESS
        x_candidate : np.ndarray
            Candidate equilibrium
        timescale_params : TimescaleParams
            Timescale parameters
        n_trials : int
            Number of perturbed initial conditions to test
        perturbation : float
            Size of perturbation (fraction of u_candidate)
        t_max : float
            Maximum integration time
            
        Returns
        -------
        convergent_stable : bool
            True if all trials converge to u_candidate
        trajectories : List[np.ndarray]
            Strategy trajectories from each trial
        """
        dynamics = DarwinianDynamics(g_function, timescale_params)
        
        trajectories = []
        converged_count = 0
        
        for trial in range(n_trials):
            # Perturb initial condition
            if u_candidate.ndim == 1:
                u0 = u_candidate + np.random.randn(len(u_candidate)) * perturbation
            else:
                u0 = u_candidate + np.random.randn(*u_candidate.shape) * perturbation
            
            # Integrate dynamics
            u_final, x_final, converged = dynamics.find_ess(
                u0, x_candidate, t_max=t_max, tol=1e-5
            )
            
            trajectories.append(u_final)
            
            # Check if converged to candidate
            if converged and np.allclose(u_final, u_candidate, rtol=0.05):
                converged_count += 1
        
        # CS if majority of trials converge
        convergent_stable = (converged_count >= n_trials * 0.8)
        
        return convergent_stable, trajectories


class MaximumPrinciple:
    """
    ESS Maximum Principle (Theorem 7.1.1) verification.
    
    Theorem 7.1.1:
    --------------
    If u_c is an ESS coalition, then for all i in the coalition:
    
        max_{v ∈ U} G(v, u_c, x*) = G(v, u_c, x*)|_{v=u_i} = 0
    
    Verification steps:
    -------------------
    1. Compute G*(v) = G(v, u_c, x*) over strategy space
    2. Check if u_i are global maxima
    3. Check if G*(u_i) ≈ 0
    """
    
    @staticmethod
    def verify(g_function: GFunction, u: np.ndarray, x: np.ndarray,
               v_range: Optional[Tuple[float, float]] = None,
               n_points: int = 200) -> Tuple[bool, Dict]:
        """
        Verify Maximum Principle by plotting adaptive landscape.
        
        Parameters
        ----------
        g_function : GFunction
            G-function
        u : np.ndarray
            Candidate ESS
        x : np.ndarray
            Equilibrium densities
        v_range : Tuple[float, float], optional
            Range of virtual strategies to test
        n_points : int
            Number of points to sample
            
        Returns
        -------
        is_maximum : bool
            True if u are global maxima
        landscape_data : dict
            Data for plotting adaptive landscape
        """
        # Determine strategy range
        if v_range is None:
            u_flat = u.flatten()
            u_min, u_max = u_flat.min(), u_flat.max()
            margin = max((u_max - u_min) * 0.5, 2.0)
            v_range = (u_min - margin, u_max + margin)
        
        # Sample adaptive landscape
        v_grid = np.linspace(v_range[0], v_range[1], n_points)
        G_star = np.zeros(n_points)
        
        for i, v in enumerate(v_grid):
            G_star[i] = g_function.evaluate(v, u, x)
        
        # Find global maximum
        i_max = np.argmax(G_star)
        v_max = v_grid[i_max]
        G_max = G_star[i_max]
        
        # Check if u are near global maximum
        u_flat = u.flatten()
        is_maximum = True
        for u_i in u_flat:
            if not np.isclose(u_i, v_max, atol=0.1):
                is_maximum = False
                break
        
        # Check if fitness is near zero
        fitness_near_zero = np.abs(G_max) < 0.1
        
        landscape_data = {
            'v_grid': v_grid,
            'G_star': G_star,
            'v_max': v_max,
            'G_max': G_max,
            'u': u_flat,
            'is_maximum': is_maximum,
            'fitness_near_zero': fitness_near_zero,
        }
        
        return is_maximum and fitness_near_zero, landscape_data


class ESSSolver:
    """
    Complete ESS solver implementing Vince (2005) framework.
    
    Workflow:
    ---------
    1. Find candidate ESS via Darwinian Dynamics integration
    2. Test Invasion Resistance (IR) via Hessian
    3. Test Convergent Stability (CS) via perturbed simulations
    4. Verify Maximum Principle
    5. Classify: ESS, CSS, or REPELLOR
    """
    
    def __init__(self, g_function: GFunction, timescale_params: TimescaleParams):
        """
        Initialize ESS solver.
        
        Parameters
        ----------
        g_function : GFunction
            G-function defining fitness landscape
        timescale_params : TimescaleParams
            Timescale parameters for dynamics
        """
        self.g_function = g_function
        self.timescale_params = timescale_params
        self.dynamics = DarwinianDynamics(g_function, timescale_params)
    
    def solve(self, u0: np.ndarray, x0: Optional[np.ndarray] = None,
              t_max: float = 10000.0, verify_cs: bool = True,
              verify_maximum: bool = True) -> ESSResult:
        """
        Solve for ESS and perform complete stability analysis.
        
        Parameters
        ----------
        u0 : np.ndarray
            Initial strategy guess
        x0 : np.ndarray, optional
            Initial density guess
        t_max : float
            Maximum integration time
        verify_cs : bool
            If True, verify convergent stability with perturbed simulations
        verify_maximum : bool
            If True, verify Maximum Principle
            
        Returns
        -------
        ESSResult
            Complete ESS analysis result
        """
        # Step 1: Find candidate ESS via Darwinian Dynamics
        print("Step 1: Finding candidate ESS via Darwinian Dynamics...")
        u_ess, x_ess, converged = self.dynamics.find_ess(u0, x0, t_max=t_max)
        
        if not converged:
            warnings.warn("Darwinian Dynamics did not converge. ESS may be invalid.")
        
        # Step 2: Test Invasion Resistance
        print("Step 2: Testing Invasion Resistance (Hessian analysis)...")
        invasion_resistant, hessian_eigs = InvasionResistance.test(
            self.g_function, u_ess, x_ess
        )
        
        curvature = InvasionResistance.classify_curvature(hessian_eigs)
        print(f"  Curvature: {curvature}")
        print(f"  Invasion Resistant: {invasion_resistant}")
        
        # Step 3: Test Convergent Stability (optional, expensive)
        convergent_stable = True  # Assume true if dynamics converged
        if verify_cs:
            print("Step 3: Testing Convergent Stability (perturbed simulations)...")
            convergent_stable, _ = ConvergentStability.test(
                self.g_function, u_ess, x_ess, self.timescale_params
            )
            print(f"  Convergent Stable: {convergent_stable}")
        
        # Step 4: Verify Maximum Principle (optional)
        if verify_maximum:
            print("Step 4: Verifying Maximum Principle...")
            is_maximum, _ = MaximumPrinciple.verify(self.g_function, u_ess, x_ess)
            print(f"  Is Global Maximum: {is_maximum}")
        
        # Step 5: Compute fitness (should be ≈ 0 for ESS)
        fitness = np.array([
            self.g_function.evaluate(u_ess[i], u_ess, x_ess) 
            for i in range(len(u_ess)) if x_ess[i] > 1e-10
        ])
        
        # Step 6: Classify stability type
        if invasion_resistant and convergent_stable:
            stability_type = StabilityType.ESS
        elif convergent_stable and not invasion_resistant:
            stability_type = StabilityType.CSS  # → Speciation
        elif not convergent_stable:
            stability_type = StabilityType.REPELLOR
        else:
            stability_type = StabilityType.UNKNOWN
        
        print(f"\nFinal Classification: {stability_type.value}")
        
        return ESSResult(
            u_ess=u_ess,
            x_ess=x_ess,
            stability_type=stability_type,
            invasion_resistant=invasion_resistant,
            convergent_stable=convergent_stable,
            fitness=fitness,
            hessian_eigenvalues=hessian_eigs,
            converged=converged,
        )
    
    def find_all_ess(self, u_grid: np.ndarray, n_trials: int = 10,
                     **solve_kwargs) -> List[ESSResult]:
        """
        Find all ESS in strategy space by grid search.
        
        Useful for detecting multiple ESS (coalitions) or bifurcations.
        
        Parameters
        ----------
        u_grid : np.ndarray
            Grid of initial strategies to try
        n_trials : int
            Number of trials per grid point
        **solve_kwargs
            Arguments passed to solve()
            
        Returns
        -------
        List[ESSResult]
            All unique ESS found
        """
        ess_list = []
        
        for u0 in u_grid:
            result = self.solve(u0, **solve_kwargs)
            
            # Check if this ESS is new (not duplicate)
            is_duplicate = False
            for prev_result in ess_list:
                if np.allclose(result.u_ess, prev_result.u_ess, rtol=0.01):
                    is_duplicate = True
                    break
            
            if not is_duplicate and result.converged:
                ess_list.append(result)
        
        return ess_list


# Export main classes
__all__ = [
    'ESSSolver',
    'ESSResult',
    'StabilityType',
    'InvasionResistance',
    'ConvergentStability',
    'MaximumPrinciple',
]
