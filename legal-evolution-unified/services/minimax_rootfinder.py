"""
MiniMax-Powered RootFinder
Enhanced genealogical tracing with MiniMax-M2 deep reasoning

Combines:
- Original RootFinder's network analysis (Hammurabi)
- MiniMax-M2's advanced reasoning for conceptual connections
- Legal knowledge extraction from cases

Author: Ignacio Adrián Lerer
Enhanced with: MiniMax-M2 (230B MoE via OpenRouter)
"""

import os
import json
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from openai import OpenAI
from pathlib import Path

# Import original RootFinder for network analysis
import sys
sys.path.append(str(Path(__file__).parent.parent / "tools" / "rootfinder"))
from rootfinder import GenealogyNode as OriginalGenealogyNode

logger = logging.getLogger(__name__)

@dataclass
class EnhancedGenealogyNode:
    """
    Enhanced genealogy node with MiniMax-M2 deep analysis.
    """
    case_id: str
    generation: int
    
    # Original RootFinder metrics
    inherited_elements: List[str]
    mutations: List[str]
    inheritance_fidelity: float
    mutation_type: str
    citation_strength: float
    doctrinal_distance: float
    precedential_weight: float
    
    # MiniMax-M2 enhanced analysis
    conceptual_roots: List[Dict]  # Deep historical roots identified by LLM
    doctrinal_reasoning: str  # LLM's analysis of doctrinal connections
    historical_context: str  # Historical legal context
    comparative_insights: List[str]  # Cross-jurisdictional insights
    confidence_score: float  # LLM's confidence in the analysis
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return asdict(self)


class MiniMaxRootFinder:
    """
    Enhanced RootFinder using MiniMax-M2 for deep conceptual analysis.
    
    Capabilities:
    - Traditional genealogical network analysis (Hammurabi)
    - Deep conceptual root identification (MiniMax-M2)
    - Historical legal context extraction
    - Cross-jurisdictional comparative analysis
    - Confidence-weighted reasoning
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize MiniMax-powered RootFinder.
        
        Parameters:
        -----------
        api_key : str, optional
            OpenRouter API key (uses OPENROUTER_API_KEY env var if not provided)
        """
        # Initialize OpenAI client with OpenRouter endpoint
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key required (set OPENROUTER_API_KEY env var)")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        
        self.model = "minimax/minimax-01"  # MiniMax-M2
        self.cache = {}
        
        logger.info("MiniMaxRootFinder initialized with MiniMax-M2")
    
    def find_conceptual_roots(self, 
                            concept: str,
                            jurisdiction: str = "Argentina",
                            context: Optional[str] = None,
                            max_depth: int = 5) -> List[EnhancedGenealogyNode]:
        """
        Find conceptual and historical roots of a legal concept.
        
        Uses MiniMax-M2's deep reasoning to identify:
        - Historical precedents (Roman law, common law, etc.)
        - Doctrinal evolution across jurisdictions
        - Conceptual mutations and adaptations
        - Cross-legal-system influences
        
        Parameters:
        -----------
        concept : str
            Legal concept to trace (e.g., "habeas corpus", "estado de sitio", "emergency powers")
        jurisdiction : str
            Primary jurisdiction (default: "Argentina")
        context : str, optional
            Additional context about the concept or case
        max_depth : int
            Maximum generations to trace back
            
        Returns:
        --------
        List[EnhancedGenealogyNode]
            Genealogical path with enhanced analysis
        """
        cache_key = f"{concept}_{jurisdiction}_{max_depth}"
        if cache_key in self.cache:
            logger.info(f"Using cached analysis for {concept}")
            return self.cache[cache_key]
        
        logger.info(f"Tracing conceptual roots for '{concept}' in {jurisdiction}")
        
        # Build comprehensive prompt with thinking tags
        prompt = self._build_root_analysis_prompt(concept, jurisdiction, context, max_depth)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto en historia jurídica comparada y análisis genealógico de conceptos legales.
Tu tarea es identificar las raíces históricas, doctrinales y conceptuales de instituciones jurídicas, 
rastreando su evolución a través de diferentes sistemas legales y períodos históricos.

Usa <think> tags para tu razonamiento interno antes de responder."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower for more factual/historical accuracy
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse LLM response into structured genealogy
            genealogy = self._parse_genealogy_response(
                analysis_text, 
                concept, 
                jurisdiction
            )
            
            # Cache result
            self.cache[cache_key] = genealogy
            
            logger.info(f"Traced {len(genealogy)} conceptual generations for {concept}")
            return genealogy
            
        except Exception as e:
            logger.error(f"Error tracing conceptual roots: {e}")
            raise
    
    def _build_root_analysis_prompt(self, 
                                   concept: str,
                                   jurisdiction: str,
                                   context: Optional[str],
                                   max_depth: int) -> str:
        """Build comprehensive prompt for root analysis."""
        
        context_section = f"\n\nContexto adicional:\n{context}" if context else ""
        
        prompt = f"""<think>
Debo realizar un análisis genealógico profundo del concepto jurídico "{concept}" en {jurisdiction}.

Pasos a seguir:
1. Identificar el origen histórico más antiguo del concepto
2. Rastrear su evolución a través de sistemas legales (derecho romano, common law, civil law)
3. Identificar mutaciones doctrinales clave
4. Analizar adaptaciones jurisdiccionales específicas
5. Evaluar la fidelidad conceptual en cada generación
6. Identificar precedentes fundacionales

Profundidad máxima: {max_depth} generaciones hacia atrás
</think>

Analiza las raíces históricas y conceptuales del concepto jurídico "{concept}" en {jurisdiction}.{context_section}

Proporciona tu análisis en el siguiente formato JSON estructurado:

{{
  "concept": "{concept}",
  "jurisdiction": "{jurisdiction}",
  "genealogy": [
    {{
      "generation": 0,
      "case_or_source": "Nombre del precedente/fuente más reciente",
      "year_approximate": 0,
      "inherited_elements": ["Elemento 1", "Elemento 2"],
      "mutations": ["Mutación 1", "Mutación 2"],
      "inheritance_fidelity": 0.0,
      "mutation_type": "conservative/incremental/expansive/revolutionary",
      "doctrinal_reasoning": "Explicación de la conexión doctrinal",
      "historical_context": "Contexto histórico relevante",
      "comparative_insights": ["Insight comparativo 1"]
    }}
  ],
  "conceptual_roots": [
    {{
      "source": "Derecho Romano / Common Law / etc.",
      "concept_origin": "Concepto original",
      "year_approximate": -500,
      "key_text": "Corpus Juris Civilis / Magna Carta / etc.",
      "connection_strength": 0.9
    }}
  ],
  "confidence_score": 0.85,
  "notes": "Notas adicionales sobre el análisis"
}}

IMPORTANTE: 
- Sé específico con nombres de casos, textos legales y años
- Usa fidelity entre 0.0 (mutación total) y 1.0 (herencia perfecta)
- Clasifica mutation_type según el grado de cambio doctrinal
- Incluye hasta {max_depth} generaciones en el array "genealogy"
- En conceptual_roots, identifica las fuentes más antiguas (derecho romano, griego, etc.)
"""
        return prompt
    
    def _parse_genealogy_response(self,
                                 response_text: str,
                                 concept: str,
                                 jurisdiction: str) -> List[EnhancedGenealogyNode]:
        """
        Parse MiniMax-M2's JSON response into structured genealogy nodes.
        """
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_text = response_text
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_text = response_text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(json_text)
            
            genealogy = []
            
            # Parse each generation
            for gen_data in data.get("genealogy", []):
                node = EnhancedGenealogyNode(
                    case_id=gen_data.get("case_or_source", "Unknown"),
                    generation=gen_data.get("generation", 0),
                    inherited_elements=gen_data.get("inherited_elements", []),
                    mutations=gen_data.get("mutations", []),
                    inheritance_fidelity=gen_data.get("inheritance_fidelity", 0.5),
                    mutation_type=gen_data.get("mutation_type", "unknown"),
                    citation_strength=1.0,  # Default for LLM-based analysis
                    doctrinal_distance=1.0 - gen_data.get("inheritance_fidelity", 0.5),
                    precedential_weight=gen_data.get("connection_strength", 0.7),
                    conceptual_roots=data.get("conceptual_roots", []),
                    doctrinal_reasoning=gen_data.get("doctrinal_reasoning", ""),
                    historical_context=gen_data.get("historical_context", ""),
                    comparative_insights=gen_data.get("comparative_insights", []),
                    confidence_score=data.get("confidence_score", 0.7)
                )
                genealogy.append(node)
            
            return genealogy
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response text: {response_text}")
            
            # Fallback: create single node with raw analysis
            return [EnhancedGenealogyNode(
                case_id="Analysis_Failed",
                generation=0,
                inherited_elements=[],
                mutations=[],
                inheritance_fidelity=0.0,
                mutation_type="unknown",
                citation_strength=0.0,
                doctrinal_distance=1.0,
                precedential_weight=0.0,
                conceptual_roots=[],
                doctrinal_reasoning=response_text[:500],
                historical_context="Parse error - see doctrinal_reasoning for raw response",
                comparative_insights=[],
                confidence_score=0.0
            )]
    
    def analyze_doctrine_evolution(self,
                                  doctrine: str,
                                  cases: List[str],
                                  jurisdiction: str = "Argentina") -> Dict:
        """
        Analyze how a doctrine evolved across multiple cases.
        
        Parameters:
        -----------
        doctrine : str
            Legal doctrine to analyze
        cases : List[str]
            List of case names/IDs
        jurisdiction : str
            Jurisdiction
            
        Returns:
        --------
        Dict with evolution analysis
        """
        logger.info(f"Analyzing evolution of '{doctrine}' across {len(cases)} cases")
        
        prompt = f"""<think>
Debo analizar cómo evolucionó la doctrina "{doctrine}" a través de {len(cases)} casos en {jurisdiction}.

Análisis requerido:
1. Identificar elementos constantes (núcleo doctrinal)
2. Rastrear mutaciones incrementales
3. Identificar puntos de inflexión (revolutionary changes)
4. Calcular fidelidad promedio de herencia
5. Identificar tendencias evolutivas
</think>

Analiza la evolución de la doctrina jurídica "{doctrine}" a través de estos casos en {jurisdiction}:

{chr(10).join(f"- {case}" for case in cases)}

Proporciona análisis en formato JSON:
{{
  "doctrine": "{doctrine}",
  "core_elements": ["Elemento núcleo 1", "Elemento núcleo 2"],
  "evolutionary_stages": [
    {{
      "stage": 1,
      "cases": ["Caso1", "Caso2"],
      "characteristics": "Descripción de esta etapa",
      "fidelity": 0.9
    }}
  ],
  "mutation_events": [
    {{
      "case": "Caso X",
      "type": "revolutionary/incremental",
      "description": "Qué cambió y por qué"
    }}
  ],
  "overall_fidelity": 0.75,
  "trend": "conservative/progressive/oscillating"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en análisis evolutivo de doctrinas jurídicas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse JSON response
            if "```json" in analysis_text:
                json_text = analysis_text.split("```json")[1].split("```")[0].strip()
            else:
                json_text = analysis_text
            
            return json.loads(json_text)
            
        except Exception as e:
            logger.error(f"Error analyzing doctrine evolution: {e}")
            return {
                "doctrine": doctrine,
                "error": str(e),
                "core_elements": [],
                "evolutionary_stages": [],
                "mutation_events": [],
                "overall_fidelity": 0.0,
                "trend": "unknown"
            }
    
    def compare_legal_traditions(self,
                                concept: str,
                                jurisdictions: List[str]) -> Dict:
        """
        Compare how a legal concept evolved across different traditions.
        
        Parameters:
        -----------
        concept : str
            Legal concept
        jurisdictions : List[str]
            List of jurisdictions to compare
            
        Returns:
        --------
        Dict with comparative analysis
        """
        logger.info(f"Comparing '{concept}' across {len(jurisdictions)} jurisdictions")
        
        prompt = f"""<think>
Debo realizar un análisis comparativo del concepto "{concept}" a través de diferentes tradiciones jurídicas.

Jurisdicciones a comparar: {', '.join(jurisdictions)}

Análisis requerido:
1. Identificar origen común (si existe)
2. Rastrear divergencias entre tradiciones
3. Identificar transplantes legales
4. Analizar adaptaciones culturales/institucionales
5. Evaluar convergencias recientes
</think>

Analiza comparativamente el concepto jurídico "{concept}" en las siguientes jurisdicciones:

{chr(10).join(f"- {j}" for j in jurisdictions)}

Proporciona análisis en formato JSON:
{{
  "concept": "{concept}",
  "common_root": {{
    "source": "Derecho Romano / Common Law / etc.",
    "year_approximate": -500,
    "description": "Descripción del origen común"
  }},
  "jurisdictional_analysis": [
    {{
      "jurisdiction": "Jurisdicción 1",
      "adaptation": "Cómo se adaptó el concepto",
      "key_cases": ["Caso1", "Caso2"],
      "distinctive_features": ["Feature 1"],
      "fidelity_to_root": 0.8
    }}
  ],
  "transplants": [
    {{
      "from": "Jurisdicción A",
      "to": "Jurisdicción B",
      "year_approximate": 1950,
      "mechanism": "colonización/reforma/jurisprudencia"
    }}
  ],
  "convergence_trends": ["Tendencia 1", "Tendencia 2"],
  "divergence_points": ["Punto de divergencia 1"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en derecho comparado y análisis de tradiciones jurídicas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse JSON
            if "```json" in analysis_text:
                json_text = analysis_text.split("```json")[1].split("```")[0].strip()
            else:
                json_text = analysis_text
            
            return json.loads(json_text)
            
        except Exception as e:
            logger.error(f"Error in comparative analysis: {e}")
            return {
                "concept": concept,
                "error": str(e),
                "common_root": {},
                "jurisdictional_analysis": [],
                "transplants": [],
                "convergence_trends": [],
                "divergence_points": []
            }
    
    def export_genealogy(self, 
                        genealogy: List[EnhancedGenealogyNode],
                        output_path: str,
                        format: str = "json"):
        """
        Export enhanced genealogy to file.
        
        Parameters:
        -----------
        genealogy : List[EnhancedGenealogyNode]
            Genealogy to export
        output_path : str
            Output file path
        format : str
            Export format ('json', 'markdown', 'html')
        """
        if format == "json":
            data = [node.to_dict() for node in genealogy]
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# Análisis Genealógico de Concepto Jurídico\n\n")
                
                if genealogy:
                    f.write(f"**Concepto:** {genealogy[0].case_id}\n\n")
                    f.write(f"**Confianza del análisis:** {genealogy[0].confidence_score:.1%}\n\n")
                
                f.write("## Genealogía Conceptual\n\n")
                
                for node in genealogy:
                    f.write(f"### Generación {node.generation}: {node.case_id}\n\n")
                    f.write(f"**Fidelidad de herencia:** {node.inheritance_fidelity:.1%}\n\n")
                    f.write(f"**Tipo de mutación:** {node.mutation_type}\n\n")
                    
                    if node.inherited_elements:
                        f.write(f"**Elementos heredados:**\n")
                        for elem in node.inherited_elements:
                            f.write(f"- {elem}\n")
                        f.write("\n")
                    
                    if node.mutations:
                        f.write(f"**Mutaciones:**\n")
                        for mut in node.mutations:
                            f.write(f"- {mut}\n")
                        f.write("\n")
                    
                    if node.doctrinal_reasoning:
                        f.write(f"**Razonamiento doctrinal:**\n{node.doctrinal_reasoning}\n\n")
                    
                    if node.historical_context:
                        f.write(f"**Contexto histórico:**\n{node.historical_context}\n\n")
                    
                    f.write("---\n\n")
                
                # Add conceptual roots section
                if genealogy and genealogy[0].conceptual_roots:
                    f.write("## Raíces Conceptuales Profundas\n\n")
                    for root in genealogy[0].conceptual_roots:
                        f.write(f"### {root.get('source', 'Unknown')}\n\n")
                        f.write(f"- **Concepto original:** {root.get('concept_origin', 'N/A')}\n")
                        f.write(f"- **Año aproximado:** {root.get('year_approximate', 'N/A')}\n")
                        f.write(f"- **Texto clave:** {root.get('key_text', 'N/A')}\n")
                        f.write(f"- **Fuerza de conexión:** {root.get('connection_strength', 0):.1%}\n\n")
        
        logger.info(f"Genealogy exported to {output_path} ({format} format)")
    
    def clear_cache(self):
        """Clear analysis cache."""
        self.cache.clear()
        logger.info("Cache cleared")
