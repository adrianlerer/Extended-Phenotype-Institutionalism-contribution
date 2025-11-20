#!/usr/bin/env python3
"""
SAIJ Citation Checker - Verify Argentine Case Law Citations

Internal tool for verifying Fallos citations exist in SAIJ database.
NOT mentioned in published papers.

Note: This is a simplified checker. Full verification requires manual SAIJ access.

Usage:
    python saij_citation_checker.py --input paper.docx
    python saij_citation_checker.py --citations "Fallos 313:1513" "Fallos 314:1738"
"""

import re
import sys
import argparse
import zipfile
import time
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class SAIJCitationChecker:
    """Verify Fallos citations (pattern-based + plausibility checks)"""
    
    def __init__(self):
        # Known valid Fallos ranges (based on historical data)
        self.valid_ranges = {
            # Tomo range: (min_year, max_year, typical_page_range)
            (1, 100): (1863, 1945, (1, 500)),     # Early Fallos
            (101, 200): (1945, 1950, (1, 600)),
            (201, 250): (1950, 1965, (1, 700)),
            (251, 300): (1965, 1980, (1, 1000)),
            (301, 320): (1980, 1995, (1, 2000)),
            (321, 340): (1995, 2015, (1, 3000)),
            (341, 360): (2015, 2025, (1, 4000)),
        }
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            with zipfile.ZipFile(docx_path, 'r') as docx:
                xml_content = docx.read('word/document.xml')
                text = xml_content.decode('utf-8')
                text = re.sub(r'<[^>]+>', ' ', text)
                return text
        except Exception as e:
            print(f"⚠️  Warning: Could not extract text from DOCX. Error: {e}")
            with open(docx_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    
    def extract_fallos_citations(self, text: str) -> List[Tuple[int, int, str]]:
        """Extract all Fallos citations from text"""
        pattern = r'Fallos\s+(\d+):(\d+)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        citations = []
        for tomo, pagina in matches:
            # Get context (50 chars before and after)
            match_obj = re.search(f'Fallos\\s+{tomo}:{pagina}', text, re.IGNORECASE)
            if match_obj:
                start = max(0, match_obj.start() - 50)
                end = min(len(text), match_obj.end() + 50)
                context = text[start:end].strip()
            else:
                context = ""
            
            citations.append((int(tomo), int(pagina), context))
        
        return citations
    
    def validate_citation(self, tomo: int, pagina: int) -> Dict:
        """Validate a single Fallos citation (plausibility checks)"""
        result = {
            'tomo': tomo,
            'pagina': pagina,
            'citation': f"Fallos {tomo}:{pagina}",
            'valid_format': True,
            'plausible': True,
            'estimated_year': None,
            'issues': []
        }
        
        # Check 1: Valid tomo range
        if tomo < 1 or tomo > 360:
            result['valid_format'] = False
            result['plausible'] = False
            result['issues'].append(f"❌ Tomo {tomo} out of valid range (1-360)")
            return result
        
        # Check 2: Valid page number
        if pagina < 1:
            result['valid_format'] = False
            result['plausible'] = False
            result['issues'].append(f"❌ Invalid page number: {pagina}")
            return result
        
        # Check 3: Estimate year based on tomo
        for (min_tomo, max_tomo), (min_year, max_year, (min_page, max_page)) in self.valid_ranges.items():
            if min_tomo <= tomo <= max_tomo:
                result['estimated_year'] = (min_year, max_year)
                
                # Check if page is plausible
                if pagina > max_page:
                    result['plausible'] = False
                    result['issues'].append(f"⚠️  Page {pagina} unusually high for tomo {tomo} (typical max: {max_page})")
                else:
                    result['issues'].append(f"✅ Plausible (est. year: {min_year}-{max_year})")
                
                break
        else:
            result['plausible'] = False
            result['issues'].append(f"⚠️  Tomo {tomo} outside known ranges (may be recent)")
        
        # Check 4: Known problematic cases (from Nov 2025 experience)
        known_issues = {
            (186, 170): "Case exists but is about fiscal immunity, NOT temporal limits (Banco de la Provincia error)"
        }
        
        if (tomo, pagina) in known_issues:
            result['issues'].append(f"⚠️  KNOWN ISSUE: {known_issues[(tomo, pagina)]}")
        
        return result
    
    def check_all_citations(self, citations: List[Tuple[int, int, str]]) -> Dict:
        """Check all citations and generate report"""
        results = {
            'total': len(citations),
            'valid_format': 0,
            'plausible': 0,
            'flagged': 0,
            'citations': []
        }
        
        for tomo, pagina, context in citations:
            validation = self.validate_citation(tomo, pagina)
            validation['context'] = context
            
            if validation['valid_format']:
                results['valid_format'] += 1
            if validation['plausible']:
                results['plausible'] += 1
            if not validation['plausible'] or len(validation['issues']) > 1:
                results['flagged'] += 1
            
            results['citations'].append(validation)
        
        return results
    
    def generate_report(self, results: Dict, output_file: str = None) -> str:
        """Generate markdown report"""
        
        report = f"""# SAIJ Citation Checker - Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Total Citations**: {results['total']}

---

## Executive Summary

**Valid Format**: {results['valid_format']}/{results['total']} ({results['valid_format']/results['total']*100 if results['total'] else 0:.0f}%)  
**Plausible**: {results['plausible']}/{results['total']} ({results['plausible']/results['total']*100 if results['total'] else 0:.0f}%)  
**Flagged for Review**: {results['flagged']} citations

"""
        
        if results['flagged'] == 0:
            report += "✅ **All citations passed plausibility checks**\n\n"
        else:
            report += f"⚠️  **{results['flagged']} citations flagged - manual SAIJ verification recommended**\n\n"
        
        report += "---\n\n## Citation-by-Citation Results\n\n"
        
        for i, cite in enumerate(results['citations'], 1):
            emoji = "✅" if cite['plausible'] else "⚠️"
            report += f"### {i}. {emoji} {cite['citation']}\n\n"
            
            if cite['estimated_year']:
                report += f"**Estimated Year**: {cite['estimated_year'][0]}-{cite['estimated_year'][1]}  \n"
            
            report += "**Checks**:\n\n"
            for issue in cite['issues']:
                report += f"- {issue}\n"
            
            if cite['context']:
                report += f"\n**Context**: ...{cite['context']}...\n"
            
            report += "\n"
        
        report += """---

## Manual Verification Steps (Required)

Even if all citations passed plausibility checks, **manual SAIJ verification is required**:

1. **Go to SAIJ**: https://www.saij.gob.ar/
2. **Search each Fallos citation**: Use "Búsqueda avanzada" → "Jurisprudencia"
3. **Verify**:
   - ✅ Case exists in database
   - ✅ Date matches estimated year range
   - ✅ Case description matches your paper's claim about it
4. **Document in VERIFICATION_LOG.md**

### Common Errors to Watch For

- **Description mismatch**: Case exists but your claim about its holding is wrong
  - *Example*: Banco de la Provincia (1940) is about federalism, NOT emergency powers
- **Wrong case**: You cited Fallos X:Y but meant Fallos X:Z
- **Outdated info**: Case was later reversed or modified

---

## SAIJ Search Tips

**Search string format**:
```
"Fallos de la Corte Suprema" AND "Tomo XXX" AND "Página YYY"
```

**Alternative**:
```
[Case name] AND "Fallos XXX:YYY"
```

**Verify date**: If paper claims case is from 1990, SAIJ result should show ~1990 date.

---

## Next Steps

"""
        
        if results['flagged'] == 0:
            report += "1. ✅ All citations plausible - proceed to manual SAIJ verification\n"
            report += "2. ✅ Verify case descriptions match paper claims\n"
            report += "3. ✅ Document in VERIFICATION_LOG.md\n"
        else:
            report += "1. ⚠️ Review flagged citations above\n"
            report += "2. ⚠️ Manual SAIJ verification for ALL citations (especially flagged ones)\n"
            report += "3. ⚠️ Fix any errors found\n"
            report += "4. ⚠️ Re-run checker after fixes\n"
        
        report += "\n---\n\n"
        report += "**Generated by**: SAIJ Citation Checker (Internal Quality Tool)  \n"
        report += "**Note**: This tool performs plausibility checks only. Manual SAIJ verification required for all citations.  \n"
        report += "**Accuracy**: Pattern-based validation + historical range checks. Not a replacement for manual verification.\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 Report saved to: {output_file}")
        
        return report


# ==================== CLI INTERFACE ====================

def main():
    parser = argparse.ArgumentParser(
        description='SAIJ Citation Checker - Verify Fallos citations (Internal tool)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python saij_citation_checker.py --input paper.docx
  python saij_citation_checker.py --citations "Fallos 313:1513" "Fallos 314:1738"
  python saij_citation_checker.py --input paper.txt --output report.md
  
Note: This tool performs plausibility checks. Manual SAIJ verification still required.
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--input', '-i', help='Input paper file (.docx or .txt)')
    group.add_argument('--citations', '-c', nargs='+', help='List of citations to check (e.g., "Fallos 313:1513")')
    
    parser.add_argument('--output', '-o', help='Output report file (default: stdout)')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"  SAIJ Citation Checker")
    print(f"{'='*60}\n")
    
    checker = SAIJCitationChecker()
    
    # Extract citations
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Error: File not found: {args.input}")
            sys.exit(1)
        
        print(f"📄 Input: {args.input}")
        print(f"⏳ Extracting citations...")
        
        # Extract text
        if input_path.suffix.lower() == '.docx':
            paper_text = checker.extract_text_from_docx(str(input_path))
        else:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                paper_text = f.read()
        
        citations = checker.extract_fallos_citations(paper_text)
        
    else:  # --citations
        print(f"📋 Checking {len(args.citations)} citation(s)...")
        citations = []
        for cite in args.citations:
            match = re.search(r'Fallos\s+(\d+):(\d+)', cite, re.IGNORECASE)
            if match:
                citations.append((int(match.group(1)), int(match.group(2)), ""))
            else:
                print(f"⚠️  Warning: Invalid citation format: {cite} (expected: Fallos XXX:YYY)")
    
    if not citations:
        print("❌ No Fallos citations found")
        sys.exit(1)
    
    print(f"\n✅ Found {len(citations)} Fallos citation(s)")
    print(f"⏳ Running validation checks...\n")
    
    # Check citations
    results = checker.check_all_citations(citations)
    
    # Generate report
    report = checker.generate_report(results, args.output)
    
    if not args.output:
        print("\n" + report)
    
    # Print summary to console
    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}\n")
    print(f"Total Citations: {results['total']}")
    print(f"✅ Valid Format: {results['valid_format']}/{results['total']}")
    print(f"✅ Plausible: {results['plausible']}/{results['total']}")
    print(f"⚠️  Flagged: {results['flagged']}")
    
    if results['flagged'] > 0:
        print(f"\n⚠️  {results['flagged']} citation(s) require manual SAIJ verification")
    else:
        print(f"\n✅ All citations passed plausibility checks")
    
    print(f"\n⚠️  REMINDER: Manual SAIJ verification required for ALL citations")
    print(f"   Visit: https://www.saij.gob.ar/\n")
    print(f"{'='*60}\n")
    
    # Exit code
    if results['flagged'] == 0:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs manual review


if __name__ == '__main__':
    main()
