"""
Iusmorfos Predictor - Enterprise Integration
Integrates Iusmorfos Enterprise with Peralta's statistical validation
"""

from typing import Dict, List, Optional, Tuple
import logging

# Import from private iusmorfos-enterprise
try:
    # TODO: Once iusmorfos-enterprise is properly packaged, import correct modules
    # from iusmorfos import IusmorfosEngine
    # from iusmorfos.enhanced_prediction import EnhancedPredictor
    # For now, IUSMORFOS_AVAILABLE = False until package structure is confirmed
    IUSMORFOS_AVAILABLE = False
    logging.warning("Iusmorfos Enterprise not available. Using placeholder.")
except ImportError:
    IUSMORFOS_AVAILABLE = False
    logging.warning("Iusmorfos Enterprise not available. Using placeholder.")

# Import from Peralta (already integrated in base)
from code.analysis import LegalConceptAnalysis
from code.bootstrap import BootstrapValidator

logger = logging.getLogger(__name__)


class IusmorfosPredictor:
    """
    Iusmorfos Enterprise predictor integrated with Peralta validation
    
    Features:
    - Implementation gap prediction (base Iusmorfos)
    - Confidence intervals via bootstrap (Enterprise)
    - Risk factor identification (Enterprise)
    - Actionable recommendations (Enterprise)
    - Multidimensional jurisdiction analysis (Peralta)
    - Network-based similar jurisdiction finding (Peralta)
    """
    
    def __init__(self, db=None):
        """
        Initialize predictor with optional database connection
        
        Args:
            db: Database connection (optional, uses defaults if None)
        """
        if IUSMORFOS_AVAILABLE:
            # self.base_engine = IusmorfosEngine(db)
            # self.enhanced = EnhancedPredictor(self.base_engine)
            logger.info("Iusmorfos Enterprise initialized")
        else:
            self.base_engine = None
            self.enhanced = None
            logger.warning("Running in placeholder mode (Iusmorfos not available)")
        
        # Peralta modules (always available)
        self.analyzer = LegalConceptAnalysis()
        self.validator = BootstrapValidator(n_iterations=1000)
        
        logger.info("IusmorfosPredictor initialized successfully")
    
    def predict_transplant_success(
        self,
        concept_name: str,
        source_jurisdiction: str,
        target_jurisdiction: str,
        include_recommendations: bool = True,
        n_bootstrap: int = 1000
    ) -> Dict:
        """
        Predict transplant success with comprehensive analysis
        
        Combines:
        - Iusmorfos Enterprise: Gap prediction, CI, risk factors
        - Peralta: Multidimensional analysis, similar jurisdictions
        
        Args:
            concept_name: Legal concept to analyze (e.g., "Corporate Compliance")
            source_jurisdiction: Origin jurisdiction code (e.g., "UK", "US")
            target_jurisdiction: Target jurisdiction code (e.g., "AR", "BR")
            include_recommendations: Include actionable recommendations
            n_bootstrap: Bootstrap iterations for confidence intervals
        
        Returns:
            Comprehensive prediction dictionary with:
                - predicted_gap: Implementation gap estimate [0,1]
                - confidence_interval: 95% CI bounds
                - passage_probability: 1 - gap
                - risk_factors: List of identified risks
                - recommendations: Actionable next steps
                - target_analysis: Multidimensional classification
                - similar_jurisdictions: Comparable cases
        """
        logger.info(f"Predicting transplant: {concept_name} from {source_jurisdiction} to {target_jurisdiction}")
        
        if not IUSMORFOS_AVAILABLE:
            return self._placeholder_prediction(
                concept_name, source_jurisdiction, target_jurisdiction
            )
        
        # ===== IUSMORFOS ENTERPRISE: Prediction + CI + Risks =====
        prediction = self.enhanced.predict_with_confidence_intervals(
            concept_name=concept_name,
            source_jurisdiction=source_jurisdiction,
            target_jurisdiction=target_jurisdiction,
            n_bootstrap=n_bootstrap
        )
        
        risk_factors = self.enhanced.identify_risk_factors(
            source_jurisdiction=source_jurisdiction,
            target_jurisdiction=target_jurisdiction
        )
        
        # ===== PERALTA: Multidimensional Analysis =====
        try:
            target_analysis = self._analyze_jurisdiction_multidimensional(
                target_jurisdiction
            )
        except Exception as e:
            logger.warning(f"Peralta analysis failed: {e}")
            target_analysis = {'status': 'unavailable'}
        
        # ===== PERALTA: Find Similar Jurisdictions =====
        try:
            similar_jurisdictions = self._find_similar_jurisdictions(
                target_jurisdiction,
                similarity_threshold=0.7
            )
        except Exception as e:
            logger.warning(f"Similar jurisdiction search failed: {e}")
            similar_jurisdictions = []
        
        # ===== IUSMORFOS ENTERPRISE: Recommendations =====
        recommendations = []
        if include_recommendations:
            recommendations = self.enhanced.generate_recommendations(
                prediction, risk_factors
            )
        
        # ===== COMPILE RESULT =====
        result = {
            'concept': concept_name,
            'source': source_jurisdiction,
            'target': target_jurisdiction,
            
            # Core prediction (Iusmorfos Enterprise)
            'predicted_gap': prediction['predicted_gap'],
            'ci_95_lower': prediction['ci_95_lower'],
            'ci_95_upper': prediction['ci_95_upper'],
            'passage_probability': prediction['passage_probability'],
            
            # Confidence assessment
            'confidence_level': prediction['confidence_level'],
            'similar_cases_used': prediction['similar_cases_used'],
            
            # Risk analysis (Iusmorfos Enterprise)
            'risk_factors': risk_factors,
            'overall_risk': self._calculate_overall_risk(risk_factors),
            
            # Recommendations (Iusmorfos Enterprise)
            'recommendations': recommendations,
            
            # Context analysis (Peralta)
            'target_analysis': target_analysis,
            'similar_jurisdictions': similar_jurisdictions,
            
            # Metadata
            'analysis_complete': True,
            'n_bootstrap_iterations': n_bootstrap
        }
        
        logger.info(f"Prediction complete: gap={prediction['predicted_gap']:.2%}, confidence={prediction['confidence_level']}")
        
        return result
    
    def _analyze_jurisdiction_multidimensional(
        self,
        jurisdiction: str
    ) -> Dict:
        """
        Multidimensional analysis using Peralta
        
        Classifies jurisdiction across economic, social, political dimensions
        """
        # TODO: Implement when jurisdiction data is available
        # For now, return basic classification from Iusmorfos
        
        if not IUSMORFOS_AVAILABLE:
            return {'status': 'unavailable'}
        
        base_classification = self.base_engine.classify_jurisdiction(jurisdiction)
        
        return {
            'jurisdiction': jurisdiction,
            'is_weird': base_classification.get('is_weird', False),
            'adaptive_coefficient': base_classification.get('adaptive_coefficient', 0),
            'features': base_classification.get('features', {}),
            'status': 'basic'  # Will be enhanced with Peralta data
        }
    
    def _find_similar_jurisdictions(
        self,
        target_jurisdiction: str,
        similarity_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Find jurisdictions similar to target using Peralta network analysis
        
        Args:
            target_jurisdiction: Jurisdiction to find similarities for
            similarity_threshold: Minimum similarity score [0,1]
        
        Returns:
            List of similar jurisdictions with similarity scores
        """
        # TODO: Implement when jurisdiction similarity data is available
        # For now, return empty list
        
        logger.debug(f"Finding jurisdictions similar to {target_jurisdiction}")
        
        return []
    
    def _calculate_overall_risk(self, risk_factors: List[Dict]) -> str:
        """
        Calculate overall risk level from individual risk factors
        
        Args:
            risk_factors: List of risk factor dicts
        
        Returns:
            Overall risk: 'low', 'medium', 'high', 'critical'
        """
        if not risk_factors:
            return 'low'
        
        # Count by severity
        high_risks = sum(1 for r in risk_factors if r['severity'] == 'high')
        medium_risks = sum(1 for r in risk_factors if r['severity'] == 'medium')
        
        if high_risks >= 3:
            return 'critical'
        elif high_risks >= 2:
            return 'high'
        elif high_risks >= 1 or medium_risks >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _placeholder_prediction(
        self,
        concept_name: str,
        source_jurisdiction: str,
        target_jurisdiction: str
    ) -> Dict:
        """
        Placeholder prediction when Iusmorfos is not available
        
        Returns realistic-looking placeholder data for testing
        """
        logger.warning("Using placeholder prediction (Iusmorfos not installed)")
        
        import numpy as np
        
        # Generate deterministic placeholder based on input hash
        seed = hash((concept_name, source_jurisdiction, target_jurisdiction)) % 1000
        np.random.seed(seed)
        
        # Simulate realistic gap
        gap = np.clip(np.random.beta(3, 5), 0.15, 0.75)
        ci_width = 0.15
        
        # Simulate risk factors
        risk_factors = []
        if gap > 0.4:
            risk_factors.append({
                'type': 'institutional_gap',
                'severity': 'high',
                'description': f'Significant institutional distance between {source_jurisdiction} and {target_jurisdiction}',
                'impact_on_gap': 0.15
            })
        if gap > 0.5:
            risk_factors.append({
                'type': 'weak_enforcement',
                'severity': 'medium',
                'description': 'Limited state capacity for implementation',
                'impact_on_gap': 0.10
            })
        
        # Simulate recommendations
        recommendations = [{
            'action': 'install_iusmorfos',
            'priority': 'high',
            'rationale': 'Iusmorfos Enterprise not available. Install to enable real predictions.',
            'next_steps': [
                'pip install git+https://github.com/adrianlerer/iusmorfos-enterprise.git',
                'Verify installation with: python -c "import iusmorfos"',
                'Re-run prediction with actual engine'
            ]
        }]
        
        return {
            'concept': concept_name,
            'source': source_jurisdiction,
            'target': target_jurisdiction,
            'predicted_gap': float(gap),
            'ci_95_lower': max(0, gap - ci_width),
            'ci_95_upper': min(1, gap + ci_width),
            'passage_probability': float(1 - gap),
            'confidence_level': 'placeholder',
            'similar_cases_used': 0,
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'target_analysis': {'status': 'placeholder'},
            'similar_jurisdictions': [],
            'overall_risk': 'unknown',
            'analysis_complete': False,
            'note': 'PLACEHOLDER DATA - Install iusmorfos-enterprise for real predictions'
        }
    
    def batch_predict(
        self,
        concept_name: str,
        source_jurisdiction: str,
        target_jurisdictions: List[str],
        include_recommendations: bool = True
    ) -> Dict[str, Dict]:
        """
        Batch prediction for multiple target jurisdictions
        
        Args:
            concept_name: Legal concept
            source_jurisdiction: Single source
            target_jurisdictions: List of targets
            include_recommendations: Include recommendations
        
        Returns:
            Dict mapping target → prediction result
        """
        logger.info(f"Batch prediction: {concept_name} from {source_jurisdiction} to {len(target_jurisdictions)} targets")
        
        results = {}
        
        for target in target_jurisdictions:
            try:
                results[target] = self.predict_transplant_success(
                    concept_name, 
                    source_jurisdiction, 
                    target,
                    include_recommendations=include_recommendations
                )
            except Exception as e:
                logger.error(f"Prediction failed for {target}: {e}")
                results[target] = {
                    'error': str(e),
                    'target': target,
                    'analysis_complete': False
                }
        
        return results
    
    def compare_targets(
        self,
        concept_name: str,
        source_jurisdiction: str,
        target_jurisdictions: List[str]
    ) -> Dict:
        """
        Compare multiple target jurisdictions and rank by suitability
        
        Args:
            concept_name: Legal concept
            source_jurisdiction: Source jurisdiction
            target_jurisdictions: List of target jurisdictions
        
        Returns:
            Dict with ranked targets and comparison metrics
        """
        logger.info(f"Comparing {len(target_jurisdictions)} targets for {concept_name}")
        
        # Get predictions for all targets
        predictions = self.batch_predict(
            concept_name,
            source_jurisdiction,
            target_jurisdictions,
            include_recommendations=False
        )
        
        # Rank by passage probability (lower gap = better)
        ranked = sorted(
            [(target, pred) for target, pred in predictions.items() if 'predicted_gap' in pred],
            key=lambda x: x[1]['predicted_gap']
        )
        
        # Compile comparison
        comparison = {
            'concept': concept_name,
            'source': source_jurisdiction,
            'targets_analyzed': len(target_jurisdictions),
            'ranked_targets': [
                {
                    'rank': i + 1,
                    'jurisdiction': target,
                    'predicted_gap': pred['predicted_gap'],
                    'passage_probability': pred['passage_probability'],
                    'confidence_level': pred['confidence_level'],
                    'overall_risk': pred['overall_risk']
                }
                for i, (target, pred) in enumerate(ranked)
            ],
            'best_target': ranked[0][0] if ranked else None,
            'worst_target': ranked[-1][0] if ranked else None
        }
        
        logger.info(f"Best target: {comparison['best_target']}")
        
        return comparison
