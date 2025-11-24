"""
Transplantation Era Classifier - IusSpace Dimension 12

Classifies legal systems by the historical era in which they originated.

Key Finding (IusSpace Paper):
Different transplantation eras show distinct patterns:
- Pre-Colonial (pre-1500): Indigenous legal traditions
- Colonial (1500-1945): European legal transplants
- Post-WWII (1945-1990): Cold War ideological influence
- Digital (1990-present): Rapid diffusion via internet

Era influences:
1. Speed of subsequent reforms
2. Likelihood of hybrid systems
3. Resistance to change
4. Implementation gap magnitude

Examples:
- USA Constitution (1787): Post-Revolutionary era → moderate lock-in
- Latin America (1810-1830): Independence era → French/Spanish influence
- Africa (1960s): Decolonization era → British/French systems
- Eastern Europe (1990s): Post-Soviet era → rapid EU convergence
- Arab Spring (2011+): Democratic transition → mixed success

This is a TRIVIAL dimension - simple date-based classification.
"""

from datetime import datetime
from typing import Dict, Optional
from enum import Enum
from dataclasses import dataclass


class TransplantationEra(Enum):
    """Historical eras of legal transplantation."""
    PRE_COLONIAL = "pre_colonial"           # Before 1500
    COLONIAL = "colonial"                   # 1500-1945
    POST_WWII = "post_wwii"                # 1945-1990
    POST_COLD_WAR = "post_cold_war"        # 1990-2010
    DIGITAL = "digital"                     # 2010-present
    
    # Regional sub-eras (optional refinement)
    INDEPENDENCE_LATIN_AMERICA = "independence_latam"  # 1810-1830
    DECOLONIZATION_AFRICA = "decolonization_africa"   # 1950-1970
    POST_SOVIET = "post_soviet"                        # 1990-2000
    ARAB_SPRING = "arab_spring"                        # 2011-2015


@dataclass
class TransplantationContext:
    """
    Context of legal transplantation.
    """
    era: TransplantationEra
    normalized_score: float  # 0.0-1.0 for Dimension 12
    year: int
    description: str
    
    # Characteristics of era
    reform_velocity_modifier: float  # Multiplier for reform speed
    implementation_gap_modifier: float  # Adjustment for gap
    hybrid_likelihood: float  # Probability of hybrid systems
    resistance_to_change: float  # Lock-in factor


class TransplantationEraClassifier:
    """
    Classifies legal systems by transplantation era.
    
    This is the simplest of the 12 dimensions - pure date-based classification.
    
    Methodology:
    1. Identify origin date of legal system
    2. Map to historical era
    3. Normalize to 0.0-1.0 for Dimension 12
    4. Provide contextual characteristics
    
    Normalization:
    - Pre-1500: 0.0-0.2 (indigenous traditions)
    - 1500-1945: 0.2-0.5 (colonial transplants)
    - 1945-1990: 0.5-0.7 (post-WWII)
    - 1990-2010: 0.7-0.9 (post-Cold War)
    - 2010+: 0.9-1.0 (digital era)
    """
    
    def __init__(self):
        """Initialize Transplantation Era Classifier."""
        
        # Era definitions with year ranges
        self.era_definitions = {
            TransplantationEra.PRE_COLONIAL: {
                'year_start': 0,
                'year_end': 1500,
                'normalized_range': (0.0, 0.2),
                'description': 'Indigenous legal traditions before European colonial expansion',
                'reform_velocity_modifier': 0.3,    # Very slow reforms
                'implementation_gap_modifier': 0.8,  # Lower gap (smaller formal-informal divide)
                'hybrid_likelihood': 0.2,
                'resistance_to_change': 0.9         # High resistance
            },
            TransplantationEra.COLONIAL: {
                'year_start': 1500,
                'year_end': 1945,
                'normalized_range': (0.2, 0.5),
                'description': 'Colonial legal transplantation from European powers',
                'reform_velocity_modifier': 0.5,
                'implementation_gap_modifier': 1.2,  # Higher gap (formal vs customary)
                'hybrid_likelihood': 0.7,            # High hybridization
                'resistance_to_change': 0.7
            },
            TransplantationEra.POST_WWII: {
                'year_start': 1945,
                'year_end': 1990,
                'normalized_range': (0.5, 0.7),
                'description': 'Post-WWII reconstruction and decolonization',
                'reform_velocity_modifier': 0.8,
                'implementation_gap_modifier': 1.3,
                'hybrid_likelihood': 0.8,
                'resistance_to_change': 0.6
            },
            TransplantationEra.POST_COLD_WAR: {
                'year_start': 1990,
                'year_end': 2010,
                'normalized_range': (0.7, 0.9),
                'description': 'Post-Cold War democratic transitions',
                'reform_velocity_modifier': 1.5,
                'implementation_gap_modifier': 1.1,
                'hybrid_likelihood': 0.6,
                'resistance_to_change': 0.4
            },
            TransplantationEra.DIGITAL: {
                'year_start': 2010,
                'year_end': 2100,
                'normalized_range': (0.9, 1.0),
                'description': 'Digital era with rapid legal diffusion',
                'reform_velocity_modifier': 3.0,    # Very fast reforms
                'implementation_gap_modifier': 1.0,
                'hybrid_likelihood': 0.5,
                'resistance_to_change': 0.2         # Low resistance
            }
        }
        
        # Regional sub-era refinements
        self.regional_eras = {
            TransplantationEra.INDEPENDENCE_LATIN_AMERICA: {
                'year_start': 1810,
                'year_end': 1830,
                'parent_era': TransplantationEra.COLONIAL,
                'description': 'Latin American independence (French/Spanish influence)',
                'regions': ['latin_america', 'south_america', 'central_america']
            },
            TransplantationEra.DECOLONIZATION_AFRICA: {
                'year_start': 1950,
                'year_end': 1970,
                'parent_era': TransplantationEra.POST_WWII,
                'description': 'African decolonization (British/French systems)',
                'regions': ['africa', 'sub_saharan_africa']
            },
            TransplantationEra.POST_SOVIET: {
                'year_start': 1990,
                'year_end': 2000,
                'parent_era': TransplantationEra.POST_COLD_WAR,
                'description': 'Post-Soviet transitions (EU convergence)',
                'regions': ['eastern_europe', 'central_asia', 'caucasus']
            },
            TransplantationEra.ARAB_SPRING: {
                'year_start': 2011,
                'year_end': 2015,
                'parent_era': TransplantationEra.DIGITAL,
                'description': 'Arab Spring democratic experiments',
                'regions': ['middle_east', 'north_africa']
            }
        }
    
    def classify(
        self,
        origin_year: int,
        region: Optional[str] = None,
        return_context: bool = False
    ) -> float:
        """
        Classify legal system by transplantation era.
        
        Args:
            origin_year: Year of constitution/legal system origin
            region: Geographic region (optional, for sub-era detection)
            return_context: If True, return full context object
        
        Returns:
            float: Normalized score 0.0-1.0 (Dimension 12)
            or TransplantationContext if return_context=True
        """
        # Check for regional sub-era first
        if region:
            for sub_era, data in self.regional_eras.items():
                if (data['year_start'] <= origin_year <= data['year_end'] and
                    region.lower() in data['regions']):
                    # Use parent era for normalization
                    parent_era = data['parent_era']
                    era_data = self.era_definitions[parent_era]
                    
                    if return_context:
                        return self._create_context(
                            sub_era, origin_year, era_data, data['description']
                        )
                    else:
                        return self._normalize_year(origin_year, era_data['normalized_range'])
        
        # Standard era classification
        for era, data in self.era_definitions.items():
            if data['year_start'] <= origin_year <= data['year_end']:
                if return_context:
                    return self._create_context(era, origin_year, data, data['description'])
                else:
                    return self._normalize_year(origin_year, data['normalized_range'])
        
        # Default: treat as pre-colonial if before 1500, digital if after 2100
        if origin_year < 1500:
            era_data = self.era_definitions[TransplantationEra.PRE_COLONIAL]
        else:
            era_data = self.era_definitions[TransplantationEra.DIGITAL]
        
        if return_context:
            era = TransplantationEra.PRE_COLONIAL if origin_year < 1500 else TransplantationEra.DIGITAL
            return self._create_context(era, origin_year, era_data, era_data['description'])
        else:
            return self._normalize_year(origin_year, era_data['normalized_range'])
    
    def _normalize_year(
        self,
        year: int,
        normalized_range: tuple
    ) -> float:
        """
        Normalize year to 0.0-1.0 within era range.
        
        Linear interpolation within era's normalized range.
        """
        min_score, max_score = normalized_range
        
        # Simple midpoint for now (can refine to linear interpolation within era)
        normalized = (min_score + max_score) / 2
        
        return normalized
    
    def _create_context(
        self,
        era: TransplantationEra,
        year: int,
        era_data: Dict,
        description: str
    ) -> TransplantationContext:
        """
        Create full context object.
        """
        normalized = self._normalize_year(year, era_data['normalized_range'])
        
        return TransplantationContext(
            era=era,
            normalized_score=normalized,
            year=year,
            description=description,
            reform_velocity_modifier=era_data['reform_velocity_modifier'],
            implementation_gap_modifier=era_data['implementation_gap_modifier'],
            hybrid_likelihood=era_data['hybrid_likelihood'],
            resistance_to_change=era_data['resistance_to_change']
        )
    
    def explain_era(
        self,
        origin_year: int,
        region: Optional[str] = None
    ) -> Dict:
        """
        Explain era classification with full details.
        """
        context = self.classify(origin_year, region, return_context=True)
        
        return {
            'era': context.era.value,
            'year': context.year,
            'normalized_score': float(context.normalized_score),
            'description': context.description,
            'characteristics': {
                'reform_velocity_modifier': float(context.reform_velocity_modifier),
                'implementation_gap_modifier': float(context.implementation_gap_modifier),
                'hybrid_likelihood': float(context.hybrid_likelihood),
                'resistance_to_change': float(context.resistance_to_change)
            },
            'interpretation': self._interpret_era(context)
        }
    
    def _interpret_era(self, context: TransplantationContext) -> str:
        """
        Human-readable interpretation of era.
        """
        velocity_desc = "very fast" if context.reform_velocity_modifier >= 2.0 else \
                       "fast" if context.reform_velocity_modifier >= 1.0 else \
                       "moderate" if context.reform_velocity_modifier >= 0.6 else "slow"
        
        gap_desc = "larger" if context.implementation_gap_modifier > 1.1 else \
                  "typical" if context.implementation_gap_modifier >= 0.9 else "smaller"
        
        resistance_desc = "high" if context.resistance_to_change >= 0.7 else \
                         "moderate" if context.resistance_to_change >= 0.4 else "low"
        
        return (
            f"Legal system from {context.era.value} era ({context.year}). "
            f"Characteristics: {velocity_desc} reforms, {gap_desc} implementation gap, "
            f"{resistance_desc} resistance to change. "
            f"Hybrid system likelihood: {context.hybrid_likelihood:.0%}."
        )


# Example usage
if __name__ == "__main__":
    classifier = TransplantationEraClassifier()
    
    test_cases = [
        ("Pre-Colonial China", 1200, None),
        ("USA Constitution", 1787, "north_america"),
        ("Argentina Independence", 1816, "latin_america"),
        ("Ghana Independence", 1957, "africa"),
        ("Poland Post-Soviet", 1997, "eastern_europe"),
        ("Tunisia Arab Spring", 2014, "north_africa"),
        ("Digital Era Reform", 2023, None)
    ]
    
    print("=" * 80)
    print("Transplantation Era Classification (IusSpace Dimension 12)")
    print("=" * 80)
    
    for name, year, region in test_cases:
        print(f"\n{name} ({year}):")
        print("-" * 80)
        
        result = classifier.explain_era(year, region)
        
        print(f"Era: {result['era']}")
        print(f"Normalized Score (D12): {result['normalized_score']:.3f}")
        print(f"Description: {result['description']}")
        print(f"\nCharacteristics:")
        for char, value in result['characteristics'].items():
            print(f"  {char}: {value:.2f}")
        print(f"\n{result['interpretation']}")
    
    print("\n" + "=" * 80)
    print("Summary: Dimension 12 provides historical context for legal system origins.")
    print("Influences reform velocity, implementation gaps, and change resistance.")
    print("=" * 80)
