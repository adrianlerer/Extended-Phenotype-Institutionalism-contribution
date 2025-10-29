# MiniMax-M2 Validation Protocol
## Empirical Assessment of Automated Paper Analysis Accuracy

**Purpose:** Systematic validation of MiniMax-M2 for academic paper analysis before full integration.  
**Threshold:** ≥85% overall accuracy required to proceed with production deployment.  
**Timeline:** Validation Study #1 (Tomasello 2012) → Full Benchmark (N=10 papers) → Production

---

## Overview

This validation protocol implements **rigorous empirical assessment** of MiniMax-M2's capacity to automate Three-Pass Method PASS 1 analysis. We compare automated output against expert manual analysis across five dimensions (Five C's) using precision/recall metrics.

### Why This Matters

**Scientific Rigor:** Automated systems must demonstrate ≥85% accuracy before replacing human expert analysis in research workflows. This threshold balances:
- **Efficiency gains** (10x throughput increase)
- **Quality assurance** (maintains research integrity)
- **Error tolerance** (<15% acceptable for PASS 1, as PASS 2-3 involve human review)

**Precedent:** Similar validation protocols used in:
- Medical AI diagnostic systems (FDA requires ≥85% sensitivity)
- Legal research automation (LexisNexis, Westlaw algorithms)
- Academic literature screening (Cochrane systematic reviews)

---

## Methodology

### 1. Ground Truth Establishment

**Manual Expert Analysis:**
- Performed by domain expert (evolutionary biology + legal theory)
- Time investment: 10 minutes for PASS 1 (Tomasello 2012)
- Documented in: `paper_analysis/EXAMPLE_Tomasello_2012.md`

**Criteria:**
- **Five C's:** Category, Context, Correctness, Contributions, Clarity
- **Decision:** READ/CITE/DISCARD/MONITOR
- **Rationale:** Explicit reasoning for each judgment

### 2. Automated Analysis

**MiniMax-M2 Configuration:**
- **Temperature:** 0.3 (analytical consistency)
- **Max tokens:** 2048
- **Input:** Abstract + Introduction (~8,000 chars)
- **Output:** Structured JSON (Five C's + decision)

**Quality Controls:**
- JSON schema validation
- Thinking process extraction (`<think>` tags)
- Error handling (API failures, malformed responses)

### 3. Metrics Calculation

#### **Exact Match Metrics**
- **Category:** Boolean match (exact or semantic equivalence)
- **Clarity:** Boolean match (Excellent/Good/Acceptable/Poor)
- **Decision:** Boolean match (READ/CITE/DISCARD/MONITOR)

#### **Set-Based Metrics** (Precision/Recall/F1)
- **Context:** References cited in automated vs. ground truth
  - **Precision:** TP / (TP + FP) — how many cited refs are relevant?
  - **Recall:** TP / (TP + FN) — how many relevant refs were cited?
  - **F1:** Harmonic mean of precision and recall
  
- **Contributions:** Key claims identified
  - Uses semantic overlap (bag-of-words with length filter >4 chars)

#### **Ordinal Agreement**
- **Correctness:** Maps assessments to ordinal scale
  - Valid = 1.0
  - Valid with caveats = 0.75
  - Uncertain = 0.5
  - Flawed = 0.0
  - Agreement = 1.0 - |automated - ground_truth|

#### **Overall Accuracy**
Weighted average of all dimensions:
```
Overall = 0.15×Category + 0.20×Context + 0.20×Correctness + 
          0.25×Contributions + 0.10×Clarity + 0.10×Decision
```

Weights reflect **relative importance** for research workflow:
- **Contributions (25%):** Most critical for deciding if paper is relevant
- **Context + Correctness (20% each):** Essential for understanding paper's place in literature
- **Category (15%):** Important for classification but less critical
- **Clarity + Decision (10% each):** Support metrics

### 4. Pass/Fail Criteria

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Overall Accuracy** | ≥85% | Industry standard for AI decision support systems |
| **Contributions F1** | ≥70% | Must capture majority of key claims |
| **Context Recall** | ≥60% | More important to avoid missing refs than having extra |
| **Correctness Agreement** | ≥75% | Must align on validity assessment |
| **Decision Match** | Boolean | Critical — wrong decision wastes researcher time |

**Decision Logic:**
- **Overall ≥85% AND Decision Match = TRUE** → ✅ PASS → Proceed to full benchmark
- **Overall ≥85% BUT Decision Match = FALSE** → ⚠️  CONDITIONAL → Manual review required
- **Overall <85%** → ❌ FAIL → Iterate on prompt engineering

---

## Execution Instructions

### Prerequisites

```bash
# 1. Install dependencies
pip install openai

# 2. Set MiniMax API key (get from https://platform.minimax.io/)
export MINIMAX_API_KEY="your-api-key-here"

# 3. Optional: Set base URL (defaults to https://api.minimax.chat/v1)
export MINIMAX_BASE_URL="https://api.minimax.chat/v1"
```

### Run Validation Study #1 (Tomasello 2012)

```bash
cd /home/user/webapp/law-rendezvous-point/methodology

# Execute validation script
python minimax_validation_tomasello2012.py

# Expected output:
# - Terminal summary with overall accuracy
# - Full validation report (Markdown) saved to:
#   VALIDATION_REPORT_Tomasello2012_YYYYMMDD_HHMMSS.md
```

### Interpret Results

**If PASS (≥85%):**
1. Review validation report for qualitative insights
2. Proceed to Full Benchmark (10 papers, see below)
3. Calculate inter-rater reliability (Cohen's kappa) across benchmark
4. Deploy to production if kappa ≥0.80

**If FAIL (<85%):**
1. Analyze error patterns (see Weaknesses section in report)
2. Update prompt (more explicit instructions, examples)
3. Re-run with temperature=0.1 (more deterministic)
4. If still fails after 2 iterations → escalate to hybrid approach:
   - MiniMax-M2 generates draft
   - Human expert reviews/corrects
   - Use corrections to fine-tune prompts

---

## Full Benchmark Protocol (N=10)

After passing Validation Study #1, proceed with full benchmark:

### Paper Selection Criteria

**Diversity Requirements:**
- **3 papers:** Evolutionary anthropology (e.g., Dawkins, Trivers, Hrdy)
- **3 papers:** Legal theory (e.g., Hart, Dworkin, Posner)
- **2 papers:** AI/ML (e.g., LLM safety, algorithmic accountability)
- **2 papers:** Interdisciplinary (e.g., law & evolution, AI & ethics)

**Quality Criteria:**
- Published in peer-reviewed journals (Q1/Q2 ranking)
- Cited ≥50 times (established influence)
- Full text available (not just abstract)
- Accessible language (avoid overly technical jargon)

### Execution

```bash
# Run benchmark script (to be implemented)
python minimax_benchmark_fullset.py \
  --papers_dir="../literature/" \
  --output_dir="./validation_results/" \
  --n_papers=10 \
  --temperature=0.3
```

### Statistical Analysis

**Inter-Rater Reliability:**
- **Cohen's Kappa:** Agreement between automated and manual analysis
  - κ ≥0.80 = Excellent agreement
  - κ 0.60-0.79 = Good agreement
  - κ <0.60 = Poor agreement (do not deploy)

**Confidence Intervals:**
- Calculate 95% CI for overall accuracy
- If lower bound of CI ≥80%, proceed with deployment

**Stratified Analysis:**
- Accuracy by paper type (theoretical vs. empirical)
- Accuracy by domain (anthropology vs. law vs. AI)
- Identify systematic biases (e.g., better on recent papers?)

---

## Production Deployment Checklist

After passing full benchmark (κ ≥0.80):

- [ ] **Documentation:** Update THREE_PASS_MASTER_PROMPT.md with automation instructions
- [ ] **Integration:** Add MiniMax-M2 analysis to literature search workflow
- [ ] **Monitoring:** Implement accuracy tracking (sample 10% for manual review)
- [ ] **Versioning:** Pin MiniMax-M2 model version to prevent drift
- [ ] **Fallback:** Define protocol for API failures (queue for manual analysis)
- [ ] **Audit Trail:** Log all automated analyses (input, output, timestamps)
- [ ] **Human Review:** Require expert sign-off for READ IN DEPTH decisions

---

## Expected Outcomes

### Validation Study #1 (Tomasello 2012)

**Hypothesis:** MiniMax-M2 will achieve ≥85% accuracy on Tomasello (2012) because:
1. Paper has clear structure (abstract + explicit methodology section)
2. Key concepts well-defined (shared intentionality, collective intentionality)
3. Context references explicit (cites Dawkins, Trivers, Hamilton clearly)
4. Contributions stated upfront (two-step model)

**Risk:** Model may struggle with:
- Timeline uncertainty (±1M years) — may not capture nuance
- Alternative hypotheses discussion — may miss caveats
- Cross-disciplinary integration — may not recognize legal theory connections

### Full Benchmark (N=10)

**Expected Range:** 80-90% overall accuracy across diverse papers

**Confidence:** 95% CI should have lower bound ≥80%

**Inter-Rater Reliability:** κ = 0.75-0.85 (good to excellent agreement)

---

## Limitations and Future Work

### Current Limitations

1. **Sample Size:** N=1 (Tomasello) → N=10 (benchmark) is small
   - Future: Expand to N=50-100 for robust statistical inference
   
2. **Domain Coverage:** Focus on anthropology + law + AI
   - Future: Test on other domains (economics, sociology, political science)
   
3. **Language:** English-only papers
   - Future: Test multilingual capabilities (especially Spanish for Argentine law)
   
4. **Paper Age:** Focus on 2000-2024 papers
   - Future: Test on historical papers (pre-2000) to assess generalization

### Planned Improvements

**Phase 2 (Q2 2025):**
- Fine-tuning on domain-specific corpus (if API allows)
- Ensemble approach (MiniMax-M2 + Claude Opus + GPT-4) with voting
- Active learning (flag low-confidence analyses for human review)

**Phase 3 (Q3 2025):**
- Extend to PASS 2 automation (deeper analysis, not just Bird's Eye View)
- Citation graph extraction (automatic reference network mapping)
- Contradiction detection (identify conflicting claims across papers)

---

## References

### Validation Methodology
- Fleiss, J. L. (1971). "Measuring nominal scale agreement among many raters." *Psychological Bulletin*, 76(5), 378-382.
- Landis, J. R., & Koch, G. G. (1977). "The measurement of observer agreement for categorical data." *Biometrics*, 33(1), 159-174.

### Comparable Systems
- **Cochrane Systematic Reviews:** Human + ML hybrid for literature screening
- **FDA AI/ML Medical Devices:** Requires ≥85% sensitivity in clinical validation
- **LexisNexis CaseMap:** Legal research automation with human oversight

### Three-Pass Method
- Keshav, S. (2007). "How to Read a Paper." *ACM SIGCOMM Computer Communication Review*, 37(3), 83-84.

---

## Contact and Contribution

**Primary Investigator:** IusMorfos Research Team  
**Repository:** `law-rendezvous-point/methodology/`  
**Issues:** Report validation failures or propose improvements via GitHub Issues  
**License:** MIT (aligned with MiniMax-M2)

---

**Last Updated:** 2025-10-27  
**Version:** 1.0.0  
**Status:** ✅ Ready for Validation Study #1
