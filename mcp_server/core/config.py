"""
MCP Server Configuration
=========================

Centralized configuration system for the Legal Evolution MCP Server.
Provides validation, defaults, and tool-specific settings.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pathlib import Path
import os


@dataclass
class ServerConfig:
    """Configuration for Legal Evolution MCP Server."""
    
    # Server identity
    name: str = "legal-evolution-unified"
    version: str = "1.0.0"
    
    # Tool configuration
    tools_enabled: List[str] = field(default_factory=lambda: [
        'cli_calculator',
        'jurisrank',
        'egt_framework',
        'workflows'
    ])
    
    # Cache configuration
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour default
    cache_dir: Optional[Path] = None
    
    # Performance tuning
    max_workers: int = 4
    timeout_seconds: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[Path] = None
    
    # Data paths
    data_dir: Optional[Path] = None
    benchmark_data: Optional[Path] = None
    
    def __post_init__(self):
        """Initialize derived paths after dataclass creation."""
        if self.cache_dir is None:
            self.cache_dir = Path.home() / ".cache" / "legal_evolution_mcp"
        
        if self.data_dir is None:
            # Try to find data relative to server location
            server_root = Path(__file__).parent.parent.parent
            self.data_dir = server_root / "data"
        
        if self.benchmark_data is None and self.data_dir:
            self.benchmark_data = self.data_dir / "benchmarks"
        
        # Ensure directories exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.data_dir:
            self.data_dir.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_env(cls) -> 'ServerConfig':
        """Create configuration from environment variables."""
        config = cls()
        
        # Override from environment
        if cache_ttl := os.getenv('MCP_CACHE_TTL'):
            config.cache_ttl = int(cache_ttl)
        
        if log_level := os.getenv('MCP_LOG_LEVEL'):
            config.log_level = log_level
        
        if cache_enabled := os.getenv('MCP_CACHE_ENABLED'):
            config.cache_enabled = cache_enabled.lower() in ('true', '1', 'yes')
        
        return config


# Tool-specific configurations
TOOL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "cli_calculator": {
        "weights": {
            "text_vagueness": 0.25,
            "judicial_activism": 0.25,
            "treaty_hierarchy": 0.20,
            "precedent_weight": 0.15,
            "amendment_difficulty": 0.15
        },
        "empirical_model": {
            "intercept": 0.92,
            "slope": -0.89,
            "r_squared": 0.74,
            "p_value": 0.001
        },
        "thresholds": {
            "high_lock_in": 0.75,
            "moderate_lock_in": 0.50,
            "low_lock_in": 0.25
        },
        "golden_ratio": {
            "phi": 1.618,
            "optimal_range": (1.0, 2.0),
            "lock_in_threshold": 2.5
        }
    },
    
    "jurisrank": {
        "damping_factor": 0.85,
        "temporal_decay": 0.05,
        "convergence_threshold": 1e-6,
        "max_iterations": 100,
        "fitness_categories": {
            "dominant": 0.75,
            "influential": 0.50,
            "relevant": 0.25,
            "marginal": 0.10
        },
        "persistence_model": {
            "half_life": 20,  # years
            "decay_rate": 0.0347
        }
    },
    
    "egt_framework": {
        "equilibrium_tolerance": 0.01,
        "max_equilibrium_iterations": 1000,
        "parasitic_advantage": {
            "base": 0.12,
            "range": (0.08, 0.16)
        },
        "fitness_matrix": {
            "reformer_vs_reformer": 1.0,
            "reformer_vs_incumbent": 0.3,
            "reformer_vs_parasite": 0.2,
            "incumbent_vs_reformer": 0.8,
            "incumbent_vs_incumbent": 0.6,
            "incumbent_vs_parasite": 0.4,
            "parasite_vs_reformer": 0.9,
            "parasite_vs_incumbent": 0.7,
            "parasite_vs_parasite": 0.5
        }
    },
    
    "workflows": {
        "default_includes": {
            "cli_analysis": True,
            "hv_analysis": True,
            "egt_analysis": True,
            "recommendations": True,
            "benchmarks": True
        },
        "recommendation_thresholds": {
            "critical": 0.80,
            "high": 0.65,
            "moderate": 0.50,
            "low": 0.35
        }
    }
}


def validate_config(config: ServerConfig) -> List[str]:
    """
    Validate server configuration.
    
    Args:
        config: Server configuration to validate
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate tools_enabled
    valid_tools = set(TOOL_CONFIGS.keys())
    for tool in config.tools_enabled:
        if tool not in valid_tools:
            errors.append(f"Invalid tool: {tool}. Valid tools: {valid_tools}")
    
    # Validate cache_ttl
    if config.cache_ttl < 0:
        errors.append(f"cache_ttl must be non-negative, got {config.cache_ttl}")
    
    # Validate max_workers
    if config.max_workers < 1:
        errors.append(f"max_workers must be positive, got {config.max_workers}")
    
    # Validate timeout
    if config.timeout_seconds < 1:
        errors.append(f"timeout_seconds must be positive, got {config.timeout_seconds}")
    
    # Validate log_level
    valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
    if config.log_level.upper() not in valid_levels:
        errors.append(f"Invalid log_level: {config.log_level}. Valid: {valid_levels}")
    
    return errors


def get_tool_config(tool_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific tool.
    
    Args:
        tool_name: Name of the tool
    
    Returns:
        Tool configuration dictionary
    
    Raises:
        KeyError: If tool not found
    """
    if tool_name not in TOOL_CONFIGS:
        raise KeyError(f"No configuration found for tool: {tool_name}")
    
    return TOOL_CONFIGS[tool_name].copy()
