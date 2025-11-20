#!/usr/bin/env python3
"""
Reality Filter v2.0 - Automated Paper Verification Tool

Internal tool for quality assurance. NOT mentioned in published papers.
Based on OpenAI continuous evaluation principles.

Usage:
    python reality_filter_v2.py --input paper.docx --stage pilot
    python reality_filter_v2.py --input paper.docx --stage production --output report.md
"""

import re
import sys
import argparse
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class RealityFilterV2:
    """6-layer verification system for academic papers"""
    
    def __init__(self, paper_text: str, stage: str = "pilot"):
        self.paper = paper_text
        self.stage = stage
        self.results = {}
        self.total_score = 0
        
        # Scoring weights (sum = 100)
        self.weights = {
            'citation_existence': 25,
            'empirical_claims': 20,
            'quantitative_sources': 15,
            'temporal_consistency': 15,
            'no_contradictions': 15,
            'abstract_alignment': 10
        }
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            with zipfile.ZipFile(docx_path, 'r') as docx:
                xml_content = docx.read('word/document.xml')
                text = xml_content.decode('utf-8')
                # Remove XML tags
                text = re.sub(r'<[^>]+>', ' ', text)
                return text
        except Exception as e:
            print(f"⚠️  Warning: Could not extract text from DOCX. Using raw file. Error: {e}")
            with open(docx_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    
    # ==================== LAYER 1: CITATION EXISTENCE ====================
    
    def layer1_citation_existence(self) -> Tuple[float, List[str]]:
        """Verify Fallos citations exist (pattern match only - manual SAIJ check still required)"""
        issues = []
        
        # Extract all Fallos citations
        fallos_pattern = r'Fallos\s+(\d+):(\d+)'
        citations = re.findall(fallos_pattern, self.paper, re.IGNORECASE)
        
        if not citations:
            return 1.0, ["ℹ️  No Fallos citations found (may be OK if no Argentine cases cited)"]
        
        # Check format validity
        verified = 0
        for tomo, pagina in citations:
            citation_str = f"Fallos {tomo}:{pagina}"
            
            # Basic sanity checks
            if int(tomo) < 1 or int(tomo) > 400:  # CSJN Fallos range ~1-350
                issues.append(f"⚠️  {citation_str}: Suspicious tomo number (valid range: 1-350)")
            elif int(pagina) < 1:
                issues.append(f"⚠️  {citation_str}: Invalid page number")
            else:
                verified += 1
        
        score = verified / len(citations) if citations else 1.0
        
        if score < 1.0:
            issues.append(f"📋 {len(citations) - verified}/{len(citations)} citations flagged for manual SAIJ verification")
        else:
            issues.append(f"✅ All {len(citations)} Fallos citations have valid format")
        
        issues.append(f"⚠️  MANUAL CHECK REQUIRED: Verify in SAIJ that cases exist + descriptions match")
        
        return score, issues
    
    # ==================== LAYER 2: EMPIRICAL CLAIMS ====================
    
    def layer2_empirical_claims(self) -> Tuple[float, List[str]]:
        """Check if empirical claims have evidence markers"""
        issues = []
        
        # Patterns for empirical claims
        claim_patterns = [
            (r'(\d+)\s+citations?', 'citation count'),
            (r'G[-\s]?fitness\s*=?\s*(-?\d+\.?\d*)', 'G-fitness value'),
            (r'(\d+)\s+cases?', 'case count'),
            (r'(\d+)\s+jurisdictions?', 'jurisdiction count'),
            (r'(\d+\.?\d*)\s*%\s+of\s+\w+', 'percentage claim'),
        ]
        
        total_claims = 0
        claims_with_sources = 0
        
        for pattern, claim_type in claim_patterns:
            matches = re.findall(pattern, self.paper, re.IGNORECASE)
            
            for match in matches:
                total_claims += 1
                match_str = str(match) if isinstance(match, str) else str(match[0])
                
                # Check if claim appears near a source marker
                # Look for footnote, table reference, or parenthetical citation within 100 chars
                claim_context = self._get_context(match_str, window=100)
                
                if any(marker in claim_context.lower() for marker in 
                       ['table', 'appendix', 'see section', 'calculated', 'figure', ')', ']']):
                    claims_with_sources += 1
                else:
                    issues.append(f"⚠️  Unsourced {claim_type}: '{match_str}' (add source reference)")
        
        if total_claims == 0:
            score = 1.0
            issues.append("ℹ️  No empirical claims detected (or pattern matching incomplete)")
        else:
            score = claims_with_sources / total_claims
            issues.append(f"📊 {claims_with_sources}/{total_claims} empirical claims have source markers ({score*100:.0f}%)")
        
        return score, issues
    
    # ==================== LAYER 3: QUANTITATIVE SOURCES ====================
    
    def layer3_quantitative_sources(self) -> Tuple[float, List[str]]:
        """Verify all percentages and p-values have sources"""
        issues = []
        
        # Patterns for quantitative claims
        quant_patterns = [
            r'\d+\.\d+%',
            r'\d+%',
            r'p\s*[<>=]\s*0\.\d+',
            r'\d+\.\d+×',
            r'\d+×',
            r'β\s*=\s*\d+\.\d+',
        ]
        
        total_numbers = 0
        sourced_numbers = 0
        
        for pattern in quant_patterns:
            matches = re.findall(pattern, self.paper, re.IGNORECASE)
            
            for match in matches:
                total_numbers += 1
                context = self._get_context(match, window=150)
                
                # Check for source markers
                has_source = any(marker in context.lower() for marker in 
                                ['table', 'fig', 'appendix', 'regression', 'model', 
                                 'calculation', 'see section', '(', ')'])
                
                if has_source:
                    sourced_numbers += 1
                else:
                    issues.append(f"⚠️  Unsourced number: '{match}'")
        
        if total_numbers == 0:
            score = 1.0
            issues.append("ℹ️  No quantitative claims detected")
        else:
            score = sourced_numbers / total_numbers
            issues.append(f"🔢 {sourced_numbers}/{total_numbers} quantitative claims sourced ({score*100:.0f}%)")
        
        return score, issues
    
    # ==================== LAYER 4: TEMPORAL CONSISTENCY ====================
    
    def layer4_temporal_consistency(self) -> Tuple[float, List[str]]:
        """Check for temporal paradoxes (A influenced B when A came after B)"""
        issues = []
        
        # Extract case mentions with years
        case_pattern = r'(\w+(?:\s+\w+)?)\s*\((\d{4})\)'
        cases = re.findall(case_pattern, self.paper)
        
        # Look for influence claims
        influence_patterns = [
            r'influenced',
            r'based on',
            r'derived from',
            r'following',
            r'relied on',
            r'built upon',
        ]
        
        errors = 0
        
        for i, (case1, year1) in enumerate(cases):
            year1 = int(year1)
            for j, (case2, year2) in enumerate(cases):
                if i == j:
                    continue
                year2 = int(year2)
                
                # Check if paper claims case1 influenced case2 when year1 > year2
                for pattern in influence_patterns:
                    if re.search(f'{case1}.*{pattern}.*{case2}', self.paper, re.IGNORECASE):
                        if year1 > year2:
                            errors += 1
                            issues.append(f"❌ TEMPORAL PARADOX: {case1} ({year1}) cannot {pattern} {case2} ({year2})")
        
        score = max(0, 1.0 - (errors * 0.1))  # -10% per error
        
        if errors == 0:
            issues.append(f"✅ No temporal inconsistencies detected ({len(cases)} cases checked)")
        else:
            issues.append(f"⚠️  {errors} temporal consistency error(s) found")
        
        return score, issues
    
    # ==================== LAYER 5: NO CONTRADICTIONS ====================
    
    def layer5_no_contradictions(self) -> Tuple[float, List[str]]:
        """Detect contradictory statements about key doctrines"""
        issues = []
        
        # Key terms to check for contradictions
        key_terms = ['barra', 'peralta', 'alitt', 'common good', 'general welfare', 'bien común', 'bienestar general']
        
        contradictions = 0
        
        for term in key_terms:
            # Check for positive statements
            positive_patterns = [
                f'{term}.*success',
                f'{term}.*victory',
                f'{term}.*prevailed',
                f'{term}.*favorable',
                f'{term}.*\d+\s+citations',  # Any positive citation count
            ]
            
            # Check for negative statements
            negative_patterns = [
                f'{term}.*fail',
                f'{term}.*defeat',
                f'{term}.*overruled',
                f'{term}.*reversed',
                f'{term}.*zero citations',
                f'{term}.*0 citations',
            ]
            
            has_positive = any(re.search(p, self.paper, re.IGNORECASE) for p in positive_patterns)
            has_negative = any(re.search(p, self.paper, re.IGNORECASE) for p in negative_patterns)
            
            if has_positive and has_negative:
                contradictions += 1
                issues.append(f"⚠️  Potential contradiction about '{term}': both positive and negative statements found")
        
        score = max(0, 1.0 - (contradictions * 0.15))  # -15% per contradiction
        
        if contradictions == 0:
            issues.append(f"✅ No contradictions detected ({len(key_terms)} terms checked)")
        else:
            issues.append(f"⚠️  {contradictions} potential contradiction(s) - review manually")
        
        return score, issues
    
    # ==================== LAYER 6: ABSTRACT-BODY ALIGNMENT ====================
    
    def layer6_abstract_alignment(self) -> Tuple[float, List[str]]:
        """Verify abstract mentions key findings from body"""
        issues = []
        
        # Extract abstract (assume it's in first 1000 chars or marked section)
        abstract_match = re.search(r'abstract:?(.*?)(?:keywords:|introduction:|section\s+i[:\.])', 
                                   self.paper[:2000], re.IGNORECASE | re.DOTALL)
        
        if not abstract_match:
            issues.append("⚠️  Could not locate abstract - manual check required")
            return 0.5, issues
        
        abstract = abstract_match.group(1).lower()
        body = self.paper.lower()
        
        # Key findings patterns to check
        key_findings = [
            (r'(\d+\.?\d*)[x×-]fold', 'fold fitness differential'),
            (r'p\s*[<>=]\s*0\.\d+', 'p-value'),
            (r'(\d+)\s+jurisdictions?', 'jurisdiction count'),
            (r'(\d+\.?\d*)\s*%', 'percentage'),
            (r'zero\s+(?:fitness|citations)', 'zero fitness/citations'),
        ]
        
        total_findings = 0
        aligned_findings = 0
        
        for pattern, finding_type in key_findings:
            body_matches = re.findall(pattern, body)
            abstract_matches = re.findall(pattern, abstract)
            
            if body_matches:
                total_findings += 1
                if abstract_matches:
                    aligned_findings += 1
                else:
                    issues.append(f"⚠️  {finding_type.capitalize()} in body but not in abstract")
        
        if total_findings == 0:
            score = 1.0
            issues.append("ℹ️  No quantitative findings detected in body (unusual for empirical paper)")
        else:
            score = aligned_findings / total_findings
            issues.append(f"📝 {aligned_findings}/{total_findings} key findings mentioned in abstract ({score*100:.0f}%)")
        
        return score, issues
    
    # ==================== HELPER METHODS ====================
    
    def _get_context(self, text: str, window: int = 100) -> str:
        """Get surrounding context for a text snippet"""
        match = re.search(re.escape(text), self.paper)
        if match:
            start = max(0, match.start() - window)
            end = min(len(self.paper), match.end() + window)
            return self.paper[start:end]
        return ""
    
    # ==================== MAIN RUNNER ====================
    
    def run_all_layers(self) -> Dict:
        """Execute all 6 layers and calculate final score"""
        
        layers = [
            ('Citation Existence', self.layer1_citation_existence),
            ('Empirical Claims', self.layer2_empirical_claims),
            ('Quantitative Sources', self.layer3_quantitative_sources),
            ('Temporal Consistency', self.layer4_temporal_consistency),
            ('No Contradictions', self.layer5_no_contradictions),
            ('Abstract Alignment', self.layer6_abstract_alignment),
        ]
        
        total_score = 0
        
        for layer_name, layer_func in layers:
            score, issues = layer_func()
            weighted_score = score * self.weights[layer_name.lower().replace(' ', '_')]
            total_score += weighted_score
            
            self.results[layer_name] = {
                'raw_score': score,
                'weighted_score': weighted_score,
                'weight': self.weights[layer_name.lower().replace(' ', '_')],
                'issues': issues
            }
        
        self.total_score = total_score
        self.results['total_score'] = total_score
        self.results['decision'] = self._get_decision(total_score)
        
        return self.results
    
    def _get_decision(self, score: float) -> Dict:
        """Determine decision based on score"""
        if score >= 95:
            return {
                'level': 'EXCELLENT',
                'action': 'Continue to Production',
                'emoji': '✅',
                'details': 'Paper meets all quality standards. Proceed to final formatting.'
            }
        elif score >= 90:
            return {
                'level': 'GOOD',
                'action': 'Minor refinements required',
                'emoji': '✅',
                'details': 'Paper is solid. Fix minor issues flagged above, then continue.'
            }
        elif score >= 85:
            return {
                'level': 'ACCEPTABLE',
                'action': 'Moderate revision needed',
                'emoji': '⚠️',
                'details': 'Paper has several issues. Address flagged problems before proceeding.'
            }
        else:
            return {
                'level': 'POOR',
                'action': 'Major revision required',
                'emoji': '🛑',
                'details': 'Paper has significant quality issues. Return to Draft stage and address problems systematically.'
            }
    
    # ==================== REPORT GENERATION ====================
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate markdown report"""
        
        report = f"""# Reality Filter v2.0 - Verification Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Stage**: {self.stage.upper()}  
**Paper length**: {len(self.paper):,} characters

---

## Executive Summary

**Overall Score**: {self.total_score:.1f}/100

**Decision**: {self.results['decision']['emoji']} **{self.results['decision']['level']}** - {self.results['decision']['action']}

{self.results['decision']['details']}

---

## Layer-by-Layer Results

"""
        
        for layer_name, data in self.results.items():
            if layer_name in ['total_score', 'decision']:
                continue
            
            report += f"### Layer: {layer_name}\n\n"
            report += f"**Raw Score**: {data['raw_score']*100:.0f}%  \n"
            report += f"**Weighted Score**: {data['weighted_score']:.1f}/{data['weight']} points  \n\n"
            report += "**Issues**:\n\n"
            
            for issue in data['issues']:
                report += f"- {issue}\n"
            
            report += "\n"
        
        report += f"""---

## Score Breakdown

| **Layer** | **Weight** | **Raw Score** | **Weighted Score** |
|-----------|------------|---------------|---------------------|
"""
        
        for layer_name, data in self.results.items():
            if layer_name in ['total_score', 'decision']:
                continue
            report += f"| {layer_name} | {data['weight']}% | {data['raw_score']*100:.0f}% | {data['weighted_score']:.1f} |\n"
        
        report += f"| **TOTAL** | **100%** | - | **{self.total_score:.1f}** |\n\n"
        
        report += """---

## Thresholds

- **95-100**: ✅ EXCELLENT - Approve for production
- **90-94**: ✅ GOOD - Minor fixes required
- **85-89**: ⚠️ ACCEPTABLE - Moderate revision needed
- **<85**: 🛑 POOR - Major revision required

---

## Next Steps

"""
        
        if self.total_score >= 93:
            report += "1. ✅ Address minor issues flagged above (if any)\n"
            report += "2. ✅ Proceed to Checkpoint 3 (Production)\n"
            report += "3. ✅ Run Chicago Format Validator\n"
            report += "4. ✅ Final submission prep\n"
        elif self.total_score >= 85:
            report += "1. ⚠️ Review all flagged issues\n"
            report += "2. ⚠️ Fix moderate problems (1-2 hours estimated)\n"
            report += "3. ⚠️ Re-run Reality Filter\n"
            report += "4. ⚠️ If score ≥93%, proceed to Production\n"
        else:
            report += "1. 🛑 Return to Draft stage\n"
            report += "2. 🛑 Address all critical issues\n"
            report += "3. 🛑 Consider peer review before re-submission\n"
            report += "4. 🛑 Re-run Reality Filter after major revisions\n"
        
        report += "\n---\n\n"
        report += "**Generated by**: Reality Filter v2.0 (Internal Quality Tool)  \n"
        report += "**Note**: This tool performs automated checks. Manual verification still required for:\n"
        report += "- SAIJ citation existence (Layer 1)\n"
        report += "- Substantive accuracy of claims (Layer 2)\n"
        report += "- Contextual appropriateness (all layers)\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 Report saved to: {output_file}")
        
        return report


# ==================== CLI INTERFACE ====================

def main():
    parser = argparse.ArgumentParser(
        description='Reality Filter v2.0 - Automated paper verification (Internal tool)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reality_filter_v2.py --input paper.docx --stage pilot
  python reality_filter_v2.py --input paper.txt --stage production --output report.md
  python reality_filter_v2.py --input paper.docx --verbose
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='Input paper file (.docx or .txt)')
    parser.add_argument('--stage', '-s', default='pilot', choices=['draft', 'pilot', 'production'],
                       help='Paper stage (default: pilot)')
    parser.add_argument('--output', '-o', help='Output report file (default: stdout)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Load paper
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: File not found: {args.input}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"  Reality Filter v2.0 - Paper Verification")
    print(f"{'='*60}\n")
    print(f"📄 Input: {args.input}")
    print(f"🔍 Stage: {args.stage.upper()}")
    print(f"\n⏳ Running verification...")
    
    # Extract text
    if input_path.suffix.lower() == '.docx':
        rf = RealityFilterV2("", stage=args.stage)
        paper_text = rf.extract_text_from_docx(str(input_path))
    else:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            paper_text = f.read()
    
    # Run analysis
    rf = RealityFilterV2(paper_text, stage=args.stage)
    results = rf.run_all_layers()
    
    # Generate report
    report = rf.generate_report(args.output)
    
    if not args.output:
        print("\n" + report)
    
    # Print summary to console
    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}\n")
    print(f"{results['decision']['emoji']} Overall Score: {rf.total_score:.1f}/100")
    print(f"{results['decision']['emoji']} Decision: {results['decision']['level']} - {results['decision']['action']}")
    print(f"\n{results['decision']['details']}")
    print(f"\n{'='*60}\n")
    
    # Exit code
    if rf.total_score >= 85:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs revision


if __name__ == '__main__':
    main()
