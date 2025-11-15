"""
Agent-Based Modeling (ABM) Module
==================================

Simulates institutional lock-in with parameterized stakeholders for
policy scenario modeling and reform prediction.

Agents:
- Worker: Individual workers with compliance preferences
- Union: Organized labor with militancy parameter (1-10)
- Employer: Business entities with coordination capacity (1-10)
- Legislator: Politicians with reform incentives
- Judge: Judicial actors with doctrine adherence

Source: Extended Phenotype Theory (EPT) - Lerer, I.A. (2025)
"""

from .worker import Worker
from .union import Union
from .employer import Employer
from .legislator import Legislator
from .judge import Judge

__all__ = [
    'Worker',
    'Union',
    'Employer',
    'Legislator',
    'Judge'
]
