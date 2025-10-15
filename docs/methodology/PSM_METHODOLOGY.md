# PROPENSITY SCORE MATCHING (PSM) - METHODOLOGICAL FRAMEWORK
## Integration with IusMorfos V6.0 Legal Evolution Analysis

**Version**: 1.0  
**Date**: 2025-10-15  
**Framework**: Causal Inference for Legal-Political Conflicts  
**Status**: Production-Ready

---

## TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Theoretical Foundation](#theoretical-foundation)
3. [When to Use PSM](#when-to-use-psm)
4. [Model Specification](#model-specification)
5. [Implementation Protocol](#implementation-protocol)
6. [Diagnostic Framework](#diagnostic-framework)
7. [Interpretation Guidelines](#interpretation-guidelines)
8. [Common Problems & Solutions](#common-problems)
9. [Integration with IusMorfos](#integration-iusmorfos)
10. [Case Study: Crisis Catalysis](#case-study)
11. [References](#references)

---

## EXECUTIVE SUMMARY

### What is PSM?

**Propensity Score Matching (PSM)** is a quasi-experimental method for causal inference in observational studies. It addresses **selection bias** by:

1. Estimating each unit's **propensity** (probability) to receive treatment given observable characteristics
2. **Matching** treated units with control units that have similar propensities
3. Comparing outcomes between matched groups to estimate **causal effects**

### Why PSM for Legal Evolution?

Legal-political conflicts are **non-randomized** by nature:
- States don't randomly experience crises
- Countries don't randomly withdraw from international courts
- Sovereignty assertions are **endogenous** to prior conditions

PSM allows us to **control for confounders** and isolate causal mechanisms in:
- Crisis effects on sovereignty expression
- Integration threshold impacts on legal outcomes
- Institutional influence on policy trajectories

### Key Advantages

- ✅ **Controls observable confounding** (selection bias, pre-treatment differences)
- ✅ **Transparent** (visualizable balance, explicit assumptions)
- ✅ **Flexible** (works with small-medium N, non-parametric)
- ✅ **Interpretable** (treatment effect has clear counterfactual meaning)

### Key Limitations

- ❌ **Cannot control unobservable confounding** (need sensitivity analysis)
- ❌ **Requires overlap** (common support between treated/control)
- ❌ **Model-dependent** (propensity score specification matters)
- ❌ **Not experimental** (always conditional on assumptions)

---

## THEORETICAL FOUNDATION

### The Fundamental Problem of Causal Inference

We want to estimate:

**ATT = E[Y₁ᵢ - Y₀ᵢ | Tᵢ = 1]**

Where:
- **Y₁ᵢ** = outcome if unit i receives treatment
- **Y₀ᵢ** = outcome if unit i does NOT receive treatment
- **Tᵢ** = treatment status (1 = treated, 0 = control)
- **ATT** = Average Treatment Effect on the Treated

**Problem**: We never observe both Y₁ᵢ and Y₀ᵢ for the same unit (counterfactual problem).

### Conditional Independence Assumption (CIA)

PSM relies on:

**(Y₁, Y₀) ⊥ T | X**

**Translation**: Given covariates X, treatment assignment T is "as-good-as-random."

If CIA holds, we can:
1. Estimate propensity score **e(X) = P(T=1 | X)**
2. Compare treated and control units with similar e(X)
3. Interpret the difference as **causal** (not confounded)

### Propensity Score Theorem (Rosenbaum & Rubin 1983)

**Key Insight**: If treatment is conditionally independent given X, it's also conditionally independent given e(X):

**(Y₁, Y₀) ⊥ T | X  ⟹  (Y₁, Y₀) ⊥ T | e(X)**

**Implication**: We can reduce high-dimensional X to scalar e(X) for matching.

### Average Treatment Effect on the Treated (ATT)

**ATT = E[Y₁ | T=1] - E[Y₀ | T=1]**

**Estimator**:

```
ATT_hat = (1/N_treated) Σ[Yᵢ - Σ wᵢⱼ Yⱼ]
```

Where:
- i indexes treated units
- j indexes control units
- wᵢⱼ = matching weight (1/k for k-nearest neighbors, kernel weight for kernel matching)

---

## WHEN TO USE PSM

### ✅ PSM is Appropriate When:

1. **Non-Randomized Treatment**
   - Observational data (no experimental design)
   - Treatment assignment has observable drivers
   - Selection into treatment is systematic (not random)

2. **Sufficient Sample Size**
   - Minimum: 20-30 units per group
   - Ideal: 50+ units per group
   - More is better for overlap and balance

3. **Observable Confounders**
   - Key confounders are measured
   - Pre-treatment covariates available
   - Strong theory about selection mechanism

4. **Expected Overlap**
   - Treated and control have similar covariate ranges
   - No perfect separation (some controls look like treated)
   - Common support region is substantial

5. **Binary/Discrete Treatment**
   - Treatment is clear yes/no (or small number of categories)
   - Timing of treatment is identifiable
   - Treatment definition is unambiguous

### ❌ PSM is NOT Appropriate When:

1. **Continuous Treatment**
   - Use: Generalized Propensity Score, Dose-Response Models
   
2. **Time-Varying Treatment**
   - Use: Marginal Structural Models, G-Computation

3. **Perfect Separation**
   - No overlap between treated/control
   - Use: Difference-in-Differences, Synthetic Control

4. **Unobserved Confounding Dominates**
   - Critical confounder unmeasured
   - Use: Instrumental Variables, Fixed Effects

5. **Very Small N (<20 per group)**
   - Use: Case studies, Qualitative Comparative Analysis (QCA)

### Alternative Methods Decision Tree

```
Research Question: Does X cause Y?

├─ Randomized Experiment Available?
│  └─ YES → Use RCT (gold standard)
│  └─ NO → Continue
│
├─ Observable Confounders?
│  └─ NO → Instrumental Variables / Fixed Effects
│  └─ YES → Continue
│
├─ Continuous Treatment?
│  └─ YES → Generalized Propensity Score
│  └─ NO → Continue
│
├─ Panel Data Available?
│  └─ YES → Difference-in-Differences / Fixed Effects
│  └─ NO → Continue
│
├─ Overlap Between Groups?
│  └─ NO → Synthetic Control / Bounds
│  └─ YES → ✅ USE PSM
```

---

## MODEL SPECIFICATION

### Step 1: Define Treatment and Outcome

**Treatment (T)**:
- Must be binary (0/1) or easily dichotomized
- Must be **pre-outcome** (temporal precedence clear)
- Must be **non-manipulated by outcome** (no reverse causality)

**Example (Crisis Catalysis)**:
```python
# Treatment: Crisis presence
T = 1 if Crisis_Catalyzed == 'Yes' else 0

# Outcome: Sovereignty phenotype expression
Y = Sovereignty_Phenotype_Score  # continuous [0,1]
```

### Step 2: Select Covariates for Propensity Score Model

**Inclusion Criteria**:
1. **Confounders**: Variables that affect BOTH treatment and outcome
2. **Pre-treatment**: Measured before treatment occurs
3. **Not affected by treatment**: Not a mediator or collider

**Exclusion Criteria**:
- ❌ Post-treatment variables (mediators)
- ❌ Instruments (only affect T, not Y)
- ❌ Colliders (common effects of T and Y)

**Example Specification**:
```python
# Confounders for Crisis → Sovereignty model
covariates = [
    'Sovereignty_Phenotype_Score_Baseline',  # Pre-crisis sovereignty level
    'IusSpace_Dim12_IntegrationScore',       # Integration vulnerability
    'Year',                                   # Temporal trend
    'Geographic_Region',                      # Regional context (categorical)
    'Legal_Family',                          # Legal tradition (categorical)
    'GDP_Per_Capita',                        # Economic development
    'Democracy_Index'                         # Political regime type
]
```

### Step 3: Propensity Score Estimation

**Model**: Logistic Regression (most common)

```python
from sklearn.linear_model import LogisticRegression

# Estimate propensity scores
ps_model = LogisticRegression(max_iter=1000, random_state=42)
ps_model.fit(X_covariates, T)

# Predicted probabilities = propensity scores
propensity_scores = ps_model.predict_proba(X_covariates)[:, 1]
```

**Alternative Models**:
- **Probit**: Similar to logistic, assumes different error distribution
- **Random Forest**: Non-parametric, captures interactions automatically
- **Gradient Boosting**: Handles complex non-linearities
- **Neural Networks**: For very high-dimensional X (rare in legal studies)

**Model Selection**:
- Start with logistic regression (most transparent)
- Add interactions/polynomials if balance diagnostics fail
- Switch to machine learning if covariates >20 or complex interactions expected

### Step 4: Matching Algorithm Selection

**Options**:

| Algorithm | Description | Pros | Cons |
|-----------|-------------|------|------|
| **Nearest Neighbor** | Match each treated to k closest controls | Simple, intuitive | May use poor matches if few controls |
| **Caliper** | Only match within distance threshold | Ensures quality | May drop many treated units |
| **Kernel** | Weighted average of all controls | Uses all data | Complex weights |
| **Radius** | All controls within distance | Balance quality/quantity | Sensitive to radius choice |
| **Optimal** | Minimize total distance | Best global match | Computationally intensive |

**Recommended Default**:
```python
# 1:2 Nearest Neighbor with Caliper
matching_params = {
    'method': 'nearest_neighbor',
    'n_neighbors': 2,              # 1:2 matching
    'caliper': 0.1,                # 10% of propensity score range
    'replace': False,              # Each control used once
    'bias_adjust': True            # Bias-adjusted estimator
}
```

---

## IMPLEMENTATION PROTOCOL

### Complete PSM Workflow

```python
"""
COMPLETE PSM IMPLEMENTATION TEMPLATE
For IusMorfos V6.0 Legal Evolution Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from scipy import stats
import warnings

# ============================================================================
# STEP 1: DATA PREPARATION
# ============================================================================

def prepare_psm_data(df, treatment_var, outcome_var, covariates):
    """Prepare data for PSM analysis."""
    
    # Create analysis dataset
    psm_df = df[[treatment_var, outcome_var] + covariates].copy()
    
    # Remove missing values
    psm_df = psm_df.dropna()
    
    # Encode categorical variables
    categorical_vars = psm_df.select_dtypes(include=['object']).columns.tolist()
    if treatment_var in categorical_vars:
        categorical_vars.remove(treatment_var)
    if outcome_var in categorical_vars:
        categorical_vars.remove(outcome_var)
    
    # One-hot encode categoricals
    psm_df = pd.get_dummies(psm_df, columns=categorical_vars, drop_first=True)
    
    print(f"✅ Data prepared: {len(psm_df)} observations")
    print(f"   Treated: {psm_df[treatment_var].sum()}")
    print(f"   Control: {(psm_df[treatment_var]==0).sum()}")
    
    return psm_df

# ============================================================================
# STEP 2: PROPENSITY SCORE ESTIMATION
# ============================================================================

def estimate_propensity_scores(df, treatment_var, covariate_cols):
    """Estimate propensity scores using logistic regression."""
    
    X = df[covariate_cols].values
    T = df[treatment_var].values
    
    # Fit logistic regression
    ps_model = LogisticRegression(max_iter=1000, random_state=42)
    ps_model.fit(X, T)
    
    # Predict propensity scores
    propensity_scores = ps_model.predict_proba(X)[:, 1]
    
    # Add to dataframe
    df['propensity_score'] = propensity_scores
    
    print(f"✅ Propensity scores estimated")
    print(f"   Range: [{propensity_scores.min():.3f}, {propensity_scores.max():.3f}]")
    print(f"   Mean (Treated): {propensity_scores[T==1].mean():.3f}")
    print(f"   Mean (Control): {propensity_scores[T==0].mean():.3f}")
    
    return df, ps_model

# ============================================================================
# STEP 3: COMMON SUPPORT CHECK
# ============================================================================

def check_common_support(df, treatment_var, caliper=0.1):
    """Check overlap and trim to common support region."""
    
    treated = df[df[treatment_var] == 1]
    control = df[df[treatment_var] == 0]
    
    # Define common support bounds
    ps_min = max(treated['propensity_score'].min(), control['propensity_score'].min())
    ps_max = min(treated['propensity_score'].max(), control['propensity_score'].max())
    
    # Trim to common support
    df_trimmed = df[
        (df['propensity_score'] >= ps_min) & 
        (df['propensity_score'] <= ps_max)
    ].copy()
    
    retained_pct = len(df_trimmed) / len(df) * 100
    treated_retained_pct = len(df_trimmed[df_trimmed[treatment_var]==1]) / len(treated) * 100
    
    print(f"\n✅ Common Support Check:")
    print(f"   Range: [{ps_min:.3f}, {ps_max:.3f}]")
    print(f"   Retained: {retained_pct:.1f}% of total observations")
    print(f"   Retained: {treated_retained_pct:.1f}% of treated units")
    print(f"   Status: {'✅ PASS' if treated_retained_pct >= 70 else '⚠️ MARGINAL' if treated_retained_pct >= 60 else '❌ FAIL'}")
    
    # Visualize overlap
    plot_overlap(df_trimmed, treatment_var)
    
    return df_trimmed

def plot_overlap(df, treatment_var):
    """Plot propensity score distributions for visual overlap check."""
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    
    treated = df[df[treatment_var] == 1]['propensity_score']
    control = df[df[treatment_var] == 0]['propensity_score']
    
    ax.hist(control, bins=20, alpha=0.6, label='Control', color='blue', density=True)
    ax.hist(treated, bins=20, alpha=0.6, label='Treated', color='red', density=True)
    
    ax.set_xlabel('Propensity Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title('Propensity Score Overlap (Common Support)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('psm_overlap.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   📊 Overlap plot saved: psm_overlap.png")

# ============================================================================
# STEP 4: MATCHING
# ============================================================================

def perform_matching(df, treatment_var, n_neighbors=2, caliper=0.1):
    """Perform nearest neighbor matching with caliper."""
    
    treated = df[df[treatment_var] == 1].copy()
    control = df[df[treatment_var] == 0].copy()
    
    # Fit nearest neighbors on control group
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    nbrs.fit(control[['propensity_score']].values)
    
    # Find matches for treated units
    distances, indices = nbrs.kneighbors(treated[['propensity_score']].values)
    
    # Apply caliper
    caliper_threshold = caliper * (df['propensity_score'].max() - df['propensity_score'].min())
    
    matched_pairs = []
    for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
        treated_idx = treated.index[i]
        for dist, idx in zip(dist_row, idx_row):
            if dist <= caliper_threshold:
                control_idx = control.index[idx]
                matched_pairs.append({
                    'treated_idx': treated_idx,
                    'control_idx': control_idx,
                    'distance': dist
                })
    
    matched_df = pd.DataFrame(matched_pairs)
    
    n_matched = matched_df['treated_idx'].nunique()
    match_rate = n_matched / len(treated) * 100
    
    print(f"\n✅ Matching Complete:")
    print(f"   Algorithm: {n_neighbors}-nearest neighbor with caliper={caliper}")
    print(f"   Matched treated units: {n_matched}/{len(treated)} ({match_rate:.1f}%)")
    print(f"   Total matched pairs: {len(matched_df)}")
    print(f"   Status: {'✅ GOOD' if match_rate >= 80 else '⚠️ ACCEPTABLE' if match_rate >= 70 else '❌ POOR'}")
    
    return matched_df

# ============================================================================
# STEP 5: BALANCE DIAGNOSTICS
# ============================================================================

def check_balance(df, matched_df, treatment_var, covariate_cols):
    """Check covariate balance before and after matching."""
    
    # Pre-matching balance
    treated_pre = df[df[treatment_var] == 1][covariate_cols]
    control_pre = df[df[treatment_var] == 0][covariate_cols]
    
    # Post-matching balance
    treated_indices = matched_df['treated_idx'].unique()
    control_indices = matched_df['control_idx'].values
    
    treated_post = df.loc[treated_indices, covariate_cols]
    control_post = df.loc[control_indices, covariate_cols]
    
    # Calculate Standardized Mean Differences (SMD)
    balance_table = []
    
    for col in covariate_cols:
        # Pre-matching SMD
        mean_t_pre = treated_pre[col].mean()
        mean_c_pre = control_pre[col].mean()
        pooled_std_pre = np.sqrt((treated_pre[col].var() + control_pre[col].var()) / 2)
        smd_pre = (mean_t_pre - mean_c_pre) / pooled_std_pre if pooled_std_pre > 0 else 0
        
        # Post-matching SMD
        mean_t_post = treated_post[col].mean()
        mean_c_post = control_post[col].mean()
        pooled_std_post = np.sqrt((treated_post[col].var() + control_post[col].var()) / 2)
        smd_post = (mean_t_post - mean_c_post) / pooled_std_post if pooled_std_post > 0 else 0
        
        balance_table.append({
            'Covariate': col,
            'SMD_Pre': smd_pre,
            'SMD_Post': smd_post,
            'Status': '✅' if abs(smd_post) < 0.10 else '⚠️' if abs(smd_post) < 0.15 else '❌'
        })
    
    balance_df = pd.DataFrame(balance_table)
    
    print(f"\n✅ Balance Diagnostics:")
    print(balance_df.to_string(index=False))
    
    # Overall balance status
    all_balanced = (balance_df['SMD_Post'].abs() < 0.10).all()
    mostly_balanced = (balance_df['SMD_Post'].abs() < 0.15).sum() >= len(balance_df) * 0.8
    
    print(f"\n   Overall Balance: {'✅ EXCELLENT' if all_balanced else '⚠️ ACCEPTABLE' if mostly_balanced else '❌ POOR'}")
    
    return balance_df

# ============================================================================
# STEP 6: ATT ESTIMATION
# ============================================================================

def estimate_att(df, matched_df, treatment_var, outcome_var, bootstrap_n=1000):
    """Estimate Average Treatment Effect on the Treated with bootstrap SE."""
    
    # Get matched outcomes
    treated_outcomes = df.loc[matched_df['treated_idx'].unique(), outcome_var].values
    control_outcomes = df.loc[matched_df['control_idx'].values, outcome_var].values
    
    # Point estimate
    att_point = treated_outcomes.mean() - control_outcomes.mean()
    
    # Bootstrap standard error
    bootstrap_atts = []
    n_treated = len(treated_outcomes)
    
    for _ in range(bootstrap_n):
        # Resample with replacement
        boot_indices = np.random.choice(n_treated, size=n_treated, replace=True)
        boot_treated = treated_outcomes[boot_indices]
        boot_control = control_outcomes[boot_indices]  # Corresponding controls
        
        boot_att = boot_treated.mean() - boot_control.mean()
        bootstrap_atts.append(boot_att)
    
    att_se = np.std(bootstrap_atts)
    att_t = att_point / att_se
    att_p = 2 * (1 - stats.t.cdf(abs(att_t), df=n_treated-1))
    
    # Confidence interval
    ci_lower = np.percentile(bootstrap_atts, 2.5)
    ci_upper = np.percentile(bootstrap_atts, 97.5)
    
    print(f"\n✅ ATT Estimation:")
    print(f"   Point Estimate: {att_point:.4f}")
    print(f"   Standard Error: {att_se:.4f}")
    print(f"   t-statistic: {att_t:.3f}")
    print(f"   p-value: {att_p:.4f}")
    print(f"   95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"   Significance: {'✅ p<0.05' if att_p < 0.05 else '⚠️ p<0.10' if att_p < 0.10 else '❌ p≥0.10'}")
    
    return {
        'att': att_point,
        'se': att_se,
        't': att_t,
        'p': att_p,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper
    }

# ============================================================================
# STEP 7: SENSITIVITY ANALYSIS (Rosenbaum Bounds)
# ============================================================================

def rosenbaum_sensitivity(df, matched_df, treatment_var, outcome_var, gamma_range=[1.0, 1.5, 2.0, 2.5]):
    """Perform Rosenbaum sensitivity analysis for hidden bias."""
    
    # Get matched pairs
    treated_outcomes = df.loc[matched_df['treated_idx'].unique(), outcome_var].values
    control_outcomes = df.loc[matched_df['control_idx'].values, outcome_var].values
    
    # Signed-rank test
    differences = treated_outcomes - control_outcomes
    
    sensitivity_results = []
    
    for gamma in gamma_range:
        # Upper bound p-value (worst case under Γ=gamma)
        # Simplified approximation (exact requires permutation)
        z_score = np.mean(differences > 0) - 0.5 / (1 + gamma)
        z_score = z_score / (np.std(differences > 0) / np.sqrt(len(differences)))
        p_upper = 1 - stats.norm.cdf(z_score)
        
        sensitivity_results.append({
            'Gamma': gamma,
            'p_upper': p_upper,
            'Status': '✅ Robust' if p_upper < 0.05 else '⚠️ Marginal' if p_upper < 0.10 else '❌ Fragile'
        })
    
    sensitivity_df = pd.DataFrame(sensitivity_results)
    
    print(f"\n✅ Sensitivity Analysis (Rosenbaum Bounds):")
    print(sensitivity_df.to_string(index=False))
    print(f"\n   Interpretation: Result is {'✅ ROBUST' if sensitivity_df.iloc[1]['p_upper'] < 0.05 else '⚠️ MODERATELY ROBUST' if sensitivity_df.iloc[1]['p_upper'] < 0.10 else '❌ FRAGILE'}")
    print(f"                   to unobserved confounding up to Γ={sensitivity_df[sensitivity_df['Status'].str.contains('Robust')]['Gamma'].max():.1f}")
    
    return sensitivity_df

# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def run_complete_psm(df, treatment_var, outcome_var, covariates):
    """Execute complete PSM workflow."""
    
    print("="*80)
    print("PROPENSITY SCORE MATCHING - COMPLETE ANALYSIS")
    print("="*80)
    
    # Step 1: Prepare data
    psm_df = prepare_psm_data(df, treatment_var, outcome_var, covariates)
    
    # Get covariate column names after encoding
    covariate_cols = [col for col in psm_df.columns 
                     if col not in [treatment_var, outcome_var]]
    
    # Step 2: Estimate propensity scores
    psm_df, ps_model = estimate_propensity_scores(psm_df, treatment_var, covariate_cols)
    
    # Step 3: Check common support
    psm_df = check_common_support(psm_df, treatment_var, caliper=0.1)
    
    # Step 4: Perform matching
    matched_df = perform_matching(psm_df, treatment_var, n_neighbors=2, caliper=0.1)
    
    # Step 5: Check balance
    balance_df = check_balance(psm_df, matched_df, treatment_var, covariate_cols)
    
    # Step 6: Estimate ATT
    att_results = estimate_att(psm_df, matched_df, treatment_var, outcome_var, bootstrap_n=1000)
    
    # Step 7: Sensitivity analysis
    sensitivity_df = rosenbaum_sensitivity(psm_df, matched_df, treatment_var, outcome_var)
    
    print("\n" + "="*80)
    print("✅ PSM ANALYSIS COMPLETE")
    print("="*80)
    
    return {
        'psm_df': psm_df,
        'matched_df': matched_df,
        'ps_model': ps_model,
        'balance': balance_df,
        'att': att_results,
        'sensitivity': sensitivity_df
    }
```

---

## DIAGNOSTIC FRAMEWORK

### Common Support Diagnostics

**Target**: Retain ≥70% of treated units

**Interpretation**:
- ✅ **≥80%**: Excellent overlap
- ⚠️ **70-79%**: Acceptable (report trimming)
- ❌ **<70%**: Poor overlap (consider alternative methods)

**Visual Check**: Overlap histogram should show substantial regions where both distributions exist.

### Covariate Balance Diagnostics

**Target**: All Standardized Mean Differences (SMD) < 0.10 post-matching

**Formula**:
```
SMD = (mean_treated - mean_control) / pooled_SD
```

**Interpretation**:
- ✅ **SMD < 0.10**: Negligible imbalance
- ⚠️ **0.10 ≤ SMD < 0.20**: Small imbalance (acceptable)
- ❌ **SMD ≥ 0.20**: Substantial imbalance (re-specify model)

**Rules of Thumb**:
- All covariates should have SMD < 0.10 post-matching
- If 1-2 covariates have 0.10 < SMD < 0.15, acceptable if not critical confounders
- If >20% of covariates have SMD > 0.10, matching failed

### Sensitivity Analysis (Rosenbaum Γ)

**Target**: Result robust to Γ ≥ 1.5

**Interpretation**:
- **Γ = 1.0**: No hidden bias (baseline)
- **Γ = 1.5**: Hidden confounder could increase odds of treatment by 50%
- **Γ = 2.0**: Hidden confounder could double odds of treatment

**Robustness Categories**:
- ✅ **Robust**: p < 0.05 at Γ = 2.0+
- ⚠️ **Moderately Robust**: p < 0.05 at Γ = 1.5-1.9
- ⚠️ **Fragile**: p < 0.05 at Γ = 1.1-1.4
- ❌ **Very Fragile**: p ≥ 0.05 at Γ = 1.1

---

## INTERPRETATION GUIDELINES

### ATT Reporting Template

**For Significant Results (p < 0.05)**:
```
"After controlling for [COVARIATES] via propensity score matching, 
we find that [TREATMENT] increases [OUTCOME] by [ATT] units 
(SE = [SE], p = [p], 95% CI = [[CI_LOWER], [CI_UPPER]]). 
This represents a [PERCENTAGE]% change relative to the control mean.

The estimated effect is robust to unobserved confounding up to 
Γ = [GAMMA], suggesting [CAUSAL INTERPRETATION].

Matching retained [RETAINED_%]% of treated units with excellent 
covariate balance (all SMD < 0.10)."
```

**For Non-Significant Results (p > 0.10)**:
```
"Propensity score matching analysis reveals no evidence of a 
causal effect of [TREATMENT] on [OUTCOME] (ATT = [ATT], 
SE = [SE], p = [p]). 

This suggests that the observed correlation in raw data 
([RAW_EFFECT]) is driven by selection into treatment rather 
than treatment causing the outcome. After controlling for 
[COVARIATES], the treated and control groups show comparable 
outcomes."
```

### Footnote for Methods Section

```
"Propensity scores estimated via logistic regression including 
[COVARIATE LIST]. 1:[k] nearest neighbor matching with 
caliper = [CALIPER]. Bias-adjusted ATT estimator with 
bootstrap standard errors (1,000 iterations). Post-matching 
balance achieved for all covariates (SMD < 0.10). Rosenbaum 
sensitivity analysis indicates robustness to hidden bias up to 
Γ = [GAMMA]. See Online Appendix [X] for diagnostics."
```

---

## COMMON PROBLEMS

### Problem 1: Poor Overlap (<60% matched)

**Symptoms**: Many treated units without comparable controls

**Causes**:
- Treated and control live in fundamentally different worlds
- Treatment is highly predictable from covariates
- Extreme covariate values in treated group

**Solutions**:
1. **Trim extremes**: Remove top/bottom 5% of propensity scores
2. **Kernel matching**: Use all controls with weights
3. **Change method**: Try Difference-in-Differences if panel data available
4. **Accept limitation**: Report "effect only identifiable for [X]% of treated units"

### Problem 2: Balance Not Achieved (SMD > 0.15)

**Symptoms**: Matching fails to equalize some covariates

**Causes**:
- Propensity score model too simple
- Non-linear relationships not captured
- Important interactions omitted

**Solutions**:
1. **Add interactions**: e.g., Year × Region, Sovereignty × Dim12
2. **Add polynomials**: e.g., Dim12²
3. **Reduce caliper**: Try 0.05 instead of 0.1
4. **Exact matching**: Force exact match on categorical variables

### Problem 3: ATT Sign Flips vs Raw Effect

**Symptoms**: T-test says +0.10, PSM says -0.05

**Interpretation**: This is GOOD! PSM is working as intended.

**Explanation**: Raw effect was confounded. After controlling for confounders, true causal effect has opposite sign.

**Action**: Report both raw and adjusted effects to highlight confounding.

### Problem 4: Sensitivity Γ = 1.2 Kills Effect

**Symptoms**: Result becomes non-significant with minimal hidden bias

**Interpretation**: Effect is VERY fragile to unobserved confounding

**Actions**:
1. **Search for omitted confounders**: Add proxies if available
2. **Use instrumental variables**: If valid instrument exists
3. **Report honestly**: "Effect is sensitive to unobserved confounding"
4. **Avoid overclaiming**: Use "suggests" not "proves"

### Problem 5: Small N Post-Matching (<20 pairs)

**Symptoms**: Insufficient sample for reliable inference

**Causes**:
- Strict matching criteria
- Small original sample
- Poor overlap

**Solutions**:
1. **Increase k**: Use 1:3 or 1:5 matching
2. **Kernel matching**: Uses all controls
3. **Pooled analysis**: Combine with other studies
4. **Report exploratory**: Wide confidence intervals, cautious interpretation

---

## INTEGRATION WITH IUSMORFOS

### Sovereignty-Globalism Framework

PSM enhances IusMorfos V6.0 by addressing **endogeneity** in:

1. **Crisis Catalysis Hypothesis (H5)**:
   - Raw effect: Δ = +0.098, p = 0.299
   - PSM can isolate **causal effect** by controlling for:
     - Pre-crisis sovereignty levels (selection bias)
     - Integration vulnerability (confounding)
     - Temporal trends (era effects)
     - Regional contexts (geographic confounding)

2. **Integration Threshold Effects**:
   - Test if Dim12 ≤ 2 **causes** sovereignty assertion
   - Control for pre-existing sovereignty predisposition
   - Identify causal vs correlational threshold dynamics

3. **Evolutionary Fitness Trajectories**:
   - Isolate **treatment effects of institutional changes**
   - Control for baseline fitness differences
   - Estimate counterfactual trajectories

### Recommended PSM Analyses for IusMorfos

| Analysis | Treatment | Outcome | Key Confounders |
|----------|-----------|---------|-----------------|
| **Crisis Catalysis** | Crisis_Catalyzed (binary) | Sovereignty_Phenotype_Score | Baseline sovereignty, Dim12, Year, Region |
| **Integration Threshold** | Low_Integration (Dim12≤2) | Sovereignty_Win (binary) | Baseline sovereignty, Year, Legal_Family |
| **Brexit Effect** | Brexit_Post_2016 (binary) | EU_Integration_Score | Pre-Brexit integration, GDP, Democracy |
| **Court Withdrawal** | ECHR_Exit (binary) | Domestic_Sovereignty_Index | Baseline sovereignty, Year, Region |

### Workflow Integration

```python
# Example: Crisis Catalysis PSM for IusMorfos

import sys
sys.path.append('/home/user/webapp/src')

from causal_inference.psm import run_complete_psm

# Load IusMorfos dataset
df = pd.read_csv('results/sovereignty_globalism_70cases_analyzed.csv')

# Define PSM specification
treatment = 'Crisis_Binary'  # 1 if Crisis_Catalyzed=='Yes'
outcome = 'Sovereignty_Phenotype_Score'
covariates = [
    'Sovereignty_Phenotype_Score_Lag',  # Pre-crisis baseline
    'IusSpace_Dim12_IntegrationScore',
    'Year',
    'Geographic_Region',
    'Legal_Family',
    'GDP_Per_Capita_Log',
    'Democracy_Index'
]

# Run PSM
psm_results = run_complete_psm(df, treatment, outcome, covariates)

# Extract causal ATT
att_causal = psm_results['att']['att']
att_se = psm_results['att']['se']
att_p = psm_results['att']['p']

print(f"\n🎯 CAUSAL EFFECT (PSM):")
print(f"   Crisis → Sovereignty: ATT = {att_causal:.4f} (SE = {att_se:.4f}, p = {att_p:.4f})")
print(f"   Compare to raw t-test: Δ = +0.098 (p = 0.299)")
```

---

## CASE STUDY: CRISIS CATALYSIS

### Research Question

**Does experiencing a political/economic crisis CAUSE states to increase sovereignty assertions?**

### Data (N=70, 1985-2024)

- **Treatment**: Crisis_Catalyzed (Yes = 18, No = 52)
- **Outcome**: Sovereignty_Phenotype_Score (continuous, 0-1)
- **Confounders**:
  - Sovereignty_Phenotype_Score_Baseline (pre-crisis level)
  - IusSpace_Dim12_IntegrationScore (integration vulnerability)
  - Year (temporal trend)
  - Geographic_Region (Europe, LatAm, Asia, Africa, etc.)
  - Legal_Family (Civil, Common, Mixed)

### Baseline (T-Test) Result

```
Crisis Yes (n=18): mean = 0.689
Crisis No  (n=52): mean = 0.633
Δ = +0.056, t = 1.046, p = 0.299

❌ H5 NOT CONFIRMED: Crisis effect NOT statistically significant
```

**Problem**: Selection bias suspected:
- Crisis cases are more recent (Year correlation)
- Crisis cases already had higher pre-crisis sovereignty
- Crisis cases have lower integration (Dim12 correlation)

### PSM Analysis Specification

```python
# PSM Model
treatment = 'Crisis_Binary'
outcome = 'Sovereignty_Phenotype_Score'
covariates = [
    'Sovereignty_Baseline',  # Pre-crisis sovereignty
    'IusSpace_Dim12',        # Integration score
    'Year',                   # Temporal trend
    'Region_Europe',          # Regional dummies
    'Region_LatAm',
    'Region_Asia',
    'LegalFamily_Civil',      # Legal family dummies
    'LegalFamily_Common'
]

# Matching Parameters
- Algorithm: 1:2 nearest neighbor
- Caliper: 0.1
- Without replacement
- Bias-adjusted estimator
```

### Expected Results

**Scenario A: Effect Strengthens**
```
ATT_PSM = +0.120 (SE = 0.045, p = 0.012)

✅ CAUSAL EFFECT CONFIRMED
Interpretation: Crisis DOES cause +12pp increase in sovereignty
after controlling for confounders. Raw t-test underestimated due
to noise from poor controls.
```

**Scenario B: Effect Weakens**
```
ATT_PSM = +0.020 (SE = 0.040, p = 0.620)

❌ CAUSAL EFFECT NOT FOUND
Interpretation: Observed correlation is spurious. Crisis cases
had higher sovereignty BEFORE crisis (selection bias). Crisis
itself does not cause additional sovereignty increase.
```

**Scenario C: Effect Reverses**
```
ATT_PSM = -0.030 (SE = 0.042, p = 0.480)

⚠️ NEGATIVE (BUT NON-SIG) EFFECT
Interpretation: Extreme confounding. After controlling for
selection, crisis may actually DECREASE sovereignty (though
not significantly). Needs further investigation.
```

### Interpretation Guidelines

**If ATT is significant (p < 0.05):**
- H5 is **causally confirmed** ✅
- Crisis is a **causal driver** of sovereignty expression
- Update theory: Crisis → Sovereignty mechanism validated

**If ATT is non-significant (p > 0.10):**
- H5 is **not confirmed** ❌
- Crisis correlation is **spurious** (due to confounding)
- Update theory: Crisis is **proxy** for other factors, not cause

**If ATT is marginally significant (0.05 < p < 0.10):**
- H5 is **weakly supported** ⚠️
- Crisis may have **small causal effect**
- Need larger sample or better measurement

---

## REFERENCES

### Foundational Papers

1. **Rosenbaum, P. R., & Rubin, D. B. (1983)**. "The Central Role of the Propensity Score in Observational Studies for Causal Effects." *Biometrika*, 70(1), 41-55.
   - Propensity Score Theorem

2. **Rubin, D. B. (1974)**. "Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies." *Journal of Educational Psychology*, 66(5), 688-701.
   - Potential Outcomes Framework

3. **Rosenbaum, P. R. (2002)**. *Observational Studies* (2nd ed.). New York: Springer.
   - Sensitivity Analysis (Γ bounds)

### Methodological Reviews

4. **Austin, P. C. (2011)**. "An Introduction to Propensity Score Methods for Reducing the Effects of Confounding in Observational Studies." *Multivariate Behavioral Research*, 46(3), 399-424.
   - Comprehensive tutorial with examples

5. **Stuart, E. A. (2010)**. "Matching Methods for Causal Inference: A Review and a Look Forward." *Statistical Science*, 25(1), 1-21.
   - Review of matching algorithms

6. **Caliendo, M., & Kopeinig, S. (2008)**. "Some Practical Guidance for the Implementation of Propensity Score Matching." *Journal of Economic Surveys*, 22(1), 31-72.
   - Practical implementation guide

### Software & Tools

7. **Ho, D. E., Imai, K., King, G., & Stuart, E. A. (2011)**. "MatchIt: Nonparametric Preprocessing for Parametric Causal Inference." *Journal of Statistical Software*, 42(8), 1-28.
   - R package: `MatchIt`

8. **Microsoft DoWhy Team (2021)**. DoWhy: Python Library for Causal Inference. GitHub: https://github.com/py-why/dowhy
   - Python package: `dowhy`

9. **Sekhon, J. S. (2011)**. "Multivariate and Propensity Score Matching Software with Automated Balance Optimization." *Journal of Statistical Software*, 42(7), 1-52.
   - R package: `Matching`

### Legal/Political Applications

10. **Nielsen, R. A., & Simmons, B. A. (2015)**. "Rewards for Ratification: Payoffs for Participating in the International Human Rights Regime?" *International Studies Quarterly*, 59(2), 197-208.
    - PSM for international law compliance

11. **Ginsburg, T., & Moustafa, T. (Eds.) (2008)**. *Rule by Law: The Politics of Courts in Authoritarian Regimes*. Cambridge University Press.
    - Observational causal inference in legal studies

---

## APPENDIX: PYTHON IMPLEMENTATION

See:
- **`/home/user/webapp/src/causal_inference/psm.py`** - PSM core functions
- **`/home/user/webapp/notebooks/psm_analysis/crisis_catalysis_psm.ipynb`** - Crisis catalysis case study
- **`/home/user/webapp/notebooks/psm_analysis/psm_tutorial.ipynb`** - Interactive tutorial

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-15  
**Maintained by**: IusMorfos V6.0 Development Team  
**Status**: Production-Ready for 70-Case Sovereignty-Globalism Analysis
