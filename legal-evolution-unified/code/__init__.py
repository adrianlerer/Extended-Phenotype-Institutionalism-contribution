"""
Legal Evolution Unified - Core Analysis Package

Adapted from peralta-metamorphosis for legal concept analysis.
"""

from .analysis import LegalConceptAnalysis, calculate_legal_fitness
from .bootstrap import BootstrapValidator
# Note: visualization module is large, import on demand

__version__ = "1.0.0"
__author__ = "Legal Evolution Unified Project"

__all__ = [
    'LegalConceptAnalysis',
    'calculate_legal_fitness',
    'BootstrapValidator',
]
