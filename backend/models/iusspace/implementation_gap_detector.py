"""
Implementation Gap Detector - IusSpace Dimension 5

Measures the gap between formal legal passage and actual implementation.

Key Finding (IusSpace Paper SSRN 5557838):
- WEIRD societies: 5.4% implementation gap
- Non-WEIRD societies: 31.2% implementation gap
- Effect size: Cohen's d = 3.749 (p < 0.0001)

This is one of the largest documented effects in comparative legal studies.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import re


@dataclass
class ProvisionCompliance:
    """Compliance data for a single legal provision."""
    provision_id: str
    provision_text: str
    mandatory: bool
    passage_date: datetime
    implementation_deadline: Optional[datetime]
    actual_implementation_date: Optional[datetime]
    compliance_rate: float  # 0.0-1.0
    enforcement_actions: int
    violations_detected: int


class ImplementationGapDetector:
    """
    Detects and measures implementation gaps in legal systems.
    
    The detector operates at three levels:
    1. Provision-level: Individual law articles/clauses
    2. Law-level: Entire statutes or regulations
    3. System-level: Overall legal system compliance
    
    Methodology:
    - Extract mandatory provisions from legal text
    - Track implementation timeline vs formal passage
    - Measure compliance rate through enforcement data
    - Calculate aggregate gap score
    
    Output:
    - Implementation Gap: 0.0 (perfect) to 1.0 (complete failure)
    - Breakdown by provision type (executive, legislative, judicial)
    - WEIRD-adjusted predictions
    """
    
    def __init__(
        self,
        weird_adjustment: bool = True,
        temporal_window: int = 5  # years to measure implementation
    ):
        """
        Initialize Implementation Gap Detector.
        
        Args:
            weird_adjustment: Apply WEIRD/Non-WEIRD adjustment factors
            temporal_window: Years after passage to measure implementation
        """
        self.weird_adjustment = weird_adjustment
        self.temporal_window = temporal_window
        
        # Provision type weights (some provisions harder to implement)
        self.provision_weights = {
            'executive_mandate': 0.8,      # Easiest (decree-based)
            'administrative_rule': 0.9,    # Easy (bureaucratic)
            'legislative_requirement': 1.0, # Baseline
            'judicial_procedure': 1.1,     # Harder (court capacity)
            'structural_reform': 1.3,      # Hardest (institutional change)
            'revenue_allocation': 1.2,     # Hard (budget constraints)
            'rights_guarantee': 1.4        # Hardest (cultural change needed)
        }
    
    def detect_gap(
        self,
        law_text: str,
        passage_date: datetime,
        compliance_data: Dict,
        enforcement_records: List[Dict],
        weird_score: float = 0.5
    ) -> Dict:
        """
        Detect implementation gap for a law.
        
        Args:
            law_text: Full text of law/statute
            passage_date: When law was formally passed
            compliance_data: Dict with compliance metrics
            enforcement_records: List of enforcement actions
            weird_score: 0.0 (pure Non-WEIRD) to 1.0 (pure WEIRD)
        
        Returns:
            Dict with gap analysis:
            {
                'overall_gap': 0.0-1.0,
                'provision_gaps': {...},
                'weird_adjusted_gap': 0.0-1.0,
                'predicted_vs_actual': {...},
                'breakdown_by_type': {...}
            }
        """
        # Extract provisions
        provisions = self._extract_provisions(law_text, passage_date)
        
        # Calculate compliance for each provision
        provision_gaps = {}
        for prov in provisions:
            gap = self._calculate_provision_gap(
                prov,
                compliance_data,
                enforcement_records
            )
            provision_gaps[prov.provision_id] = gap
        
        # Aggregate gap (weighted by provision type)
        overall_gap = self._aggregate_gaps(provisions, provision_gaps)
        
        # WEIRD adjustment
        if self.weird_adjustment:
            predicted_gap = self._predict_gap_from_weird(weird_score)
            weird_adjusted_gap = (overall_gap + predicted_gap) / 2
        else:
            weird_adjusted_gap = overall_gap
            predicted_gap = None
        
        # Breakdown by provision type
        breakdown = self._breakdown_by_type(provisions, provision_gaps)
        
        return {
            'overall_gap': float(overall_gap),
            'provision_count': len(provisions),
            'provision_gaps': {
                prov_id: float(gap) 
                for prov_id, gap in provision_gaps.items()
            },
            'weird_adjusted_gap': float(weird_adjusted_gap),
            'predicted_gap_from_weird': float(predicted_gap) if predicted_gap else None,
            'breakdown_by_type': breakdown,
            'interpretation': self._interpret_gap(weird_adjusted_gap)
        }
    
    def _extract_provisions(
        self,
        law_text: str,
        passage_date: datetime
    ) -> List[ProvisionCompliance]:
        """
        Extract mandatory provisions from law text.
        
        Uses regex patterns to identify:
        - "shall" mandates
        - "must" requirements
        - Explicit deadlines
        - Implementation timelines
        """
        provisions = []
        
        # Split by articles/sections
        # Pattern: "Article N", "Section N", "Art. N"
        article_pattern = r'(Article|Section|Art\.)\s+(\d+)'
        articles = re.split(article_pattern, law_text)
        
        for i in range(0, len(articles), 3):
            if i+2 >= len(articles):
                break
            
            article_type = articles[i+1]  # "Article", "Section", etc.
            article_num = articles[i+2]   # Number
            article_text = articles[i+3] if i+3 < len(articles) else ""
            
            # Check if mandatory
            is_mandatory = self._is_mandatory(article_text)
            
            if is_mandatory:
                # Extract deadline if present
                deadline = self._extract_deadline(article_text, passage_date)
                
                # Classify provision type
                prov_type = self._classify_provision_type(article_text)
                
                provision = ProvisionCompliance(
                    provision_id=f"{article_type}_{article_num}",
                    provision_text=article_text[:200],  # First 200 chars
                    mandatory=True,
                    passage_date=passage_date,
                    implementation_deadline=deadline,
                    actual_implementation_date=None,  # To be filled from compliance_data
                    compliance_rate=0.0,  # To be calculated
                    enforcement_actions=0,
                    violations_detected=0
                )
                
                provisions.append(provision)
        
        return provisions
    
    def _is_mandatory(self, text: str) -> bool:
        """Check if provision is mandatory (not discretionary)."""
        mandatory_indicators = [
            'shall', 'must', 'required', 'mandatory', 
            'obligatory', 'compulsory', 'will establish'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in mandatory_indicators)
    
    def _extract_deadline(
        self,
        text: str,
        passage_date: datetime
    ) -> Optional[datetime]:
        """
        Extract implementation deadline from provision text.
        
        Patterns:
        - "within 90 days"
        - "no later than December 31, 2025"
        - "within one year of passage"
        """
        # Pattern: "within X days/months/years"
        within_pattern = r'within\s+(\d+)\s+(days?|months?|years?)'
        match = re.search(within_pattern, text, re.IGNORECASE)
        
        if match:
            amount = int(match.group(1))
            unit = match.group(2).lower()
            
            if 'day' in unit:
                delta = timedelta(days=amount)
            elif 'month' in unit:
                delta = timedelta(days=amount * 30)
            elif 'year' in unit:
                delta = timedelta(days=amount * 365)
            else:
                delta = timedelta(days=365)  # Default 1 year
            
            return passage_date + delta
        
        # No explicit deadline found
        # Default: 2 years after passage (standard implementation window)
        return passage_date + timedelta(days=730)
    
    def _classify_provision_type(self, text: str) -> str:
        """
        Classify provision into implementation difficulty categories.
        """
        text_lower = text.lower()
        
        # Keywords for each type
        keywords = {
            'executive_mandate': ['president', 'executive', 'decree', 'order'],
            'administrative_rule': ['agency', 'department', 'minister', 'regulation'],
            'legislative_requirement': ['congress', 'parliament', 'legislature', 'enact'],
            'judicial_procedure': ['court', 'judge', 'tribunal', 'judicial'],
            'structural_reform': ['establish', 'create', 'reorganize', 'restructure'],
            'revenue_allocation': ['budget', 'fund', 'allocate', 'revenue', 'tax'],
            'rights_guarantee': ['right', 'freedom', 'guarantee', 'protect']
        }
        
        # Score each type
        scores = {}
        for prov_type, keywords_list in keywords.items():
            score = sum(1 for kw in keywords_list if kw in text_lower)
            scores[prov_type] = score
        
        # Return type with highest score
        if max(scores.values()) == 0:
            return 'legislative_requirement'  # Default
        
        return max(scores, key=scores.get)
    
    def _calculate_provision_gap(
        self,
        provision: ProvisionCompliance,
        compliance_data: Dict,
        enforcement_records: List[Dict]
    ) -> float:
        """
        Calculate implementation gap for single provision.
        
        Gap = 1.0 - (temporal_compliance × enforcement_compliance)
        
        Where:
        - temporal_compliance = 0.0 if missed deadline, 1.0 if met
        - enforcement_compliance = enforcement_actions / expected_actions
        """
        prov_id = provision.provision_id
        
        # Check if provision data exists
        if prov_id not in compliance_data:
            # No data = assume non-implementation
            return 1.0
        
        prov_data = compliance_data[prov_id]
        
        # Temporal compliance
        if 'actual_implementation_date' in prov_data:
            actual_date = prov_data['actual_implementation_date']
            
            if provision.implementation_deadline:
                if actual_date <= provision.implementation_deadline:
                    temporal_compliance = 1.0
                else:
                    # Partial credit for late implementation
                    days_late = (actual_date - provision.implementation_deadline).days
                    # Exponential decay: 50% credit after 1 year late, 25% after 2 years
                    temporal_compliance = 0.5 ** (days_late / 365.0)
            else:
                temporal_compliance = 1.0  # No deadline, consider compliant if implemented
        else:
            temporal_compliance = 0.0  # Not implemented
        
        # Enforcement compliance
        if 'compliance_rate' in prov_data:
            enforcement_compliance = prov_data['compliance_rate']
        else:
            # Count enforcement actions from records
            relevant_actions = [
                record for record in enforcement_records
                if record.get('provision_id') == prov_id
            ]
            
            # Heuristic: need at least 1 enforcement action per year
            years_since_passage = (datetime.now() - provision.passage_date).days / 365
            expected_actions = max(1, years_since_passage)
            actual_actions = len(relevant_actions)
            
            enforcement_compliance = min(1.0, actual_actions / expected_actions)
        
        # Combined gap
        overall_compliance = temporal_compliance * enforcement_compliance
        gap = 1.0 - overall_compliance
        
        return gap
    
    def _aggregate_gaps(
        self,
        provisions: List[ProvisionCompliance],
        provision_gaps: Dict[str, float]
    ) -> float:
        """
        Aggregate provision-level gaps into overall law gap.
        
        Uses weighted average based on provision type difficulty.
        """
        if not provisions:
            return 0.0
        
        weighted_sum = 0.0
        weight_total = 0.0
        
        for provision in provisions:
            prov_id = provision.provision_id
            gap = provision_gaps.get(prov_id, 1.0)
            
            # Get provision type from text
            prov_type = self._classify_provision_type(provision.provision_text)
            weight = self.provision_weights.get(prov_type, 1.0)
            
            weighted_sum += gap * weight
            weight_total += weight
        
        return weighted_sum / weight_total if weight_total > 0 else 0.0
    
    def _predict_gap_from_weird(self, weird_score: float) -> float:
        """
        Predict implementation gap based on WEIRD classification.
        
        From IusSpace paper (SSRN 5557838):
        - WEIRD (score ≥ 0.5): 5.4% gap
        - Non-WEIRD (score < 0.5): 31.2% gap
        
        Linear interpolation between these endpoints.
        """
        if weird_score >= 0.5:
            # Interpolate in WEIRD range: 0.5 → 0.054, 1.0 → 0.0
            # Assumption: perfect WEIRD (1.0) = 0% gap
            return 0.054 * 2 * (1.0 - weird_score)
        else:
            # Interpolate in Non-WEIRD range: 0.0 → 0.40, 0.5 → 0.312
            # Assumption: pure Non-WEIRD (0.0) = 40% gap (extreme case)
            return 0.40 - (weird_score * (0.40 - 0.312) / 0.5)
    
    def _breakdown_by_type(
        self,
        provisions: List[ProvisionCompliance],
        provision_gaps: Dict[str, float]
    ) -> Dict[str, Dict]:
        """
        Break down gaps by provision type.
        """
        breakdown = {}
        
        for provision in provisions:
            prov_type = self._classify_provision_type(provision.provision_text)
            gap = provision_gaps.get(provision.provision_id, 1.0)
            
            if prov_type not in breakdown:
                breakdown[prov_type] = {
                    'count': 0,
                    'total_gap': 0.0,
                    'provisions': []
                }
            
            breakdown[prov_type]['count'] += 1
            breakdown[prov_type]['total_gap'] += gap
            breakdown[prov_type]['provisions'].append(provision.provision_id)
        
        # Calculate averages
        for prov_type in breakdown:
            count = breakdown[prov_type]['count']
            breakdown[prov_type]['average_gap'] = (
                breakdown[prov_type]['total_gap'] / count
            )
        
        return breakdown
    
    def _interpret_gap(self, gap: float) -> str:
        """
        Human-readable interpretation of gap score.
        """
        if gap < 0.10:
            return "Excellent implementation (< 10% gap)"
        elif gap < 0.25:
            return "Good implementation (10-25% gap)"
        elif gap < 0.40:
            return "Moderate gap (25-40%) - typical for Non-WEIRD societies"
        elif gap < 0.60:
            return "Large gap (40-60%) - significant dysfunction"
        else:
            return "Severe gap (> 60%) - law largely non-operational"


# Neural Network for Implementation Gap Prediction
class ImplementationGapPredictor(nn.Module):
    """
    Neural network that predicts implementation gap from law text.
    
    Uses LegalBERT embeddings + context features to predict gap.
    Trained on historical laws with known implementation outcomes.
    """
    
    def __init__(self, bert_hidden_size=768, context_feature_dim=10):
        super().__init__()
        
        # Context features: WEIRD score, passage year, provision count, etc.
        self.context_encoder = nn.Sequential(
            nn.Linear(context_feature_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # Fusion layer
        self.fusion = nn.Sequential(
            nn.Linear(bert_hidden_size + 64, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
            nn.Sigmoid()  # Output: 0.0-1.0 (gap score)
        )
    
    def forward(self, law_embeddings, context_features):
        """
        Args:
            law_embeddings: (batch, 768) from LegalBERT
            context_features: (batch, 10) [WEIRD, year, prov_count, ...]
        
        Returns:
            predicted_gap: (batch, 1) in range 0.0-1.0
        """
        context_encoded = self.context_encoder(context_features)
        fused = torch.cat([law_embeddings, context_encoded], dim=1)
        gap_prediction = self.fusion(fused)
        return gap_prediction


# Example usage
if __name__ == "__main__":
    # Example law text
    law_text = """
    Article 1. The National Electoral Commission shall establish voter 
    registration systems within 180 days of this law's passage.
    
    Article 2. All government agencies must comply with data protection 
    standards no later than December 31, 2025.
    
    Article 3. Courts shall implement new procedural rules within one year.
    """
    
    # Simulated compliance data
    compliance_data = {
        'Article_1': {
            'actual_implementation_date': datetime(2024, 6, 15),
            'compliance_rate': 0.75
        },
        'Article_2': {
            'actual_implementation_date': None,  # Not implemented yet
            'compliance_rate': 0.0
        },
        'Article_3': {
            'actual_implementation_date': datetime(2024, 12, 1),
            'compliance_rate': 0.60
        }
    }
    
    enforcement_records = [
        {'provision_id': 'Article_1', 'date': datetime(2024, 7, 1), 'action': 'audit'},
        {'provision_id': 'Article_3', 'date': datetime(2025, 1, 15), 'action': 'review'}
    ]
    
    # Initialize detector
    detector = ImplementationGapDetector(weird_adjustment=True)
    
    # Detect gap
    result = detector.detect_gap(
        law_text=law_text,
        passage_date=datetime(2024, 1, 1),
        compliance_data=compliance_data,
        enforcement_records=enforcement_records,
        weird_score=0.35  # Non-WEIRD country
    )
    
    print("Implementation Gap Analysis:")
    print(f"Overall Gap: {result['overall_gap']:.1%}")
    print(f"WEIRD-Adjusted Gap: {result['weird_adjusted_gap']:.1%}")
    print(f"Interpretation: {result['interpretation']}")
    print(f"\nBreakdown by Type:")
    for prov_type, data in result['breakdown_by_type'].items():
        print(f"  {prov_type}: {data['average_gap']:.1%} (n={data['count']})")
