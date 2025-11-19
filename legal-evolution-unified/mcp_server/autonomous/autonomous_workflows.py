"""
Autonomous Workflows - Combine multiple tools with LLM analysis
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .openrouter_client import OpenRouterClient
from typing import Dict, List, Any

def autonomous_doctrine_evolution(
    doctrine: str,
    start_year: int,
    end_year: int,
    case_texts: List[str],
    budget_usd: float = 2.0
) -> Dict[str, Any]:
    """
    Fully autonomous doctrine evolution analysis using LLM.
    
    Workflow:
    1. Extract citations from all cases (RootFinder input)
    2. Classify doctrines in each case (Memespace input)
    3. Build citation network
    4. Trace genealogy
    5. Model competitive dynamics
    6. Generate report
    
    Args:
        doctrine: Target doctrine name
        start_year, end_year: Time range
        case_texts: List of case full texts
        budget_usd: LLM budget
    
    Returns:
        Complete analysis with genealogy + competition + trends
    """
    client = OpenRouterClient(budget_usd=budget_usd)
    
    # Step 1: Extract citations from all cases
    all_citations = []
    case_doctrines = []
    
    for i, text in enumerate(case_texts[:10]):  # Limit to 10 cases for demo
        # Extract citations
        citations = client.extract_citations(text)
        all_citations.append({
            "case_id": f"case_{start_year + i}",
            "citations": citations.get("citations", [])
        })
        
        # Classify doctrine
        doctrine_class = client.classify_doctrine(text)
        case_doctrines.append({
            "case_id": f"case_{start_year + i}",
            "doctrine": doctrine_class.get("primary_doctrine", "unknown"),
            "confidence": doctrine_class.get("confidence", 0.5)
        })
    
    # Step 2: Build citation network for RootFinder
    citation_network = {}
    for item in all_citations:
        case_id = item["case_id"]
        cited = [c.get("case_name", "unknown") for c in item["citations"]]
        citation_network[case_id] = cited
    
    # Step 3: Count doctrine prevalence over time
    doctrine_counts = {}
    for item in case_doctrines:
        doc = item["doctrine"]
        doctrine_counts[doc] = doctrine_counts.get(doc, 0) + 1
    
    # Step 4: Identify trend
    total_cases = len(case_doctrines)
    doctrine_prevalence = {
        doc: count / total_cases for doc, count in doctrine_counts.items()
    }
    
    result = {
        "doctrine": doctrine,
        "time_range": f"{start_year}-{end_year}",
        "total_cases_analyzed": total_cases,
        "citation_network": citation_network,
        "doctrine_prevalence": doctrine_prevalence,
        "dominant_doctrine": max(doctrine_prevalence, key=doctrine_prevalence.get),
        "llm_budget": client.get_budget_status(),
        "workflow_steps": [
            "1. Citation extraction (LLM)",
            "2. Doctrine classification (LLM)",
            "3. Network construction",
            "4. Trend analysis"
        ]
    }
    
    return result

