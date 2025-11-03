# Ontology Mapping: Regulatory Risk Framework
**Version**: 1.0 (2025-11-03)  
**Purpose**: Formal semantic alignment between IusMorfos, RootFinder, ICRG, Coface frameworks  
**Status**: Reference Document for Cross-Framework Integration

---

## I. SEMANTIC ALIGNMENT TABLE

### Complete Ontology Mapping

| IusMorfos Component | ICRG Variable | Coface Dimension | RRI Component | Overlap % | Directionality |
|---------------------|---------------|------------------|---------------|-----------|----------------|
| **Elite Cohesion Index (ECI)** | Government Stability | Political Stability | CVI (inverse) | 80% | ECI ↑ → Gov Stability ↑, CVI ↓ |
| **Electoral Dimension** | Democratic Accountability | Business Climate (indirect) | - | 90% | Electoral score → Democracy score |
| **Judicial Review Dimension** | Law and Order | Business Climate (legal system) | JIS | 70% | Judicial strength → Law score + JIS |
| **Procedural Dimension** | Bureaucracy Quality | Business Climate (institutions) | FS | 60% | High procedure → High bureaucracy + High FS |
| **Velocity Dimension** | Investment Profile (inverse) | Country Risk (instability) | V | 50% | High velocity → Low investment profile |
| **Economic Crisis Dimension** | Socioeconomic Conditions | Country Risk (macro) | - | 85% | Crisis severity → Socioeconomic score |
| **Legitimation Crisis** | Internal Conflict | Political Risk | - | 75% | Legitimation loss → Internal conflict risk |
| **Social Movements** | Internal Conflict | Political Risk | - | 80% | Movement intensity → Conflict risk |
| **External Shocks** | External Conflict | Country Risk (geopolitical) | - | 80% | Shock severity → External conflict |
| **Memetic Dimension** | Religious/Ethnic Tensions | Political Risk | RootFinder output | 65% | Memetic fragmentation → Tensions |
| **Teleology Dimension** | Corruption (inverse) | Business Climate (transparency) | - | 60% | Strong teleology → Low corruption |
| **Text/Doctrine Dimension** | Law and Order (Law component) | Business Climate (legal certainty) | RCI | 70% | Doctrinal stability → Legal order + RCI |

---

## II. ICRG 22-VARIABLE DECOMPOSITION

### Political Risk Components (12 variables, 100 points)

| ICRG Variable | Max Points | IusMorfos Source | Coface Equivalent | RRI Contribution |
|---------------|------------|------------------|-------------------|------------------|
| **Government Stability** | 12 | Elite Cohesion Index (ECI × 12) | Political Stability | Indirect via CVI |
| **Socioeconomic Conditions** | 12 | Economic Crisis (8) + Legitimation Crisis (4) | Country Risk (macro) | - |
| **Investment Profile** | 12 | 12 - (Velocity × 2) | Country Risk (business confidence) | Indirect via V |
| **Internal Conflict** | 12 | Social Movements (6) + Legitimation Crisis (6) | Political Risk | - |
| **External Conflict** | 12 | External Shocks (scale 0-12) | Country Risk (geopolitical) | - |
| **Corruption** | 6 | 6 - (6 × (1 - ECI)) | Business Climate (governance) | - |
| **Military in Politics** | 6 | ECI military component × 6 | Political Risk | - |
| **Religious Tensions** | 6 | Memetic Dimension × 0.5 | Political Risk | Indirect via RootFinder |
| **Law and Order** | 6 | min(6, (FS / 2) + 3) | Business Climate (legal system) | Direct via FS + JIS |
| **Ethnic Tensions** | 6 | Memetic Dimension × 0.5 | Political Risk | Indirect via RootFinder |
| **Democratic Accountability** | 6 | Electoral Dimension (scale 0-6) | Business Climate (governance) | - |
| **Bureaucracy Quality** | 4 | min(4, FS × 2) | Business Climate (institutions) | Direct via FS |

**Total Political Risk (PR)**: Sum of above (0-100 scale)

---

### Economic Risk Components (5 variables, 50 points)

| ICRG Variable | Max Points | Data Source | IusMorfos Link | Formula |
|---------------|------------|-------------|----------------|---------|
| **GDP per Head** | 5 | World Bank | Economic Crisis (indirect) | Table lookup (% of ICRG avg) |
| **Real GDP Growth** | 10 | IMF WEO | Economic Crisis (inverse) | Table lookup (-6% to +6%) |
| **Annual Inflation** | 10 | IMF WEO | Economic Crisis | Table lookup (<2% to 130%+) |
| **Budget Balance % GDP** | 10 | IMF WEO | Economic Crisis | Table lookup (+4% to -30%) |
| **Current Account % GDP** | 15 | IMF WEO | External Shocks | Table lookup (+10% to -40%) |

**Total Economic Risk (ER)**: Sum of above (0-50 scale)

---

### Financial Risk Components (5 variables, 50 points)

| ICRG Variable | Max Points | Data Source | IusMorfos Link | Formula |
|---------------|------------|-------------|----------------|---------|
| **Foreign Debt % GDP** | 10 | World Bank | Economic Crisis | Table lookup (0% to 200%+) |
| **Debt Service % Exports** | 10 | World Bank | Economic Crisis | Table lookup (0% to 85%+) |
| **Current Account % Exports** | 15 | IMF WEO | External Shocks | Table lookup (+25% to -120%) |
| **Net Int'l Liquidity (months)** | 5 | IMF IFS | External Shocks | Table lookup (15+ to <0.5 months) |
| **Exchange Rate Stability** | 10 | IMF IFS | Economic Crisis | Table lookup (-0.1% to -100%) |

**Total Financial Risk (FR)**: Sum of above (0-50 scale)

---

## III. COFACE DIMENSIONS DECOMPOSITION

### Country Risk Assessment (A1 → E scale)

| Coface Dimension | IusMorfos Source | ICRG Equivalent | Weight in Assessment |
|------------------|------------------|-----------------|---------------------|
| **Macroeconomic Outlook** | Economic Crisis | Economic Risk (ER) | 30% |
| **Financial Outlook** | Economic Crisis + External Shocks | Financial Risk (FR) | 25% |
| **Political Stability** | Elite Cohesion + Electoral + Legitimation | Government Stability + Internal Conflict | 25% |
| **Sovereign Risk** | Economic Crisis + External Shocks | Financial Risk (debt ratios) | 10% |
| **Climate/Environmental Risk** | External Shocks (climate component) | (Not in ICRG) | 10% |

**Mapping Formula**:
```python
def coface_grade_from_iusmorfos(country, year):
    # Calculate ICRG composite
    PR = calculate_political_risk(country, year)  # 0-100
    ER = calculate_economic_risk(country, year)   # 0-50
    FR = calculate_financial_risk(country, year)  # 0-50
    CPFER = 0.5 * (PR + ER + FR)  # 0-100
    
    # Map to Coface scale
    if CPFER >= 90:
        return 'A1'
    elif CPFER >= 80:
        return 'A2'
    elif CPFER >= 70:
        return 'A3'
    elif CPFER >= 60:
        return 'A4'
    elif CPFER >= 50:
        return 'B'
    elif CPFER >= 40:
        return 'C'
    elif CPFER >= 30:
        return 'D'
    else:
        return 'E'
```

---

### Business Climate Assessment (A1 → E scale)

| Coface Criterion | IusMorfos Source | ICRG Equivalent | RRI Component |
|------------------|------------------|-----------------|---------------|
| **Company Reports Availability** | Procedural Dimension | Bureaucracy Quality | - |
| **Debt Collection Effectiveness** | Judicial Review + Procedural | Law and Order | JIS |
| **Institutional Quality** | Elite Cohesion + Procedural | Bureaucracy Quality + Corruption | FS |
| **Market Openness** | Procedural + Economic Crisis | Investment Profile | - |

**Mapping Formula**:
```python
def business_climate_from_iusmorfos(country, year):
    procedural = get_procedural_score(country, year)  # 0-10
    judicial = get_judicial_review_score(country, year)  # 0-10
    eci = get_elite_cohesion_index(country, year)  # 0-1
    
    # Weighted composite
    bc_score = (procedural * 0.25 +
                judicial * 0.30 +
                eci * 10 * 0.25 +
                (10 - economic_crisis) * 0.20)
    
    # Map to Coface scale (similar to country risk)
    if bc_score >= 9.0:
        return 'A1'
    elif bc_score >= 8.0:
        return 'A2'
    # ... (same thresholds)
```

---

## IV. RRI COMPONENT DECOMPOSITION

### Regulatory Risk Index Formula

```python
RRI = (1 - CVI) × 0.25 +          # Capture Vulnerability Index
      (FS / 2.5) × 0.25 +          # Friction Score (capped at 2.5)
      (1 - V/5) × 0.20 +           # Constitutional Velocity (capped at 5)
      (JIS / 10) × 0.20 +          # Judicial Independence Score
      RCI × 0.10                   # Regulatory Consistency Index
```

#### Component Breakdown

| RRI Component | Formula | IusMorfos Source | ICRG Equivalent | Data Source |
|---------------|---------|------------------|-----------------|-------------|
| **CVI** | (Years >67% Senate / Total) × (Avg Tenure / 30) | Elite Cohesion (electoral component) | Democratic Accountability (inverse) | V-Dem + national electoral data |
| **Friction Score (FS)** | (Veto Points) × (Activation Cost) × (Reversal Difficulty) | Procedural Dimension | Bureaucracy Quality + Law and Order | Constitutional texts + case law |
| **Velocity (V)** | (Overrulings + New Doctrines) / Years | Velocity Dimension | Investment Profile (inverse) | RootFinder + judicial databases |
| **JIS** | (Tenure × 0.3) + (Appointment × 0.25) + (Budget × 0.2) + (Removal × 0.25) | Judicial Review Dimension | Law and Order (Law component) | Venice Commission + national constitutions |
| **RCI** | 1 - (σ_enforcement / μ_enforcement) | Text/Doctrine Dimension | Law and Order (Order component) | OECD Regulatory DB + national agencies |

---

## V. DIRECTIONALITY & CAUSALITY

### Causal Pathways

```
Elite Cohesion Index (ECI) → Government Stability → Country Risk Grade
         ↓                           ↓                      ↓
    Low CVI (0.15)           High PR (84)            Coface A1
    
    vs.
    
Elite Cohesion Index (ECI) → Government Stability → Country Risk Grade
         ↓                           ↓                      ↓
    High CVI (0.81)          Moderate PR (64)         Coface A3/A4
```

### Feedback Loops

1. **Negative Feedback (Stabilizing)**:
   - High FS → Low Velocity → High Investment Profile → High ECI → High FS
   - **Example**: Germany (FS=2.01, V=0.8, ECI=0.94)

2. **Positive Feedback (Destabilizing)**:
   - Low FS → High Velocity → Low Investment Profile → Low ECI → Lower FS
   - **Example**: Hungary (FS=0.05, V=2.8, ECI=0.45)

3. **Tipping Point**:
   - **Threshold**: FS < 1.0 AND ECI < 0.75 → Capture likely within 24 months
   - **Example**: USA 2024 (FS=0.08, ECI=0.86) → ECI buffer prevents immediate capture

---

## VI. OPERATIONALIZATION HIERARCHY

### Level 1: Data Collection (Raw Inputs)

```
├── V-Dem Dataset (Electoral, Democracy, Governance)
├── IMF WEO (GDP, Inflation, Debt)
├── World Bank (Debt ratios, Reserves)
├── ICRG Subscription (if available) OR Replicate using methodology
├── Coface Website (Country/Business Climate grades - scrape quarterly)
├── Constitutional Texts (Veto points, Supermajority rules)
├── Judicial Databases (Overrulings, Citations)
├── OECD Regulatory Indicators (Enforcement consistency)
└── Venice Commission Opinions (Judicial independence)
```

### Level 2: Intermediate Calculations (Framework Components)

```python
# IusMorfos 12D Scores (0-10 scale)
teleology = calculate_teleology(country, year)
procedural = calculate_procedural(country, year)
memetic = calculate_memetic(country, year)
velocity = calculate_velocity(country, year)
electoral = calculate_electoral(country, year)
social_movements = calculate_social_movements(country, year)
economic_crisis = calculate_economic_crisis(country, year)
elite_cohesion = calculate_elite_cohesion(country, year)
judicial_review = calculate_judicial_review(country, year)
text_doctrine = calculate_text_doctrine(country, year)
legitimation_crisis = calculate_legitimation_crisis(country, year)
external_shocks = calculate_external_shocks(country, year)

# ICRG Components (various scales)
PR = map_iusmorfos_to_political_risk(iusmorfos_scores)  # 0-100
ER = calculate_economic_risk(imf_data)  # 0-50
FR = calculate_financial_risk(wb_data)  # 0-50
CPFER = 0.5 * (PR + ER + FR)  # 0-100

# RRI Components (various scales)
CVI = calculate_capture_vulnerability(electoral_data, tenure_data)  # 0-1
FS = calculate_friction_score(constitutional_text, veto_data)  # 0-3
V = calculate_velocity(judicial_database)  # 0-10
JIS = calculate_judicial_independence(venice_data, constitutional_text)  # 0-10
RCI = calculate_regulatory_consistency(oecd_data, enforcement_data)  # 0-1
RRI = composite_rri(CVI, FS, V, JIS, RCI)  # 0-1
```

### Level 3: High-Level Outputs (Risk Grades)

```python
# ICRG Grade
if CPFER >= 80:
    icrg_grade = "Very Low Risk"
elif CPFER >= 70:
    icrg_grade = "Low Risk"
elif CPFER >= 60:
    icrg_grade = "Moderate Risk"
elif CPFER >= 50:
    icrg_grade = "High Risk"
else:
    icrg_grade = "Very High Risk"

# Coface Grade
coface_country = map_cpfer_to_coface(CPFER)  # A1-E
coface_business = map_iusmorfos_to_business_climate(procedural, judicial, eci)  # A1-E

# RRI Augmented Grade
augmented_pr = PR + (RRI * 15) - 15  # Adjust Political Risk by RRI
augmented_cpfer = 0.5 * (augmented_pr + ER + FR)
augmented_grade = map_cpfer_to_icrg_grade(augmented_cpfer)

# Final Output
return {
    'country': country,
    'year': year,
    'icrg_standard': {
        'composite': CPFER,
        'grade': icrg_grade,
        'political_risk': PR,
        'economic_risk': ER,
        'financial_risk': FR
    },
    'coface': {
        'country_risk': coface_country,
        'business_climate': coface_business
    },
    'rri': {
        'index': RRI,
        'cvi': CVI,
        'friction_score': FS,
        'velocity': V,
        'jis': JIS,
        'rci': RCI
    },
    'augmented': {
        'composite': augmented_cpfer,
        'grade': augmented_grade,
        'adjustment': augmented_cpfer - CPFER
    }
}
```

---

## VII. INTEGRATION BEST PRACTICES

### Rule 1: Preserve Semantic Independence

**DO**:
```python
# Keep RRI as separate module with clear interfaces
from src.analysis.regulatory_risk import RegulatoryRiskModule
rri_module = RegulatoryRiskModule()
rri_score = rri_module.calculate(country, year)
```

**DON'T**:
```python
# Don't hardcode RRI logic into IusMorfos classes
class IusMorfosCalculator:
    def calculate_all(self):
        # ... IusMorfos logic ...
        rri = (1 - cvi) * 0.25 + ...  # ❌ Wrong - breaks modularity
```

### Rule 2: Use Bridge Pattern for Cross-Framework Queries

```python
class RiskFrameworkBridge:
    """
    Mediator pattern for cross-framework queries
    """
    def __init__(self):
        self.iusmorfos = IusMorfosCalculator()
        self.icrg = ICRGCalculator()
        self.coface = CofaceMapper()
        self.rri = RegulatoryRiskModule()
    
    def get_unified_risk_profile(self, country: str, year: int) -> dict:
        """
        Single point of access for all frameworks
        """
        return {
            'iusmorfos_12d': self.iusmorfos.calculate_all(country, year),
            'icrg': self.icrg.calculate_composite(country, year),
            'coface': self.coface.get_grades(country, year),
            'rri': self.rri.calculate_rri(country, year)
        }
```

### Rule 3: Explicit Mapping Tables

Store all mappings in config files, not code:

```yaml
# config/framework_mappings.yaml
iusmorfos_to_icrg:
  elite_cohesion:
    target: government_stability
    weight: 1.0
    scale: 12
    formula: "ECI * 12"
  
  velocity:
    target: investment_profile
    weight: -2.0
    scale: 12
    formula: "12 - (V * 2)"
```

### Rule 4: Versioning & Backwards Compatibility

```python
class ICRGCalculator:
    def __init__(self, version: str = '2024'):
        """
        Support multiple ICRG methodology versions
        """
        if version == '2024':
            self.weights = {'political': 0.50, 'economic': 0.25, 'financial': 0.25}
        elif version == '2019':
            self.weights = {'political': 0.50, 'economic': 0.30, 'financial': 0.20}
```

---

## VIII. VALIDATION CHECKLIST

### Pre-Implementation Validation

- [x] All 22 ICRG variables mapped to data sources
- [x] All 12 IusMorfos dimensions have clear formulas
- [x] RRI components validated against 5 test cases (Germany, USA, Hungary, Turkey, Poland)
- [x] Coface scale thresholds documented
- [ ] Edge cases handled (missing data, historical gaps)
- [ ] Unit tests cover all mapping functions

### Post-Implementation Validation

- [ ] MAE < 1.5 for ICRG replication (vs. official ICRG scores if available)
- [ ] Coface grade matches official Coface website for 10 sample countries
- [ ] RRI predicts 6 historical crises with 80%+ accuracy
- [ ] Cross-framework consistency: High ICRG PR → Low Coface risk → High RRI

---

## IX. EXAMPLE: USA 2024 COMPLETE CALCULATION

### Step 1: IusMorfos 12D Input (Hypothetical)

```python
usa_2024_iusmorfos = {
    'teleology': 6.5,
    'procedural': 7.2,
    'memetic': 5.8,
    'velocity': 6.4,  # Note: This is IusMorfos velocity (0-10), not RRI velocity (overrulings/year)
    'electoral': 8.1,
    'social_movements': 5.2,
    'economic_crisis': 6.9,
    'elite_cohesion': 7.8,  # ECI = 0.78 (normalized to 0-10 scale = 7.8)
    'judicial_review': 7.5,
    'text_doctrine': 6.2,
    'legitimation_crisis': 5.5,
    'external_shocks': 4.8
}
```

### Step 2: ICRG Political Risk Calculation

```python
# Government Stability (12 points)
gov_stability = (7.8 / 10) * 12 = 9.36

# Democratic Accountability (6 points)
dem_accountability = (8.1 / 10) * 6 = 4.86

# Law and Order (6 points) - Using Friction Score
# FS = 0.08 (from Prakash & Sunstein analysis)
law_order = min(6, (0.08 / 2) + 3) = 3.04

# Bureaucracy Quality (4 points)
bureaucracy = min(4, 0.08 * 2) = 0.16

# Corruption (6 points)
corruption = 6 - (6 * (1 - 0.78)) = 4.68

# Investment Profile (12 points) - Using IusMorfos velocity
investment = 12 - (6.4 * 2) = -0.8  # Capped at 0 → 0

# Socioeconomic (12 points)
socioeconomic = ((10 - 6.9) / 10) * 6 + ((10 - 5.5) / 10) * 6 = 1.86 + 2.7 = 4.56

# Internal Conflict (12 points)
internal = ((10 - 5.2) / 10) * 6 + ((10 - 5.5) / 10) * 6 = 2.88 + 2.7 = 5.58

# External Conflict (12 points)
external = ((10 - 4.8) / 10) * 12 = 6.24

# Ethnic/Religious Tensions (12 points total)
ethnic_religious = (5.8 / 10) * 12 = 6.96

# Military in Politics (6 points) - Assume minimal
military = 5.0

# TOTAL PR
PR = 9.36 + 4.86 + 3.04 + 0.16 + 4.68 + 0 + 4.56 + 5.58 + 6.24 + 6.96 + 5.0
PR = 50.44 / 100  # This is MUCH lower than expected 72.5

# Issue: Need better calibration or use actual ICRG components
```

**Note**: This demonstrates the need for:
1. More sophisticated mapping functions (not just linear scaling)
2. Validation against actual ICRG scores
3. Adjustment factors based on empirical data

### Step 3: RRI Calculation

```python
# CVI (Capture Vulnerability Index)
cvi = 0.81  # From existing analysis

# Friction Score
fs = 0.08  # From Prakash & Sunstein analysis

# Velocity (Constitutional)
v = 3.4  # Overrulings per year (from RootFinder)

# Judicial Independence Score
jis = 7.2  # From Venice Commission-style analysis

# Regulatory Consistency Index
rci = 0.75  # From OECD + national data

# RRI Composite
rri = (1 - 0.81) * 0.25 + (0.08 / 2.5) * 0.25 + (1 - 3.4/5) * 0.20 + (7.2 / 10) * 0.20 + 0.75 * 0.10
rri = 0.0475 + 0.008 + 0.064 + 0.144 + 0.075
rri = 0.3385

# RRI Score (0-15 scale for ICRG integration)
rri_score = 0.3385 * 15 = 5.08
```

### Step 4: Augmented Assessment

```python
# Assuming we use actual ICRG PR = 72.5 (from design doc)
augmented_pr = 72.5 + 5.08 - 15 = 62.58

# Composite (assuming ER=38.2, FR=42.1 from design doc)
augmented_cpfer = 0.5 * (62.58 + 38.2 + 42.1) = 71.44

# Grade
# 71.44 → Low Risk (70-79.9 range)
```

**Interpretation**: 
- Standard ICRG: 76.4 (Low Risk)
- Augmented: 71.4 (Low Risk but near Moderate boundary)
- Adjustment: -5.0 points (regulatory risk penalty)

---

## X. NEXT STEPS FOR IMPLEMENTATION

### Phase 1: Validation (Week 1)
1. Collect actual ICRG scores for 10 countries (2024)
2. Replicate ICRG methodology and compare (target: MAE < 2.0)
3. Adjust mapping functions based on residuals
4. Document calibration decisions

### Phase 2: Modularization (Week 2)
1. Create `src/analysis/framework_bridge.py`
2. Implement `RiskFrameworkBridge` class
3. Write unit tests for all mapping functions
4. Create config file `config/framework_mappings.yaml`

### Phase 3: API Integration (Week 3-4)
1. Build REST endpoints using bridge pattern
2. Add caching layer for expensive calculations
3. Implement versioning system
4. Create Swagger/OpenAPI documentation

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-03  
**Status**: ✅ Reference Document Complete  
**Next**: Implement RiskFrameworkBridge class
