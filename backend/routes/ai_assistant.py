"""
AI Assistant Routes
Genspark-powered research assistant for methodology queries
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

# Add backend services to path
sys.path.append(str(Path(__file__).parent.parent))
from services.feature_registry import registry

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message"""
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


class ChatInput(BaseModel):
    """Input for chat query"""
    question: str
    context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[ChatMessage]] = []


@router.post("/query")
async def query_assistant(data: ChatInput):
    """
    Query Genspark research assistant
    
    Provides answers about methodology, formulas, data sources, interpretation
    """
    # Check if feature is enabled
    feature = registry.get_feature("genspark_assistant")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="Genspark Assistant feature is disabled")
    
    # Simulate Genspark response (in production, this would call actual Genspark API)
    response = generate_mock_response(data.question, data.context)
    
    # Track usage
    registry.track_usage("genspark_assistant")
    
    return {
        "answer": response["answer"],
        "sources": response["sources"],
        "code_examples": response.get("code_examples", []),
        "related_questions": response.get("related_questions", []),
        "generated_at": datetime.now().isoformat()
    }


def generate_mock_response(question: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Generate mock Genspark response
    
    In production, this would call Genspark API or use LangChain for RAG
    """
    question_lower = question.lower()
    
    # CLI calculation questions
    if "cli" in question_lower and ("calculate" in question_lower or "formula" in question_lower):
        if "cultural" in question_lower:
            return {
                "answer": """**CLI_cultural (Cultural Lock-In Index)** is calculated using the formula:

```
CLI_cultural = 0.40 × CT1 + 0.30 × CT2 + 0.30 × CT3
```

Where:
- **CT1** = Cultural Transmission - Narrative Stability (0.0-1.0)
- **CT2** = Cultural Transmission - Shock Resistance (0.0-1.0)
- **CT3** = Cultural Transmission - Policy Continuity (0.0-1.0)

The weights reflect that **narrative stability (40%)** is the PRIMARY mechanism of cultural transmission according to Extended Phenotype Theory (EPT).

**Example**:
For Somalia Federal: CT1=0.40, CT2=0.25, CT3=0.35
CLI_cultural = 0.40×0.40 + 0.30×0.25 + 0.30×0.35 = **0.34**""",
                "sources": ["APPENDICES_SPECIFICATIONS.md - Appendix D, Section D.1"],
                "code_examples": [
                    {
                        "language": "python",
                        "code": """def calculate_cli_cultural(CT1, CT2, CT3):
    return 0.40 * CT1 + 0.30 * CT2 + 0.30 * CT3

# Example
cli_cultural = calculate_cli_cultural(0.40, 0.25, 0.35)
print(f"CLI_cultural: {cli_cultural:.3f}")  # Output: 0.340"""
                    }
                ],
                "related_questions": [
                    "What are data sources for CT1 (Narrative Stability)?",
                    "How is CLI_cultural different from CLI?",
                    "What is Extended Phenotype Theory (EPT)?"
                ]
            }
        else:
            return {
                "answer": """**CLI (Constitutional Lock-In Index)** is calculated using:

```
CLI = 0.35 × CE + 0.40 × UA + 0.25 × JPI
```

Where:
- **CE** = Constitutional Entrenchment (0.0-1.0)
- **UA** = Unilateral Amendment difficulty (0.0-1.0)
- **JPI** = Judicial Power Index (0.0-1.0)

**Interpretation**:
- CLI ≥ 0.70: HIGH Lock-In (very rigid)
- CLI 0.50-0.70: MEDIUM Lock-In (moderately rigid)
- CLI < 0.50: LOW Lock-In (flexible)

**Example**:
For Somalia Federal: CE=0.80, UA=0.85, JPI=0.55
CLI = 0.35×0.80 + 0.40×0.85 + 0.25×0.55 = **0.76** (HIGH)""",
                "sources": ["CLI_FRAMEWORK.md", "FEATURE_INVENTORY.md"],
                "code_examples": [
                    {
                        "language": "python",
                        "code": """def calculate_cli(CE, UA, JPI):
    return 0.35 * CE + 0.40 * UA + 0.25 * JPI

# Example
cli = calculate_cli(0.80, 0.85, 0.55)
print(f"CLI: {cli:.3f}")  # Output: 0.760"""
                    }
                ],
                "related_questions": [
                    "What is Constitutional Entrenchment (CE)?",
                    "How do I collect data for UA (Unilateral Amendment)?",
                    "What is the Dual-Index Framework?"
                ]
            }
    
    # Data sources questions
    elif "data source" in question_lower and "ct1" in question_lower:
        return {
            "answer": """**Data sources for CT1 (Narrative Stability)**:

1. **Constitutional Preambles**: Textual analysis of founding narratives
   - Extract key phrases, symbols, historical references
   - Measure stability across constitutional versions

2. **Public Opinion Surveys**:
   - **World Values Survey**: Questions on trust in constitution, national identity
   - **Afrobarometer** (Africa): Constitutional legitimacy questions
   - **Latinobarómetro** (Latin America): Institutional trust metrics

3. **Historical Documents**:
   - Independence declarations
   - Peace agreements
   - Presidential speeches referencing founding principles

**Operationalization**:
- Score 0.8-1.0: Narratives unchanged 50+ years, high public recognition
- Score 0.5-0.7: Some narrative evolution, moderate recognition
- Score 0.0-0.4: Frequent narrative changes, low recognition

**Example**: Uruguay's 1830 founding narrative persists in 2025 → CT1 ≈ 0.80""",
            "sources": ["APPENDICES_SPECIFICATIONS.md - Appendix D, Section D.3"],
            "related_questions": [
                "What about data sources for CT2 (Shock Resistance)?",
                "How do I code constitutional preambles?",
                "What if survey data is unavailable for my country?"
            ]
        }
    
    # Brittle Rigidity questions
    elif "brittle rigidity" in question_lower or ("profile" in question_lower and "dual" in question_lower):
        return {
            "answer": """**Brittle Rigidity** occurs when:
- CLI ≥ 0.60 (high constitutional lock-in)
- CLI_cultural < 0.60 (weak cultural foundation)
- Interaction score < 0.30 (HIGH COLLAPSE RISK)

**Metaphor**: "Scaffold without foundation"
- Rigid constitutional structure (CLI high)
- NO cultural support (CLI_cultural low)
- Result: Formal institutions lack legitimacy, vulnerable to collapse

**Example**: Somalia Federal
- CLI = 0.76 (rigid 2012 Constitution)
- CLI_cultural = 0.34 (weak cultural transmission)
- Interaction = 0.76 × 0.34 = 0.26 (BELOW 0.30 threshold)
- **Profile**: Brittle Rigidity → HIGH COLLAPSE RISK

**Contrast**: Somalilandia
- CLI = 0.54 (flexible)
- CLI_cultural = 0.70 (strong cultural foundation)
- Interaction = 0.38 (ABOVE 0.30 threshold)
- **Profile**: Adaptive Stability → LOW RISK""",
            "sources": ["SECTION6_BRITTLE_RIGIDITY_DISCUSSION.md", "FEATURE_INVENTORY.md"],
            "related_questions": [
                "What are the other three institutional profiles?",
                "How do I move from Brittle Rigidity to Adaptive Stability?",
                "What is the collapse risk threshold (0.30)?"
            ]
        }
    
    # Rootfinder questions
    elif "rootfinder" in question_lower or "genealogy" in question_lower:
        return {
            "answer": """**Rootfinder** traces constitutional genealogy to identify origin clauses.

**How it works**:
1. **Input**: Current constitutional provision (e.g., "Art. 14 Argentine Constitution 2025")
2. **Search**: Historical constitutions (1853, 1949, 1956, 1994)
3. **Match**: Use NLP (TF-IDF, embeddings) to find semantic similarities
4. **Classify**:
   - **Living Fossil**: Unchanged 100+ years (e.g., Art. 14: 172 years)
   - **Mutation**: Minor textual changes
   - **Extinction Event**: Provision removed/suspended

**Example**: Argentine Art. 14 (Freedom of work)
- **Root**: 1853 Constitution, Art. 14
- **Genealogy**: 1853 → 1949 (suspended) → 1956 (reinstated) → 1994 (confirmed) → 2025
- **Classification**: Living Fossil (unchanged text, 172 years)
- **Survival rate**: 100%

**Use cases**:
- Legal: Build historical arguments in constitutional litigation
- Policy: Identify provisions safe to preserve vs ripe for reform
- Academic: Map constitutional diffusion across regions""",
            "sources": ["FEATURE_INVENTORY.md - Rootfinder", "DEPLOYMENT_GUIDE.md"],
            "related_questions": [
                "How accurate is Rootfinder's NLP matching?",
                "Can Rootfinder work across countries (e.g., Argentina → Chile)?",
                "What is the Constitutional Paleontology Tool?"
            ]
        }
    
    # Default response
    else:
        return {
            "answer": f"""I'm Genspark, your research assistant for constitutional analysis and policy intelligence!

**I can help with**:
- 📊 **Formulas**: CLI, CLI_cultural, Dual-Index calculations
- 📚 **Data Sources**: CT1, CT2, CT3 operationalization, survey data
- 🔍 **Methodology**: Rootfinder, EPT application, statistical validation
- 💻 **Code**: Python examples for all calculations
- 📖 **Literature**: Constitutional law, evolutionary theory, game theory

**Your question**: "{question}"

**Suggested topics**:
- "How is CLI calculated?"
- "What data sources for CT1 (Narrative Stability)?"
- "Explain Brittle Rigidity profile"
- "How does Rootfinder work?"
- "Show me Python code for Dual-Index analysis"

Feel free to ask specific questions about methodology, formulas, or use cases!""",
            "sources": ["FEATURE_INVENTORY.md", "AI_DEVOPS_ENHANCEMENT_PROPOSAL.md"],
            "related_questions": [
                "How is CLI calculated?",
                "What is the Dual-Index Framework?",
                "How do I use Rootfinder?",
                "Show me code examples for CLI calculation"
            ]
        }


@router.get("/knowledge-base")
async def get_knowledge_base():
    """Get available knowledge base topics"""
    return {
        "topics": [
            {
                "category": "Formulas & Calculations",
                "items": [
                    "CLI (Constitutional Lock-In Index)",
                    "CLI_cultural (Cultural Lock-In Index)",
                    "Dual-Index Framework",
                    "Collapse Risk Threshold"
                ]
            },
            {
                "category": "Theoretical Frameworks",
                "items": [
                    "Extended Phenotype Theory (EPT)",
                    "Brittle Rigidity vs Adaptive Stability",
                    "Constitutional Paleontology",
                    "Legal Evolvability Golden Ratio"
                ]
            },
            {
                "category": "Methodologies",
                "items": [
                    "Rootfinder (Constitutional Genealogy)",
                    "Data Collection Protocols",
                    "Statistical Validation",
                    "Robustness Checks"
                ]
            },
            {
                "category": "Data Sources",
                "items": [
                    "CT1: Narrative Stability (World Values Survey, Afrobarometer)",
                    "CT2: Shock Resistance (Uppsala Conflict Data, Polity IV)",
                    "CT3: Policy Continuity (Executive turnover, legislative stability)",
                    "CLI Components: CE, UA, JPI"
                ]
            }
        ]
    }
