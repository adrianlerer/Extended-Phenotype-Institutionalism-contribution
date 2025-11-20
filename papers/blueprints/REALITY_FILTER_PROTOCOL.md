# Reality Filter Protocol v2.0

**Version**: 2.0  
**Last updated**: 2025-11-20  
**Based on**: OpenAI continuous evaluation principles + Nov 2025 SSRN paper validation

---

## Purpose

The Reality Filter is a **6-layer verification system** to detect:
1. Invented or incorrectly cited legal cases
2. Unverifiable empirical claims
3. Statistical claims without sources
4. Temporal inconsistencies (e.g., citing 1940 case for 1991 doctrine)
5. Contradictory statements
6. Abstract-body misalignment

**When to Run**: At **Checkpoint 2 (Pilot)** before finalizing paper.

---

## Layer 1: Citation Existence Check

### Goal
Verify that all cited cases actually exist in official databases (SAIJ, vLex).

### Protocol

**Automated (if SAIJ API available)**:
```python
import re
import requests

def check_fallos_existence(paper_text):
    """Extract and verify all Fallos citations"""
    pattern = r'Fallos (\d+):(\d+)'
    citations = re.findall(pattern, paper_text)
    
    results = []
    for tomo, pagina in citations:
        # Query SAIJ API
        response = requests.get(f"https://saij.gob.ar/api/fallos/{tomo}/{pagina}")
        exists = response.status_code == 200
        results.append({
            'citation': f"Fallos {tomo}:{pagina}",
            'exists': exists,
            'metadata': response.json() if exists else None
        })
    
    return results
```

**Manual (if no API)**:
1. Extract all Fallos citations: `grep -oP 'Fallos \d+:\d+' paper.txt`
2. For each citation:
   - Search SAIJ database: https://www.saij.gob.ar/
   - Verify:
     - ✅ Case exists with matching date
     - ✅ Case description matches paper's claim about it
3. Mark any mismatches as **HIGH PRIORITY ERRORS**

### Example Error (from Nov 2025 SSRN paper)

**Paper claimed**:
> "Banco de la Provincia de Buenos Aires c. Estado Nacional (1940), Fallos 186:170, interpreted 'determinate time' elastically"

**Reality**:
- ✅ Case exists: Fallos 186:170 (March 15, 1940)
- ❌ Description WRONG: Case is about fiscal immunity/federalism, NOT temporal limits

**Fix**: Remove claim or find correct case for "determinate time" interpretation.

---

## Layer 2: Empirical Claims Verification

### Goal
Verify that all factual claims are supported by evidence in the paper.

### Protocol

**Key Claims Checklist** (adapt for your paper):

- [ ] Citation counts (e.g., "Barra 0 citations, ALITT 17 citations")
  - **Verification**: Search SAIJ for exact phrase "bienestar general" + "Barra" → count results
  
- [ ] G-function fitness values (e.g., "Barra G-fitness -0.636")
  - **Verification**: Check Appendix A calculations OR reproduce with `g_function_calculator.py`
  
- [ ] Statistical significance (e.g., "17.6× mutation odds, p<0.001")
  - **Verification**: Check if Section IV cites regression table OR external study
  
- [ ] Comparative cases (e.g., "Switzerland 10 emergency invocations in 110 years")
  - **Verification**: Web search "Switzerland emergency powers history" → verify count

**Scoring**:
- 100% verified → ✅ PASS
- 90-99% verified → ⚠️ REFINE (fix unverified claims)
- <90% verified → 🛑 FAIL (major revision required)

---

## Layer 3: Quantitative Claims Must Have Sources

### Goal
Ensure every percentage, p-value, or numerical statistic is footnoted.

### Protocol

**Automated Check**:
```bash
# Extract all quantitative claims
grep -oP '\d+\.\d+%|\d+%|p\s*<\s*0\.\d+|\d+\.\d+×|\d+×' paper.txt > quantitative_claims.txt

# For each claim, check if it appears near a footnote
# (within 100 characters of a citation)
python3 check_quantitative_sources.py paper.txt
```

**Manual Check** (if automated fails):
1. Highlight all numbers in paper (Ctrl+F in Word: `[0-9]+%`)
2. For each number, verify:
   - ✅ Appears in a Table/Figure with caption
   - ✅ Has footnote citing source
   - ✅ Is calculated in Appendix A

**Common Errors**:
- "17.8-fold fitness differential" → ❌ No source → **Add**: "(see Table 1)"
- "p<0.001" → ❌ No source → **Add**: "(regression model in Appendix A.4)"

---

## Layer 4: Temporal Consistency Check

### Goal
Detect anacronismos (temporal misalignments) in legal history claims.

### Protocol

**Pattern to Check**:
- Claiming a 1940 case influenced 1991 doctrine → ✅ PLAUSIBLE (51 years later)
- Claiming a 1991 doctrine influenced 1940 case → ❌ IMPOSSIBLE (causality reversed)

**Automated Check**:
```python
import re
from datetime import datetime

def check_temporal_consistency(paper_text):
    """Detect claims of Case A (year X) influencing Case B (year Y) where X > Y"""
    
    # Extract all case mentions with years
    cases = re.findall(r'(\w+\s+c\.\s+\w+)\s+\((\d{4})\)', paper_text)
    
    # Extract all "influenced" or "based on" claims
    influences = re.findall(r'(.+?)\s+(influenced|based on|derived from)\s+(.+)', paper_text)
    
    # Check for temporal paradoxes
    errors = []
    for source_case, year_source in cases:
        for target_case, year_target in cases:
            if year_source > year_target:
                # Check if paper claims source influenced target (impossible)
                if f"{source_case} influenced {target_case}" in paper_text:
                    errors.append({
                        'source': source_case,
                        'year_source': year_source,
                        'target': target_case,
                        'year_target': year_target,
                        'error': 'Temporal causality violation'
                    })
    
    return errors
```

**Manual Check**:
1. List all cases chronologically
2. Verify any "X influenced Y" claims respect X_year < Y_year

---

## Layer 5: Contradictory Statements Detection

### Goal
Find internal contradictions (e.g., "Barra won" in Section III vs. "Barra lost" in Section V).

### Protocol

**Automated Check**:
```bash
# Search for contradictory patterns
grep -i "barra.*successful\|barra.*victory" paper.txt > barra_positive.txt
grep -i "barra.*failed\|barra.*defeat\|barra.*zero citations" paper.txt > barra_negative.txt

# If both files have content → CONTRADICTION DETECTED
```

**Manual Check**:
1. For each key doctrine (e.g., Barra, Peralta, ALITT):
   - Note all statements about its success/failure
   - Verify consistency across sections
2. For G-function values:
   - Extract all mentions of same doctrine's fitness
   - Verify values match (e.g., "Barra G=-0.636" should be consistent)

---

## Layer 6: Abstract-Body Alignment

### Goal
Ensure abstract accurately reflects paper's actual findings.

### Protocol

**Checklist** (for 150-word SSRN abstract):

- [ ] Abstract mentions **17.8-fold fitness differential** → Body shows "Peralta 17 citations vs. Barra 0 citations" calculation
- [ ] Abstract mentions **p<0.001 significance** → Body cites regression table or statistical test
- [ ] Abstract mentions **47 jurisdictions validated** → Body lists or cites comparative study
- [ ] Abstract mentions **zero fitness for Barra** → Body documents "0 favorable citations + reversal"

**Scoring**:
- 4/4 claims aligned → ✅ PASS
- 3/4 claims aligned → ⚠️ REFINE (clarify missing claim)
- <3/4 claims aligned → 🛑 FAIL (abstract misleading)

---

## Overall Scoring System

| **Layer** | **Weight** | **Score Formula** |
|-----------|------------|-------------------|
| 1. Citation Existence | 25% | (Verified citations / Total citations) × 25 |
| 2. Empirical Claims | 20% | (Verified claims / Total claims) × 20 |
| 3. Quantitative Sources | 15% | (Sourced numbers / Total numbers) × 15 |
| 4. Temporal Consistency | 15% | (100 - Errors found × 10) capped at 0-15 |
| 5. No Contradictions | 15% | (100 - Contradictions × 15) capped at 0-15 |
| 6. Abstract Alignment | 10% | (Aligned claims / 4) × 10 |

**Final Score** = Sum of all layers (0-100%)

**Decision Criteria**:
- **95-100%**: ✅ EXCELLENT - Approve for production
- **90-94%**: ✅ GOOD - Minor fixes required
- **85-89%**: ⚠️ ACCEPTABLE - Moderate revision needed
- **<85%**: 🛑 POOR - Major revision required

---

## Usage Example (Nov 2025 SSRN Paper)

**Input**: `PAPER_COMPLETE_SSRN_NOV2025.docx` (16,952 words)

**Reality Filter v1.0 Results**:

| **Layer** | **Score** | **Issues Found** |
|-----------|-----------|------------------|
| 1. Citation Existence | 21/25 (84%) | ❌ Fallos 186:170 description mismatch |
| 2. Empirical Claims | 18/20 (90%) | ⚠️ 1/9 claims missing (Switzerland count) |
| 3. Quantitative Sources | 15/15 (100%) | ✅ All sourced |
| 4. Temporal Consistency | 15/15 (100%) | ✅ No errors |
| 5. No Contradictions | 15/15 (100%) | ✅ No contradictions |
| 6. Abstract Alignment | 9/10 (90%) | ✅ 4/4 claims present |

**OVERALL**: 93/100 (93%) → ⚠️ **GOOD - MINOR REFINE REQUIRED**

**Action Taken**: 
1. Fixed Fallos 186:170 description (removed incorrect claim)
2. Verified Switzerland emergency count (10 invocations confirmed)
3. Re-ran Reality Filter on corrected version

**Corrected Version**: `PAPER_CORRECTED_FINAL_NOV2025.docx`

**Reality Filter v1.0 Results (Corrected)**:

| **Layer** | **Score** |
|-----------|-----------|
| 1. Citation Existence | 25/25 (100%) |
| 2. Empirical Claims | 20/20 (100%) |
| 3. Quantitative Sources | 15/15 (100%) |
| 4-6. (Same as before) | 39/40 (97.5%) |

**FINAL OVERALL**: 99/100 (99%) → ✅ **EXCELLENT - APPROVED FOR SSRN**

---

## Version History

| **Version** | **Date** | **Changes** |
|-------------|----------|-------------|
| 1.0 | 2025-11-19 | Initial ad-hoc verification for SSRN paper |
| 2.0 | 2025-11-20 | Formalized protocol with 6 layers + scoring system (OpenAI-inspired) |

---

## References

- OpenAI (2025). "From experiments to deployments", pp. 21-22 (Evaluation principles)
- Applied to SSRN paper "General Welfare and Common Good as ESS" (Nov 2025)
