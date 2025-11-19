# PROMPT PARA GENSPARK: PAPER SSRN - PARTE 6

## IX. REFERENCIAS (≈150 entradas)

**INSTRUCCIONES PARA GENSPARK:**

Incluir bibliografía completa con estas secciones:

### A. TEORÍA EVOLUTIVA Y MEMÉTICA (≈25 entradas)

**Fuentes Clave:**

- Dawkins, R. (1976). *The Selfish Gene*. Oxford University Press.
- Dawkins, R. (1982). *The Extended Phenotype*. Oxford University Press.
- Dennett, D. (2017). *From Bacteria to Bach and Back*. Norton.
- Zahavi, A. (1975). "Mate selection: A selection for a handicap." *Journal of Theoretical Biology*.
- Boyd, R. & Richerson, P. (1985). *Culture and the Evolutionary Process*. University of Chicago Press.
- Henrich, J. (2016). *The Secret of Our Success*. Princeton University Press.

### B. POPULISMO Y ECONOMÍA POLÍTICA (≈30 entradas)

**Incluir:**

- Dornbusch, R. & Edwards, S. (1991). *The Macroeconomics of Populism in Latin America*.
- Mudde, C. & Rovira Kaltwasser, C. (2017). *Populism: A Very Short Introduction*.
- Acemoglu, D. & Robinson, J. (2012). *Why Nations Fail*.
- Pierson, P. (2000). "Increasing returns, path dependence, and the study of politics." *APSR*.

### C. COSTLY SIGNALING Y BEHAVIORAL ECONOMICS (≈20 entradas)

**Incluir:**

- Spence, M. (1973). "Job market signaling." *Quarterly Journal of Economics*.
- Kahneman, D. & Tversky, A. (1979). "Prospect theory." *Econometrica*.
- Camerer, C., Loewenstein, G., & Rabin, M. (2004). *Advances in Behavioral Economics*.

### D. DERECHO INTERNACIONAL Y CONSTITUCIONAL (≈25 entradas)

**Incluir:**

- Koh, H. (1997). "Why do nations obey international law?" *Yale Law Journal*.
- Goldsmith, J. & Posner, E. (2005). *The Limits of International Law*.
- Tushnet, M. (2008). *Weak Courts, Strong Rights*.

### E. ARGENTINA - ESTUDIOS DE CASO (≈20 entradas)

**Incluir:**

- Torre, J.C. & Pastoriza, E. (2002). "La democratización del bienestar." En *Nueva Historia Argentina*.
- Gerchunoff, P. & Llach, L. (2018). *El ciclo de la ilusión y el desencanto*.
- Novaro, M. & Palermo, V. (2003). *La dictadura militar 1976-1983*.

### F. TRABAJOS PREVIOS DEL AUTOR (≈10 entradas)

**CRITICAL - INCLUIR TODOS:**

```
Lerer, I.A. (2025). "The Extended Phenotype of Populism: A Memetic Analysis of Policy Persistence in Latin America." SSRN Working Paper No. 5463814. 
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5463814

Lerer, I.A. (2024a). "Constitutional Lock-in and the Phenotypic Expression of Legal Regimes: Argentina's Labor Market as Irreversible Institutional Morphology." SSRN Working Paper No. 5624710.
https://papers.ssrn.com/abstract=5624710

Lerer, I.A. (2024b). "Law as Extended Phenotype: Toward an Evolutionary Theory of Legal Systems." SSRN Working Paper No. 5593470.
https://papers.ssrn.com/abstract=5593470

Lerer, I.A. (2024c). "The Peralta Metamorphosis: Quantifying the Evolution of Legal Parasitism Through Computational Analysis of Argentine Constitutional Degradation (1922-2025)." SSRN Working Paper No. 5467928.
https://papers.ssrn.com/abstract=5467928

Lerer, I.A. (2024d). "Argentina's Fiscal Lock-in: Tax Reform as Extended Phenotype." SSRN Working Paper No. 5635152.
https://papers.ssrn.com/abstract=5635152

Lerer, I.A. (2024e). "International Law as Extended Phenotype: Globalist and Sovereigntist Memeplexes Competing Through Legal Artifacts (2000-2025)." SSRN Working Paper No. 5612010.
https://papers.ssrn.com/abstract=5612010

Lerer, I.A. (2024f). "JurisRank: Measuring Legal Phenotypic Fitness Through Citation Networks -- A Darwinian Approach to Legal Evolution with Dual Methodological Validation." SSRN Working Paper No. 5405459.
https://papers.ssrn.com/abstract=5405459
```

### G. OTROS (≈20 entradas)

Fuentes adicionales según necesidad del argumento.

-----

## X. APÉNDICES

### APPENDIX A: CODIFICACIÓN DETALLADA DE C SCORE

**INSTRUCCIONES:**

Tabla completa con los 60 casos del corpus:

```
[GENSPARK: Generar tabla con columnas]
- Case_ID
- Conflict_Name
- Year
- Sovereigntist_Narrative (texto breve)
- C_sov (1-10)
- Globalist_Narrative (texto breve)
- C_glob (1-10)
- Winner (Sov/Glob/Hybrid)
- Institutional_Success (0-100)
- Base_Mobilization (Low/Med/High)
- Notes
```

### APPENDIX B: ROBUSTEZ ESTADÍSTICA

**INSTRUCCIONES:**

Incluir:

- Correlación matrices
- VIF para multicolinealidad
- Residual plots
- Alternative model specifications

### APPENDIX C: CÓDIGO DE REPLICACIÓN

**INSTRUCCIONES:**

Incluir link a repositorio GitHub con:

- Datos completos (CSV)
- Scripts de análisis (R o Python)
- Documentación de codificación
- Instructions para replicar tablas y figuras

**Ejemplo:**

```
Replication materials available at:
https://github.com/adrianlerer/costly-signaling-populism

DOI: 10.5281/zenodo.XXXXXXX
```

-----

## XI. NOTAS FINALES PARA GENSPARK

### A. ESTILO Y VOZ

**CRITICAL - MANTENER EL ESTILO LERER:**

- Tono profesional, sobrio, conversacional
- Sin tuteo ni muletillas de IA
- **PROHIBIDO USAR:**
  - "Al final del día"
  - "Dicho esto"
  - "En pocas palabras"
  - "Marco robusto"
  - "Sinergia"
- Variar longitud de oraciones
- Metáforas discretas cuando pertinentes
- Permitir leves acotaciones humanas (ironías sutiles)

### B. RIGOR METODOLÓGICO

- Toda afirmación empírica debe tener tag:
  - **[VERIFICADO]**: dato con fuente
  - **[ESTIMACIÓN]**: cálculo derivado
  - **[INFERENCIA]**: lógica con premisas declaradas
  - **[CONJETURA]**: hipótesis provisional
- Citar siempre fuentes confiables
- No inventar datos
- Explicitar limitaciones

### C. FORMATO SSRN

- Abstract ≤ 350 palabras
- Total 12,000-15,000 palabras (≈40-50 páginas)
- Estructura estándar: Intro-Teoría-Datos-Resultados-Discusión-Conclusión
- Figuras y tablas numeradas secuencialmente
- Referencias en formato APA o Chicago
- Replication materials mencionados

### D. INTEGRACIÓN CON PAPER ANTERIOR

**CRITICAL:**

- Citar extensamente Lerer (2025, SSRN 5463814)
- Posicionar este paper como "complemento" que explica mecanismo causal
- No repetir contenido, sino **construir sobre hallazgos previos**
- Cross-references explícitos:
  - "Como demostramos en Lerer (2025)…"
  - "Esto explica el hallazgo de ventaja 216:1 reportado anteriormente…"

### E. DATASETS A USAR

**Disponibles en tu proyecto:**

- `dataset_60_cases_verified.xlsx`: Conflictos transnacionales
- `historical_reforms_database.csv`: Reformas Argentina 1946-2025
- Tablas de findings del paper anterior (incluidas en los documents)

**Genspark debe:**

- Leer estos datasets
- Generar estadística descriptiva
- Producir análisis según instrucciones
- Crear figuras/tablas con datos reales

-----

## XII. CHECKLIST FINAL PARA GENSPARK

Antes de entregar el paper completo, verificar:

- [ ] Abstract ≤350 palabras con los 5 componentes
- [ ] Todas las secciones completas (no placeholders)
- [ ] Citas a Lerer (2025) en lugares apropiados
- [ ] Tablas y figuras generadas con datos reales
- [ ] Referencias completas (≈150 entradas)
- [ ] Estilo LererSLM mantenido
- [ ] Sin buzzwords prohibidos
- [ ] Tags de verificación donde corresponda
- [ ] Código de replicación mencionado
- [ ] Limitaciones explicitadas
- [ ] Implicaciones éticas discutidas
- [ ] Longitud total ≈12,000-15,000 palabras

-----

## XIII. ESTRUCTURA FINAL DEL DOCUMENTO

Para facilitar el trabajo de Genspark, la estructura completa es:

```
COSTLY SIGNALING AND MEMETIC FILTERING
Why Populist Narratives Maintain 'Obvious' Inconsistencies

[Title Page]
- Autor, afiliación, contacto
- Abstract
- Keywords
- JEL Codes

[Section 1: INTRODUCCIÓN] (≈2500 palabras)
- 1.1 El Puzzle: La Persistencia del Absurdo
- 1.2 Innovación Teórica: De la Biología a la Política
- 1.3 Roadmap del Paper

[Section 2: MARCO TEÓRICO] (≈4000 palabras)
- 2.1 Formalización: La Función de Filtrado por Credulidad
- 2.2 Aplicación: El Caso de los Memes Populistas
- 2.3 Extensión: Competencia de Memeplexos en Derecho Internacional

[Section 3: VALIDACIÓN EMPÍRICA] (≈3500 palabras)
- 3.1 Datos y Metodología
- 3.2 Resultados Principales
- 3.3 Análisis de Casos Ilustrativos
- 3.4 Robustez y Limitaciones

[Section 4: VALIDACIÓN HISTÓRICA ARGENTINA] (≈2500 palabras)
- 4.1 Metodología de Análisis Histórico
- 4.2 Casos Históricos Específicos
- 4.3 Patrón Agregado

[Section 5: IMPLICACIONES] (≈2000 palabras)
- 5.1 Lecciones para Reformadores
- 5.2 Limitaciones Éticas
- 5.3 Agenda de Investigación Futura

[Section 6: CONCLUSIONES] (≈1500 palabras)
- 6.1 Contribuciones Teóricas
- 6.2 Hallazgos Empíricos Principales
- 6.3 Implicaciones Prácticas
- 6.4 Reflexión Final

[REFERENCIAS] (≈150 entradas)

[APÉNDICES]
- Appendix A: Codificación Detallada de C Score
- Appendix B: Robustez Estadística
- Appendix C: Código de Replicación
```

**LONGITUD TOTAL ESPERADA**: 12,000-15,000 palabras (≈40-50 páginas)

-----

**FIN DEL PROMPT COMPLETO**
