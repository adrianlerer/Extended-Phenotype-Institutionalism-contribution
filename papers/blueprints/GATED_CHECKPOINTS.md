# Gated Checkpoints for Academic Papers

**Version**: 1.0  
**Last updated**: 2025-11-20  
**Based on**: OpenAI "From experiments to deployments" (Phase 04)

---

## Purpose

This template defines 3 mandatory checkpoints for academic paper production:
1. **MVP**: Validate core logic and argument structure
2. **PILOT**: Verify all empirical claims and citations
3. **PRODUCTION**: Finalize formatting and prepare for submission

Each checkpoint has:
- Clear **goal**
- Specific **measurements**
- Explicit **decision criteria** (Continue / Refine / Stop)

---

## Checkpoint 1: Draft MVP (7,000-10,000 words)

### Goal
Validate that the paper's core argument is sound and worth developing further.

### Scope Requirements
- [ ] Introduction with clear research question
- [ ] Section II-III: Theoretical framework (EGT, G-function)
- [ ] Section IV: At least 2 case studies with preliminary analysis
- [ ] Basic bibliography (15-20 key references)

### Measurements

| **Metric** | **Threshold** | **How to Measure** |
|------------|---------------|---------------------|
| Core G-function logic is consistent | Pass/Fail | Manual review: Check all G(s,E) calculations use same formula |
| Argument structure is coherent | Pass/Fail | Peer review (1 SME): "Does Section IV follow logically from Section III?" |
| Key citations are real | 100% | Quick check: Verify 5 random citations exist (Google Scholar) |

### Decision Criteria

- **✅ CONTINUE** if:
  - Core logic passes
  - Argument structure is coherent
  - All sampled citations are real

- **⚠️ REFINE** if:
  - Minor inconsistencies in G-function (fixable in < 2 hours)
  - Argument needs restructuring but foundation is solid
  
- **🛑 STOP** if:
  - Core logic is fundamentally flawed
  - Argument cannot be salvaged without complete rewrite

### Who Decides
- Primary author + 1 SME reviewer

### Estimated Time at This Stage
- Writing: 30-40 hours
- Review: 2 hours
- Decision meeting: 30 minutes

---

## Checkpoint 2: Pilot (12,000-15,000 words + Appendix)

### Goal
Verify all empirical claims are accurate and the paper is ready for final polish.

### Scope Requirements
- [ ] All sections (I-VII) drafted
- [ ] Appendix A (Methodology) complete
- [ ] Full bibliography (30-40 references)
- [ ] All tables/figures integrated
- [ ] Abstract (draft version)

### Measurements

| **Metric** | **Threshold** | **How to Measure** |
|------------|---------------|---------------------|
| All empirical claims verifiable | 95%+ | **Reality Filter v2.0** (6-layer verification) |
| All Fallos citations exist | 100% | SAIJ database check (manual or automated) |
| G-function values are consistent across paper | Pass/Fail | Cross-reference check (grep all G-values) |
| Quantitative claims have sources | 100% | Pattern match: Every "X%" or "p<0.XX" has footnote |
| No invented cases detected | 100% | Manual check: Verify 3 random case descriptions against SAIJ |

### Evaluation Protocol

**Run Reality Filter v2.0** (see `REALITY_FILTER_PROTOCOL.md`):

```bash
cd papers/tools
python3 reality_filter_v2.py --input ../2026_WIP_Paper/PILOT_v2.docx --stage pilot
```

Expected output:
```
✅ CHECK 1: Citation existence - 38/40 verified (95%)
⚠️ CHECK 2: Fallos citations - 6/7 exist (85.7%) 
   ERROR: "Fallos 186:170" description mismatch
✅ CHECK 3: G-function consistency - PASS
✅ CHECK 4: Quantitative claims - 12/12 sourced (100%)
✅ CHECK 5: Case descriptions - 3/3 verified (100%)

OVERALL SCORE: 91% (GOOD - REFINE REQUIRED)
DECISION: ⚠️ REFINE (fix Fallos 186:170 description before production)
```

### Decision Criteria

- **✅ CONTINUE to Production** if:
  - Reality Filter score ≥ 93%
  - All Fallos citations verified
  - No critical errors detected

- **⚠️ REFINE** if:
  - Reality Filter score 85-92%
  - Minor citation issues (fixable in < 4 hours)
  
- **🛑 STOP (Return to Draft)** if:
  - Reality Filter score < 85%
  - Multiple invented cases detected
  - Core argument no longer sound

### Who Decides
- Primary author + Reality Filter automated check + 1 SME reviewer

### Estimated Time at This Stage
- Writing: 20-30 hours (incremental from MVP)
- Reality Filter: 30 minutes (automated) + 2 hours (fix issues)
- Review: 3 hours
- Decision meeting: 1 hour

---

## Checkpoint 3: Production (16,000+ words, SSRN-ready)

### Goal
Finalize all formatting, ensure SSRN compliance, and prepare for submission.

### Scope Requirements
- [ ] All sections (I-VII) finalized
- [ ] Appendix A (Methodology) complete
- [ ] Full bibliography in **Chicago author-date format**
- [ ] All tables/figures captioned and referenced
- [ ] Final abstract (150 words)
- [ ] Limitations section (Section VII.6)
- [ ] Cover page with author affiliations

### Measurements

| **Metric** | **Threshold** | **How to Measure** |
|------------|---------------|---------------------|
| Chicago format compliance | 100% | **Chicago Validator** (automated script) |
| Abstract aligns with findings | Pass/Fail | Manual check: Abstract mentions all key results (G-fitness, p-values) |
| Cross-reference integrity | 100% | Automated check: All "(see Section X)" references exist |
| Word count in range | 15,000-20,000 | `wc -w paper.txt` |
| All figures cited in text | 100% | Pattern match: Every "Figure X" in captions appears in body text |

### Evaluation Protocol

**Run Chicago Format Validator**:

```bash
cd papers/tools
python3 chicago_format_validator.py --input ../2026_WIP_Paper/PRODUCTION_v3.docx
```

Expected output:
```
✅ CHECK 1: In-text citations - 42/42 follow (Author YYYY) format
✅ CHECK 2: Bibliography entries - 38/38 Chicago-compliant
⚠️ CHECK 3: Capitalization - 2 issues detected:
   - "evolutionary game theory" should be "Evolutionary Game Theory" (in title)
✅ CHECK 4: Cross-references - 15/15 valid
✅ CHECK 5: Abstract word count - 150 words (EXACT)

OVERALL SCORE: 98% (EXCELLENT - MINOR REFINE)
DECISION: ✅ CONTINUE (fix 2 capitalization issues)
```

### Decision Criteria

- **✅ SUBMIT** if:
  - Chicago validator score ≥ 97%
  - Abstract aligns with findings (manual check PASS)
  - No cross-reference errors

- **⚠️ REFINE** if:
  - Chicago validator score 90-96%
  - Abstract needs minor rewording
  
- **🛑 RETURN TO PILOT** if:
  - Chicago validator score < 90%
  - Abstract fundamentally misaligns with paper content

### Who Decides
- Primary author (final decision)

### Estimated Time at This Stage
- Formatting: 5-8 hours
- Chicago validator: 15 minutes (automated) + 1 hour (fix issues)
- Final review: 2 hours
- Submission prep: 1 hour

---

## Usage Instructions

### For New Papers

1. **At Start of Project**:
   - Copy this template to paper directory: `cp blueprints/GATED_CHECKPOINTS.md papers/2026_NewPaper/CHECKPOINTS.md`
   - Schedule checkpoint meetings in calendar (estimate dates based on timeline above)

2. **Before Each Checkpoint**:
   - Complete all "Scope Requirements"
   - Run relevant automated tools (Reality Filter, Chicago Validator)
   - Schedule 1-hour meeting with SME reviewer (if required)

3. **At Each Checkpoint Meeting**:
   - Review all measurements
   - Make explicit decision: Continue / Refine / Stop
   - Document decision in paper directory: `echo "Checkpoint 2 (Pilot): ✅ CONTINUE - Reality Filter 94%" >> DECISIONS_LOG.md`

4. **After Stop Decision**:
   - Document reason: `echo "Checkpoint 1 (MVP): 🛑 STOP - Core G-function logic flawed (circular reasoning detected)" >> DECISIONS_LOG.md`
   - Archive paper: `mv papers/2026_FailedPaper papers/archive/`

---

## Version History

| **Version** | **Date** | **Changes** |
|-------------|----------|-------------|
| 1.0 | 2025-11-20 | Initial template based on OpenAI Phase 04 principles |

---

## References

- OpenAI (2025). "From experiments to deployments: A practical path to scaling AI", pp. 19-22 (Phase 04: Build and Scale Products)
- Applied to SSRN paper production based on Nov 2025 experience ("General Welfare and Common Good as ESS")
