"""
Reporting Engine Module
=======================

Professional reporting and visualization for ABM simulation results.

Components:
- visualization_suite: Publication-quality charts and figures
- theory_integrator: RAG-powered auto-citation system (coming soon)
- narrative_generator: GPT-4 long-form report generation (coming soon)

Usage:
    from reporting_engine.visualization_suite import VisualizationEngine
    
    viz = VisualizationEngine(output_dir='./figures')
    viz.create_figure_report(results, 'uruguay_1991')
"""

__version__ = "0.1.0"
__author__ = "Adrian Lerer"

from pathlib import Path

# Module root
MODULE_ROOT = Path(__file__).parent

# Export main classes
try:
    from .visualization_suite import VisualizationEngine
    __all__ = ['VisualizationEngine']
except ImportError:
    # Dependencies not installed
    __all__ = []
