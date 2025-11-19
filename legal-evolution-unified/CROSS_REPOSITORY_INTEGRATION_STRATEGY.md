# Cross-Repository Integration Strategy
**Version**: 1.0 (2025-11-03)  
**Purpose**: Architectural plan for merging legal-evolution-unified with IntegridAI suite  
**Status**: Design Phase

---

## I. REPOSITORY ARCHITECTURE

### Current State

```
┌─────────────────────────────────────────────┐
│  legal-evolution-unified (Academic)         │
│  ├── src/analysis/                          │
│  │   ├── complexity_heuristics.py           │
│  │   ├── interactive_coder.py               │
│  │   └── (NEW) regulatory_risk.py           │
│  ├── data/                                   │
│  │   ├── cases/                              │
│  │   ├── processed/                          │
│  │   └── raw/                                │
│  ├── ept_prakash_sunstein/                   │
│  ├── tests/                                  │
│  └── *.md (design docs)                      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  integridai-suite (Business Application)    │
│  ├── modules/                                │
│  │   ├── risk_eval/                          │
│  │   ├── compliance/                         │
│  │   └── due_diligence/                      │
│  ├── api/                                    │
│  │   └── routes/                             │
│  ├── dashboards/                             │
│  └── templates/                              │
└─────────────────────────────────────────────┘
```

---

## II. INTEGRATION PATTERNS

### Pattern 1: Submódulo Git (Recommended for MVP)

**Pros**:
- Preserva independencia de repos
- Versionado bidireccional
- Fácil sincronización

**Cons**:
- Complejidad en updates
- Dos historiales Git

**Implementation**:
```bash
cd integridai-suite
git submodule add https://github.com/adrianlerer/legal-evolution-unified.git modules/legal_evolution
git submodule update --init --recursive
```

**Usage in IntegridAI**:
```python
# integridai-suite/modules/risk_eval/rri_api.py
import sys
sys.path.insert(0, '../legal_evolution/src')

from analysis.regulatory_risk import RegulatoryRiskModule

class RRIService:
    def __init__(self):
        self.rri_module = RegulatoryRiskModule()
    
    def get_country_risk(self, country: str, year: int):
        return self.rri_module.calculate_rri(country, year)
```

---

### Pattern 2: Monorepo con Workspaces (Long-term)

**Pros**:
- Single source of truth
- Unified CI/CD
- Dependency management simplificado

**Cons**:
- Requiere reestructuración
- Más pesado para contributors

**Structure**:
```
integridad-monorepo/
├── packages/
│   ├── legal-evolution/      # Academic core
│   │   ├── package.json
│   │   └── src/
│   ├── risk-api/              # Business API
│   │   ├── package.json
│   │   └── src/
│   └── dashboard/             # Frontend
│       ├── package.json
│       └── src/
├── pnpm-workspace.yaml
└── turbo.json
```

---

### Pattern 3: Package Distribution (Production)

**Pros**:
- Desacoplamiento total
- Versionado semántico
- PyPI/npm distribution

**Cons**:
- Más overhead de packaging
- Lag entre repos

**Implementation**:
```python
# legal-evolution-unified/setup.py
from setuptools import setup, find_packages

setup(
    name='iusmorfos-risk',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.23.0',
        'scikit-learn>=1.2.0'
    ]
)

# integridai-suite/requirements.txt
iusmorfos-risk==1.0.0
```

---

## III. RECOMMENDED APPROACH (PHASE-BASED)

### Phase 1: Git Submodule (Weeks 1-4)

**Goal**: Proof of concept with minimal refactoring

**Steps**:
1. Add legal-evolution-unified as submodule to integridai-suite
2. Create thin wrapper API in integridai-suite:
   ```python
   # integridai-suite/modules/risk_eval/regulatory_risk_service.py
   from legal_evolution.src.analysis.regulatory_risk import RegulatoryRiskModule
   
   class RegulatoryRiskService:
       def __init__(self):
           self.module = RegulatoryRiskModule()
       
       def calculate(self, country, year):
           return self.module.calculate_rri(country, year)
   ```
3. Test with 5 pilot countries
4. Deploy to staging

**Deliverable**: Working API endpoint at `/api/v1/rri/{country}/{year}`

---

### Phase 2: Shared Package (Months 2-3)

**Goal**: Distribute via PyPI for external users

**Steps**:
1. Extract core logic to `iusmorfos-risk` package
2. Publish to PyPI
3. Update both repos to use package:
   ```bash
   pip install iusmorfos-risk
   ```
4. Maintain backward compatibility

**Deliverable**: `pip install iusmorfos-risk` works for external developers

---

### Phase 3: Monorepo Migration (Months 4-6)

**Goal**: Unified development experience

**Steps**:
1. Create new repo `integridad-platform`
2. Migrate with history preservation:
   ```bash
   git filter-repo --to-subdirectory-filter packages/legal-evolution
   ```
3. Set up Turborepo/Nx for build orchestration
4. Migrate CI/CD pipelines

**Deliverable**: Single repo with multiple workspaces

---

## IV. API INTEGRATION LAYER

### Bridge Service Architecture

```python
# integridai-suite/modules/risk_eval/framework_bridge.py

from typing import Dict, Any
from legal_evolution.src.analysis.regulatory_risk import RegulatoryRiskModule
from legal_evolution.src.analysis.iusmorfos_integrator import IusMorfosIntegrator

class RiskFrameworkBridge:
    """
    Unified interface for all risk frameworks.
    Implements Facade pattern to hide complexity from API layer.
    """
    
    def __init__(self):
        self.rri = RegulatoryRiskModule()
        self.iusmorfos = IusMorfosIntegrator()
        self._cache = {}  # Simple in-memory cache
    
    def get_unified_assessment(self, country: str, year: int) -> Dict[str, Any]:
        """
        Single endpoint for all risk metrics.
        
        Returns:
        {
            'country': str,
            'year': int,
            'icrg_standard': {...},
            'rri': {...},
            'iusmorfos_12d': {...},
            'coface_equivalent': str,
            'recommendation': str
        }
        """
        cache_key = f"{country}_{year}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Calculate all frameworks
        result = {
            'country': country,
            'year': year,
            'icrg_standard': self._calculate_icrg(country, year),
            'rri': self.rri.calculate_rri(country, year),
            'iusmorfos_12d': self.iusmorfos.calculate_all(country, year),
            'coface_equivalent': self._map_to_coface(country, year),
            'recommendation': self._generate_recommendation(country, year)
        }
        
        self._cache[cache_key] = result
        return result
    
    def _calculate_icrg(self, country: str, year: int) -> Dict:
        """Calculate ICRG composite from IusMorfos + external data"""
        # Implementation from ONTOLOGY_MAPPING document
        pass
    
    def _map_to_coface(self, country: str, year: int) -> str:
        """Map ICRG composite to Coface A1-E scale"""
        # Implementation from ONTOLOGY_MAPPING document
        pass
    
    def _generate_recommendation(self, country: str, year: int) -> str:
        """Generate business recommendation based on all metrics"""
        rri = self.rri.calculate_rri(country, year)['rri']
        
        if rri >= 0.70:
            return "Low regulatory risk - standard investment terms"
        elif rri >= 0.50:
            return "Moderate risk - require regulatory change clauses"
        elif rri >= 0.30:
            return "High risk - demand political risk insurance"
        else:
            return "Very high risk - avoid or sovereign guarantees required"
```

---

### FastAPI Endpoints

```python
# integridai-suite/api/routes/rri.py

from fastapi import APIRouter, HTTPException
from modules.risk_eval.framework_bridge import RiskFrameworkBridge

router = APIRouter(prefix="/api/v1", tags=["Regulatory Risk"])
bridge = RiskFrameworkBridge()

@router.get("/country-risk/{country}/{year}")
async def get_country_risk(country: str, year: int):
    """
    Get comprehensive country risk assessment.
    
    Example: GET /api/v1/country-risk/USA/2024
    """
    try:
        return bridge.get_unified_assessment(country, year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rri/{country}/{year}")
async def get_rri(country: str, year: int):
    """
    Get Regulatory Risk Index only.
    
    Example: GET /api/v1/rri/Germany/2024
    """
    try:
        result = bridge.get_unified_assessment(country, year)
        return result['rri']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_countries(countries: List[str], year: int):
    """
    Compare multiple countries side-by-side.
    
    Example: POST /api/v1/compare
    Body: {"countries": ["USA", "Germany", "Argentina"], "year": 2024}
    """
    try:
        results = {}
        for country in countries:
            results[country] = bridge.get_unified_assessment(country, year)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## V. DATA SYNCHRONIZATION STRATEGY

### Challenge: legal-evolution-unified has CSV data, IntegridAI might use PostgreSQL

**Solution**: Data Adapter Pattern

```python
# integridai-suite/modules/data/adapters.py

from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy import create_engine

class DataAdapter(ABC):
    @abstractmethod
    def get_iusmorfos_scores(self, country: str, year: int) -> dict:
        pass
    
    @abstractmethod
    def get_icrg_data(self, country: str, year: int) -> dict:
        pass

class CSVDataAdapter(DataAdapter):
    """For academic repo (CSV-based)"""
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
    
    def get_iusmorfos_scores(self, country: str, year: int) -> dict:
        df = pd.read_csv(f"{self.data_dir}/iusmorfos_12d_scores.csv")
        row = df[(df['Country'] == country) & (df['Year'] == year)]
        return row.to_dict('records')[0] if not row.empty else None

class PostgreSQLAdapter(DataAdapter):
    """For business application (database)"""
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
    
    def get_iusmorfos_scores(self, country: str, year: int) -> dict:
        query = f"""
            SELECT * FROM iusmorfos_scores 
            WHERE country = '{country}' AND year = {year}
        """
        df = pd.read_sql(query, self.engine)
        return df.to_dict('records')[0] if not df.empty else None

# Usage
class RegulatoryRiskModule:
    def __init__(self, adapter: DataAdapter):
        self.adapter = adapter
    
    def calculate_rri(self, country, year):
        iusmorfos_data = self.adapter.get_iusmorfos_scores(country, year)
        # ... rest of calculation
```

---

## VI. CI/CD PIPELINE INTEGRATION

### Dual Deployment Strategy

```yaml
# .github/workflows/deploy-unified.yml

name: Deploy Unified Risk Platform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-academic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true  # Pull legal-evolution submodule
      
      - name: Test legal-evolution
        working-directory: modules/legal_evolution
        run: |
          pip install -r requirements.txt
          pytest tests/
  
  test-business:
    runs-on: ubuntu-latest
    needs: test-academic
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      
      - name: Test IntegridAI
        run: |
          pip install -r requirements.txt
          pytest tests/
  
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [test-academic, test-business]
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to staging
        run: |
          # Deploy to AWS/GCP/Azure
          # Update submodule reference
          git submodule update --remote
```

---

## VII. VERSIONING STRATEGY

### Semantic Versioning Across Repos

```
legal-evolution-unified: v1.2.3
                          │ │ │
                          │ │ └─ Patch: Bug fixes, data updates
                          │ └─── Minor: New features (RRI, JIS, RCI)
                          └───── Major: Breaking API changes

integridai-suite: v2.5.1
                   │ │ │
                   │ │ └─ Patch: UI fixes, endpoint tweaks
                   │ └─── Minor: New dashboard, API endpoints
                   └───── Major: Architecture change, DB migration
```

**Dependency Pinning**:
```yaml
# integridai-suite/.gitmodules
[submodule "modules/legal_evolution"]
    path = modules/legal_evolution
    url = https://github.com/adrianlerer/legal-evolution-unified.git
    branch = v1.2.x  # Pin to minor version, allow patches
```

---

## VIII. DOCUMENTATION SYNC

### Shared Documentation Strategy

```
docs/ (in integridai-suite)
├── api/
│   ├── openapi.yaml          # Auto-generated from FastAPI
│   └── endpoints.md
├── methodology/
│   ├── RRI_v1.0.md            # Copied from legal-evolution
│   ├── ICRG_mapping.md        # Copied from ONTOLOGY_MAPPING
│   └── use_cases.md           # Business-specific
└── integration/
    ├── architecture.md        # This document
    └── data_flow.md
```

**Sync Script**:
```bash
#!/bin/bash
# sync_docs.sh - Run after legal-evolution updates

cp modules/legal_evolution/COUNTRY_RISK_REGULATORY_FRAMEWORK_DESIGN.md \
   docs/methodology/RRI_v1.0.md

cp modules/legal_evolution/ONTOLOGY_MAPPING_REGULATORY_RISK.md \
   docs/methodology/ICRG_mapping.md

echo "Documentation synced from legal-evolution-unified"
```

---

## IX. TESTING STRATEGY

### Unified Test Suite

```python
# integridai-suite/tests/integration/test_rri_bridge.py

import pytest
from modules.risk_eval.framework_bridge import RiskFrameworkBridge

@pytest.fixture
def bridge():
    return RiskFrameworkBridge()

def test_unified_assessment_usa(bridge):
    """Test USA 2024 assessment matches expected values"""
    result = bridge.get_unified_assessment('USA', 2024)
    
    assert result['country'] == 'USA'
    assert result['year'] == 2024
    assert 0.30 <= result['rri']['index'] <= 0.50  # Expected range
    assert result['coface_equivalent'] in ['A2', 'A3', 'A4']
    
def test_comparison_germany_usa(bridge):
    """Test Germany should have higher RRI than USA"""
    usa = bridge.get_unified_assessment('USA', 2024)
    germany = bridge.get_unified_assessment('Germany', 2024)
    
    assert germany['rri']['index'] > usa['rri']['index']
    assert germany['rri']['friction_score'] > usa['rri']['friction_score']

def test_cache_performance(bridge):
    """Test caching reduces calculation time"""
    import time
    
    start = time.time()
    result1 = bridge.get_unified_assessment('USA', 2024)
    first_call = time.time() - start
    
    start = time.time()
    result2 = bridge.get_unified_assessment('USA', 2024)
    cached_call = time.time() - start
    
    assert cached_call < first_call / 10  # Cache should be 10x faster
    assert result1 == result2  # Results identical
```

---

## X. DEPLOYMENT ARCHITECTURE

### Production Environment

```
┌─────────────────────────────────────────────────────┐
│  AWS / GCP / Azure Cloud                             │
│                                                       │
│  ┌──────────────────────────────────────────────┐   │
│  │  Load Balancer (ALB / Cloud Load Balancer)   │   │
│  └────────────────┬──────────────────────────────┘   │
│                   │                                   │
│         ┌─────────┴──────────┐                       │
│         │                    │                       │
│  ┌──────▼─────┐      ┌──────▼─────┐                 │
│  │  API Node 1 │      │  API Node 2 │                │
│  │  (FastAPI)  │      │  (FastAPI)  │                │
│  │             │      │             │                │
│  │  - Bridge   │      │  - Bridge   │                │
│  │  - RRI Calc │      │  - RRI Calc │                │
│  │  - Cache    │      │  - Cache    │                │
│  └──────┬──────┘      └──────┬──────┘                │
│         │                    │                       │
│         └─────────┬──────────┘                       │
│                   │                                   │
│         ┌─────────▼──────────┐                       │
│         │  Redis Cache        │                       │
│         │  (Shared)           │                       │
│         └─────────┬──────────┘                       │
│                   │                                   │
│         ┌─────────▼──────────┐                       │
│         │  PostgreSQL         │                       │
│         │  (Master + Replica) │                       │
│         │                     │                       │
│         │  - iusmorfos_scores │                       │
│         │  - icrg_data        │                       │
│         │  - coface_ratings   │                       │
│         └─────────────────────┘                       │
│                                                       │
│  ┌──────────────────────────────────────────────┐   │
│  │  S3 / Cloud Storage                           │   │
│  │  - Historical datasets (CSV)                  │   │
│  │  - Generated PDF reports                      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## XI. MIGRATION CHECKLIST

### Phase 1: Submodule Setup (Week 1)

- [ ] Add legal-evolution-unified as git submodule
- [ ] Create `framework_bridge.py` in integridai-suite
- [ ] Write adapter for CSV → PostgreSQL data sync
- [ ] Set up FastAPI endpoints (`/api/v1/rri/*`)
- [ ] Deploy to staging environment
- [ ] Test with 5 pilot countries

### Phase 2: Package Distribution (Weeks 2-4)

- [ ] Extract core logic to `iusmorfos-risk` package
- [ ] Set up PyPI publishing workflow
- [ ] Update both repos to use package
- [ ] Deprecate direct submodule imports
- [ ] Publish v1.0.0 to PyPI
- [ ] Update documentation

### Phase 3: Production Deployment (Weeks 5-8)

- [ ] Set up Redis caching layer
- [ ] Configure PostgreSQL with replication
- [ ] Implement rate limiting (1000 req/min)
- [ ] Set up monitoring (Datadog/New Relic)
- [ ] Load testing (10K concurrent requests)
- [ ] Deploy to production
- [ ] Beta launch with 10 pilot clients

### Phase 4: Monorepo Migration (Months 2-3)

- [ ] Create new `integridad-platform` repo
- [ ] Migrate with git-filter-repo
- [ ] Set up Turborepo/Nx
- [ ] Migrate CI/CD pipelines
- [ ] Update all external references
- [ ] Archive old repos (read-only)

---

## XII. ROLLBACK STRATEGY

### If Integration Fails

**Scenario 1: Submodule issues**
```bash
# Remove submodule
git submodule deinit modules/legal_evolution
git rm modules/legal_evolution
rm -rf .git/modules/legal_evolution

# Revert to direct copy (temporary)
cp -r ../legal-evolution-unified/src modules/risk_eval/legal_evolution_copy
```

**Scenario 2: API breaking changes**
```python
# Use version pinning
# integridai-suite/requirements.txt
iusmorfos-risk==1.0.0  # Pin to working version

# Or use submodule commit pinning
cd modules/legal_evolution
git checkout <working-commit-hash>
```

**Scenario 3: Data sync issues**
```python
# Fall back to CSV adapter
from modules.data.adapters import CSVDataAdapter

adapter = CSVDataAdapter('../legal_evolution/data')
rri_module = RegulatoryRiskModule(adapter)
```

---

## XIII. MAINTENANCE PLAN

### Weekly Tasks
- Sync submodule reference (if using submodule approach)
- Update documentation from legal-evolution changes
- Review API performance metrics

### Monthly Tasks
- Update PyPI package (if using package approach)
- Security audit of dependencies
- Performance optimization review

### Quarterly Tasks
- Major version upgrades
- Database schema migrations
- Architecture review

---

**Document Status**: ✅ Complete  
**Next Action**: Implement Phase 1 (Submodule Setup)  
**Owner**: Integration Team  
**Review Date**: 2025-11-10
