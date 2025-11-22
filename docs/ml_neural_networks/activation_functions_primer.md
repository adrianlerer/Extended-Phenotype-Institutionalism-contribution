# 🧠 Funciones de Activación para Análisis Constitucional

## Introducción

Las funciones de activación son componentes críticos en redes neuronales que introducen **no linealidad**, permitiendo que los modelos aprendan patrones complejos en textos constitucionales.

---

## 🎯 ¿Por qué Neural Networks para Análisis Constitucional?

### Problemas actuales con scoring manual:
1. **Escalabilidad limitada**: Scoring CLI manual requiere 2-3 horas por constitución
2. **Subjetividad**: CE/UA/JPI scoring depende de interpretación humana
3. **No captura matices**: Texto legal tiene sutilezas que fórmulas matemáticas simples no detectan

### Ventajas de Neural Networks:
- ✅ **Auto-scoring CLI** desde texto crudo en segundos
- ✅ **Detecta patrones ocultos** en narrativas constitucionales (CT1)
- ✅ **Predice ultraactivity** antes de que ocurra (patrones históricos)
- ✅ **Escala a 195 países** sin intervención humana

---

## 📊 Funciones de Activación: Conceptos Básicos

### 1. Sigmoide (σ)
```
σ(z) = 1 / (1 + e^(-z))
```

**Rango**: (0, 1)  
**Uso en análisis constitucional**:
- Output final para **CLI score prediction** (debe estar entre 0.0-1.0)
- Clasificación binaria: "¿Es esta cláusula ultraactiva?" (Sí/No)

**Ejemplo**:
```python
# Predecir si una provision expirará según cronología
def predict_expiration_risk(provision_text, years_active):
    z = neural_network_forward(provision_text, years_active)
    probability = sigmoid(z)  # 0.85 = 85% probabilidad de expiración
    return probability
```

**Ventajas**:
- Interpretación probabilística natural
- Smooth gradient (bueno para backpropagation)

**Desventajas**:
- Vanishing gradient problem (cuando z muy grande o pequeño)
- Computational cost (exponencial)

---

### 2. ReLU (Rectified Linear Unit)
```
f(z) = max(0, z)
```

**Rango**: [0, ∞)  
**Uso en análisis constitucional**:
- Hidden layers para **feature extraction** de textos legales
- Detectar presencia/ausencia de características (eternity clauses, supermajority thresholds)

**Ejemplo**:
```python
# Extraer features de constitutional text
def extract_entrenchment_features(text_embeddings):
    h1 = relu(W1 @ text_embeddings + b1)  # Detectar supermajorities
    h2 = relu(W2 @ h1 + b2)                # Detectar referendum requirements
    h3 = relu(W3 @ h2 + b3)                # Detectar eternity clauses
    return h3  # Features relevantes para CE scoring
```

**Ventajas**:
- Computationally efficient (solo comparación)
- No vanishing gradient en región positiva
- Sparse activation (muchas neuronas = 0)

**Desventajas**:
- Dead neurons (si z siempre negativo, gradiente = 0)
- No output negativo (problema si necesitas codificar dirección)

---

### 3. Otras Funciones Avanzadas

#### Leaky ReLU
```
f(z) = max(0.01z, z)
```
**Ventaja**: Evita dead neurons (gradiente pequeño pero no cero cuando z < 0)

#### Tanh (Tangente Hiperbólica)
```
tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))
```
**Rango**: (-1, 1)  
**Uso**: Sentiment analysis de constitutional narratives (positivo/negativo)

#### Softmax (para clasificación multi-clase)
```
softmax(z_i) = e^(z_i) / Σ e^(z_j)
```
**Uso**: Clasificar provisiones en categorías (executive, legislative, judicial, rights)

---

## 🏗️ Arquitectura Neural para CLI Prediction

### Input Layer
- **Constitutional text**: Embeddings BERT (768 dimensiones)
- **Metadata**: Year, country, previous CLI score (if available)

### Hidden Layers (con ReLU)
```python
# Layer 1: Feature extraction
h1 = relu(W1 @ embeddings + b1)  # 768 → 512 neurons

# Layer 2: Pattern detection
h2 = relu(W2 @ h1 + b2)          # 512 → 256 neurons

# Layer 3: Component synthesis
h3 = relu(W3 @ h2 + b3)          # 256 → 128 neurons
```

### Output Layer (con Sigmoid)
```python
# Predecir CLI score (0.0-1.0)
cli_score = sigmoid(W_out @ h3 + b_out)  # 128 → 1 neuron
```

### Loss Function
```python
# Mean Squared Error para regression
loss = (predicted_CLI - true_CLI)^2

# O Binary Cross-Entropy si clasificamos rigidez (high/low)
loss = -[y*log(ŷ) + (1-y)*log(1-ŷ)]
```

---

## 📈 Casos de Uso Específicos

### 1. Auto-Scoring CLI desde Texto
**Problema**: Manual scoring toma 2-3 horas por constitución  
**Solución ML**:
```python
def predict_cli_from_text(constitution_pdf):
    # 1. Extract text
    text = extract_text_from_pdf(constitution_pdf)
    
    # 2. Generate embeddings (LegalBERT)
    embeddings = legal_bert_model.encode(text)
    
    # 3. Neural network inference
    h1 = relu(W1 @ embeddings + b1)
    h2 = relu(W2 @ h1 + b2)
    cli_score = sigmoid(W_out @ h2 + b_out)
    
    return cli_score  # 0.76 (Somalia), 0.54 (Somaliland)
```

**Entrenamiento**:
- Dataset: 100+ constituciones con CLI scores anotados
- Epochs: 50-100
- Validation: 80/20 train/test split

---

### 2. Clasificación de Provisiones Constitucionales
**Problema**: Identificar qué cláusulas contribuyen a CE/UA/JPI  
**Solución ML**:
```python
def classify_provision(clause_text):
    embeddings = legal_bert_model.encode(clause_text)
    
    # Multi-class classification con Softmax
    logits = neural_network_forward(embeddings)
    probabilities = softmax(logits)
    
    # Output: [executive, legislative, judicial, rights, other]
    # Example: [0.05, 0.12, 0.70, 0.08, 0.05]
    return "judicial_constraint"  # 70% probability
```

---

### 3. Detección de Ultraactivity Patterns
**Problema**: Predecir si una provision persistirá beyond expiration  
**Solución ML (LSTM)**:
```python
# Time series prediction
def predict_ultraactivity(provision_history):
    # Input: [year1_status, year2_status, ..., yearN_status]
    # 1 = active, 0 = expired as scheduled
    
    lstm_output = lstm_model(provision_history)
    prob_ultraactive = sigmoid(lstm_output)
    
    return prob_ultraactive  # 0.92 = 92% chance persists beyond expiration
```

---

### 4. Semantic Similarity para CT1 (Narrative Continuity)
**Problema**: Calcular CT1 manualmente via Jaccard similarity es limitado  
**Solución ML**:
```python
def calculate_ct1_neural(constitution_2000, constitution_2012):
    # Embeddings semánticos (capturan significado, no solo palabras)
    emb_2000 = legal_bert_model.encode(constitution_2000)
    emb_2012 = legal_bert_model.encode(constitution_2012)
    
    # Cosine similarity en espacio embedding
    ct1_score = cosine_similarity(emb_2000, emb_2012)
    
    return ct1_score  # 0.40 Somalia, 0.70 Somaliland
```

---

## 🎯 Métricas de Evaluación

### Para Regression (CLI prediction)
- **MSE** (Mean Squared Error): Promedio de (predicted - true)²
- **MAE** (Mean Absolute Error): Promedio de |predicted - true|
- **R²**: Proporción de varianza explicada

### Para Classification (provision categorization)
- **Accuracy**: % de predicciones correctas
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall)

---

## 🚀 Implementación en el Toolkit

### Nuevo API Endpoint: `/api/ml/predict-cli`
```bash
curl -X POST http://localhost:8000/api/ml/predict-cli \
  -H "Content-Type: application/json" \
  -d '{
    "constitution_text": "Article 1. The President...",
    "country": "Somalia",
    "year": 2012
  }'
```

**Response**:
```json
{
  "predicted_CLI": 0.76,
  "confidence": 0.89,
  "components": {
    "CE": 0.80,
    "UA": 0.85,
    "JPI": 0.55
  },
  "model_version": "legal-bert-v1.0",
  "inference_time_ms": 234
}
```

---

## 📚 Referencias

1. **Neural Network Fundamentals**:
   - Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.

2. **Legal AI Applications**:
   - Chalkidis, I., et al. (2020). "LEGAL-BERT: The Muppets straight out of Law School". arXiv:2010.02559.

3. **Constitutional Text Analysis**:
   - Elkins, Z., Ginsburg, T., & Melton, J. (2009). *The Endurance of National Constitutions*. Cambridge.

4. **Activation Functions**:
   - Nwankpa, C., et al. (2018). "Activation Functions: Comparison of trends in Practice and Research for Deep Learning". arXiv:1811.03378.

---

## 🔧 Próximos Pasos

1. ✅ **Entender funciones de activación** (este documento)
2. ⏳ **Implementar dataset de entrenamiento** (100+ constituciones anotadas)
3. ⏳ **Desarrollar modelo base** (LegalBERT + CLI prediction head)
4. ⏳ **Integrar en API** (FastAPI endpoint con inferencia PyTorch)
5. ⏳ **Evaluar performance** (comparar vs manual scoring)

---

**Status**: 📝 Documentation Complete  
**Next**: Start implementing training dataset  
**Version**: 1.0.0  
**Last Updated**: 2025-11-22
