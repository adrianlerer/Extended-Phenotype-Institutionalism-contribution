#!/usr/bin/env python3
"""
MCP Server Test Suite
======================

Tests all tools to ensure they work correctly before deployment.

Usage:
    python mcp_server/test_server.py
"""

import sys
import asyncio
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server import server


async def test_calculate_cli():
    """Test CLI calculation tool."""
    print("\n📊 Testing calculate_cli...")
    
    args = {
        'text_vagueness': 0.75,
        'judicial_activism': 0.95,
        'treaty_hierarchy': 0.88,
        'precedent_weight': 0.85,
        'amendment_difficulty': 0.70
    }
    
    result = await server.call_tool('calculate_cli', args)
    data = json.loads(result[0].text)
    
    assert 'cli_score' in data, "Missing cli_score"
    assert 'success_probability' in data, "Missing success_probability"
    assert 'classification' in data, "Missing classification"
    assert 0 <= data['cli_score'] <= 1, "CLI out of bounds"
    
    print(f"✓ CLI: {data['cli_score']}")
    print(f"✓ Success probability: {data['success_probability']}")
    print(f"✓ Classification: {data['classification']}")
    
    return True


async def test_analyze_jurisdiction():
    """Test jurisdiction analysis tool."""
    print("\n🌍 Testing analyze_jurisdiction...")
    
    for jurisdiction in ['Argentina', 'Brazil', 'Spain']:
        result = await server.call_tool(
            'analyze_jurisdiction', 
            {'jurisdiction': jurisdiction}
        )
        data = json.loads(result[0].text)
        
        assert data['jurisdiction'] == jurisdiction
        assert 'cli_analysis' in data
        assert 'reform_prediction' in data
        
        print(f"✓ {jurisdiction}: CLI={data['cli_analysis']['overall_score']:.3f}, "
              f"Success={data['reform_prediction']['success_percentage']}")
    
    return True


async def test_compare_jurisdictions():
    """Test batch comparison tool."""
    print("\n📈 Testing compare_jurisdictions_batch...")
    
    result = await server.call_tool(
        'compare_jurisdictions_batch',
        {'jurisdictions': ['Argentina', 'Brazil', 'Spain', 'Poland', 'Mexico']}
    )
    data = json.loads(result[0].text)
    
    assert 'comparison' in data
    assert 'summary' in data
    assert len(data['comparison']) == 5
    
    print(f"✓ Compared {len(data['comparison'])} jurisdictions")
    print(f"✓ Most flexible: {data['summary']['most_flexible']}")
    print(f"✓ Most rigid: {data['summary']['most_rigid']}")
    
    return True


async def test_calculate_hv():
    """Test H/V ratio calculation tool."""
    print("\n📐 Testing calculate_hv_ratio...")
    
    # Argentina (lock-in case)
    args = {
        'precedent': 0.85,
        'rigidity': 0.95,
        'codification': 0.90,
        'tenure': 0.98,
        'federalism': 0.15,
        'amendment_freq': 0.08,
        'review': 0.25,
        'turnover': 0.12
    }
    
    result = await server.call_tool('calculate_hv_ratio', args)
    data = json.loads(result[0].text)
    
    assert 'H' in data
    assert 'V' in data
    assert 'ratio' in data
    assert 'd_phi' in data
    assert 'zone' in data
    
    print(f"✓ H: {data['H']}")
    print(f"✓ V: {data['V']}")
    print(f"✓ Ratio: {data['ratio']}")
    print(f"✓ Zone: {data['zone']}")
    
    return True


async def test_list_tools():
    """Test that all tools are registered."""
    print("\n🔧 Testing list_tools...")
    
    tools = await server.list_tools()
    
    assert len(tools) == 4, f"Expected 4 tools, got {len(tools)}"
    
    tool_names = [t.name for t in tools]
    expected = [
        'calculate_cli',
        'analyze_jurisdiction',
        'compare_jurisdictions_batch',
        'calculate_hv_ratio'
    ]
    
    for name in expected:
        assert name in tool_names, f"Tool {name} not found"
        print(f"✓ {name}")
    
    return True


async def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("Legal Evolution MCP Server - Test Suite")
    print("=" * 70)
    
    tests = [
        ("List Tools", test_list_tools),
        ("Calculate CLI", test_calculate_cli),
        ("Analyze Jurisdiction", test_analyze_jurisdiction),
        ("Compare Jurisdictions", test_compare_jurisdictions),
        ("Calculate H/V Ratio", test_calculate_hv),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            await test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ Test '{name}' failed: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("\n✅ All tests passed! Server is ready to use.")
        print("\nNext steps:")
        print("  1. Run: ./mcp_server/install.sh")
        print("  2. Restart Claude Desktop")
        print("  3. Try: 'Analyze Argentina's institutional configuration'")
    else:
        print("\n❌ Some tests failed. Please fix errors before deployment.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
