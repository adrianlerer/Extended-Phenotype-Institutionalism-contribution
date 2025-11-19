# Data Dictionary - Sovereignty-Globalism Dataset

## Dataset Overview

**File**: `sovereignty_synthetic_parsed.csv`  
**Cases**: 70 international law cases  
**Period**: 2002-2023  
**Treatment**: Crisis-catalyzed cases (N=20) vs control cases (N=50)

---

## Variable Definitions

### 1. `Case_ID` (String)
**Type**: Categorical identifier  
**Format**: `CRISIS_XX` or `CONTROL_XX` where XX is a sequential number  
**Example**: `CRISIS_01`, `CONTROL_03`  
**Description**: Unique identifier for each legal case in the dataset

**Coding Rules**:
- `CRISIS_XX`: Cases decided during or immediately after major economic/geopolitical crises (2008 financial crisis, COVID-19, etc.)
- `CONTROL_XX`: Cases decided during stable periods

---

### 2. `Country` (String)
**Type**: Categorical  
**Values**: Country names (e.g., Argentina, Belgium, Poland, etc.)  
**Description**: Jurisdiction where the legal case was decided

**Coding Notes**:
- Uses standard English country names
- Represents the deciding court's jurisdiction, not necessarily the country of origin of the legal dispute

---

### 3. `Year` (Integer)
**Type**: Temporal  
**Range**: 2002-2023  
**Description**: Year when the legal case was decided

**Distribution**:
- Pre-crisis period: 2002-2007
- Financial crisis period: 2008-2012
- Post-crisis period: 2013-2019
- COVID-19 period: 2020-2023

---

### 4. `Crisis_Catalyzed` (Binary)
**Type**: Treatment indicator  
**Values**: 
- `1` = Treatment group (crisis-catalyzed case)
- `0` = Control group (non-crisis case)

**Description**: Binary variable indicating whether the case was decided during or immediately following a major crisis event

**Crisis Events Considered**:
- 2008 Global Financial Crisis (2008-2012)
- European Sovereign Debt Crisis (2010-2015)
- COVID-19 Pandemic (2020-2023)
- Regional crises (e.g., Argentina 2001, Brexit 2016)

**Coding Protocol**:
- Cases within 2 years of crisis onset = `1`
- Cases outside crisis windows = `0`

---

### 5. `Sovereignty_Phenotype_Score` (Float)
**Type**: Continuous outcome variable  
**Range**: 0.0 - 1.0  
**Unit**: Probability/proportion scale  
**Description**: Strength of sovereignty-oriented argumentation in the case decision

**Interpretation**:
- **0.0-0.4**: Globalism-dominant (supranational norms prioritized)
- **0.4-0.6**: Mixed/balanced argumentation
- **0.6-1.0**: Sovereignty-dominant (national prerogatives prioritized)

**Measurement Method**:
IusMorfos V6.0 phenotype scoring algorithm:
1. Text mining of legal opinions for sovereignty vs globalism indicators
2. Weighted scoring based on:
   - Invocation of national vs supranational sources
   - Deference to domestic vs international institutions
   - Language emphasizing autonomy vs cooperation
3. Normalized to 0-1 scale

**Key Indicators**:
- **Sovereignty markers**: "national interest", "sovereign prerogative", "domestic law prevails"
- **Globalism markers**: "international obligation", "supranational authority", "global norms"

---

### 6. `IusSpace_Dim12` (Float)
**Type**: Continuous covariate  
**Range**: 0.0 - 10.0  
**Unit**: Integration level index  
**Description**: Institutional integration level of the jurisdiction (Dimension 12 of IusSpace)

**Interpretation**:
- **0-3**: Low integration (minimal supranational commitments)
- **3-7**: Medium integration (selective pooling of sovereignty)
- **7-10**: High integration (extensive supranational governance, e.g., EU member states)

**Measurement Components**:
1. Treaty ratification density
2. Supranational court jurisdiction acceptance
3. Sovereignty pooling arrangements (e.g., EU membership)
4. International organization membership depth

**Examples**:
- **Low (2.5)**: Minimally integrated jurisdictions with few binding international commitments
- **Medium (5.5)**: Moderate integration with selective treaty participation
- **High (8.5)**: Deeply integrated jurisdictions (e.g., EU core members)

---

### 7. `Geographic_Region` (String)
**Type**: Categorical covariate  
**Values**: 
- `Europe`
- `LatAm` (Latin America)
- `Asia` (if present)
- `Africa` (if present)
- `NorthAm` (North America, if present)

**Description**: Geographic region of the jurisdiction

**Coding Rules**:
- Based on standard UN regional classifications
- Used as proxy for regional legal culture and integration patterns

**Distribution in Dataset**:
- Europe: Majority (high institutional integration)
- LatAm: Significant minority (variable integration)
- Others: Minimal representation

---

### 8. `Legal_Family` (String)
**Type**: Categorical covariate  
**Values**:
- `Common Law`
- `Civil Law`
- `Mixed`

**Description**: Legal tradition of the jurisdiction

**Classification Criteria**:
- **Common Law**: Anglo-American tradition (precedent-based, adversarial)
- **Civil Law**: Romano-Germanic tradition (code-based, inquisitorial)
- **Mixed**: Hybrid systems or jurisdictions with multiple legal traditions

**Relevance**:
- Controls for structural differences in legal reasoning
- Common law systems may have different sovereignty discourse patterns than civil law systems

---

## Derived Variables (Created in Analysis)

### `Sovereignty_Win` (Binary)
**Type**: Binary outcome (derived)  
**Formula**: `Sovereignty_Win = 1 if Sovereignty_Phenotype_Score > 0.60 else 0`  
**Description**: Dichotomized outcome indicating whether sovereignty phenotype "won" the case

**Justification**:
- PSM requires binary outcome for ATT estimation
- 0.60 threshold represents clear dominance of sovereignty argumentation

---

## Missing Data

**Policy**: Complete case analysis  
**Missing Data**: None in current dataset (all 70 cases have complete data for all 8 variables)

---

## Data Quality Notes

### Synthetic Data Disclaimer
This dataset is **synthetic** and generated for methodological demonstration purposes. It is designed to:
- Preserve realistic distributional properties of international law cases
- Maintain plausible correlations between covariates
- Provide sufficient sample size for PSM analysis

### Real Data Replacement
For replication with real data:
1. Replace `sovereignty_synthetic_parsed.csv` with real case data
2. Ensure all 8 variables are coded following the protocols above
3. Maintain the same column names and data types
4. Update `DATA_COLLECTION_PROTOCOL.md` with your data sources

---

## Summary Statistics

| Variable | Type | N | Min | Max | Mean | SD |
|----------|------|---|-----|-----|------|-----|
| `Case_ID` | Categorical | 70 | - | - | - | - |
| `Country` | Categorical | 70 | - | - | - | - |
| `Year` | Integer | 70 | 2002 | 2023 | ~2012 | ~7 |
| `Crisis_Catalyzed` | Binary | 70 | 0 | 1 | 0.286 | 0.455 |
| `Sovereignty_Phenotype_Score` | Float | 70 | 0.0 | 1.0 | ~0.65 | ~0.15 |
| `IusSpace_Dim12` | Float | 70 | 0.0 | 10.0 | ~5.5 | ~2.0 |
| `Geographic_Region` | Categorical | 70 | - | - | - | - |
| `Legal_Family` | Categorical | 70 | - | - | - | - |

---

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{lerer2025sovereignty,
  author = {Lerer, Ignacio A.},
  title = {Sovereignty-Globalism Competition Dataset: 70 International Law Cases},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/adrianlerer/legal-evolution-unified}
}
```

---

## Contact

For questions about data coding or variable definitions:
- **Email**: [Insert contact email]
- **GitHub Issues**: [Repository URL]/issues

---

**Last Updated**: 2025-10-15  
**Version**: 1.0.0
