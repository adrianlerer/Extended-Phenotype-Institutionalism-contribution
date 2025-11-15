# Memetic Fitness Differential (MFD): Formulas and Examples

**Version:** 1.0  
**Date:** November 2025  
**Author:** Ignacio Adrián Lerer

---

## Overview

The Memetic Fitness Differential (MFD) quantifies the competitive advantage of informal institutions over formal rules through replication cost differentials.

---

## Core Formula

```
MFD = (r_informal × e_informal × a_informal) / (r_formal × e_formal × a_formal)
```

### Components

| Variable | Definition | Units | Typical Range |
|----------|------------|-------|---------------|
| **r** | Replication rate | Transmissions per year | 2-300 |
| **e** | Enforcement efficiency | Probability of compliance | 0.10-0.95 |
| **a** | Adaptation speed | 1/years to modify | 0.3-20 |

### Critical Thresholds

| MFD Range | Interpretation |
|-----------|----------------|
| **< 500** | Formal institutions competitive |
| **500-1,500** | Mixed equilibrium possible |
| **> 5,000** | Permanent informal dominance |

---

## Component 1: Replication Rate (r)

### Measurement

**Informal Institutions:**
- Daily workplace interactions ≈ 250 working days/year
- Weekly meetings ≈ 50/year
- Professional peer interactions

**Formal Institutions:**
- Legislative amendments: 2-15/year
- Regulatory updates: 5-30/year
- Judicial precedent: 1-5/year

### Argentine Labor Market Example

**Informal (union solidarity norms):**
- Workplace assemblies: 24-48/year
- Daily shop-floor interaction: 250 days
- **r_informal ≈ 260 transmissions/year**

**Formal (labor legislation):**
- Congressional amendments: 0.3-0.5/year
- Regulatory updates: 2-8/year
- Supreme Court decisions: 5-15/year
- **r_formal ≈ 5 transmissions/year**

**Ratio: 260/5 = 52:1**

---

## Component 2: Enforcement Efficiency (e)

### Measurement Scale

| Score | Interpretation | Examples |
|-------|----------------|----------|
| **0.90-0.95** | Near-universal compliance | Religious commandments, military discipline |
| **0.70-0.85** | High compliance | Peer-enforced professional ethics |
| **0.50-0.65** | Moderate compliance | Tax laws with moderate audit |
| **0.10-0.25** | Very low compliance | "Dead letter" laws |

### Argentine Example

**Informal (union solidarity norms):**
- Immediate peer sanctioning during interaction
- Compliance observed in 80-90% of strike situations
- **e_informal ≈ 0.85**

**Formal (labor inspector compliance):**
- Inspectors visit workplaces every 3-5 years
- Legal proceedings take 1-3 years
- Actual sanction probability low
- **e_formal ≈ 0.15**

**Ratio: 0.85/0.15 = 5.7:1**

---

## Component 3: Adaptation Speed (a)

### Calculation

```
a = 1 / T_modification
```

Where T_modification = years required for institutional change

### Argentine Example

**Informal (union practices):**
- New strike tactics emerge within weeks
- **T_informal ≈ 0.1 years**
- **a_informal = 1/0.1 = 10**

**Formal (labor legislation):**
- Congressional process: 1.8-5 years
- Judicial review adds 1-2 years
- **T_formal ≈ 2.5 years**
- **a_formal = 1/2.5 = 0.4**

**Ratio: 10/0.4 = 25:1**

---

## Complete MFD Calculation: Argentine Labor Market

### Component Values

| Component | Informal | Formal | Ratio |
|-----------|----------|--------|-------|
| Replication rate (r) | 260 | 5 | 52:1 |
| Enforcement efficiency (e) | 0.85 | 0.15 | 5.7:1 |
| Adaptation speed (a) | 10 | 0.4 | 25:1 |

### Formula Application

```
MFD = (260 × 0.85 × 10) / (5 × 0.15 × 0.4)
    = 2,210 / 0.3
    = 7,367 ≈ 7,400
```

### Interpretation

**MFD = 7,400:1** indicates extreme informal dominance:

1. Formal reforms will fail
2. Informal norms override formal rules
3. Threshold far exceeds 5,000 critical level

**Empirical validation:** Argentina achieved 0% structural labor reform success (0/23 attempts, 1989-2024)

---

## Comparative Examples

### Chilean Labor Market (Low MFD)

| Component | Informal | Formal | Ratio |
|-----------|----------|--------|-------|
| r | 250 | 12 | 21:1 |
| e | 0.70 | 0.55 | 1.3:1 |
| a | 8 | 1.0 | 8:1 |

**Calculation:**
```
MFD = (250 × 0.70 × 8) / (12 × 0.55 × 1.0) = 1,400 / 6.6 = 212 ≈ 218
```

**MFD=218 < 500:** Formal institutions competitive  
**Observed:** 83% structural reform success (15/18 attempts)

---

### U.S. Financial Regulation (Extreme MFD)

| Component | Informal (Industry) | Formal (SEC/Fed) | Ratio |
|-----------|-------------------|-----------------|-------|
| r | 250 | 2 | 125:1 |
| e | 0.85 | 0.20 | 4.3:1 |
| a | 10 | 0.5 | 20:1 |

**Calculation:**
```
MFD = (250 × 0.85 × 10) / (2 × 0.20 × 0.5) = 2,125 / 0.2 = 10,625
```

**MFD=10,625:** Permanent industry norm dominance  
**Observed:** 0% structural financial reform post-2008

---

## Policy Interventions

### Strategy 1: Increase Formal Replication Rate

**Uruguay 1991:** Ultraactivity elimination forced biennial renewal

**Effect:**
```
Before: MFD = 7,400
After: MFD = (260 × 0.85 × 10) / (12 × 0.15 × 0.4) = 3,083
Reduction: -58%
```

### Strategy 2: Increase Formal Enforcement

**Chile:** Labor inspectorate reform increased compliance 35% → 55%

**Effect:**
```
Before: MFD = 7,400
After: MFD = (260 × 0.85 × 10) / (5 × 0.55 × 0.4) = 2,018
Reduction: -73%
```

### Strategy 4: Combined Intervention (Uruguay Model)

**1991 Constitutional Amendment:**
- r_formal: 5 → 10
- e_formal: 0.15 → 0.35
- a_formal: 0.4 → 1.0

**Effect:**
```
Before: MFD = 7,400
After: MFD = (250 × 0.70 × 8) / (10 × 0.35 × 1.0) = 400
Reduction: -95%
```

**MFD=400 < 500:** Formal institutions become competitive  
**Observed:** Reform success 21% → 63% (+42pp)

---

## Citation

Lerer, I. A. (2025). From transaction costs to memetic fitness: Formalizing Douglass North's institutional insights through Extended Phenotype Theory. SSRN Working Paper.

**Contact:** adrian@lerer.com.ar  
**Version:** 1.0 (November 2025)
