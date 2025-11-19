# Data Collection Protocol

## Dataset: Sovereignty-Globalism Competition in International Law

**Version**: 1.0.0  
**Date**: 2025-10-15  
**Status**: Synthetic Dataset (Methodological Demonstration)

---

## 1. Research Question

**Primary Question**: Do crisis events (economic shocks, pandemics, geopolitical disruptions) causally increase the probability of sovereignty-oriented outcomes in international law cases?

**Hypothesis (H5 - Crisis Catalysis)**:  
Crisis events act as selective pressures that favor sovereignty phenotypes over globalism phenotypes in legal argumentation.

---

## 2. Conceptual Framework

### Theoretical Foundation: Extended Phenotype Theory (Dawkins, 1982)

**Core Concepts**:
- **Replicators**: Sovereignty meme vs Globalism meme
- **Phenotypes**: Legal doctrines, institutional arrangements, treaty regimes
- **Selective Events**: Legal cases as moments of natural selection between competing phenotypes
- **Niche Space**: 12-dimensional IusSpace representing institutional contexts
- **Fitness**: Argumental strength × structural compatibility with niche

**Key Insight**:  
Legal cases are not random events but **selective events** where competing legal phenotypes (sovereignty vs globalism) compete for dominance. Crisis events may act as **environmental perturbations** that alter fitness landscapes.

---

## 3. Case Selection Criteria

### 3.1 Inclusion Criteria

**Required Characteristics**:
1. **Subject Matter**: Cases involving tension between national sovereignty and supranational/international norms
2. **Temporal Range**: Decided between 2002-2023 (covers pre/post 2008 crisis)
3. **Jurisdictional Diversity**: Multiple jurisdictions across integration levels
4. **Argumentation Quality**: Sufficient legal reasoning in written opinions to code phenotype scores

**Specific Case Types**:
- Treaty compliance disputes
- Supranational court jurisdiction challenges
- Human rights vs national sovereignty conflicts
- Trade agreement enforcement
- International criminal law cooperation
- Migration and border sovereignty
- Economic sanctions and financial sovereignty

### 3.2 Exclusion Criteria

**Cases Excluded**:
1. Purely domestic cases with no international law dimension
2. Cases without accessible written opinions
3. Cases decided by non-judicial bodies (e.g., arbitration panels without reasoned opinions)
4. Cases where sovereignty-globalism dimension is not salient

---

## 4. Data Collection Workflow

### Phase 1: Case Identification

**Sources** (for real data implementation):
1. **International Courts**:
   - International Court of Justice (ICJ)
   - European Court of Human Rights (ECtHR)
   - Court of Justice of the European Union (CJEU)
   - Inter-American Court of Human Rights (IACHR)
   
2. **National Supreme Courts**:
   - Cases involving international law questions
   - Accessed via national court databases or WestLaw/LexisNexis

3. **Specialized Databases**:
   - Oxford Public International Law database
   - Hague Academy of International Law
   - Regional integration court databases

**Search Strategy**:
```
Keywords: "sovereignty", "international obligation", "treaty compliance", 
          "supranational authority", "domestic jurisdiction", "margin of appreciation"

Temporal Filter: 2002-2023
Language: English, Spanish, French (with translation where needed)
```

### Phase 2: Case Coding

**Variables to Code** (See `DATA_DICTIONARY.md` for detailed definitions):

#### 4.1 Basic Identifiers
- `Case_ID`: Generate systematic identifier (CRISIS_XX or CONTROL_XX)
- `Country`: Jurisdiction of deciding court
- `Year`: Year of decision

#### 4.2 Treatment Variable
- `Crisis_Catalyzed`: Code `1` if case decided within 2 years of crisis onset

**Crisis Windows**:
- **2008 Financial Crisis**: 2008-2012
- **European Sovereign Debt Crisis**: 2010-2015
- **COVID-19 Pandemic**: 2020-2023
- **Regional crises**: Case-by-case determination

**Coding Protocol**:
1. Identify decision date
2. Check if decision falls within crisis window
3. Code `1` if yes, `0` if no
4. Document crisis event in notes

#### 4.3 Outcome Variable
- `Sovereignty_Phenotype_Score`: Continuous score (0.0-1.0)

**Measurement Protocol** (IusMorfos V6.0):
1. **Text Extraction**: Extract full text of legal opinion
2. **Indicator Identification**: Identify sovereignty vs globalism linguistic markers
3. **Weighted Scoring**:
   - Count sovereignty indicators (e.g., "national interest", "sovereign prerogative")
   - Count globalism indicators (e.g., "international obligation", "global norms")
   - Apply weights based on prominence in argumentation (dicta vs ratio decidendi)
4. **Normalization**: Convert to 0-1 scale

**Sovereignty Indicators** (examples):
- Invocation of domestic constitutional law over treaties
- Emphasis on "margin of appreciation" or "domestic discretion"
- Rejection of supranational court jurisdiction
- Appeals to national security or public order

**Globalism Indicators** (examples):
- Prioritization of treaty obligations over domestic law
- Acceptance of supranational court jurisdiction
- Invocation of jus cogens or universal norms
- Appeals to "international community" or "common values"

**Inter-Coder Reliability**:
- For real data: Use multiple coders and calculate Cohen's Kappa (target κ ≥ 0.70)
- Resolve disagreements through consensus discussion

#### 4.4 Covariates

**4.4.1 IusSpace_Dim12 (Integration Level)**

**Measurement Components**:
1. **Treaty Ratification Density** (0-2.5 points):
   - Count major international treaties ratified
   - Weight by depth of commitment (e.g., EU treaties > bilateral treaties)
   
2. **Supranational Court Jurisdiction** (0-2.5 points):
   - 0: No acceptance
   - 1.25: Partial acceptance (with reservations)
   - 2.5: Full acceptance
   
3. **Sovereignty Pooling Arrangements** (0-2.5 points):
   - 0: No pooling
   - 1.25: Sectoral pooling (e.g., trade agreements)
   - 2.5: Comprehensive pooling (e.g., EU membership)
   
4. **International Organization Membership** (0-2.5 points):
   - Weighted by depth of integration (UN membership = 0.5, EU membership = 2.5)

**Total Score**: Sum of 4 components (Range: 0-10)

**Data Sources**:
- UN Treaty Database
- Regional integration organization databases
- World Bank Governance Indicators

**4.4.2 Geographic_Region**

**Coding**:
- Use UN regional classification system
- Categories: Europe, LatAm, Asia, Africa, NorthAm, Oceania

**4.4.3 Legal_Family**

**Coding**:
- Common Law: UK, USA, Commonwealth jurisdictions
- Civil Law: Continental Europe, Latin America
- Mixed: Jurisdictions with hybrid systems (e.g., South Africa, Quebec)

**Reference**: JuriGlobe - World Legal Systems Research Group

---

## 5. Data Quality Control

### 5.1 Validation Checks

**Pre-Analysis Checks**:
1. **Completeness**: Verify no missing data for key variables
2. **Range Checks**: Ensure all continuous variables within valid ranges
3. **Logical Consistency**: 
   - Crisis_Catalyzed = 1 → Year within crisis window
   - IusSpace_Dim12 for EU members should be ≥ 7.0
4. **Duplicate Detection**: Check for duplicate Case_IDs

### 5.2 Codebook Alignment

**Requirement**: All variables must match definitions in `DATA_DICTIONARY.md`

**Verification**:
```python
# Column names must match exactly
required_columns = [
    'Case_ID', 'Country', 'Year', 'Crisis_Catalyzed',
    'Sovereignty_Phenotype_Score', 'IusSpace_Dim12',
    'Geographic_Region', 'Legal_Family'
]
```

### 5.3 Documentation

**Required Documentation**:
1. **Case Notes**: Brief description of each case (separate file)
2. **Coding Decisions**: Log of non-obvious coding choices
3. **Data Provenance**: Source of each case (court, database, etc.)
4. **Version Control**: Date of coding, coder ID, revision history

---

## 6. Synthetic Data Generation (Current Dataset)

### 6.1 Purpose

**Why Synthetic Data?**:
- Methodological demonstration of PSM technique
- Proof-of-concept for analytical framework
- Template for real data collection

### 6.2 Generation Protocol

**Approach**: Parametric simulation preserving realistic structures

**Steps**:
1. **Define Distributions**:
   - Year: Uniform(2002, 2023)
   - Crisis_Catalyzed: Bernoulli(p=0.286) with temporal clustering
   - Sovereignty_Phenotype_Score: Beta(α=2, β=1.5) → right-skewed
   - IusSpace_Dim12: Normal(μ=5.5, σ=2.0), truncated [0,10]

2. **Impose Correlations**:
   - Crisis_Catalyzed × Sovereignty_Phenotype_Score: Weak positive correlation (ρ≈0.15)
   - IusSpace_Dim12 × Sovereignty_Phenotype_Score: Negative correlation (ρ≈-0.30)
   - Geographic_Region × IusSpace_Dim12: Europe higher than LatAm

3. **Sample Sizes**:
   - Total N = 70
   - Treatment (Crisis) = 20 (28.6%)
   - Control (Non-Crisis) = 50 (71.4%)

4. **Validation**:
   - Check distributional properties match theoretical expectations
   - Ensure sufficient overlap in propensity scores (common support ≥ 70%)

**Code**: See `src/data_processing/generate_synthetic_data.py` (if applicable)

---

## 7. Transition to Real Data

### 7.1 Replacement Protocol

**When Ready to Use Real Cases**:

1. **Collect Real Cases** following criteria in Section 3
2. **Code Variables** following protocols in Section 4
3. **Quality Control** following Section 5
4. **Replace File**: Overwrite `data/sovereignty_synthetic_parsed.csv` with real data
5. **Update Documentation**:
   - Update this file (DATA_COLLECTION_PROTOCOL.md) with actual sources
   - Update DATA_DICTIONARY.md with real summary statistics
   - Document any protocol deviations

### 7.2 Sample Size Considerations

**Minimum Requirements for PSM**:
- Total N ≥ 50 (current: 70 ✓)
- Treatment group N ≥ 10 (current: 20 ✓)
- Control group N ≥ 2 × Treatment N (current: 50 ≥ 40 ✓)
- Common support coverage ≥ 70% (achieved: 82.9% ✓)

**Recommended**:
- Total N ≥ 100 for more robust estimates
- Larger treatment group (N ≥ 30) for better precision

---

## 8. Ethical Considerations

### 8.1 Data Privacy

**Public Court Decisions**:
- All cases should be publicly available court decisions
- No confidential or sealed cases included
- Case identifiers anonymized if needed for sensitive jurisdictions

### 8.2 Research Ethics

**Transparency**:
- Clearly distinguish synthetic from real data
- Document all coding decisions and subjective judgments
- Make codebook and protocol publicly available
- Provide replication materials

**Bias Mitigation**:
- Use multiple coders to reduce individual bias
- Pre-register hypotheses when possible
- Report null findings (do not p-hack)

---

## 9. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-10-15 | Initial protocol for synthetic dataset | I.A. Lerer |

---

## 10. References

### Theoretical Framework
- Dawkins, R. (1982). *The Extended Phenotype*. Oxford University Press.
- Lerer, I.A. (2025). "Law as Extended Phenotype: An Evolutionary Framework for Legal Comparison" (SSRN).

### Methodological References
- Rosenbaum, P.R., & Rubin, D.B. (1983). "The Central Role of the Propensity Score in Observational Studies for Causal Effects". *Biometrika*, 70(1), 41-55.
- Austin, P.C. (2011). "An Introduction to Propensity Score Methods for Reducing the Effects of Confounding in Observational Studies". *Multivariate Behavioral Research*, 46(3), 399-424.

### Legal Data Sources (for real implementation)
- International Court of Justice: https://www.icj-cij.org/
- European Court of Human Rights: https://hudoc.echr.coe.int/
- Oxford Public International Law: https://opil.ouplaw.com/
- JuriGlobe Legal Systems: http://www.juriglobe.ca/

---

## Contact

**Protocol Questions**: [Insert contact email]  
**GitHub Issues**: [Repository URL]/issues

---

**Last Updated**: 2025-10-15  
**Next Review**: When transitioning to real data
