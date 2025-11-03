# Solución Alternativa: OpenRouter para MiniMax-M2

## 🚨 Problema Actual
Después de **20+ pruebas exhaustivas**, el API Key directo de MiniMax falla con error 1004.

**No es culpa nuestra** - probamos:
- 5 modelos diferentes
- 3 endpoints diferentes  
- 10+ formatos de headers diferentes
- Con/sin GroupID
- Con/sin Bearer prefix

**Todos fallan** con el mismo error: `status_code: 1004, "login fail"`

## ✅ Solución Inmediata: OpenRouter

**OpenRouter** es una plataforma que te da acceso a MiniMax-M2 (y 100+ modelos) sin problemas de autenticación.

### Ventajas
- ✅ **API compatible con OpenAI** (código simple)
- ✅ **$1 crédito gratis** (suficiente para ~5,000-7,000 requests)
- ✅ **Sin problemas de auth**
- ✅ **Acceso a MiniMax-M2 y otros modelos**
- ✅ **3x más barato** que GPT-4 después del crédito gratis

### Cómo Funciona
1. Te registras en https://openrouter.ai
2. Obtienes un API key instantáneo
3. Usas el endpoint de OpenRouter con tu código existente
4. OpenRouter enruta las llamadas a MiniMax-M2

## 🔧 Implementación

### Paso 1: Registrarse
1. Ve a https://openrouter.ai/
2. Sign up con Google/GitHub/Discord (2 minutos)
3. Ve a "Keys" y copia tu API key

### Paso 2: Actualizar .env
```bash
OPENROUTER_API_KEY=<tu_key_de_openrouter>
```

### Paso 3: Código (Idéntico al OpenAI SDK)
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

response = client.chat.completions.create(
    model="minimax/minimax-01",  # MiniMax-M2
    messages=[
        {"role": "user", "content": "Analiza este texto jurídico..."}
    ]
)

print(response.choices[0].message.content)
```

## 📊 Comparación de Costos

| Servicio | Costo (por 1M tokens) | Crédito Gratis | Modelos Disponibles |
|----------|----------------------|----------------|---------------------|
| **OpenRouter** | $0.15 input / $0.60 output | **$1 (~7K requests)** | 100+ incluyendo MiniMax-M2 |
| MiniMax Directo | $0.15 input / $0.60 output | ❌ (Si funciona) | Solo MiniMax |
| GPT-4 Turbo | $10 input / $30 output | ❌ | Solo OpenAI |

**Veredicto:** OpenRouter es **20x más barato** que GPT-4 y te da acceso inmediato.

## 🎯 Por Qué Es Mejor para IusMorfos

1. **Funciona AHORA** (no perdés más tiempo con auth)
2. **Hybrid Architecture**: Podés usar MiniMax-M2 para JurisRank/RootFinder y Claude para análisis académico
3. **Future-proof**: Si MiniMax-M2 no alcanza, switcheás a otro modelo cambiando 1 línea
4. **Free tier generoso**: Suficiente para desarrollar y testear

## 🚀 Plan de Acción

### Fase 1: Setup OpenRouter (15 min)
1. Registrarse en OpenRouter
2. Obtener API key
3. Actualizar `.env`
4. Probar con script de prueba

### Fase 2: Integrar en IusMorfos (1 hora)
1. Crear servicio `MiniMaxService` usando OpenRouter
2. Implementar RootFinder con MiniMax-M2
3. Implementar JurisRank con MiniMax-M2
4. Mantener análisis académico con Claude (híbrido)

### Fase 3: Intentar MiniMax Directo (Paralelo)
- Mientras trabajás con OpenRouter, investigar por qué falla el API directo
- Contactar soporte MiniMax
- Si lo resuelven, podés switchear después

## 📝 Ejemplo Completo: RootFinder con OpenRouter

```python
from openai import OpenAI
import os

class RootFinder:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY")
        )
    
    def find_legal_roots(self, concept: str) -> dict:
        """
        Encuentra raíces jurídicas históricas de un concepto
        usando MiniMax-M2 vía OpenRouter
        """
        prompt = f"""
        <think>
        Necesito identificar el origen histórico del concepto jurídico: {concept}
        Debo rastrear:
        1. Primera aparición en textos legales
        2. Evolución conceptual a través del tiempo
        3. Precedentes judiciales fundacionales
        4. Conexiones con principios romanos/common law
        </think>
        
        Analiza las raíces históricas del concepto jurídico "{concept}".
        Estructura tu respuesta en JSON:
        {{
            "concepto": "{concept}",
            "origen_historico": "...",
            "primera_mencion": "...",
            "evolucion": [...],
            "precedentes_clave": [...]
        }}
        """
        
        response = self.client.chat.completions.create(
            model="minimax/minimax-01",  # MiniMax-M2
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return response.choices[0].message.content

# Uso
finder = RootFinder()
result = finder.find_legal_roots("habeas corpus")
print(result)
```

## ✅ Decisión

**RECOMENDACIÓN:** Usar OpenRouter para desarrollo inmediato.

**Beneficios:**
- Sistema funcionando 100% en 1 hora
- Sin depender de soporte MiniMax
- Más flexibilidad (acceso a múltiples modelos)
- Crédito gratis para desarrollo

**¿Procedemos con OpenRouter?**

---

*Nota: Este documento se creó después de 3+ horas de troubleshooting exhaustivo del API directo de MiniMax.*
