"""
Implementation Gap Detector - Dimensión 5 del IusSpace

Mide la brecha entre la aprobación formal de leyes y su implementación real.

Del paper IusSpace (SSRN 5557838):
- WEIRD societies: 5.4% implementation gap
- Non-WEIRD societies: 31.2% implementation gap
- Cohen's d = 3.749, p < 0.0001 (one of largest documented effects)

El patrón "se acata pero no se cumple" (obey but don't comply) emerge como
el patrón GLOBAL dominante, no solo latinoamericano (85% de población mundial).

Author: Ignacio Adrián Lerer
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalProvision:
    """Estructura para una provisión legal obligatoria."""
    id: str
    text: str
    law_source: str
    enactment_date: datetime
    mandatory: bool
    deadline: Optional[datetime] = None
    penalties_specified: bool = False
    
    
@dataclass
class ComplianceRecord:
    """Estructura para registro de cumplimiento."""
    provision_id: str
    entity: str  # quién debe cumplir (gobierno, empresa, etc.)
    compliance_status: float  # 0.0 (no compliance) to 1.0 (full compliance)
    verification_date: datetime
    verification_source: str
    enforcement_actions: int = 0  # número de acciones de enforcement


class ImplementationGapDetector:
    """
    Detecta y cuantifica la brecha de implementación en sistemas legales.
    
    Implementa la Dimensión 5 del framework IusSpace, midiendo la distancia
    entre la aprobación formal de normas y su cumplimiento efectivo.
    
    Methodología:
    1. Extrae provisiones obligatorias de textos legales
    2. Verifica cumplimiento real via múltiples fuentes
    3. Calcula gap como 1 - (compliance promedio)
    4. Ajusta por factores temporales y de enforcement
    """
    
    def __init__(
        self,
        temporal_decay_rate: float = 0.1,
        enforcement_weight: float = 0.3,
        deadline_penalty: float = 0.2
    ):
        """
        Initialize Implementation Gap Detector.
        
        Args:
            temporal_decay_rate: Tasa anual de decay para compliance checks antiguos
            enforcement_weight: Peso de enforcement actions en score (0.0-1.0)
            deadline_penalty: Penalidad por deadline missed (0.0-1.0)
        """
        self.temporal_decay_rate = temporal_decay_rate
        self.enforcement_weight = enforcement_weight
        self.deadline_penalty = deadline_penalty
        
    def measure_gap(
        self,
        law_text: str,
        compliance_records: List[ComplianceRecord],
        enactment_date: datetime,
        verification_date: Optional[datetime] = None
    ) -> Dict:
        """
        Mide implementation gap para una ley específica.
        
        Args:
            law_text: Texto completo de la ley
            compliance_records: Registros de cumplimiento verificados
            enactment_date: Fecha de promulgación
            verification_date: Fecha de verificación (default: hoy)
            
        Returns:
            Dict con:
                - gap: 0.0 (perfect) to 1.0 (zero implementation)
                - provisions_count: número de provisiones obligatorias
                - compliance_rate: tasa promedio de cumplimiento
                - time_elapsed: años desde promulgación
                - enforcement_index: índice de enforcement actions
        """
        if verification_date is None:
            verification_date = datetime.now()
        
        logger.info(f"Measuring implementation gap for law enacted {enactment_date}")
        
        # 1. Extraer provisiones obligatorias
        provisions = self._extract_mandatory_provisions(law_text, enactment_date)
        logger.info(f"Extracted {len(provisions)} mandatory provisions")
        
        if not provisions:
            logger.warning("No mandatory provisions found")
            return {
                'gap': 0.0,
                'provisions_count': 0,
                'compliance_rate': 1.0,
                'time_elapsed': 0.0,
                'enforcement_index': 0.0,
                'interpretation': 'No mandatory provisions to evaluate'
            }
        
        # 2. Calcular compliance para cada provisión
        provision_compliance = {}
        for provision in provisions:
            compliance_score = self._calculate_provision_compliance(
                provision,
                compliance_records,
                verification_date
            )
            provision_compliance[provision.id] = compliance_score
        
        # 3. Calcular métricas agregadas
        compliance_rate = np.mean(list(provision_compliance.values()))
        gap = 1.0 - compliance_rate
        
        # 4. Calcular tiempo transcurrido
        time_elapsed = (verification_date - enactment_date).days / 365.25
        
        # 5. Calcular enforcement index
        enforcement_actions = sum(
            r.enforcement_actions for r in compliance_records
        )
        enforcement_index = min(1.0, enforcement_actions / (len(provisions) * 5))
        
        # 6. Interpretación cualitativa
        interpretation = self._interpret_gap(gap, time_elapsed)
        
        return {
            'gap': float(gap),
            'provisions_count': len(provisions),
            'compliance_rate': float(compliance_rate),
            'time_elapsed': float(time_elapsed),
            'enforcement_index': float(enforcement_index),
            'interpretation': interpretation,
            'provision_details': provision_compliance
        }
    
    def measure_systemic_gap(
        self,
        laws: List[Dict],
        compliance_database: pd.DataFrame,
        country: str
    ) -> Dict:
        """
        Mide implementation gap sistémico para todo un país.
        
        Args:
            laws: Lista de diccionarios con info de leyes
            compliance_database: DataFrame con compliance records
            country: Nombre del país
            
        Returns:
            Dict con gap sistémico y breakdown por sector
        """
        logger.info(f"Measuring systemic gap for {country}")
        
        gaps = []
        sector_gaps = {}
        
        for law in laws:
            # Filter compliance records para esta ley
            law_compliance = compliance_database[
                compliance_database['law_id'] == law['id']
            ]
            
            # Convert to ComplianceRecord objects
            records = [
                ComplianceRecord(
                    provision_id=row['provision_id'],
                    entity=row['entity'],
                    compliance_status=row['compliance_status'],
                    verification_date=pd.to_datetime(row['verification_date']),
                    verification_source=row['source'],
                    enforcement_actions=row.get('enforcement_actions', 0)
                )
                for _, row in law_compliance.iterrows()
            ]
            
            # Measure gap
            result = self.measure_gap(
                law_text=law['text'],
                compliance_records=records,
                enactment_date=pd.to_datetime(law['enactment_date'])
            )
            
            gaps.append(result['gap'])
            
            # Track by sector
            sector = law.get('sector', 'general')
            if sector not in sector_gaps:
                sector_gaps[sector] = []
            sector_gaps[sector].append(result['gap'])
        
        # Aggregate statistics
        systemic_gap = np.mean(gaps)
        sector_averages = {
            sector: np.mean(gaps)
            for sector, gaps in sector_gaps.items()
        }
        
        # WEIRD classification (rough heuristic)
        weird_threshold = 0.15  # 15% gap threshold
        is_weird = systemic_gap < weird_threshold
        
        return {
            'country': country,
            'systemic_gap': float(systemic_gap),
            'gap_std': float(np.std(gaps)),
            'laws_analyzed': len(laws),
            'sector_gaps': sector_averages,
            'weird_classification': {
                'is_weird': is_weird,
                'confidence': 1.0 - abs(systemic_gap - weird_threshold) / 0.5
            },
            'interpretation': self._interpret_systemic_gap(systemic_gap, is_weird)
        }
    
    def _extract_mandatory_provisions(
        self,
        law_text: str,
        enactment_date: datetime
    ) -> List[LegalProvision]:
        """
        Extrae provisiones obligatorias de texto legal.
        
        Busca patrones como:
        - "shall", "must", "obligatorio", "deberá"
        - Plazos específicos ("within 90 days", "en el plazo de")
        - Penalidades ("penalty", "sanción", "multa")
        """
        provisions = []
        
        # Split into articles/sections
        # TODO: Implement proper legal text parsing
        # For now, simple sentence-based extraction
        
        import re
        
        # Patterns for mandatory language
        mandatory_patterns = [
            r'\bshall\b',
            r'\bmust\b',
            r'\brequired to\b',
            r'\bobligatory\b',
            r'\bdeberá\b',
            r'\bobligatorio\b',
            r'\bestá obligado\b'
        ]
        
        # Deadline patterns
        deadline_patterns = [
            r'within (\d+) days',
            r'within (\d+) months',
            r'en el plazo de (\d+) días',
            r'en el plazo de (\d+) meses'
        ]
        
        # Penalty patterns
        penalty_patterns = [
            r'\bpenalty\b',
            r'\bfine\b',
            r'\bsanction\b',
            r'\bsanción\b',
            r'\bmulta\b'
        ]
        
        sentences = law_text.split('.')
        
        for idx, sentence in enumerate(sentences):
            # Check if mandatory
            is_mandatory = any(
                re.search(pattern, sentence, re.IGNORECASE)
                for pattern in mandatory_patterns
            )
            
            if is_mandatory:
                # Check for deadline
                deadline = None
                for pattern in deadline_patterns:
                    match = re.search(pattern, sentence, re.IGNORECASE)
                    if match:
                        days = int(match.group(1))
                        if 'month' in pattern or 'mes' in pattern:
                            days *= 30
                        deadline = enactment_date + timedelta(days=days)
                        break
                
                # Check for penalties
                has_penalty = any(
                    re.search(pattern, sentence, re.IGNORECASE)
                    for pattern in penalty_patterns
                )
                
                provision = LegalProvision(
                    id=f"PROV_{idx}",
                    text=sentence.strip(),
                    law_source="extracted",
                    enactment_date=enactment_date,
                    mandatory=True,
                    deadline=deadline,
                    penalties_specified=has_penalty
                )
                
                provisions.append(provision)
        
        return provisions
    
    def _calculate_provision_compliance(
        self,
        provision: LegalProvision,
        compliance_records: List[ComplianceRecord],
        verification_date: datetime
    ) -> float:
        """
        Calcula compliance score para una provisión específica.
        
        Factores:
        - Compliance status directo (0.0-1.0)
        - Temporal decay (registros antiguos valen menos)
        - Deadline penalty (si deadline pasó sin compliance)
        - Enforcement actions (más enforcement = mayor compliance esperado)
        """
        # Filter records para esta provisión
        relevant_records = [
            r for r in compliance_records
            if r.provision_id == provision.id
        ]
        
        if not relevant_records:
            # No data = assume non-compliance (conservative)
            return 0.0
        
        # Calcular weighted compliance
        weighted_scores = []
        weights = []
        
        for record in relevant_records:
            # Base compliance
            score = record.compliance_status
            
            # Temporal decay
            days_since = (verification_date - record.verification_date).days
            years_since = days_since / 365.25
            temporal_weight = np.exp(-self.temporal_decay_rate * years_since)
            
            # Enforcement adjustment
            if record.enforcement_actions > 0:
                # More enforcement actions = higher expected compliance
                enforcement_boost = min(0.2, record.enforcement_actions * 0.05)
                score += enforcement_boost
            
            weighted_scores.append(score)
            weights.append(temporal_weight)
        
        # Weighted average
        base_compliance = np.average(weighted_scores, weights=weights)
        
        # Deadline penalty
        if provision.deadline and verification_date > provision.deadline:
            deadline_missed = (verification_date - provision.deadline).days
            if deadline_missed > 0 and base_compliance < 1.0:
                penalty = min(self.deadline_penalty, deadline_missed / 365.25 * 0.1)
                base_compliance -= penalty
        
        return max(0.0, min(1.0, base_compliance))
    
    def _interpret_gap(self, gap: float, time_elapsed: float) -> str:
        """
        Interpreta el gap de implementación.
        """
        if gap < 0.10:
            category = "Excellent implementation (WEIRD-like pattern)"
        elif gap < 0.25:
            category = "Good implementation (above global average)"
        elif gap < 0.40:
            category = "Moderate gap (typical Non-WEIRD pattern)"
        elif gap < 0.60:
            category = "Significant gap ('se acata pero no se cumple')"
        else:
            category = "Severe implementation failure"
        
        if time_elapsed < 1.0:
            time_context = "Early stage - gap may improve"
        elif time_elapsed < 3.0:
            time_context = "Typical implementation window"
        else:
            time_context = "Mature implementation period - gap unlikely to close"
        
        return f"{category}. {time_context} ({time_elapsed:.1f} years since enactment)."
    
    def _interpret_systemic_gap(self, systemic_gap: float, is_weird: bool) -> str:
        """
        Interpreta el gap sistémico de un país.
        """
        weird_status = "WEIRD" if is_weird else "Non-WEIRD"
        
        if is_weird:
            if systemic_gap < 0.10:
                return f"{weird_status} society with excellent implementation culture (gap: {systemic_gap:.1%})"
            else:
                return f"{weird_status} society with atypically high gap (gap: {systemic_gap:.1%}) - investigate causes"
        else:
            if systemic_gap > 0.40:
                return f"{weird_status} society with severe implementation challenges (gap: {systemic_gap:.1%}) - structural reforms needed"
            else:
                return f"{weird_status} society with typical gap (gap: {systemic_gap:.1%}) - matches global Non-WEIRD average (31.2%)"


# Example usage and testing
if __name__ == "__main__":
    detector = ImplementationGapDetector()
    
    # Example: Labor reform in Argentina (Non-WEIRD)
    law_text = """
    Article 1. All employers shall implement health and safety protocols 
    within 90 days of this law's enactment.
    
    Article 2. Companies must submit quarterly compliance reports to the 
    Labor Ministry. Failure to comply results in fines of $10,000-$50,000.
    
    Article 3. Workers shall receive mandatory training on new safety procedures.
    """
    
    enactment_date = datetime(2023, 1, 1)
    verification_date = datetime(2024, 11, 1)
    
    # Mock compliance records
    compliance_records = [
        ComplianceRecord(
            provision_id="PROV_0",
            entity="Company A",
            compliance_status=0.4,  # 40% compliance
            verification_date=datetime(2024, 6, 1),
            verification_source="Labor Ministry inspection",
            enforcement_actions=2
        ),
        ComplianceRecord(
            provision_id="PROV_1",
            entity="Company B",
            compliance_status=0.6,  # 60% compliance
            verification_date=datetime(2024, 8, 1),
            verification_source="Self-reported",
            enforcement_actions=0
        ),
        ComplianceRecord(
            provision_id="PROV_2",
            entity="Company C",
            compliance_status=0.2,  # 20% compliance
            verification_date=datetime(2024, 10, 1),
            verification_source="Union complaint",
            enforcement_actions=1
        )
    ]
    
    result = detector.measure_gap(
        law_text=law_text,
        compliance_records=compliance_records,
        enactment_date=enactment_date,
        verification_date=verification_date
    )
    
    print("\n" + "="*80)
    print("IMPLEMENTATION GAP ANALYSIS")
    print("="*80)
    print(f"\nLaw enacted: {enactment_date.strftime('%Y-%m-%d')}")
    print(f"Verification date: {verification_date.strftime('%Y-%m-%d')}")
    print(f"Time elapsed: {result['time_elapsed']:.1f} years")
    print(f"\nMandatory provisions found: {result['provisions_count']}")
    print(f"Average compliance rate: {result['compliance_rate']:.1%}")
    print(f"Implementation gap: {result['gap']:.1%}")
    print(f"Enforcement index: {result['enforcement_index']:.2f}")
    print(f"\nInterpretation: {result['interpretation']}")
    
    # Example comparison: WEIRD vs Non-WEIRD
    print("\n" + "="*80)
    print("WEIRD VS NON-WEIRD COMPARISON (from IusSpace paper)")
    print("="*80)
    print(f"WEIRD societies (e.g., USA, Germany):     5.4% average gap")
    print(f"Non-WEIRD societies (e.g., Argentina):   31.2% average gap")
    print(f"Statistical significance: p < 0.0001, Cohen's d = 3.749")
    print(f"\nThis example ({result['gap']:.1%} gap) is {'WEIRD-like' if result['gap'] < 0.15 else 'Non-WEIRD typical'}")
