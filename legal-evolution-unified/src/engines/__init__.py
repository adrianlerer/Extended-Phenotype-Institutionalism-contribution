"""
Legal Engines Module

Integration point for specialized legal analysis tools:
- JurisRank: Legal fitness via citation networks
- RootFinder: Genealogy of legal concepts
- Iusmorfos: Prediction of transplant success

Each engine enhances Peralta's core methods with legal-specific functionality.
"""

from .enhanced_jurisrank import EnhancedJurisRank
from .rootfinder_adapter import RootFinderAdapter
from .iusmorfos_predictor import IusmorfosPredictor

__all__ = [
    'EnhancedJurisRank',
    'RootFinderAdapter',
    'IusmorfosPredictor',
]
