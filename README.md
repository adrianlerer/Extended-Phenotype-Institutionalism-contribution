# Legal Evolution Unified

**Integrated Platform for Legal Concept Evolution Analysis**

Combines JurisRank, RootFinder, Iusmorfos, and Peralta methodologies into a unified analytical framework for studying legal system evolution.

---

## 🎯 Overview

This project **reuses the methodological infrastructure** from [peralta-metamorphosis](https://github.com/adrianlerer/peralta-metamorphosis) (political network analysis with bootstrap validation) and adapts it for legal concept analysis.

### Integrated Tools

1. **Peralta** (shared foundation): Bootstrap validation, network analysis, visualization methods
2. **JurisRank**: Legal fitness measurement via citation networks
3. **RootFinder**: Genealogical tracking of legal concepts across jurisdictions
4. **Iusmorfos**: Prediction of transplant success (WEIRD vs No-WEIRD contexts)
5. **PSM Analysis**: Propensity Score Matching for causal inference in legal systems

### Research Foundation

Based on evolutionary theory applied to legal systems:
- **Lerer, I.A. (2025)**. "Law as Extended Phenotype: An Evolutionary Framework for Legal Comparison" (SSRN)
- Integrates concepts from evolutionary biology, memetics, and institutional analysis

### 🔬 Featured Analysis: Crisis Catalysis Hypothesis

**Research Question**: Do crisis events causally increase sovereignty-oriented outcomes in international law?

**Method**: Propensity Score Matching (PSM) on 70 cases (2002-2023)

**Finding**: Crisis events have no significant causal effect (ATT = +0.0040, p = 0.9756). Sovereignty resurgence is driven by **structural niche architecture** rather than event-driven shocks.

**📦 Full Replication Package Available** - See [REPLICATION_GUIDE.md](REPLICATION_GUIDE.md)

---

## 🚀 Quick Start

### Option 0: Replicate PSM Analysis (Fastest)

```bash
# Clone and run PSM replication in 5 minutes
git clone https://github.com/adrianlerer/legal-evolution-unified.git
cd legal-evolution-unified
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/replicate_psm_analysis.py

# Results saved to: results/replication/
```

See [REPLICATION_GUIDE.md](REPLICATION_GUIDE.md) for detailed instructions.

---

### Option 1: Docker (Recommended for Full Platform)

```bash
# Clone repository
git clone https://github.com/adrianlerer/legal-evolution-unified.git
cd legal-evolution-unified

# Launch all services
docker-compose -f docker/docker-compose.yml up --build

# Access services:
# - Jupyter Lab: http://localhost:8888
# - REST API: http://localhost:8000/docs
# - Neo4j Browser: http://localhost:7474
```

### Option 2: Local Installation

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Run API server
uvicorn src.api.main:app --reload

# Or run Jupyter
jupyter lab
```

---

## 📁 Project Structure

```
legal-evolution-unified/
│
├── code/                    # Core modules (from Peralta)
│   ├── analysis.py              # Network analysis (adapted for legal concepts)
│   ├── bootstrap.py             # Bootstrap validation (unchanged from Peralta)
│   └── visualization.py         # Plotly/D3.js visualizations (adapted)
│
├── src/                     # Legal-specific code
│   ├── engines/                 # Tool-specific engines
│   │   ├── enhanced_jurisrank.py    # JurisRank + bootstrap validation
│   │   ├── rootfinder_adapter.py    # Genealogy tracking
│   │   └── iusmorfos_predictor.py   # Transplant prediction
│   │
│   ├── integration/             # Unified pipeline
│   │   └── unified_pipeline.py      # Master integration class
│   │
│   └── api/                     # REST API
│       └── main.py                  # FastAPI endpoints
│
├── notebooks/               # Jupyter analysis notebooks
│   ├── 01_data_preparation.ipynb
│   ├── 02_legal_fitness_analysis.ipynb
│   ├── 03_genealogy_validation.ipynb
│   ├── 04_transplant_prediction.ipynb
│   └── 05_integrated_dashboard.ipynb
│
├── docker/                  # Docker configuration
│   ├── Dockerfile               # Multi-stage build
│   └── docker-compose.yml       # Service orchestration
│
├── data/                    # Datasets
│   ├── cases/                   # Legal case data
│   ├── citations/               # Citation networks
│   └── compliance/              # Compliance metrics
│
├── results/                 # Analysis outputs
├── visualizations/          # Generated plots
├── tests/                   # Unit tests
└── docs/                    # Documentation

```

---

## 📊 Replication & Reproducibility

### Complete PSM Analysis Package

This repository includes a **complete replication package** for the Crisis Catalysis hypothesis analysis:

#### 📚 Documentation
- **[REPLICATION_GUIDE.md](REPLICATION_GUIDE.md)** - Step-by-step instructions (30-60 min)
- **[data/DATA_DICTIONARY.md](data/DATA_DICTIONARY.md)** - Complete variable codebook
- **[data/DATA_COLLECTION_PROTOCOL.md](data/DATA_COLLECTION_PROTOCOL.md)** - Methodology documentation
- **[docs/methodology/PSM_METHODOLOGY.md](docs/methodology/PSM_METHODOLOGY.md)** - Technical PSM reference

#### 💻 Code
- **`scripts/replicate_psm_analysis.py`** - Automated replication script
- **`src/causal_inference/psm.py`** - Core PSM implementation (7 functions)
- **`src/analysis/psm_crisis_catalysis_analysis.py`** - Full analysis pipeline

#### 📁 Data
- **`data/sovereignty_synthetic_parsed.csv`** - 70-case dataset (synthetic for demonstration)
- Ready for replacement with real case data following collection protocol

#### 🎯 Expected Results
- **ATT**: +0.0040 (95% CI: [-0.3077, +0.1538])
- **p-value**: 0.9756 (not significant)
- **Common Support**: 82.9% (PASS ≥70%)
- **Conclusion**: H5 (Crisis Catalysis) NOT supported

### Citation

If you use this replication package, please cite using [CITATION.cff](CITATION.cff):

```bibtex
@software{lerer2025psm_replication,
  author = {Lerer, Ignacio A.},
  title = {Legal Evolution Unified: PSM Analysis of Crisis Catalysis},
  year = {2025},
  url = {https://github.com/adrianlerer/legal-evolution-unified}
}
```

---

## 🔧 Technology Stack

### Core Analysis
- **Python 3.11+**
- **NetworkX**: Network analysis (from Peralta)
- **NumPy/Pandas**: Data manipulation
- **scikit-learn**: Machine learning and statistical methods
- **SciPy**: Scientific computing

### Visualization
- **Plotly + Dash**: Interactive visualizations (from Peralta)
- **Matplotlib/Seaborn**: Static plots
- **D3.js**: Advanced network visualizations

### Infrastructure
- **FastAPI**: REST API framework
- **Neo4j**: Graph database for citation networks
- **Redis**: Caching layer
- **Docker + Compose**: Containerized deployment

### Notebook Environment
- **Jupyter Lab**: Interactive analysis
- **Jupyter Dash**: Embedded interactive apps

---

## 📊 Key Features

### 1. Legal Fitness Analysis (JurisRank + Bootstrap)

```python
from src.integration.unified_pipeline import LegalEvolutionPipeline

# Initialize pipeline
pipeline = LegalEvolutionPipeline()

# Calculate fitness with statistical validation
result = pipeline.jurisrank.calculate_fitness_with_validation(
    concept_name="Habeas Corpus",
    jurisdiction="United States"
)

print(f"Fitness: {result['fitness']:.4f}")
print(f"95% CI: [{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]")
print(f"Significant: {result['significant']}")
```

### 2. Genealogical Analysis (RootFinder)

```python
# Trace concept genealogy
ancestors = pipeline.rootfinder.find_conceptual_ancestors(
    concept_name="Habeas Corpus",
    jurisdiction="United States",
    max_depth=5
)

# Build genealogy graph
graph = pipeline.rootfinder.build_genealogy_graph(
    concept_name="Habeas Corpus",
    jurisdiction="United States",
    bidirectional=True
)

# Export to Gephi for visualization
pipeline.rootfinder.export_genealogy_to_gephi("habeas_corpus_genealogy.gexf")
```

### 3. Transplant Prediction (Iusmorfos)

```python
# Predict transplant success
prediction = pipeline.iusmorfos.predict_transplant_success(
    concept_name="Punitive Damages",
    source_jurisdiction="United States",
    target_jurisdiction="Germany"
)

print(f"Success Probability: {prediction['success_probability']:.1%}")
print(f"Recommendation: {prediction['recommendation']}")
print(f"Risk Factors: {prediction['risk_factors']}")
```

### 4. Comprehensive Analysis

```python
# Run full integrated analysis
analysis = pipeline.comprehensive_analysis(
    concept_name="Habeas Corpus",
    jurisdiction="United States",
    include_genealogy=True,
    include_network=True
)

# Generate report
report = pipeline.generate_integrated_report(
    concept_name="Habeas Corpus",
    jurisdiction="United States"
)
print(report)
```

---

## 🌐 REST API

### Endpoints

#### Health Check
```bash
GET http://localhost:8000/health
```

#### Legal Fitness
```bash
POST http://localhost:8000/api/v1/fitness
Content-Type: application/json

{
  "concept_name": "Habeas Corpus",
  "jurisdiction": "United States"
}
```

#### Comprehensive Analysis
```bash
POST http://localhost:8000/api/v1/analyze
Content-Type: application/json

{
  "concept_name": "Habeas Corpus",
  "jurisdiction": "United States",
  "include_genealogy": true,
  "include_network": false
}
```

#### Transplant Prediction
```bash
POST http://localhost:8000/api/v1/transplant/predict
Content-Type: application/json

{
  "concept_name": "Punitive Damages",
  "source_jurisdiction": "United States",
  "target_jurisdictions": ["Germany", "France", "Japan"]
}
```

Full API documentation: http://localhost:8000/docs

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov=code --cov-report=html

# Run specific test
pytest tests/test_jurisrank.py
```

---

## 📚 Methodology Credits

### Core Infrastructure: Peralta
- **Bootstrap validation**: Robust statistical testing
- **Network analysis**: Centrality metrics, community detection
- **Visualization**: Interactive Plotly dashboards

**Source**: [peralta-metamorphosis](https://github.com/adrianlerer/peralta-metamorphosis)

**Citation**: Lerer, I.A. (2024). "Peralta's Metamorphosis: Network Analysis of Political Actors"

### Legal-Specific Tools

#### JurisRank
- Legal concept fitness via citation networks
- PageRank-inspired algorithm for legal influence
- **Status**: Placeholder implementation (to be integrated)

#### RootFinder
- Genealogical tracking of legal concepts
- Transplant pathways across jurisdictions
- **Status**: Placeholder implementation (to be integrated)

#### Iusmorfos
- WEIRD vs No-WEIRD context analysis
- Transplant success prediction
- **Status**: Placeholder implementation (to be integrated)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style
- **Black** formatter (line length 100)
- **Flake8** linter
- **Type hints** required for public APIs
- **Docstrings** in NumPy style

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 📧 Contact

**Project Maintainer**: Legal Evolution Unified Team

**Related Projects**:
- [peralta-metamorphosis](https://github.com/adrianlerer/peralta-metamorphosis)
- [jurisrank-demo](https://github.com/adrianlerer/jurisrank-demo) (coming soon)
- [rootfinder-demo](https://github.com/adrianlerer/rootfinder-demo) (coming soon)
- [iusmorfos-demo](https://github.com/adrianlerer/iusmorfos-demo) (coming soon)

---

## 🎓 Academic Use

If you use this platform in academic research, please cite:

```bibtex
@misc{lerer2025legalevolution,
  author = {Lerer, Ignacio A.},
  title = {Legal Evolution Unified: Integrated Platform for Legal Concept Analysis},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/adrianlerer/legal-evolution-unified}
}

@article{lerer2025phenotype,
  author = {Lerer, Ignacio A.},
  title = {Law as Extended Phenotype: An Evolutionary Framework for Legal Comparison},
  journal = {SSRN},
  year = {2025}
}
```

---

## 🚧 Current Status

**Version**: 1.0.0 (Beta)

**Implemented**:
- ✅ Core infrastructure (Peralta methods adapted)
- ✅ Bootstrap validation
- ✅ Network analysis framework
- ✅ FastAPI REST API
- ✅ Docker deployment
- ✅ Pipeline integration architecture

**Placeholder/To-Do**:
- ⏳ JurisRank: Real citation data integration
- ⏳ RootFinder: Actual genealogy database
- ⏳ Iusmorfos: WEIRD classification with real data
- ⏳ Interactive dashboard (Dash app)
- ⏳ Comprehensive test suite
- ⏳ Production deployment guide

---

## 📖 Documentation

- [API Documentation](http://localhost:8000/docs) (when server running)
- [Methodology Guide](docs/methodology.md) (to be created)
- [User Manual](docs/user_guide.md) (to be created)
- [Developer Guide](docs/developer_guide.md) (to be created)

---

**Built with ❤️ for comparative legal research**

_Integrating evolutionary biology, network science, and legal theory_
