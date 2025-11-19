# Tools Index: Legal Evolution Unified

**Complete reference for all 10 analytical tools in the unified framework.**

---

## Quick Reference Table

| # | Tool | One-Line Description | When to Use | Implementation |
|---|------|---------------------|-------------|----------------|
| 1 | [EGT Framework](#1-egt-framework) | Evolutionary game theory for institutional lock-in | Explain why systems persist at suboptimal φ | `frameworks/institutional_parasitism_ess.py` |
| 2 | [JurisRank](#2-jurisrank) | PageRank for legal doctrine fitness | Identify "winning" legal memes | `tools/jurisrank/jurisrank.py` |
| 3 | [RootFinder](#3-rootfinder) | ABAN genealogical tracking | Trace doctrinal ancestry across jurisdictions | `tools/rootfinder/rootfinder.py` |
| 4 | [Legal-Memespace](#4-legal-memespace) | Lotka-Volterra competitive dynamics | Predict phase transitions in doctrine space | `tools/legal_memespace/memespace.py` |
| 5 | [Iusmorfos](#5-iusmorfos) | WEIRD vs No-WEIRD transplant prediction | Assess cross-jurisdictional transplant viability | `src/engines/iusmorfos_predictor.py` |
| 6 | [Fibonacci Analyzer](#6-fibonacci-analyzer) | Detect proportional patterns | Find temporal convergence/divergence from φ | `src/analysis/fibonacci_analyzer.py` |
| 7 | [PSM Analysis](#7-psm-analysis) | Propensity Score Matching for causality | Establish causal effects without RCT | `src/causal_inference/psm.py` |
| 8 | [Bootstrap Validation](#8-bootstrap-validation) | Non-parametric confidence intervals | Validate statistical robustness | `code/bootstrap.py` |
| 9 | [Network Analysis](#9-network-analysis) | Graph theory for citation networks | Characterize structural properties | `code/visualization.py` |
| 10 | [CLI Calculator](#10-cli-calculator) | Constitutional Lock-in Index | Quantify reform blocking mechanisms | `src/metrics/cli_calculator.py` |

---

## Detailed Tool Descriptions

### 1. EGT Framework

**Evolutionary Game Theory for Institutional Non-Convergence**

**What it does**: 
Implements G-functions with trait-dependent carrying capacity (Vince 2005) to explain why institutional systems persist at suboptimal H/V ratios despite φ = 1.618 being empirically superior.

**Core Innovation**:
- **ESS vs CSS distinction**: Optimal proportions lie in fitness valleys (CSS), not peaks (ESS)
- **Parasitic strategies**: "Cumplimiento cosmético" (symbolic compliance) as evolutionarily stable
- **Three lock-in mechanisms**: Path dependence, veto accumulation, centralization ratchets

**When to use**:
- System shows chronic deviation from φ (d_φ > 2.0)
- Need to explain persistence of dysfunctional institutions
- Want quantitative prediction of reform success

**Key Functions**:
```python
from frameworks.institutional_parasitism_ess import analyze_golden_ratio_case

result = analyze_golden_ratio_case(
    h_v_ratio=4.12,  # Heredity/Variation
    cli=0.87,        # Constitutional Lock-in Index
    country="Argentina"
)
```

**Output**:
- ESS location (where system will converge)
- Parasitic advantage (fitness gain from symbolic compliance)
- Resource renewal rate ρ(CLI)
- Reform viability classification

**Documentation**: [docs/egt_framework/INSTITUTIONAL_PARASITISM_ESS.md](../egt_framework/INSTITUTIONAL_PARASITISM_ESS.md)

---

### 2. JurisRank

**PageRank for Legal Doctrine Fitness Measurement**

**What it does**:
Adapts Google's PageRank algorithm to measure "memetic fitness" of legal doctrines through citation network analysis. Doctrines with high JurisRank have superior "replicative strength" and higher probability of transgenerational persistence.

**Legal-Specific Modifications**:
1. **Temporal decay**: Recent citations weighted higher (5% annual decay default)
2. **Hierarchical weighting**: Supreme Court citations > Appellate > Trial courts
3. **Doctrinal coherence**: Cases with similar doctrines amplify mutually

**When to use**:
- Identify which doctrines will dominate future jurisprudence
- Predict doctrinal survival vs extinction
- Measure relative "fitness" of competing interpretations

**Key Functions**:
```python
from tools.jurisrank import JurisRank

ranker = JurisRank(damping_factor=0.85, temporal_decay=0.05)
scores = ranker.calculate_jurisrank(citation_matrix, case_metadata)
```

**Output**:
- Normalized fitness scores [0, 1] for each doctrine
- Convergence diagnostics (iterations, delta)
- Temporal evolution of fitness

**Examples**: [examples/jurisrank/](../../examples/jurisrank/)  
**Documentation**: [JURISRANK.md](JURISRANK.md)

---

### 3. RootFinder

**Genealogical Tracking via ABAN Algorithm**

**What it does**:
Implements **ABAN** (Ancestral Backward Analysis of Networks) to trace complete genealogies of legal doctrines across jurisdictions. Like phylogenetic analysis in biology, RootFinder identifies "founder cases" and tracks mutation accumulation through generations.

**Core Metrics**:
- **Inheritance fidelity**: Proportion of doctrinal elements retained
- **Mutation types**: Classifications of conceptual variations
- **Citation strength**: Robustness of precedential links
- **Doctrinal distance**: Conceptual divergence from ancestors

**When to use**:
- Answer "Where did this doctrine come from?" with precision
- Detect covert legal transplants (high similarity to foreign ancestry)
- Measure mutation rate between jurisdictions
- Build visualizable genealogy trees

**Key Functions**:
```python
from tools.rootfinder import RootFinder

finder = RootFinder()
ancestors = finder.find_conceptual_ancestors(
    concept_name="Habeas Corpus",
    jurisdiction="United States",
    max_depth=5
)

# Export to Gephi for visualization
finder.export_genealogy_to_gephi("habeas_corpus.gexf")
```

**Output**:
- Complete ancestry tree (JSON serializable)
- Generation numbers (temporal distance from root)
- Mutation analysis (what changed between generations)
- Gephi-compatible network export

**Examples**: [examples/rootfinder/](../../examples/rootfinder/)  
**Documentation**: [ROOTFINDER.md](ROOTFINDER.md)

---

### 4. Legal-Memespace

**Lotka-Volterra Competitive Dynamics in Doctrine Space**

**What it does**:
Models legal doctrines as "species" competing in multidimensional memetic space using adapted Lotka-Volterra equations. Predicts **when** major jurisprudential shifts will occur (not just if).

**Key Capabilities**:
- **Phase transitions**: Detect abrupt changes in doctrinal coordinates
- **Competition coefficients**: Quantify conflict intensity between rival doctrines
- **Survival probabilities**: Forecast which doctrines will dominate
- **Tipping points**: Identify when dominant doctrine collapses

**When to use**:
- Predict timing of major precedent overrulings
- Map competitive landscape of doctrinal space
- Strategic timing for constitutional litigation
- Detect approaching jurisprudential "speciation events"

**Key Functions**:
```python
from tools.legal_memespace import MemeSpace

memespace = MemeSpace(n_dimensions=3)
memespace.fit(doctrine_vectors, case_metadata)

# Predict future state
future_state = memespace.simulate_dynamics(t_max=10, dt=0.1)
tipping_points = memespace.detect_phase_transitions()
```

**Output**:
- PCA-reduced doctrinal coordinates
- Competition coefficients matrix
- Phase transition timestamps
- Survival probability trajectories

**Examples**: [examples/memespace/](../../examples/memespace/)  
**Documentation**: [MEMESPACE.md](MEMESPACE.md)

---

### 5. Iusmorfos

**Transplant Success Prediction (WEIRD vs No-WEIRD)**

**What it does**:
Predicts viability of legal transplants between jurisdictions using multidimensional cultural-institutional distance analysis. Distinguishes WEIRD (Western, Educated, Industrialized, Rich, Democratic) from No-WEIRD contexts.

**Core Analysis**:
- **Implementation gap**: Formal norm vs actual application disparity
- **WEIRD factors**: Individualism, rule of law, trust in institutions
- **Risk factors**: Specific incompatibilities (e.g., judicial activism + text vagueness)
- **PSM matching**: Find "natural twin" jurisdictions as controls

**When to use**:
- Evaluate ex-ante if copying foreign institution will work
- Identify specific adaptation requirements
- Avoid costly reforms with high failure probability
- South → North transplants (historically 8% success)

**Key Functions**:
```python
from src.engines.iusmorfos_predictor import IusmorfosPredictor

predictor = IusmorfosPredictor()
result = predictor.predict_transplant_success(
    concept_name="Punitive Damages",
    source_jurisdiction="United States",
    target_jurisdiction="Germany"
)
```

**Output**:
- Success probability with 95% CI (bootstrap validated)
- Risk factors ranked by importance
- Actionable recommendations for adaptation
- Matched control jurisdictions

**Examples**: [examples/iusmorfos/](../../examples/iusmorfos/)  
**Documentation**: [docs/iusmorfos_v6/](../iusmorfos_v6/)

---

### 6. Fibonacci Analyzer

**Proportional Pattern Detection in Institutional Time Series**

**What it does**:
Searches for Fibonacci sequences (1, 1, 2, 3, 5, 8, 13...) and golden ratio convergence in institutional evolution. Analyzes H/V ratios in sliding temporal windows to detect systematic approach/divergence from φ.

**Core Metrics**:
- **d_φ over time**: Distance to golden ratio trajectory
- **Inflection points**: Where system pivots toward/away from φ
- **Correlation with crises**: Link d_φ changes to exogenous shocks
- **Fibonacci ratios**: Detect discrete proportional jumps

**When to use**:
- Validate that φ is universal attractor (or not)
- Distinguish random fluctuation from systematic trends
- Identify "critical moments" in institutional evolution
- Test temporal stability of H/V measurements

**Key Functions**:
```python
from src.analysis.fibonacci_analyzer import FibonacciAnalyzer

analyzer = FibonacciAnalyzer()
trajectory = analyzer.analyze_hv_trajectory(
    h_values, v_values, timestamps
)

inflection_points = analyzer.find_inflections(trajectory)
```

**Output**:
- d_φ time series with confidence bands
- Inflection point detection (timestamps + magnitudes)
- Crisis correlation analysis
- Fibonacci ratio detection in sequences

**Examples**: [examples/fibonacci/](../../examples/fibonacci/)  
**Documentation**: [FIBONACCI.md](FIBONACCI.md)

---

### 7. PSM Analysis

**Propensity Score Matching for Causal Inference**

**What it does**:
Establishes causal effects of legal reforms without randomized controlled trials (RCTs) using statistical matching. Constructs "twin" pairs of treated and control cases with similar propensity scores.

**Core Steps**:
1. **Propensity score estimation**: Logistic regression predicting treatment
2. **Caliper matching**: Pair cases within 0.1 SD tolerance
3. **Common support check**: Verify >70% retention
4. **ATE calculation**: Average Treatment Effect with bootstrap CI
5. **Sensitivity analysis**: Test robustness to hidden bias (Γ thresholds)

**When to use**:
- Answer "Did reform X CAUSE outcome Y?" (causation not correlation)
- No experimental data available (observational studies only)
- Need credible counterfactuals
- Validate that H/V-success correlation is causal

**Key Functions**:
```python
from src.causal_inference.psm import perform_complete_psm_analysis

result = perform_complete_psm_analysis(
    df=cases_dataframe,
    treatment_var="reform_enacted",
    outcome_var="success_binary",
    covariates=["cli", "gdp_log", "democracy"]
)
```

**Output**:
- ATE with 95% CI
- Common support diagnostics (retention %)
- Covariate balance (pre/post matching)
- Sensitivity analysis (Rosenbaum bounds)

**Examples**: [examples/psm/](../../examples/psm/)  
**Full Replication**: [REPLICATION_GUIDE.md](../../REPLICATION_GUIDE.md)  
**Documentation**: [docs/methodology/PSM_METHODOLOGY.md](../methodology/PSM_METHODOLOGY.md)

---

### 8. Bootstrap Validation

**Non-Parametric Confidence Intervals (Peralta Legacy)**

**What it does**:
Generates robust confidence intervals without assuming parametric distributions. Resamples dataset with replacement N times (N=1000 default), recalculates statistic, constructs empirical distribution.

**Methods Supported**:
- **Percentile method**: Simple 2.5% and 97.5% quantiles
- **BCa intervals**: Bias-corrected and accelerated
- **Studentized bootstrap**: For hypothesis testing

**When to use**:
- Small sample sizes (N < 100)
- Non-normal distributions
- Validate that p-values aren't sampling artifacts
- All regressions in Golden Ratio paper systematically validated

**Key Functions**:
```python
from code.bootstrap import bootstrap_confidence_interval

ci_lower, ci_upper = bootstrap_confidence_interval(
    data=metric_values,
    statistic_func=np.mean,
    n_iterations=1000,
    confidence_level=0.95
)
```

**Output**:
- 95% CI for any statistic
- Bootstrap distribution visualization
- Bias correction diagnostics

**Validation Power**:
- R²=0.74 for CLI model maintains significance in **98.7%** of bootstrap iterations
- Threshold effects (100% vs 8%) robust across all resamples

**Documentation**: [BOOTSTRAP.md](BOOTSTRAP.md)

---

### 9. Network Analysis

**Graph Theory for Citation Network Characterization**

**What it does**:
Applies NetworkX algorithms to characterize citation network structure:
- **Centrality metrics**: Betweenness, eigenvector, degree, PageRank
- **Community detection**: Doctrinal clusters (Louvain, modularity)
- **Path analysis**: Shortest paths, average separation
- **Structural holes**: Identify brokerage opportunities

**When to use**:
- Visualize complete "jurisprudential landscape"
- Identify hub cases (highly cited) vs peripheral (isolated)
- Detect disconnected components (separate doctrinal lineages)
- Measure "small-world" properties (typically 6 degrees separation)

**Key Functions**:
```python
from code.visualization import visualize_citation_network

network_viz = visualize_citation_network(
    citation_matrix,
    case_metadata,
    layout="force_directed",
    color_by="temporality",
    size_by="jurisrank"
)
```

**Output**:
- Interactive Plotly visualizations
- Gephi-compatible exports (.gexf)
- Centrality metrics table
- Community structure analysis

**Examples**: [examples/network_analysis/](../../examples/network_analysis/)  
**Documentation**: [NETWORK_ANALYSIS.md](NETWORK_ANALYSIS.md)

---

### 10. CLI Calculator

**Constitutional Lock-in Index Quantification**

**What it does**:
Generates composite index [0,1] measuring constitutional rigidity via 5 weighted dimensions. **Dominant predictor** in reform success models (β=-0.86 standardized).

**Five Dimensions** (with weights):
1. **Text Vagueness** (25%): Interpretive latitude in constitutional text
2. **Judicial Activism** (25%): Extent of judge-made law vs strict textualism
3. **Treaty Hierarchy** (20%): Supranational norms entrenchment level
4. **Precedent Weight** (15%): Stare decisis strength
5. **Amendment Difficulty** (15%): Procedural barriers to formal amendment

**Empirical Validation**:
```
Reform_Success = 0.92 - 0.89×CLI
R² = 0.74, p < 0.001
```

**When to use**:
- Diagnose "sources of rigidity" in specific jurisdiction
- Compare reformability across jurisdictions
- Identify which dimension to target (JA and TV have highest weights)
- Input to EGT Framework for reform prediction

**Key Functions**:
```python
from src.metrics.cli_calculator import calculate_cli, calculate_cli_components

cli_score = calculate_cli(
    text_vagueness=0.75,
    judicial_activism=0.85,
    treaty_hierarchy=0.65,
    precedent_weight=0.70,
    amendment_difficulty=0.80
)  # → 0.76

# Get component breakdown
components = calculate_cli_components(cli_score)
```

**Output**:
- Overall CLI [0,1]
- Component scores breakdown
- Weighted contributions
- Comparison to benchmark jurisdictions

**Empirical Ranges**:
- Argentina: CLI = 0.87 (highest lock-in)
- Brazil: CLI = 0.34 (most flexible)
- Sample mean: CLI = 0.57 (SD = 0.18)

**Examples**: [examples/cli_calculator/](../../examples/cli_calculator/)  
**Documentation**: [CLI_CALCULATOR.md](CLI_CALCULATOR.md)

---

## Integrated Workflow

**Typical analysis sequence** using all 10 tools:

1. **CLI Calculator** → Quantify constitutional rigidity
2. **JurisRank** → Extract citation network, measure doctrine fitness
3. **RootFinder** → Trace genealogy of specific doctrine
4. **Legal-Memespace** → Map current competitive landscape
5. **Iusmorfos** → If cross-border, assess transplant viability
6. **Fibonacci Analyzer** → Analyze historical H/V trajectory
7. **EGT Framework** → Predict reform success, identify ESS
8. **PSM Analysis** → Validate causal effect (if intervention occurred)
9. **Bootstrap** → Compute confidence intervals for all metrics
10. **Network Analysis** → Visualize complete system structure

**Example**: [examples/end_to_end/complete_institutional_analysis.py](../../examples/end_to_end/)

---

## Tool Selection Guide

**"Which tool should I use for..."**

| Question | Recommended Tool(s) | Example |
|----------|-------------------|---------|
| Will this reform succeed? | CLI Calculator + EGT Framework | Argentina labor reform |
| Which doctrine will dominate? | JurisRank + Memespace | Competing constitutional interpretations |
| Where did this concept originate? | RootFinder | Habeas corpus genealogy |
| Can we transplant this law? | Iusmorfos + PSM | EU directive → Latin America |
| Is the system approaching/leaving φ? | Fibonacci Analyzer | Brazil 1988-2024 trajectory |
| Did the reform CAUSE the outcome? | PSM Analysis | Crisis catalysis hypothesis |
| Are my results statistically robust? | Bootstrap Validation | All regression models |
| What's the network structure? | Network Analysis + JurisRank | SCOTUS citation patterns |

---

## Contributing New Tools

To add a new tool to this framework:

1. Implement in appropriate location:
   - Core mechanics → `src/`
   - Standalone algorithms → `tools/`
   - Theoretical models → `frameworks/`

2. Create documentation:
   - Add entry to this INDEX.md
   - Create dedicated `docs/tools/TOOLNAME.md`
   - Include minimal working example

3. Provide examples:
   - Add `examples/toolname/` directory
   - At least 2 real case studies
   - Jupyter notebook tutorial

4. Add tests:
   - Unit tests in `tests/test_toolname.py`
   - Integration test in end-to-end workflow

5. Update main README.md:
   - Add to Quick Reference table
   - Update tool count in hero section

---

## License & Citation

All tools MIT Licensed. If using in academic work:

```bibtex
@software{lerer2025legal_evolution_unified,
  author = {Lerer, Ignacio A.},
  title = {Legal Evolution Unified: Integrated Analytical Framework},
  year = {2025},
  url = {https://github.com/adrianlerer/legal-evolution-unified}
}
```

**Individual tool citations**: See respective documentation files.

---

**Last Updated**: 2025-11-11  
**Framework Version**: 1.0.0  
**Total Tools**: 10
