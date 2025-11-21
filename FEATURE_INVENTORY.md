# 🔧 Feature Inventory - Legal Evolution Analysis Platform

**Version**: 1.0.0  
**Last Updated**: 2025-11-21  
**Total Features**: 15

---

## 📊 Overview

This document provides a comprehensive inventory of all analysis tools available in the Legal Evolution platform. Each tool can be used **independently** or **in combination** with others.

**Target Users**: Academic researchers, policy consultants, legal practitioners, political analysts, journalists, government agencies, think tanks, investment firms, and international organizations.

### Feature Statistics

| Category | Count | Default Status |
|----------|-------|----------------|
| **Calculation Tools** | 3 | ✅ All Enabled |
| **Analysis Tools** | 1 | ✅ Enabled |
| **Generation Tools** | 2 | ✅ Enabled |
| **Visualization Tools** | 3 | ✅ Enabled |
| **AI Assistant Tools** | 3 | ✅ Enabled |
| **Methodology Tools** | 3 | ⚠️ Pro/Enterprise |

### SaaS Tier Distribution

| Tier | Features | Access Level |
|------|----------|--------------|
| **Free** | 7 | Public access |
| **Basic** | 4 | Registered users |
| **Pro** | 3 | Paid subscription |
| **Enterprise** | 2 | Custom licensing |

---

## 📊 CALCULATION TOOLS

### 1. Constitutional Lock-In Calculator
**ID**: `cli_calculator`  
**Icon**: 📊  
**Tier**: Free  
**Status**: ✅ Enabled by default

**Description**:
Calculate Constitutional Lock-In Index (CLI) using the formula:

```
CLI = 0.35 × CE + 0.40 × UA + 0.25 × JPI
```

Where:
- **CE** = Constitutional Entrenchment (0.0-1.0)
- **UA** = Unilateral Amendment difficulty (0.0-1.0)
- **JPI** = Judicial Power Index (0.0-1.0)

**Use Cases**:
- **Academic**: Measure constitutional rigidity for comparative politics research
- **Policy**: Assess proposed constitutional reforms (e.g., "Will this amendment procedure cause gridlock?")
- **Legal**: Evaluate litigation strategy based on amendment difficulty
- **Political Analysis**: Predict regime stability for election coverage
- **Investment**: Score country risk for portfolio decisions
- **Government**: Design optimal constitutional flexibility for new democracies

**API Endpoint**: `/api/cli/calculate`

**Example**:
```json
Input: {"CE": 0.80, "UA": 0.85, "JPI": 0.55}
Output: {"CLI": 0.76, "profile": "Brittle Rigidity"}
```

**Documentation**: [CLI Calculator Guide](/docs/cli-calculator)

---

### 2. Cultural Lock-In Calculator
**ID**: `cli_cultural_calculator`  
**Icon**: 🏛️  
**Tier**: Free  
**Status**: ✅ Enabled by default

**Description**:
Calculate Cultural Lock-In Index (CLI_cultural) using Extended Phenotype Theory (EPT):

```
CLI_cultural = 0.40 × CT1 + 0.30 × CT2 + 0.30 × CT3
```

Where:
- **CT1** = Cultural Transmission - Narrative Stability (0.0-1.0)
- **CT2** = Cultural Transmission - Shock Resistance (0.0-1.0)
- **CT3** = Cultural Transmission - Policy Continuity (0.0-1.0)

**Use Cases**:
- **Academic**: Apply Extended Phenotype Theory to cultural-institutional analysis
- **Policy**: Assess whether formal reforms will have cultural support (e.g., "Will citizens accept this new constitution?")
- **Political Analysis**: Predict post-crisis institutional continuity (e.g., "Will Somalia Federal survive?")
- **Government/UN**: Evaluate cultural readiness for constitutional transitions
- **Journalism**: Explain why some constitutions fail despite "good design" on paper
- **Think Tanks**: Identify societies with strong vs weak institutional legitimacy

**API Endpoint**: `/api/cli/calculate-cultural`

**Example**:
```json
Input: {"CT1": 0.70, "CT2": 0.65, "CT3": 0.75}
Output: {"CLI_cultural": 0.70, "strength": "Strong transmission"}
```

**Documentation**: [CLI Cultural Guide](/docs/cli-cultural)

---

### 3. Dual-Index Framework Analyzer
**ID**: `dual_index_analyzer`  
**Icon**: 🎯  
**Tier**: Basic  
**Status**: ✅ Enabled by default  
**Dependencies**: `cli_calculator`, `cli_cultural_calculator`

**Description**:
Analyze CLI × CLI_cultural interaction to classify institutional profiles:

| CLI | CLI_cultural | Profile | Risk |
|-----|--------------|---------|------|
| ≥0.60 | ≥0.60 | **Stable Rigidity** | LOW |
| ≥0.60 | <0.60 | **Brittle Rigidity** | HIGH |
| <0.60 | ≥0.60 | **Adaptive Stability** | LOW |
| <0.60 | <0.60 | **Chaotic Fragility** | MEDIUM |

**Collapse Risk Threshold**: Interaction < 0.30 = HIGH RISK

**Use Cases**:
- **Academic**: Classify 100+ countries into stability profiles for comparative studies
- **Policy**: Identify "Brittle Rigidity" risk in client countries (World Bank, USAID assessments)
- **Investment**: Score collapse risk for sovereign debt portfolios
- **Political Analysis**: Predict regime durability for election forecasting
- **Legal**: Advise governments on avoiding "scaffold without foundation" constitutional design
- **Journalism**: Generate data-driven infographics on global constitutional stability
- **Think Tanks**: Produce stability rankings and policy recommendations

**API Endpoint**: `/api/cli/dual-index`

**Example**:
```json
Input: {"CLI": 0.76, "CLI_cultural": 0.34, "entity": "Somalia Federal"}
Output: {
  "profile": "Brittle Rigidity",
  "interaction": 0.26,
  "risk": "HIGH",
  "explanation": "High constitutional lock-in WITHOUT cultural foundation = scaffold without base"
}
```

**Documentation**: [Dual-Index Framework Guide](/docs/dual-index-framework)

---

## 🔍 ANALYSIS TOOLS

### 4. Constitutional Rootfinder
**ID**: `rootfinder`  
**Icon**: 🌳  
**Tier**: Pro  
**Status**: ⚠️ Pro tier required

**Description**:
Trace constitutional genealogy and identify origin clauses. Track provisions across constitutional versions to find "root" articles.

**Use Cases**:
- **Legal Practice**: Build historical arguments in constitutional litigation (e.g., "This right has existed unchanged for 172 years")
- **Policy**: Identify provisions safe to preserve vs ripe for reform
- **Academic**: Map constitutional diffusion across regions (e.g., Latin American constitutionalism)
- **Journalism**: Create timeline graphics showing constitutional evolution for news stories
- **Government**: Identify "borrowable" provisions from successful constitutions
- **Think Tanks**: Produce reports on constitutional longevity and stability
- **Heritage/Museums**: Document constitutional history for public education

**API Endpoint**: `/api/methodology/rootfinder`

**Example**:
```json
Input: {"article": "Art. 14", "constitution": "Argentina 2025"}
Output: {
  "root": "1853 Constitution, Art. 14",
  "genealogy": ["1853", "1949 (suspended)", "1994 (reinstated)"],
  "age": "172 years",
  "status": "Living fossil (unchanged)"
}
```

**Documentation**: [Rootfinder Guide](/docs/rootfinder)

---

## 📄 GENERATION TOOLS

### 5. Research Paper Builder
**ID**: `paper_builder`  
**Icon**: 📄  
**Tier**: Basic  
**Status**: ✅ Enabled by default

**Description**:
Automated SSRN-ready paper generation. Integrates tables, sections, appendices, and references into Word documents.

**Features**:
- Table integration (e.g., Table 4: Dual-Index Framework)
- Section generation (e.g., Section 6: Brittle Rigidity Discussion)
- Appendix creation (e.g., Appendix D: CLI_cultural Methodology)
- Citation management
- Figure placeholders with captions

**Use Cases**:
- **Academic**: Generate SSRN/journal-ready manuscripts in minutes
- **Policy Consulting**: Produce professional reports for clients (World Bank, think tanks)
- **Legal Briefs**: Auto-generate constitutional analysis memoranda
- **Journalism**: Create long-form investigative reports with embedded data
- **Government**: Produce policy white papers and legislative impact assessments
- **Investment**: Generate country risk reports for clients
- **NGOs**: Create advocacy reports on constitutional rights

**API Endpoint**: `/api/papers/build`

**Example**:
```json
Input: {"paper_id": "somalia_somalilandia_ept"}
Output: {
  "status": "success",
  "paragraphs": 629,
  "word_count": 18000,
  "download_url": "/downloads/SSRN_INTEGRATED.docx"
}
```

**Documentation**: [Paper Builder Guide](/docs/paper-builder)

---

### 6. Methodology Appendix Generator
**ID**: `appendix_generator`  
**Icon**: 📚  
**Tier**: Free  
**Status**: ✅ Enabled by default  
**Dependencies**: `paper_builder`

**Description**:
Generate detailed methodology appendices with formulas, data sources, validation procedures, and limitations.

**Appendix Types**:
- **Appendix A**: Data sources and collection methods
- **Appendix B**: Statistical procedures
- **Appendix C**: Robustness checks
- **Appendix D**: CLI_cultural methodology (Extended Phenotype Theory)

**Use Cases**:
- Document research methodology
- Ensure reproducibility
- Meet journal requirements

**API Endpoint**: `/api/papers/appendix`

**Documentation**: [Appendix Generator Guide](/docs/appendix-generator)

---

## 📈 VISUALIZATION TOOLS

### 7. CLI Matrix Visualizer
**ID**: `cli_matrix_visualizer`  
**Icon**: 📈  
**Tier**: Free  
**Status**: ✅ Enabled by default  
**Dependencies**: `dual_index_analyzer`

**Description**:
Generate CLI × CLI_cultural interaction matrix with quadrant visualization. Publication-quality 300 DPI output.

**Visual Elements**:
- Collapse risk threshold curve (hyperbola: CLI × CLI_cultural = 0.30)
- Quadrant shading (Stable Rigidity, Brittle Rigidity, Adaptive Stability, Chaotic Fragility)
- Country data points with labels
- Risk zones (red = high risk, green = low risk)

**Use Cases**:
- **Academic**: Generate publication-quality figures for papers (300 DPI)
- **Journalism**: Create infographics for news articles (e.g., "Why Somalia is at risk")
- **Policy Briefs**: Visualize stability assessments for donors/governments
- **Presentations**: Board slides for investment committees, policy conferences
- **Social Media**: Data visualizations for public education campaigns
- **Think Tank Reports**: Professional charts for policy recommendations
- **Government Dashboards**: Real-time monitoring of constitutional stability

**API Endpoint**: `/api/figures/cli-matrix`

**Example**:
```json
Input: {
  "countries": [
    {"name": "Somalia Federal", "CLI": 0.76, "CLI_cultural": 0.34},
    {"name": "Somalilandia", "CLI": 0.54, "CLI_cultural": 0.70}
  ]
}
Output: {
  "file": "figure3_cli_cultural_matrix.png",
  "size": "649 KB",
  "dpi": 300,
  "format": "PNG"
}
```

**Documentation**: [CLI Matrix Guide](/docs/cli-matrix)

---

### 8. Constitutional Timeline Generator
**ID**: `timeline_generator`  
**Icon**: 📅  
**Tier**: Free  
**Status**: ✅ Enabled by default

**Description**:
Create timeline visualizations of constitutional events (independence, reforms, crises, amendments).

**Use Cases**:
- Natural experiments visualization
- Historical analysis
- Constitutional evolution tracking

**API Endpoint**: `/api/figures/timeline`

**Example**:
```json
Input: {
  "country": "Somalia",
  "events": [
    {"year": 1960, "event": "Independence"},
    {"year": 1991, "event": "State collapse"},
    {"year": 2012, "event": "Federal Constitution"}
  ]
}
Output: {"file": "figure1_timeline.png", "size": "618 KB"}
```

**Documentation**: [Timeline Generator Guide](/docs/timeline-generator)

---

### 9. CLI Correlation Plotter
**ID**: `correlation_plotter`  
**Icon**: 📉  
**Tier**: Basic  
**Status**: ✅ Enabled by default  
**Dependencies**: `cli_calculator`

**Description**:
Generate scatterplots showing CLI correlations with governance outcomes.

**Available Correlations**:
- CLI vs Freedom House Political Rights Score
- CLI vs Conflict Deaths per 100k
- CLI vs GDP per capita
- CLI vs Corruption Perception Index

**Use Cases**:
- Validate CLI predictive power
- Demonstrate governance outcomes
- Statistical analysis

**API Endpoint**: `/api/figures/correlations`

**Documentation**: [Correlation Plotter Guide](/docs/correlation-plotter)

---

## 🤖 AI ASSISTANT TOOLS

### 10. Genspark Research Assistant
**ID**: `genspark_assistant`  
**Icon**: 🤖  
**Tier**: Free  
**Status**: ✅ Enabled by default

**Description**:
AI-powered chat interface for methodology queries. Context-aware responses with citations to documentation.

**Capabilities**:
- Formula explanations
- Data source recommendations
- Interpretation guidelines
- Code examples
- Literature references

**Use Cases**:
- Learn methodology
- Troubleshoot calculations
- Get implementation guidance

**API Endpoint**: `/api/chat/query`

**Example**:
```json
Input: {"question": "How is CLI_cultural calculated?"}
Output: {
  "answer": "CLI_cultural = 0.40×CT1 + 0.30×CT2 + 0.30×CT3...",
  "sources": ["APPENDICES_SPECIFICATIONS.md", "Appendix D"],
  "code_example": "..."
}
```

**Documentation**: [AI Assistant Guide](/docs/ai-assistant)

---

### 11. AI Code Reviewer
**ID**: `code_reviewer`  
**Icon**: 🔍  
**Tier**: Basic  
**Status**: ✅ Enabled by default

**Description**:
Automated code review for statistical correctness. Verifies CLI formulas, data validation, and reproducibility.

**Review Checks**:
- ✅ Formula implementation correctness
- ✅ Input validation (0.0-1.0 ranges)
- ✅ Data type consistency
- ✅ Docstring completeness
- ✅ Reproducibility (random seeds, file paths)

**Use Cases**:
- PR reviews
- Ensure statistical correctness
- Catch bugs before deployment

**API Endpoint**: `/api/review/code`

**Documentation**: [Code Reviewer Guide](/docs/code-reviewer)

---

### 12. AI Root Cause Analyzer
**ID**: `root_cause_analyzer`  
**Icon**: 🔧  
**Tier**: Pro  
**Status**: ⚠️ Pro tier required

**Description**:
Automated error analysis using AI. Explains data divergences, calculation anomalies, and build failures.

**Capabilities**:
- Detect out-of-range values (CLI > 1.0)
- Explain data divergences (Somalia vs Somalilandia)
- Suggest fixes with specific line numbers
- Trace error propagation

**Use Cases**:
- Debugging CLI calculations
- Data quality assurance
- Build failure diagnosis

**API Endpoint**: `/api/analyze/error`

**Example**:
```json
Input: {"error": "CLI_cultural = 1.34 (out of range)"}
Output: {
  "root_cause": "CT1 = 1.10 exceeds valid range (0.0-1.0)",
  "suggested_fix": "Check row 3, column CT1 in cli_data.csv",
  "likely_issue": "Data entry error (decimal point misplacement)"
}
```

**Documentation**: [Root Cause Analyzer Guide](/docs/root-cause-analyzer)

---

## 🧬 METHODOLOGY TOOLS

### 13. Extended Phenotype Theory Analyzer
**ID**: `ept_analyzer`  
**Icon**: 🧬  
**Tier**: Pro  
**Status**: ⚠️ Pro tier required

**Description**:
Apply Extended Phenotype Theory (EPT) framework to cultural dimensions. Analyze how constitutional "genes" create institutional "extended phenotypes".

**EPT Concepts**:
- **Genes**: Constitutional provisions (text)
- **Phenotypes**: Institutional structures (observed behavior)
- **Extended Phenotypes**: Cultural transmission mechanisms (CT1, CT2, CT3)

**Use Cases**:
- Theoretical analysis
- Cultural lock-in explanation
- EPT framework application

**API Endpoint**: `/api/methodology/ept`

**Documentation**: [EPT Analyzer Guide](/docs/ept-analyzer)

---

### 14. Constitutional Paleontology Tool
**ID**: `paleontology_tool`  
**Icon**: 🦴  
**Tier**: Enterprise  
**Status**: ⚠️ Enterprise tier required

**Description**:
Fossil analysis of constitutional provisions. Identify "living fossils" (provisions unchanged for 100+ years) and "extinction events" (provisions removed).

**Analysis Types**:
- **Living Fossils**: Provisions unchanged across all constitutional versions
- **Extinction Events**: Provisions removed/suspended
- **Revival Events**: Provisions reinstated after suspension
- **Mutation Analysis**: Provisions with minor textual changes

**Use Cases**:
- Constitutional longevity analysis
- Track provision survival rates
- Identify stable vs volatile constitutional elements

**API Endpoint**: `/api/methodology/paleontology`

**Example**:
```json
Input: {"article": "Art. 14", "constitution": "Argentina"}
Output: {
  "classification": "Living fossil",
  "age": "172 years (1853-2025)",
  "survival_rate": "100%",
  "extinction_events": 0,
  "mutations": 0
}
```

**Documentation**: [Paleontology Tool Guide](/docs/paleontology)

---

### 15. Legal Evolvability Golden Ratio
**ID**: `golden_ratio_detector`  
**Icon**: ⚖️  
**Tier**: Enterprise  
**Status**: ⚠️ Enterprise tier required

**Description**:
Detect optimal constitutional flexibility ratios (entrenchment vs adaptability). Calculate deviation from "golden ratio" for legal evolution (~0.618).

**Theory**:
Optimal constitutional systems balance rigidity (CLI) with cultural adaptability (CLI_cultural) near the golden ratio (φ ≈ 0.618).

**Use Cases**:
- Identify over-rigid systems (CLI >> 0.618)
- Identify under-rigid systems (CLI << 0.618)
- Optimize constitutional design

**API Endpoint**: `/api/methodology/golden-ratio`

**Example**:
```json
Input: {"CLI": 0.76, "entity": "Somalia Federal"}
Output: {
  "golden_ratio": 0.618,
  "deviation": "+23.6%",
  "assessment": "Over-rigid system",
  "recommendation": "Reduce entrenchment or increase adaptability mechanisms"
}
```

**Documentation**: [Golden Ratio Guide](/docs/golden-ratio)

---

## 🎛️ Feature Management

### How to Enable/Disable Features

**Via API**:
```bash
# Enable a feature
POST /api/features/enable
{"feature_id": "rootfinder"}

# Disable a feature
POST /api/features/disable
{"feature_id": "paleontology_tool"}

# Get feature status
GET /api/features/inventory
```

**Via UI**:
1. Navigate to **Settings > Feature Management**
2. Toggle individual features on/off
3. Changes apply immediately

**Via Configuration File**:
Edit `config/features.json`:
```json
{
  "rootfinder": {"enabled": true},
  "paleontology_tool": {"enabled": false}
}
```

---

## 📊 Usage Analytics (SaaS)

Track feature usage for each user:

| Metric | Description |
|--------|-------------|
| **Usage Count** | Total times feature used |
| **Last Used** | Timestamp of last usage |
| **Tier Access** | Free, Basic, Pro, Enterprise |
| **Dependencies** | Required features |

**API Endpoint**: `/api/analytics/usage`

---

## 🚀 Future Features (Roadmap)

| Feature | Category | Planned Tier | ETA |
|---------|----------|--------------|-----|
| **Multi-Country Comparator** | Analysis | Basic | Q2 2025 |
| **Real-Time CLI Dashboard** | Visualization | Pro | Q3 2025 |
| **Automated Literature Review** | AI Assistant | Pro | Q3 2025 |
| **Constitutional Diff Viewer** | Methodology | Basic | Q4 2025 |
| **PDF Report Exporter** | Generation | Free | Q1 2026 |

---

## 📚 Documentation Links

- **Quick Start Guide**: `/docs/quickstart`
- **API Reference**: `/api/docs`
- **Tutorial Videos**: `/docs/tutorials`
- **SaaS Pricing**: `/pricing`
- **Support**: `/support`

---

**Last Updated**: 2025-11-21  
**Maintained by**: Legal Evolution Research Team  
**Contact**: support@legal-evolution.ai
