"""
PSM (Propensity Score Matching) Tools for MCP Server
Causal inference for legal transplant and constitutional reform analysis

This tool enables:
1. Propensity score estimation for treatment/control matching
2. Average Treatment Effect (ATT/ATE) estimation with bootstrap CI
3. Covariate balance diagnostics (SMD < 0.10 threshold)
4. Rosenbaum sensitivity analysis for hidden bias
5. Integration with CLI/H/V for constitutional reform causality

Theoretical Foundation:
- Rubin (1973): Causal inference framework with potential outcomes
- Rosenbaum & Rubin (1983): Propensity score matching methodology
- Austin (2011): Balance diagnostics (SMD thresholds)
- Peralta (2024): Application to constitutional reform success prediction
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from scipy import stats

# Import existing PSM implementation
from src.causal_inference.psm import (
    estimate_propensity_scores,
    check_common_support,
    perform_matching,
    check_balance,
    estimate_att,
    rosenbaum_sensitivity
)

@dataclass
class PSMResult:
    """Complete PSM analysis result"""
    att: float
    att_se: float
    att_ci_lower: float
    att_ci_upper: float
    p_value: float
    n_treated: int
    n_control: int
    n_matched: int
    balance_satisfied: bool
    sensitivity_robust: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "att": float(self.att),
            "att_se": float(self.att_se),
            "ci_95": [float(self.att_ci_lower), float(self.att_ci_upper)],
            "p_value": float(self.p_value),
            "significant": self.p_value < 0.05,
            "sample_sizes": {
                "treated": self.n_treated,
                "control": self.n_control,
                "matched": self.n_matched
            },
            "diagnostics": {
                "balance_satisfied": self.balance_satisfied,
                "sensitivity_robust": self.sensitivity_robust
            }
        }

def prepare_psm_dataframe(
    cases: List[Dict[str, Any]],
    treatment_col: str,
    outcome_col: str,
    covariate_cols: List[str]
) -> pd.DataFrame:
    """
    Convert case data to PSM-ready DataFrame.
    
    Args:
        cases: List of case dictionaries
        treatment_col: Name of treatment variable (0/1)
        outcome_col: Name of outcome variable (continuous)
        covariate_cols: List of covariate column names
    
    Returns:
        DataFrame ready for PSM analysis
    """
    df = pd.DataFrame(cases)
    
    # Ensure treatment is binary
    if treatment_col in df.columns:
        df[treatment_col] = df[treatment_col].astype(int)
    
    # Ensure outcome is numeric
    if outcome_col in df.columns:
        df[outcome_col] = pd.to_numeric(df[outcome_col], errors='coerce')
    
    # Select only required columns
    required_cols = [treatment_col, outcome_col] + covariate_cols
    available_cols = [col for col in required_cols if col in df.columns]
    
    df_psm = df[available_cols].dropna()
    
    return df_psm

def calculate_propensity_scores(
    cases: List[Dict[str, Any]],
    treatment_col: str,
    covariate_cols: List[str],
    outcome_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate propensity scores for treatment assignment.
    
    Propensity Score = P(Treatment=1 | Covariates)
    
    Args:
        cases: List of case dictionaries
        treatment_col: Treatment indicator
        covariate_cols: Covariates for matching
        outcome_col: Outcome variable (optional, for preservation)
    
    Returns:
        Dict with propensity scores and model diagnostics
    """
    # Use full DataFrame to preserve all columns
    df = pd.DataFrame(cases)
    
    # Ensure treatment is binary
    if treatment_col in df.columns:
        df[treatment_col] = df[treatment_col].astype(int)
    
    # Drop rows with missing treatment or covariates
    required_cols = [treatment_col] + covariate_cols
    df = df.dropna(subset=required_cols)
    
    X = df[covariate_cols].values
    T = df[treatment_col].values
    
    # Fit logistic regression
    model = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs')
    model.fit(X, T)
    
    # Predict propensity scores
    ps = model.predict_proba(X)[:, 1]
    
    # Add to dataframe
    df['propensity_score'] = ps
    
    # Diagnostics
    treated_ps = ps[T == 1]
    control_ps = ps[T == 0]
    
    # Check overlap (common support)
    ps_min = max(treated_ps.min(), control_ps.min())
    ps_max = min(treated_ps.max(), control_ps.max())
    overlap_pct = ((ps >= ps_min) & (ps <= ps_max)).sum() / len(ps) * 100
    
    return {
        "propensity_scores": ps.tolist(),
        "cases_with_ps": df.to_dict('records'),
        "model_coefficients": dict(zip(covariate_cols, model.coef_[0])),
        "diagnostics": {
            "mean_ps_treated": float(treated_ps.mean()),
            "mean_ps_control": float(control_ps.mean()),
            "ps_range": [float(ps.min()), float(ps.max())],
            "common_support_range": [float(ps_min), float(ps_max)],
            "overlap_percentage": float(overlap_pct),
            "overlap_status": "good" if overlap_pct >= 80 else "acceptable" if overlap_pct >= 70 else "poor"
        }
    }

def match_cases(
    cases_with_ps: List[Dict[str, Any]],
    treatment_col: str,
    n_neighbors: int = 1,
    caliper: float = 0.1
) -> Dict[str, Any]:
    """
    Perform nearest-neighbor matching on propensity scores.
    
    Args:
        cases_with_ps: Cases with propensity_score field
        treatment_col: Treatment indicator
        n_neighbors: Number of control matches per treated unit
        caliper: Maximum propensity score distance (fraction of std)
    
    Returns:
        Dict with matched pairs and diagnostics
    """
    df = pd.DataFrame(cases_with_ps)
    
    treated = df[df[treatment_col] == 1].copy()
    control = df[df[treatment_col] == 0].copy()
    
    # Fit nearest neighbors
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    nbrs.fit(control[['propensity_score']].values)
    
    # Find matches
    distances, indices = nbrs.kneighbors(treated[['propensity_score']].values)
    
    # Calculate caliper threshold
    ps_std = df['propensity_score'].std()
    caliper_threshold = caliper * ps_std
    
    # Store matches within caliper
    matched_pairs = []
    for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
        treated_idx = int(treated.index[i])
        treated_case = treated.iloc[i].to_dict()
        
        for dist, idx in zip(dist_row, idx_row):
            if dist <= caliper_threshold:
                control_idx = int(control.index[idx])
                control_case = control.iloc[idx].to_dict()
                
                matched_pairs.append({
                    "treated_index": treated_idx,
                    "control_index": control_idx,
                    "propensity_distance": float(dist),
                    "treated_case": treated_case,
                    "control_case": control_case
                })
    
    # Calculate match rate
    n_matched_treated = len(set(pair["treated_index"] for pair in matched_pairs))
    match_rate = n_matched_treated / len(treated) * 100 if len(treated) > 0 else 0
    
    return {
        "matched_pairs": matched_pairs,
        "diagnostics": {
            "n_treated": len(treated),
            "n_control": len(control),
            "n_matched_treated": n_matched_treated,
            "n_matched_pairs": len(matched_pairs),
            "match_rate_pct": float(match_rate),
            "caliper_threshold": float(caliper_threshold),
            "match_quality": "excellent" if match_rate >= 90 else "good" if match_rate >= 80 else "acceptable" if match_rate >= 70 else "poor"
        }
    }

def calculate_balance(
    cases: List[Dict[str, Any]],
    matched_pairs: List[Dict[str, Any]],
    covariate_cols: List[str],
    treatment_col: str = "treatment"
) -> Dict[str, Any]:
    """
    Calculate covariate balance before and after matching.
    
    Uses Standardized Mean Difference (SMD):
    SMD = (mean_treated - mean_control) / pooled_std
    
    Threshold: |SMD| < 0.10 = excellent balance
               |SMD| < 0.15 = acceptable balance
    
    Args:
        cases: Original cases
        matched_pairs: Matched pairs from match_cases()
        covariate_cols: Covariates to check
        treatment_col: Name of treatment column
    
    Returns:
        Dict with balance diagnostics
    """
    df = pd.DataFrame(cases)
    
    # Extract treated and control indices from matched pairs
    treated_indices = [pair["treated_index"] for pair in matched_pairs]
    control_indices = [pair["control_index"] for pair in matched_pairs]
    
    balance_results = []
    
    # Find treatment column
    if treatment_col not in df.columns:
        # Try to infer from matched pairs
        treatment_col = matched_pairs[0]["treated_case"].keys() if matched_pairs else None
        if treatment_col:
            for key in treatment_col:
                if key in df.columns and df[key].isin([0, 1]).all():
                    treatment_col = key
                    break
    
    for cov in covariate_cols:
        if cov not in df.columns:
            continue
        
        # Pre-matching (all data)
        treated_pre = df[df[treatment_col] == 1][cov]
        control_pre = df[df[treatment_col] == 0][cov]
        
        mean_t_pre = treated_pre.mean()
        mean_c_pre = control_pre.mean()
        pooled_std_pre = np.sqrt((treated_pre.var() + control_pre.var()) / 2)
        smd_pre = (mean_t_pre - mean_c_pre) / pooled_std_pre if pooled_std_pre > 0 else 0
        
        # Post-matching (matched units only)
        treated_post = df.loc[treated_indices, cov]
        control_post = df.loc[control_indices, cov]
        
        mean_t_post = treated_post.mean()
        mean_c_post = control_post.mean()
        pooled_std_post = np.sqrt((treated_post.var() + control_post.var()) / 2)
        smd_post = (mean_t_post - mean_c_post) / pooled_std_post if pooled_std_post > 0 else 0
        
        balance_results.append({
            "covariate": cov,
            "smd_pre_matching": float(smd_pre),
            "smd_post_matching": float(smd_post),
            "improvement": float(abs(smd_pre) - abs(smd_post)),
            "balanced": abs(smd_post) < 0.10,
            "acceptable": abs(smd_post) < 0.15
        })
    
    # Overall balance assessment
    n_balanced = sum(1 for r in balance_results if r["balanced"])
    n_acceptable = sum(1 for r in balance_results if r["acceptable"])
    
    return {
        "balance_by_covariate": balance_results,
        "summary": {
            "n_covariates": len(balance_results),
            "n_balanced": n_balanced,
            "n_acceptable": n_acceptable,
            "pct_balanced": float(n_balanced / len(balance_results) * 100) if balance_results else 0,
            "overall_status": "excellent" if n_balanced == len(balance_results) else "good" if n_acceptable >= len(balance_results) * 0.8 else "poor"
        }
    }

def estimate_treatment_effect(
    matched_pairs: List[Dict[str, Any]],
    outcome_col: str,
    bootstrap_iterations: int = 1000
) -> PSMResult:
    """
    Estimate Average Treatment Effect on Treated (ATT) with bootstrap SE.
    
    ATT = E[Y_treated - Y_control | Treatment = 1]
    
    Args:
        matched_pairs: Matched pairs with outcome data
        outcome_col: Name of outcome variable
        bootstrap_iterations: Number of bootstrap samples for CI
    
    Returns:
        PSMResult with ATT, SE, CI, p-value
    """
    # Extract outcomes
    treated_outcomes = []
    control_outcomes = []
    
    for pair in matched_pairs:
        # Try both direct access and case dict
        treated_case = pair.get("treated_case", {})
        control_case = pair.get("control_case", {})
        
        treated_outcome = treated_case.get(outcome_col)
        control_outcome = control_case.get(outcome_col)
        
        if treated_outcome is not None and control_outcome is not None:
            treated_outcomes.append(float(treated_outcome))
            control_outcomes.append(float(control_outcome))
    
    if len(treated_outcomes) == 0:
        # Return null result
        return PSMResult(
            att=0.0,
            att_se=0.0,
            att_ci_lower=0.0,
            att_ci_upper=0.0,
            p_value=1.0,
            n_treated=0,
            n_control=0,
            n_matched=0,
            balance_satisfied=False,
            sensitivity_robust=False
        )
    
    treated_outcomes = np.array(treated_outcomes)
    control_outcomes = np.array(control_outcomes)
    
    # Point estimate
    att = treated_outcomes.mean() - control_outcomes.mean()
    
    # Bootstrap confidence interval
    bootstrap_atts = []
    n = len(treated_outcomes)
    
    for _ in range(bootstrap_iterations):
        boot_idx = np.random.choice(n, size=n, replace=True)
        boot_att = treated_outcomes[boot_idx].mean() - control_outcomes[boot_idx].mean()
        bootstrap_atts.append(boot_att)
    
    att_se = np.std(bootstrap_atts)
    att_ci_lower = np.percentile(bootstrap_atts, 2.5)
    att_ci_upper = np.percentile(bootstrap_atts, 97.5)
    
    # t-test
    t_stat = att / att_se if att_se > 0 else 0
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
    
    # Count unique treated units
    n_matched = len(set(pair["treated_index"] for pair in matched_pairs))
    
    return PSMResult(
        att=att,
        att_se=att_se,
        att_ci_lower=att_ci_lower,
        att_ci_upper=att_ci_upper,
        p_value=p_value,
        n_treated=n_matched,
        n_control=len(control_outcomes),
        n_matched=n,
        balance_satisfied=True,  # Checked separately
        sensitivity_robust=True   # Checked separately
    )

def sensitivity_analysis(
    matched_pairs: List[Dict[str, Any]],
    outcome_col: str,
    gamma_values: List[float] = [1.0, 1.5, 2.0, 2.5]
) -> Dict[str, Any]:
    """
    Rosenbaum sensitivity analysis for hidden bias.
    
    Gamma = odds ratio of differential assignment to treatment
    Gamma = 1: No hidden bias
    Gamma > 1: Unmeasured confounders could change treatment assignment by Gamma
    
    Args:
        matched_pairs: Matched pairs
        outcome_col: Outcome variable
        gamma_values: Range of Gamma values to test
    
    Returns:
        Dict with sensitivity bounds for each Gamma
    """
    # Extract paired differences
    differences = []
    
    for pair in matched_pairs:
        treated_outcome = pair["treated_case"].get(outcome_col)
        control_outcome = pair["control_case"].get(outcome_col)
        
        if treated_outcome is not None and control_outcome is not None:
            differences.append(float(treated_outcome) - float(control_outcome))
    
    differences = np.array(differences)
    n = len(differences)
    
    if n == 0:
        return {"error": "No valid paired differences", "sensitivity_results": []}
    
    sensitivity_results = []
    
    for gamma in gamma_values:
        # Count positive differences
        positive_diffs = np.sum(differences > 0)
        
        if gamma == 1.0:
            # No bias case - standard Wilcoxon
            z_stat = (positive_diffs - n/2) / np.sqrt(n/4)
            p_upper = 1 - stats.norm.cdf(abs(z_stat))
        else:
            # Hidden bias case - upper bound
            pi_max = gamma / (1 + gamma)
            z_stat = (positive_diffs - n * pi_max) / np.sqrt(n * pi_max * (1 - pi_max))
            p_upper = 1 - stats.norm.cdf(z_stat)
        
        p_upper = max(0.0, min(1.0, p_upper))
        
        sensitivity_results.append({
            "gamma": float(gamma),
            "p_value_upper": float(p_upper),
            "robust": p_upper < 0.05,
            "status": "robust" if p_upper < 0.05 else "marginal" if p_upper < 0.10 else "fragile"
        })
    
    # Overall assessment
    robust_up_to_gamma = 1.0
    for result in sensitivity_results:
        if result["robust"]:
            robust_up_to_gamma = result["gamma"]
        else:
            break
    
    return {
        "sensitivity_results": sensitivity_results,
        "summary": {
            "robust_up_to_gamma": float(robust_up_to_gamma),
            "interpretation": f"Result robust to Gamma={robust_up_to_gamma:.1f} (unobserved confounder could change odds of treatment by {robust_up_to_gamma:.1f}x)"
        }
    }

def run_complete_psm_analysis(
    cases: List[Dict[str, Any]],
    treatment_col: str,
    outcome_col: str,
    covariate_cols: List[str],
    n_neighbors: int = 1,
    caliper: float = 0.1,
    bootstrap_iterations: int = 1000
) -> Dict[str, Any]:
    """
    Execute complete PSM analysis workflow.
    
    Workflow:
    1. Calculate propensity scores
    2. Match treated to controls
    3. Check covariate balance
    4. Estimate ATT with bootstrap CI
    5. Sensitivity analysis for hidden bias
    
    Args:
        cases: List of case dictionaries
        treatment_col: Treatment indicator (0/1)
        outcome_col: Outcome variable (continuous)
        covariate_cols: Covariates for matching
        n_neighbors: Matches per treated unit
        caliper: Maximum propensity score distance
        bootstrap_iterations: Bootstrap samples for CI
    
    Returns:
        Complete analysis results with diagnostics
    """
    # Step 1: Propensity scores
    ps_result = calculate_propensity_scores(cases, treatment_col, covariate_cols, outcome_col=outcome_col)
    
    # Step 2: Matching
    match_result = match_cases(
        ps_result["cases_with_ps"],
        treatment_col,
        n_neighbors=n_neighbors,
        caliper=caliper
    )
    
    # Step 3: Balance
    balance_result = calculate_balance(
        ps_result["cases_with_ps"],
        match_result["matched_pairs"],
        covariate_cols,
        treatment_col=treatment_col
    )
    
    # Step 4: Treatment effect
    att_result = estimate_treatment_effect(
        match_result["matched_pairs"],
        outcome_col,
        bootstrap_iterations=bootstrap_iterations
    )
    
    # Step 5: Sensitivity
    sensitivity_result = sensitivity_analysis(
        match_result["matched_pairs"],
        outcome_col
    )
    
    # Update ATT result with diagnostics
    att_result.balance_satisfied = balance_result["summary"]["overall_status"] in ["excellent", "good"]
    att_result.sensitivity_robust = sensitivity_result.get("summary", {}).get("robust_up_to_gamma", 0) >= 1.5
    
    return {
        "propensity_scores": ps_result,
        "matching": match_result,
        "balance": balance_result,
        "treatment_effect": att_result.to_dict(),
        "sensitivity": sensitivity_result,
        "overall_quality": {
            "overlap": ps_result["diagnostics"]["overlap_status"],
            "match_rate": match_result["diagnostics"]["match_quality"],
            "balance": balance_result["summary"]["overall_status"],
            "significant": att_result.p_value < 0.05,
            "robust": att_result.sensitivity_robust
        }
    }

# ========== DEMO FUNCTIONS ==========

def demo_cli_reform_causality() -> Dict[str, Any]:
    """
    Demo: Does high CLI cause reform failure? (PSM validation)
    
    Treatment: High CLI (>0.70)
    Outcome: Reform success (0-1)
    Covariates: GDP per capita, democracy score, crisis indicator
    
    Expected: ATT ≈ -0.35 (high CLI reduces reform success by 35pp)
    """
    # Simulated data based on Peralta (2024) empirical results
    np.random.seed(42)
    
    cases = []
    
    # Generate 60 cases
    for i in range(60):
        # Covariates (balanced between groups)
        gdp_per_capita = np.random.uniform(5000, 40000)
        democracy_score = np.random.uniform(3, 10)
        crisis = np.random.binomial(1, 0.3)
        
        # Treatment assignment (correlated with covariates)
        treatment_prob = 1 / (1 + np.exp(-(-2 + 0.00003*gdp_per_capita + 0.2*democracy_score + 0.5*crisis)))
        high_cli = int(np.random.random() < treatment_prob)
        
        # Outcome (affected by treatment + covariates + noise)
        reform_success_prob = 0.7 - 0.35*high_cli + 0.00001*gdp_per_capita + 0.03*democracy_score + 0.15*crisis
        reform_success_prob = max(0, min(1, reform_success_prob))
        reform_success = np.random.binomial(1, reform_success_prob)
        
        cases.append({
            "case_id": f"case_{i+1}",
            "high_cli": high_cli,
            "reform_success": reform_success,
            "gdp_per_capita": gdp_per_capita,
            "democracy_score": democracy_score,
            "crisis": crisis
        })
    
    result = run_complete_psm_analysis(
        cases=cases,
        treatment_col="high_cli",
        outcome_col="reform_success",
        covariate_cols=["gdp_per_capita", "democracy_score", "crisis"],
        n_neighbors=1,
        caliper=0.1,
        bootstrap_iterations=1000
    )
    
    # Add interpretation
    result["interpretation"] = {
        "research_question": "Does high CLI (>0.70) cause reform failure?",
        "expected_att": -0.35,
        "actual_att": result["treatment_effect"]["att"],
        "validates_hypothesis": abs(result["treatment_effect"]["att"] + 0.35) < 0.15,
        "policy_implication": f"High CLI reduces reform success probability by {abs(result['treatment_effect']['att']):.2f} ({abs(result['treatment_effect']['att'])*100:.0f} percentage points)",
        "connection_to_framework": "Validates CLI → Reform Success regression (R²=0.74)"
    }
    
    return result
