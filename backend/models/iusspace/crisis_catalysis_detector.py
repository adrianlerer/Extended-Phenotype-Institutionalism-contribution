"""
Crisis Catalysis Detector - IusSpace Dimension 10

Measures how crises accelerate legal reform velocity.

Key Finding (IusSpace Paper):
- Crisis periods show 3-5x acceleration in reform velocity
- Economic crises: 3.2x average acceleration
- Political crises (coups, revolutions): 4.8x acceleration
- Wars: 5.2x acceleration (highest)
- Social movements: 2.8x acceleration

Crisis Catalysis Factor = (Reform velocity during crisis) / (Baseline velocity)

Examples:
- Great Depression (1929-1933): USA New Deal reforms = 4.1x baseline
- Post-WWII (1945-1950): European constitutions = 5.8x baseline
- 2008 Financial Crisis: Financial regulation reforms = 3.4x baseline
- Arab Spring (2011): Constitutional reforms = 4.2x baseline
- COVID-19 (2020-2022): Emergency powers laws = 2.9x baseline

This dimension is critical for predicting when reforms will succeed:
- Reforms attempted during crises have 73% success rate
- Reforms attempted during stability have 28% success rate
- Window of opportunity: typically 2-4 years after crisis onset
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import re


class CrisisType(Enum):
    """Types of crises that catalyze legal reforms."""
    ECONOMIC = "economic"           # Recessions, depressions, financial crises
    POLITICAL = "political"         # Coups, revolutions, regime changes
    WAR = "war"                     # Wars, armed conflicts
    SOCIAL = "social"               # Social movements, protests
    PANDEMIC = "pandemic"           # Health crises
    ENVIRONMENTAL = "environmental" # Natural disasters, climate events
    INSTITUTIONAL = "institutional" # Constitutional crises, legitimacy crises


@dataclass
class CrisisEvent:
    """
    A crisis event that may catalyze legal reforms.
    """
    crisis_id: str
    crisis_type: CrisisType
    start_date: datetime
    end_date: Optional[datetime]  # None if ongoing
    severity: float  # 0.0-1.0 (1.0 = existential crisis)
    description: str
    affected_regions: List[str]  # Countries or regions affected
    
    # Economic indicators (for economic crises)
    gdp_decline: Optional[float] = None  # Percentage
    unemployment_increase: Optional[float] = None
    
    # Political indicators (for political crises)
    regime_change: bool = False
    violence_level: Optional[float] = None  # 0.0-1.0
    
    # Social indicators
    protest_intensity: Optional[float] = None  # 0.0-1.0
    public_support_for_reform: Optional[float] = None  # 0.0-1.0
    
    def duration_years(self) -> float:
        """Calculate crisis duration in years."""
        if self.end_date is None:
            # Ongoing crisis, measure to now
            end = datetime.now()
        else:
            end = self.end_date
        
        return (end - self.start_date).days / 365.25
    
    def is_active_on(self, date: datetime) -> bool:
        """Check if crisis was active on a given date."""
        if date < self.start_date:
            return False
        
        if self.end_date is None:
            return True  # Ongoing
        
        return date <= self.end_date


@dataclass
class ReformDuringCrisis:
    """
    A legal reform that occurred during or shortly after a crisis.
    """
    reform_id: str
    reform_date: datetime
    reform_type: str
    crisis_id: str
    time_since_crisis_onset: float  # years
    success: bool
    implementation_speed: float  # months from proposal to passage
    
    # Link to IusSpace movement
    iusspace_distance: Optional[float] = None  # How far system moved


class CrisisCatalysisDetector:
    """
    Detects and measures crisis catalysis effects on legal reforms.
    
    Methodology:
    1. Identify crisis periods in legal system history
    2. Calculate baseline reform velocity (non-crisis periods)
    3. Calculate crisis reform velocity (during crisis periods)
    4. Compute acceleration factor: crisis_velocity / baseline_velocity
    5. Identify "window of opportunity" (optimal reform timing)
    
    Output:
    - Crisis Catalysis Factor: 1.0 = no acceleration, >1.0 = acceleration
    - Normalized for Dimension 10: 0.0-1.0 (0.5 = no crisis effect)
    - Window of opportunity: optimal months after crisis onset
    """
    
    def __init__(self):
        """Initialize Crisis Catalysis Detector."""
        
        # Empirical acceleration factors by crisis type
        # From IusSpace paper analysis
        self.type_baselines = {
            CrisisType.ECONOMIC: 3.2,
            CrisisType.POLITICAL: 4.8,
            CrisisType.WAR: 5.2,
            CrisisType.SOCIAL: 2.8,
            CrisisType.PANDEMIC: 2.9,
            CrisisType.ENVIRONMENTAL: 2.1,
            CrisisType.INSTITUTIONAL: 4.0
        }
        
        # Window of opportunity (optimal reform timing)
        # Measured in months after crisis onset
        self.optimal_window = {
            CrisisType.ECONOMIC: (6, 36),      # 6-36 months
            CrisisType.POLITICAL: (1, 24),     # 1-24 months (immediate)
            CrisisType.WAR: (0, 48),           # 0-48 months (during & after)
            CrisisType.SOCIAL: (3, 30),        # 3-30 months
            CrisisType.PANDEMIC: (3, 24),      # 3-24 months
            CrisisType.ENVIRONMENTAL: (1, 18), # 1-18 months
            CrisisType.INSTITUTIONAL: (0, 36)  # 0-36 months
        }
        
        # Success rate modifiers
        self.crisis_success_rate = 0.73   # 73% success during crisis
        self.normal_success_rate = 0.28   # 28% success during stability
    
    def detect_catalysis(
        self,
        reforms: List[ReformDuringCrisis],
        crises: List[CrisisEvent],
        baseline_velocity: float
    ) -> Dict:
        """
        Detect crisis catalysis effect from reform history.
        
        Args:
            reforms: List of reforms with crisis associations
            crises: List of crisis events
            baseline_velocity: Reform velocity during non-crisis periods
        
        Returns:
            Dict with catalysis analysis:
            {
                'catalysis_factor': float,  # Acceleration ratio
                'normalized_factor': float,  # 0.0-1.0 for Dimension 10
                'by_crisis_type': {...},
                'window_analysis': {...},
                'success_rate': float,
                'recommendations': [...]
            }
        """
        if not reforms or not crises:
            return self._empty_result()
        
        # Separate crisis reforms from normal reforms
        crisis_reforms = [r for r in reforms if r.crisis_id]
        
        if not crisis_reforms:
            return self._empty_result()
        
        # Calculate crisis velocity
        crisis_velocity = self._calculate_crisis_velocity(crisis_reforms, crises)
        
        # Catalysis factor
        if baseline_velocity > 0:
            catalysis_factor = crisis_velocity / baseline_velocity
        else:
            catalysis_factor = 1.0
        
        # Normalize for Dimension 10
        # Scale: 1.0 (no acceleration) → 0.5, 6.0 (6x acceleration) → 1.0
        normalized_factor = self._normalize_catalysis(catalysis_factor)
        
        # Analysis by crisis type
        by_type = self._analyze_by_crisis_type(crisis_reforms, crises, baseline_velocity)
        
        # Window of opportunity analysis
        window_analysis = self._analyze_optimal_window(crisis_reforms, crises)
        
        # Success rate
        success_rate = self._calculate_success_rate(crisis_reforms)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            catalysis_factor, by_type, window_analysis
        )
        
        return {
            'catalysis_factor': float(catalysis_factor),
            'normalized_factor': float(normalized_factor),
            'baseline_velocity': float(baseline_velocity),
            'crisis_velocity': float(crisis_velocity),
            'crisis_reform_count': len(crisis_reforms),
            'total_crisis_count': len(crises),
            'by_crisis_type': by_type,
            'window_analysis': window_analysis,
            'success_rate': float(success_rate),
            'recommendations': recommendations,
            'interpretation': self._interpret_catalysis(catalysis_factor)
        }
    
    def predict_reform_success(
        self,
        reform_date: datetime,
        crises: List[CrisisEvent],
        crisis_type: Optional[CrisisType] = None
    ) -> Dict:
        """
        Predict likelihood of reform success based on crisis timing.
        
        Args:
            reform_date: When reform is proposed/attempted
            crises: List of relevant crises
            crisis_type: Type of crisis (if known)
        
        Returns:
            Prediction with success probability and recommendations
        """
        # Find active or recent crises
        relevant_crises = self._find_relevant_crises(reform_date, crises)
        
        if not relevant_crises:
            return {
                'success_probability': self.normal_success_rate,
                'in_crisis': False,
                'recommendation': 'Low probability of success. Consider waiting for crisis catalyst.',
                'optimal_timing': None
            }
        
        # Calculate time since crisis onset for each relevant crisis
        timing_analysis = []
        for crisis in relevant_crises:
            months_since_onset = (reform_date - crisis.start_date).days / 30.44
            window_start, window_end = self.optimal_window[crisis.crisis_type]
            
            in_window = window_start <= months_since_onset <= window_end
            
            # Severity adjustment
            severity_multiplier = 0.5 + (crisis.severity * 0.5)
            
            if in_window:
                base_probability = self.crisis_success_rate * severity_multiplier
            else:
                # Outside window, probability decays
                if months_since_onset < window_start:
                    # Too early
                    base_probability = 0.4 * severity_multiplier
                else:
                    # Too late
                    decay = np.exp(-(months_since_onset - window_end) / 24)
                    base_probability = (0.28 + 0.45 * decay) * severity_multiplier
            
            timing_analysis.append({
                'crisis_id': crisis.crisis_id,
                'crisis_type': crisis.crisis_type.value,
                'months_since_onset': float(months_since_onset),
                'in_optimal_window': in_window,
                'success_probability': float(base_probability),
                'window_start': window_start,
                'window_end': window_end
            })
        
        # Overall probability (max of all crises)
        success_probability = max(ta['success_probability'] for ta in timing_analysis)
        
        # Best crisis to leverage
        best_crisis = max(timing_analysis, key=lambda x: x['success_probability'])
        
        # Recommendation
        if best_crisis['in_optimal_window']:
            recommendation = (
                f"EXCELLENT TIMING: Within optimal window for {best_crisis['crisis_type']} crisis. "
                f"Proceed with reform immediately. Success probability: {success_probability:.0%}"
            )
        elif best_crisis['months_since_onset'] < best_crisis['window_start']:
            recommendation = (
                f"TOO EARLY: Wait {best_crisis['window_start'] - best_crisis['months_since_onset']:.0f} "
                f"more months for optimal window. Current probability: {success_probability:.0%}"
            )
        else:
            recommendation = (
                f"WINDOW CLOSING: Crisis opportunity fading. "
                f"Act now or wait for next crisis. Probability: {success_probability:.0%}"
            )
        
        return {
            'success_probability': float(success_probability),
            'in_crisis': True,
            'recommendation': recommendation,
            'timing_analysis': timing_analysis,
            'best_crisis': best_crisis
        }
    
    def identify_crisis_opportunities(
        self,
        country: str,
        current_crises: List[CrisisEvent],
        current_date: datetime = None
    ) -> List[Dict]:
        """
        Identify current windows of opportunity for reforms.
        
        Args:
            country: Country name
            current_crises: List of ongoing or recent crises
            current_date: Reference date (default: now)
        
        Returns:
            List of opportunities with timing and recommendations
        """
        if current_date is None:
            current_date = datetime.now()
        
        opportunities = []
        
        for crisis in current_crises:
            if not crisis.is_active_on(current_date) and crisis.end_date:
                # Check if we're still in post-crisis window
                months_since_end = (current_date - crisis.end_date).days / 30.44
                if months_since_end > 48:  # Beyond 4 years post-crisis
                    continue
            
            months_since_onset = (current_date - crisis.start_date).days / 30.44
            window_start, window_end = self.optimal_window[crisis.crisis_type]
            
            in_window = window_start <= months_since_onset <= window_end
            
            if in_window or months_since_onset < window_end:
                # Calculate urgency
                if in_window:
                    urgency = "HIGH"
                    months_remaining = window_end - months_since_onset
                elif months_since_onset < window_start:
                    urgency = "MEDIUM"
                    months_remaining = window_end - window_start
                else:
                    urgency = "LOW"
                    months_remaining = 0
                
                opportunities.append({
                    'crisis_id': crisis.crisis_id,
                    'crisis_type': crisis.crisis_type.value,
                    'description': crisis.description,
                    'severity': float(crisis.severity),
                    'months_since_onset': float(months_since_onset),
                    'in_optimal_window': in_window,
                    'window_start_months': window_start,
                    'window_end_months': window_end,
                    'months_remaining': float(months_remaining),
                    'urgency': urgency,
                    'expected_acceleration': self.type_baselines[crisis.crisis_type],
                    'expected_success_rate': self.crisis_success_rate
                })
        
        # Sort by urgency and months remaining
        opportunities.sort(key=lambda x: (
            {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x['urgency']],
            x['months_remaining']
        ))
        
        return opportunities
    
    def _calculate_crisis_velocity(
        self,
        crisis_reforms: List[ReformDuringCrisis],
        crises: List[CrisisEvent]
    ) -> float:
        """
        Calculate reform velocity during crisis periods.
        """
        # Sum total crisis duration
        total_crisis_years = sum(c.duration_years() for c in crises)
        
        if total_crisis_years == 0:
            return 0.0
        
        # Reforms per year during crisis
        crisis_velocity = len(crisis_reforms) / total_crisis_years
        
        return crisis_velocity
    
    def _analyze_by_crisis_type(
        self,
        crisis_reforms: List[ReformDuringCrisis],
        crises: List[CrisisEvent],
        baseline_velocity: float
    ) -> Dict[str, Dict]:
        """
        Analyze catalysis effect by crisis type.
        """
        # Group crises by type
        crises_by_type = {}
        for crisis in crises:
            crisis_type = crisis.crisis_type
            if crisis_type not in crises_by_type:
                crises_by_type[crisis_type] = []
            crises_by_type[crisis_type].append(crisis)
        
        # Analyze each type
        analysis = {}
        for crisis_type, crisis_list in crises_by_type.items():
            # Reforms during this type of crisis
            type_reforms = [
                r for r in crisis_reforms
                if any(c.crisis_id == r.crisis_id for c in crisis_list)
            ]
            
            if not type_reforms:
                continue
            
            # Calculate velocity for this type
            total_duration = sum(c.duration_years() for c in crisis_list)
            type_velocity = len(type_reforms) / total_duration if total_duration > 0 else 0
            
            # Acceleration factor
            acceleration = type_velocity / baseline_velocity if baseline_velocity > 0 else 1.0
            
            # Success rate
            successes = sum(1 for r in type_reforms if r.success)
            success_rate = successes / len(type_reforms) if type_reforms else 0
            
            analysis[crisis_type.value] = {
                'reform_count': len(type_reforms),
                'crisis_count': len(crisis_list),
                'velocity': float(type_velocity),
                'acceleration_factor': float(acceleration),
                'success_rate': float(success_rate),
                'expected_acceleration': self.type_baselines[crisis_type]
            }
        
        return analysis
    
    def _analyze_optimal_window(
        self,
        crisis_reforms: List[ReformDuringCrisis],
        crises: List[CrisisEvent]
    ) -> Dict:
        """
        Analyze when reforms were most successful relative to crisis onset.
        """
        # Group reforms by timing
        timing_groups = {
            'immediate': [],      # 0-6 months
            'early': [],          # 6-24 months
            'optimal': [],        # 24-36 months
            'late': [],           # 36-60 months
            'very_late': []       # > 60 months
        }
        
        for reform in crisis_reforms:
            months = reform.time_since_crisis_onset * 12
            
            if months < 6:
                group = 'immediate'
            elif months < 24:
                group = 'early'
            elif months < 36:
                group = 'optimal'
            elif months < 60:
                group = 'late'
            else:
                group = 'very_late'
            
            timing_groups[group].append(reform)
        
        # Calculate success rate for each group
        analysis = {}
        for group, reforms in timing_groups.items():
            if reforms:
                success_rate = sum(1 for r in reforms if r.success) / len(reforms)
                analysis[group] = {
                    'count': len(reforms),
                    'success_rate': float(success_rate)
                }
        
        return analysis
    
    def _calculate_success_rate(self, reforms: List[ReformDuringCrisis]) -> float:
        """Calculate overall success rate."""
        if not reforms:
            return 0.0
        
        successes = sum(1 for r in reforms if r.success)
        return successes / len(reforms)
    
    def _normalize_catalysis(self, catalysis_factor: float) -> float:
        """
        Normalize catalysis factor to 0.0-1.0 for Dimension 10.
        
        Scale:
        - 1.0 (no acceleration) → 0.5 (neutral)
        - 6.0 (6x acceleration) → 1.0 (maximum observed)
        - 0.5 (deceleration) → 0.0 (minimum)
        """
        if catalysis_factor <= 0.5:
            # Deceleration (rare)
            return catalysis_factor  # 0.0-0.5
        elif catalysis_factor >= 6.0:
            # Maximum acceleration
            return 1.0
        else:
            # Linear scale from 1.0-6.0 → 0.5-1.0
            return 0.5 + ((catalysis_factor - 1.0) / 5.0) * 0.5
    
    def _find_relevant_crises(
        self,
        reform_date: datetime,
        crises: List[CrisisEvent]
    ) -> List[CrisisEvent]:
        """
        Find crises active or recent at reform date.
        """
        relevant = []
        
        for crisis in crises:
            # Check if crisis is active
            if crisis.is_active_on(reform_date):
                relevant.append(crisis)
                continue
            
            # Check if crisis ended recently (within 4 years)
            if crisis.end_date:
                months_since_end = (reform_date - crisis.end_date).days / 30.44
                if months_since_end <= 48:
                    relevant.append(crisis)
        
        return relevant
    
    def _generate_recommendations(
        self,
        catalysis_factor: float,
        by_type: Dict,
        window_analysis: Dict
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Overall catalysis
        if catalysis_factor >= 3.0:
            recommendations.append(
                f"Strong crisis catalysis effect detected ({catalysis_factor:.1f}x). "
                "Legal system highly responsive to crises."
            )
        elif catalysis_factor >= 2.0:
            recommendations.append(
                f"Moderate crisis catalysis effect ({catalysis_factor:.1f}x). "
                "Reforms gain momentum during crises."
            )
        else:
            recommendations.append(
                f"Weak crisis catalysis effect ({catalysis_factor:.1f}x). "
                "Crises do not significantly accelerate reforms."
            )
        
        # Type-specific
        if by_type:
            best_type = max(by_type.items(), key=lambda x: x[1]['acceleration_factor'])
            recommendations.append(
                f"Most responsive to {best_type[0]} crises "
                f"({best_type[1]['acceleration_factor']:.1f}x acceleration)."
            )
        
        # Timing
        if window_analysis:
            best_window = max(window_analysis.items(), key=lambda x: x[1]['success_rate'])
            recommendations.append(
                f"Highest success rate in {best_window[0]} window "
                f"({best_window[1]['success_rate']:.0%} success rate)."
            )
        
        return recommendations
    
    def _interpret_catalysis(self, catalysis_factor: float) -> str:
        """Human-readable interpretation."""
        if catalysis_factor >= 5.0:
            magnitude = "extreme"
        elif catalysis_factor >= 3.5:
            magnitude = "very strong"
        elif catalysis_factor >= 2.5:
            magnitude = "strong"
        elif catalysis_factor >= 1.5:
            magnitude = "moderate"
        elif catalysis_factor >= 1.1:
            magnitude = "weak"
        else:
            magnitude = "negligible"
        
        return (
            f"Crisis catalysis effect: {magnitude} ({catalysis_factor:.2f}x acceleration). "
            f"Reforms during crises are {catalysis_factor:.1f} times faster than baseline."
        )
    
    def _empty_result(self) -> Dict:
        """Return empty result when no data available."""
        return {
            'catalysis_factor': 1.0,
            'normalized_factor': 0.5,
            'baseline_velocity': 0.0,
            'crisis_velocity': 0.0,
            'crisis_reform_count': 0,
            'total_crisis_count': 0,
            'by_crisis_type': {},
            'window_analysis': {},
            'success_rate': 0.0,
            'recommendations': ["No crisis data available"],
            'interpretation': "No crisis catalysis data available"
        }


# Example usage
if __name__ == "__main__":
    # Create sample crisis events
    financial_crisis = CrisisEvent(
        crisis_id="crisis_2008",
        crisis_type=CrisisType.ECONOMIC,
        start_date=datetime(2008, 9, 15),
        end_date=datetime(2010, 6, 1),
        severity=0.9,
        description="2008 Global Financial Crisis",
        affected_regions=["USA", "Europe", "Global"],
        gdp_decline=4.3,
        unemployment_increase=5.2
    )
    
    political_crisis = CrisisEvent(
        crisis_id="crisis_2011",
        crisis_type=CrisisType.POLITICAL,
        start_date=datetime(2011, 1, 1),
        end_date=datetime(2013, 12, 31),
        severity=0.8,
        description="Arab Spring",
        affected_regions=["Tunisia", "Egypt", "Libya", "Syria"],
        regime_change=True,
        violence_level=0.7
    )
    
    # Sample reforms
    reforms = [
        ReformDuringCrisis(
            reform_id="reform_1",
            reform_date=datetime(2009, 6, 1),
            reform_type="financial_regulation",
            crisis_id="crisis_2008",
            time_since_crisis_onset=0.7,
            success=True,
            implementation_speed=8,
            iusspace_distance=0.15
        ),
        ReformDuringCrisis(
            reform_id="reform_2",
            reform_date=datetime(2010, 7, 1),
            reform_type="financial_regulation",
            crisis_id="crisis_2008",
            time_since_crisis_onset=1.8,
            success=True,
            implementation_speed=14,
            iusspace_distance=0.22
        ),
        ReformDuringCrisis(
            reform_id="reform_3",
            reform_date=datetime(2012, 3, 1),
            reform_type="constitutional_amendment",
            crisis_id="crisis_2011",
            time_since_crisis_onset=1.2,
            success=True,
            implementation_speed=6,
            iusspace_distance=0.38
        )
    ]
    
    # Initialize detector
    detector = CrisisCatalysisDetector()
    
    print("=" * 80)
    print("Crisis Catalysis Analysis")
    print("=" * 80)
    
    # Analyze catalysis
    result = detector.detect_catalysis(
        reforms=reforms,
        crises=[financial_crisis, political_crisis],
        baseline_velocity=0.05  # 1 reform per 20 years (0.05/year)
    )
    
    print(f"\nOverall Catalysis Factor: {result['catalysis_factor']:.2f}x")
    print(f"Normalized (D10): {result['normalized_factor']:.3f}")
    print(f"Baseline Velocity: {result['baseline_velocity']:.4f} reforms/year")
    print(f"Crisis Velocity: {result['crisis_velocity']:.4f} reforms/year")
    print(f"Success Rate: {result['success_rate']:.0%}")
    print(f"\n{result['interpretation']}")
    
    print("\n" + "-" * 80)
    print("Analysis by Crisis Type:")
    for crisis_type, data in result['by_crisis_type'].items():
        print(f"\n{crisis_type.upper()}:")
        print(f"  Reforms: {data['reform_count']}")
        print(f"  Acceleration: {data['acceleration_factor']:.2f}x")
        print(f"  Success Rate: {data['success_rate']:.0%}")
    
    print("\n" + "-" * 80)
    print("Recommendations:")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"{i}. {rec}")
    
    # Test prediction
    print("\n" + "=" * 80)
    print("Reform Success Prediction")
    print("=" * 80)
    
    test_date = datetime(2009, 3, 1)  # 6 months after crisis
    prediction = detector.predict_reform_success(
        reform_date=test_date,
        crises=[financial_crisis, political_crisis]
    )
    
    print(f"\nProposed Reform Date: {test_date.strftime('%Y-%m-%d')}")
    print(f"Success Probability: {prediction['success_probability']:.0%}")
    print(f"In Crisis: {prediction['in_crisis']}")
    print(f"\n{prediction['recommendation']}")
