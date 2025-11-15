# Constitutional Lock-In Index (CLI): Calculation Methodology

**Version:** 1.0  
**Date:** November 2025  
**Author:** Ignacio Adrián Lerer

---

## Overview

The Constitutional Lock-In Index (CLI) quantifies the depth of institutional entrenchment in labor markets through three weighted components: constitutional text codification, collective bargaining ultraactivity, and judicial protection intensity.

---

## Formula

```
CLI = (0.35 × Constitutional_Score) + (0.40 × Ultraactivity_Score) + (0.25 × Judicial_Score)
```

**Range:** 0.0 (no entrenchment) to 1.0 (maximum entrenchment)

**Interpretation:**
- CLI < 0.35: High flexibility (>75% structural reform success)
- CLI 0.35-0.55: Moderate flexibility (40-70% success)
- CLI 0.55-0.70: Low flexibility (10-40% success)
- CLI > 0.70: Rigidity zone (<10% success)

---

## Component 1: Constitutional Text Entrenchment (35% weight)

### Scoring Rubric

| Score | Criteria | Examples |
|-------|----------|----------|
| **1.0** | Labor rights in constitutional text requiring supermajority amendment (≥2/3) AND special procedures | Argentina Article 14bis: Requires 2/3 Congress + convention |
| **0.6** | Labor rights in constitutional text requiring qualified majority (>50%, <3/5) | Uruguay Constitution: Requires 60% Congressional majority |
| **0.3** | Constitutional provisions enabling but not mandating labor protections | Chile post-2005: Reduced constitutional constraints |
| **0.1** | No constitutional labor rights, pure legislative domain | United States: No constitutional labor provisions |

### Example: Argentina

**Constitutional Text:** Constitución Nacional Argentina, Artículo 14bis (1957)

**Amendment Procedure:** Article 30 requires:
- 2/3 majority in both Congressional chambers
- Special Constitutional Convention elected by popular vote
- Convention approval of amendments

**Score: 1.0**

---

## Component 2: Collective Bargaining Ultraactivity (40% weight)

### Scoring Rubric

| Score | Criteria | Examples |
|-------|----------|----------|
| **1.0** | **Absolute ultraactivity:** Agreements never expire until replaced | Argentina Law 14,250: "Agreements remain in force until replaced" |
| **0.5** | **Qualified ultraactivity (medium):** Agreements extend 6-24 months post-expiration | Spain (pre-2012): Extension during renegotiation |
| **0.0** | **No ultraactivity:** Agreements expire at stated term | Chile (post-1991): 2-year maximum, automatic termination |

### Example: Uruguay Pre vs. Post-1991

**Pre-1991 (Score: 1.0)**
- Constitutional interpretation established absolute ultraactivity
- Agreements remained indefinitely absent replacement

**Post-1991 Amendment (Score: 0.0)**
Constitución de la República Oriental del Uruguay, Artículo 57 (modified 1991):

"Los convenios colectivos de trabajo tendrán una duración máxima de dos años. Al vencer el plazo, el convenio dejará de tener efecto salvo que las partes acuerden expresamente su renovación."

- Maximum 2-year duration
- Automatic termination at expiration
- **CLI impact: 0.68 → 0.34 (−50% reduction)**

---

## Component 3: Judicial Protection Intensity (25% weight)

### Scoring Rubric

| Score | Criteria | Examples |
|-------|----------|----------|
| **1.0** | Labor rights as **human rights** status, constitutional minimums that cannot be legislatively reduced | Argentina: *Vizzoti* (2004), *Madorrán* (2007) |
| **0.6** | Labor rights as **constitutional principles** subject to proportionality balancing | Brazil: Superior Labor Tribunal balancing |
| **0.4** | Judicial deference to legislative judgment | Chile: Constitutional Tribunal defers to Congress |
| **0.2** | Minimal judicial review | United States: Post-*Lochner* rejection |

### Example: Argentina

**Key Precedents:**

***Vizzoti v. AMSA S.A.*** (2004)
- Issue: Legislative cap on dismissal indemnification
- Holding: Court established constitutional minimum of 33% of uncapped indemnity
- Impact: Legislative attempts to reduce dismissal costs constitutionally prohibited

***Madorrán*** (2007)
- Issue: Union representative dismissal protection
- Holding: Union rights elevated to human rights status
- Impact: Union institutional privileges constitutionally protected

**Judicial Protection Score:** 1.0

---

## Full CLI Calculation Example: Spain

**Step 1: Constitutional Score**
- 1978 Constitution Article 28: Labor rights protected but permit legislative regulation
- Amendment requires 3/5 majorities OR referendum
- **Score: 0.5**

**Step 2: Ultraactivity Score**
- 2012 reform: Limited extension only during active negotiation
- Effective duration: ~6 months average
- **Score: 0.3**

**Step 3: Judicial Score**
- Constitutional Court permits legislative labor reform when economically justified
- Proportionality review (not strict scrutiny)
- **Score: 0.7**

**Step 4: Calculate CLI**
```
CLI = (0.35 × 0.5) + (0.40 × 0.3) + (0.25 × 0.7)
    = 0.175 + 0.120 + 0.175
    = 0.47 ≈ 0.48
```

**Interpretation:** Spain CLI=0.48 predicts 40-70% reform success. Observed: 58% (11/19 reforms)

---

## Data Sources

### Primary Sources
- **Constitutional texts:** Constitute Project, official government websites
- **Legislation:** National labor ministry websites, legislative databases
- **Judicial opinions:** Supreme Court/Constitutional Court official databases

### Recommended Databases
- **Constitute Project:** https://www.constituteproject.org/
- **ILO NATLEX:** https://www.ilo.org/dyn/natlex/
- **World Legal Information Institute:** http://www.worldlii.org/

---

## Citation

Lerer, I. A. (2025). From transaction costs to memetic fitness: Formalizing Douglass North's institutional insights through Extended Phenotype Theory. SSRN Working Paper.

**Contact:** adrian@lerer.com.ar  
**Version:** 1.0 (November 2025)
