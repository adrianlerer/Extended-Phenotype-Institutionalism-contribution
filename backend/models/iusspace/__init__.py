"""
IusSpace Framework - 12-Dimensional Legal System Analysis

This module implements the complete 12-dimensional IusSpace framework from:
- "IusSpace: A 12-Dimensional Framework for Mapping Legal Systems" (SSRN 5557838)
- "JurisRank: PageRank for Legal Doctrines" (SSRN 5405459)

The 12 Dimensions:
1. Constitutional Entrenchment (CE) - Difficulty of formal amendment
2. Ultraactivity (UA) - Persistence beyond formal expiration
3. Judicial Protection Intensity (JPI) - Strength of judicial review
4. Cultural Lock-In (CLI_cultural) - Narrative continuity in legal culture
5. Implementation Gap - Formal passage vs actual compliance
6. Legal Norm Fitness (JurisRank) - Network influence of legal doctrines
7. Network Topology - Graph density of legal system
8. Constitutional Centrality - Betweenness centrality of constitution
9. Reform Velocity - Speed of legal system evolution
10. Crisis Catalysis - Reform acceleration during crises
11. WEIRD Classification - Western, Educated, Industrialized, Rich, Democratic
12. Transplantation Era - Historical period of legal origin

Key Findings:
- WEIRD vs Non-WEIRD predicts implementation gap (r=0.87, Cohen's d=3.749)
- Reform velocity: Pre-digital (45 years) → Digital (3.2 years) = 14x acceleration
- Implementation gap: WEIRD 5.4% vs Non-WEIRD 31.2%
- 85% of global population is Non-WEIRD
"""

from .implementation_gap_detector import (
    ImplementationGapDetector,
    ImplementationGapPredictor,
    ProvisionCompliance
)

from .weird_classifier import (
    WEIRDClassifier,
    WEIRDComponents
)

from .reform_velocity_calculator import (
    ReformVelocityCalculator,
    ReformEvent,
    IusSpaceVector,
    ReformEra
)

from .crisis_catalysis_detector import (
    CrisisCatalysisDetector,
    CrisisEvent,
    CrisisType,
    ReformDuringCrisis
)

from .network_analyzer import (
    NetworkAnalyzer,
    LegalNode,
    LegalEdge,
    NodeType,
    EdgeType
)

from .transplantation_era_classifier import (
    TransplantationEraClassifier,
    TransplantationEra,
    TransplantationContext
)

__all__ = [
    # Implementation Gap (Dimension 5)
    'ImplementationGapDetector',
    'ImplementationGapPredictor',
    'ProvisionCompliance',
    
    # WEIRD Classification (Dimension 11)
    'WEIRDClassifier',
    'WEIRDComponents',
    
    # Reform Velocity (Dimension 9)
    'ReformVelocityCalculator',
    'ReformEvent',
    'IusSpaceVector',
    'ReformEra',
    
    # Crisis Catalysis (Dimension 10)
    'CrisisCatalysisDetector',
    'CrisisEvent',
    'CrisisType',
    'ReformDuringCrisis',
    
    # Network Analysis (Dimensions 7 & 8)
    'NetworkAnalyzer',
    'LegalNode',
    'LegalEdge',
    'NodeType',
    'EdgeType',
    
    # Transplantation Era (Dimension 12)
    'TransplantationEraClassifier',
    'TransplantationEra',
    'TransplantationContext',
]

__version__ = '0.1.0'
