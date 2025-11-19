# Dataset Structure: Clerical Orthodoxy and Reform Effectiveness
## 50 Jurisdictions, 3 Legal Domains (n=150)

---

## Dataset Schema

### Unit of Analysis
**Jurisdiction × Legal Domain**
- Each jurisdiction is coded across 3 legal domains: Criminal Law, Labor Law, Constitutional Law
- Total observations: 50 jurisdictions × 3 domains = 150

### Variables Structure

#### Identifying Variables
1. `jurisdiction_id` (string): Unique identifier
2. `jurisdiction_name` (string): Full name
3. `legal_domain` (categorical): Criminal | Labor | Constitutional
4. `region` (categorical): Latin_America | Europe | Common_Law | Asia | Africa
5. `legal_system` (categorical): Civil_Law | Common_Law | Mixed

#### Independent Variable: Clerical Strength Index (CSI)
**Range:** 0.0-1.0 (continuous)

**Component 1: Endogamy_Score** (weight: 0.30)
- `citation_endogamy_rate` (0.0-1.0): % of citations within same doctrinal tradition
  - **Measurement:** Sample 30 articles from top 3 journals in domain (2019-2024)
  - **Coding:** Count citations to same-tradition vs. different-tradition authors
  - **Sources:** Google Scholar, Scopus, SciELO, HeinOnline

**Component 2: Sacralization_Score** (weight: 0.25)
- `sacred_language_frequency` (0.0-1.0): Frequency of absolutist deontological terms per 10k words
  - **Measurement:** NLP analysis of 20 most-cited texts in domain
  - **Terms tracked:** "inalienable", "inviolable", "sacred", "absolute", "non-negotiable"
  - **Normalization:** Compare to baseline from hard sciences
  
- `empirical_resistance` (0.0-1.0): Documented cases of empirical evidence rejected on moral grounds
  - **Measurement:** Count controversies where evidence was dismissed as "neoliberal", "reductionist", etc.
  - **Sources:** Academic controversies, journal rejection patterns, conference exclusions

**Component 3: Costly_Signaling_Score** (weight: 0.20)
- `orthodoxy_requirement` (0.0-1.0): Degree of ideological conformity required for membership
  - **Measurement:** Analysis of hiring patterns, association membership requirements
  - **Proxy:** % of faculty hired from same doctrinal school
  - **Sources:** University websites, academic genealogy databases

- `exclusion_rate` (0.0-1.0): Rate of heterodox scholars excluded from conferences/journals
  - **Measurement:** Document cases of exclusion for ideological (not quality) reasons
  - **Sources:** Conference programs, editorial board changes, controversies

**Component 4: Institutional_Control_Score** (weight: 0.25)
- `journal_concentration` (0.0-1.0): Herfindahl index of control over top journals
  - **Measurement:** H = Σ(si²) where si = market share of doctrinal tradition i
  - **Sources:** Journal editorial boards, citation networks

- `gatekeeper_concentration` (0.0-1.0): % of decision-making forums controlled by single tradition
  - **Measurement:** Count editorial boards, conference committees, academic chairs
  - **Sources:** Institutional websites, professional associations

**CSI Calculation:**
```
CSI = (0.30 × Endogamy) + (0.25 × Sacralization) + (0.20 × Costly_Signaling) + (0.25 × Control)
```

#### Dependent Variable: Reform Effectiveness Index (REI)
**Range:** 0.0-1.0 (continuous)

**Component 1: Implementation_Rate** (weight: 0.30)
- `reforms_proposed` (integer): Number of significant reform proposals (2010-2024)
- `reforms_implemented` (integer): Number successfully enacted
- `implementation_rate` (0.0-1.0): reforms_implemented / reforms_proposed
- `implementation_speed` (months): Average time from proposal to enactment
- **Sources:** Legislative databases, official gazettes, policy trackers

**Component 2: Outcome_Alignment** (weight: 0.40)
- For each reform: measure stated objective vs. actual outcome
- `alignment_score` (-1.0 to +1.0): Direction and magnitude of effect
  - +1.0: Strong movement toward stated goal (>20%)
  - +0.5: Moderate movement toward goal (10-20%)
  - 0.0: No significant change (<10%)
  - -0.5: Moderate movement away from goal
  - -1.0: Strong movement away from goal (>20%)
- **Example (Criminal Law):** If reform aims to reduce incarceration:
  - Measure: Pre-reform incarceration rate vs. 3-years-post rate
  - If rate decreased 25% → alignment = +1.0
  - If rate increased 15% → alignment = -0.5
- **Sources:** National statistics, OECD, World Bank, ILO, academic evaluations

**Component 3: Adaptability_Score** (weight: 0.30)
- `evaluation_mechanisms` (0.0-1.0): Presence of sunset clauses, mandatory reviews
- `evidence_based_revisions` (0.0-1.0): Rate of reforms modified based on evidence
- `reversal_rate` (0.0-1.0): 1 - (% reforms reversed within 5 years)
- **Sources:** Legislative texts, evaluation reports, amendment records

**REI Calculation:**
```
REI = (0.30 × Implementation) + (0.40 × Alignment) + (0.30 × Adaptability)
```

#### Control Variables
1. `gdp_per_capita` (float): World Bank data (2020)
2. `population` (integer): UN data (2020)
3. `democracy_score` (0-10): V-Dem Liberal Democracy Index (2020)
4. `rule_of_law_score` (0-1): World Bank Governance Indicators (2020)
5. `ideological_orientation` (categorical): Left | Center | Right | Mixed
   - Based on dominant legal academic orientation in past 20 years

---

## Jurisdictions List (n=50)

### Latin America (n=15)
1. Argentina (Civil Law)
2. Brazil (Civil Law)
3. Chile (Civil Law)
4. Uruguay (Civil Law)
5. Colombia (Civil Law)
6. Mexico (Civil Law)
7. Peru (Civil Law)
8. Venezuela (Civil Law)
9. Bolivia (Civil Law)
10. Ecuador (Civil Law)
11. Paraguay (Civil Law)
12. Costa Rica (Civil Law)
13. Panama (Civil Law)
14. Guatemala (Civil Law)
15. Dominican Republic (Civil Law)

### Europe (n=15)
16. Germany (Civil Law)
17. France (Civil Law)
18. United Kingdom (Common Law)
19. Spain (Civil Law)
20. Italy (Civil Law)
21. Netherlands (Civil Law)
22. Sweden (Civil Law)
23. Norway (Civil Law)
24. Denmark (Civil Law)
25. Finland (Civil Law)
26. Poland (Civil Law)
27. Portugal (Civil Law)
28. Belgium (Civil Law)
29. Austria (Civil Law)
30. Switzerland (Civil Law)

### Common Law (n=10)
31. United States - Federal (Common Law)
32. United States - California (Common Law)
33. United States - Texas (Common Law)
34. United States - New York (Common Law)
35. United States - Illinois (Common Law)
36. Canada (Common Law)
37. Australia (Common Law)
38. New Zealand (Common Law)
39. India (Mixed)
40. South Africa (Mixed)

### Asia (n=5)
41. Japan (Civil Law)
42. South Korea (Civil Law)
43. Taiwan (Civil Law)
44. Singapore (Mixed)
45. Israel (Mixed)

### Africa (n=5)
46. South Africa (Mixed) [duplicate, replace with:]
46. Kenya (Mixed)
47. Nigeria (Mixed)
48. Ghana (Mixed)
49. Egypt (Civil Law)
50. Morocco (Civil Law)

---

## Data Collection Protocol

### Phase 1: Pilot Study (n=15)
**Objective:** Validate methodology with deep-dive cases
**Jurisdictions:** 5 from each region (Argentina, Chile, Germany, UK, USA-Federal)
**Domains:** All 3 per jurisdiction (n=15 observations)
**Timeline:** Week 1-2

### Phase 2: Expansion (n=60)
**Objective:** Code additional 20 jurisdictions × 3 domains
**Timeline:** Week 3-6

### Phase 3: Completion (n=150)
**Objective:** Complete remaining 15 jurisdictions × 3 domains
**Timeline:** Week 7-8

---

## Data Quality Standards

### Minimum Requirements per Observation
1. **CSI Components:** At least 3 of 4 components must have primary source data
2. **REI Components:** At least 5 reforms coded per jurisdiction-domain
3. **Sources:** Minimum 3 independent sources per variable
4. **Verification:** Cross-reference with secondary literature when available

### Coding Reliability
- **Intercoder reliability:** Target Krippendorff's α > 0.80 (if second coder available)
- **Transparency:** All coding decisions documented in supplementary material
- **Uncertainty:** Variables with low confidence flagged for sensitivity analysis

### Missing Data Protocol
- **Acceptable threshold:** <10% missing data per variable
- **Handling:** Multiple imputation if missing data is random; listwise deletion if systematic
- **Reporting:** All missing data patterns reported in appendix

---

## Expected Correlations (Predictions)

### H1: Primary Hypothesis
**r(CSI, REI) < -0.50, p < 0.01**
- Prediction: Strong negative correlation
- Falsification threshold: If r > -0.20 or p > 0.10, hypothesis rejected

### H2: Threshold Effect
**Piecewise regression shows threshold at CSI ≈ 0.65**
- Below threshold: Weak or no effect
- Above threshold: Strong negative effect
- Test: Chow test for structural break

### H3: Ideological Independence
**r(CSI, REI) persists controlling for ideological_orientation**
- Test: Partial correlation controlling for ideology
- Prediction: Partial r remains < -0.40

### H4: Regional Robustness
**Effect persists within regions**
- Latin America: r < -0.40
- Europe: r < -0.40
- Common Law: r < -0.40
- Test: Stratified correlation analysis

---

## Deliverables

1. **Raw Dataset** (`dataset_raw.csv`): All coded variables with sources
2. **Clean Dataset** (`dataset_clean.csv`): Processed data for analysis
3. **Codebook** (`codebook.md`): Variable definitions, coding rules, sources
4. **Analysis Script** (`analysis.R` or `analysis.py`): Reproducible statistical analysis
5. **Jupyter Notebook** (`analysis.ipynb`): Interactive exploration and visualization
6. **Supplementary Materials** (`appendix_sources.md`): Complete bibliography per observation

---

**Version:** 1.0  
**Date:** 2025-11-18  
**Author:** Ignacio Adrian Lerer
