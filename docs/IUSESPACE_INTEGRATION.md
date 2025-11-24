# 🌐 IusSpace Integration: 12 Dimensiones + Neural Networks + JurisRank

## Executive Summary

Este documento integra **tres frameworks teóricos** en un toolkit unificado:

1. **IusSpace (12 dimensiones)**: Framework para mapear sistemas legales en espacio continuo
2. **JurisRank**: Algoritmo para medir fitness evolutivo via redes de citación
3. **Neural Networks**: ML para análisis del ecosistema legal completo (no solo constituciones)

---

## 📊 Las 12 Dimensiones del IusSpace

Según tu paper (SSRN 5557838), IusSpace mapea sistemas legales en 12 dimensiones:

### **Dimensión 1: Constitutional Entrenchment (CE)**
```python
# Ya implementado: CLI Calculator
ce_score = calculate_ce(
    amendment_threshold,      # 0.0-1.0
    eternity_clauses,         # boolean
    referendum_requirement    # boolean
)
```

### **Dimensión 2: Ultraactivity (UA)**
```python
# Ya implementado: CLI Calculator
ua_score = calculate_ua(
    term_extensions,          # years beyond intended
    provisional_persistence,  # years as "transitional"
    formula_persistence       # years beyond expiration
)
```

### **Dimensión 3: Judicial Protection Intensity (JPI)**
```python
# Ya implementado: CLI Calculator
jpi_score = calculate_jpi(
    constitutional_court_exists,  # 0.0-0.3
    judicial_independence,        # 0.0-0.4
    active_review_cases          # 0.0-0.3
)
```

### **Dimensión 4: Cultural Lock-In (CLI_cultural)**
```python
# Ya implementado: CLI Cultural Calculator
cli_cultural = calculate_cultural_lockin(
    narrative_continuity,     # CT1: 0.0-1.0
    shock_resistance,         # CT2: 0.0-1.0
    policy_sustainability     # CT3: 0.0-1.0
)
```

### **Dimensión 5: Implementation Gap**
```python
# NUEVO - Necesita implementación
implementation_gap = measure_gap(
    formal_passage_date,
    actual_implementation_date,
    compliance_rate
)
# Output: 0.0 (perfect) to 1.0 (complete failure)
# Paper muestra: WEIRD 5.4%, Non-WEIRD 31.2%
```

### **Dimensión 6: Legal Norm Fitness (JurisRank)**
```python
# Ya implementado: tools/jurisrank/jurisrank.py
fitness_scores = jurisrank.calculate_jurisrank(
    citation_matrix,         # N×N matrix
    case_metadata,           # dates, court levels
    temporal_decay=0.05,     # annual decay rate
    hierarchical_weights=True
)
# Output: PageRank-style scores for cada norma
```

### **Dimensión 7: Network Topology (Graph Density)**
```python
# Parcialmente implementado en docs/ml_neural_networks/iusespacio_network_analysis.md
# Necesita implementación completa
graph_density = calculate_density(
    legal_network           # Graph of norms + citations
)
# Somalia: 0.12 (LOW - fragmentado)
# Somalilandia: 0.68 (HIGH - cohesivo)
```

### **Dimensión 8: Constitutional Centrality**
```python
# NUEVO - Necesita implementación usando NetworkX
centrality = calculate_betweenness_centrality(
    legal_network,
    target_node='constitution'
)
# ¿Qué tan central es la constitución en la red normativa?
# Somalia: 0.35 (periférica)
# Somalilandia: 0.85 (hub central)
```

### **Dimensión 9: Reform Velocity**
```python
# NUEVO - Del paper IusSpace
reform_velocity = measure_velocity(
    start_point,            # Estado legal inicial en IusSpace
    end_point,              # Estado legal final
    time_elapsed            # años
)
# Output: Distancia euclidiana / tiempo
# Pre-digital: 45 años promedio
# Digital era: 3.2 años promedio (aceleración 14x)
```

### **Dimensión 10: Crisis Catalysis Factor**
```python
# NUEVO - Del paper JurisRank
crisis_factor = detect_crisis_catalysis(
    reform_timeline,
    major_crises            # economic, political, social
)
# Output: 0.0-1.0 indicating crisis-driven vs normal-time reform
# Crisis reforms: 78% adoption rate
# Normal-time: 23% adoption rate
```

### **Dimensión 11: WEIRD/Non-WEIRD Classification**
```python
# NUEVO - Del paper IusSpace
weird_score = classify_weird(
    country,
    western=bool,
    educated=float,          # education index
    industrialized=float,    # GDP per capita
    rich=float,              # wealth index
    democratic=float         # polity score
)
# Threshold: 0.5 → Non-WEIRD (85% población mundial)
# Predicts implementation gap con p < 0.0001
```

### **Dimensión 12: Temporal Transplantation Era**
```python
# NUEVO - Del paper JurisRank
transplant_era = classify_era(
    reform_year
)
# Output:
# - "pre-digital" (1679-1945): Convergent evolution
# - "transitional" (1945-1990): Catalytic influence
# - "digital" (1990-present): Accelerated transplantation
```

---

## 🔗 Integración: IusSpace + JurisRank + Neural Networks

### **Framework Unificado**

```python
class IusSpaceAnalyzer:
    """
    Analiza sistemas legales en espacio 12-dimensional.
    Integra CLI, JurisRank, Neural Networks y Graph Analysis.
    """
    
    def __init__(self):
        # Módulos existentes
        self.cli_calculator = CLICalculator()
        self.jurisrank = JurisRank()
        self.neural_predictor = CLINeuralPredictor()
        self.graph_analyzer = LegalGraphNet()
        
        # Nuevos módulos
        self.implementation_gap_detector = ImplementationGapDetector()
        self.reform_velocity_calculator = ReformVelocityCalculator()
        self.weird_classifier = WEIRDClassifier()
    
    def map_to_iusspace(
        self, 
        country: str,
        constitution_text: str,
        legal_corpus: List[str],
        reform_history: List[Dict]
    ) -> np.ndarray:
        """
        Mapea un sistema legal al espacio 12-dimensional.
        
        Returns:
            np.ndarray: Vector de 12 dimensiones
            [CE, UA, JPI, CLI_cultural, Impl_Gap, JurisRank_avg,
             Graph_Density, Centrality, Reform_Velocity, Crisis_Factor,
             WEIRD_score, Transplant_Era]
        """
        
        # Dimensiones 1-4: CLI components (ya implementadas)
        cli_components = self.cli_calculator.calculate(constitution_text)
        
        # Dimensión 5: Implementation Gap (NUEVO)
        impl_gap = self.implementation_gap_detector.measure(
            formal_laws=legal_corpus,
            actual_compliance=get_compliance_data(country)
        )
        
        # Dimensión 6: JurisRank (ya implementado)
        citation_network = build_citation_network(legal_corpus)
        jurisrank_scores = self.jurisrank.calculate_jurisrank(
            citation_network['matrix'],
            citation_network['metadata']
        )
        avg_fitness = np.mean(list(jurisrank_scores.values()))
        
        # Dimensión 7-8: Network Topology (parcialmente implementado)
        legal_graph = build_legal_graph(legal_corpus)
        graph_density = nx.density(legal_graph)
        constitution_centrality = nx.betweenness_centrality(legal_graph)['constitution']
        
        # Dimensión 9: Reform Velocity (NUEVO)
        reform_velocity = self.reform_velocity_calculator.calculate(
            reform_history
        )
        
        # Dimensión 10: Crisis Catalysis (NUEVO)
        crisis_factor = detect_crisis_reforms(reform_history)
        
        # Dimensión 11: WEIRD Classification (NUEVO)
        weird_score = self.weird_classifier.classify(country)
        
        # Dimensión 12: Transplantation Era (NUEVO)
        current_year = datetime.now().year
        transplant_era = classify_transplantation_era(current_year)
        
        # Vector 12-dimensional
        iusspace_vector = np.array([
            cli_components['CE'],           # D1
            cli_components['UA'],           # D2
            cli_components['JPI'],          # D3
            cli_components['CLI_cultural'], # D4
            impl_gap,                       # D5
            avg_fitness,                    # D6
            graph_density,                  # D7
            constitution_centrality,        # D8
            reform_velocity,                # D9
            crisis_factor,                  # D10
            weird_score,                    # D11
            transplant_era                  # D12
        ])
        
        return iusspace_vector
    
    def calculate_euclidean_distance(
        self,
        vector_a: np.ndarray,
        vector_b: np.ndarray
    ) -> float:
        """
        Distancia euclidiana en IusSpace.
        Predice dificultad de reforma (paper IusSpace).
        """
        return np.linalg.norm(vector_a - vector_b)
    
    def predict_implementation_success(
        self,
        start_vector: np.ndarray,
        target_vector: np.ndarray,
        weird_status: float
    ) -> Dict:
        """
        Predice éxito de reforma basado en geometría IusSpace.
        
        Del paper IusSpace: 87.4% accuracy.
        """
        distance = self.calculate_euclidean_distance(start_vector, target_vector)
        
        # Ajuste por WEIRD/Non-WEIRD
        if weird_status < 0.5:  # Non-WEIRD
            base_gap = 0.312  # 31.2% implementation gap
        else:  # WEIRD
            base_gap = 0.054  # 5.4% implementation gap
        
        # Distancia afecta probabilidad
        distance_penalty = distance * 0.15  # 15% penalty per unit distance
        
        predicted_success_rate = 1.0 - base_gap - distance_penalty
        
        return {
            'predicted_success': max(0.0, min(1.0, predicted_success_rate)),
            'euclidean_distance': distance,
            'weird_adjusted_gap': base_gap,
            'distance_penalty': distance_penalty
        }
```

---

## 🧠 Neural Networks Amplificados

### **Antes (limitado)**:
```python
# Solo predecíamos CLI desde constitución
cli = neural_predictor.predict_cli_from_text(constitution_text)
```

### **Ahora (IusSpace completo)**:
```python
# Predecimos VECTOR 12-dimensional desde corpus completo
iusspace_vector = neural_predictor.predict_iusspace_vector(
    constitution_text,
    statutes,
    court_rulings,
    customary_law,
    reform_history
)

# Output: [CE, UA, JPI, CLI_cultural, Impl_Gap, JurisRank_avg,
#          Graph_Density, Centrality, Reform_Velocity, Crisis_Factor,
#          WEIRD_score, Transplant_Era]
```

### **Arquitectura Neural para IusSpace**:

```python
class IusSpaceNeuralPredictor(nn.Module):
    """
    Neural network que predice posición en IusSpace 12-dimensional.
    """
    
    def __init__(self):
        super().__init__()
        
        # Separate encoders para cada tipo de documento
        self.constitution_encoder = LegalBERT()
        self.statute_encoder = LegalBERT()
        self.case_encoder = LegalBERT()
        
        # Fusion layer
        self.fusion = nn.Linear(768 * 3, 512)
        
        # Hidden layers (ReLU activations)
        self.hidden1 = nn.Linear(512, 256)
        self.hidden2 = nn.Linear(256, 128)
        
        # Output: 12 dimensions
        self.output = nn.Linear(128, 12)
    
    def forward(
        self,
        constitution_embeddings,
        statute_embeddings,
        case_embeddings
    ):
        # Concatenate all embeddings
        fused = torch.cat([
            constitution_embeddings,
            statute_embeddings,
            case_embeddings
        ], dim=1)
        
        # Fusion
        x = torch.relu(self.fusion(fused))
        
        # Hidden layers
        x = torch.relu(self.hidden1(x))
        x = torch.relu(self.hidden2(x))
        
        # Output (12 dimensions)
        # Each dimension 0.0-1.0 via sigmoid
        iusspace_vector = torch.sigmoid(self.output(x))
        
        return iusspace_vector
```

---

## 🔧 Herramientas a Implementar (Prioritizadas)

### **Tier 1: Critical (implementar YA)**

#### 1. **Implementation Gap Detector** ⚠️
```python
# Mide diferencia entre ley formal y cumplimiento real
# Paper IusSpace: WEIRD 5.4%, Non-WEIRD 31.2%

class ImplementationGapDetector:
    def measure_gap(
        self,
        law_text: str,
        compliance_data: Dict,
        enforcement_records: List
    ) -> float:
        """
        Output: 0.0 (perfect implementation) to 1.0 (zero implementation)
        """
        # Parse mandatory provisions from law
        provisions = extract_mandatory_provisions(law_text)
        
        # Check compliance for each
        compliance_scores = []
        for provision in provisions:
            score = check_provision_compliance(
                provision,
                compliance_data,
                enforcement_records
            )
            compliance_scores.append(score)
        
        # Gap = 1 - average compliance
        return 1.0 - np.mean(compliance_scores)
```

**Use Cases**:
- **Policy Makers**: "Esta ley tiene 68% implementation gap, rediseñar enforcement"
- **Investment**: "Argentina tiene 45% gap en labor law, riesgo laboral alto"
- **Academia**: "Non-WEIRD societies show 31.2% gap vs 5.4% WEIRD (p<0.0001)"

---

#### 2. **WEIRD Classifier** 🌍
```python
# Clasifica país como WEIRD vs Non-WEIRD
# Critical porque predice implementation gap (r=0.87)

class WEIRDClassifier:
    def classify(self, country: str) -> float:
        """
        Returns: 0.0 (pure Non-WEIRD) to 1.0 (pure WEIRD)
        """
        components = {
            'western': self._is_western(country),              # 0.0-1.0
            'educated': self._education_index(country),        # 0.0-1.0
            'industrialized': self._gdp_per_capita(country),   # 0.0-1.0
            'rich': self._wealth_index(country),               # 0.0-1.0
            'democratic': self._polity_score(country)          # 0.0-1.0
        }
        
        # Equal weights (could be optimized)
        weird_score = np.mean(list(components.values()))
        
        return weird_score
```

**Use Cases**:
- **World Bank**: "Target country is Non-WEIRD (0.32), expect 31% implementation gap"
- **UN**: "Design bottom-up processes for Non-WEIRD contexts (85% of world)"
- **Research**: "Control for WEIRD bias in comparative studies"

---

#### 3. **Reform Velocity Calculator** 🚀
```python
# Del paper IusSpace + JurisRank
# Pre-digital: 45 years, Digital: 3.2 years (aceleración 14x)

class ReformVelocityCalculator:
    def calculate(
        self,
        reform_history: List[Dict]
    ) -> float:
        """
        Returns: Reforms per year (velocity in IusSpace)
        """
        # Extract reforms with before/after vectors
        velocities = []
        
        for reform in reform_history:
            start_vector = reform['before_iusspace']
            end_vector = reform['after_iusspace']
            years = reform['years_elapsed']
            
            # Euclidean distance in IusSpace
            distance = np.linalg.norm(end_vector - start_vector)
            
            # Velocity = distance / time
            velocity = distance / years if years > 0 else 0
            velocities.append(velocity)
        
        return np.mean(velocities)
```

**Use Cases**:
- **Policy**: "This reform moves 0.3 units in IusSpace, expect 5-year implementation"
- **Research**: "Digital era shows 14x acceleration in legal transplantation"
- **Journalism**: "Country X reformed 8x faster than regional average"

---

### **Tier 2: Important (implementar después)**

#### 4. **Crisis Catalysis Detector**
- Detecta si reforma fue crisis-driven (78% success) vs normal-time (23% success)
- Del paper JurisRank: crisis = political economy mechanism

#### 5. **IusSpace Distance Calculator**
- Calcula distancia euclidiana entre dos países en IusSpace
- Predice feasibility de transplantation

#### 6. **Network Centrality Analyzer**
- Ya parcialmente en `iusespacio_network_analysis.md`
- Needs complete NetworkX integration

---

### **Tier 3: Nice-to-have (roadmap)**

#### 7. **Transplantation Era Classifier**
- Categoriza reforma en pre-digital / transitional / digital
- Automático basado en fecha

#### 8. **"Se Acata Pero No Se Cumple" Detector**
- Detecta patrón latinoamericano de formal compliance + practical evasion
- Paper IusSpace: es el patrón GLOBAL dominante (85% población)

#### 9. **Convergent vs Transplanted Evolution**
- Distingue si norma evolucionó independently vs fue transplanted
- Del paper JurisRank: pre-1945 convergent, post-1990 transplanted

---

## 🎯 Roadmap de Implementación

### **Fase 1: Completar IusSpace Core** (2-3 semanas)
```
✅ CLI Calculator (D1-D3) - YA EXISTE
✅ CLI Cultural (D4) - YA EXISTE
✅ JurisRank (D6) - YA EXISTE
🚧 Implementation Gap (D5) - IMPLEMENTAR
🚧 Network Topology (D7-D8) - COMPLETAR
🚧 Reform Velocity (D9) - IMPLEMENTAR
🚧 Crisis Catalysis (D10) - IMPLEMENTAR
🚧 WEIRD Classifier (D11) - IMPLEMENTAR
✅ Transplant Era (D12) - TRIVIAL (solo fecha)
```

### **Fase 2: Neural Networks para IusSpace** (3-4 semanas)
```
🚧 IusSpaceNeuralPredictor - Predice vector 12D desde corpus
🚧 Multi-encoder architecture - Constitution + Statutes + Cases
🚧 Training dataset - 50+ países con vectores IusSpace anotados
🚧 Validation - r > 0.80 con manual scoring
```

### **Fase 3: API Integration** (1-2 semanas)
```
🚧 POST /api/iusspace/map - Mapea país a 12D space
🚧 POST /api/iusspace/distance - Calcula distancia entre países
🚧 POST /api/iusspace/predict-reform - Predice success de reforma
🚧 POST /api/iusspace/weird-classify - Clasifica WEIRD vs Non-WEIRD
```

### **Fase 4: Visualization** (2 semanas)
```
🚧 3D IusSpace viewer (plotly) - Visualiza países en espacio 12D
🚧 Reform trajectory visualizer - Muestra path de reforma
🚧 WEIRD/Non-WEIRD clusters - Muestra segregación espacial
```

---

## 📚 Papers Integration Summary

### **IusSpace Paper (SSRN 5557838)**
- **Contribución**: Framework 12-dimensional para mapear sistemas legales
- **Hallazgo clave**: Non-WEIRD 31.2% gap vs WEIRD 5.4% gap (d=3.749, p<0.0001)
- **Ya implementado**: D1-D4, D6 (parcial)
- **Falta implementar**: D5, D7-D12

### **JurisRank Paper (SSRN 5405459)**
- **Contribución**: Algoritmo para medir fitness evolutivo via citations
- **Hallazgo clave**: Pre-digital 45 años → Digital 3.2 años (14x aceleración)
- **Ya implementado**: `tools/jurisrank/jurisrank.py` ✅ COMPLETO
- **Mejoras posibles**: Cross-jurisdictional adoption tracking

### **EPT Framework** (papers múltiples)
- **Contribución**: Teoría evolutiva de instituciones legales
- **Componentes**: CLI, CLI_cultural, Extended Phenotype
- **Ya implementado**: CLI calculators, Neural predictor
- **Falta implementar**: Network analysis completo (iusespacio)

---

## 🚀 Next Steps

### **Prioridad 1**: Implementar dimensiones faltantes
1. Implementation Gap Detector (D5)
2. WEIRD Classifier (D11)
3. Reform Velocity Calculator (D9)

### **Prioridad 2**: Integrar con Neural Networks
1. IusSpaceNeuralPredictor (12D output)
2. Training dataset (50+ países)
3. Validation contra IusSpace paper results

### **Prioridad 3**: API + Visualization
1. API endpoints completos
2. 3D IusSpace viewer
3. Documentation + examples

---

## 💡 Conclusión

**Tenemos**:
- ✅ JurisRank implementado (citation fitness)
- ✅ CLI calculators (D1-D4)
- ✅ Neural predictor base (LegalBERT)
- ✅ Teoría completa (3 papers)

**Necesitamos**:
- 🚧 Implementar D5, D7-D12 (dimensiones faltantes)
- 🚧 Neural network 12D (no solo CLI)
- 🚧 API integration + visualization

**Con esto tendremos**:
- 🎯 Toolkit COMPLETO para análisis del iusespacio
- 🎯 No solo constituciones, sino ecosistema legal completo
- 🎯 Predicción de reforms con 87.4% accuracy (paper IusSpace)
- 🎯 Framework unificado: EPT + JurisRank + IusSpace + Neural Networks

¿Empezamos con Implementation Gap Detector (D5)? Es crítico porque diferencia WEIRD vs Non-WEIRD.
