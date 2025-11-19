# Metodología: Índices de Fuerza Clerical y Efectividad de Reforma

## 1. Clerical Strength Index (CSI)

**Definición conceptual:** Grado de institucionalización de ortodoxias doctrinales que funcionan como "cleros epistemológicos" resistentes a falsación empírica.

**Operacionalización:** Promedio ponderado de 4 dimensiones medibles (0.0-1.0):

### Dimensión 1: Endogamia Académica (peso: 30%)
**Indicadores verificables:**
- Tasa de citación endogámica en las 3 principales revistas de derecho de la jurisdicción
- Proporción de autores citados que comparten afiliación institucional o escuela doctrinal
- Diversidad de filiaciones institucionales en comités editoriales

**Método de medición:**
1. Seleccionar las 3 revistas de derecho más citadas de la jurisdicción
2. Muestrear 30 artículos por revista (últimos 5 años)
3. Codificar citas: endogámicas (misma tradición doctrinal) vs. exogámicas (tradiciones diferentes)
4. Calcular proporción endogámica
5. Normalizar a escala 0-1:
   - 0.0-0.35: Baja endogamia (comparable a ciencias duras)
   - 0.35-0.65: Endogamia moderada
   - 0.65-1.0: Alta endogamia (característica clerical)

**Fuentes de datos:**
- Google Scholar, Scopus, SciELO
- Análisis de redes de citación
- Comités editoriales publicados en sitios web de revistas

### Dimensión 2: Sacralización de Conceptos (peso: 25%)
**Indicadores verificables:**
- Frecuencia de lenguaje deontológico absoluto ("inalienable", "inviolable", "sagrado")
- Proporción de proposiciones empíricas reenmarcadas como imperativos morales
- Resistencia documentada a cuestionamiento empírico (rechazos editoriales, controversias)

**Método de medición:**
1. Análisis textual de corpus doctrinal (tratados, papers influyentes)
2. Frecuencia de términos sacralizantes por 10,000 palabras
3. Análisis de controversias documentadas donde evidencia empírica fue rechazada con argumentos morales
4. Normalizar a escala 0-1:
   - 0.0-0.3: Discurso empírico predominante
   - 0.3-0.6: Mezcla empírico-normativo
   - 0.6-1.0: Discurso sacralizado predominante

**Fuentes de datos:**
- Corpus de textos legales (tratados, artículos influyentes)
- Análisis de lenguaje NLP
- Controversias académicas documentadas

### Dimensión 3: Señalización Costosa (peso: 20%)
**Indicadores verificables:**
- Defensa pública de posiciones empíricamente problemáticas como requisito de membresía
- Exclusión documentada de académicos por heterodoxia (no por calidad)
- Rituales de afiliación (declaraciones de principios, juramentos de fidelidad doctrinal)

**Método de medición:**
1. Documentar casos de exclusión por heterodoxia vs. desacuerdo sustantivo
2. Identificar "pruebas de pureza" explícitas (declaraciones requeridas, posiciones obligatorias)
3. Codificar nivel de costosidad:
   - 0.0-0.3: Pluralismo tolerado, debate libre
   - 0.3-0.6: Presión informal hacia ortodoxia
   - 0.6-1.0: Exclusión sistemática de heterodoxia

**Fuentes de datos:**
- Casos documentados de controversias académicas
- Requisitos de membresía en asociaciones profesionales
- Patrones de contratación académica

### Dimensión 4: Control Institucional (peso: 25%)
**Indicadores verificables:**
- Proporción de foros de decisión controlados por misma tradición doctrinal
- Concentración de poder editorial (índice Herfindahl de control de revistas)
- Barreras de entrada a debate (requisitos de credenciales, acceso a publicaciones)

**Método de medición:**
1. Mapear foros principales de debate (revistas, conferencias, asociaciones)
2. Identificar afiliación doctrinal dominante de cada foro
3. Calcular índice Herfindahl de concentración: H = Σ(si²) donde si = cuota de mercado del foro i
4. Normalizar a escala 0-1:
   - 0.0-0.3: Control distribuido, pluralismo institucional
   - 0.3-0.6: Concentración moderada
   - 0.6-1.0: Control monopolístico de ortodoxia

**Fuentes de datos:**
- Directorios de revistas académicas
- Comités organizadores de conferencias
- Afiliaciones de editores y gatekeepers

### Cálculo del CSI:
```
CSI = (0.30 × Endogamia) + (0.25 × Sacralización) + (0.20 × Señalización) + (0.25 × Control)
```

**Rangos interpretativos:**
- **CSI < 0.35:** Institucionalización clerical baja (ciencias duras, derecho comparado pragmático)
- **CSI 0.35-0.65:** Institucionalización clerical moderada (campo normal con ortodoxias parciales)
- **CSI > 0.65:** Institucionalización clerical alta (estructura religiosa secular)

---

## 2. Reform Effectiveness Index (REI)

**Definición conceptual:** Grado en que reformas legales propuestas logran sus objetivos declarados, medido por alineación entre intenciones y resultados verificables.

**Operacionalización:** Promedio ponderado de 3 dimensiones medibles (0.0-1.0):

### Dimensión 1: Tasa de Implementación (peso: 30%)
**Indicadores verificables:**
- Proporción de reformas propuestas que se implementan efectivamente
- Tiempo promedio desde propuesta hasta implementación
- Tasa de reversión de reformas implementadas

**Método de medición:**
1. Identificar reformas significativas propuestas en últimos 15 años (mínimo 10 por jurisdicción)
2. Clasificar estado: No implementada / Parcialmente implementada / Implementada / Implementada y revertida
3. Calcular proporción de implementación efectiva
4. Normalizar a escala 0-1:
   - 0.0-0.3: Implementación baja (<30% de reformas)
   - 0.3-0.7: Implementación moderada (30-70%)
   - 0.7-1.0: Implementación alta (>70%)

**Fuentes de datos:**
- Registros legislativos oficiales
- Bases de datos de reformas legales (CEJA, CEPAL, etc.)
- Estudios de implementación de políticas

### Dimensión 2: Alineación de Resultados (peso: 40%)
**Indicadores verificables:**
- Cambio medible en indicadores clave post-reforma vs. objetivos declarados
- Dirección del cambio (alineado/neutral/opuesto a objetivo)
- Magnitud del cambio (efecto pequeño/moderado/grande)

**Método de medición:**
1. Para cada reforma implementada, identificar objetivo declarado explícito
2. Identificar indicador medible correspondiente (ej. si objetivo es "reducir encarcelamiento", indicador = tasa de encarcelamiento)
3. Medir cambio pre-post implementación (mínimo 3 años post)
4. Codificar alineación:
   - +1.0: Cambio fuerte en dirección deseada (>20%)
   - +0.5: Cambio moderado en dirección deseada (10-20%)
   - 0.0: Sin cambio significativo (<10%)
   - -0.5: Cambio moderado en dirección opuesta
   - -1.0: Cambio fuerte en dirección opuesta (>20%)
5. Promediar alineación a través de reformas

**Fuentes de datos:**
- Estadísticas oficiales (INE, INDEC, census bureaus, etc.)
- Bases de datos internacionales (World Bank, OECD, ILO)
- Evaluaciones de impacto publicadas

### Dimensión 3: Adaptabilidad (peso: 30%)
**Indicadores verificables:**
- Ciclos de revisión y ajuste de reformas basados en evidencia
- Incorporación de evaluaciones empíricas en modificaciones posteriores
- Capacidad de corrección cuando reformas no logran objetivos

**Método de medición:**
1. Identificar si reformas incluyen cláusulas de evaluación (sunset clauses, revisión obligatoria)
2. Documentar casos de ajuste basado en evidencia post-implementación
3. Codificar nivel de adaptabilidad:
   - 0.0-0.3: Reformas rígidas, sin mecanismos de evaluación
   - 0.3-0.7: Evaluación ocasional, ajustes limitados
   - 0.7-1.0: Evaluación sistemática, ajustes basados en evidencia

**Fuentes de datos:**
- Textos de leyes (cláusulas de evaluación)
- Reportes de evaluación gubernamentales
- Modificaciones legislativas posteriores

### Cálculo del REI:
```
REI = (0.30 × Implementación) + (0.40 × Alineación) + (0.30 × Adaptabilidad)
```

**Rangos interpretativos:**
- **REI < 0.35:** Efectividad baja (reformas fracasan sistemáticamente)
- **REI 0.35-0.65:** Efectividad moderada (resultados mixtos)
- **REI > 0.65:** Efectividad alta (reformas logran objetivos)

---

## 3. Hipótesis a Testear

**H1 (Principal):** CSI y REI correlacionan negativamente: r < -0.50, p < 0.01

**H2 (Umbral):** Efecto clerical es no-lineal con umbral crítico en CSI ≈ 0.65

**H3 (Independencia ideológica):** Correlación CSI-REI persiste controlando por orientación ideológica (izquierda/derecha)

**H4 (Mediación institucional):** Efecto CSI sobre REI es mediado por control institucional (Dimensión 4 del CSI)

---

## 4. Limitaciones Metodológicas (A Declarar Explícitamente)

### Limitaciones de Datos
1. **Sesgo de disponibilidad:** Jurisdicciones con mejor documentación están sobrerrepresentadas
2. **Sesgo de idioma:** Jurisdicciones angloparlantes e hispanoparlantes dominan (limitado acceso a fuentes en otros idiomas)
3. **Ventana temporal:** Datos limitados a 2005-2025 (20 años)

### Limitaciones Conceptuales
1. **Operacionalización imperfecta:** Los índices son proxies, no mediciones directas de conceptos teóricos
2. **Causalidad vs. correlación:** Diseño correlacional no permite inferencias causales definitivas
3. **Variables omitidas:** Factores no medidos (cultura política, recursos económicos) pueden confundir relación

### Limitaciones de Validez
1. **Confiabilidad inter-codificador:** Codificación realizada por un solo investigador (ideal: múltiples codificadores independientes)
2. **Validez de constructo:** CSI y REI requieren validación convergente con otras medidas
3. **Generalización:** Muestra no aleatoria limita generalización a todas las jurisdicciones

### Mitigaciones Implementadas
1. **Triangulación:** Múltiples indicadores por dimensión
2. **Transparencia:** Datos y código disponibles para replicación
3. **Análisis de sensibilidad:** Testar robustez con diferentes ponderaciones de componentes
4. **Documentación completa:** Decisiones de codificación explícitas y justificadas

---

## 5. Protocolo de Falsación

Para que este estudio sea científicamente riguroso, debe ser falsable. Las siguientes observaciones falsarían la hipótesis clerical:

### Falsadores Fuertes (refutarían completamente la teoría)
1. **No-correlación:** Si r(CSI, REI) > -0.20 o p > 0.10 → hipótesis clerical falsada
2. **Reversión de signo:** Si r(CSI, REI) > +0.30, p < 0.05 → teoría radicalmente equivocada
3. **Reducción a factores económicos:** Si controlando por PIB per cápita, r(CSI, REI) → 0 → institucionalización clerical es epifenómeno de riqueza

### Falsadores Moderados (requerirían modificación sustantiva)
1. **Dependencia ideológica total:** Si correlación es fuerte en una orientación (ej. izquierda) pero nula en otra → mecanismo es ideológico, no estructural
2. **Casos contradictorios persistentes:** Si >30% de casos muestran alta CSI + alta REI → teoría captura fenómeno minoritario
3. **Ausencia de mecanismo:** Si dimensiones de CSI no predicen REI individualmente → índice compuesto es espurio

### Protocolo de Reportar Resultados Nulos
**Compromiso:** Si las hipótesis son falsadas, el paper reportará:
1. Los resultados nulos completamente
2. Análisis post-hoc de por qué las predicciones fallaron
3. Implicaciones para la teoría clerical
4. Qué evidencia cambiaría la conclusión

**No se hará:** Reconfigurar análisis hasta obtener resultados significativos (p-hacking), omitir análisis no favorables, o reinterpretar hipótesis post-hoc.

---

## 6. Plan de Análisis Estadístico

### Análisis Descriptivo
- Distribución de CSI y REI (histogramas, estadísticas resumen)
- Identificación de outliers y casos extremos
- Matriz de correlaciones entre componentes

### Análisis Inferencial Principal
1. **Correlación de Pearson:** r(CSI, REI) con IC 95% y p-value
2. **Regresión lineal simple:** REI ~ CSI
3. **Regresión con controles:** REI ~ CSI + PIB + Sistema_Legal + Región

### Análisis de Robustez
1. **Correlación de Spearman** (no-paramétrica) para verificar no-linealidad
2. **Regresión segmentada** (piecewise) para detectar umbrales
3. **Análisis de sensibilidad** con diferentes ponderaciones de componentes CSI/REI

### Análisis de Mediación
- Test de Sobel para mediación de Control Institucional
- Modelos de ecuaciones estructurales (SEM) si tamaño muestral lo permite

### Visualizaciones
1. Scatterplot CSI vs REI con línea de regresión
2. Heatmap de correlaciones entre componentes
3. Boxplots de REI por categorías de CSI (bajo/medio/alto)
4. Gráficos de casos ilustrativos con etiquetas de jurisdicciones

---

**Fecha de elaboración:** 2025-11-18  
**Autor:** Ignacio Adrian Lerer  
**Versión:** 1.0 (Draft metodológico inicial)
