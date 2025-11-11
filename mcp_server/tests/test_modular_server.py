"""
Tests for Modular MCP Server Architecture
==========================================

Validates that the world-class modular architecture works correctly.
"""

import pytest
import sys
from pathlib import Path

# Add repo root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_core_imports():
    """Test that core modules can be imported."""
    from mcp_server.core import LegalEvolutionMCPServer, ServerConfig
    assert LegalEvolutionMCPServer is not None
    assert ServerConfig is not None


def test_tool_module_imports():
    """Test that all tool modules can be imported."""
    from mcp_server.tools.cli_tools import register_cli_tools
    from mcp_server.tools.egt_tools import register_egt_tools
    from mcp_server.tools.jurisrank_tools import register_jurisrank_tools
    from mcp_server.tools.workflow_tools import register_workflow_tools
    
    assert callable(register_cli_tools)
    assert callable(register_egt_tools)
    assert callable(register_jurisrank_tools)
    assert callable(register_workflow_tools)


def test_config_creation():
    """Test ServerConfig initialization."""
    from mcp_server.core import ServerConfig
    
    config = ServerConfig()
    
    assert config.name == "legal-evolution-unified"
    assert config.version == "1.0.0"
    assert len(config.tools_enabled) == 4
    assert "cli_calculator" in config.tools_enabled
    assert "jurisrank" in config.tools_enabled
    assert "egt_framework" in config.tools_enabled
    assert "workflows" in config.tools_enabled
    assert config.cache_enabled is True
    assert config.cache_ttl == 3600


def test_config_validation():
    """Test config validation."""
    from mcp_server.core import ServerConfig, validate_config
    
    # Valid config
    config = ServerConfig()
    errors = validate_config(config)
    assert len(errors) == 0
    
    # Invalid tool
    config_invalid = ServerConfig(tools_enabled=["invalid_tool"])
    errors = validate_config(config_invalid)
    assert len(errors) > 0
    assert "invalid_tool" in errors[0].lower()


def test_tool_configs():
    """Test tool-specific configurations."""
    from mcp_server.core.config import TOOL_CONFIGS
    
    assert "cli_calculator" in TOOL_CONFIGS
    assert "jurisrank" in TOOL_CONFIGS
    assert "egt_framework" in TOOL_CONFIGS
    assert "workflows" in TOOL_CONFIGS
    
    # Check CLI config
    cli_config = TOOL_CONFIGS["cli_calculator"]
    assert "weights" in cli_config
    assert "empirical_model" in cli_config
    assert cli_config["weights"]["text_vagueness"] == 0.25
    assert cli_config["empirical_model"]["r_squared"] == 0.74
    
    # Check JurisRank config
    jr_config = TOOL_CONFIGS["jurisrank"]
    assert jr_config["damping_factor"] == 0.85
    assert jr_config["temporal_decay"] == 0.05
    
    # Check EGT config
    egt_config = TOOL_CONFIGS["egt_framework"]
    assert "parasitic_advantage" in egt_config
    assert egt_config["parasitic_advantage"]["base"] == 0.12


def test_cache_manager():
    """Test CacheManager functionality."""
    from mcp_server.utils.cache import CacheManager
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(cache_dir=Path(tmpdir), ttl=60)
        
        # Test set and get
        cache.set("test_tool", {"arg1": "value1"}, {"result": "test_result"})
        
        cached_value = cache.get("test_tool", {"arg1": "value1"})
        assert cached_value is not None
        assert cached_value["result"] == "test_result"
        
        # Test cache miss
        miss = cache.get("test_tool", {"arg2": "value2"})
        assert miss is None


def test_validation_utils():
    """Test validation utilities."""
    from mcp_server.utils.validation import (
        validate_input,
        validate_cli_components,
        ValidationError
    )
    
    # Test number validation
    is_valid, error = validate_input(0.5, float, 0.0, 1.0)
    assert is_valid
    assert error == ""
    
    is_valid, error = validate_input(1.5, float, 0.0, 1.0)
    assert not is_valid
    assert "above maximum" in error.lower()
    
    # Test CLI components validation
    valid_components = {
        "text_vagueness": 0.5,
        "judicial_activism": 0.7,
        "treaty_hierarchy": 0.6,
        "precedent_weight": 0.8,
        "amendment_difficulty": 0.4
    }
    is_valid, error = validate_cli_components(valid_components)
    assert is_valid
    
    invalid_components = {
        "text_vagueness": 0.5,
        "judicial_activism": 0.7
        # Missing other components
    }
    is_valid, error = validate_cli_components(invalid_components)
    assert not is_valid
    assert "missing" in error.lower()


def test_cli_calculator_integration():
    """Test that CLI calculator works through the new architecture."""
    from src.metrics.cli_calculator import (
        calculate_cli,
        predict_reform_success_from_cli,
        calculate_h_v_from_components
    )
    
    # Test CLI calculation
    cli = calculate_cli(0.75, 0.95, 0.88, 0.85, 0.70)
    expected = 0.25 * 0.75 + 0.25 * 0.95 + 0.20 * 0.88 + 0.15 * 0.85 + 0.15 * 0.70
    assert abs(cli - expected) < 0.01
    
    # Test prediction - function may return dict or float
    result = predict_reform_success_from_cli(cli)
    if isinstance(result, dict):
        success_prob = result.get('success_probability', result.get('probability', 0))
    else:
        success_prob = result
    # Expected success as fraction (0-1), not percentage
    expected_success = (92 - 89 * cli) / 100  # Convert to fraction
    assert abs(success_prob - expected_success) < 0.01
    
    # Test H/V calculation
    H, V, hv_ratio = calculate_h_v_from_components(
        precedent=0.85,
        rigidity=0.95,
        codification=0.90,
        tenure=0.98,
        federalism=0.15,
        amendment_freq=0.08,
        review=0.25,
        turnover=0.12
    )
    
    expected_H = 0.25 * (0.85 + 0.95 + 0.90 + 0.98)
    expected_V = 0.25 * (0.15 + 0.08 + 0.25 + 0.12)
    
    assert abs(H - expected_H) < 0.01
    assert abs(V - expected_V) < 0.01
    assert abs(hv_ratio - (H / V)) < 0.01


def test_architecture_completeness():
    """Test that all architectural components are present."""
    import os
    from pathlib import Path
    
    mcp_dir = Path(__file__).parent.parent
    
    # Check core directory
    assert (mcp_dir / "core" / "__init__.py").exists()
    assert (mcp_dir / "core" / "server.py").exists()
    assert (mcp_dir / "core" / "config.py").exists()
    
    # Check tools directory
    assert (mcp_dir / "tools" / "__init__.py").exists()
    assert (mcp_dir / "tools" / "cli_tools.py").exists()
    assert (mcp_dir / "tools" / "egt_tools.py").exists()
    assert (mcp_dir / "tools" / "jurisrank_tools.py").exists()
    assert (mcp_dir / "tools" / "workflow_tools.py").exists()
    
    # Check utils directory
    assert (mcp_dir / "utils" / "__init__.py").exists()
    assert (mcp_dir / "utils" / "cache.py").exists()
    assert (mcp_dir / "utils" / "logging.py").exists()
    assert (mcp_dir / "utils" / "validation.py").exists()
    
    # Check docs
    assert (mcp_dir / "README.md").exists()
    assert (mcp_dir / "INSTALLATION.md").exists()


def test_world_class_features():
    """Test that world-class features are present."""
    from mcp_server.core import ServerConfig
    from mcp_server.core.config import TOOL_CONFIGS
    
    # Modular architecture
    config = ServerConfig()
    assert len(config.tools_enabled) >= 4
    
    # Intelligent caching
    assert config.cache_enabled is True
    assert config.cache_ttl > 0
    
    # Comprehensive configuration
    assert len(TOOL_CONFIGS) >= 4
    for tool_name, tool_config in TOOL_CONFIGS.items():
        assert isinstance(tool_config, dict)
        assert len(tool_config) > 0
    
    # Production-ready settings
    assert config.max_workers >= 1
    assert config.timeout_seconds > 0
    assert config.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
