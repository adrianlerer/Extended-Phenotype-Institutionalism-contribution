"""
Fractal Reasoning Protocol (FRP) Module
========================================

Multi-level narrative analysis framework for constitutional and political narratives.

Exports:
    - FractalAnalyzer: Main analysis interface
    - DomainContext: Domain configuration
    - FRPAnalysis: Analysis results container
    - create_constitutional_analyzer: Factory for constitutional analysis
    - create_political_analyzer: Factory for political analysis
"""

from .fractal_analyzer import (
    FractalAnalyzer,
    DomainContext,
    FRPAnalysis,
    FRPLevelOutput,
    FRPPromptGenerator,
    create_constitutional_analyzer,
    create_political_analyzer
)

__all__ = [
    'FractalAnalyzer',
    'DomainContext',
    'FRPAnalysis',
    'FRPLevelOutput',
    'FRPPromptGenerator',
    'create_constitutional_analyzer',
    'create_political_analyzer'
]

__version__ = '1.0.0'
__author__ = 'Legal Evolution Project'
