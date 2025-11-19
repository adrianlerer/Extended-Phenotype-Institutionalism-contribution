"""
Bootstrap Tools for MCP Server
Statistical validation via bootstrap resampling for CLI/H/V metrics

This tool enables:
1. Bootstrap confidence intervals (non-parametric) for any statistic
2. Hypothesis testing via bootstrap p-values
3. Stability assessment across N=1000 iterations
4. Bias-corrected and accelerated (BCa) confidence intervals
5. Integration with CLI/H/V/LEI metrics for robustness validation

Theoretical Foundation:
- Efron (1979): Bootstrap methods for standard errors and confidence intervals
- DiCiccio & Efron (1996): Bootstrap confidence intervals (BCa method)
- Davison & Hinkley (1997): Bootstrap methods and their application
- Peralta (2024): Application to constitutional metrics validation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from scipy import stats

# Import existing bootstrap implementation
from code.bootstrap import BootstrapValidator, calculate_bootstrap_ci, bootstrap_hypothesis_test

@dataclass
class BootstrapResult:
    """Bootstrap validation result"""
    point_estimate: float
    bootstrap_mean: float
    bootstrap_std: float
    ci_lower: float
    ci_upper: float
    bias: float
    n_iterations: int
    confidence_level: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "point_estimate": float(self.point_estimate),
            "bootstrap_mean": float(self.bootstrap_mean),
            "bootstrap_std": float(self.bootstrap_std),
            "ci_95": [float(self.ci_lower), float(self.ci_upper)],
            "bias": float(self.bias),
            "bias_percentage": float((self.bias / self.point_estimate * 100) if self.point_estimate != 0 else 0),
            "n_iterations": self.n_iterations,
            "confidence_level": float(self.confidence_level),
            "stable": abs(self.bias / self.bootstrap_std) < 0.25 if self.bootstrap_std > 0 else True
        }

def bootstrap_statistic(
    data: List[float],
    statistic_func: Callable[[np.ndarray], float],
    n_iterations: int = 1000,
    confidence_level: float = 0.95,
    random_state: Optional[int] = 42
) -> BootstrapResult:
    """
    Calculate bootstrap confidence interval for any statistic.
    
    Bootstrap Procedure (Efron 1979):
    1. Resample data with replacement N times
    2. Calculate statistic on each resample
    3. Estimate CI from bootstrap distribution
    
    Args:
        data: Observed data points
        statistic_func: Function to calculate statistic (e.g., np.mean, np.median)
        n_iterations: Number of bootstrap samples
        confidence_level: CI level (default 0.95 for 95% CI)
        random_state: Seed for reproducibility
    
    Returns:
        BootstrapResult with CI and diagnostics
    """
    np.random.seed(random_state)
    
    data_array = np.array(data)
    n = len(data_array)
    
    # Original statistic
    point_estimate = statistic_func(data_array)
    
    # Bootstrap resamples
    bootstrap_estimates = []
    for _ in range(n_iterations):
        bootstrap_sample = np.random.choice(data_array, size=n, replace=True)
        bootstrap_stat = statistic_func(bootstrap_sample)
        bootstrap_estimates.append(bootstrap_stat)
    
    bootstrap_array = np.array(bootstrap_estimates)
    
    # Statistics
    bootstrap_mean = np.mean(bootstrap_array)
    bootstrap_std = np.std(bootstrap_array)
    bias = bootstrap_mean - point_estimate
    
    # Confidence interval (percentile method)
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_array, (alpha/2) * 100)
    ci_upper = np.percentile(bootstrap_array, (1 - alpha/2) * 100)
    
    return BootstrapResult(
        point_estimate=point_estimate,
        bootstrap_mean=bootstrap_mean,
        bootstrap_std=bootstrap_std,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        bias=bias,
        n_iterations=n_iterations,
        confidence_level=confidence_level
    )

def bootstrap_correlation(
    x: List[float],
    y: List[float],
    n_iterations: int = 1000,
    confidence_level: float = 0.95,
    random_state: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Bootstrap confidence interval for correlation coefficient.
    
    Used to validate CLI ↔ Reform Success correlation (R²=0.74).
    
    Args:
        x: First variable (e.g., CLI scores)
        y: Second variable (e.g., Reform success rates)
        n_iterations: Bootstrap iterations
        confidence_level: CI level
        random_state: Random seed
    
    Returns:
        Dict with correlation, CI, and significance test
    """
    np.random.seed(random_state)
    
    x_array = np.array(x)
    y_array = np.array(y)
    n = len(x_array)
    
    # Original correlation
    original_corr, original_p = stats.pearsonr(x_array, y_array)
    
    # Bootstrap
    bootstrap_corrs = []
    for _ in range(n_iterations):
        indices = np.random.choice(n, size=n, replace=True)
        boot_x = x_array[indices]
        boot_y = y_array[indices]
        boot_corr, _ = stats.pearsonr(boot_x, boot_y)
        bootstrap_corrs.append(boot_corr)
    
    bootstrap_array = np.array(bootstrap_corrs)
    
    # Statistics
    bootstrap_mean = np.mean(bootstrap_array)
    bootstrap_std = np.std(bootstrap_array)
    
    # CI
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_array, (alpha/2) * 100)
    ci_upper = np.percentile(bootstrap_array, (1 - alpha/2) * 100)
    
    # Bootstrap p-value (test H0: ρ = 0)
    bootstrap_p = np.sum(np.abs(bootstrap_array) <= np.abs(original_corr)) / n_iterations
    
    return {
        "correlation": float(original_corr),
        "r_squared": float(original_corr ** 2),
        "parametric_p_value": float(original_p),
        "bootstrap_mean_correlation": float(bootstrap_mean),
        "bootstrap_std": float(bootstrap_std),
        "ci_95": [float(ci_lower), float(ci_upper)],
        "bootstrap_p_value": float(bootstrap_p),
        "significant": ci_lower > 0 or ci_upper < 0,  # CI excludes 0
        "stable": abs(bootstrap_mean - original_corr) < 0.05,
        "n_iterations": n_iterations
    }

def bootstrap_regression_coefficient(
    X: List[List[float]],
    y: List[float],
    coefficient_index: int = 0,
    n_iterations: int = 1000,
    confidence_level: float = 0.95,
    random_state: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Bootstrap CI for regression coefficient.
    
    Validates: Reform_Success = 0.92 - 0.89 × CLI
    
    Args:
        X: Predictors (can be multivariate)
        y: Outcome variable
        coefficient_index: Which coefficient to analyze (0=intercept, 1+=predictors)
        n_iterations: Bootstrap iterations
        confidence_level: CI level
        random_state: Random seed
    
    Returns:
        Dict with coefficient, CI, and stability metrics
    """
    np.random.seed(random_state)
    
    X_array = np.array(X)
    y_array = np.array(y)
    n = len(y_array)
    
    # Add intercept if not present
    if X_array.ndim == 1:
        X_array = X_array.reshape(-1, 1)
    
    X_with_intercept = np.column_stack([np.ones(n), X_array])
    
    # Original regression
    original_coefs, _, _, _ = np.linalg.lstsq(X_with_intercept, y_array, rcond=None)
    original_coef = original_coefs[coefficient_index]
    
    # Bootstrap
    bootstrap_coefs = []
    for _ in range(n_iterations):
        indices = np.random.choice(n, size=n, replace=True)
        boot_X = X_with_intercept[indices]
        boot_y = y_array[indices]
        
        try:
            boot_coefs, _, _, _ = np.linalg.lstsq(boot_X, boot_y, rcond=None)
            bootstrap_coefs.append(boot_coefs[coefficient_index])
        except:
            continue
    
    bootstrap_array = np.array(bootstrap_coefs)
    
    # Statistics
    bootstrap_mean = np.mean(bootstrap_array)
    bootstrap_std = np.std(bootstrap_array)
    
    # CI
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_array, (alpha/2) * 100)
    ci_upper = np.percentile(bootstrap_array, (1 - alpha/2) * 100)
    
    # Z-score for significance
    z_score = original_coef / bootstrap_std if bootstrap_std > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    return {
        "coefficient": float(original_coef),
        "bootstrap_mean": float(bootstrap_mean),
        "bootstrap_std": float(bootstrap_std),
        "ci_95": [float(ci_lower), float(ci_upper)],
        "z_score": float(z_score),
        "p_value": float(p_value),
        "significant": p_value < 0.05,
        "bias": float(bootstrap_mean - original_coef),
        "stable": abs(bootstrap_mean - original_coef) / bootstrap_std < 0.25 if bootstrap_std > 0 else True,
        "n_iterations": len(bootstrap_coefs),
        "success_rate": len(bootstrap_coefs) / n_iterations
    }

def bootstrap_h_v_ratio(
    h_values: List[float],
    v_values: List[float],
    n_iterations: int = 1000,
    phi: float = 1.618,
    confidence_level: float = 0.95,
    random_state: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Bootstrap validation of H/V ratio convergence to φ.
    
    Tests whether H/V → φ (golden ratio) is statistically robust.
    
    Args:
        h_values: Heredity measurements
        v_values: Variation measurements
        n_iterations: Bootstrap iterations
        phi: Target golden ratio
        confidence_level: CI level
        random_state: Random seed
    
    Returns:
        Dict with H/V ratio, distance to φ, and CI
    """
    np.random.seed(random_state)
    
    h_array = np.array(h_values)
    v_array = np.array(v_values)
    n = len(h_array)
    
    # Original H/V ratio
    original_hv = np.mean(h_array) / np.mean(v_array)
    original_distance = abs(original_hv - phi)
    
    # Bootstrap
    bootstrap_hvs = []
    bootstrap_distances = []
    
    for _ in range(n_iterations):
        indices = np.random.choice(n, size=n, replace=True)
        boot_h = h_array[indices]
        boot_v = v_array[indices]
        
        boot_hv = np.mean(boot_h) / np.mean(boot_v)
        boot_distance = abs(boot_hv - phi)
        
        bootstrap_hvs.append(boot_hv)
        bootstrap_distances.append(boot_distance)
    
    hv_array = np.array(bootstrap_hvs)
    dist_array = np.array(bootstrap_distances)
    
    # Statistics
    bootstrap_mean_hv = np.mean(hv_array)
    bootstrap_std_hv = np.std(hv_array)
    
    # CI for H/V ratio
    alpha = 1 - confidence_level
    ci_lower_hv = np.percentile(hv_array, (alpha/2) * 100)
    ci_upper_hv = np.percentile(hv_array, (1 - alpha/2) * 100)
    
    # CI for distance to φ
    ci_lower_dist = np.percentile(dist_array, (alpha/2) * 100)
    ci_upper_dist = np.percentile(dist_array, (1 - alpha/2) * 100)
    
    # Test: Is H/V significantly different from φ?
    contains_phi = ci_lower_hv <= phi <= ci_upper_hv
    
    return {
        "h_v_ratio": float(original_hv),
        "distance_to_phi": float(original_distance),
        "bootstrap_mean_hv": float(bootstrap_mean_hv),
        "bootstrap_std_hv": float(bootstrap_std_hv),
        "ci_95_hv": [float(ci_lower_hv), float(ci_upper_hv)],
        "ci_95_distance": [float(ci_lower_dist), float(ci_upper_dist)],
        "contains_phi": contains_phi,
        "converging_to_phi": original_distance < 0.2 and ci_upper_dist < 0.3,
        "stable": abs(bootstrap_mean_hv - original_hv) < 0.1,
        "n_iterations": n_iterations
    }

def bootstrap_cli_components(
    case_data: List[Dict[str, float]],
    component_names: List[str] = ["TV", "JA", "TH", "PW", "AD"],
    n_iterations: int = 1000,
    confidence_level: float = 0.95,
    random_state: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Bootstrap validation of CLI component stability.
    
    CLI = 0.25×TV + 0.25×JA + 0.20×TH + 0.15×PW + 0.15×AD
    
    Args:
        case_data: List of cases with CLI components
        component_names: CLI components to validate
        n_iterations: Bootstrap iterations
        confidence_level: CI level
        random_state: Random seed
    
    Returns:
        Dict with component CIs and overall CLI stability
    """
    np.random.seed(random_state)
    
    # Convert to arrays
    n_cases = len(case_data)
    component_arrays = {comp: np.array([case.get(comp, 0.0) for case in case_data]) for comp in component_names}
    
    # Original CLI calculation
    weights = {"TV": 0.25, "JA": 0.25, "TH": 0.20, "PW": 0.15, "AD": 0.15}
    
    def calculate_cli(components: Dict[str, np.ndarray]) -> float:
        return sum(weights.get(comp, 0) * np.mean(values) for comp, values in components.items())
    
    original_cli = calculate_cli(component_arrays)
    original_components = {comp: np.mean(arr) for comp, arr in component_arrays.items()}
    
    # Bootstrap
    bootstrap_clis = []
    bootstrap_components = {comp: [] for comp in component_names}
    
    for _ in range(n_iterations):
        indices = np.random.choice(n_cases, size=n_cases, replace=True)
        boot_components = {comp: arr[indices] for comp, arr in component_arrays.items()}
        
        boot_cli = calculate_cli(boot_components)
        bootstrap_clis.append(boot_cli)
        
        for comp in component_names:
            bootstrap_components[comp].append(np.mean(boot_components[comp]))
    
    cli_array = np.array(bootstrap_clis)
    
    # CLI statistics
    cli_mean = np.mean(cli_array)
    cli_std = np.std(cli_array)
    
    alpha = 1 - confidence_level
    cli_ci_lower = np.percentile(cli_array, (alpha/2) * 100)
    cli_ci_upper = np.percentile(cli_array, (1 - alpha/2) * 100)
    
    # Component statistics
    component_results = {}
    for comp in component_names:
        comp_array = np.array(bootstrap_components[comp])
        comp_mean = np.mean(comp_array)
        comp_std = np.std(comp_array)
        comp_ci_lower = np.percentile(comp_array, (alpha/2) * 100)
        comp_ci_upper = np.percentile(comp_array, (1 - alpha/2) * 100)
        
        component_results[comp] = {
            "original": float(original_components[comp]),
            "bootstrap_mean": float(comp_mean),
            "bootstrap_std": float(comp_std),
            "ci_95": [float(comp_ci_lower), float(comp_ci_upper)],
            "stable": abs(comp_mean - original_components[comp]) < 0.05
        }
    
    return {
        "cli": {
            "original": float(original_cli),
            "bootstrap_mean": float(cli_mean),
            "bootstrap_std": float(cli_std),
            "ci_95": [float(cli_ci_lower), float(cli_ci_upper)],
            "stable": abs(cli_mean - original_cli) / cli_std < 0.25 if cli_std > 0 else True
        },
        "components": component_results,
        "n_iterations": n_iterations,
        "all_components_stable": all(comp["stable"] for comp in component_results.values())
    }

# ========== DEMO FUNCTIONS ==========

def demo_cli_reform_correlation_validation() -> Dict[str, Any]:
    """
    Demo: Validate CLI ↔ Reform Success correlation with bootstrap.
    
    Expected: r ≈ -0.86, R² ≈ 0.74, robust across 1000 iterations
    """
    np.random.seed(42)
    
    # Simulated data based on Peralta (2024) empirical results
    n_cases = 50
    
    # Generate CLI scores
    cli_scores = np.random.uniform(0.2, 0.9, n_cases)
    
    # Generate reform success (negatively correlated with CLI + noise)
    reform_success = 0.92 - 0.89 * cli_scores + np.random.normal(0, 0.10, n_cases)
    reform_success = np.clip(reform_success, 0, 1)
    
    result = bootstrap_correlation(
        x=cli_scores.tolist(),
        y=reform_success.tolist(),
        n_iterations=1000,
        confidence_level=0.95
    )
    
    # Add interpretation
    result["interpretation"] = {
        "research_question": "Is CLI → Reform Success correlation robust?",
        "expected_r": -0.86,
        "expected_r_squared": 0.74,
        "actual_r": result["correlation"],
        "actual_r_squared": result["r_squared"],
        "validates_framework": abs(result["correlation"] + 0.86) < 0.15,
        "conclusion": f"Correlation is {'stable and significant' if result['stable'] and result['significant'] else 'unstable or non-significant'}"
    }
    
    return result

def demo_hv_phi_convergence_validation() -> Dict[str, Any]:
    """
    Demo: Validate H/V → φ convergence hypothesis with bootstrap.
    
    Expected: Systems near φ have higher reform success
    """
    np.random.seed(42)
    
    # Generate 30 constitutional systems with varying H/V ratios
    n_systems = 30
    
    # H/V ratios clustered around φ = 1.618
    phi = 1.618
    h_values = np.random.normal(phi * 5, 1.5, n_systems)  # Simulated H
    v_values = h_values / (phi + np.random.normal(0, 0.3, n_systems))  # V such that H/V ≈ φ
    
    result = bootstrap_h_v_ratio(
        h_values=h_values.tolist(),
        v_values=v_values.tolist(),
        n_iterations=1000,
        phi=phi
    )
    
    # Add interpretation
    result["interpretation"] = {
        "hypothesis": "H/V ratios converge to φ (golden ratio) in optimal systems",
        "golden_ratio_phi": phi,
        "observed_hv": result["h_v_ratio"],
        "distance_to_phi": result["distance_to_phi"],
        "contains_phi": result["contains_phi"],
        "conclusion": f"H/V ratio is {'converging to φ' if result['converging_to_phi'] else 'not near φ'}, CI {'contains' if result['contains_phi'] else 'excludes'} φ"
    }
    
    return result
