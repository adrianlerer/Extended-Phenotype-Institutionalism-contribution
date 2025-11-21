# ⚖️ Legal Evolution Analysis Platform

**AI-Powered Constitutional Analysis & Policy Intelligence**

Analyze constitutional rigidity, political stability, and governance outcomes for academic research, policy consulting, legal practice, and political analysis.

[![CI/CD](https://github.com/your-org/legal-evolution-unified/actions/workflows/ai-powered-ci.yml/badge.svg)](https://github.com/your-org/legal-evolution-unified/actions)
[![Security](https://github.com/your-org/legal-evolution-unified/actions/workflows/security-scan.yml/badge.svg)](https://github.com/your-org/legal-evolution-unified/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Features

### 📊 Calculation Tools
- **CLI Calculator**: Constitutional Lock-In Index (rigidity measurement)
- **CLI Cultural Calculator**: Cultural transmission strength (Extended Phenotype Theory)
- **Dual-Index Analyzer**: Institutional profile classification (Brittle Rigidity, Adaptive Stability, etc.)

### 🔍 Analysis Tools
- **Rootfinder**: Constitutional genealogy tracing (identify provision origins)
- **EPT Analyzer**: Extended Phenotype Theory application to cultural dimensions
- **Paleontology Tool**: "Living fossil" provision identification

### 📄 Generation Tools
- **Paper Builder**: Automated SSRN-ready document generation
- **Appendix Generator**: Methodology appendix creation

### 📈 Visualization Tools
- **CLI Matrix Visualizer**: Quadrant matrix with collapse risk threshold
- **Timeline Generator**: Constitutional event timelines
- **Correlation Plotter**: CLI vs governance outcomes

### 🤖 AI Assistant Tools
- **Genspark Research Assistant**: Methodology Q&A chatbot
- **AI Code Reviewer**: Statistical correctness verification
- **Root Cause Analyzer**: Error diagnosis and fix suggestions

## 📦 Installation

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-org/legal-evolution-unified.git
cd legal-evolution-unified

# Install dependencies
pip install -r requirements.txt

# Run Streamlit UI
streamlit run frontend/streamlit/app.py

# Run Backend API (separate terminal)
cd backend
python app.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🎯 Quick Start Guide

### 1. Enable Features

Navigate to **Feature Manager** in the UI and enable the tools you need (all enabled by default).

### 2. Calculate CLI

```python
from backend.routes.cli_calculator import calculate_cli

result = calculate_cli({
    "entity": "Somalia Federal",
    "CE": 0.80,
    "UA": 0.85,
    "JPI": 0.55
})

print(f"CLI: {result['CLI']}")  # 0.76
```

### 3. Analyze Dual-Index

```python
result = analyze_dual_index({
    "entity": "Somalia Federal",
    "CLI": 0.76,
    "CLI_cultural": 0.34
})

print(f"Profile: {result['profile']}")  # Brittle Rigidity
print(f"Risk: {result['risk_level']}")  # HIGH
```

### 4. Generate Paper

```bash
# Via UI
streamlit run frontend/streamlit/app.py
# Navigate to Paper Builder

# Via API
curl -X POST http://localhost:8000/api/papers/build \
  -H "Content-Type: application/json" \
  -d '{"paper_id": "somalia_somalilandia_ept"}'
```

## 📚 Documentation

- **Feature Inventory**: [FEATURE_INVENTORY.md](FEATURE_INVENTORY.md) - Complete list of 15 research tools
- **AI DevOps Proposal**: [AI_DEVOPS_ENHANCEMENT_PROPOSAL.md](AI_DEVOPS_ENHANCEMENT_PROPOSAL.md) - Infrastructure enhancement plan
- **API Reference**: http://localhost:8000/api/docs (when backend running)
- **Deployment Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment instructions

## 🎛️ Feature Management

### Enable/Disable Tools

**Via UI**:
1. Navigate to **Feature Manager**
2. Toggle individual features
3. Changes apply immediately

**Via API**:
```bash
# Enable feature
curl -X POST http://localhost:8000/api/features/enable \
  -H "Content-Type: application/json" \
  -d '{"feature_id": "rootfinder"}'

# Disable feature
curl -X POST http://localhost:8000/api/features/disable \
  -H "Content-Type: application/json" \
  -d '{"feature_id": "paleontology_tool"}'
```

**Via Config File**:
Edit `config/features.json`:
```json
{
  "rootfinder": {"enabled": true},
  "paleontology_tool": {"enabled": false}
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 🔒 Security

Automated security scanning with:
- **Safety**: Python dependency vulnerabilities
- **Bandit**: Code security linting
- **Dependabot**: Automated dependency updates

```bash
# Manual security scan
safety check
bandit -r . -f json
```

## 🚢 Deployment

### GitHub Pages (Static UI)

```bash
# Build Streamlit to static HTML
streamlit build frontend/streamlit/app.py

# Deploy to GitHub Pages
gh-pages deploy
```

### Vercel (Streamlit)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Railway (Backend API)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway up
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📊 Usage Analytics (SaaS)

Track feature usage per user:

```bash
# Get usage statistics
curl http://localhost:8000/api/analytics/usage
```

**Metrics**:
- Total usage count per feature
- Last used timestamp
- SaaS tier access (free, basic, pro, enterprise)

## 🗺️ Architecture

```
┌─────────────────────────────────────┐
│  Frontend (Streamlit UI)            │
│  - Modular tool selection           │
│  - Feature explanations             │
│  - Real-time calculations           │
└─────────────────────────────────────┘
             ↓ HTTP/WebSocket
┌─────────────────────────────────────┐
│  Backend (FastAPI)                  │
│  - Feature registry                 │
│  - CLI calculation endpoints        │
│  - Paper generation                 │
│  - Genspark integration             │
└─────────────────────────────────────┘
             ↓ File System / Git
┌─────────────────────────────────────┐
│  Repository                         │
│  - knowledge_base/                  │
│  - simulation_module/               │
│  - visualizations/                  │
│  - reporting_engine/                │
└─────────────────────────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-tool`)
3. Commit changes (`git commit -m 'Add amazing tool'`)
4. Push to branch (`git push origin feature/amazing-tool`)
5. Open Pull Request (AI code review will run automatically)

## 🎯 Use Cases

### 📚 Academic Researchers
- Publish papers on constitutional law, comparative politics
- Generate SSRN-ready documents with automated formatting
- Validate statistical models and methodologies

### 🏛️ Policy Consultants & Think Tanks
- Assess constitutional reform proposals
- Predict governance stability risks
- Generate policy briefs and reports
- Compare constitutional frameworks across countries

### ⚖️ Legal Practitioners
- Trace constitutional provision genealogy (rootfinder)
- Analyze amendment difficulty for litigation strategy
- Identify "living fossil" provisions for historical arguments
- Constitutional impact assessments

### 📊 Political Analysts & Journalists
- Analyze regime stability and collapse risk
- Generate visualizations for reports and articles
- Compare constitutional rigidity across regions
- Predict political outcomes based on institutional design

### 🏢 Government & International Organizations
- Constitutional design consulting (UN, World Bank, USAID)
- Democratization program assessment
- Post-conflict constitution evaluation
- Institutional stability forecasting

### 💼 Investment Firms & Risk Analysis
- Political risk assessment for investments
- Country stability scoring
- Governance quality metrics
- Constitutional crisis prediction

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 👥 Team

**Legal Evolution Analysis Platform**
- Constitutional Law & Political Science
- AI-Powered Policy Intelligence
- Multi-Sector Analysis Tools

## 📞 Support

- **Documentation**: `/docs`
- **API Reference**: http://localhost:8000/api/docs
- **Issues**: [GitHub Issues](https://github.com/your-org/legal-evolution-unified/issues)
- **Email**: support@legal-evolution.ai
- **Consulting**: consulting@legal-evolution.ai

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-21  
**Status**: ✅ Production Ready
