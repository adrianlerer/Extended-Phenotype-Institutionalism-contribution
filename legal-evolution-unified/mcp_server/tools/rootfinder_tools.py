"""
RootFinder Tools for MCP Server
Genealogical tracing of legal doctrines using ABAN algorithm
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.rootfinder.rootfinder import RootFinder, GenealogyNode
import networkx as nx
from typing import Dict, List, Any

# Initialize RootFinder instance (reusable)
_rootfinder_instance = None

def get_rootfinder() -> RootFinder:
    """Get or create RootFinder singleton instance"""
    global _rootfinder_instance
    if _rootfinder_instance is None:
        _rootfinder_instance = RootFinder()
    return _rootfinder_instance

def trace_lineage(
    case_id: str,
    citation_network: Dict[str, List[str]],
    max_depth: int = 3,
    include_mutations: bool = True
) -> Dict[str, Any]:
    """
    Trace genealogical lineage of a legal doctrine.
    
    Args:
        case_id: Target case identifier
        citation_network: Dict mapping case_id -> list of cited cases
        max_depth: Maximum generations to trace back
        include_mutations: Include mutation analysis
    
    Returns:
        Dict with genealogy tree and metrics
    """
    finder = get_rootfinder()
    
    # Convert citation dict to NetworkX graph
    G = nx.DiGraph()
    for source, targets in citation_network.items():
        for target in targets:
            G.add_edge(source, target)
    
    # Run ABAN algorithm
    try:
        genealogy = finder.trace_ancestry(
            G, 
            case_id, 
            max_depth=max_depth
        )
        
        # Extract metrics
        result = {
            "case_id": case_id,
            "total_ancestors": len(genealogy),
            "max_generation": max(n.generation for n in genealogy) if genealogy else 0,
            "average_fidelity": sum(n.inheritance_fidelity for n in genealogy) / len(genealogy) if genealogy else 0,
            "genealogy_tree": [node.to_dict() for node in genealogy],
            "root_cases": [n.case_id for n in genealogy if n.generation == max(n.generation for n in genealogy)],
            "mutation_count": sum(len(n.mutations) for n in genealogy) if include_mutations else 0
        }
        
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "case_id": case_id,
            "total_ancestors": 0
        }

def find_doctrinal_roots(
    cases: List[str],
    citation_network: Dict[str, List[str]],
    min_citations: int = 3
) -> Dict[str, Any]:
    """
    Identify foundational cases (roots) in a citation network.
    
    Args:
        cases: List of case identifiers to analyze
        citation_network: Citation network
        min_citations: Minimum citations to be considered a root
    
    Returns:
        Dict with identified roots and their influence scores
    """
    finder = get_rootfinder()
    
    # Build graph
    G = nx.DiGraph()
    for source, targets in citation_network.items():
        for target in targets:
            G.add_edge(source, target)
    
    # Calculate in-degree (how many cases cite this one)
    in_degrees = dict(G.in_degree())
    
    # Identify roots (highly cited, early cases)
    roots = []
    for case in cases:
        if case in in_degrees and in_degrees[case] >= min_citations:
            # Calculate influence (citations + downstream citations)
            descendants = nx.descendants(G, case) if G.has_node(case) else set()
            influence_score = in_degrees[case] + len(descendants)
            
            roots.append({
                "case_id": case,
                "direct_citations": in_degrees[case],
                "total_descendants": len(descendants),
                "influence_score": influence_score
            })
    
    # Sort by influence
    roots.sort(key=lambda x: x["influence_score"], reverse=True)
    
    return {
        "total_roots": len(roots),
        "roots": roots[:10],  # Top 10
        "network_size": G.number_of_nodes(),
        "total_citations": G.number_of_edges()
    }

# Example citation network for testing
EXAMPLE_ARGENTINA_LABOR = {
    "Vizzoti_2004": ["Aquino_2004", "Milone_1956"],
    "Aquino_2004": ["Gorosito_2002", "Castillo_1985"],
    "Castillo_1985": ["Milone_1956"],
    "Milone_1956": [],
    "Gorosito_2002": ["Castillo_1985"],
    "Madorrán_2007": ["Vizzoti_2004", "Aquino_2004"],
    "Pérez_2009": ["Vizzoti_2004"],
    "Negri_2015": ["Vizzoti_2004", "Madorrán_2007"]
}

def demo_argentina_labor() -> Dict[str, Any]:
    """
    Demonstration: Trace Argentine labor law doctrine from Vizzoti.
    
    This is Smulovitz-style judicialización case study.
    """
    result = trace_lineage(
        case_id="Vizzoti_2004",
        citation_network=EXAMPLE_ARGENTINA_LABOR,
        max_depth=3,
        include_mutations=True
    )
    
    # Add interpretation
    result["interpretation"] = {
        "doctrine": "Núcleo irreductible de derechos laborales",
        "key_precedent": "Vizzoti establishes 'irreducible core' doctrine",
        "williamson_level": 2,  # Institutional environment (decades)
        "cli_component": "Precedent Weight = 0.95 (very high)",
        "judicialización": "Strategic use of law by CGT to block reforms"
    }
    
    return result

