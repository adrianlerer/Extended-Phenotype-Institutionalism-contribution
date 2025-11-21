# ⚖️ Legal Evolution Analysis Platform

**AI-Powered Constitutional Analysis & Policy Intelligence**

Multi-sector platform for constitutional law research, policy consulting, legal practice, political analysis, journalism, government agencies, and investment risk assessment.

---

## 🎯 What Can You Do With This Platform?

### 📊 **Calculate Constitutional Metrics**
- **CLI (Constitutional Lock-In Index)**: Measure constitutional rigidity
- **CLI_cultural**: Assess cultural transmission strength (Extended Phenotype Theory)
- **Dual-Index Analysis**: Classify institutional profiles (Brittle Rigidity, Adaptive Stability, etc.)

### 📈 **Generate Publication-Quality Visualizations** ⭐
- **CLI Matrix**: Quadrant charts showing collapse risk (300 DPI, publication-ready)
- **Constitutional Timelines**: Track events from independence to present
- **Correlation Plots**: CLI vs governance outcomes (Freedom House, conflict intensity, GDP)
- **Export formats**: PNG (high-res), SVG (vector), base64 (web embedding)

### 🌳 **Trace Constitutional Genealogy**
- **Rootfinder**: Find origin clauses across constitutional versions
- Identify "living fossil" provisions (unchanged 100+ years)
- Map constitutional borrowing across countries

### 📄 **Generate Professional Reports**
- Automated report assembly with tables, sections, appendices
- Multiple formats: research reports, policy briefs, legal memos, analysis documents
- Professional structure and formatting for diverse audiences

### 🤖 **AI-Powered Research Assistant**
- Ask questions about methodology, formulas, data sources
- Get Python code examples
- Receive interpretation guidance

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/adrianlerer/legal-evolution-unified.git
cd legal-evolution-unified

# Install dependencies
pip install -r requirements.txt
```

### Run Backend API

```bash
cd backend
uvicorn app:app --reload --port 8000
```

### Run Streamlit UI (Optional)

```bash
streamlit run frontend/streamlit/app.py
```

### Access API Documentation

Open http://localhost:8000/api/docs for interactive API documentation.

---

## 📊 Feature Inventory (15 Tools)

| Category | Tool | Description | Tier | API Endpoint |
|----------|------|-------------|------|--------------|
| **Calculation** | CLI Calculator | Calculate constitutional rigidity (CLI = 0.35×CE + 0.40×UA + 0.25×JPI) | Free | `/api/cli/calculate` |
| **Calculation** | CLI Cultural Calculator | Cultural transmission strength (CLI_cultural = 0.40×CT1 + 0.30×CT2 + 0.30×CT3) | Free | `/api/cli/calculate-cultural` |
| **Calculation** | Dual-Index Analyzer | Classify profiles: Brittle Rigidity, Adaptive Stability, etc. | Basic | `/api/cli/dual-index` |
| **Visualization** | **CLI Matrix Generator** | **Generate quadrant matrix with collapse risk threshold** | **Free** | `/api/figures/cli-matrix` |
| **Visualization** | **Timeline Generator** | **Create constitutional event timelines** | **Free** | `/api/figures/timeline` |
| **Visualization** | **Correlation Plotter** | **Scatterplots with trendlines (CLI vs outcomes)** | **Basic** | `/api/figures/correlation` |
| **Analysis** | Rootfinder | Trace constitutional provision genealogy | Pro | `/api/methodology/rootfinder` |
| **Generation** | Report Builder | Generate professional reports and documents | Basic | `/api/papers/build` |
| **Generation** | Appendix Generator | Create methodology appendices | Free | `/api/papers/appendix` |
| **AI Assistant** | Genspark Assistant | Methodology Q&A chatbot | Free | `/api/chat/query` |
| **AI Assistant** | Code Reviewer | Statistical correctness verification | Basic | `/api/review/code` |
| **AI Assistant** | Root Cause Analyzer | Error diagnosis and fix suggestions | Pro | `/api/analyze/error` |
| **Methodology** | EPT Analyzer | Apply Extended Phenotype Theory | Pro | `/api/methodology/ept` |
| **Methodology** | Paleontology Tool | Identify "living fossil" provisions | Enterprise | `/api/methodology/paleontology` |
| **Methodology** | Golden Ratio Detector | Optimal constitutional flexibility | Enterprise | `/api/methodology/golden-ratio` |

---

## 📈 Visualization Tools (Detailed)

### 1. CLI Matrix Visualizer

**Generate publication-quality CLI × CLI_cultural matrices**

```bash
curl -X POST http://localhost:8000/api/figures/cli-matrix \
  -H "Content-Type: application/json" \
  -d '{
    "countries": [
      {"name": "Somalia Federal", "CLI": 0.76, "CLI_cultural": 0.34, "color": "red"},
      {"name": "Somalilandia", "CLI": 0.54, "CLI_cultural": 0.70, "color": "green"},
      {"name": "Uruguay", "CLI": 0.75, "CLI_cultural": 0.77, "color": "blue"}
    ],
    "title": "Dual-Index Framework: Horn of Africa",
    "show_threshold": true,
    "threshold_value": 0.30,
    "dpi": 300
  }'
```

**Output**: Base64-encoded PNG (300 DPI) with:
- Quadrant shading (Stable Rigidity, Brittle Rigidity, Adaptive Stability, Chaotic Fragility)
- Collapse risk threshold curve (hyperbola: CLI × CLI_cultural = 0.30)
- Country data points with labels
- Legend and grid

**Use cases**:
- Academic papers (SSRN, journal articles)
- Policy briefs (World Bank, think tanks)
- Journalism (infographics for news articles)
- Presentations (board slides, conferences)

### 2. Timeline Generator

**Create constitutional event timelines**

```bash
curl -X POST http://localhost:8000/api/figures/timeline \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Somalia",
    "events": [
      {"year": 1960, "event": "Independence", "marker_color": "green"},
      {"year": 1991, "event": "State Collapse", "marker_color": "red"},
      {"year": 2012, "event": "Federal Constitution", "marker_color": "blue"}
    ],
    "title": "Somalia Constitutional Timeline (1960-2025)"
  }'
```

**Output**: Base64-encoded PNG (300 DPI) with:
- Horizontal timeline with year markers
- Event labels (alternating high/low for readability)
- Color-coded markers
- Custom start/end years

**Use cases**:
- Historical analysis for papers
- Legal briefs (constitutional evolution)
- Journalism (timeline graphics)
- Educational materials

### 3. Correlation Plotter

**Generate scatterplots showing CLI correlations**

```bash
curl -X POST http://localhost:8000/api/figures/correlation \
  -H "Content-Type: application/json" \
  -d '{
    "x_values": [0.76, 0.54, 0.75, 0.68, 0.55],
    "y_values": [2.5, 6.8, 7.2, 6.5, 5.8],
    "x_label": "CLI (Constitutional Lock-In Index)",
    "y_label": "Freedom House Political Rights Score",
    "title": "CLI vs Political Rights",
    "show_trendline": true
  }'
```

**Output**: Base64-encoded PNG (300 DPI) with:
- Scatterplot points
- Linear regression trendline
- Correlation coefficient (r)
- R² value
- Equation of line

**Use cases**:
- Validate CLI predictive power
- Academic papers (results section)
- Policy reports (governance outcomes)
- Investment analysis (risk metrics)

---

## 💻 Code Examples

### Calculate CLI

```python
import requests

response = requests.post('http://localhost:8000/api/cli/calculate', json={
    "entity": "Somalia Federal",
    "CE": 0.80,
    "UA": 0.85,
    "JPI": 0.55
})

data = response.json()
print(f"CLI: {data['CLI']}")  # 0.76
print(f"Classification: {data['classification']}")  # HIGH Lock-In
```

### Generate CLI Matrix

```python
import requests
import base64
from PIL import Image
import io

response = requests.post('http://localhost:8000/api/figures/cli-matrix', json={
    "countries": [
        {"name": "Somalia Federal", "CLI": 0.76, "CLI_cultural": 0.34, "color": "red"},
        {"name": "Somalilandia", "CLI": 0.54, "CLI_cultural": 0.70, "color": "green"}
    ],
    "dpi": 300
})

data = response.json()

# Decode base64 image
img_data = base64.b64decode(data['image_base64'])
img = Image.open(io.BytesIO(img_data))
img.save('cli_matrix.png')
print("✅ Matrix saved: cli_matrix.png")
```

### Query AI Assistant

```python
import requests

response = requests.post('http://localhost:8000/api/chat/query', json={
    "question": "How is CLI_cultural calculated?"
})

data = response.json()
print(f"Answer: {data['answer']}")
print(f"Sources: {', '.join(data['sources'])}")
```

---

## 🎯 Use Cases by Sector

### 📚 Academic Researchers
- **Reports**: Generate research papers with automated formatting
- **Figures**: Publication-quality visualizations (300 DPI PNG)
- **Validation**: Verify statistical correctness of CLI calculations
- **Citations**: Reference management and bibliography

### 🏛️ Policy Consultants & Think Tanks
- **Assessments**: Evaluate constitutional reform proposals
- **Reports**: Generate professional policy briefs
- **Visuals**: Create infographics for presentations
- **Risk Analysis**: Predict governance stability

### ⚖️ Legal Practitioners
- **Genealogy**: Trace constitutional provision origins with Rootfinder
- **Arguments**: Build historical arguments for litigation
- **Impact**: Assess constitutional amendment effects
- **Memos**: Generate legal analysis documents

### 📊 Political Analysts & Journalists
- **Stability**: Score regime stability and collapse risk
- **Graphics**: Generate data visualizations for articles
- **Comparisons**: Compare constitutional rigidity across countries
- **Predictions**: Forecast political outcomes

### 💼 Investment Firms & Risk Analysis
- **Country Risk**: Score political risk for portfolios
- **Metrics**: Track governance quality metrics
- **Crisis Prediction**: Predict constitutional crises
- **Reports**: Generate client risk assessments

### 🏢 Government & International Organizations
- **Design**: Constitutional design consulting (UN, World Bank, USAID)
- **Evaluation**: Post-conflict constitution assessment
- **Forecasting**: Institutional stability predictions
- **Programs**: Democratization program evaluation

---

## 🎛️ Feature Management

All 15 tools can be enabled/disabled individually:

**Via Configuration File** (`config/features.json`):
```json
{
  "cli_calculator": {"enabled": true},
  "cli_matrix_visualizer": {"enabled": true},
  "rootfinder": {"enabled": true},
  "paleontology_tool": {"enabled": false}
}
```

**Via API**:
```bash
# Enable feature
curl -X POST http://localhost:8000/api/features/enable \
  -d '{"feature_id": "rootfinder"}'

# Disable feature
curl -X POST http://localhost:8000/api/features/disable \
  -d '{"feature_id": "paleontology_tool"}'
```

---

## 📚 Documentation

- **[FEATURE_INVENTORY.md](FEATURE_INVENTORY.md)**: Complete catalog of 15 tools with examples
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: GitHub Pages, Streamlit Cloud, Vercel, Railway, Docker
- **[AI_DEVOPS_ENHANCEMENT_PROPOSAL.md](AI_DEVOPS_ENHANCEMENT_PROPOSAL.md)**: Infrastructure enhancement plan
- **API Reference**: http://localhost:8000/api/docs (interactive Swagger UI)

---

## 🔧 Backend Architecture

```
backend/
├── app.py                          # FastAPI main application
├── routes/
│   ├── cli_calculator.py           # CLI, CLI_cultural, Dual-Index endpoints
│   ├── figure_generator.py         # CLI Matrix, Timeline, Correlations
│   ├── paper_builder.py            # Report and document generation
│   └── ai_assistant.py             # Genspark chat interface
├── services/
│   ├── feature_registry.py         # 15 tools with enable/disable
│   └── monitoring.py               # Usage analytics, error tracking
└── requirements.txt                # Python dependencies
```

---

## 🚢 Deployment Options

| Platform | Use Case | Cost | Setup Time |
|----------|----------|------|------------|
| **Streamlit Cloud** | UI deployment | Free-$200/mo | 5 min |
| **Vercel** | Frontend + Serverless API | Free-$20/mo | 10 min |
| **Railway** | Backend API | $5-$50/mo | 10 min |
| **GitHub Pages** | Static docs | Free | 15 min |
| **Docker (self-hosted)** | Full control | $5-$100/mo | 30 min |

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-tool`)
3. Commit changes (`git commit -m 'Add new analysis tool'`)
4. Push to branch (`git push origin feature/new-tool`)
5. Open Pull Request

**AI Code Review**: Genspark automatically reviews all PRs for statistical correctness and reproducibility.

---

## 📝 License

MIT License - Open source for academic, commercial, and government use.

---

## 👥 Team

**Legal Evolution Analysis Platform**
- Constitutional Law & Political Science Research
- AI-Powered Multi-Sector Policy Intelligence
- Open-Source Analysis Tools

---

## 📞 Support

- **API Docs**: http://localhost:8000/api/docs
- **Issues**: [GitHub Issues](https://github.com/adrianlerer/legal-evolution-unified/issues)
- **Discussions**: [GitHub Discussions](https://github.com/adrianlerer/legal-evolution-unified/discussions)
- **Email**: support@legal-evolution.ai
- **Consulting**: consulting@legal-evolution.ai

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-21  
**Status**: ✅ Production Ready  
**GitHub**: https://github.com/adrianlerer/legal-evolution-unified
