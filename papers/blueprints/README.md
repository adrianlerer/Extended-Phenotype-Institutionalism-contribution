# Blueprint Library

**Purpose**: Reusable templates and protocols for academic paper production.  
**Based on**: OpenAI "From experiments to deployments" playbook (Phase 04: Build and Scale Products)

---

## Available Blueprints

### Core Protocols

1. **`GATED_CHECKPOINTS.md`** - 3-stage validation system
   - Checkpoint 1: Draft MVP (7,000-10,000 words)
   - Checkpoint 2: Pilot (12,000-15,000 words + Appendix)
   - Checkpoint 3: Production (16,000+ words, SSRN-ready)
   - **Use when**: Starting any new academic paper

2. **`REALITY_FILTER_PROTOCOL.md`** - 6-layer verification system
   - Layer 1: Citation existence check (SAIJ/vLex)
   - Layer 2: Empirical claims verification
   - Layer 3: Quantitative claims must have sources
   - Layer 4: Temporal consistency check
   - Layer 5: Contradictory statements detection
   - Layer 6: Abstract-body alignment
   - **Use when**: At Checkpoint 2 (Pilot) before finalizing paper

### Templates (papers/blueprints/templates/)

3. **`BIBLIOGRAPHY_TEMPLATE.md`** - Chicago author-date format
   - Academic references structure
   - Fallos citation standard
   - Verification checklist
   - **Use when**: Creating bibliography section

4. **`METHODOLOGY_APPENDIX_TEMPLATE.md`** - EGT framework
   - G-function explanation structure
   - Environmental variables table
   - Software/replication section boilerplate
   - Limitations section framework
   - **Use when**: Writing Appendix A (Methodology)

### Evaluation Scripts (papers/blueprints/evaluation/)

5. **`reality_filter_v2.py`** - Automated verification tool (COMING SOON)
   - Runs all 6 layers automatically
   - Generates score report
   - Flags errors for manual review

6. **`chicago_format_validator.py`** - Citation format checker (COMING SOON)
   - Validates (Author YYYY) in-text citations
   - Checks bibliography entries
   - Verifies cross-references

---

## Usage Workflow

### Starting a New Paper

```bash
# 1. Create paper directory
mkdir -p papers/2026_NewPaper

# 2. Copy checkpoint template
cp papers/blueprints/GATED_CHECKPOINTS.md papers/2026_NewPaper/CHECKPOINTS.md

# 3. Copy reusable templates
cp papers/blueprints/templates/BIBLIOGRAPHY_TEMPLATE.md papers/2026_NewPaper/
cp papers/blueprints/templates/METHODOLOGY_APPENDIX_TEMPLATE.md papers/2026_NewPaper/

# 4. Create decision log
touch papers/2026_NewPaper/DECISIONS_LOG.md
```

### At Each Checkpoint

**Checkpoint 1 (MVP)**:
1. Complete 7,000-10,000 words (Sections I-IV)
2. Review `CHECKPOINTS.md` → Checkpoint 1 criteria
3. Make decision: Continue / Refine / Stop
4. Document in `DECISIONS_LOG.md`

**Checkpoint 2 (Pilot)**:
1. Complete all sections + Appendix
2. **Run Reality Filter Protocol**:
   ```bash
   # Manual process (until automated script ready)
   # Follow REALITY_FILTER_PROTOCOL.md step-by-step
   ```
3. Score must be ≥93% to proceed
4. Fix issues if score 85-92%
5. Document in `DECISIONS_LOG.md`

**Checkpoint 3 (Production)**:
1. Finalize formatting
2. Run Chicago Format Validator (when available)
3. Final abstract check (150 words)
4. Submit to SSRN / journal

---

## Reuse Metrics

| **Paper** | **Blueprints Reused** | **Time Saved** | **Reality Filter Score** |
|-----------|-----------------------|----------------|--------------------------|
| SSRN Nov 2025 (baseline) | 0 | 0 hours | 93% → 99% (after fix) |
| Emergencia y Federalismo (projected) | 3 | 25 hours (40% reduction) | TBD |

---

## Creating New Blueprints

When you identify a reusable pattern (e.g., "Linguistic Analysis Method"), create a new blueprint:

```bash
# 1. Create blueprint file
touch papers/blueprints/templates/LINGUISTIC_ANALYSIS_TEMPLATE.md

# 2. Document structure:
# - Purpose
# - When to use
# - Step-by-step protocol
# - Example from previous paper
# - Checklist

# 3. Update this README with new blueprint
```

---

## Blueprint Quality Standards

All blueprints must include:
- [ ] **Purpose**: What problem does this solve?
- [ ] **When to use**: At which checkpoint or stage?
- [ ] **Protocol**: Step-by-step instructions
- [ ] **Example**: Real usage from past paper
- [ ] **Checklist**: Verification steps
- [ ] **Version history**: Track updates

---

## Continuous Improvement

After each paper completion:
1. Review what worked / what didn't
2. Update blueprints based on lessons learned
3. Add new blueprints for novel patterns
4. Document time savings in Reuse Metrics table

---

## References

- OpenAI (2025). "From experiments to deployments", pp. 19-22
- SSRN Paper (Nov 2025): "General Welfare and Common Good as ESS" - First paper to use blueprint approach
