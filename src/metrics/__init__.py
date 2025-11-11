"""
Metrics module for Legal Evolution Unified
==========================================

Quantitative metrics for institutional analysis:
- Constitutional Lock-in Index (CLI)
- H/V ratios (Heredity/Variation)
- Legal Evolvability Index (LEI)
"""

from .cli_calculator import (
    calculate_cli,
    predict_reform_success_from_cli,
    compare_jurisdictions,
    calculate_h_v_from_components,
    integrated_analysis,
    CLIComponents,
    CLI_WEIGHTS,
    BENCHMARK_JURISDICTIONS
)

__all__ = [
    'calculate_cli',
    'predict_reform_success_from_cli',
    'compare_jurisdictions',
    'calculate_h_v_from_components',
    'integrated_analysis',
    'CLIComponents',
    'CLI_WEIGHTS',
    'BENCHMARK_JURISDICTIONS'
]
