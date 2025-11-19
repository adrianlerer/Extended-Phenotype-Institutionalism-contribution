# PROMPT PARA GENSPARK: PAPER SSRN - PARTE 2

## IV. SECCIÓN 2: MARCO TEÓRICO (≈4000 palabras)

### 2.1 FORMALIZACIÓN: LA FUNCIÓN DE FILTRADO POR CREDULIDAD

**INSTRUCCIONES:**

**[Subsección 2.1.1 - Definiciones y Supuestos]**

Establecer notación formal (≈500 palabras):

**Definición 1 (Meme Político):**
Un meme político M es una tupla:

```
M = (N, E, D, C)
Donde:
N = Narrativa Central (estructura semántica)
E = Disparadores Emocionales (componentes afectivos)
D = Mecanismos de Defensa (inmunización contra evidencia)
C = Complejidad Cognitiva (costo de procesamiento)
```

**Definición 2 (Población Receptora):**
Población heterogénea con distribución de credulidad:

```
θ ∈ [0,1] donde:
θ = 0: escepticismo extremo (requiere evidencia completa)
θ = 1: credulidad extrema (acepta narrativa sin verificación)
```

**Supuesto 1 (Distribución):**

```
θ ~ Beta(α, β)
Donde parámetros α, β varían por contexto cultural
```

Para Argentina (del paper anterior):

- Bajo capital educativo (PISA 402 vs. OCDE 489)
- Alta desconfianza institucional (28% vs. 51% OCDE)
- → Distribución sesgada hacia mayor θ

**Supuesto 2 (Costos de Conversión):**

```
C_conversión(θ) = C_base + k/θ
```

Donde:

- C_base = costo mínimo de movilización
- k/θ = costo de superar resistencia epistémica (crece cuando θ→0)

**[Subsección 2.1.2 - Función de Utilidad del Propagador de Memes]**

Derivar formalmente (≈800 palabras):

**Objetivo del Propagador:**
Maximizar conversiones netas dado presupuesto finito de recursos.

**Componentes:**

1. **Costo de Transmisión Inicial (C_T):**

```
C_T = c_t × N_broadcast
Donde c_t ≈ 0 en era digital (como email del timo nigeriano)
```

2. **Respuestas Iniciales (R):**

```
R(C) = ∫_{θ_min(C)}^{1} f(θ) dθ
Donde:
θ_min(C) = umbral mínimo de credulidad para aceptar narrativa de complejidad C
```

**Crucial:** Narrativas más simples/absurdas tienen θ_min más alto (filtran más)

3. **Costo de Seguimiento (C_S):**

```
C_S = Σ[i=1 to R] C_conversión(θ_i)
```

4. **Tasa de Abandono (A):**

```
A(θ, t) = Probabilidad de abandonar en tiempo t dado credulidad inicial θ
```

**Insight Key:** Receptores con bajo θ (escépticos) que pasaron filtro inicial tienen *alta* probabilidad de abandono tardío (costoso).

**Función de Utilidad Total:**

```
U(C) = G × Σ[i=1 to R] [1 - A(θ_i, t_final)] - C_T - C_S

Donde:
G = ganancia por conversión completa (voto, donación, movilización)
```

**[Subsección 2.1.3 - Equilibrio Óptimo]**

Resolver para C* óptimo (≈700 palabras):

**Proposición 1 (Filtrado Óptimo):**
Existe un nivel óptimo de "absurdidad" narrativa C* que maximiza U.

**Prueba (sketch):**

Analizar trade-off:

- **C bajo** (narrativa sofisticada): θ_min bajo → muchas respuestas → alto abandono → alto C_S
- **C alto** (narrativa absurda): θ_min alto → pocas respuestas → bajo abandono → bajo C_S

**Derivando:**

```
dU/dC = G × d/dC[Conversiones Netas] - dC_S/dC

En equilibrio: dU/dC = 0

Esto implica: Beneficio_Marginal(filtrado adicional) = Costo_Marginal(perder respuestas)
```

**Resultado:**

```
C* = función creciente de:
- Varianza de distribución de θ (mayor heterogeneidad → más filtrado)
- Costo de seguimiento (mayor C_S → más filtrado)
- Probabilidad de abandono tardío (mayor A → más filtrado)
```

**Corolario 1:**
En ambientes con alta varianza de θ y alto costo de conversión, **narrativas absurdas dominan a narrativas sofisticadas**.

**[Subsección 2.1.4 - Comparación con Modelos Alternativos]**

Contrastar con explicaciones estándar (≈600 palabras):

**Tabla Comparativa:**

| Modelo | Predicción sobre C | Evidencia Empírica |
|--------|-------------------|-------------------|
| **Rational Choice** | C → 0 (sofisticación óptima) | Rechazado: narrativas simples dominan |
| **Bounded Rationality** | C moderado (heurísticas) | Insuficiente: no predice persistencia del absurdo |
| **Path Dependence** | C histórico (lock-in) | Insuficiente: no explica selección inicial |
| **Costly Signaling** (este paper) | C* alto (filtrado óptimo) | **Consistente**: absurdo como equilibrio |

**[Subsección 2.1.5 - Predicciones Testeables]**

Derivar hipótesis específicas (≈400 palabras):

**H1 (Correlación Negativa Sofisticación-Éxito):**
Memeplexos con mayor C (narrativas más absurdas) deberían exhibir:

- Mayor persistencia institucional (años de supervivencia)
- Mayor cohesión de base (menor deserción)
- Mayor movilización (participación en manifestaciones/votos)

**H2 (Instituciones Ineficientes como Filtro):**
Políticas públicas con mayor "ineficiencia aparente" deberían:

- Sobrevivir más tiempo que las "técnicamente óptimas"
- Generar mayor lealtad grupal
- Resistir mejor los intentos de reforma

**H3 (Efecto de Distribución de θ):**
En sociedades con:

- Menor capital educativo → narrativas más simples deberían dominar
- Mayor desconfianza institucional → mayor ventaja de populismo
- Mayor desigualdad → mayor resonancia de narrativas binarias

**H4 (Intentos de Racionalización como Señal de Debilidad):**
Movimientos populistas que "sofistican" su discurso deberían:

- Perder núcleo duro de adherentes
- Sufrir fragmentación interna
- Eventualmente colapsar o revertir a simplicidad

### 2.2 APLICACIÓN: EL CASO DE LOS MEMES POPULISTAS

**INSTRUCCIONES:**

Aplicar el marco formal al populismo latinoamericano (≈1000 palabras)

**[Subsección 2.2.1 - Arquitectura Memética Populista como C* Óptimo]**

Retomar del paper anterior la tabla de arquitectura comparativa:

| Componente | Meme Populista | Meme Liberal | Ventaja Transmisión |
|-----------|---------------|--------------|---------------------|
| Narrativa Central | "Nosotros vs. Ellos" | "Equilibrio complejo" | Populista: 4x |
| C (complejidad) | **C alto** (binario) | C bajo (multidimensional) | Populista: filtro efectivo |
| θ_min | **θ alto** (requiere lealtad tribal) | θ bajo (requiere análisis) | Populista: pre-selección |

**Interpretación:**
La simplicidad populista NO es defecto sino **C* óptimo** dadas las condiciones:

- Distribución de θ en Latinoamérica (PISA 402, desconfianza 28%)
- Alto costo de movilización sostenida
- Necesidad de resistir contra-narrativas liberal-tecnocráticas

**[Subsección 2.2.2 - Obras Sociales como Feature, no Bug]**

Reinterpretar las obras sociales argentinas (≈400 palabras):

**Visión Tradicional:**
Sistema "mal diseñado" por ignorancia técnica o captura regulatoria

**Visión desde Costly Signaling:**
Fragmentación e ineficiencia son **señales costosas** que:

1. Filtran adherentes que priorizan pertenencia sobre eficiencia
2. Crean red de stakeholders con intereses anti-reforma
3. Generan complejidad que impide comprensión técnica masiva

**Evidencia del Paper Anterior:**

- 55 años de persistencia
- Sobrevivió a 22 gobiernos, 6 golpes, 2 hiperinflaciones
- Intentos de racionalización (Macri 2015-2019) fracasaron

**Predicción Confirmada:**
La "mejora técnica" del sistema (unificación, estandarización) **reduciría** su fitness memético al eliminar el filtro de selección.

**[Subsección 2.2.3 - Aguinaldo como Señal Tribal]**

Análisis similar del aguinaldo (≈300 palabras):

**Contradicción Evidente:**

- Meta: pleno empleo
- Instrumento: encarecer trabajo formal (13º mes)
- Resultado: incentivo al empleo informal

**Función de Filtro:**
Solo quienes valoran **símbolo de dignidad laboral** sobre **eficiencia económica** aceptan la narrativa.

**Dato del Paper Anterior:**
80 años de persistencia, cero reformas exitosas.

### 2.3 EXTENSIÓN: COMPETENCIA DE MEMEPLEXOS EN DERECHO INTERNACIONAL

**INSTRUCCIONES:**

Conectar con tu corpus de soberanía vs. globalismo (≈800 palabras)

**[Subsección 2.3.1 - Soberanía Absoluta como C Alto]**

Aplicar el marco teórico:

**Narrativa Soberanista:**

- C alto: "Soberanía irrestricta", "No intervención externa", "Orden nacional"
- θ_min alto: requiere priorizar identidad nacional sobre interdependencia
- Mecanismo de filtro: descarta quienes valoran cooperación internacional

**Narrativa Globalista:**

- C bajo: "Gobernanza multinivel", "Interdependencia compleja", "Derecho cosmopolita"
- θ_min bajo: requiere comprensión de trade-offs
- Sin filtro efectivo: atrae escépticos que luego abandonan

**Predicción:**
En conflictos legales transnacionales, narrativas soberanistas simples deberían exhibir:

- Mayor movilización doméstica
- Mayor persistencia institucional
- Menor deserción de base

**[Subsección 2.3.2 - Setup para Validación Empírica]**

Anticipar Sección 3 (≈200 palabras):

**Dataset:**
60 conflictos transnacionales (2000-2025) del corpus de International Law as Extended Phenotype

**Variables a Codificar:**

1. **C_narrativa**: Complejidad de narrativa dominante (escala 1-10)
2. **Éxito_institucional**: Persistencia de estructura legal generada
3. **Movilización**: Intensidad de apoyo popular
4. **Deserción**: Tasa de abandono de posición inicial

**Predicción Específica:**
Correlación negativa entre C_narrativa y Éxito_institucional.
