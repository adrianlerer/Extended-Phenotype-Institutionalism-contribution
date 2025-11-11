"""
Tests for CLI Calculator MCP Tools
===================================
"""

import sys
from pathlib import Path

# Add repo to path
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))


def test_cli_calculator_import():
    """Test that underlying CLI calculator works."""
    from src.metrics.cli_calculator import calculate_cli, calculate_h_v_from_components
    
    # Test CLI calculation
    cli = calculate_cli(
        text_vagueness=0.75,
        judicial_activism=0.95,
        treaty_hierarchy=0.88,
        precedent_weight=0.85,
        amendment_difficulty=0.70
    )
    
    expected_cli = 0.25*0.75 + 0.25*0.95 + 0.20*0.88 + 0.15*0.85 + 0.15*0.70
    assert abs(cli - expected_cli) < 0.01, f"CLI mismatch: {cli} vs {expected_cli}"
    
    print(f"✅ CLI calculation works: {cli:.3f}")
    
    # Test H/V calculation
    H, V, ratio = calculate_h_v_from_components(
        precedent=0.85,
        rigidity=0.95,
        codification=0.90,
        tenure=0.98,
        federalism=0.15,
        amendment_freq=0.08,
        review=0.25,
        turnover=0.12
    )
    
    expected_h = 0.25 * (0.85 + 0.95 + 0.90 + 0.98)
    expected_v = 0.25 * (0.15 + 0.08 + 0.25 + 0.12)
    
    assert abs(H - expected_h) < 0.01, f"H mismatch: {H} vs {expected_h}"
    assert abs(V - expected_v) < 0.01, f"V mismatch: {V} vs {expected_v}"
    
    print(f"✅ H/V calculation works: H={H:.3f}, V={V:.3f}, ratio={ratio:.3f}")


def test_mcp_server_structure():
    """Test that MCP server structure is correct."""
    # Check key files exist
    repo_root = Path(__file__).parent.parent.parent
    mcp_root = repo_root / "mcp_server"
    
    required_files = [
        "core/server.py",
        "core/config.py",
        "tools/cli_tools.py",
        "tools/jurisrank_tools.py",
        "tools/egt_tools.py",
        "tools/workflow_tools.py",
        "utils/cache.py",
        "README.md"
    ]
    
    missing = []
    for file_path in required_files:
        full_path = mcp_root / file_path
        if not full_path.exists():
            missing.append(file_path)
    
    if missing:
        print(f"⚠️  Missing files: {missing}")
    
    assert len(missing) == 0, f"Missing {len(missing)} required files"
    
    print("✅ MCP server structure is complete")


if __name__ == "__main__":
    print("Running MCP Server Tests...\n")
    test_cli_calculator_import()
    test_mcp_server_structure()
    print("\n✅ All MCP server tests passed!")
