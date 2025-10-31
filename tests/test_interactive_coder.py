"""
Basic tests for InteractiveCoder (Level 1)

Tests:
- Complexity scoring heuristics
- Feature extraction
- Score calculation
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analysis.complexity_heuristics import ComplexityScorer, score_text_quick
from src.analysis.interactive_coder import InteractiveCoder, NarrativeScore


class TestComplexityScorer:
    """Test complexity scoring heuristics."""
    
    def test_scorer_initialization(self):
        """Test scorer can be initialized."""
        scorer_es = ComplexityScorer(language='es')
        assert scorer_es.language == 'es'
        
        scorer_en = ComplexityScorer(language='en')
        assert scorer_en.language == 'en'
    
    def test_simple_binary_narrative(self):
        """Test scoring of simple binary narrative."""
        text = "Nosotros contra ellos. Defensa de la patria. Enemigo extranjero."
        
        scorer = ComplexityScorer(language='es')
        result = scorer.score_narrative(text)
        
        # Should have low score (binary, simple)
        assert 1.0 <= result['score'] <= 4.0
        assert result['features']['binary_markers'] >= 2
    
    def test_complex_technical_narrative(self):
        """Test scoring of complex technical narrative."""
        text = """
        Los tratados internacionales establecen mecanismos de jurisdicción
        complementaria. La armonización regulatoria requiere procedimientos
        multilaterales de evaluación. Los estándares técnicos deben equilibrar
        sustentabilidad con competencia nacional.
        """
        
        scorer = ComplexityScorer(language='es')
        result = scorer.score_narrative(text)
        
        # Should have high score (technical, complex)
        assert 6.0 <= result['score'] <= 10.0
        assert result['features']['technical_terms'] >= 4
    
    def test_feature_extraction(self):
        """Test feature extraction works correctly."""
        text = "Simple text with subordinate clause because reasons."
        
        scorer = ComplexityScorer(language='en')
        features = scorer.extract_features(text)
        
        assert features.text_length > 0
        assert features.avg_sentence_length > 0
        assert features.subordinate_clauses_count >= 1
    
    def test_score_clamping(self):
        """Test scores are clamped to [1, 10]."""
        # Very simple text
        simple = "Us vs them."
        
        # Very complex text
        complex_text = " ".join([
            "jurisdicción", "complementariedad", "multilateral",
            "mecanismos", "tratados", "estándares", "armonización"
        ] * 3)
        
        scorer = ComplexityScorer(language='es')
        
        simple_score = scorer.score_narrative(simple)['score']
        complex_score = scorer.score_narrative(complex_text)['score']
        
        assert 1.0 <= simple_score <= 10.0
        assert 1.0 <= complex_score <= 10.0
    
    def test_quick_scoring_function(self):
        """Test convenience function works."""
        text = "Defensa nacional contra imposición extranjera."
        score = score_text_quick(text, language='es')
        
        assert isinstance(score, float)
        assert 1.0 <= score <= 10.0


class TestInteractiveCoder:
    """Test InteractiveCoder functionality (non-interactive parts)."""
    
    def test_coder_initialization(self):
        """Test coder can be initialized."""
        coder = InteractiveCoder(language='es', verbose=False)
        assert coder.language == 'es'
        assert coder.scoring_method == 'heuristic'
    
    def test_propose_score(self):
        """Test score proposal works."""
        coder = InteractiveCoder(language='es', verbose=False)
        
        text = "Soberanía nacional contra tribunal ilegítimo."
        proposal = coder.propose_score(text, case_id='TEST-001')
        
        assert isinstance(proposal, NarrativeScore)
        assert proposal.case_id == 'TEST-001'
        assert 1.0 <= proposal.proposed_score <= 10.0
        assert 0.0 <= proposal.confidence <= 1.0
    
    def test_generate_report(self):
        """Test report generation."""
        coder = InteractiveCoder(verbose=False)
        
        # Mock coded dataframe
        df = pd.DataFrame({
            'case_id': ['A', 'B', 'C'],
            'proposed_score': [3.0, 5.0, 7.0],
            'human_score': [3.0, 6.0, 7.0]
        })
        
        report = coder.generate_report(df)
        
        assert report['n_coded'] == 3
        assert 0.0 <= report['acceptance_rate'] <= 1.0


def test_synthetic_dataset_exists():
    """Test synthetic dataset file exists."""
    synthetic_path = Path(__file__).parent.parent / 'data' / 'raw' / 'synthetic_cases_example.csv'
    assert synthetic_path.exists(), "Synthetic dataset not found"
    
    # Verify can be loaded
    df = pd.read_csv(synthetic_path)
    assert 'Case_ID' in df.columns
    assert 'Sov_Narrative' in df.columns
    assert len(df) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
