# Evolutionary Game Theory Framework for Constitutional Law

## ⚠️ CRITICAL: This Framework is DOMAIN-AGNOSTIC

**This is a UNIVERSAL tool for analyzing ANY constitutional topic, not limited to specific domains.**

Works for:
- ✅ Labor law reforms
- ✅ Property rights reforms  
- ✅ Tax/fiscal reforms
- ✅ Free speech doctrine
- ✅ Environmental regulations
- ✅ Criminal procedure
- ✅ **ANY constitutional domain you specify**

**Only input needed**: CLI score from IusMorfos for your domain of interest.

---

## Overview

This framework implements the **Darwinian Dynamics** approach from Vince (2005) *"Evolutionary Game Theory, Natural Selection, and Darwinian Dynamics"* (Cambridge University Press) applied to constitutional law evolution.

**Core Insight**: Constitutional doctrines evolve as **Evolutionarily Stable Strategies (ESS)** that resist legislative reforms through judicial precedent accumulation.

**Universal Application**: The same G-function, ESS solver, and bifurcation analysis work identically whether analyzing labor rights, property expropriation, tax reform, or free speech limits. The framework is completely domain-agnostic.

---

## 🎯 Reality Filter: Proven vs Hypothetical

### ✅ PROVEN (Rigorous Mathematical Theory from Vince 2005)

1. **G-Function Framework** (Chapter 4)
   - Fitness-Generating Function: G(v, u, x)
   - Per capita growth rate for strategy v in population (u, x)
   - **Status**: Mathematically proven, peer-reviewed

2. **ESS Maximum Principle** (Theorem 7.1.1)
   - ESS requires: max G(v, u, x*) = G(u_i, u, x*) = 0
   - Invasion resistance: ∂²G/∂v² < 0 (peak)
   - **Status**: Proven theorem, rigorously implemented

3. **Darwinian Dynamics** (Chapter 5)
   - Coupled population-strategy evolution
   - Timescale separation: T_evo >> T_eco
   - **Status**: Established theoretical framework

4. **Disruptive Selection → Speciation** (Chapter 8)
   - ∂²G/∂v² > 0 (valley) → evolutionary branching
   - Mechanism for doctrinal subdivision
   - **Status**: Proven mathematical result

5. **Coevolution Framework** (Chapter 10)
   - Multiple G-functions for interacting populations
   - Predator-prey analogue (legislative-judicial)
   - **Status**: Peer-reviewed theory

### ⚠️ HYPOTHETICAL (Requires Empirical Validation)

1. **CLI → sigma_k Mapping**
   - Hypothesis: High CLI → low sigma_k → speciation
   - **Status**: Testable hypothesis, NOT proven
   - **Method**: Linear inverse mapping (conservative)
   - **Validation Needed**: Empirical calibration with 60-case dataset

2. **Reform Success Prediction**
   - Hypothesis: G(u_reform, u_ess, x*) predicts success probability
   - **Status**: Logical extension, NOT validated
   - **Validation Needed**: Out-of-sample prediction accuracy

3. **Frequency-Wave Effects**
   - Hypothesis: Reform waves change adaptive landscape topology
   - **Status**: Plausible from theory, NOT empirically tested
   - **Validation Needed**: Time-series analysis of reform clustering

4. **Coevolutionary Red Queen**
   - Hypothesis: Legislative-judicial arms race strengthens lock-in
   - **Status**: Theoretical prediction, NOT observed
   - **Validation Needed**: Historical case studies with time dynamics

### ❌ SPECULATIVE (Explicitly Avoided in Implementation)

1. **Invented Coefficients**
   - ❌ NOT used: β_reform, ε_critical, τ_convergence with arbitrary values
   - ✅ USED: Parameters from Vince's worked examples (r=0.25, K_max=100, sigma ∈ [0.5, 4])

2. **Predictive Claims Without Data**
   - ❌ NOT claimed: "Reforms will fail with 93.4% probability"
   - ✅ CLAIMED: "ESS theory predicts high CLI → low reform success"

3. **Untestable Mechanisms**
   - ❌ NOT invoked: "Judicial neurons fire in ESS patterns"
   - ✅ INVOKED: "Precedent accumulation follows Darwinian selection gradient"

---

## 📊 Empirical Validation Status

### Dataset: 62 Labor Law Reforms (1991-2025)
- **Argentina**: CLI=0.87, N=23, Success=0% ✓ (Validates strong lock-in prediction)
- **Chile**: CLI=0.15, N=17, Success=88% ✓ (Validates weak lock-in prediction)
- **Brazil**: CLI=0.40, N=12, Success=67% ⚠️ (Moderate CLI, moderate success)
- **Spain**: CLI=0.35, N=10, Success=60% ⚠️ (Moderate CLI, moderate success)

**Validation Metrics** (from `empirical_validation.py`):
- Accuracy: TBD (to be computed)
- AUC: TBD
- Cross-validation: TBD

**Status**: Preliminary validation supports core predictions (high CLI → low success), but precise quantitative predictions require further calibration.

---

## 🔬 Mathematical Rigor: Implementation Details

### 1. G-Function (src/egt/g_function.py)

**Lotka-Volterra Model** (Example 4.1.1):
```
G(v, u, x) = r * [K(v) - sum_j x_j * a(v, u_j)] / K(v)

where:
  K(v) = K_max * exp(-v²/(2*sigma_k²))
  a(v, u_j) = exp(-(v - u_j - beta)²/(2*sigma_alpha²))
```

**Parameters**:
- `r = 0.25`: Intrinsic growth rate (from Vince Example 5.4.1)
- `K_max = 100.0`: Maximum carrying capacity (normalized units)
- `sigma_k`: Resource niche width (mapped from CLI)
- `sigma_alpha = 2.0`: Competition niche width
- `beta = 0.0`: Asymmetry (symmetric competition baseline)

**Legal Interpretation**:
- `v`: Doctrinal rigidity (strategy)
- `K(v)`: Maximum sustainable doctrine strength
- `a(v, u_j)`: Conflict between reform v and doctrine u_j
- `r * (K - competition) / K`: Net fitness of doctrine v

### 2. ESS Solver (src/egt/ess_solver.py)

**ESS Maximum Principle** (Theorem 7.1.1):
```
If u_c is ESS, then:
  1. max G(v, u, x*) = G(u_i, u, x*) = 0
  2. ∂²G/∂v² < 0 (negative curvature = peak)
```

**Implementation**:
- Darwinian Dynamics integration until convergence
- Hessian analysis for invasion resistance (IR)
- Convergent stability (CS) via perturbed simulations
- Classification: ESS (peak), CSS (valley → speciation), Repellor (saddle)

### 3. Darwinian Dynamics (src/egt/darwinian_dynamics.py)

**Coupled Equations**:
```
Population (fast):  dx_i/dt = x_i * G(u_i, u, x)
Strategy (slow):    du_i/dt = sigma² * ∂G/∂v|_{v=u_i}
```

**Quasi-Equilibrium Assumption**:
- If `T_evo >> T_eco` (separation ratio > 10), then x ≈ x*(u) always
- Allows ESS analysis on fixed adaptive landscape G*(v) = G(v, u, x*(u))
- **Legal interpretation**: Legislative activity (fast) reaches equilibrium before judicial doctrine (slow) changes

### 4. Bifurcation Analysis (src/egt/adaptive_landscape.py)

**CLI as Bifurcation Parameter**:
- Low CLI → Wide niche (sigma_k large) → Single ESS (doctrinal unity)
- High CLI → Narrow niche (sigma_k small) → Multiple ESS (doctrinal pluralism)

**Mechanism**: As CLI increases, competition intensifies → disruptive selection → speciation

---

## 🧬 Legal Analogy Table

| **Biology (Vince 2005)** | **Constitutional Law (Our Framework)** |
|--------------------------|---------------------------------------|
| Species strategy `u` | Judicial doctrine (level of rigidity) |
| Population density `x` | Doctrine strength (precedent weight) |
| Fitness `G(v, u, x)` | Reform viability (success probability) |
| ESS (peak) | Constitutional lock-in (núcleo irreductible) |
| CSS (valley) | Unstable doctrine → speciation |
| Speciation | Doctrinal subdivision (conflicting precedents) |
| Predation `b(v, u_j)` | Judicial blocking of reform v by doctrine u_j |
| Harvesting | Legislative reforms (external pressure) |
| ESOHS | Optimal reform strategy (incremental, not shock) |
| Chemotherapy resistance | Lock-in strengthens under reform pressure |
| Red Queen dynamics | Legislative-judicial arms race |
| Timescale separation | Reforms fast, precedent evolution slow |

---

## 📚 Integration with Existing Tools

### 1. IusMorfos (CLI Calculator)
- **Integration**: CLI score → sigma_k via `LotkaVolterraGFunction(params, cli)`
- **Enhancement**: ESS strength predicts CLI effectiveness
- **Status**: Ready for integration

### 2. JurisRank (Precedent Network)
- **Integration**: Precedent centrality → strategy u_i in G-function
- **Enhancement**: Network topology predicts ESS stability
- **Status**: Requires module development

### 3. RootFinder (Genealogy Tracer)
- **Integration**: Citation network → phylogenetic tree = strategy evolution trajectory
- **Enhancement**: Darwinian Dynamics models precedent accumulation paths
- **Status**: Requires module development

### 4. Peralta Network Analysis (Coalition Clusters)
- **Integration**: Voting clusters → multi-strategy coalition ESS
- **Enhancement**: Coalition ESS theory (Section 6.2) predicts cluster stability
- **Status**: Requires empirical validation

---

## 🚀 Usage Examples: Multi-Domain Application

### Example 1: Labor Law (Argentina)
```python
from src.egt import LotkaVolterraGFunction, ESSSolver, TimescaleParams

# Analyze labor law reform resistance
cli_labor = 0.87  # From IusMorfos for Art. 14bis
g_func = LotkaVolterraGFunction(base_params, cli_labor)
solver = ESSSolver(g_func, timescale_params)
result = solver.solve(u0=[0.0])

print(f"Labor Law ESS: {result.u_ess}")
print(f"Reform Viability: {'LOW' if cli_labor > 0.7 else 'HIGH'}")
# Output: Reform Viability: LOW (strong lock-in)
```

### Example 2: Property Rights (Argentina)
```python
# Analyze property expropriation doctrine
cli_property = 0.72  # From IusMorfos for property rights
g_func = LotkaVolterraGFunction(base_params, cli_property)
result = solver.solve(u0=[0.0])

print(f"Property ESS: {result.u_ess}")
print(f"Stability: {result.stability_type.value}")
# Output: Stability: ESS (invasion resistant)
```

### Example 3: Free Speech (Spain)
```python
# Analyze free speech doctrine evolution
cli_speech = 0.45  # From IusMorfos for Art. 20 Spanish Constitution
g_func = LotkaVolterraGFunction(base_params, cli_speech)
result = solver.solve(u0=[0.0])

print(f"Speech ESS: {result.u_ess}")
print(f"Reform Viability: {'MODERATE' if 0.3 < cli_speech < 0.6 else 'OTHER'}")
# Output: Reform Viability: MODERATE (mixed outcomes expected)
```

### Example 4: Environmental Law (Brazil)
```python
# Analyze environmental regulation doctrine
cli_environment = 0.35  # From IusMorfos for Amazon protection
g_func = LotkaVolterraGFunction(base_params, cli_environment)
result = solver.solve(u0=[0.0])

if result.stability_type == StabilityType.CSS:
    print("⚠️ WARNING: Doctrinal fragmentation risk (disruptive selection)")
else:
    print("✓ Stable unified doctrine")
```

### Example 5: Complete Multi-Domain Analysis
```python
from analysis.egt_validation.general_domain_analysis import GeneralDomainAnalyzer

# Analyze ANY constitutional domain
analyzer = GeneralDomainAnalyzer()

domains = [
    ConstitutionalDomain("Labor Law", cli=0.87, country="Argentina"),
    ConstitutionalDomain("Property", cli=0.72, country="Argentina"),
    ConstitutionalDomain("Free Speech", cli=0.45, country="Spain"),
    ConstitutionalDomain("Environment", cli=0.35, country="Brazil"),
    ConstitutionalDomain("Tax/Fiscal", cli=0.87, country="Argentina"),
]

# Generate comparative analysis
fig, results = analyzer.compare_domains(domains)
plt.savefig('multi_domain_comparison.png')
```

**Key Insight**: Same code, same G-function, different CLI inputs. The framework is completely domain-agnostic.

---

## 📖 References

### Primary Source
Vince, T.L. (2005). *Evolutionary Game Theory, Natural Selection, and Darwinian Dynamics*. Cambridge University Press. ISBN: 978-0-521-84170-2

### Application to Law
Lerer, I.A. (2025). *Constitutional Paleontology: Tracing the Ancestor's Tale of Legal Doctrines*. SSRN: https://ssrn.com/abstract=5660770

### Key Theorems Implemented
- **Theorem 7.1.1**: ESS Maximum Principle
- **Theorem 9.1.2**: Matrix-ESS for frequency-dependent selection
- **Equation 5.25**: First-order strategy dynamics
- **Chapter 8**: Evolutionary branching and speciation

---

## ⚠️ Limitations and Future Work

### Current Limitations
1. **Parameter Calibration**: CLI → sigma_k mapping is linear (conservative but not optimal)
2. **Reform Strategy Estimation**: Assumes reforms target u=0 (neutral point)
3. **Single-Trait Model**: Does not capture multi-dimensional doctrinal trade-offs
4. **Static ESS**: Does not model time-varying lock-in (requires coevolution module)

### Future Enhancements
1. **Empirical Calibration**: Maximum likelihood estimation of G-function parameters
2. **Multi-Trait Strategies**: Vector strategies for complex doctrinal dimensions
3. **Resource-Explicit Models**: Explicit resource dynamics (political capital, public support)
4. **Temporal Analysis**: Time-series of reform waves and precedent evolution
5. **Coalition ESS**: Multi-strategy equilibria for Peralta network clusters

---

## 📧 Contact

Ignacio A. Lerer  
SSRN: https://ssrn.com/abstract=5660770  
GitHub: https://github.com/[your-repo]/legal-evolution-unified

---

**Last Updated**: October 26, 2025  
**Framework Version**: 1.0.0  
**Status**: Core modules complete, empirical validation in progress
