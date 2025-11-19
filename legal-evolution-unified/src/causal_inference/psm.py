"""
Propensity Score Matching - Core Implementation
For IusMorfos V6.0 Legal Evolution Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from scipy import stats

def prepare_psm_data(df, treatment_var, outcome_var, covariates):
    """Prepare data for PSM analysis."""
    psm_df = df[[treatment_var, outcome_var] + covariates].copy()
    psm_df = psm_df.dropna()
    
    categorical_vars = psm_df.select_dtypes(include=['object']).columns.tolist()
    if treatment_var in categorical_vars:
        categorical_vars.remove(treatment_var)
    if outcome_var in categorical_vars:
        categorical_vars.remove(outcome_var)
    
    psm_df = pd.get_dummies(psm_df, columns=categorical_vars, drop_first=True)
    
    print(f"✅ Data prepared: {len(psm_df)} observations")
    print(f"   Treated: {psm_df[treatment_var].sum()}")
    print(f"   Control: {(psm_df[treatment_var]==0).sum()}")
    
    return psm_df

def estimate_propensity_scores(df, treatment_var, covariate_cols):
    """Estimate propensity scores using logistic regression."""
    X = df[covariate_cols].values
    T = df[treatment_var].values
    
    ps_model = LogisticRegression(max_iter=1000, random_state=42)
    ps_model.fit(X, T)
    
    propensity_scores = ps_model.predict_proba(X)[:, 1]
    df['propensity_score'] = propensity_scores
    
    print(f"✅ Propensity scores estimated")
    print(f"   Range: [{propensity_scores.min():.3f}, {propensity_scores.max():.3f}]")
    print(f"   Mean (Treated): {propensity_scores[T==1].mean():.3f}")
    print(f"   Mean (Control): {propensity_scores[T==0].mean():.3f}")
    
    return df, ps_model

def check_common_support(df, treatment_var, caliper=0.1):
    """Check overlap and trim to common support region."""
    treated = df[df[treatment_var] == 1]
    control = df[df[treatment_var] == 0]
    
    ps_min = max(treated['propensity_score'].min(), control['propensity_score'].min())
    ps_max = min(treated['propensity_score'].max(), control['propensity_score'].max())
    
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
    plt.savefig('visualizations/psm_overlap.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   📊 Overlap plot saved: visualizations/psm_overlap.png")

def perform_matching(df, treatment_var, n_neighbors=2, caliper=0.1):
    """Perform nearest neighbor matching with caliper."""
    treated = df[df[treatment_var] == 1].copy()
    control = df[df[treatment_var] == 0].copy()
    
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    nbrs.fit(control[['propensity_score']].values)
    
    distances, indices = nbrs.kneighbors(treated[['propensity_score']].values)
    
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

def check_balance(df, matched_df, treatment_var, covariate_cols):
    """Check covariate balance before and after matching."""
    treated_pre = df[df[treatment_var] == 1][covariate_cols]
    control_pre = df[df[treatment_var] == 0][covariate_cols]
    
    treated_indices = matched_df['treated_idx'].unique()
    control_indices = matched_df['control_idx'].values
    
    treated_post = df.loc[treated_indices, covariate_cols]
    control_post = df.loc[control_indices, covariate_cols]
    
    balance_table = []
    
    for col in covariate_cols:
        mean_t_pre = treated_pre[col].mean()
        mean_c_pre = control_pre[col].mean()
        pooled_std_pre = np.sqrt((treated_pre[col].var() + control_pre[col].var()) / 2)
        smd_pre = (mean_t_pre - mean_c_pre) / pooled_std_pre if pooled_std_pre > 0 else 0
        
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
    
    all_balanced = (balance_df['SMD_Post'].abs() < 0.10).all()
    mostly_balanced = (balance_df['SMD_Post'].abs() < 0.15).sum() >= len(balance_df) * 0.8
    
    print(f"\n   Overall Balance: {'✅ EXCELLENT' if all_balanced else '⚠️ ACCEPTABLE' if mostly_balanced else '❌ POOR'}")
    
    return balance_df

def estimate_att(df, matched_df, treatment_var, outcome_var, bootstrap_n=1000):
    """Estimate Average Treatment Effect on the Treated with bootstrap SE."""
    treated_outcomes = df.loc[matched_df['treated_idx'].unique(), outcome_var].values
    control_outcomes = df.loc[matched_df['control_idx'].values, outcome_var].values
    
    att_point = treated_outcomes.mean() - control_outcomes.mean()
    
    bootstrap_atts = []
    n_treated = len(treated_outcomes)
    
    for _ in range(bootstrap_n):
        boot_indices = np.random.choice(n_treated, size=n_treated, replace=True)
        boot_treated = treated_outcomes[boot_indices]
        boot_control = control_outcomes[boot_indices]
        
        boot_att = boot_treated.mean() - boot_control.mean()
        bootstrap_atts.append(boot_att)
    
    att_se = np.std(bootstrap_atts)
    att_t = att_point / att_se
    att_p = 2 * (1 - stats.t.cdf(abs(att_t), df=n_treated-1))
    
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

def rosenbaum_sensitivity(df, matched_df, treatment_var, outcome_var, gamma_range=[1.0, 1.5, 2.0, 2.5]):
    """Perform Rosenbaum sensitivity analysis for hidden bias."""
    # matched_df contains treated_idx and control_idx columns
    # Extract outcomes using these indices
    
    if len(matched_df) == 0:
        print("\n⚠️  WARNING: No matched pairs for sensitivity analysis")
        return pd.DataFrame({'Gamma': gamma_range, 'p_value_upper': [np.nan] * len(gamma_range), 
                           'Status': ['N/A'] * len(gamma_range)})
    
    # Get unique treated units and their outcomes
    treated_indices = matched_df['treated_idx'].unique()
    treated_outcomes = df.loc[treated_indices, outcome_var].values
    
    # Get control outcomes (may have duplicates if k>1)
    control_indices = matched_df['control_idx'].values
    control_outcomes = df.loc[control_indices, outcome_var].values
    
    sensitivity_results = []
    
    # If unequal sizes due to k-NN matching, aggregate controls by treated unit
    if len(treated_outcomes) != len(control_outcomes):
        # Group controls by treated unit (if matched_idx info available)
        n_treated = len(treated_outcomes)
        n_control = len(control_outcomes)
        k = n_control // n_treated  # matches per treated unit
        
        # Aggregate control outcomes (take mean of k nearest neighbors)
        control_outcomes_agg = []
        for i in range(n_treated):
            start_idx = i * k
            end_idx = start_idx + k
            control_outcomes_agg.append(np.mean(control_outcomes[start_idx:end_idx]))
        control_outcomes = np.array(control_outcomes_agg)
    
    differences = treated_outcomes - control_outcomes
    
    for gamma in gamma_range:
        # Simplified Rosenbaum bound calculation
        # Under Gamma=1 (no hidden bias), test H0: median(diff) = 0
        if len(differences) > 0:
            # Wilcoxon signed-rank test approximation
            positive_diffs = np.sum(differences > 0)
            n = len(differences)
            
            # Adjusted probability under hidden bias
            p_plus = positive_diffs / n if n > 0 else 0.5
            
            # Upper bound on p-value under gamma bias
            if gamma == 1.0:
                z_stat = (positive_diffs - n/2) / np.sqrt(n/4)
                p_upper = 1 - stats.norm.cdf(abs(z_stat))
            else:
                # Conservative upper bound
                pi_max = gamma / (1 + gamma)
                z_stat = (positive_diffs - n * pi_max) / np.sqrt(n * pi_max * (1 - pi_max))
                p_upper = 1 - stats.norm.cdf(z_stat)
        else:
            p_upper = 1.0
        
        sensitivity_results.append({
            'Gamma': gamma,
            'p_value_upper': max(0, min(1, p_upper)),  # Bound between 0 and 1
            'Status': '✅ Robust' if p_upper < 0.05 else '⚠️ Marginal' if p_upper < 0.10 else '❌ Fragile'
        })
    
    sensitivity_df = pd.DataFrame(sensitivity_results)
    
    print(f"\n✅ Sensitivity Analysis (Rosenbaum Bounds):")
    print(sensitivity_df.to_string(index=False))
    
    if len(sensitivity_df) > 1:
        print(f"\n   Interpretation: Result is {'✅ ROBUST' if sensitivity_df.iloc[1]['p_value_upper'] < 0.05 else '⚠️ MODERATELY ROBUST' if sensitivity_df.iloc[1]['p_value_upper'] < 0.10 else '❌ FRAGILE'}")
    
    return sensitivity_df

def run_complete_psm(df, treatment_var, outcome_var, covariates):
    """Execute complete PSM workflow."""
    print("="*80)
    print("PROPENSITY SCORE MATCHING - COMPLETE ANALYSIS")
    print("="*80)
    
    psm_df = prepare_psm_data(df, treatment_var, outcome_var, covariates)
    
    covariate_cols = [col for col in psm_df.columns 
                     if col not in [treatment_var, outcome_var]]
    
    psm_df, ps_model = estimate_propensity_scores(psm_df, treatment_var, covariate_cols)
    psm_df = check_common_support(psm_df, treatment_var, caliper=0.1)
    matched_df = perform_matching(psm_df, treatment_var, n_neighbors=2, caliper=0.1)
    balance_df = check_balance(psm_df, matched_df, treatment_var, covariate_cols)
    att_results = estimate_att(psm_df, matched_df, treatment_var, outcome_var, bootstrap_n=1000)
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
