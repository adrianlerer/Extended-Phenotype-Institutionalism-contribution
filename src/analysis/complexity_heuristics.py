"""
Complexity Heuristics for Narrative Scoring

Simple rule-based system to propose C scores (1-10) for political narratives.

Heuristic Components:
1. Binary framing detection (us vs them) → Lower scores
2. Technical/academic vocabulary → Higher scores  
3. Sentence structure complexity → Higher scores
4. Subordinate clauses → Higher scores
5. Emotional language → Lower scores
"""

import re
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ComplexityFeatures:
    """Features extracted from narrative for scoring."""
    text_length: int
    avg_sentence_length: float
    technical_terms_count: int
    binary_markers_count: int
    subordinate_clauses_count: int
    emotional_words_count: int
    base_score: float = 5.0
    
    def to_dict(self) -> Dict:
        return {
            'text_length': self.text_length,
            'avg_sentence_length': self.avg_sentence_length,
            'technical_terms': self.technical_terms_count,
            'binary_markers': self.binary_markers_count,
            'subordinate_clauses': self.subordinate_clauses_count,
            'emotional_words': self.emotional_words_count
        }


class ComplexityScorer:
    """
    Heuristic-based complexity scorer for political narratives.
    
    Scoring Logic:
    - Base score = 5.0
    - Binary framing: -2.0 per marker
    - Technical terms: +0.5 per term (max +3.0)
    - Long sentences (>15 words avg): +0.5
    - Subordinate clauses: +0.5 per clause (max +2.0)
    - Emotional words: -0.3 per word (max -2.0)
    
    Final score clamped to [1.0, 10.0]
    """
    
    # Keywords for different features
    BINARY_MARKERS_ES = [
        'nosotros', 'ellos', 'enemigo', 'contra', 'defensa',
        'patria', 'violación', 'imposición', 'ataque', 'amenaza',
        'ilegítimo', 'rechazo', 'sumisión'
    ]
    
    BINARY_MARKERS_EN = [
        'us', 'them', 'enemy', 'against', 'defense', 'violation',
        'imposition', 'attack', 'threat', 'illegitimate', 'rejection',
        'take back', 'control'
    ]
    
    TECHNICAL_TERMS_ES = [
        'jurisdicción', 'complementariedad', 'multilateral', 'bilateral',
        'mecanismos', 'tratados', 'estándares', 'armonización',
        'evaluación', 'procedimientos', 'competencia', 'ratificación',
        'condicionalidades', 'sustentabilidad'
    ]
    
    TECHNICAL_TERMS_EN = [
        'jurisdiction', 'complementarity', 'multilateral', 'bilateral',
        'mechanisms', 'treaties', 'standards', 'harmonization',
        'assessment', 'procedures', 'competence', 'ratification',
        'conditionalities', 'sustainability', 'supranational'
    ]
    
    EMOTIONAL_WORDS_ES = [
        'destruye', 'persigue', 'colonial', 'imperialista', 'ilegítimo',
        'impone', 'sumisión', 'traición', 'vergüenza', 'orgullo'
    ]
    
    EMOTIONAL_WORDS_EN = [
        'destroys', 'persecutes', 'colonial', 'imperialist', 'illegitimate',
        'imposes', 'submission', 'betrayal', 'shame', 'pride'
    ]
    
    SUBORDINATE_MARKERS = [
        'cuando', 'porque', 'aunque', 'mientras', 'si', 'que',
        'when', 'because', 'although', 'while', 'if', 'that', 'which'
    ]
    
    def __init__(self, language: str = 'es'):
        """
        Initialize scorer.
        
        Args:
            language: 'es' (español) or 'en' (english)
        """
        self.language = language
        
        # Select appropriate keyword lists
        if language == 'es':
            self.binary_markers = self.BINARY_MARKERS_ES
            self.technical_terms = self.TECHNICAL_TERMS_ES
            self.emotional_words = self.EMOTIONAL_WORDS_ES
        else:
            self.binary_markers = self.BINARY_MARKERS_EN
            self.technical_terms = self.TECHNICAL_TERMS_EN
            self.emotional_words = self.EMOTIONAL_WORDS_EN
    
    def extract_features(self, text: str) -> ComplexityFeatures:
        """
        Extract complexity features from text.
        
        Args:
            text: Narrative text to analyze
            
        Returns:
            ComplexityFeatures object with extracted metrics
        """
        text_lower = text.lower()
        
        # Text length
        text_length = len(text)
        
        # Sentence analysis
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            words_per_sentence = [len(s.split()) for s in sentences]
            avg_sentence_length = sum(words_per_sentence) / len(words_per_sentence)
        else:
            avg_sentence_length = 0
        
        # Count features
        technical_count = sum(1 for term in self.technical_terms 
                             if term in text_lower)
        
        binary_count = sum(1 for marker in self.binary_markers 
                          if marker in text_lower)
        
        emotional_count = sum(1 for word in self.emotional_words 
                             if word in text_lower)
        
        subordinate_count = sum(1 for marker in self.SUBORDINATE_MARKERS 
                               if marker in text_lower)
        
        return ComplexityFeatures(
            text_length=text_length,
            avg_sentence_length=avg_sentence_length,
            technical_terms_count=technical_count,
            binary_markers_count=binary_count,
            subordinate_clauses_count=subordinate_count,
            emotional_words_count=emotional_count
        )
    
    def calculate_score(self, features: ComplexityFeatures) -> float:
        """
        Calculate complexity score from features.
        
        Args:
            features: ComplexityFeatures object
            
        Returns:
            C score (1.0 - 10.0)
        """
        score = features.base_score
        
        # Binary framing penalty
        score -= min(features.binary_markers_count * 2.0, 4.0)
        
        # Technical terms bonus
        score += min(features.technical_terms_count * 0.5, 3.0)
        
        # Sentence complexity bonus
        if features.avg_sentence_length > 15:
            score += 0.5
        if features.avg_sentence_length > 20:
            score += 0.5
        
        # Subordinate clauses bonus
        score += min(features.subordinate_clauses_count * 0.5, 2.0)
        
        # Emotional language penalty
        score -= min(features.emotional_words_count * 0.3, 2.0)
        
        # Clamp to valid range
        score = max(1.0, min(10.0, score))
        
        return round(score, 1)
    
    def score_narrative(self, text: str) -> Dict:
        """
        Score a narrative and return detailed results.
        
        Args:
            text: Narrative text to score
            
        Returns:
            Dict with score, features, and explanation
        """
        features = self.extract_features(text)
        score = self.calculate_score(features)
        
        # Generate explanation
        explanation = self._generate_explanation(features, score)
        
        return {
            'text': text,
            'score': score,
            'confidence': self._estimate_confidence(features),
            'features': features.to_dict(),
            'explanation': explanation
        }
    
    def _estimate_confidence(self, features: ComplexityFeatures) -> float:
        """
        Estimate confidence in scoring (0-1).
        
        Higher confidence when:
        - Clear signals (many binary markers OR many technical terms)
        - Adequate text length
        
        Returns:
            Confidence score (0.0 - 1.0)
        """
        confidence = 0.5  # Base confidence
        
        # Text length factor
        if features.text_length > 200:
            confidence += 0.2
        elif features.text_length < 50:
            confidence -= 0.2
        
        # Strong signals factor
        if features.binary_markers_count >= 3:
            confidence += 0.2
        if features.technical_terms_count >= 4:
            confidence += 0.2
        
        # Clamp to [0, 1]
        return max(0.0, min(1.0, confidence))
    
    def _generate_explanation(self, features: ComplexityFeatures, 
                             score: float) -> List[str]:
        """
        Generate human-readable explanation of score.
        
        Returns:
            List of explanation strings
        """
        explanations = []
        
        if features.binary_markers_count > 0:
            explanations.append(
                f"✓ Binary framing detected ({features.binary_markers_count} markers) → -2.0"
            )
        
        if features.technical_terms_count > 0:
            explanations.append(
                f"✓ Technical terms found ({features.technical_terms_count}) → +{min(features.technical_terms_count * 0.5, 3.0):.1f}"
            )
        
        if features.avg_sentence_length > 15:
            explanations.append(
                f"✓ Complex sentence structure (avg {features.avg_sentence_length:.1f} words) → +0.5"
            )
        
        if features.subordinate_clauses_count > 0:
            explanations.append(
                f"✓ Subordinate clauses ({features.subordinate_clauses_count}) → +{min(features.subordinate_clauses_count * 0.5, 2.0):.1f}"
            )
        
        if features.emotional_words_count > 0:
            explanations.append(
                f"✓ Emotional language ({features.emotional_words_count} words) → -{min(features.emotional_words_count * 0.3, 2.0):.1f}"
            )
        
        explanations.append("✓ Base score: 5.0")
        explanations.append("─" * 40)
        explanations.append(f"Final score: {score}")
        
        return explanations


# Convenience function for quick scoring
def score_text_quick(text: str, language: str = 'es') -> float:
    """
    Quick scoring function.
    
    Args:
        text: Narrative text
        language: 'es' or 'en'
        
    Returns:
        C score (1.0 - 10.0)
    """
    scorer = ComplexityScorer(language=language)
    result = scorer.score_narrative(text)
    return result['score']
