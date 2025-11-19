# Replication Guide: PSM Analysis of Crisis Catalysis Hypothesis

## 🎯 Overview

This guide provides step-by-step instructions to **fully replicate** the Propensity Score Matching (PSM) analysis testing whether crisis events causally increase sovereignty-oriented outcomes in international law cases.

**Estimated Time**: 30-60 minutes (depending on computational resources)

---

## 📋 Prerequisites

### Required Software
- **Python**: Version 3.9 or higher
- **pip**: Python package manager
- **Git**: For cloning repository (optional)

### System Requirements
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Storage**: 500 MB free space
- **OS**: Linux, macOS, or Windows with WSL

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Run Automated Script

```bash
# 1. Clone repository
git clone https://github.com/adrianlerer/legal-evolution-unified.git
cd legal-evolution-unified

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run complete PSM analysis
python scripts/replicate_psm_analysis.py
```

**Output**: Results will be saved to `results/replication/` directory with:
- Statistical reports (Markdown)
- Diagnostic plots (PNG)
- Data files (CSV)

### Option 2: Use Jupyter Notebook

```bash
# After steps 1-3 above:
jupyter lab

# Open: notebooks/PSM_Replication.ipynb
# Run all cells
```

---

## 📖 Detailed Step-by-Step Instructions

### Step 1: Environment Setup

#### 1.1 Install Python 3.9+

**Linux/macOS**:
```bash
python3 --version  # Check if already installed
```

**Windows**:
Download from [python.org](https://www.python.org/downloads/)

#### 1.2 Create Virtual Environment

```bash
# Navigate to project directory
cd legal-evolution-unified

# Create isolated environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

**Verification**:
```bash
which python  # Should show path to venv/bin/python
```

#### 1.3 Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E 'pandas|numpy|scikit-learn|matplotlib|statsmodels'
```

**Expected Output**:
```
numpy             1.24.3
pandas            2.0.3
scikit-learn      1.3.0
matplotlib        3.7.2
statsmodels       0.14.0
```

---

### Step 2: Data Verification

#### 2.1 Locate Dataset

```bash
# Check data file exists
ls -lh data/sovereignty_synthetic_parsed.csv

# Expected: ~6 KB file with 70 cases
```

#### 2.2 Inspect Data

```bash
# View first 5 rows
head -n 6 data/sovereignty_synthetic_parsed.csv

# Count rows (should be 71: 70 cases + 1 header)
wc -l data/sovereignty_synthetic_parsed.csv
```

#### 2.3 Validate Data Structure

```python
import pandas as pd

# Load data
df = pd.read_csv('data/sovereignty_synthetic_parsed.csv')

# Check dimensions
print(f"Shape: {df.shape}")  # Expected: (70, 8)

# Check columns
required_cols = [
    'Case_ID', 'Country', 'Year', 'Crisis_Catalyzed',
    'Sovereignty_Phenotype_Score', 'IusSpace_Dim12',
    'Geographic_Region', 'Legal_Family'
]
assert all(col in df.columns for col in required_cols), "Missing columns!"

print("✓ Data structure validated")
```

---

### Step 3: Run PSM Analysis

#### 3.1 Option A: Automated Script

```bash
# Run complete analysis pipeline
python scripts/replicate_psm_analysis.py

# Monitor progress (script prints status updates)
```

**What This Does**:
1. Loads data from CSV
2. Creates binary outcome variable (`Sovereignty_Win`)
3. Estimates propensity scores (logistic regression)
4. Performs k-NN matching with caliper
5. Checks covariate balance (SMD)
6. Estimates Average Treatment Effect on Treated (ATT)
7. Conducts Rosenbaum sensitivity analysis
8. Generates diagnostic plots
9. Writes academic-style report

**Expected Runtime**: 2-5 minutes

#### 3.2 Option B: Step-by-Step Python

```python
import pandas as pd
from src.causal_inference.psm import run_complete_psm

# Load data
df = pd.read_csv('data/sovereignty_synthetic_parsed.csv')

# Create binary outcome
df['Sovereignty_Win'] = (df['Sovereignty_Phenotype_Score'] > 0.60).astype(int)

# Define analysis parameters
results = run_complete_psm(
    df=df,
    treatment_var='Crisis_Catalyzed',
    outcome_var='Sovereignty_Win',
    covariates=[
        'Sovereignty_Phenotype_Score',
        'IusSpace_Dim12',
        'Year',
        'Geographic_Region',
        'Legal_Family'
    ],
    n_neighbors=2,
    caliper=0.1,
    bootstrap_n=1000,
    output_dir='results/replication/'
)

# Print ATT estimate
print(f"ATT: {results['att']['estimate']:.4f}")
print(f"95% CI: [{results['att']['ci_lower']:.4f}, {results['att']['ci_upper']:.4f}]")
print(f"p-value: {results['att']['p']:.4f}")
```

**Expected Output**:
```
ATT: +0.0040
95% CI: [-0.3077, +0.1538]
p-value: 0.9756
```

---

### Step 4: Verify Results

#### 4.1 Check Key Diagnostics

**Common Support (Target: ≥70%)**:
```python
overlap_pct = results['common_support']['overlap_percentage']
print(f"Common Support: {overlap_pct:.1%}")  # Expected: ~82.9%

assert overlap_pct >= 0.70, "Insufficient overlap!"
print("✓ Common support PASS")
```

**Covariate Balance (Target: SMD <0.10)**:
```python
balance = results['balance']
imbalanced = balance[balance['SMD_After'] > 0.10]
print(f"Imbalanced covariates: {len(imbalanced)}/{len(balance)}")

# Note: Some imbalance expected due to structural differences
```

**Sensitivity Analysis (Target: Γ ≥1.5)**:
```python
sensitivity = results['sensitivity']
robust_gamma = sensitivity[sensitivity['P_Upper'] > 0.05]['Gamma'].max()
print(f"Robust to Γ = {robust_gamma}")  # Expected: ~1.5
```

#### 4.2 Compare to Published Results

**Reference Values** (from original analysis):

| Metric | Expected Value | Your Result |
|--------|---------------|-------------|
| ATT Estimate | +0.0040 | _________ |
| p-value | 0.9756 | _________ |
| Common Support | 82.9% | _________ |
| Robust Γ | 1.5 | _________ |

**Tolerance**: Allow ±5% variation due to bootstrap randomness

#### 4.3 Inspect Visualizations

```bash
# Check output directory
ls -lh results/replication/

# Expected files:
# - psm_overlap.png (propensity score distribution)
# - balance_plot.png (covariate balance before/after)
# - att_estimate.png (treatment effect with CI)
# - outcome_comparison.png (treated vs control outcomes)
```

**Visual Checks**:
1. **psm_overlap.png**: Should show substantial overlap between treated/control distributions
2. **balance_plot.png**: Most covariates should have reduced SMD after matching
3. **att_estimate.png**: Confidence interval should include zero
4. **outcome_comparison.png**: Minimal difference between matched groups

---

### Step 5: Reproduce Academic Report

#### 5.1 Generate Full Report

```bash
# Run report generation
python scripts/replicate_psm_analysis.py --report-only

# Output: results/replication/PSM_REPLICATION_REPORT.md
```

#### 5.2 Compare Report Sections

**Required Sections**:
- [ ] Abstract (research question, methods, finding)
- [ ] Sample Description (N=70, treatment=20, control=50)
- [ ] Propensity Score Model (logistic regression specification)
- [ ] Common Support (overlap percentage ≥70%)
- [ ] Covariate Balance (SMD table)
- [ ] ATT Estimate (point estimate, SE, 95% CI, p-value)
- [ ] Sensitivity Analysis (Γ bounds table)
- [ ] Interpretation (H5 not supported)

#### 5.3 Export Results to LaTeX (Optional)

```python
# Convert markdown tables to LaTeX
from src.utils.export_utils import markdown_to_latex

markdown_to_latex(
    input_file='results/replication/PSM_REPLICATION_REPORT.md',
    output_file='results/replication/PSM_REPLICATION_REPORT.tex'
)
```

---

## 🔍 Troubleshooting

### Common Issues

#### Issue 1: Import Error

**Symptom**:
```
ModuleNotFoundError: No module named 'src.causal_inference'
```

**Solution**:
```bash
# Install package in development mode
pip install -e .

# Verify installation
python -c "from src.causal_inference import psm; print('✓ Import successful')"
```

#### Issue 2: Data Not Found

**Symptom**:
```
FileNotFoundError: data/sovereignty_synthetic_parsed.csv
```

**Solution**:
```bash
# Check current directory
pwd

# Should be in project root (legal-evolution-unified/)
# If not, navigate back:
cd /path/to/legal-evolution-unified
```

#### Issue 3: Poor Covariate Balance

**Symptom**: All covariates have SMD > 0.10 after matching

**Diagnosis**: 
- May indicate fundamental structural differences between treated/control
- Not necessarily a "bug" - reflects real heterogeneity

**Solutions**:
1. **Increase sample size**: Collect more cases (target N ≥ 100)
2. **Refine matching**: Try different caliper values (0.05, 0.15)
3. **Alternative methods**: Consider inverse propensity weighting (IPW) or regression adjustment

#### Issue 4: Bootstrap Takes Too Long

**Symptom**: Script hangs at ATT estimation

**Solution**:
```python
# Reduce bootstrap iterations for testing
results = run_complete_psm(
    df=df,
    treatment_var='Crisis_Catalyzed',
    outcome_var='Sovereignty_Win',
    covariates=[...],
    bootstrap_n=100  # Reduce from 1000 to 100
)
```

**Note**: Use `bootstrap_n=1000` for final publication-quality results

---

## 📊 Understanding Results

### Interpreting ATT = +0.0040

**Statistical Interpretation**:
- Crisis-catalyzed cases have 0.4 percentage point higher probability of sovereignty wins
- 95% CI includes zero → effect not statistically significant (p = 0.9756)
- **Conclusion**: Crisis events do NOT have a causal effect on sovereignty outcomes

**Theoretical Interpretation** (Extended Phenotype Framework):
- Environmental perturbations (crises) are insufficient to override structural niche architecture
- Sovereignty vs globalism fitness determined by:
  - Integration level (IusSpace_Dim12)
  - Legal tradition (Legal_Family)
  - Regional context (Geographic_Region)
  - Path-dependent institutional structures
- 2008 crisis is a **marker** of tectonic shifts, not a **cause** of sovereignty resurgence

**Implication**: Focus future research on structural determinants (niche architecture) rather than event-driven causality.

---

## 🔄 Robustness Checks

### Alternative Specifications

#### 1. Different Outcome Threshold

```python
# Try 0.55 and 0.65 thresholds
for threshold in [0.55, 0.60, 0.65]:
    df['Sovereignty_Win'] = (df['Sovereignty_Phenotype_Score'] > threshold).astype(int)
    results = run_complete_psm(df, ...)
    print(f"Threshold {threshold}: ATT = {results['att']['estimate']:.4f}")
```

#### 2. Different Matching Methods

```python
# Try different n_neighbors
for k in [1, 2, 3, 5]:
    results = run_complete_psm(df, ..., n_neighbors=k)
    print(f"k={k}: ATT = {results['att']['estimate']:.4f}")
```

#### 3. Subgroup Analysis

```python
# Analyze Europe only
df_europe = df[df['Geographic_Region'] == 'Europe']
results_europe = run_complete_psm(df_europe, ...)

# Analyze high integration only
df_high_int = df[df['IusSpace_Dim12'] >= 7.0]
results_high_int = run_complete_psm(df_high_int, ...)
```

---

## 📚 Additional Resources

### Documentation
- **Methodology**: [`docs/methodology/PSM_METHODOLOGY.md`](docs/methodology/PSM_METHODOLOGY.md)
- **Data Dictionary**: [`data/DATA_DICTIONARY.md`](data/DATA_DICTIONARY.md)
- **Data Collection Protocol**: [`data/DATA_COLLECTION_PROTOCOL.md`](data/DATA_COLLECTION_PROTOCOL.md)

### Code
- **Core PSM Functions**: [`src/causal_inference/psm.py`](src/causal_inference/psm.py)
- **Analysis Script**: [`src/analysis/psm_crisis_catalysis_analysis.py`](src/analysis/psm_crisis_catalysis_analysis.py)
- **Replication Script**: [`scripts/replicate_psm_analysis.py`](scripts/replicate_psm_analysis.py)

### References

**PSM Methodology**:
- Rosenbaum, P.R., & Rubin, D.B. (1983). "The Central Role of the Propensity Score in Observational Studies for Causal Effects". *Biometrika*, 70(1), 41-55.
- Austin, P.C. (2011). "An Introduction to Propensity Score Methods for Reducing the Effects of Confounding". *Multivariate Behavioral Research*, 46(3), 399-424.
- Stuart, E.A. (2010). "Matching Methods for Causal Inference". *Statistical Science*, 25(1), 1-21.

**Theoretical Framework**:
- Dawkins, R. (1982). *The Extended Phenotype*. Oxford University Press.
- Lerer, I.A. (2025). "Law as Extended Phenotype: An Evolutionary Framework for Legal Comparison" (SSRN).

---

## 🤝 Getting Help

### Support Channels
1. **GitHub Issues**: [Repository URL]/issues - Bug reports, feature requests
2. **Email**: [Insert contact email] - Methodological questions
3. **Discussion Forum**: [Link if available] - General questions

### Reporting Replication Failures

If you cannot reproduce results, please provide:
1. **System Information**: OS, Python version, package versions (`pip freeze`)
2. **Error Messages**: Full traceback
3. **Your Results**: ATT estimate, p-value, common support %
4. **Script Used**: Copy of your code

**Template**:
```markdown
## Replication Issue

**Expected ATT**: +0.0040  
**Your ATT**: _____  
**Expected p-value**: 0.9756  
**Your p-value**: _____

**System**:
- OS: Linux Ubuntu 20.04
- Python: 3.9.7
- pandas: 2.0.3

**Error Message** (if any):
```
[paste error here]
```
```

---

## ✅ Replication Checklist

Use this checklist to verify complete replication:

- [ ] **Environment Setup**
  - [ ] Python 3.9+ installed
  - [ ] Virtual environment created and activated
  - [ ] All dependencies installed from `requirements.txt`

- [ ] **Data Verification**
  - [ ] Dataset located at `data/sovereignty_synthetic_parsed.csv`
  - [ ] 70 cases (71 rows including header)
  - [ ] 8 columns present
  - [ ] No missing values

- [ ] **Analysis Execution**
  - [ ] PSM script runs without errors
  - [ ] ATT estimate matches reference (±5%)
  - [ ] p-value matches reference (±0.01)
  - [ ] Common support ≥70%

- [ ] **Diagnostics**
  - [ ] 4 plots generated
  - [ ] Balance table created
  - [ ] Sensitivity analysis table generated

- [ ] **Results Interpretation**
  - [ ] ATT not statistically significant
  - [ ] H5 (Crisis Catalysis) not supported
  - [ ] Structural factors dominate event-driven effects

- [ ] **Documentation**
  - [ ] Full report generated
  - [ ] Results saved to `results/replication/`
  - [ ] Version information recorded

**Date Replicated**: __________  
**Your Name**: __________  
**Any Deviations**: __________

---

## 📄 Citation

If you use this replication package, please cite:

```bibtex
@software{lerer2025psm_replication,
  author = {Lerer, Ignacio A.},
  title = {PSM Analysis Replication Package: Crisis Catalysis in International Law},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/adrianlerer/legal-evolution-unified}
}
```

---

**Last Updated**: 2025-10-15  
**Package Version**: 1.0.0  
**Estimated Replication Time**: 30-60 minutes

---

**Questions?** Open an issue or contact [Insert contact email]

**Happy Replicating!** 🚀📊
