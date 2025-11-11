"""
Legal-Memespace Tools for MCP Server
Competitive dynamics modeling using Lotka-Volterra equations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.legal_memespace.memespace import LegalMemespace, PhaseTransition
import numpy as np
from typing import Dict, List, Any, Tuple
import json

# Initialize Memespace instance (reusable)
_memespace_instance = None

def get_memespace() -> LegalMemespace:
    """Get or create Memespace singleton instance"""
    global _memespace_instance
    if _memespace_instance is None:
        _memespace_instance = LegalMemespace(n_dimensions=4)
    return _memespace_instance

def analyze_doctrinal_competition(
    doctrines: List[str],
    initial_prevalence: List[float],
    competition_matrix: List[List[float]],
    time_horizon: int = 50,
    carrying_capacity: List[float] = None
) -> Dict[str, Any]:
    """
    Model competitive dynamics between legal doctrines using Lotka-Volterra.
    
    Args:
        doctrines: List of doctrine names (e.g., ["textualism", "purposivism"])
        initial_prevalence: Initial prevalence [0,1] for each doctrine
        competition_matrix: NxN matrix of competition coefficients
        time_horizon: Years to simulate
        carrying_capacity: Max prevalence for each doctrine (defaults to 1.0)
    
    Returns:
        Dict with trajectories, equilibria, phase transitions
    """
    memespace = get_memespace()
    
    n_doctrines = len(doctrines)
    if carrying_capacity is None:
        carrying_capacity = [1.0] * n_doctrines
    
    # Lotka-Volterra dynamics
    def lotka_volterra(y, t, r, K, alpha):
        """
        dy/dt = r * y * (1 - (y + alpha*y_other)/K)
        """
        dydt = np.zeros(n_doctrines)
        for i in range(n_doctrines):
            competition_sum = sum(alpha[i][j] * y[j] for j in range(n_doctrines) if i != j)
            dydt[i] = r[i] * y[i] * (1 - (y[i] + competition_sum) / K[i])
        return dydt
    
    # Growth rates (assume 0.1 for all)
    r = [0.1] * n_doctrines
    
    # Simulate
    from scipy.integrate import odeint
    t = np.linspace(0, time_horizon, time_horizon * 10)
    solution = odeint(lotka_volterra, initial_prevalence, t, args=(r, carrying_capacity, competition_matrix))
    
    # Detect phase transitions (sudden changes in prevalence)
    transitions = []
    for i in range(1, len(solution)):
        delta = np.abs(solution[i] - solution[i-1])
        if np.max(delta) > 0.05:  # Threshold for significant change
            transitions.append({
                "time": t[i],
                "magnitude": float(np.max(delta)),
                "doctrines_affected": [doctrines[j] for j, d in enumerate(delta) if d > 0.02]
            })
    
    # Final equilibrium
    final_state = solution[-1]
    dominant_doctrine = doctrines[np.argmax(final_state)]
    
    # Survival probabilities
    survival_probs = {
        doc: float(final_state[i] > 0.1) for i, doc in enumerate(doctrines)
    }
    
    return {
        "doctrines": doctrines,
        "trajectories": {
            doc: solution[:, i].tolist()[::10]  # Sample every 10th point
            for i, doc in enumerate(doctrines)
        },
        "time_points": t.tolist()[::10],
        "final_equilibrium": {doc: float(final_state[i]) for i, doc in enumerate(doctrines)},
        "dominant_doctrine": dominant_doctrine,
        "phase_transitions": transitions[:5],  # Top 5
        "survival_probabilities": survival_probs,
        "competition_intensity": float(np.mean(np.abs(competition_matrix)))
    }

def detect_tipping_point(
    doctrine_trajectory: List[float],
    time_points: List[float],
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Detect tipping point where doctrine crosses dominance threshold.
    
    Args:
        doctrine_trajectory: Prevalence over time [0,1]
        time_points: Corresponding time points
        threshold: Dominance threshold (default 0.5)
    
    Returns:
        Dict with tipping point info
    """
    traj = np.array(doctrine_trajectory)
    
    # Find crossing point
    crossings = np.where(np.diff(np.sign(traj - threshold)))[0]
    
    if len(crossings) == 0:
        return {
            "tipping_point_detected": False,
            "final_prevalence": float(traj[-1]),
            "trend": "stable" if np.std(traj) < 0.1 else "fluctuating"
        }
    
    first_crossing = crossings[0]
    tipping_time = time_points[first_crossing]
    
    # Calculate velocity (rate of change)
    if first_crossing > 0 and first_crossing < len(traj) - 1:
        velocity = (traj[first_crossing + 1] - traj[first_crossing - 1]) / 2
    else:
        velocity = 0
    
    return {
        "tipping_point_detected": True,
        "tipping_time": float(tipping_time),
        "crossing_prevalence": float(traj[first_crossing]),
        "velocity": float(velocity),
        "direction": "ascent" if velocity > 0 else "descent",
        "total_crossings": len(crossings)
    }

# Example: Argentina constitutional interpretation doctrines
EXAMPLE_ARGENTINA_DOCTRINES = {
    "doctrines": ["originalismo", "textualismo", "purposivismo", "living_constitution"],
    "initial_prevalence": [0.7, 0.6, 0.3, 0.1],  # 1853-1994 baseline
    "competition_matrix": [
        [0.0, 0.3, 0.8, 0.9],  # Originalismo competes strongly with purposivism/living
        [0.3, 0.0, 0.5, 0.7],  # Textualismo
        [0.8, 0.5, 0.0, 0.2],  # Purposivismo (weaker competition with living)
        [0.9, 0.7, 0.2, 0.0]   # Living constitution (strongest competitor)
    ],
    "time_horizon": 30,  # 1994-2024
    "carrying_capacity": [1.0, 1.0, 0.8, 0.6]  # Living constitutionalism limited by CLI
}

def demo_argentina_doctrinal_shift() -> Dict[str, Any]:
    """
    Demonstration: Model shift from originalismo to purposivismo post-1994.
    
    This models Smulovitz "descubrimiento de la ley" - how courts discovered
    activist interpretation after 1994 constitutional reform.
    """
    result = analyze_doctrinal_competition(
        **EXAMPLE_ARGENTINA_DOCTRINES
    )
    
    # Add interpretation
    result["interpretation"] = {
        "context": "Post-1994 constitutional reform (Art. 75.22 - treaty hierarchy)",
        "mechanism": "Judicial activism (JA) increases via international human rights law",
        "williamson_level": 2,  # Institutional environment shift
        "cli_impact": "JA component: 0.65 (1994) → 0.85 (2024)",
        "smulovitz_framework": "Courts discover law as political tool",
        "key_cases": ["Ekmekdjian 1992", "Vizzoti 2004", "Madorrán 2007"],
        "consequence": "Lock-in: CLI rises from 0.65 to 0.87"
    }
    
    # Detect tipping point for purposivismo
    if "purposivismo" in result["trajectories"]:
        tipping = detect_tipping_point(
            result["trajectories"]["purposivismo"],
            result["time_points"],
            threshold=0.5
        )
        result["purposivismo_tipping_point"] = tipping
    
    return result

