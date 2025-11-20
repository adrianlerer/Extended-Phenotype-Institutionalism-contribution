# Research Governance Framework: AI-Assisted Legal Scholarship

**Version**: 1.0  
**Last updated**: 2025-11-20  
**Based on**: OpenAI Phase 01 governance principles

---

## Purpose

This framework establishes **clear rules** for using AI (LLMs) in legal research to ensure:
1. **Academic integrity**: All claims are verifiable and properly sourced
2. **Efficiency**: Researchers know what can be done autonomously vs. what needs verification
3. **Risk mitigation**: Prevent errors like "Banco de la Provincia 1940" (invented case description)

**Core Principle**: *The more sensitive the claim, the more layers of verification required.*

---

## 4-Tier Data Classification System

### Tier 1: Low-Sensitivity Claims (✅ Self-Service OK)

**Definition**: General statements, well-established doctrines, published academic work.

**Examples**:
- "Bienestar general promotes utilitarian logic" (descriptive, no citation needed)
- "Dawkins (1982) developed Extended Phenotype Theory" (published book, easily verified)
- "Argentina experienced dictatorship 1976-1983" (historical fact)

**Governance**:
- ✅ AI can generate autonomously
- ✅ Peer review optional (recommended but not mandatory)
- ✅ Publication direct (no additional verification)

**Justification**: Low risk of error, minimal impact if wrong, easy to correct.

---

### Tier 2: Medium-Sensitivity Claims (⚠️ Verification Required)

**Definition**: Quantitative statements with clear sources, interpretations of well-known cases.

**Examples**:
- "Barra achieved 0 citations, ALITT 17 citations" (requires SAIJ search, but straightforward)
- "Peralta (1990) expanded emergency powers to economic measures" (well-documented case)
- "Switzerland invoked emergency 10 times in 110 years" (requires source, but public data)

**Governance**:
- ⚠️ AI can generate, but **Reality Filter v2.0 mandatory**
- ⚠️ 1 SME validation required (author counts as SME if expert in topic)
- ⚠️ Must document source: `[Source: SAIJ search "bienestar general" + "Barra", 2025-11-15]`

**Justification**: Moderate risk of error, but verifiable with public databases.

---

### Tier 3: High-Sensitivity Claims (🔴 Multi-Layer Verification)

**Definition**: Claims about specific cases never before cited, original statistical calculations, novel legal interpretations.

**Examples**:
- "Banco de la Provincia de Buenos Aires (1940) interpreted 'tiempo determinado' elastically" 
  - **Why Tier 3**: Specific case + specific claim about its holding → requires manual SAIJ verification
- "17.6× mutation odds, p<0.001" (original regression calculation)
  - **Why Tier 3**: Novel statistical finding → requires reproducible code + SME validation
- "Justice X's opinion in Case Y influenced Justice Z's dissent in Case W" (causal claim)
  - **Why Tier 3**: Requires close reading of both opinions to verify influence

**Governance**:
- 🔴 Reality Filter v2.0 **mandatory**
- 🔴 Manual SAIJ database check (visual verification of case text)
- 🔴 2 SME reviews:
  - 1 legal expert (verify case interpretation is accurate)
  - 1 methodological expert (if statistical claim)
- 🔴 Escalation to "Center of Excellence" (primary author) if reviewers disagree

**Verification Protocol**:

1. **AI generates claim** (e.g., "Case X said Y")
2. **Reality Filter v2.0** flags it as Tier 3 (specific case + specific holding)
3. **Researcher actions**:
   - Step 1: Search SAIJ for "Banco de la Provincia de Buenos Aires" + "1940"
   - Step 2: Download full case text (Fallos 186:170)
   - Step 3: Read relevant sections (search for "tiempo determinado" or related terms)
   - Step 4: Document finding in `VERIFICATION_LOG.md`:
     ```
     Claim: "Banco Provincia (1940) interpreted 'tiempo determinado' elastically"
     SAIJ search: Case exists (Fallos 186:170, March 15, 1940)
     Case text review: ❌ CASE ABOUT FISCAL IMMUNITY, NOT TEMPORAL LIMITS
     Decision: ❌ REJECT CLAIM - Remove from paper
     ```
4. **SME review**: Independent researcher verifies same finding
5. **Decision**: If both agree case description is wrong → remove claim

**Justification**: High risk of error, high impact if wrong (damages paper credibility).

---

### Tier 4: Prohibited (🚫 No AI Without Supervision)

**Definition**: Claims that, if wrong, fundamentally undermine paper integrity.

**Examples**:
- **Inventing case citations**: "In Doe v. Roe (1985), Fallos 200:100, the court held..."
  - **Why Prohibited**: If case doesn't exist → instant rejection from journal
- **Fabricating statistical results**: "Our regression shows β=2.45, p=0.003" (without running regression)
  - **Why Prohibited**: Scientific fraud
- **Misattributing quotes**: "Justice Scalia wrote, 'The Constitution is dead'" (without verifying quote)
  - **Why Prohibited**: Defamation + academic misconduct

**Governance**:
- 🚫 AI **CANNOT** generate these claims autonomously
- 🚫 If AI generates, immediate **REJECT + manual rewrite**
- 🚫 Triple verification:
  1. Manual database check
  2. Human reading of source
  3. External SME validation (not just author)

**Consequences of Violation**:
- Paper retraction if published
- Loss of credibility
- Potential academic misconduct investigation

**How to Prevent**:
- **Never** ask AI to "create a case that supports X argument"
- **Always** ask AI to "find existing cases that support X, then I will verify them"
- Use Reality Filter v2.0 **before** any claim becomes final text

---

## Decision Tree: Which Tier is My Claim?

```
START: I have a claim I want to include in my paper.

┌─────────────────────────────────────────────┐
│ Is it a general statement or well-known     │
│ fact? (e.g., "Argentina had dictatorship    │
│ 1976-1983")                                  │
└─────────────────────────────────────────────┘
    │
    ├─ YES → Tier 1 (Self-Service OK)
    │
    └─ NO → Continue
        │
        ┌─────────────────────────────────────────┐
        │ Does it involve a specific case or      │
        │ quantitative finding?                   │
        │ (e.g., "Barra 0 citations")             │
        └─────────────────────────────────────────┘
            │
            ├─ YES → Continue
            │   │
            │   ┌─────────────────────────────────────────┐
            │   │ Is the case/finding well-documented?    │
            │   │ (e.g., Peralta is famous case)          │
            │   └─────────────────────────────────────────┘
            │       │
            │       ├─ YES → Tier 2 (Verification Required)
            │       │
            │       └─ NO → Continue
            │           │
            │           ┌─────────────────────────────────────────┐
            │           │ Have I personally verified the case     │
            │           │ text or calculation?                    │
            │           └─────────────────────────────────────────┘
            │               │
            │               ├─ YES → Tier 3 (Multi-Layer Verification)
            │               │
            │               └─ NO → Tier 4 (Prohibited - Verify First)
            │
            └─ NO → Tier 1 (Self-Service OK)
```

---

## Intake & Escalation Workflow

### Intake Process (For New Claims)

**Step 1: Researcher generates claim with AI**
- Example: "Claude, find cases where CSJN interpreted 'bienestar general' expansively"

**Step 2: Classify claim using Decision Tree**
- Example: Tier 3 (specific cases + specific holdings)

**Step 3: Apply appropriate governance**
- Example: Run Reality Filter v2.0 → Manual SAIJ check → SME review

**Step 4: Document verification**
- Example: Add to `VERIFICATION_LOG.md`:
  ```
  [2025-11-20] Claim: "Case X interpreted Y"
  Tier: 3
  Verification: ✅ SAIJ verified | ✅ SME reviewed
  Approved by: [Author name]
  ```

**Step 5: Include in paper**
- Example: Add footnote: `[Verified via SAIJ database search, 2025-11-20]`

---

## Roles & Responsibilities

### Primary Author
- **Classify** all claims using Decision Tree
- **Apply** appropriate governance (Reality Filter, SME reviews)
- **Document** verification in logs
- **Escalate** conflicts to SME reviewers

### SME Reviewers (Subject Matter Experts)
- **Review** Tier 3 claims when requested
- **Verify** case interpretations and statistical calculations
- **Provide** expert opinion within 48 hours of request
- **Document** reasoning in review notes

### "Center of Excellence" (typically = Primary Author + 1 Senior Researcher)
- **Resolve** escalated conflicts between SME reviewers
- **Audit** Tier 4 violations (if any)
- **Update** governance framework based on new error types
- **Train** researchers on classification system

---

## Metrics & Continuous Improvement

### Monthly Governance Audit

Track these metrics:

| **Metric** | **Target** | **Action if Below Target** |
|------------|------------|----------------------------|
| % of Tier 3 claims verified before publication | 100% | Audit unverified claims, add to VIOLATIONS_LOG |
| % of papers passing Reality Filter v2.0 on first try | 80%+ | Review training materials, improve prompts |
| Average SME review turnaround time | <48 hours | Expand SME reviewer network |
| # of Tier 4 violations detected | 0 | If >0: Mandatory training + process review |

---

## Version History

| **Version** | **Date** | **Changes** |
|-------------|----------|-------------|
| 1.0 | 2025-11-20 | Initial framework based on OpenAI Phase 01 + Nov 2025 SSRN paper errors |

---

## References

- OpenAI (2025). "From experiments to deployments", pp. 8-10 (Phase 01: Set the Foundations)
- Lesson learned: "Banco de la Provincia de Buenos Aires (1940)" error (Tier 3 violation, fixed via manual SAIJ check)
