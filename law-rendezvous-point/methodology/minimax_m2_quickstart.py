"""
MiniMax-M2 Integration - Quickstart Examples
============================================

Ejemplos prácticos de integración de MiniMax-M2 con el sistema unificado IusMorfos.

Requisitos:
    pip install openai  # Compatible con MiniMax API
    
Setup:
    export MINIMAX_API_KEY="your-api-key-here"
    export MINIMAX_BASE_URL="https://api.minimax.chat/v1"
    
Uso:
    python minimax_m2_quickstart.py
"""

import os
import json
from typing import List, Dict, Optional
from openai import OpenAI


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Opción 1: API de MiniMax (gratis temporalmente)
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "dummy")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")

# Opción 2: Local deployment con vLLM
LOCAL_BASE_URL = "http://localhost:8000/v1"

# Cliente global
client = OpenAI(
    base_url=MINIMAX_BASE_URL,  # Cambiar a LOCAL_BASE_URL para uso local
    api_key=MINIMAX_API_KEY
)


# ============================================================================
# EJEMPLO 1: THREE-PASS METHOD - PASS 1 (BIRD'S EYE VIEW)
# ============================================================================

def analyze_paper_pass1(
    paper_text: str,
    title: str,
    authors: str,
    year: int,
    journal: str
) -> Dict:
    """
    Automatiza PASS 1 del Three-Pass Method usando MiniMax-M2.
    
    Extrae las Five C's en 5-10 minutos:
    - Category
    - Context
    - Correctness
    - Contributions
    - Clarity
    
    Args:
        paper_text: Texto completo del paper (abstract + intro + conclusions mínimo)
        title: Título del paper
        authors: Autores (formato: "Lastname, F., Lastname2, F.")
        year: Año de publicación
        journal: Revista o conferencia
    
    Returns:
        Dict con Five C's + decisión (READ/CITE/DISCARD/MONITOR)
    """
    
    prompt = f"""
You are an expert academic paper analyst specializing in:
- Legal theory and compliance
- Evolutionary biology and anthropology  
- AI/ML research

**YOUR TASK:** Analyze this paper using Keshav's Three-Pass Method (PASS 1 ONLY).

---

## PAPER METADATA

- **Title:** {title}
- **Authors:** {authors}
- **Year:** {year}
- **Journal:** {journal}

---

## PAPER CONTENT (First 8,000 characters)

{paper_text[:8000]}

---

## ANALYSIS INSTRUCTIONS

Answer the **Five C's** (5-10 minutes maximum):

### 1. CATEGORY
What type of paper is this?
- Measurement paper
- Analysis paper  
- Systems/implementation paper
- Theoretical/conceptual paper
- Legal-doctrinal paper
- Empirical study
- Literature review
- Other (specify)

### 2. CONTEXT
Which theories/frameworks does this paper build on?
List 3-5 key references/concepts the paper assumes you already know.

### 3. CORRECTNESS
Do the assumptions and methodology appear valid?
- Any obvious flaws?
- Are claims supported by evidence?
- Is the reasoning sound?

### 4. CONTRIBUTIONS
What are the paper's main claims/contributions?
State in 3 bullet points maximum.

### 5. CLARITY
Is the paper well-written?
- Excellent: Clear, well-structured, easy to follow
- Good: Minor issues but generally understandable
- Acceptable: Significant effort needed to understand
- Poor: Confusing, poorly structured, hard to follow

---

## DECISION

Based on your analysis, recommend ONE action:

- **READ IN DEPTH** (PASS 2): Highly relevant, worth detailed analysis
- **CITE ONLY**: Relevant but don't need to deep-dive  
- **DISCARD**: Not relevant to current research
- **MONITOR**: Bookmark for future review (potentially relevant later)

---

## OUTPUT FORMAT

Respond in **valid JSON** with this exact structure:

{{
  "category": "string",
  "context": ["reference1", "reference2", "reference3"],
  "correctness": {{
    "assessment": "valid|flawed|uncertain",
    "notes": "brief explanation"
  }},
  "contributions": ["contribution1", "contribution2", "contribution3"],
  "clarity": "excellent|good|acceptable|poor",
  "decision": "READ|CITE|DISCARD|MONITOR",
  "rationale": "1-2 sentence explanation of decision",
  "estimated_reading_time": "X hours for PASS 2 (if READ decision)"
}}

**IMPORTANT:** Output ONLY valid JSON, no markdown formatting.
"""
    
    response = client.chat.completions.create(
        model="MiniMax-M2",
        messages=[
            {"role": "system", "content": "You are an expert academic paper analyst. Respond in valid JSON format only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # Lower temperature for analytical consistency
        max_tokens=2048
    )
    
    # Parse response
    content = response.choices[0].message.content
    
    # Extract JSON from response (handle markdown code blocks)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    
    try:
        result = json.loads(content.strip())
        
        # Add thinking process if available (MiniMax-M2 specific)
        if hasattr(response.choices[0].message, 'thinking'):
            result['thinking_process'] = response.choices[0].message.thinking
        
        return result
    
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse JSON response",
            "raw_response": content,
            "exception": str(e)
        }


# ============================================================================
# EJEMPLO 2: LITERATURE SEARCH AGENT (LEGAL RUBICON)
# ============================================================================

def search_literature_with_tools(research_question: str) -> Dict:
    """
    Usa MiniMax-M2 con tool calling para búsqueda automatizada de literatura.
    
    El modelo puede invocar múltiples herramientas en paralelo:
    - search_academic_databases
    - extract_paper_metadata
    - summarize_findings
    
    Args:
        research_question: Pregunta de investigación (e.g., "When did shared intentionality evolve?")
    
    Returns:
        Dict con resultados de búsqueda + papers relevantes
    """
    
    tools = [
        {
            "name": "search_academic_databases",
            "description": "Search academic databases for papers relevant to the research question",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query with Boolean operators (AND, OR, NOT)"
                    },
                    "databases": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of databases: ['pubmed', 'google_scholar', 'jstor', 'anthrosource', 'researchgate']"
                    },
                    "date_range": {
                        "type": "object",
                        "properties": {
                            "start_year": {"type": "integer"},
                            "end_year": {"type": "integer"}
                        }
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results per database (default: 20)"
                    }
                },
                "required": ["query", "databases"]
            }
        },
        {
            "name": "extract_paper_metadata",
            "description": "Extract structured metadata from a paper (DOI, abstract, citations, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "Paper identifier (DOI, PubMed ID, or URL)"
                    },
                    "fields_to_extract": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Fields to extract: ['title', 'authors', 'abstract', 'citations', 'references', 'year']"
                    }
                },
                "required": ["paper_id"]
            }
        },
        {
            "name": "summarize_findings",
            "description": "Summarize key findings from retrieved papers relevant to research question",
            "parameters": {
                "type": "object",
                "properties": {
                    "paper_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of paper IDs to summarize"
                    },
                    "focus_aspects": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Aspects to focus on: ['timeline', 'evidence', 'methodology', 'contradictions']"
                    }
                },
                "required": ["paper_ids", "focus_aspects"]
            }
        }
    ]
    
    response = client.chat.completions.create(
        model="MiniMax-M2",
        messages=[
            {
                "role": "system",
                "content": """You are a research assistant specializing in cross-disciplinary literature search.
                
Your expertise covers:
- Evolutionary anthropology
- Paleoanthropology  
- Legal theory and institutions
- Cognitive science

When searching for papers, prioritize:
1. High-impact journals (Nature, Science, PNAS)
2. Foundational works (highly cited)
3. Recent publications (last 5 years for emerging topics)
4. Cross-disciplinary connections
"""
            },
            {
                "role": "user",
                "content": f"""
Research Question: {research_question}

Please help me find relevant literature by:

1. Formulating effective search queries (use Boolean operators)
2. Searching appropriate academic databases
3. Extracting metadata from promising papers
4. Summarizing key findings relevant to the research question

Focus on papers that provide:
- Empirical evidence (fossil records, behavioral experiments)
- Theoretical frameworks (evolution, game theory, legal theory)
- Timeline estimates (if asking about evolutionary events)
- Contradicting viewpoints (to understand debate)

After your analysis, provide a structured summary of:
- Top 5-10 most relevant papers
- Key findings consensus
- Areas of disagreement/uncertainty
- Recommended next steps for deeper investigation
"""
            }
        ],
        tools=tools,
        tool_choice="auto"
    )
    
    # Parse tool calls (MiniMax-M2 uses XML format)
    tool_calls = parse_minimax_tool_calls(response.choices[0].message.content)
    
    return {
        "research_question": research_question,
        "tool_calls": tool_calls,
        "model_response": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
    }


def parse_minimax_tool_calls(model_output: str) -> List[Dict]:
    """
    Parse tool calls from MiniMax-M2 XML format.
    
    MiniMax-M2 usa formato XML:
    <minimax:tool_call>
    <invoke name="function_name">
    <parameter name="param1">value1</parameter>
    <parameter name="param2">value2</parameter>
    </invoke>
    </minimax:tool_call>
    
    Args:
        model_output: Raw output del modelo
    
    Returns:
        List of parsed tool calls con name y arguments
    """
    import re
    
    if "<minimax:tool_call>" not in model_output:
        return []
    
    tool_calls = []
    
    # Regex patterns
    tool_call_regex = re.compile(r"<minimax:tool_call>(.*?)</minimax:tool_call>", re.DOTALL)
    invoke_regex = re.compile(r"<invoke name=(.*?)</invoke>", re.DOTALL)
    parameter_regex = re.compile(r"<parameter name=(.*?)</parameter>", re.DOTALL)
    
    # Extract all tool_call blocks
    for tool_call_match in tool_call_regex.findall(model_output):
        # Extract all invokes in this block
        for invoke_match in invoke_regex.findall(tool_call_match):
            # Extract function name
            name_match = re.search(r'^([^>]+)', invoke_match)
            if not name_match:
                continue
            
            function_name = name_match.group(1).strip().strip('"').strip("'")
            
            # Extract parameters
            param_dict = {}
            for match in parameter_regex.findall(invoke_match):
                param_match = re.search(r'^([^>]+)>(.*)', match, re.DOTALL)
                if param_match:
                    param_name = param_match.group(1).strip().strip('"').strip("'")
                    param_value = param_match.group(2).strip()
                    
                    # Try to parse as JSON if it looks like JSON
                    if param_value.startswith(('[', '{')):
                        try:
                            param_value = json.loads(param_value)
                        except json.JSONDecodeError:
                            pass  # Keep as string
                    
                    param_dict[param_name] = param_value
            
            tool_calls.append({
                "name": function_name,
                "arguments": param_dict
            })
    
    return tool_calls


# ============================================================================
# EJEMPLO 3: EGT FRAMEWORK DEBUG AGENT
# ============================================================================

def debug_pytest_failure(
    test_file: str,
    test_output: str,
    max_iterations: int = 3
) -> Dict:
    """
    Usa MiniMax-M2 como agente de debugging para fallos en pytest.
    
    El modelo puede:
    1. Leer archivos de código fuente
    2. Ejecutar pytest con opciones específicas
    3. Hacer edits focalizados
    4. Verificar que el fix funciona
    
    Args:
        test_file: Path al archivo de test que falló
        test_output: Output completo del pytest failure
        max_iterations: Máximo número de intentos de fix
    
    Returns:
        Dict con diagnóstico + fix propuesto + validación
    """
    
    tools = [
        {
            "name": "read_file",
            "description": "Read contents of a source file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute or relative path to file"
                    }
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "run_pytest",
            "description": "Execute pytest on specific test file",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_file": {"type": "string"},
                    "verbose": {"type": "boolean"},
                    "capture": {
                        "type": "string",
                        "enum": ["yes", "no"],
                        "description": "Capture stdout/stderr (yes) or show in real-time (no)"
                    },
                    "stop_on_first_failure": {"type": "boolean"}
                },
                "required": ["test_file"]
            }
        },
        {
            "name": "propose_fix",
            "description": "Propose a code fix for the identified issue",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "line_number": {"type": "integer"},
                    "old_code": {
                        "type": "string",
                        "description": "Code to be replaced (exact match required)"
                    },
                    "new_code": {
                        "type": "string",
                        "description": "New code to replace old_code"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Brief explanation of why this fix works"
                    }
                },
                "required": ["file_path", "old_code", "new_code", "explanation"]
            }
        }
    ]
    
    response = client.chat.completions.create(
        model="MiniMax-M2",
        messages=[
            {
                "role": "system",
                "content": """You are an expert Python debugger specializing in:
- Scientific computing (NumPy, SciPy, pytest)
- Game theory implementations
- Numerical optimization

Your debugging methodology:
1. Read the failing test carefully
2. Read the source code being tested
3. Identify the root cause (expected vs. actual behavior)
4. Propose a minimal, targeted fix
5. Verify the fix doesn't break other tests

Always explain your reasoning using <think> tags.
"""
            },
            {
                "role": "user",
                "content": f"""
A pytest test has failed. Please debug it systematically.

**TEST FILE:** `{test_file}`

**FAILURE OUTPUT:**
```
{test_output}
```

**YOUR TASK:**

1. **Read the test file** to understand what's being tested
2. **Identify the source code** being tested (likely in `src/` directory)
3. **Read the source code** to understand the implementation
4. **Diagnose the root cause:**
   - Is it a logic error?
   - Numerical precision issue?
   - Missing edge case handling?
   - Incorrect test expectations?
5. **Propose a fix** with explanation
6. **Verify** the fix would work (read additional context if needed)

**IMPORTANT:** 
- Make minimal changes (don't refactor unrelated code)
- Preserve existing test coverage
- If the test expectations are wrong (not the code), say so explicitly
"""
            }
        ],
        tools=tools,
        tool_choice="auto",
        max_tokens=8192  # Longer output for debugging sessions
    )
    
    tool_calls = parse_minimax_tool_calls(response.choices[0].message.content)
    
    return {
        "test_file": test_file,
        "diagnosis": response.choices[0].message.content,
        "tool_calls": tool_calls,
        "iterations_used": 1,  # Would implement multi-iteration loop here
        "status": "fix_proposed" if any(tc['name'] == 'propose_fix' for tc in tool_calls) else "diagnosis_only"
    }


# ============================================================================
# EJEMPLO 4: BATCH PROCESSING (PASS 1 EN MÚLTIPLES PAPERS)
# ============================================================================

def batch_analyze_papers(papers: List[Dict]) -> List[Dict]:
    """
    Analiza múltiples papers en paralelo usando MiniMax-M2.
    
    Aprovecha la eficiencia del modelo (10B activations) para procesar
    muchos papers simultáneamente.
    
    Args:
        papers: Lista de dicts con {title, authors, year, journal, text}
    
    Returns:
        Lista de análisis PASS 1 para cada paper
    """
    import concurrent.futures
    
    # Process in parallel (MiniMax-M2 tiene baja latencia, ideal para batch)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(
                analyze_paper_pass1,
                paper['text'],
                paper['title'],
                paper['authors'],
                paper['year'],
                paper['journal']
            )
            for paper in papers
        ]
        
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    return results


# ============================================================================
# MAIN: EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("MiniMax-M2 Integration Examples")
    print("=" * 80)
    
    # Ejemplo 1: Analizar paper de Tomasello (2012)
    print("\n[EJEMPLO 1] Three-Pass Method - PASS 1")
    print("-" * 80)
    
    tomasello_abstract = """
    Two Key Steps in the Evolution of Human Cooperation
    
    The biological and cultural evolution of human cooperation involves two key
    steps. The first step is shared intentionality, which emerged in our
    early evolutionary history (~2 million years ago) as individuals began to
    collaborate in ways requiring joint attention and shared goals. This
    cognitive capacity enabled collaborative foraging and defense. The second
    step is collective intentionality, which emerged more recently (~200,000
    years ago) as groups formed shared norms, institutions, and cultural
    identities. This paper reviews evidence from developmental psychology,
    comparative primatology, and paleoanthropology supporting this two-step
    model.
    """
    
    result = analyze_paper_pass1(
        paper_text=tomasello_abstract,
        title="Two Key Steps in the Evolution of Human Cooperation",
        authors="Tomasello, M.",
        year=2012,
        journal="Current Anthropology",
    )
    
    print(json.dumps(result, indent=2))
    
    # Ejemplo 2: Búsqueda de literatura
    print("\n\n[EJEMPLO 2] Literature Search Agent")
    print("-" * 80)
    
    search_result = search_literature_with_tools(
        "When did shared intentionality evolve in human ancestors?"
    )
    
    print(f"Research Question: {search_result['research_question']}")
    print(f"Tool Calls Detected: {len(search_result['tool_calls'])}")
    for tc in search_result['tool_calls']:
        print(f"  - {tc['name']}: {list(tc['arguments'].keys())}")
    
    # Ejemplo 3: Debug agent (simulado)
    print("\n\n[EJEMPLO 3] Debug Agent (Simulated)")
    print("-" * 80)
    print("(Ejemplo completo requiere pytest failure real)")
    print("Ver función debug_pytest_failure() para implementación completa")
    
    # Ejemplo 4: Batch processing (simulado)
    print("\n\n[EJEMPLO 4] Batch Processing")
    print("-" * 80)
    print("(Ejemplo completo requiere dataset de papers)")
    print("Ver función batch_analyze_papers() para implementación completa")
    
    print("\n" + "=" * 80)
    print("✅ Todos los ejemplos completados")
    print("=" * 80)
