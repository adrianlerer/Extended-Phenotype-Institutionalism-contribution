"""
Tests for Iusmorfos Enterprise integration

Tests the integration between Iusmorfos Enterprise and Legal Evolution Unified platform.
"""

import pytest
from src.engines.iusmorfos_predictor import IusmorfosPredictor


class TestIusmorfosIntegration:
    """Test suite for Iusmorfos Enterprise integration"""
    
    def setup_method(self):
        """Setup test instance"""
        self.predictor = IusmorfosPredictor(db=None)
    
    def test_initialization(self):
        """Test that predictor initializes correctly"""
        assert self.predictor is not None
        assert hasattr(self.predictor, 'analyzer')
        assert hasattr(self.predictor, 'validator')
    
    def test_predict_transplant_success(self):
        """Test basic prediction functionality"""
        result = self.predictor.predict_transplant_success(
            concept_name="Corporate Compliance",
            source_jurisdiction="UK",
            target_jurisdiction="AR"
        )
        
        # Check required fields
        assert 'predicted_gap' in result
        assert 'ci_95_lower' in result
        assert 'ci_95_upper' in result
        assert 'passage_probability' in result
        assert 'confidence_level' in result
        
        # Check value ranges
        assert 0 <= result['predicted_gap'] <= 1
        assert 0 <= result['passage_probability'] <= 1
        assert result['ci_95_lower'] <= result['predicted_gap'] <= result['ci_95_upper']
    
    def test_batch_predict(self):
        """Test batch prediction"""
        targets = ["AR", "BR", "CL"]
        
        results = self.predictor.batch_predict(
            concept_name="Due Process",
            source_jurisdiction="US",
            target_jurisdictions=targets
        )
        
        assert len(results) == len(targets)
        for target in targets:
            assert target in results
            assert 'predicted_gap' in results[target] or 'error' in results[target]
    
    def test_confidence_intervals(self):
        """Test that confidence intervals are reasonable"""
        result = self.predictor.predict_transplant_success(
            concept_name="Habeas Corpus",
            source_jurisdiction="US",
            target_jurisdiction="MX"
        )
        
        # CI should span reasonable range
        ci_width = result['ci_95_upper'] - result['ci_95_lower']
        assert 0 < ci_width < 0.5  # Not too narrow or too wide
    
    def test_risk_assessment(self):
        """Test risk factor identification"""
        result = self.predictor.predict_transplant_success(
            concept_name="Punitive Damages",
            source_jurisdiction="US",
            target_jurisdiction="DE"
        )
        
        assert 'risk_factors' in result
        assert 'overall_risk' in result
        assert result['overall_risk'] in ['low', 'medium', 'high', 'critical', 'unknown']
    
    def test_recommendations_included(self):
        """Test that recommendations are generated"""
        result = self.predictor.predict_transplant_success(
            concept_name="Class Action",
            source_jurisdiction="US",
            target_jurisdiction="UK",
            include_recommendations=True
        )
        
        assert 'recommendations' in result
        assert len(result['recommendations']) > 0
        
        # Check recommendation structure
        rec = result['recommendations'][0]
        assert 'action' in rec
        assert 'priority' in rec
        assert 'rationale' in rec
    
    def test_compare_targets(self):
        """Test target comparison functionality"""
        targets = ["AR", "BR", "MX", "CL"]
        
        comparison = self.predictor.compare_targets(
            concept_name="Judicial Independence",
            source_jurisdiction="US",
            target_jurisdictions=targets
        )
        
        assert 'ranked_targets' in comparison
        assert len(comparison['ranked_targets']) == len(targets)
        assert 'best_target' in comparison
        assert comparison['best_target'] in targets
    
    def test_placeholder_mode(self):
        """Test that placeholder mode works when Iusmorfos not installed"""
        # This test verifies graceful degradation
        result = self.predictor.predict_transplant_success(
            concept_name="Test Concept",
            source_jurisdiction="TEST_SRC",
            target_jurisdiction="TEST_TGT"
        )
        
        # Should still return valid structure
        assert 'predicted_gap' in result
        assert 'note' in result  # Placeholder mode should add note
        assert 'analysis_complete' in result
    
    def test_peralta_integration(self):
        """Test Peralta module integration"""
        # Verify Peralta modules are available
        assert self.predictor.analyzer is not None
        assert self.predictor.validator is not None
        
        # Verify they're properly initialized
        assert hasattr(self.predictor.analyzer, 'calculate_similarity_matrix')
        assert hasattr(self.predictor.validator, 'n_iterations')
        assert self.predictor.validator.n_iterations == 1000


class TestIusmorfosEdgeCases:
    """Test edge cases and error handling"""
    
    def setup_method(self):
        """Setup test instance"""
        self.predictor = IusmorfosPredictor(db=None)
    
    def test_empty_target_list(self):
        """Test batch prediction with empty target list"""
        results = self.predictor.batch_predict(
            concept_name="Test",
            source_jurisdiction="US",
            target_jurisdictions=[]
        )
        
        assert results == {}
    
    def test_single_target_batch(self):
        """Test batch prediction with single target"""
        results = self.predictor.batch_predict(
            concept_name="Test",
            source_jurisdiction="US",
            target_jurisdictions=["UK"]
        )
        
        assert len(results) == 1
        assert "UK" in results
    
    def test_same_source_and_target(self):
        """Test prediction when source equals target"""
        result = self.predictor.predict_transplant_success(
            concept_name="Constitutional Rights",
            source_jurisdiction="US",
            target_jurisdiction="US"
        )
        
        # Should still work (may show low gap)
        assert 'predicted_gap' in result
    
    def test_recommendations_optional(self):
        """Test that recommendations can be disabled"""
        result = self.predictor.predict_transplant_success(
            concept_name="Test",
            source_jurisdiction="US",
            target_jurisdiction="UK",
            include_recommendations=False
        )
        
        # Recommendations should be empty list
        assert result['recommendations'] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
