"""
Guardian Protocol - Preregistration System
Ensures AI-generated research meets academic integrity standards
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Preregistration:
    """Preregistration record for research transparency"""
    
    research_question: str
    hypotheses: List[str]
    tools_used: List[str]
    expected_metrics: Dict[str, str]
    stopping_criteria: str
    timestamp: str
    hash_signature: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Serialize to JSON"""
        return json.dumps(self.to_dict(), indent=2)

def create_preregistration(
    research_question: str,
    hypotheses: List[str],
    tools: List[str],
    expected_metrics: Optional[Dict[str, str]] = None,
    stopping_criteria: str = "Complete all tool executions"
) -> Preregistration:
    """
    Create preregistration certificate before analysis.
    
    This is AI Scientist v2 Guardian Protocol - transparency requirement.
    
    Args:
        research_question: Main research question
        hypotheses: All hypotheses to test (not just successful ones)
        tools: List of tools to be used
        expected_metrics: Expected outcome metrics
        stopping_criteria: When to stop analysis
    
    Returns:
        Preregistration object with cryptographic signature
    """
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    if expected_metrics is None:
        expected_metrics = {
            "cli_score": "0.0-1.0",
            "reform_success": "percentage",
            "genealogy_depth": "integer"
        }
    
    # Create content for hashing
    content = {
        "research_question": research_question,
        "hypotheses": sorted(hypotheses),  # Sort for consistency
        "tools_used": sorted(tools),
        "expected_metrics": expected_metrics,
        "stopping_criteria": stopping_criteria,
        "timestamp": timestamp
    }
    
    # Generate cryptographic hash (SHA-256)
    content_str = json.dumps(content, sort_keys=True)
    hash_signature = hashlib.sha256(content_str.encode()).hexdigest()
    
    return Preregistration(
        research_question=research_question,
        hypotheses=hypotheses,
        tools_used=tools,
        expected_metrics=expected_metrics,
        stopping_criteria=stopping_criteria,
        timestamp=timestamp,
        hash_signature=hash_signature
    )

def verify_preregistration(prereg: Preregistration) -> bool:
    """Verify preregistration hasn't been tampered with"""
    # Recreate hash
    content = {
        "research_question": prereg.research_question,
        "hypotheses": sorted(prereg.hypotheses),
        "tools_used": sorted(prereg.tools_used),
        "expected_metrics": prereg.expected_metrics,
        "stopping_criteria": prereg.stopping_criteria,
        "timestamp": prereg.timestamp
    }
    content_str = json.dumps(content, sort_keys=True)
    expected_hash = hashlib.sha256(content_str.encode()).hexdigest()
    
    return expected_hash == prereg.hash_signature

