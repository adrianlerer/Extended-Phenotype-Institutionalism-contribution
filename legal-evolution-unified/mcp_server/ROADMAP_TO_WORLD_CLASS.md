# Roadmap to World-Class MCP Server
**Legal Evolution Unified - Complete Development Plan**

Last Updated: 2025-11-11  
Current Status: **Phase 1 Complete** (3/10 tools + infrastructure)

---

## 🎯 Vision: End-to-End Autonomous Research System

Transform from "tool execution platform" to "AI Scientist for Legal Evolution" - autonomous system that:
1. Formulates research questions from case law
2. Designs multi-tool analysis pipelines
3. Executes experiments with tree search
4. Generates peer-reviewable papers
5. Complies with academic integrity standards

**Inspiration**: The AI Scientist v2 (arXiv:2504.08066) - first AI system to produce accepted workshop paper

---

## 📊 Current State (Phase 1: ✅ COMPLETE)

### Implemented (5,126 lines)
- ✅ MCP server infrastructure (`mcp_server/core/`)
- ✅ CLI Calculator (620 lines, 5 benchmarks)
- ✅ EGT Predictor (662 lines, Vince 2005)
- ✅ JurisRank (620 lines, PageRank adaptation)
- ✅ Basic workflows (570 lines)
- ✅ Tests (5/5 passing)
- ✅ Claude Desktop integration
- ✅ 98% token reduction validated

### Infrastructure Ready
- ✅ Tool registry system
- ✅ Caching layer (162 lines)
- ✅ Validation framework (79 lines)
- ✅ Logging system (37 lines)
- ✅ Config management (221 lines)

---

## 🚧 Phase 2: Complete Tool Integration (Priority: HIGH)

**Goal**: Connect remaining 7 tools to MCP server

### 2.1 RootFinder - Genealogical Tracing
**Status**: Tool exists in `tools/rootfinder/`, needs MCP wrapper  
**Effort**: 2-3 hours  
**Files to create**:
- `mcp_server/tools/rootfinder_tools.py` (~400 lines)

**Capabilities**:
```python
# Trace doctrine genealogy
genealogy = rootfinder_trace_lineage(
    case="Vizzoti 2004",
    depth=3,
    include_mutations=True
)

# Output: Complete ancestry tree with fidelity scores
```

**Integration points**:
- Connects to `tools/rootfinder/rootfinder.py` (existing)
- Uses ABAN algorithm (Ancestral Backward Analysis)
- Returns JSON genealogy trees

---

### 2.2 Legal-Memespace - Competitive Dynamics
**Status**: Tool exists in `tools/legal_memespace/`, needs MCP wrapper  
**Effort**: 2-3 hours  
**Files to create**:
- `mcp_server/tools/memespace_tools.py` (~450 lines)

**Capabilities**:
```python
# Map doctrinal competition
competition = memespace_analyze(
    doctrines=["textualismo", "purposivismo", "originalismo"],
    time_range=(1994, 2025),
    jurisdiction="argentina"
)

# Output: Lotka-Volterra dynamics, tipping points, survival probabilities
```

**Integration points**:
- Connects to `tools/legal_memespace/memespace.py`
- PCA clustering + K-means
- scipy.integrate.odeint for dynamics

---

### 2.3 Iusmorfos - Transplant Prediction
**Status**: Engine exists in `src/engines/iusmorfos_predictor.py`, needs MCP wrapper  
**Effort**: 3-4 hours  
**Files to create**:
- `mcp_server/tools/iusmorfos_tools.py` (~500 lines)

**Capabilities**:
```python
# Predict transplant success
prediction = iusmorfos_predict(
    source="brazil",
    target="argentina", 
    institution="labor_flexibility",
    domain="labor_law"
)

# Output: Success probability, implementation gap, adaptation recommendations
```

**Integration points**:
- Connects to `src/engines/iusmorfos_predictor.py`
- WEIRD/No-WEIRD distance metrics
- ML prediction model

---

### 2.4 Fibonacci Analyzer - Golden Ratio Detection
**Status**: Logic exists in `frameworks/institutional_parasitism_ess.py`, needs extraction  
**Effort**: 2 hours  
**Files to create**:
- `mcp_server/tools/fibonacci_tools.py` (~300 lines)

**Capabilities**:
```python
# Detect phi convergence
analysis = fibonacci_analyze(
    h_v_timeseries=[2.1, 1.9, 1.7, 1.65, 1.62],
    years=[2000, 2005, 2010, 2015, 2020]
)

# Output: Distance to φ, convergence rate, inflection points
```

**Integration points**:
- Extracts from `frameworks/institutional_parasitism_ess.py`
- scipy.optimize for φ-finding
- scipy.signal.find_peaks for inflection points

---

### 2.5 PSM Analyzer - Causal Inference
**Status**: Module exists in `src/causal_inference/psm.py`, needs MCP wrapper  
**Effort**: 3-4 hours  
**Files to create**:
- `mcp_server/tools/psm_tools.py` (~450 lines)

**Capabilities**:
```python
# Causal analysis
causal = psm_analyze(
    treatment_cases=[...],
    control_cases=[...],
    covariates=["gdp", "democracy", "cli"],
    outcome="reform_success"
)

# Output: ATE, confidence intervals, sensitivity analysis (Γ)
```

**Integration points**:
- Connects to `src/causal_inference/psm.py`
- Logistic regression for propensity scores
- Bootstrap for confidence intervals

---

### 2.6 Bootstrap Validator - Statistical Robustness
**Status**: Module exists in `code/bootstrap.py`, needs MCP wrapper  
**Effort**: 2 hours  
**Files to create**:
- `mcp_server/tools/bootstrap_tools.py` (~350 lines)

**Capabilities**:
```python
# Validate any result
validation = bootstrap_validate(
    data=[...],
    statistic="correlation",
    n_iterations=1000,
    confidence_level=0.95
)

# Output: CI (2.5%, 97.5%), p-value, BCa intervals
```

**Integration points**:
- Connects to `code/bootstrap.py`
- Implements percentile + BCa methods
- Works on any numeric result

---

### 2.7 Network Visualizer - Graph Analysis
**Status**: Module exists in `code/visualization.py`, needs MCP wrapper  
**Effort**: 3 hours  
**Files to create**:
- `mcp_server/tools/network_tools.py` (~400 lines)

**Capabilities**:
```python
# Visualize citation network
viz = network_visualize(
    cases=[...],
    citations=[...],
    layout="force_directed",
    export="html"
)

# Output: Interactive Plotly graph + centrality metrics
```

**Integration points**:
- Connects to `code/visualization.py`
- NetworkX for graph metrics
- Plotly for interactive viz

---

## 🤖 Phase 3: OpenRouter Autonomous Analysis (Priority: HIGH)

**Goal**: Enable LLM-powered autonomous analysis of legal documents

### 3.1 OpenRouter Integration
**Status**: Credentials exist in `.env`, needs implementation  
**Effort**: 4-5 hours  
**Files to create**:
- `mcp_server/autonomous/openrouter_client.py` (~300 lines)
- `mcp_server/autonomous/document_analyzer.py` (~400 lines)

**Capabilities**:
```python
# Autonomous case analysis
analysis = autonomous_analyze_case(
    case_url="https://...",
    tasks=["extract_doctrine", "identify_precedents", "classify_approach"],
    model="anthropic/claude-3.5-sonnet",
    budget_usd=0.50
)

# Output: Structured analysis + citations extracted
```

**Use cases**:
1. **RootFinder automation**: LLM reads case, extracts all citations, builds genealogy
2. **Memespace classification**: LLM identifies doctrinal position from text
3. **JurisRank seed data**: LLM builds initial citation network from corpus
4. **CLI component scoring**: LLM analyzes constitutional text for vagueness/activism

**Cost control**:
- Token counting pre-request
- Budget limits per task
- Caching of parsed documents
- Estimated: $0.10-0.50 per complete case analysis

---

### 3.2 Document Processing Pipeline
**Effort**: 3 hours  
**Files to create**:
- `mcp_server/autonomous/pdf_processor.py` (~200 lines)
- `mcp_server/autonomous/citation_extractor.py` (~250 lines)

**Capabilities**:
- Extract text from judicial PDFs
- Parse citations (formal + informal)
- Identify ratio decidendi vs obiter dicta
- Extract key dates, parties, holdings

---

## 🌲 Phase 4: AI Scientist v2 Integration (Priority: MEDIUM)

**Goal**: Implement agentic tree search for multi-tool workflows

### 4.1 Agentic Tree Search Framework
**Status**: Not started  
**Effort**: 8-10 hours  
**Files to create**:
- `mcp_server/agentic/tree_search.py` (~500 lines)
- `mcp_server/agentic/experiment_manager.py` (~400 lines)
- `mcp_server/agentic/hypothesis_generator.py` (~300 lines)

**Architecture** (inspired by AI Scientist v2):
```
Research Question
    ├─ Hypothesis 1 (RootFinder → genealogy identified)
    │   ├─ Sub-hypothesis 1.1 (JurisRank → fitness measured)
    │   │   └─ Experiment 1.1.1 (Memespace → competition analyzed)
    │   └─ Sub-hypothesis 1.2 (EGT → evolutionary dynamics)
    └─ Hypothesis 2 (Iusmorfos → transplant evaluated)
        └─ Sub-hypothesis 2.1 (PSM → causal validation)
```

**Key features**:
1. **Progressive exploration**: Best branches get deeper analysis
2. **Checkpoint system**: Save intermediate results, resume from best nodes
3. **Cost-aware**: Budget allocation across branches
4. **Pruning**: Eliminate low-promise hypotheses early

**Example workflow**:
```python
search = AgenticTreeSearch(
    question="Why does Argentina CLI=0.87 resist all reforms?",
    tools=["rootfinder", "jurisrank", "memespace", "egt", "psm"],
    max_depth=3,
    branches_per_level=2,
    budget_usd=10.00
)

result = search.explore()
# Output: 
# - Tree of 14 hypotheses (2^3 + 2^2 + 2^1)
# - Best path identified: RootFinder→JurisRank→EGT
# - 50-page report generated
```

---

### 4.2 Experiment Manager
**Effort**: 5 hours  
**Responsibilities**:
- Orchestrate tool execution order
- Manage data flow between tools
- Handle failures gracefully
- Cache intermediate results
- Track computational costs

---

### 4.3 Hypothesis Generator
**Effort**: 4 hours  
**Uses OpenRouter to**:
- Formulate testable hypotheses from initial question
- Suggest tool combinations for each hypothesis
- Predict which branches are most promising
- Generate experiment designs

---

## 📝 Phase 5: Automated Paper Generation (Priority: MEDIUM)

**Goal**: Generate peer-reviewable LaTeX papers from analysis results

### 5.1 Paper Generator
**Status**: Not started  
**Effort**: 6-8 hours  
**Files to create**:
- `mcp_server/paper/latex_generator.py` (~500 lines)
- `mcp_server/paper/figure_generator.py` (~400 lines)
- `mcp_server/paper/citation_formatter.py` (~200 lines)

**Capabilities**:
```python
paper = generate_paper(
    results={...},  # From agentic tree search
    template="ssrn",
    target_journal="Constitutional Political Economy",
    word_count=8000
)

# Output: Complete LaTeX + PDF + figures + BibTeX
```

**Sections auto-generated**:
1. Abstract (150-250 words)
2. Introduction (with literature review)
3. Methodology (tools used + parameters)
4. Results (tables + figures from analysis)
5. Discussion (interpretation + limitations)
6. Conclusion (contributions + future work)
7. References (auto-formatted citations)

---

### 5.2 VLM Figure Feedback Loop
**Effort**: 4 hours (inspired by AI Scientist v2)  
**Uses VLM to critique and improve figures**:
1. Generate initial figure (matplotlib/plotly)
2. VLM evaluates: clarity, aesthetics, compliance with journal style
3. Regenerate with improvements
4. Iterate until quality threshold met

---

## 🛡️ Phase 6: Guardian Protocol (Priority: HIGH for Academia)

**Goal**: Ensure AI-generated research meets integrity standards

### 6.1 Preregistration System
**Effort**: 3 hours  
**Files to create**:
- `mcp_server/guardian/preregistration.py` (~300 lines)

**Captures before analysis**:
- Research question
- Hypotheses (all, not just successful)
- Tools to be used
- Expected metrics
- Stopping criteria
- Timestamp + hash

**Output**: Preregistration JSON with cryptographic signature

---

### 6.2 Data & Code Cards
**Effort**: 2 hours  
**Files to create**:
- `mcp_server/guardian/data_card_generator.py` (~200 lines)
- `mcp_server/guardian/code_card_generator.py` (~200 lines)

**Data Card includes**:
- Dataset sources + versions
- Filtering applied
- Missing data handling
- Bias assessment
- Limitations

**Code Card includes**:
- Dependencies + versions
- Random seeds used
- Hyperparameters
- Computational environment
- Runtime costs

---

### 6.3 Disclosure Templates
**Effort**: 2 hours  
**Auto-generates**:
- "AI-assisted research" badge for papers
- Detailed methods appendix
- Reproducibility checklist
- Ethics statement template

---

### 6.4 Reproducibility Package
**Effort**: 3 hours  
**Bundles for publication**:
- All code (versioned)
- All data (or access instructions)
- Environment specification (Docker/conda)
- Seeds + hashes for verification
- Execution logs
- Preregistration certificate

---

## 🔄 Phase 7: Advanced Workflows (Priority: LOW)

### 7.1 Cross-Jurisdictional Comparison
**Effort**: 4 hours  
```python
comparison = cross_jurisdictional_workflow(
    countries=["argentina", "brazil", "spain", "poland"],
    domain="labor_law",
    analysis_depth="full"
)
```

Chains: CLI → EGT → Iusmorfos → PSM → Bootstrap for each country

---

### 7.2 Temporal Evolution Tracking
**Effort**: 5 hours  
```python
evolution = temporal_evolution_workflow(
    jurisdiction="argentina",
    domain="labor_law",
    start_year=1994,
    end_year=2025,
    interval_years=5
)
```

Chains: RootFinder → JurisRank → Fibonacci for each time slice

---

### 7.3 Doctrine Lifecycle Analysis
**Effort**: 6 hours  
```python
lifecycle = doctrine_lifecycle_workflow(
    doctrine="núcleo irreductible",
    jurisdiction="argentina",
    include_mutations=True
)
```

Chains: RootFinder → JurisRank → Memespace → EGT

---

## 📊 Effort Summary

| Phase | Description | Priority | Effort | Status |
|-------|-------------|----------|--------|--------|
| **Phase 1** | Infrastructure + 3 tools | HIGH | 40h | ✅ DONE |
| **Phase 2** | 7 remaining tools | HIGH | 18-21h | ⏳ Pending |
| **Phase 3** | OpenRouter autonomous | HIGH | 7-8h | ⏳ Pending |
| **Phase 4** | AI Scientist v2 tree search | MEDIUM | 17-19h | ⏳ Pending |
| **Phase 5** | Paper generation | MEDIUM | 10-12h | ⏳ Pending |
| **Phase 6** | Guardian Protocol | HIGH | 10h | ⏳ Pending |
| **Phase 7** | Advanced workflows | LOW | 15h | ⏳ Pending |
| **TOTAL** | Complete world-class system | - | **117-130h** | 31% done |

---

## 🎯 Immediate Next Steps (Option 4)

### Quick Win Package (2-3 hours)
1. ✅ **RootFinder integration** (1h) - Most requested tool
2. ✅ **Memespace integration** (1h) - Completes doctrine analysis trilogy
3. ✅ **OpenRouter basic** (45min) - Demonstrates autonomous analysis
4. ✅ **Guardian Protocol minimal** (30min) - Academic credibility

**Deliverable**: Working demo of autonomous doctrine evolution analysis:
```python
# Full autonomous analysis
result = await call_tool("doctrine_evolution_autonomous", {
    "doctrine": "núcleo irreductible",
    "start_year": 1994,
    "end_year": 2025,
    "use_llm": true,  # OpenRouter
    "generate_preregistration": true  # Guardian Protocol
})

# Output:
# 1. Preregistration certificate (timestamped)
# 2. RootFinder genealogy (LLM-extracted from 50 cases)
# 3. JurisRank fitness scores
# 4. Memespace competitive dynamics
# 5. Data card + code card
# 6. 20-page report with reproducibility package
```

---

## 📚 References

1. **The AI Scientist v2**: arXiv:2504.08066 (April 2025)
   - Agentic tree search methodology
   - VLM feedback loops
   - First workshop-accepted AI paper

2. **MCP Protocol**: Anthropic (2024)
   - 98% token reduction architecture
   - Tool execution paradigm

3. **Vince (2005)**: *Evolutionary Game Theory, Natural Selection, and Darwinian Dynamics*
   - G-functions for institutional fitness
   - ESS conditions

4. **Peralta Bootstrap**: Inherited validation framework
   - Non-parametric confidence intervals
   - Robustness testing

---

## 🚀 How to Contribute

1. Pick a Phase 2 tool (easiest entry point)
2. Create `mcp_server/tools/{tool_name}_tools.py`
3. Follow pattern from existing `cli_tools.py` or `egt_tools.py`
4. Add tests in `mcp_server/tests/test_{tool_name}_tools.py`
5. Update `mcp_server/server.py` to register new tool
6. Submit PR with "feat(mcp): Add {tool} integration"

---

**Last Updated**: 2025-11-11  
**Maintainer**: Ignacio Adrian Lerer  
**License**: MIT  
**Status**: Active Development (Phase 1 complete, Phase 2-7 in progress)
