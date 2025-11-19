"""
Evolutionary Game Theory (EGT) Framework for Legal Evolution
==============================================================

This module implements the Darwinian Dynamics framework from Vince (2005)
"Evolutionary Game Theory, Natural Selection, and Darwinian Dynamics"
(Cambridge University Press) applied to constitutional law evolution.

Core Concepts:
--------------
- G-function (Fitness-Generating Function): G(v, u, x) 
  where v = virtual strategy, u = resident strategies, x = population densities
- ESS (Evolutionarily Stable Strategy): Strategy immune to invasion by rare mutants
- Darwinian Dynamics: Coupling of population dynamics (fast, ecological) and 
  strategy dynamics (slow, evolutionary)
- Adaptive Landscape: Visualization of fitness landscape where peaks = ESS

Legal Analogy:
--------------
BIOLOGY → CONSTITUTIONAL LAW
═══════════════════════════════════════════
Harvesting (fishing) → Legislative reforms
Evolutionary response → Judicial lock-in strengthens
ESOHS (optimal harvest) → Optimal reform strategy
Chemotherapy resistance → Constitutional lock-in
Speciation (branching) → Doctrinal subdivision
Tragedy of commons → Reform paradox (attempts strengthen ESS)

Modules:
--------
- g_function: Core G-function implementations (scalar, vectorial, frequency-based)
- darwinian_dynamics: Coupled population-strategy dynamics with timescale separation
- ess_solver: ESS Maximum Principle solver with convergent stability verification
- adaptive_landscape: Visualization tools for fitness landscapes
- coevolution: Multi-bauplan systems (legislative-judicial coevolution)
- empirical_calibration: Methods for fitting G-functions to discrete empirical data

References:
-----------
Vince, T.L. (2005). Evolutionary Game Theory, Natural Selection, and Darwinian 
Dynamics. Cambridge University Press. ISBN: 978-0-521-84170-2

Lerer, I.A. (2025). Constitutional Paleontology: Tracing the Ancestor's Tale of 
Legal Doctrines. SSRN: https://ssrn.com/abstract=5660770
"""

__version__ = "1.0.0"
__author__ = "Ignacio A. Lerer"

from .g_function import (
    GFunction,
    ScalarGFunction,
    VectorGFunction,
    FrequencyGFunction,
    LotkaVolterraGFunction,
)

from .darwinian_dynamics import (
    DarwinianDynamics,
    PopulationDynamics,
    StrategyDynamics,
    TimescaleSeparation,
)

from .ess_solver import (
    ESSSolver,
    MaximumPrinciple,
    ConvergentStability,
    InvasionResistance,
)

from .adaptive_landscape import (
    AdaptiveLandscape,
    LandscapeVisualizer,
    BifurcationAnalyzer,
)

from .coevolution import (
    CoevolutionSystem,
    CoupledGFunctions,
    RedQueenDynamics,
)

from .empirical_calibration import (
    DiscreteOutcomeCalibrator,
    ParameterEstimator,
    ModelValidator,
)

from .universal_predictor import (
    UniversalEGTPredictor,
    VinceParameters,
    predict_reform_success,
)

__all__ = [
    # Universal API (Main entry point for users)
    "UniversalEGTPredictor",
    "VinceParameters",
    "predict_reform_success",
    
    # G-function classes
    "GFunction",
    "ScalarGFunction",
    "VectorGFunction",
    "FrequencyGFunction",
    "LotkaVolterraGFunction",
    
    # Darwinian Dynamics
    "DarwinianDynamics",
    "PopulationDynamics",
    "StrategyDynamics",
    "TimescaleSeparation",
    
    # ESS Solver
    "ESSSolver",
    "MaximumPrinciple",
    "ConvergentStability",
    "InvasionResistance",
    
    # Adaptive Landscape
    "AdaptiveLandscape",
    "LandscapeVisualizer",
    "BifurcationAnalyzer",
    
    # Coevolution
    "CoevolutionSystem",
    "CoupledGFunctions",
    "RedQueenDynamics",
    
    # Empirical Calibration
    "DiscreteOutcomeCalibrator",
    "ParameterEstimator",
    "ModelValidator",
]
