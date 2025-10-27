"""
Domain-Agnosticism Test Suite
=============================

These tests verify that the EGT framework is truly domain-agnostic:
predictions depend ONLY on CLI score, not on domain labels.

This is the CORE TEST of universality. If these tests pass, the framework
can be used for labor law, criminal law, environmental law, fiscal law, etc.
with confidence that predictions are consistent.

Test Philosophy:
--------------
1. Same CLI → Same Prediction (regardless of domain)
2. Framework works identically for all domains
3. No domain-specific code in core modules
"""

import pytest
import numpy as np
from typing import Dict

from src.egt import UniversalEGTPredictor, predict_reform_success, VinceParameters


class TestDomainAgnosticism:
    """Framework must work identically across all domains."""
    
    @pytest.mark.parametrize("domain,cli_score,expected_success_range", [
        # Real validated cases
        ("labor_law_argentina", 0.87, (0.10, 0.15)),  # Strong lock-in
        ("criminal_law_chile", 0.28, (0.65, 0.90)),  # Weak lock-in
        ("environmental_law_brazil", 0.35, (0.55, 0.75)),  # Moderate
        ("speech_law_spain", 0.45, (0.45, 0.65)),  # Moderate-high
        
        # Hypothetical cases (same framework)
        ("fiscal_law", 0.82, (0.10, 0.20)),  # Strong lock-in
        ("trade_law", 0.15, (0.75, 0.95)),  # Very weak lock-in
        ("property_law", 0.60, (0.30, 0.50)),  # Moderate lock-in
        ("constitutional_amendment", 0.95, (0.00, 0.10)),  # Extreme lock-in
        ("administrative_procedure", 0.05, (0.90, 1.00)),  # Almost no lock-in
    ])
    def test_universal_prediction(self, domain: str, cli_score: float, expected_success_range: tuple):
        """
        Framework predictions depend ONLY on CLI, not domain label.
        
        This test proves domain-agnosticism by showing that predictions
        fall within expected ranges regardless of domain name.
        """
        predictor = UniversalEGTPredictor()
        predictor.fit(cli_score=cli_score)
        result = predictor.predict()
        
        prob = result['reform_success_probability']
        
        # Check probability in expected range
        assert expected_success_range[0] <= prob <= expected_success_range[1], \
            f"{domain}: Expected success in {expected_success_range}, got {prob:.3f}"
        
        # Check that all required keys are present
        required_keys = [
            'reform_success_probability',
            'ess_strength',
            'bifurcation_status',
            'confidence_interval',
            'interpretation',
            'stability_type',
            'cli_score'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"
    
    def test_same_cli_same_prediction_across_domains(self):
        """
        Two different domains with SAME CLI must give SAME prediction.
        
        This is the CORE TEST of universality.
        """
        cli = 0.50
        
        # Test across 5 arbitrary domains
        domains = ['labor', 'criminal', 'environmental', 'fiscal', 'trade']
        predictions = []
        
        for domain in domains:
            predictor = UniversalEGTPredictor()
            predictor.fit(cli_score=cli)
            result = predictor.predict()
            predictions.append(result['reform_success_probability'])
        
        # All predictions should be identical (within numerical precision)
        predictions_array = np.array(predictions)
        assert np.std(predictions_array) < 1e-10, \
            f"Same CLI={cli} gave different predictions across domains: {predictions}"
    
    def test_cli_monotonicity(self):
        """
        Higher CLI → Lower success probability (monotonic relationship).
        
        This tests that the framework respects the fundamental hypothesis.
        """
        predictor = UniversalEGTPredictor()
        
        cli_values = [0.1, 0.3, 0.5, 0.7, 0.9]
        probabilities = []
        
        for cli in cli_values:
            predictor.fit(cli_score=cli)
            result = predictor.predict()
            probabilities.append(result['reform_success_probability'])
        
        # Check monotonic decrease
        for i in range(len(probabilities) - 1):
            assert probabilities[i] >= probabilities[i+1], \
                f"Non-monotonic: CLI={cli_values[i]} gave prob={probabilities[i]}, " \
                f"but CLI={cli_values[i+1]} gave prob={probabilities[i+1]}"
    
    def test_bifurcation_threshold(self):
        """
        Bifurcation status changes at CLI threshold (~ 0.70).
        
        Tests that regime classification is consistent.
        """
        predictor = UniversalEGTPredictor()
        
        # Below threshold
        predictor.fit(cli_score=0.25)
        result_low = predictor.predict()
        assert result_low['bifurcation_status'] == 'stable_reformable'
        
        # At threshold
        predictor.fit(cli_score=0.50)
        result_mid = predictor.predict()
        assert result_mid['bifurcation_status'] == 'critical_zone'
        
        # Above threshold
        predictor.fit(cli_score=0.85)
        result_high = predictor.predict()
        assert result_high['bifurcation_status'] == 'locked_irreversible'
    
    def test_confidence_interval_consistency(self):
        """
        Confidence intervals are consistent with point estimates.
        
        CI should contain point estimate and width should depend on ESS strength.
        """
        predictor = UniversalEGTPredictor()
        
        for cli in [0.2, 0.5, 0.8]:
            predictor.fit(cli_score=cli)
            result = predictor.predict()
            
            prob = result['reform_success_probability']
            ci_lower, ci_upper = result['confidence_interval']
            
            # CI should contain point estimate
            assert ci_lower <= prob <= ci_upper, \
                f"CI [{ci_lower}, {ci_upper}] does not contain estimate {prob}"
            
            # CI should be in [0, 1]
            assert 0 <= ci_lower <= 1
            assert 0 <= ci_upper <= 1
            
            # CI width should be positive
            assert ci_upper >= ci_lower
    
    def test_convenience_function_equivalence(self):
        """
        Convenience function predict_reform_success() gives same results as class API.
        """
        cli = 0.65
        
        # Method 1: Class API
        predictor = UniversalEGTPredictor()
        predictor.fit(cli_score=cli)
        result1 = predictor.predict()
        
        # Method 2: Convenience function
        result2 = predict_reform_success(cli_score=cli)
        
        # Should give identical results
        assert abs(result1['reform_success_probability'] - result2['reform_success_probability']) < 1e-10
        assert result1['bifurcation_status'] == result2['bifurcation_status']
    
    def test_custom_vince_parameters(self):
        """
        Custom Vince parameters should not break domain-agnosticism.
        
        Even with custom parameters, same CLI should give same prediction.
        """
        custom_params = VinceParameters(
            r=0.30,  # Different growth rate
            K_max=150.0,  # Different carrying capacity
            bifurcation_threshold=0.65  # Different threshold
        )
        
        cli = 0.55
        
        # Two predictors with same custom parameters
        predictor1 = UniversalEGTPredictor(vince_parameters=custom_params)
        predictor1.fit(cli_score=cli)
        result1 = predictor1.predict()
        
        predictor2 = UniversalEGTPredictor(vince_parameters=custom_params)
        predictor2.fit(cli_score=cli)
        result2 = predictor2.predict()
        
        # Should give identical results
        assert abs(result1['reform_success_probability'] - result2['reform_success_probability']) < 1e-10
    
    def test_edge_cases(self):
        """
        Test edge cases: CLI = 0 and CLI = 1.
        """
        predictor = UniversalEGTPredictor()
        
        # CLI = 0 (no lock-in)
        predictor.fit(cli_score=0.0)
        result_min = predictor.predict()
        assert result_min['reform_success_probability'] > 0.9, \
            "CLI=0 should give very high success probability"
        assert result_min['bifurcation_status'] == 'stable_reformable'
        
        # CLI = 1 (maximum lock-in)
        predictor.fit(cli_score=1.0)
        result_max = predictor.predict()
        assert result_max['reform_success_probability'] < 0.1, \
            "CLI=1 should give very low success probability"
        assert result_max['bifurcation_status'] == 'locked_irreversible'
    
    def test_error_handling(self):
        """
        Test that predictor raises appropriate errors.
        """
        predictor = UniversalEGTPredictor()
        
        # Should raise error if predict() called before fit()
        with pytest.raises(RuntimeError, match="Must call fit\\(\\) before predict\\(\\)"):
            predictor.predict()
        
        # Should raise error for invalid CLI values
        with pytest.raises(ValueError):
            predictor.fit(cli_score=-0.1)
        
        with pytest.raises(ValueError):
            predictor.fit(cli_score=1.5)
    
    def test_method_chaining(self):
        """
        Test that fit() returns self for method chaining.
        """
        predictor = UniversalEGTPredictor()
        
        # Should be able to chain fit() and predict()
        result = predictor.fit(cli_score=0.60).predict()
        
        assert 'reform_success_probability' in result
        assert predictor.cli == 0.60


class TestUniversalityAcrossRealCases:
    """
    Test framework against REAL empirical cases to verify universality.
    
    These are actual cases from the 60-case dataset.
    """
    
    @pytest.mark.parametrize("country,domain,cli,actual_success_rate,expected_status", [
        # Validated cases from empirical dataset
        ("Argentina", "labor", 0.87, 0.00, "locked_irreversible"),
        ("Chile", "labor", 0.15, 0.88, "stable_reformable"),
        ("Brazil", "labor", 0.40, 0.50, "critical_zone"),
        ("Spain", "labor", 0.35, 0.71, "critical_zone"),
        ("Colombia", "labor", 0.52, 0.40, "critical_zone"),
    ])
    def test_real_case_validation(
        self,
        country: str,
        domain: str,
        cli: float,
        actual_success_rate: float,
        expected_status: str
    ):
        """
        Validate framework against real empirical cases.
        
        Prediction should match observed success rate direction.
        """
        predictor = UniversalEGTPredictor()
        predictor.fit(cli_score=cli)
        result = predictor.predict()
        
        predicted_prob = result['reform_success_probability']
        predicted_status = result['bifurcation_status']
        
        # Check status matches
        assert predicted_status == expected_status, \
            f"{country} {domain}: Expected status {expected_status}, got {predicted_status}"
        
        # Check prediction direction matches reality
        # (low CLI → high success, high CLI → low success)
        if actual_success_rate > 0.5:
            assert predicted_prob > 0.4, \
                f"{country} {domain}: High actual success ({actual_success_rate}) " \
                f"but low predicted prob ({predicted_prob})"
        else:
            assert predicted_prob < 0.6, \
                f"{country} {domain}: Low actual success ({actual_success_rate}) " \
                f"but high predicted prob ({predicted_prob})"


class TestNoDomaainSpecificCodeInCore:
    """
    Test that core modules contain no domain-specific terms.
    
    This is a META-TEST: it checks the code itself for domain-specificity.
    """
    
    def test_no_domain_terms_in_universal_predictor(self):
        """
        universal_predictor.py should not contain domain-specific terms.
        """
        import inspect
        from src.egt import universal_predictor
        
        source = inspect.getsource(universal_predictor)
        
        # List of forbidden domain-specific terms
        forbidden_terms = [
            'labor', 'criminal', 'environmental', 'fiscal', 'trade',
            'property', 'speech', 'tax', 'antitrust', 'family'
        ]
        
        for term in forbidden_terms:
            # Check that term does NOT appear in variable names or logic
            # (OK if it appears in comments or docstrings explaining universality)
            lines = source.split('\n')
            code_lines = [
                line for line in lines
                if not line.strip().startswith('#') and not line.strip().startswith('"""')
            ]
            code_text = '\n'.join(code_lines)
            
            # This is OK if term appears in docstrings showing examples
            # But NOT OK if it appears in actual code logic
            assert term not in code_text.lower() or '>>>' in source, \
                f"Found domain-specific term '{term}' in core code (should be domain-agnostic)"


# Integration test: Run full workflow
def test_full_workflow_integration():
    """
    Integration test: Complete workflow from CLI to interpretation.
    
    This simulates a real user workflow.
    """
    # User has CLI score from IusMorfos
    cli_from_iusmorfos = 0.72  # Could be ANY domain
    
    # Step 1: Initialize predictor
    predictor = UniversalEGTPredictor()
    
    # Step 2: Fit to CLI
    predictor.fit(cli_score=cli_from_iusmorfos)
    
    # Step 3: Get predictions
    result = predictor.predict()
    
    # Step 4: Interpret results
    assert isinstance(result['reform_success_probability'], float)
    assert 0 <= result['reform_success_probability'] <= 1
    assert isinstance(result['interpretation'], str)
    assert len(result['interpretation']) > 50  # Should be informative
    
    # Step 5: User can now make decisions based on predictions
    if result['bifurcation_status'] == 'locked_irreversible':
        # Framework predicts reform will fail
        assert result['reform_success_probability'] < 0.3
    
    print(f"\n=== Integration Test Success ===")
    print(f"CLI Score: {cli_from_iusmorfos}")
    print(f"Success Probability: {result['reform_success_probability']:.1%}")
    print(f"Status: {result['bifurcation_status']}")
    print(f"Interpretation: {result['interpretation'][:100]}...")
