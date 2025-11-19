# Plan de Recolección de Datos: Dataset CSI-REI
## Estrategia realista para construir dataset defendible (n=150)

---

## Fase 1: CASOS ANCLA (Ya completados: n=12)

### ✅ Completados con datos primarios
**Argentina (3 dominios):**
- Criminal: CSI=0.871, REI=0.131 ✅
- Labor: CSI=0.867, REI=0.121 ✅
- Constitutional: CSI=0.804, REI=0.185 ✅

**Chile (3 dominios):**
- Criminal: CSI=0.408, REI=0.496 ✅
- Labor: CSI=0.381, REI=0.452 ✅
- Constitutional: CSI=0.401, REI=0.455 ✅

**Uruguay (3 dominios):**
- Criminal: CSI=0.370, REI=0.531 ✅
- Labor: CSI=0.347, REI=0.562 ✅
- Constitutional: CSI=0.371, REI=0.508 ✅

**Texas (1 dominio):**
- Criminal: CSI=0.325, REI=0.593 ✅

**Illinois (1 dominio):**
- Criminal: CSI=0.757, REI=0.221 ✅

**Total completado: 12/150 (8%)**

---

## Fase 2: EXPANSIÓN ESTRATÉGICA (Objetivo: +38, Total: 50/150, 33%)

### Prioridad 1: América Latina (completar región más conocida)
**Objetivo:** 15 jurisdicciones × 3 dominios = 45 observaciones
**Ya tenemos:** Argentina, Chile, Uruguay (9 obs)
**Faltan:** 12 jurisdicciones × 3 dominios = 36 observaciones

#### Estrategia por país:

**BRASIL (3 obs)** - Prioridad ALTA
- **Fuentes primarias:**
  - Criminal: Código Penal 1940, reformas 2003-2020. Pacote Anticrime (2019).
  - Labor: CLT (Consolidação das Leis do Trabalho). Reforma Laboral 2017.
  - Constitutional: CF 1988, ADIs en STF.
- **Datos verificables:**
  - Tasa encarcelamiento: DEPEN/InfoPen
  - Datos laborales: IBGE, PNAD Contínua
  - Literatura: Zaffaroni (criminal), Delgado (labor), Barroso (constitutional)
- **Hipótesis CSI:** Labor=Alto (proteccionismo CLT), Criminal=Medio-Alto (garantismo influencia argentina), Constitutional=Medio

**COLOMBIA (3 obs)** - Prioridad ALTA
- **Fuentes primarias:**
  - Criminal: Código Penal 2000, Sistema Acusatorio Ley 906/2004
  - Labor: Código Sustantivo del Trabajo, reformas 2002-2023
  - Constitutional: CP 1991, jurisprudencia Corte Constitucional
- **Datos verificables:**
  - INPEC (estadísticas carcelarias)
  - DANE (datos laborales)
  - Literatura: Corte Constitucional muy productiva, citación rastreable
- **Hipótesis CSI:** Constitutional=Bajo-Medio (corte activista pero pluralista), Criminal=Medio, Labor=Alto

**MÉXICO (3 obs)** - Prioridad ALTA
- **Fuentes primarias:**
  - Criminal: Reforma constitucional 2008 (sistema acusatorio), implementación 2016
  - Labor: LFT, reforma 2019 (libertad sindical)
  - Constitutional: CPEUM, amparos
- **Datos verificables:**
  - INEGI (todo tipo de estadísticas)
  - Estadísticas judiciales (SCJN)
  - Literatura abundante, IIJ-UNAM muy productivo
- **Hipótesis CSI:** Variable por dominio

**PERÚ (3 obs)** - Prioridad MEDIA
- Criminal: NCPP 2004, reformas graduales
- Labor: Regulación híbrida
- Constitutional: Tribunal Constitucional activo

**COSTA RICA (3 obs)** - Prioridad MEDIA
- Reputación de institucionalidad fuerte
- Datos verificables en INEC
- Literatura académica accesible

**VENEZUELA (3 obs)** - Prioridad BAJA (caso extremo)
- Colapso institucional post-1999
- Útil como outlier
- Datos menos confiables pero documentado internacionalmente

#### Método de codificación rápida para completar región:

**Protocolo de 3 horas por jurisdicción (9 horas por país):**

**Hora 1: CSI - Endogamia y Control Institucional**
1. Identificar 3 revistas principales del dominio (Google Scholar Metrics, SciELO)
2. Muestrear 10 artículos recientes (no 30, reducir carga)
3. Codificar citas: endogámicas (misma tradición) vs exogámicas
4. Identificar concentración editorial (buscar comités editoriales)
5. **Output:** citation_endogamy_rate, journal_concentration, gatekeeper_concentration

**Hora 2: CSI - Sacralización y Señalización Costosa**
1. Seleccionar 5 textos doctrinales influyentes (tratados, papers muy citados)
2. Análisis textual simple: frecuencia términos sacralizantes
3. Buscar controversias documentadas (exclusión de heterodoxos)
4. **Output:** sacred_language_freq, empirical_resistance, orthodoxy_requirement, exclusion_rate

**Hora 3: REI - Reformas y Resultados**
1. Identificar 5-10 reformas principales (últimos 15 años)
2. Clasificar: propuesta/implementada/revertida
3. Buscar indicadores pre-post (1-2 indicadores clave por reforma)
4. **Output:** reforms_proposed, reforms_implemented, alignment_scores

**Total por país:** 9 horas de trabajo concentrado
**Total región (12 países pendientes):** 108 horas = **3 semanas full-time** o **6 semanas part-time**

---

### Prioridad 2: Europa (casos clave para contraste)
**Objetivo:** 6 jurisdicciones × 3 dominios = 18 observaciones

**Selección estratégica (no todas las 15):**

1. **Alemania (3 obs)** - Modelo civil law, institucionalidad fuerte
2. **Francia (3 obs)** - Tradición civilista clásica
3. **UK (3 obs)** - Common law, contraste con civil law
4. **España (3 obs)** - Puente Europa-Latinoamérica, idioma accesible
5. **Países Nórdicos - Noruega (3 obs)** - Modelo consensual pragmático
6. **Polonia (3 obs)** - Tensión democracia-autoritarismo

**Método:** Mismo protocolo 3 horas × jurisdicción
**Total:** 18 jurisdicciones × 3 horas = 54 horas = **2 semanas**

---

### Prioridad 3: Common Law y Asia (casos críticos)
**Objetivo:** 8 jurisdicciones × 3 dominios = 24 observaciones (selectivo, no todos)

**Common Law:**
1. **USA Federal (3 obs)** - Ya tenemos Texas y Illinois criminal, expandir
2. **California (3 obs)** - Abolicionismo progresista
3. **New York (3 obs)** - Centro financiero, regulación laboral fuerte
4. **Canada (3 obs)** - Modelo intermedio
5. **Australia (3 obs)** - Common law pragmático

**Asia:**
1. **Japan (3 obs)** - Híbrido civil law/tradición local
2. **South Korea (3 obs)** - Modernización acelerada
3. **Singapore (3 obs)** - Autoritarismo eficiente

**Método:** Protocolo 3 horas, pero mayor dificultad idioma/acceso
**Total estimado:** 24 obs × 4 horas (por dificultad) = 96 horas = **3 semanas**

---

## RESUMEN PLAN REALISTA

### Cronograma Total
| Fase | Observaciones | Tiempo Estimado | % Total |
|------|---------------|-----------------|---------|
| ✅ Casos Ancla | 12 | Ya completado | 8% |
| América Latina | 36 | 6 semanas | 32% |
| Europa | 18 | 2 semanas | 44% |
| Common Law/Asia | 24 | 3 semanas | 60% |
| **TOTAL REALISTA** | **90** | **11 semanas** | **60%** |

### Estrategia Conservadora vs Ambiciosa

**OPCIÓN A: Dataset Conservador (n=90)**
- **Claims defendibles:** "Analicé 30 jurisdicciones a través de 3 dominios legales (n=90)"
- **Correlación esperada:** Si r=-0.73 se mantiene → Muy defendible
- **Ventaja:** 100% datos primarios, alta confiabilidad
- **Desventaja:** Menor n reduce poder estadístico

**OPCIÓN B: Dataset Híbrido (n=120)**
- 90 observaciones con datos primarios completos
- 30 observaciones con codificación secundaria (literatura existente)
- **Claims:** "Analicé 40 jurisdicciones (n=120), 75% con datos primarios, 25% con codificación secundaria"
- **Ventaja:** Mayor n, poder estadístico mejorado
- **Desventaja:** Metodología mixta requiere justificación

**OPCIÓN C: Dataset Completo (n=150)**
- 90 observaciones primarias
- 60 observaciones secundarias (extrapolación, literatura)
- **Claims:** "50 jurisdicciones (n=150)"
- **Ventaja:** Claims originales
- **Desventaja:** Riesgo de sobre-extrapolación, menor defendibilidad

---

## RECOMENDACIÓN

### Estrategia Progresiva:

**PASO 1:** Completar n=90 con datos primarios rigurosos (11 semanas)

**PASO 2:** Análisis estadístico preliminar con n=90
- Si r < -0.50, p < 0.01 → Hipótesis confirmada con dataset conservador
- Publicar working paper con n=90

**PASO 3:** Decisión basada en resultados:
- **Si correlación es fuerte (r < -0.65):** Expandir a n=120-150 para robustez
- **Si correlación es moderada (r ≈ -0.50):** Mantener n=90, claims más conservadores
- **Si correlación es débil (r > -0.40):** No expandir, replantear hipótesis

### Claims Honestos para Paper

**Versión Conservadora (n=90):**
> "Conduje análisis comparativo de 30 jurisdicciones a través de tres dominios legales (derecho penal, laboral y constitucional), generando 90 observaciones. Cada observación fue codificada con datos primarios verificables..."

**Versión Híbrida (n=120, si se expande):**
> "Analicé 40 jurisdicciones (n=120 observaciones), utilizando codificación primaria para 75% de casos y codificación secundaria basada en literatura para 25%..."

**NUNCA claims sin respaldo:**
> ❌ "50 jurisdicciones, n=150" sin haber completado el trabajo

---

## Herramientas y Recursos

### Bases de Datos
1. **Criminal Justice:**
   - World Prison Brief (ICPR)
   - UNODC Statistics
   - CEJA (América Latina)
   - Vera Institute (USA)

2. **Labor:**
   - ILO Statistics
   - OECD Employment Database
   - National statistical agencies (INDEC, IBGE, INEGI, etc.)

3. **Constitutional:**
   - Constitute Project
   - V-Dem Institute
   - Comparative Constitutions Project

4. **Academic Literature:**
   - Google Scholar
   - SciELO
   - HeinOnline
   - JSTOR

### Software
- **Análisis:** Python (pandas, scipy, statsmodels) o R
- **Visualización:** matplotlib, seaborn, ggplot2
- **Gestión:** Excel/Google Sheets para entrada inicial
- **Control de versiones:** Git para rastreabilidad

---

## Protocolo de Calidad

### Checks de Validación
1. **Consistencia interna:** CSI components deben correlacionar positivamente
2. **Validez de rostro:** Casos conocidos (Argentina alto CSI, Chile bajo CSI) deben matchear
3. **Outliers:** Identificar y justificar casos extremos
4. **Missing data:** <10% por variable, documentar patrones

### Documentación
- Cada observación debe tener:
  - Fuentes específicas citadas
  - Decisiones de codificación justificadas
  - Nivel de confianza (Alto/Medio/Bajo)
  - Notas sobre dificultades o ambigüedades

### Revisión
- Peer review informal: Compartir codificación con colegas expertos en jurisdicciones específicas
- Sensitivity analysis: Re-codificar 10% de casos para evaluar confiabilidad

---

**Próximos pasos inmediatos:**
1. ¿Confirmas OPCIÓN A (n=90 conservador)?
2. ¿Empezamos con Brasil, Colombia, México?
3. ¿Necesitas ayuda automatizando búsquedas bibliográficas?

**Fecha:** 2025-11-18
**Autor:** Ignacio Adrian Lerer
