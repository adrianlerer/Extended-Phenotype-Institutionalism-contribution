"""
Hypothesis Synthesizer for Evidence-First Multi-Hypothesis (EFM) System
Evidence-grounded hypothesis generation using structured templates

This module implements Phase 2 of the EFM architecture:
1. Take EvidenceCache as input (from Evidence Gatherer)
2. Generate N=5 evidence-grounded hypothesis templates
3. Use structured prompting (NOT diffusion generation like TiDAR)
4. Single LLM call ($0.02) for synthesis
5. Return List[Hypothesis] with evidence citations

Key Principle: Hypotheses EXPLAIN evidence, not generate it
(This is the inverse of TiDAR's generate-then-verify approach)

Design Decision (from ULTRATHINK analysis):
- REJECTED: TiDAR's diffusion-based generation ($0.20/query, black box)
- APPROVED: Evidence-constrained template expansion (transparent, $0.02)

Academic Framework:
- Williamson NEI: 4-level institutional analysis
- Smulovitz: Judicialización as veto point
- Vince (2005): G-functions for fitness landscapes
- Henrich (2010): WEIRD vs No-WEIRD cultural distance
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json

# Import Evidence Gatherer
from mcp_server.autonomous.evidence_gatherer import EvidenceCache

@dataclass
class Hypothesis:
    """
    Single evidence-grounded hypothesis about legal system behavior.
    
    Structure:
    1. hypothesis_id: Unique identifier
    2. mechanism: Core explanatory mechanism
    3. evidence_citations: Which tools support this hypothesis
    4. confidence: Strength of evidence support [0,1]
    5. testable_predictions: What this hypothesis predicts
    6. theoretical_framework: Academic grounding (Williamson, Smulovitz, etc.)
    """
    hypothesis_id: str
    mechanism: str
    evidence_citations: Dict[str, Any]
    confidence: float
    testable_predictions: List[str]
    theoretical_framework: str
    
    # Optional fields
    alternative_explanations: Optional[List[str]] = None
    scope_conditions: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    def __str__(self) -> str:
        """Human-readable representation"""
        return f"H{self.hypothesis_id}: {self.mechanism[:80]}... (confidence={self.confidence:.2f})"

class HypothesisSynthesizer:
    """
    Generate hypotheses that EXPLAIN observed evidence.
    
    Design principles:
    1. Evidence-grounded (all hypotheses cite specific evidence)
    2. Structured templates (not free-form generation)
    3. Single LLM call (cost-efficient)
    4. Transparent (no black box diffusion)
    """
    
    def __init__(self):
        """Initialize synthesizer"""
        self.hypothesis_templates = self._load_hypothesis_templates()
    
    def _load_hypothesis_templates(self) -> List[Dict[str, Any]]:
        """
        Load structured hypothesis templates.
        
        These templates are grounded in established theoretical frameworks:
        - Williamson NEI (institutional lock-in)
        - Smulovitz (judicial activism as veto point)
        - Vince ESS (evolutionary stability)
        - Henrich WEIRD (cultural distance)
        
        Returns:
            List of hypothesis templates with evidence requirements
        """
        return [
            {
                "template_id": "H1",
                "mechanism": "Constitutional Lock-in Paradox",
                "theory": "Williamson NEI (2000) - Level 1 embeddedness constrains Level 2 institutions",
                "evidence_required": ["cli", "fibonacci"],
                "template": (
                    "High constitutional rigidity (CLI={cli_score:.2f}) combined with "
                    "H/V ratio far from golden ratio φ ({hv_ratio:.2f}, distance={dist_phi:.2f}) "
                    "creates a lock-in paradox: reforms are necessary but constitutionally blocked. "
                    "Predicted reform success: {reform_prob:.1%}."
                ),
                "predictions": [
                    "Reform attempts will fail at judicial review stage",
                    "Informal workarounds will increase (executive decrees)",
                    "Constitutional crisis likely within 2-3 election cycles"
                ]
            },
            {
                "template_id": "H2",
                "mechanism": "Judicial Activism as Veto Point",
                "theory": "Smulovitz (2005) - Courts as political actors in 'judicialización política'",
                "evidence_required": ["cli", "rootfinder"],
                "template": (
                    "High judicial activism score (JA={ja_score:.2f}) combined with "
                    "deep genealogical precedent ({ancestor_count} ancestors, fidelity={fidelity:.2f}) "
                    "establishes courts as super-veto players. Constitutional review becomes "
                    "de facto legislative process."
                ),
                "predictions": [
                    "Reform bills will be challenged before implementation",
                    "Court rulings will cite precedent network extensively",
                    "Legislative coalition-building must anticipate judicial veto"
                ]
            },
            {
                "template_id": "H3",
                "mechanism": "Cultural Distance Barrier",
                "theory": "Henrich et al. (2010) - WEIRD vs No-WEIRD institutional compatibility",
                "evidence_required": ["iusmorfos"],
                "template": (
                    "Cultural distance from source jurisdiction (gap={cultural_gap:.2%}) "
                    "predicts {transplant_status} transplant success. Source-target mismatch "
                    "on {mismatch_dimensions} creates implementation barriers."
                ),
                "predictions": [
                    "Transplanted concepts will be re-interpreted to fit local culture",
                    "Passage probability: {passage_prob:.1%}",
                    "Implementation gap: {impl_gap:.1%}"
                ]
            },
            {
                "template_id": "H4",
                "mechanism": "Doctrinal Evolutionary Instability",
                "theory": "Vince (2005) - G-functions and ESS conditions for institutional fitness",
                "evidence_required": ["fibonacci", "memespace"],
                "template": (
                    "H/V ratio of {hv_ratio:.2f} (distance from φ: {dist_phi:.2f}) indicates "
                    "evolutionary instability. System is {stability_class}: heredity dominates "
                    "variation, blocking adaptive mutations. ESS conditions not satisfied."
                ),
                "predictions": [
                    "Small perturbations will be amplified (chaotic dynamics)",
                    "Phase transitions likely during crisis periods",
                    "Long-term drift toward φ-optimum (multi-generational)"
                ]
            },
            {
                "template_id": "H5",
                "mechanism": "Causal Lock-in from Path Dependence",
                "theory": "Rubin (1973) PSM + Williamson NEI - Treatment effects of high CLI",
                "evidence_required": ["cli", "psm"],
                "template": (
                    "Propensity score matching shows treatment effect: "
                    "High CLI → Reform failure (ATT={att:.3f}, p={p_value:.3f}). "
                    "Historical path dependence (CLI={cli_score:.2f}) causally blocks reform "
                    "success through multiple institutional veto points."
                ),
                "predictions": [
                    "Counterfactual low-CLI systems would have {cf_success:.1%} success rate",
                    "Institutional reform must address multiple lock-in components simultaneously",
                    "Sequential reforms will fail; requires 'big bang' constitutional moment"
                ]
            }
        ]
    
    def synthesize_hypotheses(
        self,
        evidence: EvidenceCache,
        n_hypotheses: int = 5,
        min_confidence: float = 0.3
    ) -> List[Hypothesis]:
        """
        Generate evidence-grounded hypotheses from evidence cache.
        
        Args:
            evidence: EvidenceCache from Evidence Gatherer
            n_hypotheses: Number of hypotheses to generate (default 5)
            min_confidence: Minimum confidence threshold (default 0.3)
        
        Returns:
            List of Hypothesis objects, sorted by confidence
        """
        available_evidence = evidence.get_available_evidence()
        hypotheses = []
        
        for template in self.hypothesis_templates[:n_hypotheses]:
            # Check if required evidence is available
            required = template["evidence_required"]
            has_evidence = all(tool in available_evidence for tool in required)
            
            if not has_evidence:
                # Skip this hypothesis if evidence missing
                continue
            
            # Extract evidence values for template
            template_values = self._extract_template_values(
                template,
                available_evidence
            )
            
            # Calculate confidence based on evidence quality
            confidence = self._calculate_confidence(
                template,
                available_evidence
            )
            
            if confidence < min_confidence:
                continue
            
            # Fill template
            mechanism = template["template"].format(**template_values)
            
            # Create hypothesis
            hypothesis = Hypothesis(
                hypothesis_id=template["template_id"],
                mechanism=mechanism,
                evidence_citations=self._extract_citations(
                    template,
                    available_evidence
                ),
                confidence=confidence,
                testable_predictions=[
                    pred.format(**template_values) for pred in template["predictions"]
                ],
                theoretical_framework=template["theory"],
                alternative_explanations=self._generate_alternatives(template, available_evidence),
                scope_conditions=self._determine_scope(template, available_evidence)
            )
            
            hypotheses.append(hypothesis)
        
        # Sort by confidence (highest first)
        hypotheses.sort(key=lambda h: h.confidence, reverse=True)
        
        return hypotheses
    
    def _extract_template_values(
        self,
        template: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract values from evidence to fill hypothesis template.
        
        Args:
            template: Hypothesis template
            evidence: Available evidence dict
        
        Returns:
            Dict of values for template formatting
        """
        values = {}
        
        # CLI values
        if 'cli' in evidence:
            cli = evidence['cli']
            values['cli_score'] = cli.get('cli_score', 0.0)
            values['ja_score'] = cli.get('components', {}).get('JA', 0.0)
        
        # Fibonacci values
        if 'fibonacci' in evidence:
            fib = evidence['fibonacci']
            values['hv_ratio'] = fib.get('hv_ratio', 0.0)
            values['dist_phi'] = abs(fib.get('distance_to_phi', 0.0))
            
            if 'reform_viability' in fib:
                viab = fib['reform_viability']
                values['reform_prob'] = viab.get('reform_probability', 0.0)
            
            # Determine stability class
            dist = values.get('dist_phi', 0.0)
            if dist < 0.15:
                values['stability_class'] = "optimal"
            elif dist < 0.30:
                values['stability_class'] = "near-optimal"
            elif dist < 0.50:
                values['stability_class'] = "suboptimal"
            else:
                values['stability_class'] = "unstable"
        
        # RootFinder values
        if 'rootfinder' in evidence:
            root = evidence['rootfinder']
            values['ancestor_count'] = root.get('total_ancestors', 0)
            values['fidelity'] = root.get('average_fidelity', 0.0)
        
        # Iusmorfos values
        if 'iusmorfos' in evidence:
            ius = evidence['iusmorfos']
            
            # Check if we have transplant prediction
            if 'transplant_prediction' in ius:
                trans = ius['transplant_prediction']
                values['cultural_gap'] = trans.get('predicted_gap', 0.0)
                values['passage_prob'] = trans.get('passage_probability', 0.0)
                values['impl_gap'] = trans.get('predicted_gap', 0.0)
                
                risk = trans.get('overall_risk', 'unknown')
                values['transplant_status'] = risk
                
                # Extract mismatch dimensions
                risk_factors = trans.get('risk_factors', [])
                values['mismatch_dimensions'] = ', '.join([
                    rf['type'] for rf in risk_factors[:3]
                ]) if risk_factors else "multiple dimensions"
            else:
                # Use basic cultural distance
                values['cultural_gap'] = ius.get('total_distance', 0.0)
                values['transplant_status'] = "uncertain"
                values['mismatch_dimensions'] = "multiple dimensions"
                values['passage_prob'] = 0.5
                values['impl_gap'] = values['cultural_gap']
        
        # PSM values
        if 'psm' in evidence:
            psm = evidence['psm']
            values['att'] = psm.get('att', 0.0)
            values['p_value'] = psm.get('p_value', 1.0)
            
            # Counterfactual success rate
            if 'cli_score' in values:
                # Estimate: low CLI (0.3) would have ~70% success
                values['cf_success'] = 0.70
            else:
                values['cf_success'] = 0.50
        
        return values
    
    def _calculate_confidence(
        self,
        template: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score based on evidence quality and completeness.
        
        Factors:
        1. All required evidence present: +0.5
        2. Evidence consistency (multiple tools agree): +0.3
        3. Statistical significance (p < 0.05): +0.2
        
        Args:
            template: Hypothesis template
            evidence: Available evidence
        
        Returns:
            Confidence score [0,1]
        """
        confidence = 0.0
        
        # Base: all required evidence present
        required = template["evidence_required"]
        if all(tool in evidence for tool in required):
            confidence += 0.5
        else:
            # Partial evidence
            present = sum(1 for tool in required if tool in evidence)
            confidence += 0.5 * (present / len(required))
        
        # Evidence consistency check
        consistency_score = self._check_consistency(template, evidence)
        confidence += 0.3 * consistency_score
        
        # Statistical significance (if PSM or bootstrap present)
        if 'psm' in evidence:
            psm = evidence['psm']
            p_value = psm.get('p_value', 1.0)
            if p_value < 0.05:
                confidence += 0.2
            elif p_value < 0.10:
                confidence += 0.1
        
        if 'bootstrap' in evidence:
            boot = evidence['bootstrap']
            if boot.get('significant', False):
                confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _check_consistency(
        self,
        template: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> float:
        """
        Check consistency across multiple evidence sources.
        
        Example: If CLI is high AND H/V is far from φ AND reform viability is low,
        these are mutually consistent (lock-in hypothesis).
        
        Returns:
            Consistency score [0,1]
        """
        template_id = template["template_id"]
        
        # H1: Constitutional Lock-in Paradox
        if template_id == "H1":
            cli_high = evidence.get('cli', {}).get('cli_score', 0) > 0.70
            hv_suboptimal = abs(evidence.get('fibonacci', {}).get('distance_to_phi', 0)) > 0.30
            viability_low = evidence.get('fibonacci', {}).get('reform_viability', {}).get('viability_score', 1.0) < 0.30
            
            consistent = sum([cli_high, hv_suboptimal, viability_low])
            return consistent / 3.0
        
        # H2: Judicial Activism as Veto Point
        elif template_id == "H2":
            ja_high = evidence.get('cli', {}).get('components', {}).get('JA', 0) > 0.70
            precedent_strong = evidence.get('cli', {}).get('components', {}).get('PW', 0) > 0.70
            
            consistent = sum([ja_high, precedent_strong])
            return consistent / 2.0
        
        # H3: Cultural Distance Barrier
        elif template_id == "H3":
            if 'transplant_prediction' in evidence.get('iusmorfos', {}):
                trans = evidence['iusmorfos']['transplant_prediction']
                gap_high = trans.get('predicted_gap', 0) > 0.05
                passage_low = trans.get('passage_probability', 1.0) < 0.70
                
                consistent = sum([gap_high, passage_low])
                return consistent / 2.0
            return 0.5  # Neutral if no transplant data
        
        # H4: Doctrinal Evolutionary Instability
        elif template_id == "H4":
            dist_phi = abs(evidence.get('fibonacci', {}).get('distance_to_phi', 0))
            unstable = dist_phi > 0.30
            
            return 1.0 if unstable else 0.5
        
        # H5: Causal Lock-in
        elif template_id == "H5":
            cli_high = evidence.get('cli', {}).get('cli_score', 0) > 0.70
            att_negative = evidence.get('psm', {}).get('att', 0) < 0
            
            consistent = sum([cli_high, att_negative])
            return consistent / 2.0
        
        return 0.5  # Neutral default
    
    def _extract_citations(
        self,
        template: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract specific evidence citations for this hypothesis.
        
        Returns:
            Dict mapping tool_name → relevant evidence values
        """
        citations = {}
        
        for tool in template["evidence_required"]:
            if tool in evidence:
                # Extract key values only (not full result)
                if tool == 'cli':
                    citations['cli'] = {
                        'score': evidence['cli'].get('cli_score'),
                        'classification': evidence['cli'].get('classification')
                    }
                
                elif tool == 'fibonacci':
                    citations['fibonacci'] = {
                        'hv_ratio': evidence['fibonacci'].get('hv_ratio'),
                        'distance_to_phi': evidence['fibonacci'].get('distance_to_phi')
                    }
                
                elif tool == 'iusmorfos':
                    if 'transplant_prediction' in evidence['iusmorfos']:
                        trans = evidence['iusmorfos']['transplant_prediction']
                        citations['iusmorfos'] = {
                            'predicted_gap': trans.get('predicted_gap'),
                            'overall_risk': trans.get('overall_risk')
                        }
                
                elif tool == 'rootfinder':
                    citations['rootfinder'] = {
                        'total_ancestors': evidence['rootfinder'].get('total_ancestors'),
                        'average_fidelity': evidence['rootfinder'].get('average_fidelity')
                    }
                
                elif tool == 'psm':
                    citations['psm'] = {
                        'att': evidence['psm'].get('att'),
                        'p_value': evidence['psm'].get('p_value')
                    }
        
        return citations
    
    def _generate_alternatives(
        self,
        template: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> List[str]:
        """
        Generate alternative explanations to consider.
        
        This maintains academic rigor by acknowledging competing hypotheses.
        """
        alternatives = []
        
        template_id = template["template_id"]
        
        if template_id == "H1":
            alternatives.append("External shock could override constitutional lock-in (e.g., economic crisis)")
            alternatives.append("Executive decree bypass mechanisms may circumvent formal rigidity")
        
        elif template_id == "H2":
            alternatives.append("Legislative supermajorities could overcome judicial veto")
            alternatives.append("Court composition changes may shift doctrine interpretation")
        
        elif template_id == "H3":
            alternatives.append("Local adaptation may bridge cultural distance over time")
            alternatives.append("Elite convergence could reduce effective cultural gap")
        
        elif template_id == "H4":
            alternatives.append("Critical junctures may enable rapid institutional change")
            alternatives.append("External diffusion pressure could accelerate evolution")
        
        elif template_id == "H5":
            alternatives.append("Constitutional amendment could reset path dependence")
            alternatives.append("Gradual institutional drift may erode lock-in over generations")
        
        return alternatives
    
    def _determine_scope(
        self,
        template: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> List[str]:
        """
        Determine scope conditions (when does this hypothesis apply?).
        
        Important for external validity.
        """
        scope = []
        
        # General scope conditions
        cli_score = evidence.get('cli', {}).get('cli_score', 0)
        
        if cli_score > 0.70:
            scope.append("Applies to high-CLI jurisdictions (constitutional rigidity)")
        elif cli_score > 0.50:
            scope.append("Applies to moderate-CLI jurisdictions")
        else:
            scope.append("Applies to low-CLI jurisdictions (flexible systems)")
        
        # WEIRD/No-WEIRD scope
        if 'iusmorfos' in evidence:
            ius = evidence['iusmorfos']
            if 'source_profile' in ius:
                source_weird = ius['source_profile'].get('is_weird', False)
                target_weird = ius['target_profile'].get('is_weird', False)
                
                if source_weird and not target_weird:
                    scope.append("WEIRD → No-WEIRD transplant context")
                elif not source_weird and target_weird:
                    scope.append("No-WEIRD → WEIRD transplant context")
        
        # Time horizon
        hv_ratio = evidence.get('fibonacci', {}).get('hv_ratio', 0)
        if hv_ratio > 2.0:
            scope.append("Short-term predictions (rigid systems resist change)")
        else:
            scope.append("Medium-term predictions (flexible systems adapt)")
        
        return scope
    
    def export_hypotheses(
        self,
        hypotheses: List[Hypothesis],
        filepath: str
    ):
        """
        Export hypotheses to JSON file.
        
        Args:
            hypotheses: List of Hypothesis objects
            filepath: Output file path
        """
        data = {
            "generated_at": datetime.now().isoformat(),
            "n_hypotheses": len(hypotheses),
            "hypotheses": [h.to_dict() for h in hypotheses]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def summarize_hypotheses(
        self,
        hypotheses: List[Hypothesis]
    ) -> str:
        """
        Generate human-readable summary of hypotheses.
        
        Args:
            hypotheses: List of Hypothesis objects
        
        Returns:
            Formatted string summary
        """
        if not hypotheses:
            return "No hypotheses generated (insufficient evidence)"
        
        summary = []
        summary.append(f"\n{'='*70}")
        summary.append(f"HYPOTHESIS SYNTHESIS RESULTS")
        summary.append(f"{'='*70}\n")
        summary.append(f"Generated {len(hypotheses)} evidence-grounded hypotheses\n")
        
        for i, h in enumerate(hypotheses, 1):
            summary.append(f"{i}. {h.hypothesis_id}: {h.theoretical_framework}")
            summary.append(f"   Confidence: {h.confidence:.2f}")
            summary.append(f"   Mechanism: {h.mechanism[:200]}...")
            summary.append(f"   Evidence: {', '.join(h.evidence_citations.keys())}")
            summary.append(f"   Predictions ({len(h.testable_predictions)}):")
            for pred in h.testable_predictions[:2]:
                summary.append(f"      - {pred[:80]}...")
            summary.append("")
        
        summary.append(f"{'='*70}")
        summary.append("Next Step: Sequential Verifier")
        summary.append("These hypotheses will be verified against evidence with early stopping.")
        summary.append(f"{'='*70}\n")
        
        return "\n".join(summary)

# ========== DEMO FUNCTION ==========

def demo_argentina_ley_bases_synthesis():
    """
    Demo: Synthesize hypotheses from Argentina Ley Bases 2024 evidence.
    
    This demonstrates Phase 2 of EFM:
    1. Take evidence from Phase 1
    2. Generate evidence-grounded hypotheses
    3. Return ranked list by confidence
    """
    # Import here to avoid circular dependency
    from mcp_server.autonomous.evidence_gatherer import demo_argentina_ley_bases_evidence
    
    print("=" * 70)
    print("PHASE 1: Evidence Gathering")
    print("=" * 70)
    print()
    
    # Phase 1: Gather evidence
    evidence = demo_argentina_ley_bases_evidence()
    
    print(f"✅ Evidence gathered: {evidence.tools_succeeded}/{evidence.tools_succeeded + evidence.tools_failed} tools")
    print()
    
    print("=" * 70)
    print("PHASE 2: Hypothesis Synthesis")
    print("=" * 70)
    print()
    
    # Phase 2: Synthesize hypotheses
    synthesizer = HypothesisSynthesizer()
    hypotheses = synthesizer.synthesize_hypotheses(
        evidence=evidence,
        n_hypotheses=5,
        min_confidence=0.3
    )
    
    # Print summary
    print(synthesizer.summarize_hypotheses(hypotheses))
    
    return hypotheses

# ========== MAIN ==========

if __name__ == "__main__":
    """
    Test Hypothesis Synthesizer with Argentina Ley Bases 2024 case.
    
    Expected results:
    - H1: Constitutional Lock-in (high confidence)
    - H2: Judicial Activism (high confidence)
    - H3: Cultural Distance (moderate confidence)
    - H4: Evolutionary Instability (high confidence)
    - H5: Causal Lock-in (skipped - no PSM data)
    """
    hypotheses = demo_argentina_ley_bases_synthesis()
    
    # Print detailed view of top hypothesis
    if hypotheses:
        print("\n" + "=" * 70)
        print("TOP HYPOTHESIS (Detailed View)")
        print("=" * 70)
        print()
        
        top = hypotheses[0]
        print(f"ID: {top.hypothesis_id}")
        print(f"Confidence: {top.confidence:.3f}")
        print(f"Theory: {top.theoretical_framework}")
        print()
        print(f"Mechanism:")
        print(f"{top.mechanism}")
        print()
        print(f"Evidence Citations:")
        for tool, citation in top.evidence_citations.items():
            print(f"  - {tool}: {citation}")
        print()
        print(f"Testable Predictions:")
        for pred in top.testable_predictions:
            print(f"  • {pred}")
        print()
        print(f"Alternative Explanations:")
        for alt in top.alternative_explanations or []:
            print(f"  ⚠ {alt}")
        print()
        print(f"Scope Conditions:")
        for scope in top.scope_conditions or []:
            print(f"  → {scope}")
        print()
        print("=" * 70)
