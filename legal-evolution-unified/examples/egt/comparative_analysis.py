"""
Comparative Analysis Example
============================

Compare multiple jurisdictions/domains using the universal framework.

This shows how the SAME code works for completely different contexts.

Usage:
------
python examples/egt/comparative_analysis.py
"""

from src.egt import UniversalEGTPredictor
import pandas as pd

# CLI scores from different contexts
# (These could come from IusMorfos calculations)
cases = [
    {'name': 'Argentina Labor', 'cli': 0.87, 'domain': 'labor'},
    {'name': 'Chile Labor', 'cli': 0.15, 'domain': 'labor'},
    {'name': 'Brazil Environmental', 'cli': 0.35, 'domain': 'environmental'},
    {'name': 'Spain Speech', 'cli': 0.45, 'domain': 'speech'},
    {'name': 'Poland EU Integration', 'cli': 0.82, 'domain': 'international'},
    {'name': 'UK Brexit (hypothetical)', 'cli': 0.88, 'domain': 'constitutional'},
    # Add YOUR case here with YOUR CLI from IusMorfos
]

predictor = UniversalEGTPredictor()
results = []

for case in cases:
    # Same code for ALL domains
    predictor.fit(cli_score=case['cli'])
    pred = predictor.predict()
    
    results.append({
        'Case': case['name'],
        'Domain': case['domain'],
        'CLI': f"{case['cli']:.2f}",
        'P(Success)': f"{pred['reform_success_probability']:.1%}",
        'Status': pred['bifurcation_status'],
        'ESS Strength': f"{pred['ess_strength']:.2f}"
    })

# Display results
df = pd.DataFrame(results)
print("\n=== Universal EGT Framework - Comparative Analysis ===\n")
print(df.to_string(index=False))

# Key insight: Same framework, different domains, consistent predictions
print("\n" + "="*60)
print("NOTE: Framework uses SAME code for all domains.")
print("Only input that varies is CLI score.")
print("="*60)
