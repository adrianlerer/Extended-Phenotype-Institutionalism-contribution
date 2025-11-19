"""
Evidence Gatherer for Evidence-First Multi-Hypothesis (EFM) System
Parallel execution of all available analytical tools

This module implements Phase 1 of the EFM architecture:
1. Execute all 7 tools in parallel (async)
2. Cache results for hypothesis synthesis
3. Provide structured evidence for verification

Key Principle: Evidence FIRST, hypotheses SECOND
(NOT TiDAR's generation-first approach)

Tools integrated:
- CLI Calculator (constitutional lock-in)
- PSM Analyzer (causal inference)
- Bootstrap Validator (statistical robustness)
- Iusmorfos Predictor (transplant success)
- RootFinder (genealogical tracing)
- Memespace (doctrinal competition)
- Fibonacci Analyzer (H/V → φ convergence)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json

# Import all tool modules
from mcp_server.tools import (
    iusmorfos_tools,
    psm_tools,
    bootstrap_tools,
    fibonacci_tools,
    rootfinder_tools,
    memespace_tools
)

@dataclass
class EvidenceCache:
    """
    Cached evidence from all tool executions.
    
    This is the "source of truth" for hypothesis synthesis.
    All hypotheses must be grounded in this evidence.
    """
    # Metadata
    timestamp: str
    case_id: str
    jurisdiction: str
    
    # Tool results (Optional because not all tools may succeed)
    cli_result: Optional[Dict[str, Any]] = None
    psm_result: Optional[Dict[str, Any]] = None
    bootstrap_result: Optional[Dict[str, Any]] = None
    iusmorfos_result: Optional[Dict[str, Any]] = None
    rootfinder_result: Optional[Dict[str, Any]] = None
    memespace_result: Optional[Dict[str, Any]] = None
    fibonacci_result: Optional[Dict[str, Any]] = None
    
    # Execution diagnostics
    execution_time_ms: float = 0.0
    tools_succeeded: int = 0
    tools_failed: int = 0
    error_log: List[str] = None
    
    def __post_init__(self):
        if self.error_log is None:
            self.error_log = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    def get_available_evidence(self) -> Dict[str, Dict[str, Any]]:
        """
        Get only non-None evidence results.
        
        Returns:
            Dict mapping tool_name → result
        """
        evidence = {}
        
        if self.cli_result:
            evidence['cli'] = self.cli_result
        if self.psm_result:
            evidence['psm'] = self.psm_result
        if self.bootstrap_result:
            evidence['bootstrap'] = self.bootstrap_result
        if self.iusmorfos_result:
            evidence['iusmorfos'] = self.iusmorfos_result
        if self.rootfinder_result:
            evidence['rootfinder'] = self.rootfinder_result
        if self.memespace_result:
            evidence['memespace'] = self.memespace_result
        if self.fibonacci_result:
            evidence['fibonacci'] = self.fibonacci_result
        
        return evidence

class EvidenceGatherer:
    """
    Parallel evidence gathering from all analytical tools.
    
    Design principles:
    1. Evidence-first (gather before generating hypotheses)
    2. Parallel execution (maximize throughput)
    3. Graceful degradation (partial evidence OK)
    4. Caching (avoid re-execution)
    """
    
    def __init__(self):
        self.cache: Dict[str, EvidenceCache] = {}
    
    async def gather_all_evidence_async(
        self,
        case_data: Dict[str, Any],
        case_id: str,
        jurisdiction: str
    ) -> EvidenceCache:
        """
        Execute all tools in parallel and cache results.
        
        Args:
            case_data: Input data for tools (varies by tool requirements)
            case_id: Unique identifier for this case
            jurisdiction: Jurisdiction name
        
        Returns:
            EvidenceCache with all tool results
        """
        start_time = datetime.now()
        
        # Check cache first
        if case_id in self.cache:
            return self.cache[case_id]
        
        # Initialize cache entry
        cache = EvidenceCache(
            timestamp=datetime.now().isoformat(),
            case_id=case_id,
            jurisdiction=jurisdiction
        )
        
        # Create async tasks for all tools
        tasks = {
            'cli': self._execute_cli(case_data, cache),
            'psm': self._execute_psm(case_data, cache),
            'bootstrap': self._execute_bootstrap(case_data, cache),
            'iusmorfos': self._execute_iusmorfos(case_data, cache),
            'rootfinder': self._execute_rootfinder(case_data, cache),
            'memespace': self._execute_memespace(case_data, cache),
            'fibonacci': self._execute_fibonacci(case_data, cache)
        }
        
        # Execute all in parallel
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        # Process results
        for tool_name, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                cache.error_log.append(f"{tool_name}: {str(result)}")
                cache.tools_failed += 1
            else:
                cache.tools_succeeded += 1
        
        # Calculate execution time
        end_time = datetime.now()
        cache.execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        # Cache result
        self.cache[case_id] = cache
        
        return cache
    
    def gather_all_evidence(
        self,
        case_data: Dict[str, Any],
        case_id: str,
        jurisdiction: str
    ) -> EvidenceCache:
        """
        Synchronous wrapper for async evidence gathering.
        
        Use this in non-async contexts.
        """
        return asyncio.run(
            self.gather_all_evidence_async(case_data, case_id, jurisdiction)
        )
    
    # ========== TOOL EXECUTORS (Async) ==========
    
    async def _execute_cli(
        self,
        case_data: Dict[str, Any],
        cache: EvidenceCache
    ) -> None:
        """Execute CLI Calculator"""
        try:
            # CLI calculation is synchronous, wrap in executor
            loop = asyncio.get_event_loop()
            
            # Extract CLI components from case_data
            components = case_data.get('cli_components', {})
            
            if not components:
                # Use defaults if not provided
                components = {
                    "TV": case_data.get('treaty_veto', 0.0),
                    "JA": case_data.get('judicial_activism', 0.0),
                    "TH": case_data.get('threshold_high', 0.0),
                    "PW": case_data.get('precedent_weight', 0.0),
                    "AD": case_data.get('amendment_difficulty', 0.0)
                }
            
            # Calculate CLI
            cli_score = sum([
                0.25 * components.get('TV', 0.0),
                0.25 * components.get('JA', 0.0),
                0.20 * components.get('TH', 0.0),
                0.15 * components.get('PW', 0.0),
                0.15 * components.get('AD', 0.0)
            ])
            
            cache.cli_result = {
                "cli_score": cli_score,
                "components": components,
                "classification": "high" if cli_score > 0.70 else "moderate" if cli_score > 0.50 else "low"
            }
            
        except Exception as e:
            cache.error_log.append(f"CLI: {str(e)}")
            raise
    
    async def _execute_psm(
        self,
        case_data: Dict[str, Any],
        cache: EvidenceCache
    ) -> None:
        """Execute PSM Analyzer"""
        try:
            # PSM requires treatment/outcome data
            psm_data = case_data.get('psm_data')
            
            if not psm_data:
                cache.psm_result = {"skipped": "No PSM data provided"}
                return
            
            # This would call actual PSM tool
            # For now, placeholder
            cache.psm_result = {
                "att": None,
                "status": "Would execute PSM with provided data"
            }
            
        except Exception as e:
            cache.error_log.append(f"PSM: {str(e)}")
            raise
    
    async def _execute_bootstrap(
        self,
        case_data: Dict[str, Any],
        cache: EvidenceCache
    ) -> None:
        """Execute Bootstrap Validator"""
        try:
            # Bootstrap validation requires correlation/regression data
            bootstrap_data = case_data.get('bootstrap_data')
            
            if not bootstrap_data:
                cache.bootstrap_result = {"skipped": "No bootstrap data provided"}
                return
            
            cache.bootstrap_result = {
                "status": "Would execute bootstrap validation"
            }
            
        except Exception as e:
            cache.error_log.append(f"Bootstrap: {str(e)}")
            raise
    
    async def _execute_iusmorfos(
        self,
        case_data: Dict[str, Any],
        cache: EvidenceCache
    ) -> None:
        """Execute Iusmorfos Predictor"""
        try:
            # Get jurisdiction profiles
            source = case_data.get('source_jurisdiction')
            target = case_data.get('target_jurisdiction', cache.jurisdiction)
            
            if not source:
                cache.iusmorfos_result = {"skipped": "No source jurisdiction provided"}
                return
            
            # Calculate cultural distance
            result = iusmorfos_tools.calculate_cultural_distance(source, target)
            
            # Add transplant prediction if CLI available
            if cache.cli_result:
                prediction = iusmorfos_tools.predict_transplant_success(
                    concept=case_data.get('concept', 'Reform'),
                    source=source,
                    target=target,
                    cli_target=cache.cli_result['cli_score']
                )
                result['transplant_prediction'] = prediction
            
            cache.iusmorfos_result = result
            
        except Exception as e:
            cache.error_log.append(f"Iusmorfos: {str(e)}")
            raise
    
    async def _execute_rootfinder(
        self,
        case_data: Dict[str, Any],
        cache: EvidenceCache
    ) -> None:
        """Execute RootFinder"""
        try:
            # RootFinder requires citation network
            citation_network = case_data.get('citation_network')
            target_case = case_data.get('target_case')
            
            if not citation_network or not target_case:
                cache.rootfinder_result = {"skipped": "No citation network provided"}
                return
            
            # Trace lineage
            result = rootfinder_tools.trace_lineage(
                case_id=target_case,
                citation_network=citation_network,
                max_depth=3
            )
            
            cache.rootfinder_result = result
            
        except Exception as e:
            cache.error_log.append(f"RootFinder: {str(e)}")
            raise
    
    async def _execute_memespace(
        self,
        case_data: Dict[str, Any],
        cache: EvidenceCache
    ) -> None:
        """Execute Memespace Analyzer"""
        try:
            # Memespace requires doctrinal competition data
            doctrines = case_data.get('doctrines')
            
            if not doctrines:
                cache.memespace_result = {"skipped": "No doctrinal data provided"}
                return
            
            cache.memespace_result = {
                "status": "Would execute Lotka-Volterra competition analysis"
            }
            
        except Exception as e:
            cache.error_log.append(f"Memespace: {str(e)}")
            raise
    
    async def _execute_fibonacci(
        self,
        case_data: Dict[str, Any],
        cache: EvidenceCache
    ) -> None:
        """Execute Fibonacci Analyzer"""
        try:
            # Get H/V values
            h_values = case_data.get('h_values', [])
            v_values = case_data.get('v_values', [])
            
            if not h_values or not v_values:
                # Use defaults if not provided
                hv_ratio = case_data.get('hv_ratio', 2.0)
            else:
                hv_ratio = fibonacci_tools.calculate_hv_ratio(h_values, v_values)
            
            # Analyze convergence if time series provided
            if 'hv_timeseries' in case_data:
                convergence = fibonacci_tools.analyze_phi_convergence(
                    case_data['hv_timeseries'],
                    case_data.get('years')
                )
                
                cache.fibonacci_result = convergence.to_dict()
            else:
                # Single point analysis
                cache.fibonacci_result = {
                    "hv_ratio": hv_ratio,
                    "distance_to_phi": fibonacci_tools.distance_to_phi(hv_ratio),
                    "optimal": abs(fibonacci_tools.distance_to_phi(hv_ratio)) < 0.15
                }
            
            # Add reform viability if CLI available
            if cache.cli_result:
                viability = fibonacci_tools.assess_reform_viability(
                    hv_ratio,
                    cache.cli_result['cli_score']
                )
                cache.fibonacci_result['reform_viability'] = viability
            
        except Exception as e:
            cache.error_log.append(f"Fibonacci: {str(e)}")
            raise
    
    # ========== UTILITY METHODS ==========
    
    def get_cached_evidence(self, case_id: str) -> Optional[EvidenceCache]:
        """Retrieve cached evidence for a case"""
        return self.cache.get(case_id)
    
    def clear_cache(self, case_id: Optional[str] = None):
        """
        Clear evidence cache.
        
        Args:
            case_id: Specific case to clear, or None to clear all
        """
        if case_id:
            self.cache.pop(case_id, None)
        else:
            self.cache.clear()
    
    def export_evidence(self, case_id: str, filepath: str):
        """
        Export evidence cache to JSON file.
        
        Args:
            case_id: Case to export
            filepath: Output file path
        """
        cache = self.cache.get(case_id)
        if not cache:
            raise ValueError(f"No cached evidence for case_id={case_id}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cache.to_dict(), f, indent=2, ensure_ascii=False)
    
    def summarize_evidence(self, case_id: str) -> Dict[str, Any]:
        """
        Generate human-readable summary of gathered evidence.
        
        Args:
            case_id: Case to summarize
        
        Returns:
            Summary dict with key findings
        """
        cache = self.cache.get(case_id)
        if not cache:
            raise ValueError(f"No cached evidence for case_id={case_id}")
        
        summary = {
            "case_id": case_id,
            "jurisdiction": cache.jurisdiction,
            "timestamp": cache.timestamp,
            "execution_time_ms": cache.execution_time_ms,
            "tools_status": {
                "succeeded": cache.tools_succeeded,
                "failed": cache.tools_failed,
                "total": cache.tools_succeeded + cache.tools_failed
            },
            "key_findings": {}
        }
        
        # Extract key findings from each tool
        if cache.cli_result:
            summary["key_findings"]["cli"] = {
                "score": cache.cli_result.get("cli_score"),
                "classification": cache.cli_result.get("classification")
            }
        
        if cache.iusmorfos_result and 'transplant_prediction' in cache.iusmorfos_result:
            pred = cache.iusmorfos_result['transplant_prediction']
            summary["key_findings"]["transplant"] = {
                "predicted_gap": pred.get("predicted_gap"),
                "risk": pred.get("overall_risk")
            }
        
        if cache.fibonacci_result:
            summary["key_findings"]["hv_convergence"] = {
                "hv_ratio": cache.fibonacci_result.get("hv_ratio"),
                "distance_to_phi": cache.fibonacci_result.get("distance_to_phi"),
                "optimal": cache.fibonacci_result.get("optimal")
            }
        
        return summary

# ========== DEMO FUNCTION ==========

def demo_argentina_ley_bases_evidence() -> EvidenceCache:
    """
    Demo: Gather evidence for Argentina Ley Bases 2024 case.
    
    This demonstrates the Evidence-First approach:
    1. Collect all available evidence
    2. THEN synthesize hypotheses from evidence
    """
    gatherer = EvidenceGatherer()
    
    # Case data for Ley Bases 2024
    case_data = {
        # CLI components
        "cli_components": {
            "TV": 0.95,  # Treaty veto (Art 75.22)
            "JA": 0.95,  # Judicial activism (post-1994)
            "TH": 0.75,  # Threshold high (qualified majority)
            "PW": 0.95,  # Precedent weight (Vizzoti)
            "AD": 0.75   # Amendment difficulty
        },
        
        # H/V ratio
        "hv_ratio": 2.45,  # Very rigid
        
        # Transplant analysis
        "source_jurisdiction": "brazil",
        "target_jurisdiction": "argentina",
        "concept": "Labor Flexibility Reform",
        
        # Citation network (simplified)
        "citation_network": rootfinder_tools.EXAMPLE_ARGENTINA_LABOR,
        "target_case": "Vizzoti_2004"
    }
    
    # Gather evidence (synchronous for demo)
    evidence = gatherer.gather_all_evidence(
        case_data=case_data,
        case_id="ley_bases_2024",
        jurisdiction="argentina"
    )
    
    return evidence

# ========== MAIN ==========

if __name__ == "__main__":
    """
    Test Evidence Gatherer with Argentina Ley Bases 2024 case.
    
    Expected results:
    - CLI: Score ~0.88 (high)
    - Iusmorfos: Low transplant risk (Brazil → Argentina)
    - Fibonacci: H/V = 2.45, far from φ, very low reform viability
    - RootFinder: May have 0 ancestors (minimal citation network)
    """
    print("=" * 60)
    print("Evidence Gatherer - Argentina Ley Bases 2024 Demo")
    print("=" * 60)
    print()
    
    # Run demo
    evidence = demo_argentina_ley_bases_evidence()
    
    # Print results
    print(f"Case ID: {evidence.case_id}")
    print(f"Jurisdiction: {evidence.jurisdiction}")
    print(f"Execution Time: {evidence.execution_time_ms:.1f}ms")
    print(f"Tools Succeeded: {evidence.tools_succeeded}/{evidence.tools_succeeded + evidence.tools_failed}")
    print()
    
    # Print evidence collected
    print("Evidence Collected:")
    print("-" * 60)
    
    if evidence.cli_result:
        cli = evidence.cli_result
        print(f"✅ CLI Calculator:")
        print(f"   Score: {cli['cli_score']:.3f} ({cli['classification']} classification)")
        print()
    
    if evidence.iusmorfos_result and 'transplant_prediction' in evidence.iusmorfos_result:
        ius = evidence.iusmorfos_result['transplant_prediction']
        print(f"✅ Iusmorfos (Transplant):")
        print(f"   Predicted Gap: {ius['predicted_gap']:.2%} ({ius['overall_risk']} risk)")
        print(f"   Passage Probability: {ius['passage_probability']:.2%}")
        print()
    
    if evidence.fibonacci_result:
        fib = evidence.fibonacci_result
        print(f"✅ Fibonacci (H/V Convergence):")
        print(f"   H/V Ratio: {fib['hv_ratio']:.3f}")
        print(f"   Distance to φ: {fib['distance_to_phi']:.3f}")
        print(f"   Optimal: {'Yes' if fib.get('optimal') else 'No'}")
        if 'reform_viability' in fib:
            viab = fib['reform_viability']
            print(f"   Reform Viability: {viab['viability_score']:.2f} ({viab['viability_class']})")
        print()
    
    if evidence.rootfinder_result:
        root = evidence.rootfinder_result
        print(f"✅ RootFinder (Genealogy):")
        print(f"   Total Ancestors: {root['total_ancestors']}")
        
        # Handle edge case: 0 ancestors
        if root['total_ancestors'] > 0:
            print(f"   Max Generation: {root['max_generation']}")
            print(f"   Root Cases: {', '.join(root['root_cases'][:3])}")
        else:
            print(f"   Note: No genealogical ancestors found (minimal citation network)")
        print()
    
    if evidence.psm_result and not evidence.psm_result.get('skipped'):
        print(f"✅ PSM Analyzer: {evidence.psm_result}")
        print()
    
    if evidence.bootstrap_result and not evidence.bootstrap_result.get('skipped'):
        print(f"✅ Bootstrap Validator: {evidence.bootstrap_result}")
        print()
    
    if evidence.memespace_result and not evidence.memespace_result.get('skipped'):
        print(f"✅ Memespace: {evidence.memespace_result}")
        print()
    
    # Print errors if any
    if evidence.error_log:
        print("Errors:")
        print("-" * 60)
        for error in evidence.error_log:
            print(f"❌ {error}")
        print()
    
    print("=" * 60)
    print("✅ Evidence gathering complete!")
    print()
    print("Next Step: Hypothesis Synthesizer")
    print("This evidence will be used to generate 5 evidence-grounded")
    print("hypotheses about reform failure mechanisms.")
    print("=" * 60)
