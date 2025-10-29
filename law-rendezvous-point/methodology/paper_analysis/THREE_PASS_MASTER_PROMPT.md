# Three-Pass Paper Analyzer: Master Prompt System
## Based on Keshav (2007) "How to Read a Paper" + Extended Phenotype Theory Framework

**Version**: 2.0  
**Date**: October 2025  
**Optimized for**: Legal, AI, Compliance, Evolutionary Theory papers  
**Integration**: IusMorfos Research Ecosystem

---

## 🎯 SYSTEM OVERVIEW

This master prompt system implements Keshav's three-pass method with **domain-specific adaptations** for:

1. **Legal/Regulatory papers** (constitutional law, compliance, legislation analysis)
2. **AI/Technical papers** (machine learning, formal methods, systems)
3. **Evolutionary/Game Theory papers** (cooperation, institutional evolution, EGT)
4. **Cross-disciplinary papers** (law + AI, evolution + law, etc.)

**Estimated Time**:
- **Pass 1**: 5-10 minutes (bird's eye view)
- **Pass 2**: 1 hour (grasp paper)
- **Pass 3**: 4-5 hours (virtual re-implementation)

---

## 📋 MASTER PROMPT

### Universal Header (All Paper Types)

```
You are an expert research analyst specializing in [DOMAIN: legal/AI/evolutionary theory/cross-disciplinary].

Apply the Keshav Three-Pass Method to analyze the following paper rigorously and critically.

**Paper Title**: [TITLE]
**Authors**: [AUTHORS]
**Publication**: [JOURNAL/CONFERENCE, YEAR]
**Citation**: [FULL CITATION]
**Domain**: [Legal / AI / Evolutionary / Regulatory / Cross-disciplinary]
**Sub-domain**: [e.g., Constitutional Law, Machine Learning, Game Theory, Compliance]

Execute all three passes sequentially, providing detailed outputs for each.
```

---

## 🔍 PASS 1: BIRD'S EYE VIEW (5-10 minutes)

### Objective
Get a **general idea** of the paper. Decide if it's worth a full read.

### Instructions

```
PASS 1: INITIAL SCAN

Read carefully:
1. Title
2. Abstract
3. Introduction (first and last paragraphs)
4. Section and sub-section headings
5. Conclusions
6. Glance at references (mark familiar ones)

Ignore:
- Detailed proofs, algorithms, or case law citations
- Technical details
- Figures/tables (just glance)

Answer the Five C's:

1. **Category**: What type of paper is this?
   - [ ] Theoretical/Conceptual
   - [ ] Empirical/Experimental
   - [ ] Literature Review/Survey
   - [ ] Doctrinal/Legal Analysis
   - [ ] Case Study
   - [ ] Technical/Implementation
   - [ ] Methodological
   - [ ] Other: _______

2. **Context**: Which other papers/theories does it relate to?
   - List 3-5 key references or theoretical frameworks cited
   - Identify the "conversation" this paper joins

3. **Correctness**: Do the assumptions appear valid?
   - [ ] Assumptions stated clearly
   - [ ] Assumptions reasonable
   - [ ] Potential hidden assumptions: _______
   - [ ] Red flags: _______

4. **Contributions**: What are the main contributions?
   - List 3-5 key claims or findings
   - Rate novelty: [ ] Incremental / [ ] Significant / [ ] Revolutionary

5. **Clarity**: Is the paper well written?
   - [ ] Clear structure
   - [ ] Good writing quality
   - [ ] Figures/tables helpful
   - [ ] Issues: _______

DECISION POINT:
Based on Pass 1, should you:
- [ ] Read in depth (Pass 2 + 3)
- [ ] Cite without deep reading (relevant but not central)
- [ ] Discard (not relevant or low quality)
- [ ] Monitor (potentially relevant, revisit later)

PASS 1 OUTPUT (≤ 200 words):
[Provide concise summary addressing the Five C's]
```

---

## 📖 PASS 2: GRASP THE PAPER (1 hour)

### Objective
Understand the paper's **content** (but not details). Be able to summarize to someone else.

### Instructions

```
PASS 2: CAREFUL READING (Ignore proofs/details)

Read the paper carefully BUT:
- Skip proofs, detailed algorithms, or lengthy case citations
- Take notes in margins (or digital annotations)
- Mark unclear passages
- Look up unfamiliar terms/references

Focus on:
1. **Figures, diagrams, tables**:
   - What do they show?
   - Do they support the claims?
   - Are there inconsistencies?

2. **Mark unread references** for further follow-up:
   - Which references are foundational?
   - Which are recent/cutting-edge?
   - Which are cited but not central?

Answer:

### A. ARGUMENT STRUCTURE

1. **Main Thesis**: What is the paper's central claim?
   [State in 1-2 sentences]

2. **Supporting Arguments**:
   - Argument 1: _______ [Evidence: _______]
   - Argument 2: _______ [Evidence: _______]
   - Argument 3: _______ [Evidence: _______]

3. **Conclusion**: What does the paper conclude?
   [State in 1-2 sentences]

### B. CRITICAL EVALUATION

**Strengths**:
1. _______
2. _______
3. _______

**Weaknesses**:
1. _______
2. _______
3. _______

**Gaps/Omissions**:
1. Missing data: _______
2. Unexplored alternatives: _______
3. Scope limitations: _______

### C. EVIDENCE QUALITY

Rate the evidence quality:
- [ ] Strong (rigorous methods, comprehensive data)
- [ ] Moderate (some limitations but defensible)
- [ ] Weak (significant methodological issues)
- [ ] Insufficient (more data needed)

Issues:
- Sample size: _______
- Generalizability: _______
- Reproducibility: _______

### D. KEY REFERENCES FOR FOLLOW-UP

List 5-10 references you should read:
1. [Reference 1] - Why: _______
2. [Reference 2] - Why: _______
...

DECISION POINT:
After Pass 2, should you:
- [ ] Proceed to Pass 3 (deep understanding needed)
- [ ] Stop here (sufficient understanding for your purposes)
- [ ] Re-read specific sections only

PASS 2 OUTPUT (≤ 500 words):
[Provide structured summary addressing sections A-D]
```

---

## 🔬 PASS 3: VIRTUAL RE-IMPLEMENTATION (4-5 hours)

### Objective
**Virtually re-implement** the paper. Understand it at the deepest level. Be able to **reconstruct it from memory**.

### Instructions

```
PASS 3: DEEP DIVE (Read every word, understand every proof/argument)

Goal: Understand the paper so deeply you could:
- Re-explain it from scratch
- Identify implicit assumptions
- Spot errors or gaps
- Extend or improve the work

Process:
1. **Challenge every assumption**:
   - Is assumption X necessary?
   - What if we relaxed assumption Y?
   - Are there hidden assumptions?

2. **Re-derive/reconstruct**:
   - For technical papers: Re-derive key equations/algorithms
   - For legal papers: Re-construct arguments from first principles
   - For empirical papers: Trace data → analysis → conclusions

3. **Compare with related work**:
   - How does this differ from Paper A, B, C?
   - What innovations are truly novel?
   - What is incremental vs revolutionary?

4. **Identify errors or weaknesses**:
   - Logical fallacies
   - Methodological issues
   - Overgeneralization
   - Cherry-picked evidence

Answer:

### A. RE-IMPLEMENTATION NOTES

**If Technical Paper**:
- Can you re-derive the main algorithm/proof?
  - [ ] Yes, fully
  - [ ] Mostly, with some gaps
  - [ ] No, too complex
- Bottlenecks or clever innovations: _______

**If Legal Paper**:
- Can you reconstruct the legal argument?
  - [ ] Yes, fully
  - [ ] Mostly, with some gaps
  - [ ] No, too complex
- Key precedents or statutory interpretation: _______

**If Empirical Paper**:
- Can you trace data → analysis → conclusions?
  - [ ] Yes, transparent
  - [ ] Mostly, some steps unclear
  - [ ] No, methods opaque
- Statistical rigor: _______

### B. CRITICAL ANALYSIS

**Implicit Assumptions Found**:
1. _______
2. _______
3. _______

**Errors or Weaknesses Identified**:
1. Type: [Logical / Methodological / Evidentiary]
   Description: _______
   Severity: [ ] Minor / [ ] Moderate / [ ] Major

2. Type: [Logical / Methodological / Evidentiary]
   Description: _______
   Severity: [ ] Minor / [ ] Moderate / [ ] Major

**Alternative Explanations Considered**:
- Did the paper consider alternative hypothesis H'?
  - [ ] Yes, and refuted it
  - [ ] No, oversight
- Could the data support alternative interpretation I'?
  - [ ] No, data is conclusive
  - [ ] Yes, possible (describe: _______)

### C. INNOVATION ASSESSMENT

**Truly Novel Contributions**:
1. _______
2. _______

**Incremental Contributions**:
1. _______
2. _______

**Claims Not Fully Supported**:
1. Claim: _______ | Gap: _______
2. Claim: _______ | Gap: _______

### D. FUTURE WORK & EXTENSIONS

**How to Improve This Work**:
1. Better data: _______
2. Alternative method: _______
3. Broader scope: _______

**How to Extend This Work**:
1. Apply to new domain: _______
2. Combine with theory X: _______
3. Test with dataset Y: _______

**How to Refute This Work**:
1. Counter-example: _______
2. Alternative hypothesis: _______
3. Data that would falsify claim: _______

### E. INTEGRATION WITH YOUR RESEARCH

**Relevance to Your Work** (e.g., Extended Phenotype Theory, Constitutional Lock-in, EGT):
- Direct application: _______
- Methodological insight: _______
- Theoretical connection: _______

**Citation Strategy**:
- [ ] Cite as foundational
- [ ] Cite as supporting evidence
- [ ] Cite as alternative approach
- [ ] Critique or contrast

PASS 3 OUTPUT (≤ 1,000 words):
[Provide detailed analysis addressing sections A-E]
```

---

## 📊 FINAL OUTPUT: STRUCTURED SYNTHESIS

After completing all three passes, generate:

### Executive Summary (≤ 300 words)

```
**Paper**: [Title]
**Authors**: [Authors]
**Publication**: [Venue, Year]

**Summary**:
[2-3 paragraph synthesis of main contributions, strengths, weaknesses]

**Key Findings**:
1. _______
2. _______
3. _______

**Relevance**: [To your research agenda]

**Recommendation**: [ ] Must-read / [ ] Important / [ ] Relevant / [ ] Optional / [ ] Skip
```

### SWOT Analysis Table

| **Strengths** | **Weaknesses** |
|---------------|----------------|
| 1. _______ | 1. _______ |
| 2. _______ | 2. _______ |
| 3. _______ | 3. _______ |

| **Opportunities** | **Risks/Threats** |
|-------------------|-------------------|
| 1. _______ | 1. _______ |
| 2. _______ | 2. _______ |
| 3. _______ | 3. _______ |

### Action Items

- [ ] Read foundational references: [List]
- [ ] Replicate/validate findings: [Method]
- [ ] Integrate into Paper #X: [Section]
- [ ] Cite in context of: [Your argument]
- [ ] Follow-up with authors: [Question]

---

## 🎓 DOMAIN-SPECIFIC ADAPTATIONS

### For LEGAL/REGULATORY Papers

Add these questions:

**Legal Analysis**:
1. **Doctrinal Soundness**: Is the legal reasoning consistent with precedent?
2. **Statutory Interpretation**: Are statutes interpreted correctly?
3. **Normative Claims**: Are "ought" claims justified or just asserted?
4. **Comparative Law**: Does it consider other jurisdictions?
5. **Practical Applicability**: Can this be operationalized by courts/regulators?

**Extended Phenotype Theory Integration**:
- Does the paper treat law as:
  - [ ] Rules (formalist)
  - [ ] Institutions (extended phenotypes of memes)
  - [ ] Evolutionary systems
- Can EPT framework improve the analysis?

### For AI/TECHNICAL Papers

Add these questions:

**Technical Validation**:
1. **Reproducibility**: Is code/data available?
2. **Scalability**: Does it work on real-world datasets?
3. **Robustness**: How does it handle edge cases?
4. **Computational Complexity**: O(?) time/space
5. **Limitations**: When does it fail?

**AI Ethics/Law Integration**:
- Does the paper address:
  - [ ] Bias/fairness
  - [ ] Transparency/explainability
  - [ ] Legal compliance (GDPR, AI Act, etc.)
  - [ ] Dual-use concerns

### For EVOLUTIONARY/GAME THEORY Papers

Add these questions:

**Evolutionary Analysis**:
1. **Model Assumptions**: Are they biologically/socially realistic?
2. **ESS Stability**: Are equilibria robust?
3. **Falsifiability**: Can predictions be tested empirically?
4. **Scope**: Does it apply to cultural evolution (memes)?
5. **Mechanism**: What selection pressure drives the result?

**Application to Law**:
- Can this model explain:
  - [ ] Legal norm emergence
  - [ ] Institutional persistence
  - [ ] Reform dynamics
  - [ ] Constitutional evolution

---

## 🔧 USAGE INSTRUCTIONS

### For a New Paper

1. **Copy this master prompt**
2. **Fill in Universal Header** with paper details
3. **Execute Pass 1** → Make decision (read/cite/discard)
4. **Execute Pass 2** (if Pass 1 = "read") → Structured notes
5. **Execute Pass 3** (if Pass 2 = "deep dive needed") → Full mastery
6. **Generate Final Output** → Store in literature database

### For Batch Processing

If analyzing multiple papers (e.g., literature review):
- Run **Pass 1 only** on all papers (5-10 min each)
- Sort by relevance
- Run **Pass 2** on top 20%
- Run **Pass 3** on top 5% (most critical papers)

### Integration with Research Workflow

**Store outputs in**:
```
literature/
  [domain]/
    [paper_id]/
      - paper.pdf
      - pass1_summary.md
      - pass2_notes.md
      - pass3_analysis.md
      - swot_table.md
      - citations.bib
```

---

## 📚 EXAMPLES

### Example 1: Tomasello (2012) "Two Key Steps in Evolution of Human Cooperation"

**Pass 1 Output** (5 mins):
- **Category**: Theoretical/Empirical (primatology + child development)
- **Context**: Builds on Trivers (reciprocal altruism), challenges standard cooperation models
- **Correctness**: Assumptions about collaborative foraging plausible
- **Contributions**: (1) Shared intentionality as key human trait, (2) Two-step evolutionary model
- **Clarity**: Excellent writing, clear structure
- **Decision**: READ IN DEPTH (relevant to Rubicon question)

**Pass 2 Output** (1 hour):
- **Thesis**: Human cooperation uniquely stems from shared intentionality (not just reciprocity)
- **Evidence**: Children 3yo share more equitably than adult chimps (experimental)
- **Strengths**: Cross-species comparison, developmental data
- **Weaknesses**: Limited archaeological evidence for timeline
- **References to follow**: Vince & Brown (2005) EGT, Axelrod cooperation
- **Decision**: PROCEED TO PASS 3 (critical for Paper #33)

**Pass 3 Output** (4 hours):
- **Re-implementation**: Can reconstruct two-step model (mutualism → altruism)
- **Implicit assumptions**: Language co-evolved with shared intentionality (not proven)
- **Errors**: None major, but timeline speculative (~2M years vs 200k years)
- **Extension**: Apply to legal norms emergence (shared intentionality → proto-contracts)
- **Integration**: Fits EPT framework (shared intentionality = Rubicon for law)

---

## 🤖 AI-ASSISTED USAGE

This prompt can be used with:
- **Claude/GPT-4**: Paste full paper text + this prompt
- **Document Analysis Tools**: Upload PDF + trigger automated Pass 1
- **Research Assistant Workflows**: Batch process literature database

**Tip**: For long papers (>20 pages), split into sections and run Pass 2/3 per section.

---

## 📖 REFERENCES

1. **Keshav, S. (2007)**. "How to Read a Paper". *ACM SIGCOMM Computer Communication Review*, 37(3).
2. **Dawkins, R. (1982)**. *The Extended Phenotype*. Oxford University Press.
3. **Dawkins, R. (1996)**. *Climbing Mount Improbable*. W.W. Norton & Company.
4. **Lerer, A. (2024-2025)**. IusMorfos Extended Phenotype Theory papers (32 papers, SSRN).

---

**Last Updated**: October 27, 2025  
**Version**: 2.0  
**Maintainer**: Adrian Lerer / GenSpark AI Research Assistant  
**License**: CC BY 4.0 (Creative Commons Attribution)
