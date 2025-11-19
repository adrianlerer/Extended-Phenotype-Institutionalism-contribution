# PROMPT MAESTRO PARA GENSPARK: COSTLY SIGNALING PAPER

## Estructura Modular del Prompt

Este prompt ha sido dividido en 6 partes para facilitar su procesamiento:

### 📄 PARTE 1: Metadatos e Introducción
**Archivo**: `PROMPT_GENSPARK_COSTLY_SIGNALING_PARTE1.md`

**Contenido**:
- Metadatos del paper (autor, afiliación, JEL codes)
- Objetivos y preguntas de investigación
- Abstract (≤350 palabras)
- Sección 1: Introducción (≈2500 palabras)
  - El puzzle de la persistencia del absurdo
  - Innovación teórica (timo nigeriano, Zahavi, extended phenotype)
  - Roadmap del paper

---

### 📐 PARTE 2: Marco Teórico
**Archivo**: `PROMPT_GENSPARK_COSTLY_SIGNALING_PARTE2.md`

**Contenido**:
- Sección 2: Marco Teórico (≈4000 palabras)
  - Formalización matemática (función de utilidad, equilibrios)
  - Definiciones (meme político, distribución de credulidad θ)
  - Predicciones testeables (H1-H4)
  - Aplicación a populismo y derecho internacional

---

### 📊 PARTE 3: Validación Empírica
**Archivo**: `PROMPT_GENSPARK_COSTLY_SIGNALING_PARTE3.md`

**Contenido**:
- Sección 3: Validación Empírica (≈3500 palabras)
  - Dataset: 60 conflictos transnacionales (2000-2025)
  - Metodología analítica (correlaciones, regresiones, survival analysis)
  - Resultados principales (r=-0.67, HR=2.3)
  - Casos ilustrativos (Botnia, CPI, Brexit)
  - Robustez y limitaciones

---

### 🇦🇷 PARTE 4: Validación Histórica Argentina
**Archivo**: `PROMPT_GENSPARK_COSTLY_SIGNALING_PARTE4.md`

**Contenido**:
- Sección 4: Validación Histórica Argentina (≈2500 palabras)
  - Metodología de análisis histórico (1946-2025)
  - Casos específicos:
    - Obras sociales (C=2, 55 años)
    - Aguinaldo (C=1, 80 años)
    - Convertibilidad (C=4, 10 años)
    - Reforma laboral Menem (C=7, fracaso)
    - Milei 2023-presente (en progreso)
  - Patrón agregado (tabla survival rates por C)

---

### 💡 PARTE 5: Implicaciones y Conclusiones
**Archivo**: `PROMPT_GENSPARK_COSTLY_SIGNALING_PARTE5.md`

**Contenido**:
- Sección 5: Implicaciones (≈2000 palabras)
  - Lecciones para reformadores (tabla memetic engineering)
  - Casos de éxito relativo (Bolsa Família)
  - Prescripciones específicas (5 reglas)
  - Limitaciones éticas
  - Agenda de investigación futura
- Sección 6: Conclusiones (≈1500 palabras)
  - Contribuciones teóricas
  - Hallazgos empíricos
  - Implicaciones prácticas
  - Reflexión final (cita memorable)

---

### 📚 PARTE 6: Referencias y Notas Finales
**Archivo**: `PROMPT_GENSPARK_COSTLY_SIGNALING_PARTE6.md`

**Contenido**:
- Referencias (≈150 entradas)
  - Teoría evolutiva y memética
  - Populismo y economía política
  - Costly signaling y behavioral economics
  - Derecho internacional
  - Argentina - estudios de caso
  - **CRITICAL**: Trabajos previos del autor (7 papers SSRN)
- Apéndices
  - Appendix A: Codificación detallada C score (60 casos)
  - Appendix B: Robustez estadística
  - Appendix C: Código de replicación
- Notas finales para Genspark
  - Estilo y voz (prohibiciones específicas)
  - Rigor metodológico (tags: VERIFICADO, ESTIMACIÓN, etc.)
  - Formato SSRN
  - Integración con paper anterior
  - Datasets a usar
  - Checklist final (12 ítems)

---

## 🎯 Objetivo del Paper

**Título**: "Costly Signaling and Memetic Filtering: Why Populist Narratives Maintain 'Obvious' Inconsistencies"

**Pregunta Central**: ¿Por qué las narrativas políticas más exitosas no son las más "racionales" sino las que incorporan absurdos evidentes que funcionan como filtros de selección de adherentes?

**Tesis**: Las inconsistencias lógicas en narrativas populistas no son defectos (bugs) sino características optimizadas (features) que implementan filtrado diferencial por credulidad, maximizando ROI de movilización política vía señalización costosa (Zahavi's handicap principle).

---

## 📈 Estructura de Contribución

Este paper **complementa** el paper anterior de Lerer (2025, SSRN 5463814):

| Paper Anterior | Este Paper |
|---------------|-----------|
| **QUÉ**: Ventaja 216:1 de populismo | **POR QUÉ**: Mecanismo causal (filtrado por C) |
| **EVIDENCIA**: Persistencia institucional | **EXPLICACIÓN**: C* óptimo bajo restricciones |
| **DESCRIPTIVO**: ESS como equilibrio | **PREDICTIVO**: Correlación C-supervivencia |

**Key Innovation**: Aplicar teoría de señalización costosa (biología evolutiva) + timo nigeriano (Dennett) → explicar arquitectura memética populista como diseño óptimo.

---

## 📊 Datos Empíricos Clave

**Dataset 1: Conflictos Transnacionales**
- N = 60 casos (2000-2025)
- Fuente: Lerer (2024e, SSRN 5612010)
- Variables: C_narrativa, Institutional_Success, Base_Mobilization, Defection_Rate

**Dataset 2: Políticas Argentinas**
- N = 35 políticas (1946-2025)
- Fuente: Lerer (2025, SSRN 5463814)
- Variables: C_policy, Years_Survived, Reversal_Status

**Predicciones Principales**:
1. ρ(C, Success) < 0 → **CONFIRMADO**: r = -0.67 (p<0.001)
2. HR(C alto vs. bajo) > 1 → **CONFIRMADO**: HR = 2.3 (p=0.002)
3. Mediación vía movilización → **CONFIRMADO**: 59% del efecto

---

## ⚠️ Instrucciones Críticas para Genspark

### MANDATORY REQUIREMENTS:

1. **CITAR EXTENSAMENTE** paper anterior (Lerer 2025, SSRN 5463814)
2. **USAR DATOS REALES** de los datasets mencionados
3. **MANTENER ESTILO LERER**: profesional, sobrio, sin buzzwords IA
4. **INCLUIR TAGS**: [VERIFICADO], [ESTIMACIÓN], [INFERENCIA], [CONJETURA]
5. **LONGITUD**: 12,000-15,000 palabras (verificar con word count)
6. **ABSTRACT**: Exactamente ≤350 palabras
7. **REFERENCIAS**: ~150 entradas, incluir TODOS los papers previos del autor

### FORBIDDEN PHRASES:
- ❌ "Al final del día"
- ❌ "Dicho esto"
- ❌ "En pocas palabras"
- ❌ "Marco robusto"
- ❌ "Sinergia"

### REQUIRED ELEMENTS:
- ✅ Tabla comparativa (Rational Choice vs. Costly Signaling)
- ✅ Figuras (scatterplot, Kaplan-Meier, mediation diagram)
- ✅ Tabla de survival rates por C range
- ✅ Casos ilustrativos (Botnia, CPI, Brexit, obras sociales, aguinaldo)
- ✅ Sección de limitaciones éticas
- ✅ Código de replicación (mencionar GitHub)
- ✅ Cita memorable final

---

## 🔗 Integración con Corpus Existente

Este paper se integra con:

1. **Extended Phenotype of Populism** (SSRN 5463814) → explica mecanismo
2. **International Law as Extended Phenotype** (SSRN 5612010) → usa dataset
3. **Constitutional Lock-in** (SSRN 5624710) → ejemplo de C bajo exitoso
4. **JurisRank** (SSRN 5405459) → métrica de persistencia institucional

**Position**: Paper #8 en la serie "Law as Extended Phenotype"

---

## 📋 Checklist de Completitud

Antes de entregar, Genspark debe verificar:

- [ ] Abstract ≤350 palabras ✓
- [ ] Todas las secciones completas (no placeholders) ✓
- [ ] Citas a Lerer (2025) en 10+ lugares ✓
- [ ] Tablas con datos reales (no "ejemplo" o "placeholder") ✓
- [ ] Figuras descritas con especificaciones exactas ✓
- [ ] Referencias completas (~150 entradas) ✓
- [ ] Estilo sin buzzwords prohibidos ✓
- [ ] Tags [VERIFICADO] donde corresponda ✓
- [ ] Limitaciones explicitadas (4+) ✓
- [ ] Implicaciones éticas (sección completa) ✓
- [ ] Longitud 12,000-15,000 palabras ✓
- [ ] Cita final memorable ✓

---

## 🚀 Instrucción de Ejecución para Genspark

**PASO 1**: Leer las 6 partes del prompt en orden secuencial

**PASO 2**: Leer papers previos del autor (especialmente SSRN 5463814)

**PASO 3**: Acceder a datasets mencionados en el proyecto

**PASO 4**: Generar paper completo siguiendo estructura exacta

**PASO 5**: Verificar checklist de completitud

**PASO 6**: Revisar estilo (eliminar buzzwords, mantener tono Lerer)

**PASO 7**: Word count final (debe estar en rango 12,000-15,000)

**PASO 8**: Entregar documento listo para SSRN upload

---

## 📝 Formato de Entrega

**Output esperado**:

```
COSTLY_SIGNALING_MEMETIC_FILTERING.docx
Formato: SSRN-ready
Longitud: 12,000-15,000 palabras
Estructura: Ver PARTE 6 (sección XIII)
Referencias: APA 7th edition
Figuras/Tablas: Numeradas secuencialmente
Apéndices: 3 (A, B, C)
```

---

**FIN DEL MASTER INDEX**

**Total archivos del prompt**: 7
- 1 master index (este archivo)
- 6 partes modulares

**Para usar**: Proporcionar a Genspark en orden:
1. Este archivo (contexto general)
2. Partes 1-6 (contenido específico)
3. Acceso a datasets del proyecto
4. Papers previos del autor (PDFs o links SSRN)
