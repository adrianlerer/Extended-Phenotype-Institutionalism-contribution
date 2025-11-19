"""
Data & Code Cards for Reproducibility
"""

from typing import Dict, List, Any
from datetime import datetime
import sys
import platform

def generate_data_card(
    dataset_sources: List[str],
    filtering_applied: str,
    missing_data: str,
    limitations: List[str]
) -> Dict[str, Any]:
    """
    Generate data card for transparency.
    
    Args:
        dataset_sources: List of data source URLs/citations
        filtering_applied: Description of filtering
        missing_data: How missing data was handled
        limitations: Known limitations
    
    Returns:
        Data card dictionary
    """
    return {
        "data_card_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "dataset_sources": dataset_sources,
        "filtering_applied": filtering_applied,
        "missing_data_handling": missing_data,
        "known_limitations": limitations,
        "bias_assessment": "Manual review required - AI-generated analysis"
    }

def generate_code_card(
    tools_used: List[str],
    random_seeds: Dict[str, int],
    dependencies: Dict[str, str]
) -> Dict[str, Any]:
    """
    Generate code card for reproducibility.
    
    Args:
        tools_used: List of tool names
        random_seeds: Seeds used for each tool
        dependencies: Package versions
    
    Returns:
        Code card dictionary
    """
    return {
        "code_card_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "tools_used": tools_used,
        "random_seeds": random_seeds,
        "dependencies": dependencies,
        "python_version": sys.version,
        "platform": platform.platform(),
        "reproducibility_notes": "All code available in mcp_server/ directory"
    }

def generate_disclosure_statement() -> str:
    """Generate AI-assisted research disclosure"""
    return """
## AI-Assisted Research Disclosure

This research was conducted using the Legal Evolution Unified MCP Server, 
which integrates AI tools for:

1. Citation extraction (LLM-powered via OpenRouter)
2. Doctrine classification (LLM-powered)
3. Genealogical analysis (RootFinder - ABAN algorithm)
4. Competitive dynamics modeling (Memespace - Lotka-Volterra)
5. Constitutional Lock-in Index calculation (CLI Calculator)

All AI-generated content was validated against primary sources where possible.
Preregistration certificate and reproducibility package available upon request.

**Compliance**: Guardian Protocol v1.0 (inspired by AI Scientist v2, arXiv:2504.08066)
"""

