"""
Iusmorfos Tools for MCP Server
Cross-jurisdictional transplant prediction using WEIRD/No-WEIRD distance metrics

This tool enables:
1. Transplant success prediction based on cultural/institutional distance
2. WEIRD vs No-WEIRD classification and adaptive coefficient calculation
3. Implementation gap analysis (passage vs implementation)
4. Cross-tool integration (CLI, RootFinder, Memespace)
5. Williamson NEI level mapping

Theoretical Foundation:
- Henrich et al. (2010): WEIRD populations (Western, Educated, Industrialized, Rich, Democratic)
- Williamson (2000): 4-level NEI framework
- Peralta (2024): H/V-CLI-LEI system + transplant prediction
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Load cultural data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "iusmorfos_v6"

def load_json_data(filename: str) -> Dict:
    """Load JSON data file from iusmorfos_v6 directory"""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load cultural metrics at module level
ADAPTIVE_COEFFICIENTS = load_json_data("adaptive_coefficients.json")
CULTURAL_METRICS = load_json_data("cultural_metrics.json")

# WEIRD classification thresholds (from Henrich et al. 2010 + WJP 2023)
WEIRD_THRESHOLDS = {
    "rule_of_law_min": 0.75,
    "individualism_min": 60,
    "institutional_quality_min": 1.0,
    "adaptive_coefficient_max": -0.10  # Less negative = higher fidelity
}

@dataclass
class JurisdictionProfile:
    """Cultural/institutional profile for a jurisdiction"""
    jurisdiction: str
    is_weird: bool
    adaptive_coefficient: float
    rule_of_law_index: float
    institutional_quality: float
    individualism_score: int
    informal_institutions_strength: float
    williamson_level_dominant: int  # 1=embeddedness, 2=institutions, 3=governance, 4=markets
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "jurisdiction": self.jurisdiction,
            "is_weird": self.is_weird,
            "adaptive_coefficient": self.adaptive_coefficient,
            "cultural_metrics": {
                "rule_of_law_index": self.rule_of_law_index,
                "institutional_quality": self.institutional_quality,
                "individualism_score": self.individualism_score,
                "informal_institutions_strength": self.informal_institutions_strength
            },
            "williamson_level": self.williamson_level_dominant,
            "classification": "WEIRD" if self.is_weird else "No-WEIRD"
        }

def classify_jurisdiction(jurisdiction: str) -> JurisdictionProfile:
    """
    Classify jurisdiction as WEIRD or No-WEIRD using cultural metrics.
    
    WEIRD criteria (Henrich et al. 2010):
    - Rule of Law Index ≥ 0.75
    - Individualism Score ≥ 60
    - Institutional Quality ≥ 1.0
    - Adaptive Coefficient ≥ -0.10 (high fidelity)
    
    Args:
        jurisdiction: Jurisdiction name (normalized)
    
    Returns:
        JurisdictionProfile with complete classification
    """
    jurisdiction_key = jurisdiction.lower().replace(" ", "_")
    
    # Get adaptive coefficient (default = -0.25 for unknown jurisdictions)
    adaptive_coef = ADAPTIVE_COEFFICIENTS.get(
        jurisdiction_key, 
        ADAPTIVE_COEFFICIENTS.get("default", -0.25)
    )
    
    # Get cultural metrics
    metrics = CULTURAL_METRICS.get(jurisdiction_key, {})
    cultural_data = metrics.get("cultural_metrics", {})
    
    # Extract metrics with defaults
    rule_of_law = cultural_data.get("rule_of_law_index", 0.5)
    inst_quality = cultural_data.get("institutional_quality", 0.0)
    individualism = cultural_data.get("individualism_score", 40)
    informal_strength = cultural_data.get("informal_institutions_strength", 0.5)
    
    # WEIRD classification (must meet ALL criteria)
    is_weird = (
        rule_of_law >= WEIRD_THRESHOLDS["rule_of_law_min"] and
        individualism >= WEIRD_THRESHOLDS["individualism_min"] and
        inst_quality >= WEIRD_THRESHOLDS["institutional_quality_min"] and
        adaptive_coef >= WEIRD_THRESHOLDS["adaptive_coefficient_max"]
    )
    
    # Determine dominant Williamson level
    # Level 1 (embeddedness): High informal institutions + low rule of law
    # Level 2 (institutions): High rule of law + moderate formal structures
    # Level 3 (governance): High institutional quality + adaptive
    # Level 4 (markets): Low transaction costs + high individualism
    
    williamson_scores = {
        1: informal_strength * (1 - rule_of_law),  # Embeddedness
        2: rule_of_law * (1 + abs(adaptive_coef)),  # Institutional environment
        3: inst_quality if inst_quality > 0 else 0,  # Governance
        4: individualism / 100.0  # Resource allocation (market-based)
    }
    
    dominant_level = max(williamson_scores, key=williamson_scores.get)
    
    return JurisdictionProfile(
        jurisdiction=jurisdiction,
        is_weird=is_weird,
        adaptive_coefficient=adaptive_coef,
        rule_of_law_index=rule_of_law,
        institutional_quality=inst_quality,
        individualism_score=individualism,
        informal_institutions_strength=informal_strength,
        williamson_level_dominant=dominant_level
    )

def calculate_cultural_distance(
    source: str,
    target: str
) -> Dict[str, Any]:
    """
    Calculate cultural/institutional distance between jurisdictions.
    
    Uses Euclidean distance in normalized metric space:
    - Rule of Law Index [0,1]
    - Institutional Quality (normalized to [0,1])
    - Individualism Score (normalized to [0,1])
    - Adaptive Coefficient distance
    
    Args:
        source: Source jurisdiction
        target: Target jurisdiction
    
    Returns:
        Dict with distance metrics and interpretation
    """
    source_profile = classify_jurisdiction(source)
    target_profile = classify_jurisdiction(target)
    
    # Normalize institutional quality to [0,1]
    # Range is approximately [-2, +2] in World Bank data
    def normalize_inst_quality(x: float) -> float:
        return (x + 2.0) / 4.0
    
    # Normalize individualism to [0,1]
    def normalize_individualism(x: int) -> float:
        return x / 100.0
    
    # Normalize adaptive coefficient to [0,1]
    # Range is [-0.50, -0.02] → invert so higher = better
    def normalize_adaptive(x: float) -> float:
        return (x + 0.50) / 0.48
    
    # Calculate component distances
    distance_components = {
        "rule_of_law": abs(
            source_profile.rule_of_law_index - target_profile.rule_of_law_index
        ),
        "institutional_quality": abs(
            normalize_inst_quality(source_profile.institutional_quality) -
            normalize_inst_quality(target_profile.institutional_quality)
        ),
        "individualism": abs(
            normalize_individualism(source_profile.individualism_score) -
            normalize_individualism(target_profile.individualism_score)
        ),
        "adaptive_coefficient": abs(
            normalize_adaptive(source_profile.adaptive_coefficient) -
            normalize_adaptive(target_profile.adaptive_coefficient)
        ),
        "informal_institutions": abs(
            source_profile.informal_institutions_strength -
            target_profile.informal_institutions_strength
        )
    }
    
    # Euclidean distance (weighted)
    weights = {
        "rule_of_law": 0.30,
        "institutional_quality": 0.25,
        "individualism": 0.15,
        "adaptive_coefficient": 0.20,
        "informal_institutions": 0.10
    }
    
    euclidean_distance = np.sqrt(
        sum(weights[k] * (v ** 2) for k, v in distance_components.items())
    )
    
    # WEIRD/No-WEIRD crossing penalty
    weird_penalty = 0.0
    if source_profile.is_weird != target_profile.is_weird:
        weird_penalty = 0.15  # 15% additional gap for WEIRD ↔ No-WEIRD
    
    total_distance = min(1.0, euclidean_distance + weird_penalty)
    
    # Williamson level compatibility
    williamson_compatible = (
        source_profile.williamson_level_dominant == 
        target_profile.williamson_level_dominant
    )
    
    return {
        "source": source,
        "target": target,
        "source_profile": source_profile.to_dict(),
        "target_profile": target_profile.to_dict(),
        "distance_components": distance_components,
        "euclidean_distance": float(euclidean_distance),
        "weird_crossing": source_profile.is_weird != target_profile.is_weird,
        "weird_penalty": float(weird_penalty),
        "total_distance": float(total_distance),
        "williamson_compatible": williamson_compatible,
        "williamson_levels": {
            "source": source_profile.williamson_level_dominant,
            "target": target_profile.williamson_level_dominant
        }
    }

def predict_transplant_success(
    concept: str,
    source: str,
    target: str,
    cli_source: Optional[float] = None,
    cli_target: Optional[float] = None,
    h_v_ratio_source: Optional[float] = None,
    h_v_ratio_target: Optional[float] = None
) -> Dict[str, Any]:
    """
    Predict transplant success using cultural distance + CLI integration.
    
    Prediction model (Peralta 2024):
    predicted_gap = α × cultural_distance + β × CLI_diff + γ × H/V_distance
    
    Where:
    - α = 0.45 (cultural distance weight)
    - β = 0.35 (CLI differential weight)
    - γ = 0.20 (H/V distance weight)
    
    Implementation Gap = predicted_gap
    Passage Probability = 1 - (predicted_gap × 1.2)  # Passage easier than implementation
    
    Args:
        concept: Legal concept/institution being transplanted
        source: Source jurisdiction
        target: Target jurisdiction
        cli_source: CLI score for source (optional)
        cli_target: CLI score for target (optional)
        h_v_ratio_source: H/V ratio for source (optional)
        h_v_ratio_target: H/V ratio for target (optional)
    
    Returns:
        Comprehensive prediction with gap, probability, recommendations
    """
    # Calculate cultural distance
    distance_result = calculate_cultural_distance(source, target)
    cultural_distance = distance_result["total_distance"]
    
    # CLI differential (if provided)
    cli_diff = 0.0
    if cli_source is not None and cli_target is not None:
        # Higher target CLI = more lock-in = harder transplant
        # Directional: positive diff = target more locked than source
        cli_diff = abs(cli_target - cli_source)
    
    # H/V distance (if provided)
    hv_distance = 0.0
    phi = 1.618
    if h_v_ratio_source is not None and h_v_ratio_target is not None:
        # Distance from optimal (φ) in both jurisdictions
        source_phi_dist = abs(h_v_ratio_source - phi)
        target_phi_dist = abs(h_v_ratio_target - phi)
        hv_distance = abs(target_phi_dist - source_phi_dist)
    
    # Prediction model weights
    alpha = 0.45  # Cultural distance
    beta = 0.35   # CLI differential
    gamma = 0.20  # H/V distance
    
    # Predicted implementation gap
    predicted_gap = (
        alpha * cultural_distance +
        beta * cli_diff +
        gamma * hv_distance
    )
    
    # Normalize to [0, 1]
    predicted_gap = min(1.0, predicted_gap)
    
    # Passage probability (passage easier than implementation)
    passage_probability = max(0.0, 1 - (predicted_gap * 1.2))
    
    # Implementation success probability
    implementation_probability = max(0.0, 1 - predicted_gap)
    
    # Risk assessment
    risk_factors = []
    
    if distance_result["weird_crossing"]:
        risk_factors.append({
            "type": "WEIRD_crossing",
            "severity": "high",
            "description": f"WEIRD ↔ No-WEIRD transplant incurs {distance_result['weird_penalty']:.1%} penalty",
            "impact": distance_result["weird_penalty"]
        })
    
    if cli_diff > 0.20:
        risk_factors.append({
            "type": "CLI_differential",
            "severity": "high",
            "description": f"CLI difference = {cli_diff:.2f} (threshold: 0.20)",
            "impact": beta * cli_diff
        })
    
    if not distance_result["williamson_compatible"]:
        risk_factors.append({
            "type": "williamson_mismatch",
            "severity": "medium",
            "description": f"Williamson level mismatch: {distance_result['williamson_levels']['source']} → {distance_result['williamson_levels']['target']}",
            "impact": 0.10
        })
    
    if distance_result["target_profile"]["cultural_metrics"]["informal_institutions_strength"] > 0.65:
        risk_factors.append({
            "type": "strong_informal_institutions",
            "severity": "medium",
            "description": f"Target has strong informal institutions ({distance_result['target_profile']['cultural_metrics']['informal_institutions_strength']:.2f})",
            "impact": 0.08
        })
    
    # Overall risk classification
    high_risk_count = sum(1 for r in risk_factors if r["severity"] == "high")
    if predicted_gap > 0.60 or high_risk_count >= 2:
        overall_risk = "critical"
    elif predicted_gap > 0.40 or high_risk_count >= 1:
        overall_risk = "high"
    elif predicted_gap > 0.25:
        overall_risk = "medium"
    else:
        overall_risk = "low"
    
    # Generate recommendations
    recommendations = []
    
    if distance_result["weird_crossing"]:
        recommendations.append({
            "action": "Incremental adaptation strategy",
            "priority": "critical",
            "rationale": "WEIRD ↔ No-WEIRD transplants require substantial local adaptation",
            "next_steps": [
                "Pilot program in limited jurisdiction",
                "Engage local stakeholders early",
                "Allow 2-3 year transition period",
                "Monitor informal institution responses"
            ]
        })
    
    if cli_target is not None and cli_target > 0.70:
        recommendations.append({
            "action": "Address constitutional lock-in",
            "priority": "high",
            "rationale": f"Target CLI = {cli_target:.2f} indicates high institutional rigidity",
            "next_steps": [
                "Identify veto players (use JurisRank)",
                "Build coalition with judiciary",
                "Consider constitutional amendment pathway",
                "Use crisis windows (Williamson Level 2)"
            ]
        })
    
    if hv_distance > 0.5:
        recommendations.append({
            "action": "Balance H/V ratio",
            "priority": "high",
            "rationale": f"H/V distance = {hv_distance:.2f} suggests institutional incompatibility",
            "next_steps": [
                "Analyze target's H/V components",
                "Adjust transplant rigidity/flexibility",
                "Test with Fibonacci analyzer for φ-convergence"
            ]
        })
    
    recommendations.append({
        "action": "Validate with PSM",
        "priority": "medium",
        "rationale": "Propensity Score Matching can validate causal claims",
        "next_steps": [
            "Identify similar transplants (use RootFinder)",
            "Match on covariates (CLI, H/V, cultural distance)",
            "Estimate Average Treatment Effect (ATE)"
        ]
    })
    
    return {
        "concept": concept,
        "source": source,
        "target": target,
        
        # Core predictions
        "predicted_gap": float(predicted_gap),
        "passage_probability": float(passage_probability),
        "implementation_probability": float(implementation_probability),
        
        # Model components
        "prediction_components": {
            "cultural_distance": float(cultural_distance),
            "cultural_weight": alpha,
            "cli_differential": float(cli_diff),
            "cli_weight": beta,
            "hv_distance": float(hv_distance),
            "hv_weight": gamma
        },
        
        # Cultural analysis
        "cultural_distance_details": distance_result,
        
        # Risk assessment
        "risk_factors": risk_factors,
        "overall_risk": overall_risk,
        
        # Recommendations
        "recommendations": recommendations,
        
        # Confidence
        "confidence_level": "high" if (cli_source is not None and h_v_ratio_source is not None) else "medium",
        "missing_data": {
            "cli_scores": cli_source is None or cli_target is None,
            "hv_ratios": h_v_ratio_source is None or h_v_ratio_target is None
        }
    }

def batch_compare_targets(
    concept: str,
    source: str,
    targets: List[str],
    cli_scores: Optional[Dict[str, float]] = None,
    h_v_ratios: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Compare multiple target jurisdictions for transplant suitability.
    
    Args:
        concept: Legal concept
        source: Source jurisdiction
        targets: List of target jurisdictions
        cli_scores: Dict mapping jurisdiction → CLI score (optional)
        h_v_ratios: Dict mapping jurisdiction → H/V ratio (optional)
    
    Returns:
        Ranked comparison of all targets
    """
    results = []
    
    cli_scores = cli_scores or {}
    h_v_ratios = h_v_ratios or {}
    
    for target in targets:
        prediction = predict_transplant_success(
            concept=concept,
            source=source,
            target=target,
            cli_source=cli_scores.get(source),
            cli_target=cli_scores.get(target),
            h_v_ratio_source=h_v_ratios.get(source),
            h_v_ratio_target=h_v_ratios.get(target)
        )
        
        results.append({
            "target": target,
            "predicted_gap": prediction["predicted_gap"],
            "passage_probability": prediction["passage_probability"],
            "implementation_probability": prediction["implementation_probability"],
            "overall_risk": prediction["overall_risk"],
            "is_weird": prediction["cultural_distance_details"]["target_profile"]["is_weird"],
            "full_prediction": prediction
        })
    
    # Sort by implementation probability (higher = better)
    results.sort(key=lambda x: x["implementation_probability"], reverse=True)
    
    # Add rankings
    for i, result in enumerate(results):
        result["rank"] = i + 1
    
    return {
        "concept": concept,
        "source": source,
        "targets_analyzed": len(targets),
        "ranked_results": results,
        "best_target": results[0]["target"] if results else None,
        "worst_target": results[-1]["target"] if results else None,
        "weird_targets": [r["target"] for r in results if r["is_weird"]],
        "no_weird_targets": [r["target"] for r in results if not r["is_weird"]]
    }

# ========== DEMO FUNCTIONS ==========

def demo_argentina_brazil_labor_flexibility() -> Dict[str, Any]:
    """
    Demo: Predict Brazil → Argentina labor flexibility transplant.
    
    Context:
    - Brazil: 2017 labor reform (Temer), moderate success
    - Argentina: 2024 labor reform attempts (Milei), strong resistance
    - Both No-WEIRD, but different institutional lock-in levels
    """
    # Hypothetical CLI scores (would come from CLI calculator)
    cli_scores = {
        "brazil": 0.58,  # Moderate lock-in
        "argentina": 0.87  # Very high lock-in (post-1994 + Vizzoti)
    }
    
    # Hypothetical H/V ratios
    h_v_ratios = {
        "brazil": 1.85,  # Slightly rigid
        "argentina": 2.45  # Very rigid (high H)
    }
    
    result = predict_transplant_success(
        concept="Labor Flexibility (Brazil 2017 model)",
        source="brazil",
        target="argentina",
        cli_source=cli_scores["brazil"],
        cli_target=cli_scores["argentina"],
        h_v_ratio_source=h_v_ratios["brazil"],
        h_v_ratio_target=h_v_ratios["argentina"]
    )
    
    # Add interpretation
    result["interpretation"] = {
        "context": "Milei 2024 labor reform using Brazilian 2017 model",
        "smulovitz_connection": "Judiciary blocks via Vizzoti doctrine (CLI component: PW=0.95)",
        "williamson_analysis": {
            "brazil_dominant_level": 3,  # Governance (PT coalition building)
            "argentina_dominant_level": 2,  # Institutions (constitutional lock-in)
            "mismatch": "Brazil succeeded via Level 3 (governance), Argentina blocked at Level 2 (institutions)"
        },
        "historical_parallel": "Similar to Menem 1990s reforms - needed constitutional crisis (hyperinflation) to overcome Level 2 lock-in"
    }
    
    return result

def demo_cross_jurisdictional_comparison() -> Dict[str, Any]:
    """
    Demo: Compare multiple Latin American targets for GDPR-style data protection.
    
    Use case: Which Latin American country is best suited for GDPR transplant?
    """
    targets = ["argentina", "brazil", "chile", "colombia", "mexico", "uruguay"]
    
    # Hypothetical CLI scores (higher = more locked-in)
    cli_scores = {
        "germany": 0.45,  # GDPR origin
        "argentina": 0.72,
        "brazil": 0.65,
        "chile": 0.55,
        "colombia": 0.68,
        "mexico": 0.70,
        "uruguay": 0.52
    }
    
    # Hypothetical H/V ratios
    h_v_ratios = {
        "germany": 1.65,  # Close to φ
        "argentina": 2.10,
        "brazil": 1.95,
        "chile": 1.72,
        "colombia": 1.88,
        "mexico": 2.05,
        "uruguay": 1.68
    }
    
    result = batch_compare_targets(
        concept="GDPR-style Data Protection",
        source="germany",
        targets=targets,
        cli_scores=cli_scores,
        h_v_ratios=h_v_ratios
    )
    
    # Add interpretation
    result["interpretation"] = {
        "expected_ranking": "Uruguay > Chile > Brazil > Colombia > Argentina > Mexico",
        "rationale": "Uruguay and Chile have lowest CLI + H/V closest to φ",
        "actual_adoption": {
            "uruguay": "Ley 18.331 (2008) - early adopter, GDPR-aligned 2018",
            "chile": "Boletín 11.144-07 (2017) - GDPR-inspired, slow progress",
            "argentina": "Ley 25.326 (2000) + Ley 27.483 (2018) - moderate adaptation",
            "brazil": "LGPD (2018) - successful GDPR adaptation",
            "colombia": "Ley 1581 (2012) + Decreto 1074 (2015) - pre-GDPR framework"
        }
    }
    
    return result
