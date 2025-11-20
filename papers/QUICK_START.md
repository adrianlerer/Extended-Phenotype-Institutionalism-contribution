# Quick Start: OpenAI Playbook for Legal Research

**30-Second Version**: Copy templates → Follow checkpoints → Run Reality Filter at Pilot stage → Submit paper with 23% less time.

---

## 🚀 New Paper Setup (5 minutes)

```bash
# 1. Create paper directory
mkdir -p papers/2026_YourPaperName

# 2. Copy essential files
cp papers/blueprints/GATED_CHECKPOINTS.md papers/2026_YourPaperName/CHECKPOINTS.md
cp papers/blueprints/templates/BIBLIOGRAPHY_TEMPLATE.md papers/2026_YourPaperName/
cp papers/blueprints/templates/METHODOLOGY_APPENDIX_TEMPLATE.md papers/2026_YourPaperName/

# 3. Create decision log
echo "# Decisions Log - YourPaperName" > papers/2026_YourPaperName/DECISIONS_LOG.md
echo "" >> papers/2026_YourPaperName/DECISIONS_LOG.md
echo "## Checkpoint 1 (MVP)" >> papers/2026_YourPaperName/DECISIONS_LOG.md
echo "Date: TBD" >> papers/2026_YourPaperName/DECISIONS_LOG.md
echo "Decision: [ ] Continue  [ ] Refine  [ ] Stop" >> papers/2026_YourPaperName/DECISIONS_LOG.md

# 4. Start writing! (aim for 7-10k words first)
```

---

## 📝 The 3 Checkpoints (What to Do When)

### Checkpoint 1: MVP (at 7,000-10,000 words)

**What you have**:
- Sections I-IV drafted
- Basic bibliography (15-20 refs)
- Core argument clear

**What to check**:
- [ ] G-function logic consistent?
- [ ] Argument structure coherent?
- [ ] 5 random citations real? (Google Scholar quick check)

**Decision**:
- ✅ Continue → Keep writing to 12-15k words
- ⚠️ Refine → Fix issues (< 2 hours), then continue
- 🛑 Stop → Archive paper, move to next idea

**Document in DECISIONS_LOG.md**:
```
[2026-XX-XX] Checkpoint 1: ✅ CONTINUE
Core logic: PASS | Argument: PASS | Citations: 5/5 verified
```

---

### Checkpoint 2: PILOT (at 12,000-15,000 words) ⚠️ CRITICAL

**What you have**:
- All sections (I-VII) drafted
- Appendix A complete
- Full bibliography (30-40 refs)
- Tables/figures integrated

**What to check** (Reality Filter Protocol):

```bash
# Open these side-by-side:
# 1. Your paper (DOCX or PDF)
# 2. papers/blueprints/REALITY_FILTER_PROTOCOL.md

# Execute 6 layers manually:

Layer 1: Citation Existence
├─ Extract: grep -oP 'Fallos \d+:\d+' paper.txt
├─ Verify: Search each in SAIJ (https://www.saij.gob.ar/)
└─ Score: (Verified / Total) × 25 points

Layer 2: Empirical Claims
├─ List: All factual claims (citation counts, G-fitness values)
├─ Verify: Check sources or reproduce calculations
└─ Score: (Verified / Total) × 20 points

Layer 3: Quantitative Sources
├─ Extract: grep -oP '\d+\.\d+%|\d+%|p\s*<\s*0\.\d+' paper.txt
├─ Check: Each number has footnote or table reference
└─ Score: (Sourced / Total) × 15 points

Layer 4: Temporal Consistency
├─ Check: No "1991 doctrine influenced 1940 case" paradoxes
└─ Score: 15 points (minus 10 per error, min 0)

Layer 5: No Contradictions
├─ Search: grep -i "barra.*success" vs. "barra.*fail" paper.txt
├─ Check: Statements consistent across sections
└─ Score: 15 points (minus 15 per contradiction, min 0)

Layer 6: Abstract-Body Alignment
├─ Check: Abstract claims match body findings (4-5 key claims)
└─ Score: (Aligned / Total) × 10 points

TOTAL SCORE = Sum of all layers (0-100%)
```

**Scoring thresholds**:
- **95-100%**: ✅ EXCELLENT → Continue to Production
- **90-94%**: ✅ GOOD → Minor fixes, then continue
- **85-89%**: ⚠️ ACCEPTABLE → Moderate revision needed
- **<85%**: 🛑 POOR → Return to Draft

**Example** (from SSRN Nov 2025 paper):
```
Layer 1: Citation Existence - 21/25 (84%)
  ERROR: Fallos 186:170 description wrong (fiscal immunity, not temporal limits)
Layer 2: Empirical Claims - 18/20 (90%)
Layer 3: Quantitative Sources - 15/15 (100%)
Layer 4: Temporal Consistency - 15/15 (100%)
Layer 5: No Contradictions - 15/15 (100%)
Layer 6: Abstract Alignment - 9/10 (90%)

TOTAL: 93/100 (93%) → ✅ GOOD - REFINE LAYER 1
```

**Decision**:
- ✅ Continue (≥93%) → Finalize formatting
- ⚠️ Refine (85-92%) → Fix issues, re-run Reality Filter
- 🛑 Return to Draft (<85%) → Major revision needed

**Document in DECISIONS_LOG.md + VERIFICATION_LOG.md**

---

### Checkpoint 3: PRODUCTION (at 16,000+ words)

**What you have**:
- Finalized text
- Chicago format applied
- Final abstract (150 words)
- Cover page ready

**What to check**:
- [ ] Chicago format 100%? (Manual check or automated validator)
- [ ] Abstract mentions all key findings?
- [ ] Cross-references valid? (All "see Section X" links work)
- [ ] Word count 15-20k?
- [ ] All figures cited in text?

**Decision**:
- ✅ Submit (≥97% Chicago score)
- ⚠️ Refine (90-96%)
- 🛑 Return to Pilot (<90%)

**Document in DECISIONS_LOG.md**:
```
[2026-XX-XX] Checkpoint 3: ✅ SUBMIT
Chicago: 98% | Abstract: PASS | Cross-refs: 15/15 valid
Submitted to: [Journal name] on [Date]
```

---

## 🎯 Claim Classification (4-Tier System)

**Use this decision tree for ANY claim you write**:

```
Is it common knowledge?
├─ YES → Tier 1 (Self-Service) → No verification
└─ NO → Is it quantitative or case-specific?
    ├─ NO → Tier 1 (Self-Service)
    └─ YES → Is the case/data well-documented?
        ├─ YES → Tier 2 (Reality Filter + 1 SME)
        └─ NO → Have you verified it yourself?
            ├─ YES → Tier 3 (Manual SAIJ + 2 SMEs + Reality Filter)
            └─ NO → Tier 4 (PROHIBITED - Verify first!)
```

**Examples**:
- "Argentina had dictatorship 1976-1983" → **Tier 1** (common knowledge)
- "Barra 0 citations" → **Tier 2** (quantitative, SAIJ verifiable)
- "Case X interpreted Y elastically" → **Tier 3** (specific holding, needs manual check)
- "In Fallos 999:999, court held Z" → **Tier 4** (if case doesn't exist → academic misconduct)

**Tier 3 Protocol** (Banco de la Provincia was this tier):
1. Search SAIJ for case
2. Download full case text
3. Read relevant sections
4. Verify claim matches case holding
5. Document in VERIFICATION_LOG.md

---

## 📊 Time Savings (Baseline vs. With Playbook)

| **Phase** | **Baseline** | **With Playbook** | **Savings** |
|-----------|--------------|-------------------|-------------|
| Research + writing | 40h | 40h | 0h (no change) |
| Components (biblio, method) | 15h | 6h | **9h (60%)** |
| Error detection | 2h | 1h | **1h (50%)** |
| Correction | 3h | 0.5h | **2.5h (83%)** |
| Reality Filter | 2h | 0.5h | **1.5h (75%)** |
| **TOTAL** | **62h** | **48h** | **14h (23%)** |

**Breakeven**: After 1st paper (6h investment, 14h savings)

---

## 🔧 Templates Quick Reference

### Bibliography (Chicago Author-Date)

**Format**: Author Last, First. Year. *Title*. City: Publisher.

**Example**:
```
Gargarella, Roberto. 2013. Latin American Constitutionalism, 1810-2010: 
  The Engine Room of the Constitution. Oxford: Oxford University Press.
```

**Fallos format**: *Case Name*, Fallos Tomo:Página (Date). [Description]

**Example**:
```
Peralta, Luis Arcenio y otro c/ Estado Nacional, Fallos 313:1513 
  (December 27, 1990). [Expanded emergency powers to economic measures]
```

**Tool**: Use `papers/blueprints/templates/BIBLIOGRAPHY_TEMPLATE.md` (copy & customize)

---

### Methodology Appendix

**Required sections**:
- A.1: G-function definition
- A.2: Environmental variables table
- A.3: Doctrinal strategy classification
- A.4: Citation analysis protocol
- A.5: Software + replication instructions
- A.6: Limitations

**Tool**: Use `papers/blueprints/templates/METHODOLOGY_APPENDIX_TEMPLATE.md` (copy & adapt variables)

---

## 📝 Verification Log Format

**When**: After verifying any Tier 3 claim

**Where**: `papers/VERIFICATION_LOG.md`

**Format**:
```markdown
### [2026-XX-XX] Paper: "Your Paper Title"
**Claim**: "Exact claim text"
**Tier**: 3 (specific case holding)
**Verification method**: SAIJ manual check + case text reading
**Result**: ✅ VERIFIED / ❌ REJECTED / ⚠️ REFINED
**Verified by**: [Your name]
**Notes**: [What you found]
---
```

**Example** (Banco de la Provincia error):
```markdown
### [2025-11-19] Paper: "General Welfare and Common Good as ESS"
**Claim**: "Banco de la Provincia (1940) interpreted 'tiempo determinado' elastically"
**Tier**: 3
**Verification method**: SAIJ manual check
**Result**: ❌ REJECTED
**Verified by**: Research team
**Notes**: Case EXISTS (Fallos 186:170) but is about fiscal immunity, NOT temporal limits.
ACTION: Removed claim from paper.
---
```

---

## 🎓 Key Lessons (From SSRN Nov 2025 Paper)

1. **Always read full case text** → Headnotes can be misleading (Banco Provincia error)
2. **Run Reality Filter at Checkpoint 2** → Not at end (would have caught error early)
3. **Budget 30-60 min per Tier 3 claim** → Manual verification takes time
4. **Document everything in logs** → Audit trail for continuous improvement

---

## 📞 Need Help?

**Documentation**:
- Full details: `papers/README.md`
- Protocols: `papers/blueprints/GATED_CHECKPOINTS.md`, `REALITY_FILTER_PROTOCOL.md`
- Governance: `papers/foundations/GOVERNANCE_RESEARCH.md`
- Backlog: `papers/backlog/2025_Q4_ROADMAP.md`

**Validation**: Run `papers/validate_implementation.sh` to check system status

---

**Last updated**: 2025-11-20  
**Status**: ✅ OPERATIONAL (83% validation success)
