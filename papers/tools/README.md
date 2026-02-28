# Internal Quality Tools (Wave 2)

**Purpose**: Automated verification tools for academic papers  
**Status**: OPERATIONAL (not mentioned in published papers - internal use only)  
**Based on**: OpenAI continuous evaluation principles

---

## 🔧 Available Tools

### 1. Reality Filter v2.0 (`reality_filter_v2.py`)

**6-layer automated verification system**

**What it checks**:
1. Citation existence (Fallos format validation)
2. Empirical claims have evidence markers
3. Quantitative claims have sources
4. Temporal consistency (no paradoxes)
5. No contradictions
6. Abstract-body alignment

**Usage**:
```bash
# Check paper at Pilot stage
python3 reality_filter_v2.py --input paper.docx --stage pilot

# Generate report file
python3 reality_filter_v2.py --input paper.txt --stage production --output report.md
```

**Output**:
- Overall score (0-100)
- Decision: EXCELLENT (≥95) | GOOD (90-94) | ACCEPTABLE (85-89) | POOR (<85)
- Layer-by-layer issues flagged

**When to use**: At **Checkpoint 2 (Pilot)** before finalizing paper

---

### 2. Chicago Format Validator (`chicago_format_validator.py`)

**Citation format compliance checker**

**What it checks**:
1. In-text citations: (Author YYYY) format
2. Bibliography entries: Chicago 17th edition
3. Title capitalization
4. Cross-references (Section X, Table Y)
5. Abstract word count (150-250 typical)

**Usage**:
```bash
# Check formatting
python3 chicago_format_validator.py --input paper.docx

# Generate report
python3 chicago_format_validator.py --input paper.txt --output format_report.md
```

**Output**:
- Overall score (0-100)
- Decision: EXCELLENT (≥97) | GOOD (90-96) | ACCEPTABLE (80-89) | POOR (<80)
- Format issues flagged

**When to use**: At **Checkpoint 3 (Production)** before submission

---

### 3. SAIJ Citation Checker (`saij_citation_checker.py`)

**Fallos citation plausibility checker**

**What it checks**:
1. Valid Fallos format (Fallos XXX:YYY)
2. Plausible tomo/page ranges
3. Estimated year based on historical data
4. Known problematic cases (e.g., Banco de la Provincia 1940)

**Usage**:
```bash
# Check all citations in paper
python3 saij_citation_checker.py --input paper.docx

# Check specific citations
python3 saij_citation_checker.py --citations "Fallos 313:1513" "Fallos 314:1738"

# Generate report
python3 saij_citation_checker.py --input paper.txt --output saij_report.md
```

**Output**:
- Total citations found
- Valid format count
- Plausible citations count
- Flagged citations (require manual SAIJ verification)

**IMPORTANT**: This tool performs plausibility checks only. **Manual SAIJ verification still required** for all citations.

**When to use**: During **Checkpoint 2 (Pilot)** as part of Reality Filter Layer 1

---

## 📋 Testing

**Run all tests**:
```bash
cd papers/tools
chmod +x test_all_tools.sh
./test_all_tools.sh
```

**Expected output**: All tests passing (100%)

---

## 🔄 Typical Workflow

### At Checkpoint 2 (Pilot Stage)

```bash
cd papers/tools

# Step 1: Run Reality Filter (comprehensive check)
python3 reality_filter_v2.py --input ../2026_Paper/PILOT_v2.docx --stage pilot --output reality_report.md

# Step 2: Review reality_report.md
# If score ≥93% → Continue to Step 3
# If score <93% → Fix issues, re-run

# Step 3: Check SAIJ citations (if paper cites Argentine cases)
python3 saij_citation_checker.py --input ../2026_Paper/PILOT_v2.docx --output saij_report.md

# Step 4: Manual SAIJ verification (go to https://www.saij.gob.ar/)
# Verify each Fallos citation exists and description matches

# Step 5: Document results in VERIFICATION_LOG.md
```

### At Checkpoint 3 (Production Stage)

```bash
# Step 1: Run Chicago Format Validator
python3 chicago_format_validator.py --input ../2026_Paper/PRODUCTION_v3.docx --output format_report.md

# Step 2: Review format_report.md
# If score ≥90% → Fix minor issues, submit
# If score <90% → Formatting revision needed
```

---

## 📊 Score Thresholds

### Reality Filter v2.0
- **95-100**: ✅ EXCELLENT - Approve for production
- **90-94**: ✅ GOOD - Minor fixes required
- **85-89**: ⚠️ ACCEPTABLE - Moderate revision needed
- **<85**: 🛑 POOR - Major revision required

### Chicago Format Validator
- **97-100**: ✅ EXCELLENT - Ready for submission
- **90-96**: ✅ GOOD - Minor fixes required
- **80-89**: ⚠️ ACCEPTABLE - Moderate revision needed
- **<80**: 🛑 POOR - Major formatting required

### SAIJ Citation Checker
- **All plausible**: ✅ Proceed to manual verification
- **Some flagged**: ⚠️ Review flagged citations carefully
- **Manual verification**: 🔴 REQUIRED for ALL citations (always)

---

## 🛠️ Dependencies

**Python 3.7+** (all tools are pure Python, no external dependencies)

**Optional** (for better DOCX extraction):
```bash
pip install python-docx  # Better DOCX parsing (optional)
```

---

## 📝 Logging & Documentation

**After running tools, document results**:

1. **VERIFICATION_LOG.md** (for Tier 3 claims):
```markdown
### [2026-XX-XX] Paper: "Your Paper Title"
**Reality Filter Score**: 94% (GOOD)
**SAIJ Citations**: 7 found, 7 verified (100%)
**Chicago Format**: 92% (GOOD)
**Decision**: ✅ CONTINUE to Production
**Verified by**: [Your name]
---
```

2. **DECISIONS_LOG.md** (for checkpoints):
```markdown
## Checkpoint 2 (Pilot)
Date: 2026-XX-XX
Reality Filter: 94% ✅
SAIJ: All verified ✅
Decision: ✅ CONTINUE to Production
```

---

## 🚨 Important Notes

1. **Not mentioned in papers**: These are internal quality tools. Do not cite in published papers.

2. **Manual verification still required**: Automated tools catch 80-90% of issues. Human review is essential.

3. **Known limitations**:
   - DOCX extraction may be imperfect (formatting artifacts)
   - SAIJ Checker uses historical ranges (not real-time SAIJ API)
   - Pattern matching can have false positives/negatives

4. **When in doubt**: Always defer to manual verification

5. **Update tools**: As you discover new patterns/errors, update the scripts accordingly

---

## 📚 References

- **OpenAI Playbook**: "From experiments to deployments" (Phase 04: Build and Scale Products)
- **Chicago Manual of Style**: 17th edition, Author-Date system
- **SAIJ Database**: https://www.saij.gob.ar/ (manual verification)

---

## 🔄 Version History

| **Version** | **Date** | **Changes** |
|-------------|----------|-------------|
| 2.0 | 2025-11-20 | Wave 2 implementation: Reality Filter v2.0, Chicago Validator, SAIJ Checker |

---

## 📞 Support

**Issues**: Document in VERIFICATION_LOG.md and update tool scripts  
**Improvements**: Add new patterns/checks as you discover them  
**Questions**: Review protocols in `papers/blueprints/` directory

---

**Last updated**: 2025-11-20  
**Status**: OPERATIONAL (Wave 2 complete)
