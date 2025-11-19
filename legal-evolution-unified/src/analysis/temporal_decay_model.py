"""
Temporal Decay Model (TDM)
===========================

Predicts legislative policy lifespan with confidence intervals.

This is the core unique advantage of the framework: forecasting WHEN policies
will be reversed, not just IF they will pass.

Mathematical Foundation:
    L(t) = L₀ × e^(-λt) × Π(1 - P_trigger_i)
    
    Where:
    - L(t) = Legitimacy/survival probability at time t
    - L₀ = Initial legitimacy (from ESS fitness or default 1.0)
    - λ = Base decay rate (from Velocity + RRI + Friction Score)
    - P_trigger_i = Probability of trigger event i

Author: Constitutional Evolution Framework
Date: 2025-11-04
Version: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import warnings


class TemporalDecayModel:
    """
    Predicts legislative lifespan with confidence intervals.
    
    The core unique advantage of this framework.
    """
    
    def __init__(self, historical_data_path: Optional[str] = None):
        """
        Initialize Temporal Decay Model.
        
        Args:
            historical_data_path: Path to CSV with historical cases
                                  (case_id, country, year_enacted, year_reversed, 
                                   actual_lifespan, velocity, rri, friction_score, eci)
        """
        self.historical_cases = None
        if historical_data_path:
            try:
                self.historical_cases = pd.read_csv(historical_data_path)
            except FileNotFoundError:
                warnings.warn(f"Historical data not found: {historical_data_path}")
        
        self.trigger_catalogue = self._load_trigger_catalogue()
        self.decay_functions = {
            'exponential': lambda t, λ: np.exp(-λ * t),
            'power_law': lambda t, α: t ** (-α) if t > 0 else 1.0,
            'step_function': lambda t, T: 1.0 if t < T else 0.0,
            'logistic': lambda t, k, t_mid: 1 / (1 + np.exp(k * (t - t_mid)))
        }
    
    def predict_lifespan(self,
                         bill_id: str,
                         country: str,
                         year: int,
                         velocity: float,
                         rri: float,
                         friction_score: float,
                         eci: float = 0.70,
                         judicial_review_risk: float = 0.15,
                         bill_type: str = 'legislation',
                         initial_legitimacy: float = 1.0) -> Dict[str, Any]:
        """
        Main prediction method.
        
        Args:
            bill_id: Unique identifier (e.g., 'ARG-2025-EXPORT-TAX')
            country: Country name
            year: Year of analysis
            velocity: Constitutional Velocity (overrulings/year)
            rri: Regulatory Risk Index (0-1)
            friction_score: Friction Score (0-3)
            eci: Elite Cohesion Index (0-1), default 0.70
            judicial_review_risk: Probability of judicial challenge (0-1)
            bill_type: Type of bill ('legislation', 'constitutional_doctrine', etc.)
            initial_legitimacy: L₀ parameter (0-1), default 1.0
        
        Returns:
            Dict with:
            - base_decay_rate
            - base_half_life_years
            - decay_function
            - scenario_analysis (list of scenarios)
            - weighted_expected_lifespan
            - survival_probability_by_year
            - early_warning_indicators
            - comparable_historical_cases
        """
        
        # Calculate base decay rate
        λ = self._calculate_decay_rate(velocity, rri, friction_score)
        
        # Calculate base half-life
        if λ > 0:
            half_life = np.log(2) / λ
        else:
            half_life = np.inf  # Effectively permanent
        
        # Select decay function
        decay_func_name = self._select_decay_function(
            bill_type, friction_score, judicial_review_risk
        )
        
        # Generate scenario analysis
        scenarios = self._generate_scenarios(
            half_life, eci, velocity, rri, judicial_review_risk, initial_legitimacy
        )
        
        # Calculate weighted expected lifespan
        weighted_lifespan = sum(s['probability'] * s['expected_lifespan'] 
                               for s in scenarios)
        
        # Calculate median and mode
        lifespans = [s['expected_lifespan'] for s in scenarios]
        probabilities = [s['probability'] for s in scenarios]
        
        # Weighted median (approximate)
        sorted_indices = np.argsort(lifespans)
        sorted_lifespans = np.array(lifespans)[sorted_indices]
        sorted_probs = np.array(probabilities)[sorted_indices]
        cumsum_probs = np.cumsum(sorted_probs)
        median_idx = np.where(cumsum_probs >= 0.5)[0][0]
        median_lifespan = sorted_lifespans[median_idx]
        
        # Mode (most likely scenario)
        mode_idx = np.argmax(probabilities)
        mode_lifespan = lifespans[mode_idx]
        
        # Standard deviation
        variance = sum(s['probability'] * (s['expected_lifespan'] - weighted_lifespan) ** 2 
                      for s in scenarios)
        std_deviation = np.sqrt(variance)
        
        # Generate survival probability curve
        survival_curve = self._generate_survival_curve(
            λ, self.decay_functions[decay_func_name], scenarios, initial_legitimacy
        )
        
        # Identify early warning indicators
        early_warnings = self._identify_early_warnings(
            eci, velocity, rri, friction_score
        )
        
        # Find comparable historical cases
        comparable = self._find_comparable_cases(
            country, velocity, rri, friction_score, bill_type
        )
        
        return {
            'bill_id': bill_id,
            'country': country,
            'year': year,
            'base_decay_rate': round(λ, 4),
            'base_half_life_years': round(half_life, 1) if half_life != np.inf else 'infinite',
            'decay_function': decay_func_name,
            'scenario_analysis': scenarios,
            'weighted_expected_lifespan': round(weighted_lifespan, 1),
            'median_lifespan': round(median_lifespan, 1),
            'mode_lifespan': round(mode_lifespan, 1),
            'std_deviation': round(std_deviation, 1),
            'survival_probability_by_year': survival_curve,
            'early_warning_indicators': early_warnings,
            'comparable_historical_cases': comparable,
            'metadata': {
                'model_version': '1.0',
                'prediction_date': pd.Timestamp.now().isoformat(),
                'parameters': {
                    'velocity': velocity,
                    'rri': rri,
                    'friction_score': friction_score,
                    'eci': eci,
                    'judicial_review_risk': judicial_review_risk
                }
            }
        }
    
    def _calculate_decay_rate(self, V: float, RRI: float, FS: float) -> float:
        """
        Calculate base decay rate λ.
        
        Formula: λ = (V / 10) × (1 - RRI) × (1 - FS/3)
        
        ADJUSTMENT: For very low friction (FS < 0.2), amplify decay rate by 1.5x
        because policies with no institutional barriers reverse faster.
        
        Args:
            V: Constitutional Velocity (0-10+)
            RRI: Regulatory Risk Index (0-1)
            FS: Friction Score (0-3)
        
        Returns:
            Decay rate λ (per year)
        """
        # Normalize inputs
        V_norm = V / 10  # Normalize velocity to 0-1 scale
        FS_norm = min(FS, 3) / 3  # Normalize friction to 0-1 scale
        
        λ = V_norm * (1 - RRI) * (1 - FS_norm)
        
        # ADJUSTMENT: Low friction amplification
        if FS < 0.2:
            λ *= 1.5  # Executive orders, easy reversals
        
        return max(λ, 0.001)  # Minimum decay rate to avoid division by zero
    
    def _select_decay_function(self, bill_type: str, FS: float, 
                                judicial_risk: float) -> str:
        """
        Select appropriate decay function shape.
        
        Args:
            bill_type: Type of legislation
            FS: Friction Score
            judicial_risk: Probability of judicial review
        
        Returns:
            Decay function name
        """
        if judicial_risk > 0.70:
            return 'step_function'  # Likely to be struck down suddenly
        elif FS > 1.5:
            return 'power_law'  # Institutional inertia protects
        elif bill_type == 'constitutional_doctrine':
            return 'power_law'  # Doctrines evolve slowly
        else:
            return 'exponential'  # Default for most legislation
    
    def _generate_scenarios(self, base_half_life: float, eci: float,
                            velocity: float, rri: float, judicial_risk: float,
                            initial_legitimacy: float) -> List[Dict]:
        """
        Generate 5-7 scenarios with probabilities and trigger events.
        
        Args:
            base_half_life: Base half-life in years
            eci: Elite Cohesion Index
            velocity: Constitutional Velocity
            rri: Regulatory Risk Index
            judicial_risk: Judicial review probability
            initial_legitimacy: Initial legitimacy L₀
        
        Returns:
            List of scenario dicts
        """
        scenarios = []
        
        # Scenario 1: No trigger events (baseline)
        scenarios.append({
            'scenario': 'No trigger events',
            'probability': 0.20,
            'trigger_events': [],
            'legitimacy_impact': 0.0,
            'expected_lifespan': base_half_life,
            'confidence_interval_80': [
                round(base_half_life * 0.75, 1),
                round(base_half_life * 1.35, 1)
            ]
        })
        
        # Scenario 2: ECI drop
        if eci > 0.65:
            eci_drop_prob = 0.30
            scenarios.append({
                'scenario': f'ECI drop to {round(eci - 0.15, 2)}',
                'probability': eci_drop_prob,
                'trigger_events': ['ECI_DROP_0.15'],
                'legitimacy_impact': -0.30,
                'expected_lifespan': round(base_half_life * 0.70, 1),
                'confidence_interval_80': [
                    round(base_half_life * 0.70 * 0.75, 1),
                    round(base_half_life * 0.70 * 1.35, 1)
                ]
            })
        
        # Scenario 3: Judicial review
        if judicial_risk > 0.15:
            scenarios.append({
                'scenario': 'Supreme Court challenge',
                'probability': judicial_risk,
                'trigger_events': ['JUDICIAL_REVIEW'],
                'legitimacy_impact': -0.50,
                'expected_lifespan': round(base_half_life * 0.50, 1),
                'confidence_interval_80': [
                    round(base_half_life * 0.50 * 0.75, 1),
                    round(base_half_life * 0.50 * 1.35, 1)
                ]
            })
        
        # Scenario 4: Economic crisis
        scenarios.append({
            'scenario': 'Economic crisis (GDP < -2%)',
            'probability': 0.15,
            'trigger_events': ['ECONOMIC_CRISIS'],
            'legitimacy_impact': -0.35,
            'expected_lifespan': round(base_half_life * 0.65, 1),
            'confidence_interval_80': [
                round(base_half_life * 0.65 * 0.75, 1),
                round(base_half_life * 0.65 * 1.35, 1)
            ]
        })
        
        # Scenario 5: Electoral turnover
        scenarios.append({
            'scenario': 'Electoral turnover (opposition wins)',
            'probability': 0.25,
            'trigger_events': ['ELECTORAL_TURNOVER'],
            'legitimacy_impact': -0.25,
            'expected_lifespan': round(base_half_life * 0.75, 1),
            'confidence_interval_80': [
                round(base_half_life * 0.75 * 0.75, 1),
                round(base_half_life * 0.75 * 1.35, 1)
            ]
        })
        
        # Normalize probabilities to sum to 1.0
        total_prob = sum(s['probability'] for s in scenarios)
        for s in scenarios:
            s['probability'] = round(s['probability'] / total_prob, 2)
        
        return scenarios
    
    def _generate_survival_curve(self, λ: float, decay_func, 
                                  scenarios: List[Dict],
                                  initial_legitimacy: float) -> Dict:
        """
        Generate survival probability for years 1-10.
        
        Args:
            λ: Decay rate
            decay_func: Decay function (callable)
            scenarios: List of scenarios
            initial_legitimacy: L₀
        
        Returns:
            Dict mapping year → survival probability
        """
        survival = {}
        for year in range(1, 11):
            # Weighted average across scenarios
            prob = 0
            for s in scenarios:
                # Apply decay function
                if 'exponential' in str(decay_func):
                    scenario_prob = decay_func(year, λ) * initial_legitimacy
                else:
                    scenario_prob = decay_func(year, λ)
                
                # Apply trigger event impact
                legitimacy_multiplier = 1 + s['legitimacy_impact']
                prob += s['probability'] * scenario_prob * legitimacy_multiplier
            
            survival[f'year_{year}'] = round(max(prob, 0), 2)
        
        return survival
    
    def _identify_early_warnings(self, eci: float, velocity: float,
                                  rri: float, fs: float) -> List[Dict]:
        """
        Identify which indicators to monitor and at what frequency.
        
        Args:
            eci: Elite Cohesion Index
            velocity: Constitutional Velocity
            rri: Regulatory Risk Index
            fs: Friction Score
        
        Returns:
            List of early warning indicator dicts
        """
        warnings = []
        
        if eci > 0.65:
            warnings.append({
                'indicator': 'Elite Cohesion Index',
                'current_value': eci,
                'critical_threshold': 0.65,
                'monitor_frequency': 'Quarterly',
                'lead_time_months': 6
            })
        
        if velocity > 2.0:
            warnings.append({
                'indicator': 'Constitutional Velocity',
                'current_value': velocity,
                'critical_threshold': 4.0,
                'monitor_frequency': 'Annual',
                'lead_time_months': 12
            })
        
        if rri < 0.50:
            warnings.append({
                'indicator': 'Regulatory Risk Index',
                'current_value': rri,
                'critical_threshold': 0.50,
                'monitor_frequency': 'Quarterly',
                'lead_time_months': 6
            })
        
        warnings.append({
            'indicator': 'GDP Growth',
            'current_value': 'TBD',  # Would pull from IMF data
            'critical_threshold': -2.0,
            'monitor_frequency': 'Quarterly',
            'lead_time_months': 3
        })
        
        return warnings
    
    def _find_comparable_cases(self, country: str, velocity: float, rri: float,
                                fs: float, bill_type: str) -> List[Dict]:
        """
        Find historical cases with similar profiles.
        
        Args:
            country: Country name
            velocity: Constitutional Velocity
            rri: Regulatory Risk Index
            fs: Friction Score
            bill_type: Type of bill
        
        Returns:
            List of comparable case dicts
        """
        if self.historical_cases is None:
            return []
        
        # Calculate similarity score for each historical case
        similar_cases = []
        
        for _, case in self.historical_cases.iterrows():
            # Skip if different country (unless we want cross-country comparisons)
            if case.get('country') != country:
                continue
            
            # Calculate Euclidean distance in (V, RRI, FS) space
            v_dist = (case.get('velocity', 0) - velocity) ** 2
            rri_dist = (case.get('rri', 0) - rri) ** 2
            fs_dist = (case.get('friction_score', 0) - fs) ** 2
            
            distance = np.sqrt(v_dist + rri_dist + fs_dist)
            
            # Only include cases within reasonable similarity threshold
            if distance < 2.0:  # Adjust threshold as needed
                similar_cases.append({
                    'case_id': case.get('case_id'),
                    'actual_lifespan': case.get('actual_lifespan_years'),
                    'similarity_score': round(1 / (1 + distance), 2),
                    'trigger_events_realized': case.get('trigger_events_realized', []),
                    'notes': case.get('notes', '')
                })
        
        # Sort by similarity and return top 3
        similar_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar_cases[:3]
    
    def _load_trigger_catalogue(self) -> Dict:
        """
        Load catalogue of trigger events with probabilities and impacts.
        
        Returns:
            Dict mapping trigger_event_id → properties
        """
        return {
            'ECI_DROP_0.15': {
                'base_probability': 0.25,
                'legitimacy_impact': -0.30,
                'description': 'Elite Cohesion Index drops by 0.15 or more'
            },
            'JUDICIAL_REVIEW': {
                'base_probability': 0.15,
                'legitimacy_impact': -0.50,
                'description': 'Supreme Court strikes down or significantly limits'
            },
            'ELECTORAL_TURNOVER': {
                'base_probability': 0.25,
                'legitimacy_impact': -0.25,
                'description': 'Opposition party wins executive or legislative control'
            },
            'ECONOMIC_CRISIS': {
                'base_probability': 0.12,
                'legitimacy_impact': -0.35,
                'description': 'GDP growth < -2% for two consecutive quarters'
            },
            'SOCIAL_MOVEMENT': {
                'base_probability': 0.18,
                'legitimacy_impact': -0.30,
                'description': 'Large-scale protests (>100K participants)'
            },
            'COALITION_FRAGMENTATION': {
                'base_probability': 0.20,
                'legitimacy_impact': -0.35,
                'description': 'Governing coalition loses supermajority or splits'
            }
        }
    
    def validate_predictions(self, test_cases_path: str) -> Dict[str, float]:
        """
        Validate TDM predictions against historical test cases.
        
        Args:
            test_cases_path: Path to CSV with test cases
                            (must have actual_lifespan_years column)
        
        Returns:
            Dict with validation metrics (MAE, RMSE, accuracy_within_2years)
        """
        test_cases = pd.read_csv(test_cases_path)
        
        predictions = []
        actuals = []
        
        for _, case in test_cases.iterrows():
            # Make prediction
            result = self.predict_lifespan(
                bill_id=case['case_id'],
                country=case['country'],
                year=case['year_enacted'],
                velocity=case.get('velocity', 2.0),
                rri=case.get('rri', 0.50),
                friction_score=case.get('friction_score', 0.50),
                eci=case.get('eci', 0.70),
                judicial_review_risk=case.get('judicial_review_risk', 0.15)
            )
            
            predicted = result['weighted_expected_lifespan']
            actual = case['actual_lifespan_years']
            
            predictions.append(predicted)
            actuals.append(actual)
        
        # Calculate metrics
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        
        errors = np.abs(predictions - actuals)
        mae = np.mean(errors)
        rmse = np.sqrt(np.mean((predictions - actuals) ** 2))
        accuracy_within_2years = np.mean(errors <= 2.0)
        
        return {
            'MAE': round(mae, 2),
            'RMSE': round(rmse, 2),
            'accuracy_within_2years': round(accuracy_within_2years, 2),
            'sample_size': len(test_cases),
            'predictions': predictions.tolist(),
            'actuals': actuals.tolist(),
            'errors': errors.tolist()
        }


# Convenience function for quick analysis
def predict_lifespan_quick(country: str, year: int, velocity: float, 
                           rri: float, friction_score: float, **kwargs) -> Dict:
    """
    Quick lifespan prediction without instantiating class.
    
    Example:
        result = predict_lifespan_quick(
            country='Argentina',
            year=2025,
            velocity=4.1,
            rri=0.58,
            friction_score=0.52,
            eci=0.72
        )
    """
    tdm = TemporalDecayModel()
    return tdm.predict_lifespan(
        bill_id=f"{country}-{year}-ANALYSIS",
        country=country,
        year=year,
        velocity=velocity,
        rri=rri,
        friction_score=friction_score,
        **kwargs
    )
