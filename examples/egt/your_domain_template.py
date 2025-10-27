"""
Template for YOUR Domain
========================

Copy this template and adapt it to YOUR specific domain.

The framework is domain-agnostic, so you only need to:
1. Calculate CLI for your domain using IusMorfos
2. Call the predictor
3. Interpret results

Usage:
------
1. Copy this file to your_domain_name.py
2. Fill in your CLI score
3. Run: python examples/egt/your_domain_name.py
"""

from src.egt import UniversalEGTPredictor

# =============================================================================
# STEP 1: CALCULATE CLI FOR YOUR DOMAIN
# =============================================================================
# Use IusMorfos to calculate CLI with 5 components:
# 1. Text Vagueness (0-1)
# 2. Judicial Activism (0-1)
# 3. Treaty Hierarchy (0-1)
# 4. Precedent Weight (0-1)
# 5. Amendment Difficulty (0-1)
#
# CLI = average of these 5 components

# TODO: Replace this with YOUR actual CLI calculation
my_domain_cli = 0.XX  # <-- PUT YOUR CLI HERE

# Optional: Add metadata about your domain
domain_metadata = {
    'domain_name': 'YOUR_DOMAIN_HERE',  # e.g., 'privacy_law', 'antitrust', etc.
    'jurisdiction': 'YOUR_JURISDICTION',  # e.g., 'Germany', 'EU', etc.
    'time_period': '2020-2025',  # When is this CLI score from?
    'data_source': 'IusMorfos calculation based on...'
}

# =============================================================================
# STEP 2: RUN PREDICTION
# =============================================================================
predictor = UniversalEGTPredictor()
predictor.fit(cli_score=my_domain_cli)
result = predictor.predict()

# =============================================================================
# STEP 3: INTERPRET RESULTS
# =============================================================================
print(f"\n{'='*70}")
print(f"EGT Framework Prediction for {domain_metadata['domain_name']}")
print(f"{'='*70}\n")

print(f"Constitutional Lock-in Index: {result['cli_score']:.2f}")
print(f"Jurisdiction: {domain_metadata['jurisdiction']}")
print(f"Time Period: {domain_metadata['time_period']}\n")

print(f"--- Predictions ---")
print(f"Reform Success Probability: {result['reform_success_probability']:.1%}")
print(f"Confidence Interval: [{result['confidence_interval'][0]:.1%}, "
      f"{result['confidence_interval'][1]:.1%}]")
print(f"Bifurcation Status: {result['bifurcation_status']}")
print(f"ESS Stability Type: {result['stability_type']}")
print(f"ESS Strength: {result['ess_strength']:.2f}\n")

print(f"--- Interpretation ---")
print(result['interpretation'])

print(f"\n{'='*70}\n")

# =============================================================================
# STEP 4: MAKE DECISIONS BASED ON PREDICTIONS
# =============================================================================
if result['bifurcation_status'] == 'locked_irreversible':
    print("⚠️  WARNING: Strong constitutional lock-in detected")
    print("    → Standard reform processes likely to fail")
    print("    → Consider: constitutional amendment, regime change, or crisis catalyst")
    
elif result['bifurcation_status'] == 'critical_zone':
    print("⚡ MODERATE: System near bifurcation threshold")
    print("    → Reform possible but requires strategic coalition building")
    print("    → Timing and political capital crucial")
    
else:  # stable_reformable
    print("✅ FAVORABLE: Weak constitutional lock-in")
    print("    → Standard legislative processes should work")
    print("    → Focus on policy design and implementation")

print(f"\n{'='*70}\n")

# =============================================================================
# OPTIONAL: SENSITIVITY ANALYSIS
# =============================================================================
print("--- Sensitivity Analysis ---")
print("How sensitive are predictions to CLI measurement error?\n")

cli_variations = [my_domain_cli - 0.05, my_domain_cli, my_domain_cli + 0.05]

for cli_var in cli_variations:
    if 0 <= cli_var <= 1:  # Valid CLI range
        predictor.fit(cli_score=cli_var)
        result_var = predictor.predict()
        print(f"CLI = {cli_var:.2f}: P(success) = {result_var['reform_success_probability']:.1%}, "
              f"Status = {result_var['bifurcation_status']}")

print(f"\n{'='*70}\n")
