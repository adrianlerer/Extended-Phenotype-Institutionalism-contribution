"""
Legal Evolution MCP Server - Core Module
=========================================

Core components for the MCP server including configuration and server initialization.
"""

from .server import LegalEvolutionMCPServer
from .config import ServerConfig, TOOL_CONFIGS, validate_config

__all__ = [
    'LegalEvolutionMCPServer',
    'ServerConfig',
    'TOOL_CONFIGS',
    'validate_config'
]
