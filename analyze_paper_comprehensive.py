import os
import json
import time
from openai import OpenAI
from pathlib import Path

# Configuración API
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")
if not MINIMAX_API_KEY:
    raise ValueError("MINIMAX_API_KEY no está configurada")

client = OpenAI(
    base_url="https://api.minimax.io/v1",
    api_key=MINIMAX_API_KEY
)

def parse_response(output):
    """Extrae thinking + JSON de respuesta MiniMax"""
    thinking = ""
    if "<think>" in output and "</think>" in output:
        start = output.index("<think>") + 7
        end = output.index("</think>")
        thinking = output[start:end].strip()
        output = output[:output.index("<think>")] + output[output.index("</think>")+8:]
    
    # Parsear JSON
    import re
    json_match = re.search(r'\{.*\}', output, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            return thinking, data
        except:
            pass
    
    return thinking, None

# Leer paper
paper_text = Path("paper_mapping_back_slope.txt").read_text(encoding='utf-8')

# Metadata
metadata = {
    "titulo": "MAPPING THE BACK SLOPE: GRADUAL ACCUMULATIONS AND REVOLUTIONARY PUNCTUATION IN THE 6-MILLION-YEAR ORIGIN OF LEGAL INSTITUTIONS",
    "autor": "Ignacio Adrian Lerer",
    "afiliacion": "Independent Researcher",
    "fecha": "October 2025",
    "palabras": 18117
}

print("="*80)
print("ANÁLISIS COMPRENSIVO DE PAPER PARA SSRN")
print("="*80)
print(f"\nPaper: {metadata['titulo']}")
print(f"Autor: {metadata['autor']}")
print(f"Palabras: {metadata['palabras']:,}")
print("\n" + "="*80)

# ============================================================================
# ANÁLISIS 1: TRES PASADAS (PASS 1) - Vista de Pájaro
# ============================================================================
print("\n📚 ANÁLISIS 1: MÉTODO TRES PASADAS (PASS 1)")
print("-" * 80)

prompt_pass1 = f"""Sos un revisor académico experto analizando este paper para publicación en SSRN.

METADATA:
Título: {metadata['titulo']}
Autor: {metadata['autor']} (Independent Researcher)
Fecha: {metadata['fecha']}
Longitud: {metadata['palabras']:,} palabras

TEXTO COMPLETO:
{paper_text[:30000]}
[...CONTINUACIÓN DISPONIBLE EN CONTEXTO COMPLETO...]

TAREA: Aplicar PASS 1 del Método de Tres Pasadas (Keshav 2007) - Vista de Pájaro (5-10 min).

Evaluá usando el framework de las Cinco C's:

1. CATEGORÍA: ¿Qué tipo de paper es? (Teórico, Empírico, Revisión sistemática, etc.)

2. CONTEXTO: ¿Sobre qué teorías/frameworks se construye? Identificá los 5-8 trabajos académicos más importantes que cita o debería citar.

3. CORRECCIÓN: ¿La metodología y argumentos son válidos?
   - Fortalezas metodológicas
   - Debilidades o gaps metodológicos
   - Evaluación: "Válido" | "Válido con salvedades" | "Incierto" | "Defectuoso"

4. CONTRIBUCIONES: ¿Cuáles son los claims principales y su novedad?
   - ¿Qué aporta este paper que no haya sido dicho antes?
   - ¿Las contribuciones están claramente articuladas?

5. CLARIDAD: ¿Qué tan bien está escrito para un paper académico?
   - Estructura lógica
   - Calidad de escritura
   - Uso de evidencia
   - Evaluación: "Excelente" | "Bueno" | "Regular" | "Pobre"

6. APTO PARA SSRN: ¿Está listo para publicación o necesita revisión?
   - "PUBLICAR - Listo para SSRN sin cambios mayores"
   - "REVISIÓN MENOR - Necesita ajustes pequeños antes de publicar"
   - "REVISIÓN MAYOR - Necesita trabajo sustancial antes de publicar"
   - "RECHAZAR - No apto para publicación académica"

Respondé en JSON:
{{
  "categoria": "...",
  "contexto": ["Autor (Año) - Contribución clave"],
  "correccion": {{
    "evaluacion": "Válido|Válido con salvedades|Incierto|Defectuoso",
    "fortalezas": ["..."],
    "debilidades": ["..."]
  }},
  "contribuciones": ["Contribución específica 1", "..."],
  "claridad": "Excelente|Bueno|Regular|Pobre",
  "decision_ssrn": "PUBLICAR|REVISIÓN MENOR|REVISIÓN MAYOR|RECHAZAR",
  "justificacion_decision": "Explicación breve de la decisión"
}}"""

start = time.time()
response_pass1 = client.chat.completions.create(
    model="MiniMax-M2",
    messages=[{"role": "user", "content": prompt_pass1}],
    temperature=0.3,
    max_tokens=3000
)
elapsed_pass1 = time.time() - start

thinking_pass1, analysis_pass1 = parse_response(response_pass1.choices[0].message.content)

print(f"⏱️  Tiempo de respuesta: {elapsed_pass1:.2f}s")
print(f"🧠 Proceso de pensamiento: {len(thinking_pass1)} caracteres\n")

if analysis_pass1:
    print(f"📋 CATEGORÍA: {analysis_pass1.get('categoria', 'N/A')}")
    print(f"📊 DECISIÓN SSRN: {analysis_pass1.get('decision_ssrn', 'N/A')}")
    print(f"💡 JUSTIFICACIÓN: {analysis_pass1.get('justificacion_decision', 'N/A')}\n")
    
    print("🎯 CONTRIBUCIONES:")
    for i, contrib in enumerate(analysis_pass1.get('contribuciones', []), 1):
        print(f"   {i}. {contrib}")
    
    print("\n✅ FORTALEZAS:")
    for fortaleza in analysis_pass1.get('correccion', {}).get('fortalezas', []):
        print(f"   • {fortaleza}")
    
    print("\n⚠️  DEBILIDADES:")
    for debilidad in analysis_pass1.get('correccion', {}).get('debilidades', []):
        print(f"   • {debilidad}")
else:
    print("❌ Error: No se pudo parsear JSON de PASS 1")
    print("Respuesta cruda:", response_pass1.choices[0].message.content[:500])

# ============================================================================
# ANÁLISIS 2: RIGOR ACADÉMICO - Evaluación Profunda
# ============================================================================
print("\n" + "="*80)
print("\n🔬 ANÁLISIS 2: RIGOR ACADÉMICO Y EVIDENCIA")
print("-" * 80)

prompt_rigor = f"""Sos un revisor académico especializado en evolución del derecho, antropología evolutiva y teoría institucional.

PAPER: "{metadata['titulo']}" por {metadata['autor']}

TEXTO COMPLETO:
{paper_text[:30000]}
[...CONTINUACIÓN...]

TAREA: Evaluar rigor académico con estándares de peer-review para journals de alto impacto.

Analizá:

1. CALIDAD DE EVIDENCIA:
   - ¿Las claims están respaldadas por evidencia peer-reviewed?
   - ¿Hay claims especulativas presentadas como hechos?
   - ¿La evidencia citada es de alta calidad (Nature, Science, PNAS) o marginal?

2. TIMELINES Y DATACIÓN:
   - ¿Los timelines evolutivos son precisos según consenso académico actual?
   - ¿Hay errores de datación o malinterpretación de evidencia arqueológica?
   - Ej: ¿250,000 años para lenguaje recursivo es defendible? ¿6-7 Mya para reciprocidad?

3. GAPS EN LITERATURA:
   - ¿Qué papers/autores importantes NO están citados pero deberían?
   - ¿Hay debates académicos actuales que el paper ignora?

4. CLAIMS CONTROVERSIALES:
   - ¿Hay claims que expertos del campo considerarían problemáticas?
   - ¿El paper reconoce incertidumbres y debates activos?

5. COHERENCIA TEÓRICA:
   - ¿Extended Phenotype Theory está aplicada correctamente?
   - ¿Punctuated Equilibrium vs. Gradualism están bien representados?
   - ¿Hay contradicciones internas?

Respondé en JSON:
{{
  "calidad_evidencia": {{
    "evaluacion": "Excelente|Buena|Adecuada|Insuficiente",
    "claims_bien_respaldadas": ["..."],
    "claims_debiles": ["Claim específica con problema"]
  }},
  "timelines": {{
    "precisos": ["Timeline que es correcto"],
    "cuestionables": ["Timeline que podría ser problemático"]
  }},
  "gaps_literatura": ["Autor/Trabajo que debería citarse"],
  "claims_controversiales": ["Claim que expertos podrían cuestionar"],
  "coherencia_teorica": {{
    "evaluacion": "Excelente|Buena|Adecuada|Problemática",
    "explicacion": "..."
  }},
  "recomendacion_final": "Breve resumen del rigor académico"
}}"""

start = time.time()
response_rigor = client.chat.completions.create(
    model="MiniMax-M2",
    messages=[{"role": "user", "content": prompt_rigor}],
    temperature=0.3,
    max_tokens=3000
)
elapsed_rigor = time.time() - start

thinking_rigor, analysis_rigor = parse_response(response_rigor.choices[0].message.content)

print(f"⏱️  Tiempo de respuesta: {elapsed_rigor:.2f}s")
print(f"🧠 Proceso de pensamiento: {len(thinking_rigor)} caracteres\n")

if analysis_rigor:
    print(f"📊 CALIDAD DE EVIDENCIA: {analysis_rigor.get('calidad_evidencia', {}).get('evaluacion', 'N/A')}")
    print(f"🧬 COHERENCIA TEÓRICA: {analysis_rigor.get('coherencia_teorica', {}).get('evaluacion', 'N/A')}\n")
    
    print("✅ CLAIMS BIEN RESPALDADAS:")
    for claim in analysis_rigor.get('calidad_evidencia', {}).get('claims_bien_respaldadas', [])[:3]:
        print(f"   • {claim}")
    
    print("\n⚠️  CLAIMS DÉBILES:")
    for claim in analysis_rigor.get('calidad_evidencia', {}).get('claims_debiles', []):
        print(f"   • {claim}")
    
    print("\n📚 GAPS EN LITERATURA:")
    for gap in analysis_rigor.get('gaps_literatura', [])[:5]:
        print(f"   • {gap}")
    
    print("\n🔥 CLAIMS CONTROVERSIALES:")
    for claim in analysis_rigor.get('claims_controversiales', []):
        print(f"   • {claim}")
else:
    print("❌ Error: No se pudo parsear JSON de análisis de rigor")

# ============================================================================
# ANÁLISIS 3: MEJORAS ESPECÍFICAS - Recomendaciones Prácticas
# ============================================================================
print("\n" + "="*80)
print("\n🛠️  ANÁLISIS 3: MEJORAS ESPECÍFICAS PARA SSRN")
print("-" * 80)

prompt_mejoras = f"""Sos un editor académico dando feedback constructivo a un autor antes de publicación.

PAPER: "{metadata['titulo']}" por {metadata['autor']}

CONTEXTO: El autor quiere publicar en SSRN (repositorio académico de papers). Necesita feedback PRÁCTICO y ESPECÍFICO sobre mejoras.

TEXTO COMPLETO:
{paper_text[:30000]}
[...CONTINUACIÓN...]

TAREA: Proveer recomendaciones concretas y accionables organizadas por prioridad.

1. MEJORAS CRÍTICAS (debe hacerse antes de publicar):
   - Errores factuales que deben corregirse
   - Claims sin respaldo que deben eliminarse o respaldarse
   - Problemas estructurales mayores

2. MEJORAS IMPORTANTES (debería hacerse):
   - Citas faltantes que fortalecerían el argumento
   - Secciones que necesitan expansión
   - Clarificaciones necesarias

3. MEJORAS MENORES (nice-to-have):
   - Pulido de escritura
   - Ejemplos adicionales
   - Figuras/tablas sugeridas

4. TÍTULO Y ABSTRACT:
   - ¿El título es efectivo para captar atención académica?
   - ¿El abstract resume bien las contribuciones?
   - Sugerencias específicas de mejora

5. FORTALEZAS A DESTACAR:
   - ¿Qué hace bien este paper que el autor debería enfatizar más?

Respondé en JSON:
{{
  "mejoras_criticas": [
    {{"problema": "...", "solucion": "..."}}
  ],
  "mejoras_importantes": [
    {{"aspecto": "...", "recomendacion": "..."}}
  ],
  "mejoras_menores": ["..."],
  "titulo_abstract": {{
    "titulo_efectivo": true/false,
    "titulo_sugerido": "Si tenés alternativa mejor",
    "abstract_efectivo": true/false,
    "abstract_feedback": "..."
  }},
  "fortalezas_destacar": ["..."],
  "resumen_ejecutivo": "Síntesis breve: ¿Listo para SSRN o necesita trabajo?"
}}"""

start = time.time()
response_mejoras = client.chat.completions.create(
    model="MiniMax-M2",
    messages=[{"role": "user", "content": prompt_mejoras}],
    temperature=0.3,
    max_tokens=3500
)
elapsed_mejoras = time.time() - start

thinking_mejoras, analysis_mejoras = parse_response(response_mejoras.choices[0].message.content)

print(f"⏱️  Tiempo de respuesta: {elapsed_mejoras:.2f}s")
print(f"🧠 Proceso de pensamiento: {len(thinking_mejoras)} caracteres\n")

if analysis_mejoras:
    print("🚨 MEJORAS CRÍTICAS (HACER ANTES DE PUBLICAR):")
    for i, mejora in enumerate(analysis_mejoras.get('mejoras_criticas', []), 1):
        print(f"\n   {i}. PROBLEMA: {mejora.get('problema', 'N/A')}")
        print(f"      SOLUCIÓN: {mejora.get('solucion', 'N/A')}")
    
    print("\n\n⭐ MEJORAS IMPORTANTES (DEBERÍA HACER):")
    for i, mejora in enumerate(analysis_mejoras.get('mejoras_importantes', [])[:5], 1):
        print(f"\n   {i}. {mejora.get('aspecto', 'N/A')}")
        print(f"      → {mejora.get('recomendacion', 'N/A')}")
    
    print("\n\n💪 FORTALEZAS A DESTACAR:")
    for fortaleza in analysis_mejoras.get('fortalezas_destacar', []):
        print(f"   • {fortaleza}")
    
    titulo_data = analysis_mejoras.get('titulo_abstract', {})
    print(f"\n\n📝 TÍTULO: {'✅ Efectivo' if titulo_data.get('titulo_efectivo') else '⚠️  Necesita mejora'}")
    if titulo_data.get('titulo_sugerido'):
        print(f"   Sugerencia: {titulo_data['titulo_sugerido']}")
    
    print(f"\n📄 ABSTRACT: {'✅ Efectivo' if titulo_data.get('abstract_efectivo') else '⚠️  Necesita mejora'}")
    if titulo_data.get('abstract_feedback'):
        print(f"   Feedback: {titulo_data['abstract_feedback']}")
    
    print(f"\n\n{'='*80}")
    print(f"🎯 RESUMEN EJECUTIVO:")
    print(f"{'='*80}")
    print(f"{analysis_mejoras.get('resumen_ejecutivo', 'N/A')}")
else:
    print("❌ Error: No se pudo parsear JSON de mejoras")

# Guardar resultados
results = {
    "metadata": metadata,
    "pass1_analysis": analysis_pass1,
    "rigor_analysis": analysis_rigor,
    "mejoras_analysis": analysis_mejoras,
    "thinking_processes": {
        "pass1": thinking_pass1,
        "rigor": thinking_rigor,
        "mejoras": thinking_mejoras
    },
    "timing": {
        "pass1_seconds": elapsed_pass1,
        "rigor_seconds": elapsed_rigor,
        "mejoras_seconds": elapsed_mejoras,
        "total_seconds": elapsed_pass1 + elapsed_rigor + elapsed_mejoras
    }
}

output_path = Path("paper_analysis_results.json")
output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')

print(f"\n\n{'='*80}")
print(f"✅ Análisis completo guardado en: {output_path}")
print(f"⏱️  Tiempo total: {results['timing']['total_seconds']:.1f}s")
print(f"{'='*80}")
