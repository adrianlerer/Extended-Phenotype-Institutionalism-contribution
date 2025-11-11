"""
Legal Evolution Unified - MCP Server
Integrates 10 analytical tools for institutional analysis
"""

__version__ = "1.0.0"
__author__ = "Ignacio Adrian Lerer"

# Tool registry
AVAILABLE_TOOLS = [
    "cli_calculator",           # Constitutional Lock-in Index
    "egt_predictor",            # Evolutionary Game Theory Framework
    "jurisrank_analyzer",       # Citation network fitness
    "rootfinder_genealogy",     # Doctrinal lineage tracing
    "memespace_mapper",         # Lotka-Volterra competition
    "iusmorfos_transplant",     # Legal transplant prediction
    "fibonacci_detector",       # Golden ratio pattern detection
    "psm_causal",              # Propensity Score Matching
    "bootstrap_validator",      # Statistical robustness testing
    "network_visualizer"        # Network analysis & viz
]

# Cross-tool workflows
WORKFLOWS = [
    "full_institutional_analysis",  # All 10 tools chained
    "reform_viability_pipeline",    # CLI → EGT → Bootstrap
    "doctrine_evolution_analysis",  # RootFinder → JurisRank → Memespace
    "transplant_success_prediction" # Iusmorfos → PSM → Bootstrap
]
