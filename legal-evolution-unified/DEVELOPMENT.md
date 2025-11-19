# Development Guide

## Getting Started

This project integrates multiple legal analysis tools under a unified framework.

### Development Branch

All AI-assisted development occurs on the `genspark_ai_developer` branch.

### Local Development

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest

# Start API server
uvicorn src.api.main:app --reload
```

### Docker Development

```bash
# Build and run
docker-compose -f docker/docker-compose.yml up --build

# Access services
# - API: http://localhost:8000/docs
# - Jupyter: http://localhost:8888
# - Neo4j: http://localhost:7474
```

## Architecture Overview

### Core Modules (from Peralta)
- `code/bootstrap.py`: Statistical validation
- `code/analysis.py`: Network analysis
- `code/visualization.py`: Interactive plots

### Legal Engines
- `src/engines/enhanced_jurisrank.py`: Legal fitness
- `src/engines/rootfinder_adapter.py`: Genealogy
- `src/engines/iusmorfos_predictor.py`: Transplant prediction

### Integration
- `src/integration/unified_pipeline.py`: Master pipeline
- `src/api/main.py`: REST API

## Contributing

1. All work in `genspark_ai_developer` branch
2. Commit frequently with descriptive messages
3. Create PR to main when ready
4. Ensure tests pass before merging

## Code Style

- Black formatter (line length 100)
- Type hints for public APIs
- NumPy-style docstrings
