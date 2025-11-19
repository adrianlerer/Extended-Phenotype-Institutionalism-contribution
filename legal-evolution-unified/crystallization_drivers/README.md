# Crystallization Drivers Framework

## Executive Summary

This project decomposes the **Constitutional Lock-in Index (CLI)** into 5 independent causal drivers that explain institutional irreversibility, operationalizes them quantitatively, and builds a predictive model validated against 10 institutional cases.

**Model Performance**: MAE = 0.1599 (acceptable, target < 0.20)

**Reference**: Lerer (2024), "Constitutional Lock-in Index" (SSRN 5402461)

---

## 🎯 The Five Crystallization Drivers

### 1. Economic Self-Reinforcement Index (ESRI)
**Formula**: `(rent_capture × automaticity × independence)^(1/3)`

Measures automatic economic rents captured by organized beneficiaries independent of political coalitions.

**Components**:
- Rent capture percentage (% of economic flow)
- Automaticity of operation (0-1 scale)
- Independence from party politics (0-1 scale)

### 2. Premature Constitutionalization Index (PCI)
**Formula**: `(constitutional_level / log10(years_before_const + 1)) × judicial_entrenchment`

Measures artificial rigidity from constitutionalizing institutions before social maturation.

**Components**:
- Constitutional level (0=ordinary law, 0.5=constitutional, 1.0=core)
- Years of pre-constitutional maturation
- Judicial entrenchment degree (0-1 scale)

### 3. Reversal Cost Asymmetry (RCA)
**Formula**: `normalize(log10(diffuse / concentrated)) × (1 - visibility)`

Measures asymmetry between concentrated beneficiaries and diffuse cost bearers.

**Components**:
- Number of concentrated beneficiaries
- Number of diffuse cost bearers
- Visibility of costs (0=invisible, 1=highly visible)

### 4. Veto Player Fragmentation Index (VPFI)
**Formula**: `(n_veto_players × lack_coordination) / (1 - sunset + 0.1)`

Measures gridlock from fragmented veto players and coordination failure.

**Components**:
- Number of institutional veto players
- Degree of coordination failure (0-1 scale)
- Presence of sunset mechanism (0-1 scale, inverted)

### 5. Existential Identity Linkage Index (EILI)
**Formula**: `(founding_docs × electoral_dependence × survival_necessity)^(1/3)`

Measures ontological necessity for political coalition survival.

**Components**:
- Prominence in founding documents (0-1 scale)
- Electoral dependence of coalition (0-1 scale)
- Survival necessity for memeplex (0-1 scale)

---

## 📊 CLI Prediction Model

### Formula (Calibrated v3)
```
economic_base = 0.30 × ESRI + 0.10 × PCI + 0.10 × RCA
political_base = 0.25 × VPFI + 0.30 × EILI
interaction_boost = 0.10 × (VPFI × EILI)

CLI = economic_base + political_base + interaction_boost
```

### Theoretical Rationale
- **Economic drivers** (ESRI, PCI, RCA): 50% total weight
  - Rent-seeking, premature constitutionalization, cost asymmetry
- **Political drivers** (VPFI, EILI): 55% total weight
  - Veto player gridlock, existential identity linkage
- **Interaction term**: Sacred institutions + fragmented veto players = extreme lock-in

---

## 📁 Project Structure

```
crystallization_drivers/
├── data/
│   ├── driver_components.csv          # Raw components for 10 cases
│   ├── crystallization_drivers.csv    # Calculated driver indices
│   └── validation_cases.csv           # Train/test/validation split
├── scripts/
│   ├── calculate_drivers.py           # CrystallizationDrivers class
│   ├── visualize_drivers.py           # 4 plotting functions
│   └── validate_model.py              # ModelValidator class
├── visualizations/
│   ├── driver_radar_comparison.png    # Radar chart (300 DPI)
│   ├── driver_correlation_heatmap.png # Correlation matrix
│   ├── prediction_accuracy_scatter.png# Predicted vs observed
│   ├── pathway_distribution.png       # Distribution by pathway
│   └── sensitivity_analysis.png       # Driver sensitivity plots
├── analysis/
│   └── crystallization_analysis.ipynb # Jupyter notebook analysis
├── docs/
│   ├── driver_operationalization.md   # Methodology details
│   ├── data_sources.md                # Complete references
│   └── validation_report.txt          # Statistical validation
└── README.md                          # This file
```

---

## 🚀 Quick Start

### 1. Calculate Drivers
```bash
python3 scripts/calculate_drivers.py
```

**Output**: `data/crystallization_drivers.csv` with predicted CLI values

### 2. Generate Visualizations
```bash
python3 scripts/visualize_drivers.py
```

**Output**: 4 PNG files in `visualizations/` directory (300 DPI)

### 3. Validate Model
```bash
python3 scripts/validate_model.py
```

**Output**: 
- `visualizations/sensitivity_analysis.png`
- `docs/validation_report.txt`

### 4. Explore Analysis
```bash
jupyter notebook analysis/crystallization_analysis.ipynb
```

---

## 📈 Model Performance

### Formula-Based Model (Theoretical)
- **MAE**: 0.1599 ✓ (target < 0.20)
- **RMSE**: 0.1906
- **R²**: 0.3527
- **Max Error**: 0.3244 (CHL_001 failed case)
- **Median Error**: 0.1654

### Linear Regression Benchmark (ML)
- **MAE**: 0.0502 (training set)
- **Cross-validation MAE**: 0.2537 ± 0.1647
- **R²**: 0.9256 (overfitting with n=10)

**Conclusion**: Theoretical formula achieves acceptable performance with better generalizability than ML benchmark (cross-validation evidence).

---

## 🔍 Key Findings

### Driver Influence (Sensitivity Analysis)
1. **EILI** (Identity): Elasticity = 0.2332 (most influential)
2. **ESRI** (Economic): Elasticity = 0.1678
3. **VPFI** (Veto Players): Elasticity = 0.1520
4. **RCA** (Cost Asymmetry): Elasticity = 0.0257
5. **PCI** (Premature Const.): Elasticity = 0.0066

**Interpretation**: Existential identity linkage is the strongest predictor of crystallization, followed by economic self-reinforcement and veto player fragmentation.

### Pathway Classification
- **Political pathway**: 7 cases (ARG_001, ARG_002, USA_002, CHL_001, CHL_002, BRA_001, FRA_001)
- **Hybrid pathway**: 3 cases (USA_001, USA_003, ESP_001)
- **Economic pathway**: 0 cases (none observed in current dataset)

**Interpretation**: Most crystallization occurs via political-identity mechanisms rather than pure economic rent-seeking.

---

## 📚 Institutional Cases

### Crystallized Cases (CLI > 0.70)
1. **USA_002**: Social Security (CLI = 0.94) - "Third rail politics"
2. **BRA_001**: CLT labor code (CLI = 0.89) - 45-year maturation
3. **ARG_001**: Ultraactividad Sindical (CLI = 0.87) - Union power
4. **ARG_002**: Coparticipación Federal (CLI = 0.82) - 24 veto players
5. **CHL_002**: AFP pension system (CLI = 0.76) - Survived 2019 protests

### Contested Cases (0.40 < CLI < 0.70)
6. **USA_003**: Chevron Doctrine (CLI = 0.68) - Reversed 2024
7. **ESP_001**: Estatuto Trabajadores (CLI = 0.58) - Reformed multiple times
8. **FRA_001**: 35-hour workweek (CLI = 0.52) - Weakened 2017
9. **USA_001**: Affordable Care Act (CLI = 0.48) - Repeatedly challenged

### Failed Case (CLI < 0.20)
10. **CHL_001**: Chile Constitution 2022 (CLI = 0.12) - Rejected 62%

---

## 🛠️ Dependencies

```python
pandas >= 1.5.0
numpy >= 1.23.0
matplotlib >= 3.6.0
seaborn >= 0.12.0
scikit-learn >= 1.2.0
scipy >= 1.9.0
jupyter >= 1.0.0
```

Install: `pip install -r requirements.txt`

---

## 📖 Documentation

- **Methodology**: `docs/driver_operationalization.md`
- **Data Sources**: `docs/data_sources.md`
- **Validation Report**: `docs/validation_report.txt`
- **Analysis Notebook**: `analysis/crystallization_analysis.ipynb`

---

## 🔬 Theoretical Foundation

### Extended Phenotype Theory
Institutions as self-replicating memeplexes (Dawkins 1982):
- Institutions = vehicles for memeplex replication
- Crystallization = evolutionary fitness optimization
- Lock-in = institutional phenotype survival mechanisms

### Path Dependency Literature
- **Pierson (2000)**: Increasing returns and political institutions
- **Mahoney & Thelen (2010)**: Institutional change theory
- **Tsebelis (2002)**: Veto players and policy stability

### Rent-Seeking Theory
- **Olson (1965)**: Logic of collective action
- **Stigler (1971)**: Theory of economic regulation
- **Tullock (1967)**: Welfare costs of tariffs, monopolies

---

## 🎓 Citation

If you use this framework in your research, please cite:

```bibtex
@techreport{lerer2024cli,
  title={Constitutional Lock-in Index: Quantifying Institutional Irreversibility},
  author={Lerer, Daniel},
  year={2024},
  institution={SSRN},
  number={5402461}
}
```

---

## 📧 Contact

**Author**: GenSpark AI Developer  
**Version**: 1.0.0  
**Date**: 2025-11-04  
**License**: MIT

---

## 🚧 Future Work

### Phase 2: Integration with legal-evolution-unified
- Merge into main repository
- Update unified documentation
- Create API endpoints for CLI prediction
- Integrate with existing comparative law database

### Expansion Opportunities
- Increase sample size (target N ≥ 30)
- Add machine learning models (Random Forest, XGBoost)
- Implement fuzzy-set QCA for causal pathways
- Develop time-series analysis for temporal decay
- Create interactive web dashboard

---

## ⚖️ License

MIT License - See LICENSE file for details
