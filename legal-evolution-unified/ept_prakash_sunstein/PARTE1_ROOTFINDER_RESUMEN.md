# PARTE 1: RootFinder - Análisis de Extinción del Memeplex "Wechsler Critique"

## 📋 Resumen Ejecutivo

**Objetivo**: Cuantificar la extinción del argumento de Herbert Wechsler (1959) que defendía que la integración racial forzada violaba la "freedom of association" de los blancos.

**Estado**: ⏳ **LISTO PARA IMPLEMENTAR**

**Predicción Teórica**:
- Extinction rate > 95% (similar a 19th Amendment analysis: 93.3%)
- Half-life < 10 años
- Functional extinction year ≈ 1988

---

## 🎯 Contexto Teórico: El Caso Wechsler

### La Crítica Original (1959)

Herbert Wechsler, en su influyente artículo "Toward Neutral Principles of Constitutional Law" (1959), argumentó que **Brown v. Board of Education** (1954) no podía justificarse bajo "neutral principles" porque:

> La integración forzada viola la **freedom of association** de aquellos que prefieren no asociarse con personas de otras razas.

**Razonamiento**:
- Derecho constitucional de asociarse libremente (First Amendment)
- Si negros tienen derecho a integración, blancos tienen derecho simétrico a NO asociarse
- Brown impone una preferencia (integración) sobre otra (segregación) sin principio neutral

### Por qué es Relevante para P&S

Prakash & Sunstein describen cómo este argumento es hoy **"unthinkable"** (impensable):

| Período | Status del Argumento |
|---------|---------------------|
| **1959-1965** | Mainstream (artículo de Wechsler citado ampliamente) |
| **1965-1975** | Extreme (solo conservadores lo sostienen) |
| **1975-1990** | Outlandish (marginado incluso en círculos conservadores) |
| **1990-presente** | **Unthinkable** (citar con aprobación = suicidio académico/judicial) |

**Pregunta de Investigación**: ¿Podemos **cuantificar** esta extinción usando citation networks y semantic analysis?

---

## 🔬 Metodología RootFinder

### Algoritmo Propuesto

```python
class RootFinder:
    """
    Traces genealogical extinction of legal memeplexes
    """
    def __init__(self, citation_network, time_range):
        self.network = citation_network  # Case citations
        self.time_range = time_range      # 1959-2025
        
    def calculate_extinction_rate(self, memeplex_id, measurement_window):
        """
        Extinction Rate = 1 - (citations_final_period / citations_initial_period)
        
        Adjusts for overall citation inflation using control group
        """
        peak_citations = self.get_peak_citations(memeplex_id)
        current_citations = self.get_recent_citations(memeplex_id, window=10)
        
        # Normalize by general law review citation inflation
        inflation_factor = self.calculate_citation_inflation()
        
        adjusted_current = current_citations / inflation_factor
        extinction_rate = 1 - (adjusted_current / peak_citations)
        
        return extinction_rate
    
    def compute_half_life(self, memeplex_id):
        """
        Time required for citation frequency to decay to 50% of peak
        
        Model: N(t) = N₀ * e^(-λt)
        Half-life = ln(2) / λ
        """
        citation_series = self.get_citation_time_series(memeplex_id)
        
        # Fit exponential decay model
        from scipy.optimize import curve_fit
        
        def exponential_decay(t, N0, lambda_):
            return N0 * np.exp(-lambda_ * t)
        
        params, _ = curve_fit(exponential_decay, 
                              citation_series['year'], 
                              citation_series['citations'])
        
        N0, lambda_ = params
        half_life = np.log(2) / lambda_
        
        return half_life
    
    def trace_genealogy(self, memeplex_id):
        """
        Build citation tree showing:
        - Direct descendants (cases citing Wechsler)
        - Semantic mutations (cases modifying argument)
        - Extinction events (last citation clusters)
        """
        G = nx.DiGraph()
        
        # Start with root node (Wechsler 1959)
        root = "Wechsler_1959"
        G.add_node(root, year=1959, citations=0)
        
        # Add all cases citing Wechsler
        citing_cases = self.get_citing_cases(root)
        
        for case in citing_cases:
            G.add_node(case['id'], 
                      year=case['year'],
                      context=case['context'],  # Equal Protection vs Other
                      semantic_valence=case['valence'])  # Positive, Neutral, Critical
            
            G.add_edge(root, case['id'])
        
        # Build multi-generational tree (cases citing Wechsler-citers)
        for case in citing_cases:
            second_gen = self.get_citing_cases(case['id'])
            for child in second_gen:
                G.add_node(child['id'], year=child['year'])
                G.add_edge(case['id'], child['id'])
        
        return G
    
    def plot_extinction_curve(self):
        """
        Visualization: Citation frequency over time
        Include: 
        - Point estimates (annual citations)
        - Confidence intervals (bootstrap)
        - Inflection points (identified algorithmically)
        - Extinction threshold (< 1 per decade)
        """
        pass
```

---

## 📊 Datos Requeridos

### 1. Citation Network

**Source**: Westlaw, LexisNexis, Google Scholar Case Law

**Query**:
```
"Toward Neutral Principles" OR "Herbert Wechsler" 
AND (
    "Brown v. Board" OR "equal protection" OR 
    "freedom of association" OR "associational rights"
)
```

**Extraction**:
- Case name, year, court
- Citation context (±200 words around mention)
- Subsequent citations (who cites the case that cited Wechsler)

**Expected Size**: ~500-1000 cases (1959-2025)

### 2. Semantic Classification

Para cada citación, clasificar:

#### A) **Context**:
- **Equal Protection** (direct relevance to Brown/integration)
- **Other** (unrelated constitutional areas)

#### B) **Valence** (stance toward Wechsler):
- **Positive**: "Wechsler correctly argues..."
- **Neutral**: "As Wechsler noted..." (descriptive)
- **Critical**: "Wechsler's flawed argument..."

#### C) **Function**:
- **Substantive**: Using argument in reasoning
- **Historical**: Citing as historical artifact
- **Dismissive**: Mentioning to reject

**Hypothesis**: Shift over time from **Positive/Substantive** → **Historical/Dismissive**

### 3. Control Group

**Purpose**: Normalize for general citation inflation (older articles get less cited regardless of content)

**Sample**: 10-15 contemporary law review articles (1959-1965) on constitutional law

**Metric**: Average citation decay rate for non-extinct ideas

---

## 📈 Outputs Esperados

### 1. Extinction Metrics

```python
{
    "memeplex_id": "wechsler_freedom_association_critique",
    "peak_year": 1965,
    "peak_citations": 23,
    "current_citations_per_decade": 0.4,
    "extinction_rate": 0.957,  # 95.7% decline
    "extinction_rate_ci": [0.932, 0.978],  # Bootstrap CI 95%
    "half_life_years": 8.3,
    "half_life_ci": [6.7, 10.1],
    "functional_extinction_year": 1988,
    "p_value_trend": 0.0001,  # Mann-Kendall test
    "classification": "extinct"
}
```

### 2. Visualizaciones

#### A) **Extinction Curve**
- **X-axis**: Year (1959-2025)
- **Y-axis**: Citations per year
- **Elements**:
  - Point estimates (blue dots)
  - Exponential decay fit (red line)
  - Confidence interval band (shaded gray)
  - Inflection points (marked with vertical lines)
  - Extinction threshold (horizontal dashed line at 1 per decade)

#### B) **Genealogical Tree**
- **Format**: Network diagram
- **Nodes**: Cases (sized by importance)
- **Edges**: Citations (thickness = frequency)
- **Colors**: 
  - Green = Positive valence
  - Yellow = Neutral
  - Red = Critical
- **Layout**: Time-based (left to right 1959 → 2025)

#### C) **Semantic Heatmap**
- **Rows**: Time periods (5-year bins)
- **Columns**: Context categories (Equal Protection, Other)
- **Cell color**: Citation frequency
- **Overlay**: Valence breakdown (stacked bars)

### 3. Statistical Validation

```python
# Mann-Kendall trend test
{
    "statistic": -4.82,
    "p_value": 0.0001,
    "tau": -0.67,
    "interpretation": "Highly significant downward trend"
}

# Comparison to control group
{
    "wechsler_decay_rate": -0.12,  # per year
    "control_avg_decay_rate": -0.03,  # general citation decay
    "difference": -0.09,
    "p_value_diff": 0.002,
    "interpretation": "Wechsler decays 3x faster than control"
}

# Bootstrap validation
{
    "n_iterations": 10000,
    "extinction_rate_mean": 0.957,
    "extinction_rate_std": 0.012,
    "ci_95": [0.932, 0.978],
    "robust": True
}
```

---

## 🎯 Hipótesis a Validar

### H1: Extinction Rate > 95%
**Rationale**: Idea pasó de mainstream (1960s) a unthinkable (present)

**Test**: Compare peak citations (1965) vs recent (2015-2025)

**Expected**: Extinction rate ≈ 95-98%

### H2: Half-Life < 10 Years
**Rationale**: Rapid paradigm shift post-Civil Rights Act (1964) + Voting Rights Act (1965)

**Test**: Exponential decay model fit

**Expected**: Half-life ≈ 8-9 years

### H3: Functional Extinction by 1990
**Rationale**: By 1990, citing Wechsler positively in Equal Protection context = career suicide

**Test**: Identify last year with >1 citation per year in Equal Protection context

**Expected**: Functional extinction ≈ 1988-1992

### H4: Valence Shift (Positive → Critical)
**Rationale**: Even when cited, tone changed from endorsement to critique

**Test**: Chi-square test of valence distribution across time periods

**Expected**: 
- 1960s: 60% positive, 30% neutral, 10% critical
- 1990s-present: 5% positive, 20% neutral, 75% critical

### H5: Context Shift (Equal Protection → Other)
**Rationale**: Argument evacuated from its original domain, relegated to historical footnotes

**Test**: Proportion of citations in Equal Protection context over time

**Expected**:
- 1960s: 80% Equal Protection
- 2000s: 20% Equal Protection

---

## 📁 Deliverables

### 1. Python Script
**File**: `ept_prakash_sunstein/rootfinder/rootfinder_wechsler.py`

**Dependencies**:
```python
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
from scipy.stats import mannkendall
from sklearn.utils import resample
```

**Key Functions**:
- `load_citation_data(file_path)`: Import CSV with case citations
- `calculate_extinction_rate(citation_series)`: Core metric
- `compute_half_life(citation_series)`: Exponential decay fit
- `build_genealogical_tree(citation_network)`: NetworkX graph
- `plot_extinction_curve(citation_series)`: Matplotlib visualization
- `run_statistical_tests(citation_series)`: Mann-Kendall, bootstrap
- `generate_report(results)`: Markdown output

### 2. Visualization Files
- `wechsler_extinction_curve.png` (300 DPI)
- `wechsler_genealogical_tree.png` (vector SVG + PNG)
- `wechsler_semantic_heatmap.png` (300 DPI)

### 3. Data Files
- `wechsler_citations_1959_2025.csv`: Raw citation data
- `wechsler_extinction_metrics.json`: Computed results
- `wechsler_statistical_validation.csv`: Bootstrap samples

### 4. Analysis Report
**File**: `ept_prakash_sunstein/reports/extinction_analysis_wechsler.md`

**Structure** (2-3 pages):
1. **Introduction**: Context and research question
2. **Methodology**: RootFinder algorithm summary
3. **Results**: 
   - Extinction metrics
   - Statistical tests
   - Visualization interpretation
4. **Comparison**: 19th Amendment analysis (93.3% extinction)
5. **Conclusions**: Validation of P&S "unthinkable" concept

---

## 🔧 Implementación: Opciones

### Opción A: **Synthetic Data** (Rápida, para proof-of-concept)
**Pros**:
- Implemento algoritmo completo ahora (2-3 horas)
- Visualizaciones listas inmediatamente
- Valida arquitectura de código

**Cons**:
- No publica-ready (necesita datos reales después)
- Patrones inventados (aunque basados en hipótesis teóricas)

**Timeline**: Hoy mismo

### Opción B: **Web Scraping Real** (Lenta, publication-ready)
**Pros**:
- Datos reales de Westlaw/LexisNexis/Google Scholar
- Resultados publicables en paper
- Validación empírica genuina

**Cons**:
- Requiere API access o manual scraping (2-3 días mínimo)
- Westlaw/LexisNexis = paywalls
- Google Scholar Case Law = rate limits

**Timeline**: 3-5 días

### Opción C: **Híbrida** (Recomendada)
**Fase 1**: Synthetic data + algoritmo completo (hoy)
**Fase 2**: Replace con real data cuando esté disponible (próxima semana)

**Pros**:
- Progreso inmediato en arquitectura
- Framework listo para recibir datos reales
- Código reutilizable para otros memeplexes

**Cons**:
- Trabajo duplicado (run twice)

---

## 🚀 Próximos Pasos (Opción C Recomendada)

### Paso 1: Implementar con Synthetic Data (HOY)
```python
# Generate synthetic citation time series
years = np.arange(1959, 2026)
peak_year = 1965
peak_citations = 23
decay_rate = 0.15  # 15% annual decline

citations = []
for year in years:
    if year <= peak_year:
        # Growth phase (1959-1965)
        cites = int(23 * ((year - 1959) / 6))
    else:
        # Decay phase (1965-2025)
        time_since_peak = year - peak_year
        cites = int(peak_citations * np.exp(-decay_rate * time_since_peak))
        # Add noise
        cites = max(0, cites + np.random.randint(-2, 3))
    
    citations.append({'year': year, 'citations': cites})

synthetic_data = pd.DataFrame(citations)
```

### Paso 2: Run RootFinder Algorithm
- Calculate extinction rate
- Fit exponential decay
- Generate visualizations
- Run statistical tests

### Paso 3: Validate Against Expected Results
- Extinction rate ≈ 95%? ✓
- Half-life ≈ 8 years? ✓
- Functional extinction ≈ 1988? ✓

### Paso 4: Generate Report
- Markdown file with results
- Interpretation in context of P&S theory
- Comparison to 19th Amendment case

### Paso 5: Commit to Git
- All code, data, visualizations, report
- Ready for PARTE 2 (IusMorfos)

---

## ❓ Pregunta para Vos

**¿Arranco con implementación usando synthetic data (Opción C)?**

**Pros**:
- Tenés algoritmo funcionando hoy
- Visualizaciones listas para mostrar concepto
- Framework preparado para datos reales

**Timeline**:
- 2-3 horas para implementación completa
- 1 commit con todo el módulo RootFinder

**O preferís que primero busque datos reales** (va a tomar 3-5 días de scraping)?

---

**Status**: ⏳ **ESPERANDO TU CONFIRMACIÓN PARA PROCEDER**
