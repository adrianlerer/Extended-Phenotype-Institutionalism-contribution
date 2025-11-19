# EPT + Prakash & Sunstein Integration Project

## Overview

Este proyecto integra la teoría de **"Radical Constitutional Change"** de Prakash & Sunstein con el framework de **Extended Phenotype Theory (EPT)** para operacionalizar y cuantificar el concepto de "vértigo constitucional".

**Autores**:
- **Teoría Base**: Saikrishna Prakash & Cass Sunstein - "Radical Constitutional Change" (describen el fenómeno cualitativo)
- **Framework Computacional**: Ignacio Adrián Lerer - Extended Phenotype Theory + Herramientas EPT (cuantifica el cambio constitucional)

## Objetivo Central

**Operacionalizar** los conceptos cualitativos de P&S usando herramientas computacionales:

| Concepto P&S | Herramienta EPT | Output |
|--------------|-----------------|--------|
| **Extinction** (ideas se vuelven "unthinkable") | **RootFinder** | Extinction rate, half-life, genealogical tree |
| **Transplant success** (ideas migran entre jurisdicciones) | **IusMorfos** | Fitness score (0-1), compatibility matrix |
| **Ideological trajectory** (movimiento en "continuum of understandings") | **IusSpace** | 12D positioning, trajectory visualization |
| **Elite gatekeepers** (controlan qué ideas prosperan) | **Peralta** | Network centrality, ideological homophily |
| **Constitutional vertigo** (magnitud del cambio) | **Vertigo Index** | Unified metric (ΔFitness × Resistance / Time) |

## Arquitectura del Proyecto

```
ept_prakash_sunstein/
├── rootfinder/           # PARTE 1: Genealogical extinction analysis
├── iusmorfos/            # PARTE 2: Transplant success prediction
├── iusspace/             # PARTE 3: 12D constitutional positioning
├── peralta/              # PARTE 4: Elite network analysis
├── integration/          # PARTE 5: Vertigo Index calculation
├── data/
│   ├── input/            # Raw datasets
│   ├── output/           # Processed results
│   └── visualizations/   # Publication-ready figures
└── reports/              # Analysis markdown reports
```

## Datasets Disponibles

### 1. **60 Transnational Conflicts** (2000-2025)
- **File**: `data/dataset_PSM_60casos_clean.csv`
- **Variables**: Country, Year, Crisis_Catalyzed, Event_Name, Legal_Family, Conflict_Type, International_Tribunal
- **Uso**: Validación empírica de patrones de sovereignty vs globalism

### 2. **70 Sovereignty-Globalism Cases**
- **File**: `data/cases/sovereignty_globalism_complete_70cases.csv`
- **Variables**: Sovereignty_Phenotype_Score, Globalism_Phenotype_Score, IusSpace_Dim12_IntegrationScore, Outcome
- **Uso**: IusSpace positioning, fitness landscape mapping

### 3. **Historical Reforms Database** (Argentina)
- **Source**: `historical_reforms_database.csv` (a construir)
- **Period**: 1932-2025
- **Variables**: Reform_Name, Year, Complexity_Score, Survival_Years, Elite_Support
- **Uso**: Validation de half-life predictions, elite gatekeeper analysis

## Módulos y Status

### ✅ Módulo 1: RootFinder - Extinction Analysis
**Objetivo**: Medir extinción de memeplex "Wechsler Critique" (Freedom of Association anti-integration)

**Inputs**:
- Citation network: US Supreme Court cases citing Wechsler (1959-2025)
- Search corpus: Equal Protection cases mentioning "freedom of association"

**Outputs**:
- Extinction rate (% decline from peak)
- Half-life (years to 50% of peak citations)
- Genealogical tree visualization
- Statistical validation (Mann-Kendall trend test, bootstrap CI 95%)

**Predicted Results**:
- Extinction rate > 95%
- Half-life < 10 years
- Functional extinction year ≈ 1988

---

### ✅ Módulo 2: IusMorfos - Transplant Success Prediction
**Objetivo**: Predecir éxito de transplante "Nondelegation Doctrine" (US → Argentina)

**Inputs**:
- Source jurisdiction features (US constitutional structure)
- Target jurisdiction features (Argentina institutional capacity)
- Memeplex characteristics (ideological valence, institutional requirements)

**Outputs**:
- Fitness score (0-1 scale)
- Component breakdown: Environmental (0.40), Ideological (0.30), Institutional (0.20), Network (0.10)
- Comparative validation vs. historical transplants
- Sensitivity analysis (scenarios: Milei reforms, CSJN composition changes)

**Predicted Results**:
- Fitness ≈ 0.34 (LIKELY TO FAIL < 0.50 threshold)
- Key bottleneck: Environmental compatibility (civil law vs. common law = 0.20)

---

### ✅ Módulo 3: IusSpace - 12D Constitutional Positioning
**Objetivo**: Trazar trayectoria de "Income Tax Unconstitutionality" (Argentina 1932-2025)

**Inputs**:
- 8 time points (1932, 1935, 1949, 1957, 1994, 2001, 2015, 2025)
- 12-dimensional positioning:
  1. Sovereignty ↔ Globalism
  2. Originalism ↔ Living Constitution
  3. Judicial Restraint ↔ Activism
  4. Formal ↔ Substantive Equality
  5. Individual ↔ Collective Rights
  6. Market ↔ State Intervention
  7. Federalism ↔ Centralization
  8. Separation ↔ Fusion of Powers
  9. Textualism ↔ Purposivism
  10. Majoritarianism ↔ Countermajoritarian
  11. Procedural ↔ Substantive
  12. Stability ↔ Adaptability

**Outputs**:
- 3D trajectory visualization (PCA projection)
- Vertigo Index = Total distance traveled / time elapsed
- Fitness landscape mapping (2D slices)
- Comparative validation vs. US constitutional changes (Brown, Obergefell)

**Predicted Results**:
- Vertigo Index < 0.03 (MINIMAL vertigo = stasis)
- Trajectory shows minimal movement 1932-2015 (lock-in)
- 2025 Milei position = furthest from consensus (potential paradigm shift)

---

### ⏳ Módulo 4: Peralta Network - Elite Gatekeepers
**Objetivo**: Mapear red de élites jurídicas argentinas (1983-2025)

**Inputs**:
- Nodes: ~100-200 key actors (academics, CSJN justices, clerks, law firm partners)
- Edges: Coauthorship, citations, institutional affiliations, mentorship, litigation
- Attributes: Ideology (progressive, moderate, conservative, libertarian), institution, CSJN status

**Outputs**:
- Community detection (Louvain clustering)
- Centrality metrics (degree, betweenness, eigenvector, PageRank)
- Ideological homophily coefficient
- Top 20 gatekeepers identification
- Bootstrap validation (n=10,000 iterations, CI 95%)

**Predicted Results**:
- Ideological homophily > 0.60 (high clustering)
- Top 10% gatekeepers control >40% of information flow
- Reforms without gatekeeper support: <20% success rate

**Data Collection Status**: ⚠️ **PENDIENTE** - Requiere scraping de:
- Law faculty publications (UBA, UCA, UTDT)
- CSJN justice biographies + clerk rosters
- Constitutional law conference participants

---

### ⏳ Módulo 5: Integration - Vertigo Index
**Objetivo**: Crear métrica cuantitativa unificada del "vértigo constitucional"

**Formula**:
```
Vertigo Index (VI) = (ΔFitness × Elite_Resistance) / Adaptation_Time

Components:
- ΔFitness: from IusMorfos (change in memeplex fitness)
- Elite_Resistance: from Peralta (% of gatekeepers opposing × centrality)
- Adaptation_Time: from RootFinder + IusSpace (max of extinction + stabilization)
```

**Classification**:
- VI < 0.05: Minimal vertigo (incremental change)
- VI 0.05-0.15: Moderate vertigo
- VI 0.15-0.30: High vertigo (P&S's Brown v. Board range)
- VI > 0.30: Extreme vertigo (constitutional crisis)

**Validation Dataset**:
Compile VI for 10-15 canonical cases:
- Brown v. Board (1954): Expected VI ≈ 0.12
- Roe v. Wade (1973): Expected VI ≈ 0.18
- Obergefell (2015): Expected VI ≈ 0.10
- Dobbs (2022): Expected VI ≈ 0.25
- Argentina Income Tax (1935): Expected VI ≈ 0.01 (stasis, not vertigo)

**Success Criteria**:
- Correlation between calculated VI and P&S qualitative descriptions > 0.70
- VI correctly distinguishes "stasis" (Argentina) from "resolution" (US cases)

## Plan de Ejecución Modular

### **Week 1**: PROMPT 1 (RootFinder - Wechsler)
→ Output: Extinction metrics para caso testigo

### **Week 2**: PROMPT 2 (IusMorfos - Nondelegation)
→ Output: Fitness predictions para transplante doctrinal

### **Week 3**: PROMPT 3 (IusSpace - Argentina Income Tax)
→ Output: Trajectory visualization en 12D

### **Week 4**: PROMPT 4 (Peralta - Elite Networks)
→ Output: Network analysis con gatekeepers identificados

### **Week 5**: PROMPT 5 (Integration - Vertigo Index)
→ Output: Métrica unificada + validation dataset

## Deliverables Finales

Cada módulo produce:
1. ✅ **Python script ejecutable** (reproducible pipeline)
2. ✅ **Visualizations publication-ready** (PNG 300 DPI, vector SVG)
3. ✅ **Data files (.csv)** con resultados procesados
4. ✅ **Brief analysis report (.md)** (2-10 pages según complejidad)

**Replication Materials**:
- 5 Python modules (un pipeline completo)
- 15-20 figuras para manuscript
- Validation datasets (para supplements)
- GitHub repository con instrucciones paso a paso

## Prioridad de Ejecución

1. **ALTA PRIORIDAD** (ya tengo parte de los datos):
   - ✅ PROMPT 1 (RootFinder)
   - ✅ PROMPT 3 (IusSpace)

2. **PRIORIDAD MEDIA** (datos parciales):
   - ⏳ PROMPT 2 (IusMorfos)
   - ⏳ PROMPT 5 (Integration)

3. **REQUIERE DATA COLLECTION**:
   - ⚠️ PROMPT 4 (Peralta) - Necesita scraping manual de red de élites

## Tone & Style

- **Código**: Limpio, bien comentado, reproducible
- **Outputs**: Publication-ready visualizations
- **Explicaciones**: Técnicas pero concisas
- **Validación**: Estadística rigurosa (bootstrap, CI 95%)
- **Documentación**: Suficiente para replicar, no excesiva

## Referencias Clave

### Teoría Base:
- **Prakash & Sunstein** (2025): "Radical Constitutional Change" - Yale Law Journal (forthcoming)
- **Zahavi** (1975): "Mate selection—A selection for a handicap" - costly signaling
- **Dawkins** (1982): "The Extended Phenotype" - genes build beyond bodies

### Framework EPT Aplicado a Derecho:
- **Lerer** (2025): "Extended Phenotype Theory of Law" - SSRN
- **Lerer** (2025): "Constitutional Lock-In Index" - SSRN
- **Lerer** (2025): "Costly Signaling and Memetic Filtering" - SSRN

### Metodología:
- **Baron & Kenny** (1986): Mediation analysis
- **Cox** (1972): Proportional hazards model
- **Newman & Girvan** (2004): Community detection in networks
- **Mann-Kendall** (1975): Trend detection test

## Contacto

**Ignacio Adrián Lerer**
- ORCID: https://orcid.org/0009-0007-6378-9749
- GitHub: @adrianlerer
- SSRN Author Page: https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=6378749

---

**Status del Proyecto**: 🚧 **EN CONSTRUCCIÓN - PARTE 1 INICIADA**

**Última actualización**: 2025-10-31
