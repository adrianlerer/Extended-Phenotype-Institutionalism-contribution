# MiniMax API Key Setup Guide
## Guía Paso a Paso para Obtener y Configurar tu API Key

**Tiempo estimado:** 5 minutos  
**Costo:** ✅ **GRATIS temporalmente** (según README oficial)  
**Propósito:** Habilitar validación automatizada de papers con MiniMax-M2

---

## 📋 Pasos para Obtener la API Key

### 1. Acceder a la Plataforma MiniMax

**URL:** https://platform.minimax.io/

**Opciones de acceso:**
- Crear nueva cuenta (email + password)
- Login con cuenta existente
- Puede requerir verificación de email

### 2. Obtener tu GroupID

El GroupID es un identificador de 19 dígitos necesario para vincular tu API key a tu cuenta.

**Pasos:**
1. Una vez logueado, ir al menú izquierdo
2. Click en **"Account"** → **"Your Profile"**
3. Encontrarás el campo **"GroupID"** (número de 19 dígitos)
4. Click en el ícono de **copiar** para copiarlo al portapapeles
5. Guardarlo temporalmente (lo necesitarás para facturación/uso)

**Ejemplo:** `1234567890123456789`

### 3. Generar API Key

**Pasos:**
1. En el menú izquierdo, click en **"API Keys"**
2. Click en **"Create New Secret Key"**
3. Ingresar un **nombre descriptivo** para la key (ej: "IusMorfos-Research")
4. Click en **"Create"**
5. ⚠️ **CRÍTICO:** Cuando aparezca el diálogo con la key:
   - **Copiar la API key INMEDIATAMENTE** (click en ícono de copiar)
   - **NO SERÁ MOSTRADA NUEVAMENTE**
   - Si la pierdes, deberás generar una nueva

**Formato típico de API key:**  
`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 4. Guardar la API Key de Forma Segura

**❌ NO hacer:**
- No commitear en Git (agregar a `.gitignore`)
- No compartir públicamente
- No guardar en archivos sin encriptar en repositorios públicos

**✅ SÍ hacer:**

**Opción A: Variable de entorno (recomendado)**
```bash
# Linux/Mac - agregar a ~/.bashrc o ~/.zshrc
export MINIMAX_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Recargar shell
source ~/.bashrc  # o source ~/.zshrc

# Verificar
echo $MINIMAX_API_KEY
```

**Opción B: Archivo .env (para desarrollo local)**
```bash
# Crear archivo .env en root del proyecto
cd /home/user/webapp
nano .env

# Agregar:
MINIMAX_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
MINIMAX_BASE_URL=https://api.minimax.io/v1

# Guardar (Ctrl+O, Enter, Ctrl+X)

# Agregar .env a .gitignore
echo ".env" >> .gitignore
```

**Opción C: Gestor de secrets (producción)**
```bash
# Usando pass (password store)
pass insert minimax/api_key

# Usando 1Password CLI
op item create --category="API Key" --title="MiniMax API" --vault="Research" \
  api_key="sk-xxxxxxxx..."
```

---

## 🔧 Configuración del Proyecto

### 1. Instalar Dependencias

```bash
cd /home/user/webapp/law-rendezvous-point/methodology

# Instalar OpenAI SDK (compatible con MiniMax)
pip install openai

# Opcional: para manejo de .env
pip install python-dotenv
```

### 2. Configurar Variables de Entorno

**Método A: Export directo**
```bash
export MINIMAX_API_KEY="sk-xxxxxxxx..."
export MINIMAX_BASE_URL="https://api.minimax.io/v1"
```

**Método B: Usando python-dotenv**
```python
# Al inicio de minimax_validation_tomasello2012.py (ya incluido)
from dotenv import load_dotenv
load_dotenv()  # Carga variables de .env automáticamente

# Luego el código usa:
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
```

### 3. Verificar Configuración

```bash
# Test rápido de conexión
python -c "
import os
from openai import OpenAI

client = OpenAI(
    base_url='https://api.minimax.io/v1',
    api_key=os.getenv('MINIMAX_API_KEY')
)

try:
    response = client.chat.completions.create(
        model='MiniMax-M2',
        messages=[{'role': 'user', 'content': 'Hello!'}],
        max_tokens=50
    )
    print('✅ API Key válida!')
    print('Respuesta:', response.choices[0].message.content)
except Exception as e:
    print('❌ Error:', str(e))
"
```

**Output esperado:**
```
✅ API Key válida!
Respuesta: Hello! How can I assist you today?
```

---

## 🚀 Ejecutar Validación de Tomasello (2012)

Una vez configurada la API key:

```bash
cd /home/user/webapp/law-rendezvous-point/methodology

# Ejecutar validación
python minimax_validation_tomasello2012.py

# Output esperado:
# ================================================================================
# MiniMax-M2 Validation Study: Tomasello (2012)
# ================================================================================
# 
# 📊 Step 1: Running automated analysis with MiniMax-M2...
# 🔄 Sending request to MiniMax-M2 (temperature=0.3)...
# ✅ Response received in 3.45s
# 💭 Thinking process extracted (1234 chars)
# ✅ Automated analysis completed
# 
# 📊 Step 2: Calculating validation metrics...
# ✅ Metrics calculated: 87.5% overall accuracy
# 
# 📊 Step 3: Generating validation report...
# 📄 Validation report saved to: VALIDATION_REPORT_Tomasello2012_20251027_165432.md
# 
# ================================================================================
# VALIDATION SUMMARY
# ================================================================================
# Overall Accuracy: 87.5%
# Decision Gate: ✅ PASS (≥85%)
# 
# Detailed Metrics:
#   Category Match:          ✅
#   Context F1:              82.3%
#   Correctness Agreement:   91.2%
#   Contributions F1:        85.7%
#   Clarity Match:           ✅
#   Decision Match:          ✅
# 
# 📄 Full report: VALIDATION_REPORT_Tomasello2012_20251027_165432.md
# ================================================================================
```

---

## 📊 Límites y Cuotas

### Información Disponible (Según Documentación Oficial)

**Estado actual:**
- ✅ **Gratuito "for a limited time"** (según README de MiniMax-M2)
- ℹ️ **No hay información pública sobre límites de rate** en la documentación actual
- ℹ️ **GroupID vincula a billing**, sugiere que habrá pricing futuro

### Límites Esperados (Estimación basada en modelos similares)

| Métrica | Estimación Razonable | Fuente |
|---------|---------------------|--------|
| **Requests/min** | 60-100 | Estándar en API gratuitas (Claude, OpenAI) |
| **Tokens/día** | 100k-1M | Suficiente para ~50-500 papers/día |
| **Context window** | 128k tokens | Confirmado en specs técnicas |
| **Max tokens/response** | 4096-8192 | Estándar para modelos MoE |

### Monitoreo de Uso

**Recomendación:** Implementar logging para tracking:

```python
import time
import json
from datetime import datetime

def log_api_usage(request_type, tokens_used, latency_ms, cost_estimate=None):
    """Log every API call for usage tracking"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "request_type": request_type,
        "tokens_used": tokens_used,
        "latency_ms": latency_ms,
        "cost_estimate": cost_estimate or 0.0
    }
    
    with open("minimax_usage_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Uso:
# log_api_usage("validation_tomasello2012", 2048, 3450, 0.0)
```

**Análisis periódico:**
```bash
# Total requests
cat minimax_usage_log.jsonl | wc -l

# Total tokens used
cat minimax_usage_log.jsonl | jq -s 'map(.tokens_used) | add'

# Average latency
cat minimax_usage_log.jsonl | jq -s 'map(.latency_ms) | add / length'
```

---

## ⚠️ Troubleshooting

### Error: "Invalid API Key"

**Causas posibles:**
1. API key mal copiada (falta caracteres)
2. Variable de entorno no cargada correctamente
3. API key expirada o revocada

**Solución:**
```bash
# Verificar que variable esté seteada
echo $MINIMAX_API_KEY  # Debe mostrar sk-...

# Si está vacía, re-exportar
export MINIMAX_API_KEY="sk-xxxxxxxx..."

# Verificar que no tenga espacios o saltos de línea
echo "$MINIMAX_API_KEY" | xxd  # Debe mostrar solo caracteres válidos
```

### Error: "Connection timeout"

**Causas posibles:**
1. Problemas de red
2. Base URL incorrecta
3. Firewall bloqueando requests

**Solución:**
```bash
# Test de conectividad
curl -I https://api.minimax.io/v1

# Verificar base URL
echo $MINIMAX_BASE_URL  # Debe ser https://api.minimax.io/v1

# Test con verbose output
python -c "
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv('MINIMAX_BASE_URL', 'https://api.minimax.io/v1'),
    api_key=os.getenv('MINIMAX_API_KEY'),
    timeout=30.0  # Aumentar timeout
)

try:
    response = client.chat.completions.create(
        model='MiniMax-M2',
        messages=[{'role': 'user', 'content': 'Test'}],
        max_tokens=10
    )
    print('✅ Conexión exitosa')
except Exception as e:
    print('❌ Error:', str(e))
    import traceback
    traceback.print_exc()
"
```

### Error: "Rate limit exceeded"

**Causas:**
- Demasiados requests en ventana de tiempo corta

**Solución:**
```python
import time

def call_with_retry(func, max_retries=3, backoff=2.0):
    """Retry API calls with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                wait_time = backoff ** attempt
                print(f"⏳ Rate limit hit, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    
# Uso:
# result = call_with_retry(lambda: analyze_with_minimax(...))
```

### Error: "OpenAI library not installed"

**Solución:**
```bash
pip install openai

# Verificar instalación
python -c "import openai; print(openai.__version__)"
# Debe mostrar versión (e.g., 1.54.3)
```

---

## 🔐 Seguridad y Best Practices

### 1. Rotación de Keys

**Recomendación:** Rotar API keys cada 90 días

```bash
# Generar nueva key en platform.minimax.io
# Actualizar variable de entorno
export MINIMAX_API_KEY="sk-NEW_KEY..."

# Revocar key antigua en plataforma
```

### 2. Separación de Entornos

```bash
# Development
export MINIMAX_API_KEY="sk-dev-xxxxx..."

# Production
export MINIMAX_API_KEY="sk-prod-xxxxx..."

# Usar diferentes keys para evitar contaminar límites
```

### 3. Auditoría de Uso

**Logs obligatorios:**
- Timestamp de cada request
- Input text hash (para detectar duplicados)
- Output summary (tokens, latency)
- User/session ID (si multi-usuario)

```python
import hashlib

def hash_input(text):
    """Create hash of input for deduplication"""
    return hashlib.sha256(text.encode()).hexdigest()[:16]

# Antes de cada request:
input_hash = hash_input(paper_text)
# Log input_hash para detectar re-análisis del mismo paper
```

---

## 📚 Referencias Oficiales

### Documentación
- **Platform:** https://platform.minimax.io/
- **API Docs:** https://platform.minimax.io/docs/guides/text-generation
- **Function Calling:** https://platform.minimax.io/docs/guides/text-m2-function-call

### SDKs Compatibles
- **OpenAI SDK:** `pip install openai` (recomendado para este proyecto)
- **Anthropic SDK:** `pip install anthropic` (alternativa)

### Soporte
- **GitHub Issues:** https://github.com/MiniMax-AI/MiniMax-M2/issues
- **Email:** model@minimax.io (según README oficial)

---

## ✅ Checklist de Setup Completo

Antes de ejecutar la validación, verificar:

- [ ] **Cuenta creada** en https://platform.minimax.io/
- [ ] **GroupID obtenido** (19 dígitos)
- [ ] **API Key generada** y copiada
- [ ] **API Key guardada** de forma segura (.env o variable de entorno)
- [ ] **OpenAI SDK instalado** (`pip install openai`)
- [ ] **Variables de entorno configuradas** (MINIMAX_API_KEY, MINIMAX_BASE_URL)
- [ ] **Test de conexión exitoso** (script de verificación)
- [ ] **Git configurado** para ignorar .env (en .gitignore)
- [ ] **Listo para ejecutar** `python minimax_validation_tomasello2012.py`

---

## 🚀 Siguiente Paso

Una vez completado el setup:

```bash
cd /home/user/webapp/law-rendezvous-point/methodology
python minimax_validation_tomasello2012.py
```

**Resultado esperado:**
- Accuracy ≥85% → ✅ Proceder con benchmark completo (N=10 papers)
- Accuracy <85% → ⚠️ Iterar en prompt engineering

---

**Última actualización:** 2025-10-27  
**Versión:** 1.0.0  
**Autor:** IusMorfos Research Team  
**Licencia:** MIT
