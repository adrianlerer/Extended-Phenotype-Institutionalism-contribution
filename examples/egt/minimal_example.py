"""
Minimal Working Example: 10 Lines of Code
=========================================

Shows that framework requires NO domain-specific knowledge.
Works for ANY constitutional topic.

Usage:
------
python examples/egt/minimal_example.py
"""

from src.egt import UniversalEGTPredictor

# Step 1: You calculated CLI for your domain somehow
my_cli_score = 0.65  # Could be labor, criminal, environmental, fiscal, etc.

# Step 2: Predict
predictor = UniversalEGTPredictor()
predictor.fit(cli_score=my_cli_score)
result = predictor.predict()

# Step 3: Interpret
print(f"Reform success: {result['reform_success_probability']:.1%}")
print(f"Status: {result['bifurcation_status']}")
print(f"ESS strength: {result['ess_strength']:.2f}")
print(f"\nInterpretation:\n{result['interpretation']}")

# That's it. Framework is domain-agnostic.
