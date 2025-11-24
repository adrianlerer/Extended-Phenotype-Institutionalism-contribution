"""
Reform Velocity Calculator - IusSpace Dimension 9

Measures the speed of legal system evolution as distance traveled in IusSpace per unit time.

Key Finding (JurisRank Paper SSRN 5405459):
- Pre-digital era (1679-1945): 45 years average reform cycle
- Transitional era (1945-1990): 15-20 years
- Digital era (1990-present): 3.2 years average
- Acceleration factor: 14x speedup

This dramatic acceleration is attributed to:
1. Digital diffusion of legal ideas
2. International legal networks (EU, UN, OAS)
3. Constitutional courts sharing jurisprudence
4. Reduced transaction costs for legal transplantation
5. Real-time monitoring of reform outcomes

Velocity = Euclidean distance in 12D IusSpace / Time elapsed
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import math


class ReformEra(Enum):
    """Historical eras with different reform velocities."""
    PRE_DIGITAL = "pre_digital"        # 1679-1945: 45 years avg
    TRANSITIONAL = "transitional"      # 1945-1990: 15-20 years avg
    DIGITAL = "digital"                # 1990-present: 3.2 years avg


@dataclass
class IusSpaceVector:
    """
    12-dimensional vector representing a legal system state.
    
    Dimensions (from IusSpace paper):
    1. Constitutional Entrenchment (CE)
    2. Ultraactivity (UA)
    3. Judicial Protection Intensity (JPI)
    4. Cultural Lock-In (CLI_cultural)
    5. Implementation Gap
    6. Legal Norm Fitness (JurisRank)
    7. Network Topology (Graph Density)
    8. Constitutional Centrality (Betweenness)
    9. Reform Velocity (self-referential - calculated from history)
    10. Crisis Catalysis Factor
    11. WEIRD Classification
    12. Transplantation Era
    """
    ce: float                    # D1: 0.0-1.0
    ua: float                    # D2: 0.0-1.0
    jpi: float                   # D3: 0.0-1.0
    cli_cultural: float          # D4: 0.0-1.0
    implementation_gap: float    # D5: 0.0-1.0
    jurisrank: float             # D6: 0.0-1.0 (normalized)
    network_density: float       # D7: 0.0-1.0
    centrality: float            # D8: 0.0-1.0
    reform_velocity: float       # D9: 0.0-1.0 (normalized)
    crisis_factor: float         # D10: 0.0-1.0
    weird_score: float           # D11: 0.0-1.0
    transplantation_era: float   # D12: 0.0-1.0
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array for distance calculations."""
        return np.array([
            self.ce, self.ua, self.jpi, self.cli_cultural,
            self.implementation_gap, self.jurisrank,
            self.network_density, self.centrality,
            self.reform_velocity, self.crisis_factor,
            self.weird_score, self.transplantation_era
        ])
    
    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'IusSpaceVector':
        """Create from numpy array."""
        return cls(*arr.tolist())


@dataclass
class ReformEvent:
    """
    Single reform event in legal system history.
    """
    event_id: str
    event_type: str  # 'constitutional_amendment', 'new_law', 'court_ruling', 'revolution'
    date: datetime
    description: str
    iusspace_before: IusSpaceVector
    iusspace_after: IusSpaceVector
    triggered_by_crisis: bool = False
    crisis_type: Optional[str] = None  # 'economic', 'political', 'war', 'social'
    
    def calculate_distance(self) -> float:
        """Calculate Euclidean distance traveled in IusSpace."""
        before = self.iusspace_before.to_array()
        after = self.iusspace_after.to_array()
        
        # Euclidean distance in 12D space
        return np.linalg.norm(after - before)
    
    def calculate_velocity(self, reference_date: Optional[datetime] = None) -> float:
        """
        Calculate instantaneous velocity (distance per year).
        
        Args:
            reference_date: Compare to this date instead of previous state
        
        Returns:
            Velocity in IusSpace units per year
        """
        distance = self.calculate_distance()
        
        if reference_date:
            time_elapsed = (self.date - reference_date).days / 365.25
        else:
            # Assume 1 year if no reference (instantaneous)
            time_elapsed = 1.0
        
        if time_elapsed == 0:
            return 0.0
        
        return distance / time_elapsed


class ReformVelocityCalculator:
    """
    Calculates reform velocity for legal systems.
    
    Methodology:
    1. Track IusSpace vector at multiple time points
    2. Calculate distance between consecutive states
    3. Divide by time elapsed
    4. Aggregate velocities (mean, trend)
    5. Compare to era baselines (45 years → 3.2 years)
    
    Output:
    - Current velocity (IusSpace units/year)
    - Acceleration trend (positive/negative)
    - Era classification (pre-digital, transitional, digital)
    - Predicted next reform date
    """
    
    def __init__(self):
        """Initialize Reform Velocity Calculator."""
        
        # Era baselines (from JurisRank paper)
        self.era_baselines = {
            ReformEra.PRE_DIGITAL: 45.0,      # years per reform
            ReformEra.TRANSITIONAL: 17.5,     # midpoint of 15-20
            ReformEra.DIGITAL: 3.2            # years per reform
        }
        
        # Velocity normalization (for Dimension 9)
        # Assume max realistic velocity: 1 reform per year = 1.0
        # Assume min: 1 reform per 100 years = 0.01
        self.velocity_min = 0.01  # 1 per 100 years
        self.velocity_max = 1.0   # 1 per year
    
    def calculate_velocity(
        self,
        reform_history: List[ReformEvent],
        current_date: Optional[datetime] = None
    ) -> Dict:
        """
        Calculate reform velocity from history.
        
        Args:
            reform_history: List of reform events (chronological)
            current_date: Reference date (default: now)
        
        Returns:
            Dict with velocity analysis:
            {
                'current_velocity': float,  # reforms per year
                'normalized_velocity': float,  # 0.0-1.0 for Dimension 9
                'mean_velocity': float,
                'acceleration': float,  # positive = speeding up
                'era': ReformEra,
                'predicted_next_reform': datetime,
                'time_series': List[Tuple[datetime, float]]
            }
        """
        if not reform_history:
            return self._empty_result()
        
        if current_date is None:
            current_date = datetime.now()
        
        # Sort by date
        sorted_history = sorted(reform_history, key=lambda e: e.date)
        
        # Calculate velocity for each reform pair
        velocities = []
        time_series = []
        
        for i in range(len(sorted_history) - 1):
            event_current = sorted_history[i]
            event_next = sorted_history[i + 1]
            
            distance = self._calculate_distance_between_events(
                event_current, event_next
            )
            time_elapsed = (event_next.date - event_current.date).days / 365.25
            
            if time_elapsed > 0:
                velocity = distance / time_elapsed
                velocities.append(velocity)
                time_series.append((event_next.date, velocity))
        
        if not velocities:
            return self._empty_result()
        
        # Current velocity (most recent)
        current_velocity = velocities[-1]
        
        # Mean velocity
        mean_velocity = np.mean(velocities)
        
        # Acceleration (trend)
        acceleration = self._calculate_acceleration(velocities, time_series)
        
        # Normalize velocity for Dimension 9
        normalized_velocity = self._normalize_velocity(current_velocity)
        
        # Era classification
        era = self._classify_era(sorted_history[-1].date)
        
        # Predict next reform
        predicted_next_reform = self._predict_next_reform(
            sorted_history[-1], current_velocity, current_date
        )
        
        return {
            'current_velocity': float(current_velocity),
            'normalized_velocity': float(normalized_velocity),
            'mean_velocity': float(mean_velocity),
            'median_velocity': float(np.median(velocities)),
            'acceleration': float(acceleration),
            'era': era.value,
            'era_baseline': self.era_baselines[era],
            'predicted_next_reform': predicted_next_reform,
            'time_series': [(dt.isoformat(), float(v)) for dt, v in time_series],
            'reform_count': len(sorted_history),
            'time_span_years': (sorted_history[-1].date - sorted_history[0].date).days / 365.25,
            'interpretation': self._interpret_velocity(current_velocity, era)
        }
    
    def calculate_system_velocity(
        self,
        country: str,
        start_date: datetime,
        end_date: datetime,
        snapshots: List[Tuple[datetime, IusSpaceVector]]
    ) -> Dict:
        """
        Calculate velocity from IusSpace snapshots (alternative method).
        
        Args:
            country: Country name
            start_date: Start of observation period
            end_date: End of observation period
            snapshots: List of (date, IusSpace vector) tuples
        
        Returns:
            Velocity analysis similar to calculate_velocity()
        """
        if len(snapshots) < 2:
            return self._empty_result()
        
        # Sort snapshots
        sorted_snapshots = sorted(snapshots, key=lambda s: s[0])
        
        # Calculate distances between consecutive snapshots
        velocities = []
        time_series = []
        
        for i in range(len(sorted_snapshots) - 1):
            date1, vec1 = sorted_snapshots[i]
            date2, vec2 = sorted_snapshots[i + 1]
            
            distance = np.linalg.norm(vec2.to_array() - vec1.to_array())
            time_elapsed = (date2 - date1).days / 365.25
            
            if time_elapsed > 0:
                velocity = distance / time_elapsed
                velocities.append(velocity)
                time_series.append((date2, velocity))
        
        if not velocities:
            return self._empty_result()
        
        current_velocity = velocities[-1]
        mean_velocity = np.mean(velocities)
        acceleration = self._calculate_acceleration(velocities, time_series)
        normalized_velocity = self._normalize_velocity(current_velocity)
        era = self._classify_era(end_date)
        
        # Predict next significant reform
        time_to_next_reform = 1.0 / current_velocity if current_velocity > 0 else self.era_baselines[era]
        predicted_next_reform = end_date + timedelta(days=time_to_next_reform * 365.25)
        
        return {
            'country': country,
            'current_velocity': float(current_velocity),
            'normalized_velocity': float(normalized_velocity),
            'mean_velocity': float(mean_velocity),
            'median_velocity': float(np.median(velocities)),
            'acceleration': float(acceleration),
            'era': era.value,
            'era_baseline': self.era_baselines[era],
            'predicted_next_reform': predicted_next_reform.isoformat(),
            'time_series': [(dt.isoformat(), float(v)) for dt, v in time_series],
            'snapshot_count': len(sorted_snapshots),
            'time_span_years': (end_date - start_date).days / 365.25,
            'interpretation': self._interpret_velocity(current_velocity, era)
        }
    
    def compare_velocities(
        self,
        country1: str,
        velocity1: float,
        country2: str,
        velocity2: float
    ) -> Dict:
        """
        Compare reform velocities between two countries.
        
        Returns:
            Comparison analysis with ratio and interpretation
        """
        ratio = velocity1 / velocity2 if velocity2 > 0 else float('inf')
        
        faster_country = country1 if velocity1 > velocity2 else country2
        slower_country = country2 if velocity1 > velocity2 else country1
        
        if ratio > 2.0 or ratio < 0.5:
            magnitude = "significantly"
        elif ratio > 1.5 or ratio < 0.67:
            magnitude = "moderately"
        else:
            magnitude = "slightly"
        
        return {
            'country1': country1,
            'velocity1': float(velocity1),
            'country2': country2,
            'velocity2': float(velocity2),
            'ratio': float(ratio),
            'faster_country': faster_country,
            'slower_country': slower_country,
            'interpretation': f"{faster_country} is reforming {magnitude} faster than {slower_country} (ratio: {ratio:.2f}x)"
        }
    
    def _calculate_distance_between_events(
        self,
        event1: ReformEvent,
        event2: ReformEvent
    ) -> float:
        """
        Calculate distance between two reform events.
        
        Uses the 'after' state of event1 and 'after' state of event2.
        """
        vec1 = event1.iusspace_after.to_array()
        vec2 = event2.iusspace_after.to_array()
        
        return np.linalg.norm(vec2 - vec1)
    
    def _calculate_acceleration(
        self,
        velocities: List[float],
        time_series: List[Tuple[datetime, float]]
    ) -> float:
        """
        Calculate acceleration (rate of change of velocity).
        
        Uses linear regression slope over time.
        Positive = speeding up, Negative = slowing down
        """
        if len(velocities) < 2:
            return 0.0
        
        # Convert dates to years since first event
        first_date = time_series[0][0]
        x = np.array([(dt - first_date).days / 365.25 for dt, _ in time_series])
        y = np.array(velocities)
        
        # Linear regression
        if len(x) < 2:
            return 0.0
        
        # Slope = acceleration
        coeffs = np.polyfit(x, y, 1)
        acceleration = coeffs[0]
        
        return acceleration
    
    def _normalize_velocity(self, velocity: float) -> float:
        """
        Normalize velocity to 0.0-1.0 for Dimension 9.
        
        Uses logarithmic scale:
        - 0.01 reforms/year (1 per 100 years) → 0.0
        - 0.1 reforms/year (1 per 10 years) → 0.5
        - 1.0 reforms/year (1 per year) → 1.0
        """
        if velocity <= self.velocity_min:
            return 0.0
        if velocity >= self.velocity_max:
            return 1.0
        
        # Logarithmic normalization
        log_velocity = np.log10(velocity)
        log_min = np.log10(self.velocity_min)
        log_max = np.log10(self.velocity_max)
        
        normalized = (log_velocity - log_min) / (log_max - log_min)
        
        return np.clip(normalized, 0.0, 1.0)
    
    def _classify_era(self, date: datetime) -> ReformEra:
        """
        Classify date into reform era.
        """
        year = date.year
        
        if year < 1945:
            return ReformEra.PRE_DIGITAL
        elif year < 1990:
            return ReformEra.TRANSITIONAL
        else:
            return ReformEra.DIGITAL
    
    def _predict_next_reform(
        self,
        last_event: ReformEvent,
        current_velocity: float,
        current_date: datetime
    ) -> datetime:
        """
        Predict when next reform will occur.
        
        Based on current velocity and acceleration trends.
        """
        if current_velocity == 0:
            # No reforms happening, use era baseline
            era = self._classify_era(current_date)
            years_to_next = self.era_baselines[era]
        else:
            # Time to next reform = 1 / velocity
            years_to_next = 1.0 / current_velocity
        
        # Bound predictions
        years_to_next = np.clip(years_to_next, 0.1, 50.0)
        
        predicted_date = last_event.date + timedelta(days=years_to_next * 365.25)
        
        return predicted_date
    
    def _interpret_velocity(self, velocity: float, era: ReformEra) -> str:
        """
        Human-readable interpretation of velocity.
        """
        baseline = self.era_baselines[era]
        observed_cycle = 1.0 / velocity if velocity > 0 else float('inf')
        
        if observed_cycle < baseline * 0.5:
            speed = "very fast"
        elif observed_cycle < baseline * 0.8:
            speed = "fast"
        elif observed_cycle < baseline * 1.2:
            speed = "normal"
        elif observed_cycle < baseline * 2.0:
            speed = "slow"
        else:
            speed = "very slow"
        
        return (
            f"Reform cycle: {observed_cycle:.1f} years ({speed} for {era.value} era). "
            f"Baseline: {baseline:.1f} years. "
            f"Velocity: {velocity:.3f} reforms/year."
        )
    
    def _empty_result(self) -> Dict:
        """Return empty result when no data available."""
        return {
            'current_velocity': 0.0,
            'normalized_velocity': 0.0,
            'mean_velocity': 0.0,
            'median_velocity': 0.0,
            'acceleration': 0.0,
            'era': ReformEra.DIGITAL.value,
            'era_baseline': self.era_baselines[ReformEra.DIGITAL],
            'predicted_next_reform': None,
            'time_series': [],
            'reform_count': 0,
            'time_span_years': 0.0,
            'interpretation': "No reform history available"
        }


# Example usage
if __name__ == "__main__":
    # Create sample reform history
    
    # Pre-digital era country (slow reforms)
    pre_digital_events = [
        ReformEvent(
            event_id="reform_1",
            event_type="constitutional_amendment",
            date=datetime(1850, 1, 1),
            description="First constitution",
            iusspace_before=IusSpaceVector(0.3, 0.2, 0.1, 0.4, 0.5, 0.2, 0.3, 0.2, 0.0, 0.1, 0.2, 0.1),
            iusspace_after=IusSpaceVector(0.5, 0.3, 0.2, 0.5, 0.4, 0.3, 0.4, 0.3, 0.0, 0.1, 0.2, 0.2)
        ),
        ReformEvent(
            event_id="reform_2",
            event_type="constitutional_amendment",
            date=datetime(1895, 1, 1),
            description="Major amendment",
            iusspace_before=IusSpaceVector(0.5, 0.3, 0.2, 0.5, 0.4, 0.3, 0.4, 0.3, 0.0, 0.1, 0.2, 0.2),
            iusspace_after=IusSpaceVector(0.6, 0.4, 0.3, 0.6, 0.35, 0.4, 0.5, 0.4, 0.0, 0.1, 0.3, 0.3)
        )
    ]
    
    # Digital era country (fast reforms)
    digital_events = [
        ReformEvent(
            event_id="reform_1",
            event_type="constitutional_amendment",
            date=datetime(2015, 1, 1),
            description="Digital rights amendment",
            iusspace_before=IusSpaceVector(0.6, 0.5, 0.7, 0.6, 0.15, 0.7, 0.6, 0.7, 0.0, 0.2, 0.8, 0.9),
            iusspace_after=IusSpaceVector(0.7, 0.6, 0.8, 0.7, 0.10, 0.8, 0.7, 0.8, 0.0, 0.2, 0.85, 0.95)
        ),
        ReformEvent(
            event_id="reform_2",
            event_type="new_law",
            date=datetime(2017, 6, 1),
            description="Data protection law",
            iusspace_before=IusSpaceVector(0.7, 0.6, 0.8, 0.7, 0.10, 0.8, 0.7, 0.8, 0.0, 0.2, 0.85, 0.95),
            iusspace_after=IusSpaceVector(0.75, 0.65, 0.85, 0.75, 0.08, 0.85, 0.75, 0.85, 0.0, 0.2, 0.87, 0.97)
        ),
        ReformEvent(
            event_id="reform_3",
            event_type="court_ruling",
            date=datetime(2020, 3, 1),
            description="Landmark privacy ruling",
            iusspace_before=IusSpaceVector(0.75, 0.65, 0.85, 0.75, 0.08, 0.85, 0.75, 0.85, 0.0, 0.2, 0.87, 0.97),
            iusspace_after=IusSpaceVector(0.8, 0.7, 0.9, 0.8, 0.06, 0.9, 0.8, 0.9, 0.0, 0.15, 0.9, 0.98)
        )
    ]
    
    # Initialize calculator
    calculator = ReformVelocityCalculator()
    
    print("=" * 80)
    print("Reform Velocity Analysis")
    print("=" * 80)
    
    # Analyze pre-digital country
    print("\n1. Pre-Digital Era Country (1850-1895):")
    print("-" * 80)
    result_pre = calculator.calculate_velocity(pre_digital_events)
    print(f"Current Velocity: {result_pre['current_velocity']:.4f} reforms/year")
    print(f"Normalized Velocity (D9): {result_pre['normalized_velocity']:.3f}")
    print(f"Mean Velocity: {result_pre['mean_velocity']:.4f} reforms/year")
    print(f"Era: {result_pre['era']}")
    print(f"Era Baseline: {result_pre['era_baseline']:.1f} years")
    print(f"Interpretation: {result_pre['interpretation']}")
    
    # Analyze digital era country
    print("\n2. Digital Era Country (2015-2020):")
    print("-" * 80)
    result_digital = calculator.calculate_velocity(digital_events)
    print(f"Current Velocity: {result_digital['current_velocity']:.4f} reforms/year")
    print(f"Normalized Velocity (D9): {result_digital['normalized_velocity']:.3f}")
    print(f"Mean Velocity: {result_digital['mean_velocity']:.4f} reforms/year")
    print(f"Acceleration: {result_digital['acceleration']:.4f} (positive = speeding up)")
    print(f"Era: {result_digital['era']}")
    print(f"Era Baseline: {result_digital['era_baseline']:.1f} years")
    print(f"Interpretation: {result_digital['interpretation']}")
    
    # Compare velocities
    print("\n3. Velocity Comparison:")
    print("-" * 80)
    comparison = calculator.compare_velocities(
        "Digital Era Country", result_digital['current_velocity'],
        "Pre-Digital Country", result_pre['current_velocity']
    )
    print(f"{comparison['interpretation']}")
    print(f"Acceleration Factor: {comparison['ratio']:.1f}x")
    
    print("\n" + "=" * 80)
    print("Key Finding Validation:")
    print("-" * 80)
    print(f"Pre-digital: {1/result_pre['current_velocity']:.1f} years per reform")
    print(f"Digital: {1/result_digital['current_velocity']:.1f} years per reform")
    print(f"Expected (from paper): 45 years → 3.2 years (14x speedup)")
    print(f"Observed: {comparison['ratio']:.1f}x speedup")
