#!/usr/bin/env python3
"""
Chicago Format Validator - Citation Format Checker

Internal tool for verifying Chicago Manual of Style (17th ed.) compliance.
NOT mentioned in published papers.

Usage:
    python chicago_format_validator.py --input paper.docx
    python chicago_format_validator.py --input paper.txt --output report.md
"""

import re
import sys
import argparse
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class ChicagoFormatValidator:
    """Validate Chicago Manual of Style (17th ed.) author-date format"""
    
    def __init__(self, paper_text: str):
        self.paper = paper_text
        self.results = {}
        self.total_score = 0
    
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
    
    # ==================== CHECK 1: IN-TEXT CITATIONS ====================
    
    def check_intext_citations(self) -> Tuple[float, List[str]]:
        """Verify in-text citations follow (Author YYYY) or (Author YYYY, page) format"""
        issues = []
        
        # Pattern: (Author Year) or (Author Year, page)
        correct_pattern = r'\([A-Z][a-zá-ú]+(?:\s+(?:et\s+al\.|and\s+[A-Z][a-zá-ú]+))?\s+\d{4}(?:[a-z])?(?:,\s*\d+(?:-\d+)?)?\)'
        
        # Find all parenthetical citations
        all_citations = re.findall(r'\([A-Z][^\)]*\d{4}[^\)]*\)', self.paper)
        
        if not all_citations:
            issues.append("ℹ️  No in-text citations detected (unusual for academic paper)")
            return 1.0, issues
        
        correct_citations = [c for c in all_citations if re.match(correct_pattern, c)]
        
        score = len(correct_citations) / len(all_citations)
        
        # Find incorrect citations
        incorrect = [c for c in all_citations if c not in correct_citations]
        
        if incorrect:
            issues.append(f"⚠️  {len(incorrect)} citations may not follow Chicago format:")
            for cite in incorrect[:5]:  # Show first 5
                issues.append(f"   - {cite}")
            if len(incorrect) > 5:
                issues.append(f"   ... and {len(incorrect) - 5} more")
        else:
            issues.append(f"✅ All {len(all_citations)} in-text citations follow (Author YYYY) format")
        
        # Check for common errors
        if re.search(r'\[\d+\]', self.paper):
            issues.append("⚠️  Detected bracketed citations [1] - should be (Author YYYY)")
        
        if re.search(r'\(\d{4}\)', self.paper):
            issues.append("⚠️  Detected year-only citations (YYYY) - should include author")
        
        return score, issues
    
    # ==================== CHECK 2: BIBLIOGRAPHY ENTRIES ====================
    
    def check_bibliography(self) -> Tuple[float, List[str]]:
        """Verify bibliography entries follow Chicago format"""
        issues = []
        
        # Extract bibliography section
        bib_match = re.search(r'(?:bibliography|references|works cited):?(.*?)(?:\n\n\n|$)', 
                             self.paper, re.IGNORECASE | re.DOTALL)
        
        if not bib_match:
            issues.append("⚠️  Could not locate bibliography section")
            return 0.5, issues
        
        bibliography = bib_match.group(1)
        
        # Split into entries (assume entries separated by newlines)
        entries = [e.strip() for e in bibliography.split('\n') if e.strip() and len(e) > 50]
        
        if not entries:
            issues.append("⚠️  No bibliography entries found")
            return 0.0, issues
        
        # Check format: Author Last, First. Year. Title. Publisher.
        # Book pattern: Last, First. YYYY. *Title*. City: Publisher.
        # Article pattern: Last, First. YYYY. "Title." *Journal* Volume (Issue): Pages.
        
        correct_entries = 0
        
        for entry in entries:
            # Check basic elements
            has_author = bool(re.search(r'^[A-Z][a-zá-ú]+,\s+[A-Z]', entry))
            has_year = bool(re.search(r'\d{4}[a-z]?\.', entry))
            has_period_after_year = bool(re.search(r'\d{4}[a-z]?\.\s+', entry))
            
            if has_author and has_year and has_period_after_year:
                correct_entries += 1
            else:
                issues.append(f"⚠️  Potential format issue: {entry[:80]}...")
        
        score = correct_entries / len(entries) if entries else 0.0
        
        issues.append(f"📚 {correct_entries}/{len(entries)} bibliography entries follow Chicago format ({score*100:.0f}%)")
        
        # Check for common errors
        if re.search(r'\d{4}\s+[A-Z]', bibliography):  # Year not followed by period
            issues.append("⚠️  Some entries missing period after year")
        
        if not re.search(r'\*[^\*]+\*', bibliography):  # No italicized titles
            issues.append("⚠️  No italicized titles detected (books/journals should be italicized)")
        
        return score, issues
    
    # ==================== CHECK 3: CAPITALIZATION ====================
    
    def check_capitalization(self) -> Tuple[float, List[str]]:
        """Check title capitalization (sentence case for articles, title case for books)"""
        issues = []
        
        # Extract titles (in quotes for articles, italicized for books)
        article_titles = re.findall(r'"([^"]+)"', self.paper)
        
        errors = 0
        
        # Article titles should be sentence case (only first word capitalized)
        for title in article_titles:
            # Count capitalized words (excluding first word)
            words = title.split()[1:]  # Skip first word
            caps_count = sum(1 for w in words if w and w[0].isupper() and w not in ['AI', 'US', 'UK', 'DNA'])
            
            if caps_count > len(words) * 0.3:  # More than 30% capitalized (suspicious)
                errors += 1
                if len(issues) < 5:  # Show first 5
                    issues.append(f"⚠️  Title may need sentence case: \"{title[:60]}...\"")
        
        score = max(0, 1.0 - (errors * 0.05))  # -5% per error
        
        if errors == 0:
            issues.append(f"✅ Title capitalization looks correct ({len(article_titles)} titles checked)")
        else:
            issues.append(f"⚠️  {errors} potential capitalization issues (review manually)")
        
        return score, issues
    
    # ==================== CHECK 4: CROSS-REFERENCES ====================
    
    def check_cross_references(self) -> Tuple[float, List[str]]:
        """Verify all cross-references (see Section X, Table Y) are valid"""
        issues = []
        
        # Find all section references
        section_refs = re.findall(r'(?:see |Section |Appendix )\s*([IVX]+|[A-Z]|\d+)', self.paper, re.IGNORECASE)
        
        # Find all table/figure references
        table_refs = re.findall(r'(?:Table|Figure)\s+(\d+)', self.paper, re.IGNORECASE)
        
        # Extract actual sections from paper
        actual_sections = re.findall(r'^(?:Section |Appendix |#)\s*([IVX]+|[A-Z]|\d+)', self.paper, re.MULTILINE | re.IGNORECASE)
        
        # Extract actual tables/figures
        actual_tables = re.findall(r'^(?:Table|Figure)\s+(\d+)', self.paper, re.MULTILINE | re.IGNORECASE)
        
        broken_refs = 0
        
        # Check section references
        for ref in section_refs:
            if ref.upper() not in [s.upper() for s in actual_sections]:
                broken_refs += 1
                if len(issues) < 5:
                    issues.append(f"⚠️  Broken reference: Section {ref} not found")
        
        # Check table/figure references
        for ref in table_refs:
            if ref not in actual_tables:
                broken_refs += 1
                if len(issues) < 5:
                    issues.append(f"⚠️  Broken reference: Table/Figure {ref} not found")
        
        total_refs = len(section_refs) + len(table_refs)
        
        if total_refs == 0:
            score = 1.0
            issues.append("ℹ️  No cross-references detected")
        else:
            score = max(0, 1.0 - (broken_refs / total_refs))
            if broken_refs == 0:
                issues.append(f"✅ All {total_refs} cross-references are valid")
            else:
                issues.append(f"⚠️  {broken_refs}/{total_refs} cross-references may be broken")
        
        return score, issues
    
    # ==================== CHECK 5: ABSTRACT WORD COUNT ====================
    
    def check_abstract_wordcount(self) -> Tuple[float, List[str]]:
        """Verify abstract is appropriate length (150-250 words typical)"""
        issues = []
        
        # Extract abstract
        abstract_match = re.search(r'abstract:?(.*?)(?:keywords:|introduction:|section\s+i[:\.])', 
                                   self.paper[:3000], re.IGNORECASE | re.DOTALL)
        
        if not abstract_match:
            issues.append("⚠️  Could not locate abstract")
            return 0.5, issues
        
        abstract = abstract_match.group(1).strip()
        word_count = len(abstract.split())
        
        # Ideal range: 150-250 words
        if 150 <= word_count <= 250:
            score = 1.0
            issues.append(f"✅ Abstract word count: {word_count} words (ideal: 150-250)")
        elif 100 <= word_count < 150:
            score = 0.8
            issues.append(f"⚠️  Abstract word count: {word_count} words (short - consider expanding to 150+)")
        elif 250 < word_count <= 350:
            score = 0.8
            issues.append(f"⚠️  Abstract word count: {word_count} words (long - consider condensing to 250 max)")
        else:
            score = 0.5
            issues.append(f"⚠️  Abstract word count: {word_count} words (outside typical range 150-250)")
        
        return score, issues
    
    # ==================== MAIN RUNNER ====================
    
    def run_all_checks(self) -> Dict:
        """Execute all checks and calculate final score"""
        
        checks = [
            ('In-text Citations', self.check_intext_citations, 35),
            ('Bibliography Entries', self.check_bibliography, 30),
            ('Capitalization', self.check_capitalization, 15),
            ('Cross-references', self.check_cross_references, 10),
            ('Abstract Word Count', self.check_abstract_wordcount, 10),
        ]
        
        total_score = 0
        
        for check_name, check_func, weight in checks:
            score, issues = check_func()
            weighted_score = score * weight
            total_score += weighted_score
            
            self.results[check_name] = {
                'raw_score': score,
                'weighted_score': weighted_score,
                'weight': weight,
                'issues': issues
            }
        
        self.total_score = total_score
        self.results['total_score'] = total_score
        self.results['decision'] = self._get_decision(total_score)
        
        return self.results
    
    def _get_decision(self, score: float) -> Dict:
        """Determine decision based on score"""
        if score >= 97:
            return {
                'level': 'EXCELLENT',
                'action': 'Ready for submission',
                'emoji': '✅',
                'details': 'Chicago format compliance is excellent. Minor tweaks only.'
            }
        elif score >= 90:
            return {
                'level': 'GOOD',
                'action': 'Minor fixes required',
                'emoji': '✅',
                'details': 'Format is mostly compliant. Address flagged issues (1-2 hours).'
            }
        elif score >= 80:
            return {
                'level': 'ACCEPTABLE',
                'action': 'Moderate revision needed',
                'emoji': '⚠️',
                'details': 'Several formatting issues detected. Requires revision pass.'
            }
        else:
            return {
                'level': 'POOR',
                'action': 'Major formatting required',
                'emoji': '🛑',
                'details': 'Significant formatting issues. Review Chicago Manual of Style guidelines.'
            }
    
    # ==================== REPORT GENERATION ====================
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate markdown report"""
        
        report = f"""# Chicago Format Validator - Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Paper length**: {len(self.paper):,} characters

---

## Executive Summary

**Overall Score**: {self.total_score:.1f}/100

**Decision**: {self.results['decision']['emoji']} **{self.results['decision']['level']}** - {self.results['decision']['action']}

{self.results['decision']['details']}

---

## Check-by-Check Results

"""
        
        for check_name, data in self.results.items():
            if check_name in ['total_score', 'decision']:
                continue
            
            report += f"### {check_name}\n\n"
            report += f"**Raw Score**: {data['raw_score']*100:.0f}%  \n"
            report += f"**Weighted Score**: {data['weighted_score']:.1f}/{data['weight']} points  \n\n"
            report += "**Issues**:\n\n"
            
            for issue in data['issues']:
                report += f"- {issue}\n"
            
            report += "\n"
        
        report += f"""---

## Score Breakdown

| **Check** | **Weight** | **Raw Score** | **Weighted Score** |
|-----------|------------|---------------|---------------------|
"""
        
        for check_name, data in self.results.items():
            if check_name in ['total_score', 'decision']:
                continue
            report += f"| {check_name} | {data['weight']}% | {data['raw_score']*100:.0f}% | {data['weighted_score']:.1f} |\n"
        
        report += f"| **TOTAL** | **100%** | - | **{self.total_score:.1f}** |\n\n"
        
        report += """---

## Thresholds

- **97-100**: ✅ EXCELLENT - Ready for submission
- **90-96**: ✅ GOOD - Minor fixes required
- **80-89**: ⚠️ ACCEPTABLE - Moderate revision needed
- **<80**: 🛑 POOR - Major formatting required

---

## Common Chicago Format Rules (Quick Reference)

### In-text Citations
- ✅ Correct: (Gargarella 2013, 45)
- ❌ Wrong: [1], (2013), Gargarella (2013)

### Bibliography Entries

**Books**:
```
Author Last, First. Year. *Title in Italics*. City: Publisher.
```

**Journal Articles**:
```
Author Last, First. Year. "Title in Quotes." *Journal Name* Volume (Issue): Pages.
```

**Case Law (Argentine)**:
```
*Case Name*, Fallos Tomo:Página (Date). [Description]
```

### Title Capitalization
- Articles: Sentence case ("The evolution of constitutional law")
- Books: Title Case (*The Evolution of Constitutional Law*)

---

## Next Steps

"""
        
        if self.total_score >= 90:
            report += "1. ✅ Review flagged issues (if any)\n"
            report += "2. ✅ Make minor corrections (< 1 hour)\n"
            report += "3. ✅ Proceed to final submission\n"
        elif self.total_score >= 80:
            report += "1. ⚠️ Fix moderate formatting issues\n"
            report += "2. ⚠️ Review Chicago Manual of Style sections flagged above\n"
            report += "3. ⚠️ Re-run validator after fixes\n"
        else:
            report += "1. 🛑 Major formatting revision required\n"
            report += "2. 🛑 Consult Chicago Manual of Style (17th ed.)\n"
            report += "3. 🛑 Consider using citation management software (Zotero, EndNote)\n"
            report += "4. 🛑 Re-run validator after comprehensive revision\n"
        
        report += "\n---\n\n"
        report += "**Generated by**: Chicago Format Validator (Internal Quality Tool)  \n"
        report += "**Reference**: Chicago Manual of Style, 17th edition (Author-Date system)  \n"
        report += "**Note**: This tool performs automated checks. Manual review still recommended.\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 Report saved to: {output_file}")
        
        return report


# ==================== CLI INTERFACE ====================

def main():
    parser = argparse.ArgumentParser(
        description='Chicago Format Validator - Citation format checker (Internal tool)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chicago_format_validator.py --input paper.docx
  python chicago_format_validator.py --input paper.txt --output report.md
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='Input paper file (.docx or .txt)')
    parser.add_argument('--output', '-o', help='Output report file (default: stdout)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Load paper
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: File not found: {args.input}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"  Chicago Format Validator")
    print(f"{'='*60}\n")
    print(f"📄 Input: {args.input}")
    print(f"\n⏳ Running format checks...")
    
    # Extract text
    if input_path.suffix.lower() == '.docx':
        validator = ChicagoFormatValidator("")
        paper_text = validator.extract_text_from_docx(str(input_path))
    else:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            paper_text = f.read()
    
    # Run checks
    validator = ChicagoFormatValidator(paper_text)
    results = validator.run_all_checks()
    
    # Generate report
    report = validator.generate_report(args.output)
    
    if not args.output:
        print("\n" + report)
    
    # Print summary to console
    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}\n")
    print(f"{results['decision']['emoji']} Overall Score: {validator.total_score:.1f}/100")
    print(f"{results['decision']['emoji']} Decision: {results['decision']['level']} - {results['decision']['action']}")
    print(f"\n{results['decision']['details']}")
    print(f"\n{'='*60}\n")
    
    # Exit code
    if validator.total_score >= 80:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs revision


if __name__ == '__main__':
    main()
