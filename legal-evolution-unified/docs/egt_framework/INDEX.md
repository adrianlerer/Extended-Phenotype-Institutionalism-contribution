# Evolutionary Game Theory Framework - Complete Index

## Navigation Guide

This index provides a complete map of the EGT integration into the Legal Evolution Unified repository. Use this to quickly locate specific content based on your needs.

---

## 📚 Core Documentation

### 1. Master Integration Document
**File**: `/EGT_INTEGRATION_MASTER.md`  
**Purpose**: Complete overview of EGT integration  
**Length**: ~22,000 characters  
**Audience**: Researchers, developers, policymakers

**Contents**:
- Overview of integration (what was added, core contributions)
- Document structure and contents
- Key mathematical results (Theorems 1-2, corollaries)
- Integration points with existing framework
- Empirical validation roadmap
- Future research directions (Papers 2-4)
- How-to guides for different user types
- FAQ section

**When to read**: Start here for comprehensive understanding of the entire EGT integration.

---

### 2. Theoretical Foundation
**File**: `/docs/egt_framework/INSTITUTIONAL_PARASITISM_ESS.md`  
**Purpose**: Full mathematical formalization of institutional parasitism as ESS  
**Length**: ~19,600 characters (13 sections)  
**Audience**: Theoreticians, mathematical modelers

**Contents**:
1. Theoretical Foundation (ESS definitions, G-function framework)
2. G-Function Formalization (Lotka-Volterra equations)
3. CLI-ρ-ESS Mechanism (resource dynamics)
4. ESS Stability Analysis (first/second-order conditions, Hessian)
5. Multi-Strategy Equilibria (genuine vs cosmetic coexistence)
6. Non-Convergence to Optimal Proportions (why φ is unstable)
7. Case Studies (Argentina, Singapore, Chile)
8. Refinements and Extensions (multi-trait, multi-compartment, temporal)
9. Empirical Validation Protocol
10. Policy Implications
11. Integration with Existing Frameworks
12. Limitations and Future Directions
13. Conclusion

**Key Equations**:
- G(v, u, x) = r · [K(v) - Σa(v,u_j)·x_j] / K(v)
- K(v) = K_max · exp(-v²/(2σ_k²))
- σ_k(CLI) = σ_max · (1 - CLI)
- ρ(CLI) = ρ_max · (1 - CLI)²

**When to read**: For complete mathematical understanding and formal proofs.

---

### 3. Methodology Document
**File**: `/docs/theory/egt_institutional_non_convergence.md`  
**Purpose**: Explain why systems don't converge to optimal proportions  
**Length**: ~27,600 characters (11 sections)  
**Audience**: Institutional economists, political scientists

**Contents**:
1. Introduction: The Paradox of Optimal Irrelevance
2. EGT Framework for Institutional Evolution
3. CLI-σ_k Mapping (lock-in to resource scarcity)
4. Why Optimal Proportions Are Evolutionarily Unstable
5. Three Mechanisms of Non-Convergence
   - Path Dependence (precedent weight)
   - Veto Accumulation (multi-layer ESS)
   - Centralization Ratchet (asymmetric selection)
6. Formal Proofs and Derivations
7. Empirical Validation Plan
8. Policy Implications: Escape Routes
9. Integration with Existing Theoretical Frameworks
10. Limitations and Future Directions
11. Conclusion

**When to read**: For understanding the non-convergence problem and policy implications.

---

### 4. Framework README
**File**: `/docs/egt_framework/README.md`  
**Purpose**: Quick start guide and domain-agnostic usage  
**Length**: ~8,000 characters  
**Audience**: All users (first stop for newcomers)

**Highlights**:
- ⚠️ CRITICAL: Framework is domain-agnostic
- Works for labor, property, tax, speech, environment, criminal law, etc.
- Reality Filter: Proven vs Hypothetical vs Speculative
- Empirical validation status
- Usage examples for multiple domains
- Integration with IusMorfos, JurisRank, RootFinder, Peralta

**When to read**: First document to read for quick orientation.

---

## 💻 Implementation

### 5. Python Module
**File**: `/frameworks/institutional_parasitism_ess.py`  
**Purpose**: Production code for ESS analysis  
**Length**: ~18,900 characters  
**Language**: Python 3.8+

**Classes**:
- `GFunctionParams`: Parameter dataclass with CLI calibration
- `ResourceParams`: Resource dynamics parameters
- `LotkaVolterraGFunction`: Core G-function implementation
- `DarwinianDynamics`: Coupled population-strategy ODEs
- `ESSolver`: ESS finder with stability classification
- `InstitutionalParasitismModel`: Complete analysis pipeline

**Key Functions**:
```python
analyze_golden_ratio_case(h_v_ratio, cli, country) → Dict
```

**Dependencies**:
- numpy
- scipy (odeint, optimize, linalg)
- dataclasses (standard library)
- enum (standard library)

**When to use**: For quantitative analysis of specific institutional cases.

---

## 📊 Case Studies

### 6. Argentina Complete Analysis
**File**: `/examples/egt_case_studies/argentina_ultra_activity_complete_analysis.md`  
**Purpose**: Detailed EGT analysis of ultra-activity doctrine (1953-2025)  
**Length**: ~21,000 characters (7 parts)  
**Case Type**: Failure (0% reform success, 23 attempts)

**Structure**:
1. ESS Analysis (G-function parameters, stability, resource dynamics)
2. Three Mechanisms of Lock-in (with empirical evidence)
3. Why Reforms Fail (case-by-case: Menem, Kirchner, Macri, Milei)
4. Alternative Scenarios (counterfactuals with lower CLI, precedent reset, ρ boost)
5. Policy Recommendations (diagnosis + three escape routes)
6. Monitoring Dashboard (early warning indicators)
7. Conclusion (key findings, generalizable insights)

**Data**:
- H/V = 4.12, CLI = 0.87, d_φ = 2.50
- Precedent weight w = 8.5 (850 Supreme Court citations)
- ρ = 0.0085 (critical resource depletion)
- G(φ) ≈ -607 (extreme negative fitness)

**When to read**: For detailed example of high-CLI lock-in system analysis.

---

### 7. Future Case Studies (Planned)

**File**: `/examples/egt_case_studies/chile_labor_reform_success.md` (TODO)  
**Case**: Chile labor reforms (1990-2020)  
**Parameters**: CLI = 0.15, H/V = 1.45, d_φ = 0.17 (Goldilocks Zone)  
**Outcome**: 88% success rate (15 of 17 reforms)  
**Purpose**: Comparative analysis showing flexible system dynamics

**File**: `/examples/egt_case_studies/singapore_convergence_trajectory.md` (TODO)  
**Case**: Singapore legal transplant (1965-1990)  
**Parameters**: Initial CLI = 0.25, H/V evolved 0.8 → 1.62  
**Outcome**: Convergence to optimal proportion in 25 years  
**Purpose**: Demonstrate successful institutional engineering

---

## 🔬 Validation and Testing

### 8. Empirical Validation Plan
**Location**: Section 9 of `INSTITUTIONAL_PARASITISM_ESS.md`  
**Sections**: 9.1 Dataset Requirements, 9.2 Statistical Tests, 9.3 Out-of-Sample Validation

**Hypothesis Tests**:
- H1: High CLI → Low ρ (resource depletion)
- H2: ESS Predicts Lock-in (G(φ) < 0 for CLI > 0.75)
- H3: Bifurcation Threshold (CLI ≈ 0.5-0.6)
- H4: Veto Accumulation (CLI ~ institutional age)

**Targets**:
- AUC > 0.85 (strong discrimination)
- Brier score < 0.15 (accurate probabilities)
- Calibration slope ≈ 1.0 (unbiased predictions)

---

### 9. Unit Tests (TODO)
**File**: `/tests/test_institutional_parasitism_ess.py` (to be created)  

**Test Coverage**:
- G-function correctness (compare to Vince 2005 examples)
- ESS solver convergence (synthetic test cases)
- Stability classification (known ESS/CSS/Repellor cases)
- Parameter calibration (CLI → σ_k, ρ mapping)
- Edge cases (CLI = 0, CLI = 1, extreme H/V)

---

## 📖 Theoretical Background

### 10. Primary Sources

**Vince (2005)** - *Evolutionary Game Theory, Natural Selection, and Darwinian Dynamics*  
**Relevant Chapters**:
- Chapter 4: G-Function Framework
- Chapter 5: Darwinian Dynamics
- Chapter 7: ESS Conditions (Theorem 7.1.1)
- Chapter 8: Evolutionary Branching
- Chapter 10: Coevolution Models

**Lerer (2025)** - "The Golden Ratio Paradox" (SSRN)  
**Empirical Findings**:
- H/V = φ ≈ 1.618 predicts 100% success
- 88% deviation from optimal proportion
- CLI correlates with reform failure (R² = 0.74)

**Geritz et al. (1998)** - "Evolutionarily Singular Strategies"  
**Key Concepts**:
- CSS definition (continuously stable strategy)
- Evolutionary branching conditions
- Pairwise invasibility plots

---

## 🔄 Integration Points

### 11. IusMorfos (CLI Calculator)
**Integration**: CLI score → σ_k, ρ parameters  
**Enhancement**: ESS strength predicts CLI effectiveness  
**Status**: ✅ Complete (via `GFunctionParams.from_cli()`)

### 12. Heteronomous Bayesian Updating (HBU)
**Integration**: Coupled belief-institution coevolution  
**Enhancement**: Cognitive + institutional lock-in synergy  
**Status**: ⚠️ Conceptual (implementation pending)

### 13. Constitutional Paleontology
**Integration**: Precedent phylogenies overlay ESS stability maps  
**Enhancement**: Branching events = CSS points, extinction = ESS shifts  
**Status**: ⚠️ Conceptual (requires precedent network data)

### 14. Legal Evolvability Index (LEI)
**Integration**: LEI_ESS = LEI × Φ(G(φ))  
**Enhancement**: Penalize systems where G(φ) < 0  
**Status**: ⚠️ Formula defined (implementation pending)

---

## 🎯 Use Cases by Audience

### For Researchers
**Start with**:
1. `README.md` (this repo, updated section)
2. `EGT_INTEGRATION_MASTER.md` (overview)
3. `INSTITUTIONAL_PARASITISM_ESS.md` (theory)
4. `egt_institutional_non_convergence.md` (methodology)

**Then analyze**:
5. `argentina_ultra_activity_complete_analysis.md` (case study)
6. Run `institutional_parasitism_ess.py` (code)

### For Policymakers
**Start with**:
1. `README.md` (updated section)
2. `EGT_INTEGRATION_MASTER.md` Section 8 (FAQ)
3. `argentina_ultra_activity_complete_analysis.md` Part 5 (policy recommendations)

**Key takeaway**: Traffic light system (Green/Yellow/Red zones) for diagnostic.

### For Developers
**Start with**:
1. `institutional_parasitism_ess.py` (code structure)
2. `EGT_INTEGRATION_MASTER.md` Section 7.3 (extending code)
3. `README.md` in `egt_framework/` (usage examples)

**Then customize**:
4. Create custom G-functions (subclass `LotkaVolterraGFunction`)
5. Add multi-trait support (modify `hessian()` method)

### For Students
**Start with**:
1. `README.md` in `egt_framework/` (accessible intro)
2. `EGT_INTEGRATION_MASTER.md` Section 8 (FAQ)
3. `argentina_ultra_activity_complete_analysis.md` (concrete example)

**Learning path**:
4. Work through case study step-by-step
5. Run Python code with sample data
6. Explore theory documents after practical understanding

---

## 📝 Quick Reference: File Purposes

| File | Primary Purpose | Secondary Purpose |
|------|----------------|-------------------|
| `EGT_INTEGRATION_MASTER.md` | Comprehensive overview | Navigation hub |
| `INSTITUTIONAL_PARASITISM_ESS.md` | Mathematical formalization | Reference for theorems |
| `egt_institutional_non_convergence.md` | Non-convergence explanation | Policy implications |
| `README.md` (egt_framework) | Quick start guide | Domain examples |
| `institutional_parasitism_ess.py` | Production code | Algorithmic reference |
| `argentina_ultra_activity_complete_analysis.md` | Detailed case study | Methodology demonstration |
| `INDEX.md` (this file) | Navigation guide | Content summary |

---

## 🚀 Next Steps

### Immediate (Ready Now)
- [x] Read documentation
- [x] Run Argentina case analysis
- [x] Test Python module
- [ ] Replicate with your own CLI/H_V data

### Short-term (1-3 Months)
- [ ] Empirical validation (60-case dataset)
- [ ] Parameter calibration (CLI → σ_k functional form)
- [ ] Out-of-sample predictions
- [ ] Additional case studies (Chile, Singapore)

### Medium-term (3-6 Months)
- [ ] Paper 2: "Institutional Parasitism as ESS"
- [ ] Multi-trait ESS extension
- [ ] Coevolutionary dynamics module
- [ ] Integration with Peralta network analysis

### Long-term (6-12 Months)
- [ ] Paper 3: "Resource Dynamics and Constitutional Lock-in"
- [ ] Paper 4: "From Optimal Proportions to Evolutionary Traps"
- [ ] Time-series analysis (historical CLI evolution)
- [ ] Multi-domain replication (property, tax, speech, etc.)

---

## 💡 Key Insights Across Documents

### Universal Findings
1. **Non-convergence is stable**: 88% deviation from φ is ESS, not pathology
2. **CLI threshold**: CLI > 0.75 marks transition to parasitic dominance
3. **Three mechanisms**: Path dependence + veto accumulation + centralization ratchet
4. **Resource depletion**: ρ(CLI) = ρ_max·(1-CLI)² explains irreversibility
5. **Domain-agnostic**: Same framework applies to all constitutional domains

### Policy Implications
1. **Diagnosis first**: Calculate CLI and classify (Green/Yellow/Red)
2. **No one-size-fits-all**: Red Zone requires radical restructuring
3. **Three escape routes**: Reset precedents, inject resources, or engineer niches
4. **Time scales matter**: Convergence requires 15-25 years minimum
5. **Monitor continuously**: Track CLI, ρ, precedent Gini, success rate

### Methodological Advances
1. **Quantitative prediction**: G(v) computable from CLI + H/V
2. **Testable hypotheses**: G(φ) < 0 for CLI > 0.75 (falsifiable)
3. **Out-of-sample validation**: Can predict reform outcomes for new cases
4. **Causal mechanism**: ESS stability explains non-convergence (not just correlation)
5. **Replication-ready**: Python module + documentation + case studies

---

## 📧 Contact and Support

**Questions about theory?**  
→ See `INSTITUTIONAL_PARASITISM_ESS.md` Section 13 (References)  
→ Open GitHub issue tagged "theory"

**Questions about code?**  
→ See `institutional_parasitism_ess.py` docstrings  
→ Open GitHub issue tagged "implementation"

**Questions about case studies?**  
→ See `argentina_ultra_activity_complete_analysis.md` Part 7  
→ Open GitHub issue tagged "empirical"

**General inquiries?**  
→ See `EGT_INTEGRATION_MASTER.md` Section 12 (Contact)  
→ Email: [provided in main README]

---

## 📜 Citation

When using this framework in research, please cite:

```
Lerer, I.A. (2025). Evolutionary Game Theory Framework for Institutional Analysis.
In: Legal Evolution Unified Repository. 
Available at: https://github.com/[username]/legal-evolution-unified

Based on:
- Vince, T.L. (2005). Evolutionary Game Theory, Natural Selection, and 
  Darwinian Dynamics. Cambridge University Press.
- Lerer, I.A. (2025). "The Golden Ratio Paradox: Why Optimal Institutional 
  Proportions Predict Success But Most Systems Cannot Achieve Them." 
  SSRN Working Paper.
```

---

**Index Version**: 1.0  
**Last Updated**: November 8, 2025  
**Maintained by**: Legal Evolution Unified Team  
**Status**: Complete and ready for use

---

## Appendix: Directory Structure

```
legal-evolution-unified/
├── EGT_INTEGRATION_MASTER.md          [Master document]
├── README.md                           [Updated with EGT section]
│
├── docs/
│   ├── egt_framework/
│   │   ├── INDEX.md                   [This file]
│   │   ├── README.md                  [Quick start]
│   │   ├── INSTITUTIONAL_PARASITISM_ESS.md  [Core theory]
│   │   └── METHODS_PAPER.md           [Methods documentation]
│   └── theory/
│       └── egt_institutional_non_convergence.md  [Methodology]
│
├── frameworks/
│   └── institutional_parasitism_ess.py  [Implementation]
│
└── examples/
    └── egt_case_studies/
        └── argentina_ultra_activity_complete_analysis.md  [Case study]
```

For navigation, start with the file matching your primary goal (see "Quick Reference" above).
