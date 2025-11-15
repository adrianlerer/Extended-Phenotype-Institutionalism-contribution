# Computational Tools for Institutional Analysis

**Version:** 1.0  
**Date:** November 2025  
**Author:** Ignacio Adrián Lerer

---

## Overview

Extended Phenotype Theory (EPT) operationalizes institutional analysis through three computational tools:

1. **RootFinder:** Constitutional archaeology through textual lineage tracing
2. **JurisRank:** Normative dominance mapping via legal citation networks
3. **IusMorfos:** Temporal institutional evolution and phylogenetic reconstruction

---

## Tool 1: RootFinder - Constitutional Archaeology

### Purpose
Traces legislative provisions backward through amendment chains to identify original source text and measure temporal persistence.

### Algorithm

```
INPUT: Current provision text, jurisdiction
OUTPUT: Root provision, amendment history, persistence metrics

PROCEDURE:
1. Text Ingestion
   - Parse constitutional texts into atomic provisions
   - Create timestamp for each version
   
2. Amendment Tracking
   - Identify explicit amendments through legislative metadata
   - Extract amendment dates and scope
   
3. Semantic Matching
   - Calculate similarity between successive versions
   - Use BERT embeddings → cosine similarity
   - Threshold: similarity > 0.85 = implicit amendment
   
4. Root Identification
   - Trace backward through amendment chain
   - Identify earliest provision version
   
5. Persistence Calculation
   - Temporal distance: Current_year - Root_year
   - Stability index: 1 - (Amendments / Years_in_existence)
```

### Example Output: Argentine Article 14bis

```yaml
Provision: Constitución Nacional Argentina, Artículo 14bis
Root_Date: 1949-03-11
Root_Text: "Constitución de 1949, Artículo 37 [identical text]"
Temporal_Persistence: 76 years (1949-2025)
Amendment_Attempts: 8 proposals
Successful_Amendments: 0
Stability_Index: 1.00
Semantic_Stability: 0.99
Classification: CONSTITUTIONAL_FOSSIL
```

### Comparative Analysis

| Metric | Argentina (Art. 14bis) | Chile (Art. 19.16) |
|--------|------------------------|-------------------|
| Root date | 1949 | 1980 |
| Temporal persistence | 76 years | 45 years |
| Successful amendments | 0 | 5 |
| Stability index | 1.00 | 0.89 |
| Semantic similarity | 0.99 | 0.62 |
| Classification | FOSSIL | EVOLVING |

---

## Tool 2: JurisRank - Normative Dominance Mapping

### Purpose
Applies PageRank algorithm to legal citation networks, identifying which provisions exercise greatest normative influence.

### Algorithm

```
INPUT: Legal corpus (statutes, judicial opinions, constitutional provisions)
OUTPUT: JurisRank scores (0-1), network topology metrics

PROCEDURE:
1. Network Construction
   - Nodes: Legal provisions
   - Edges: Citations (directed)
   
2. PageRank Calculation
   For each provision p:
   JR(p) = (1-d)/N + d × Σ[JR(q) / C(q)]
   
   Where:
   - d = damping factor (0.85)
   - N = total provisions
   - q = provisions citing p
   - C(q) = outbound citations from q
   
3. Network Topology Analysis
   - Centralization: Gini coefficient of JR scores
   - Hub identification: JR > 2 × median
```

### Example: Argentine Labor Law Network

```
Corpus: 1,247 Supreme Court decisions, 8,932 legislative provisions (1994-2024)

Top_5_Provisions:
  1. Constitución_Article_14bis: JR = 0.0247 (412 inbound citations)
  2. Law_14250_Ultraactivity: JR = 0.0198 (327 citations)
  3. Law_23551_Union_Monopoly: JR = 0.0156 (289 citations)

Median_JR: 0.0098
Article_14bis_Multiplier: 2.52× median

Network_Centralization: Gini = 0.73 (high centralization)
Top_10_Share: 18.4% of total JR mass
```

### Comparative Analysis

| Metric | Argentina | Chile |
|--------|-----------|-------|
| Top provision JR | 0.0247 | 0.0143 |
| Multiplier vs. median | 2.52× | 1.46× |
| Network centralization | 0.73 | 0.51 |
| Top 10 share | 18.4% | 12.7% |
| Structure | Hub-and-spoke | Distributed |

**Conclusion:** Argentine labor law exhibits higher centralization around Article 14bis, indicating concentrated normative authority.

---

## Tool 3: IusMorfos - Temporal Institutional Evolution

### Purpose
Tracks institutional evolution by constructing phylogenetic trees showing how provisions replicate, mutate, and diversify.

### Algorithm

```
INPUT: Multi-temporal legal corpus (all provision versions)
OUTPUT: Phylogenetic tree, evolutionary rates, extinction events

PROCEDURE:
1. Similarity Matrix Construction
   - Calculate pairwise semantic similarity (BERT embeddings)
   - Distance = 1 - similarity
   
2. Phylogenetic Reconstruction
   - Apply neighbor-joining algorithm
   - Root: Earliest provision version
   
3. Evolutionary Rate Calculation
   - Rate = Total_distance / Time_span
   - Units: Semantic changes per year
```

### Example: Argentine Ultraactivity Phylogeny

```
Root: 1953 Law 14,250 Article 6
├─ 1974 Supreme Court Díaz (Constitutional elevation)
│  └─ 2024 [Current: Original semantic content preserved]
└─ Reform attempts (8 EXTINCT branches, 1989-2024)

Temporal_Span: 72 years
Evolutionary_Rate: 0.014 changes/year (VERY SLOW)
Extinct_Branches: 8 reform attempts
Classification: FOSSIL with strong selection pressure
```

### Comparative: Chilean Collective Bargaining

```
Root: 1924 Law 4,053
├─ 1979 Labor Plan (Reconstruction)
│  └─ 1991 Law 19,069 (MAJOR MUTATION: ultraactivity elimination)
│     ├─ 2001 Reform (Expansion: subcontracting)
│     ├─ 2016 Reform (Mixed provisions)
│     └─ 2024 [Multiple viable branches coexisting]

Temporal_Span: 101 years
Evolutionary_Rate: 0.089 changes/year (6.4× FASTER than Argentina)
Extinct_Branches: 2 only
Classification: ADAPTIVE_RADIATION
```

---

## Integration: Using All Three Tools Together

### Workflow Example

**Step 1: RootFinder (Historical Depth)**
- Identify oldest provisions still in effect
- Calculate temporal persistence

**Step 2: JurisRank (Current Importance)**
- Map citation network
- Calculate centralization metrics

**Step 3: IusMorfos (Evolutionary Trajectory)**
- Construct phylogenetic trees
- Calculate evolutionary rates

**Step 4: Synthesis**
- Cross-reference: Do high-JR provisions have long persistence?
- Compare: Do slow-evolving institutions correlate with high centralization?
- Predict: Reform feasibility based on combined metrics

---

## Data Requirements

### Public Databases
- **Constitute Project:** https://www.constituteproject.org/
- **ILO NATLEX:** https://www.ilo.org/dyn/natlex/
- **World Legal Information Institute:** http://www.worldlii.org/

### National Databases (Argentina)
- **InfoLEG:** http://www.infoleg.gob.ar/
- **CSJN:** https://www.csjn.gov.ar/

### Computational Code
**GitHub Repository:** https://github.com/adrianlerer/Extended-Phenotype-Institutionalism-contribution

---

## Citation

Lerer, I. A. (2025). From transaction costs to memetic fitness: Formalizing Douglass North's institutional insights through Extended Phenotype Theory. SSRN Working Paper.

**Contact:** adrian@lerer.com.ar  
**Version:** 1.0 (November 2025)
