# MiniMax-M2 Integration

Production-ready integration of **MiniMax-M2** (230B params, 10B active, MIT license) for the IusMorfos unified research system.

## 🎯 Purpose

Accelerate research workflows by automating:

1. **Three-Pass Paper Analysis** (PASS 1: 5-10 min → automated)
2. **Legal Rubicon Literature Search** (cross-disciplinary browsing)
3. **EGT Framework Development** (debugging, code review, documentation)

## 📊 Performance

- **#1 Open-Source** model (Artificial Analysis Intelligence: 61)
- **BrowseComp: 44%** (vs Claude Sonnet 4: 12.2%)
- **Terminal-Bench: 46.3%** (vs Claude: 36.4%)
- **Latency: ~500ms** (3x faster than Claude)
- **Cost: $0.01/1M tokens** (3x cheaper, API free temporarily)

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install openai  # MiniMax uses OpenAI-compatible API

# Set API key
export MINIMAX_API_KEY="your-api-key-here"
```

Get your API key: https://platform.minimax.io/

### 2. Basic Usage

```python
from integrations.minimax_m2 import chat

# Simple chat
response = chat("Explain shared intentionality in human evolution")

print(response.content)
# => "Shared intentionality refers to..."

# Access thinking process (unique to MiniMax-M2)
if response.has_thinking():
    print("\nModel's reasoning:")
    print(response.thinking.cleaned_thinking)

# Check performance
print(f"\nTokens: {response.usage['total_tokens']}")
print(f"Latency: {response.latency_ms}ms")
```

### 3. Advanced Usage

```python
from integrations.minimax_m2 import MiniMaxClient

client = MiniMaxClient()

# Multi-turn conversation
messages = [
    {"role": "user", "content": "What is the Legal Rubicon hypothesis?"},
]

response = client.chat(
    messages=messages,
    system_prompt="You are an expert in evolutionary anthropology and legal theory.",
    temperature=0.3,  # Lower for analytical tasks
    extract_thinking=True
)

# Continue conversation
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": "How does it relate to Tomasello's work?"})

response2 = client.chat(messages)
```

## 🧪 Benchmarks

We benchmark MiniMax-M2 against manual expert analysis to validate accuracy.

### Tomasello (2012) Benchmark

Compare MiniMax-M2's Three-Pass Method PASS 1 against our manual analysis (10 minutes human time).

```bash
cd integrations/minimax-m2/benchmarks
python tomasello_2012_benchmark.py
```

**Success Criteria:**
- ✅ Overall accuracy ≥ 85% vs. manual analysis
- ✅ Inference time < 60 seconds
- ✅ Five C's correctness (Category, Context, Correctness, Contributions, Clarity)
- ✅ Decision alignment (READ/CITE/DISCARD)

**Ground Truth:**
- Manual analysis: `law-rendezvous-point/methodology/paper_analysis/EXAMPLE_Tomasello_2012.md`
- Total time: 5h 55min (PASS 1: 10min, PASS 2: 1h 15min, PASS 3: 4h 30min)

**Save Results:**
```bash
python tomasello_2012_benchmark.py --save results.json
```

## 📁 Directory Structure

```
integrations/minimax-m2/
├── __init__.py              # Package exports
├── README.md                # This file
├── config.py                # Configuration management
├── client.py                # MiniMax client with thinking extraction
├── benchmarks/              # Benchmarking scripts
│   └── tomasello_2012_benchmark.py
├── tests/                   # Unit tests
│   └── test_client.py
└── logs/                    # Benchmark results and logs
    └── tomasello_2012_*.json
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
export MINIMAX_API_KEY="your-key"

# Optional
export MINIMAX_BASE_URL="https://api.minimax.chat/v1"  # Default
export MINIMAX_MODEL="MiniMax-M2"                       # Default
```

### Local vLLM Deployment

For intensive usage, deploy locally:

```bash
# Download model (460GB FP16)
huggingface-cli download MiniMaxAI/MiniMax-M2 --local-dir ./models/minimax-m2

# Start vLLM server (requires 40GB+ VRAM)
vllm serve MiniMaxAI/MiniMax-M2 \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 2 \
  --dtype float16 \
  --max-model-len 128000
```

Then use mock configuration:

```python
from integrations.minimax_m2 import MiniMaxConfig, MiniMaxClient

config = MiniMaxConfig.mock_config()
client = MiniMaxClient(config)
```

## 🎓 Key Features

### 1. Interleaved Thinking Extraction

MiniMax-M2 exposes its reasoning process in `<think>...</think>` tags:

```python
response = chat("Analyze this paper...", extract_thinking=True)

if response.has_thinking():
    print("Model's internal reasoning:")
    print(response.thinking.cleaned_thinking)
    print(f"Thinking tokens: ~{response.thinking.thinking_tokens}")
```

**Why this matters:**
- **Academic rigor:** Audit the model's reasoning process
- **Error detection:** Catch faulty assumptions early
- **Trust:** Understand how conclusions were reached

### 2. XML Tool Calling

MiniMax-M2 uses structured XML for tool calling (more robust than JSON):

```python
tools = [{
    "name": "search_academic_literature",
    "description": "Search papers in academic databases",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "databases": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
}]

response = client.chat(
    messages=[{"role": "user", "content": "Find papers on shared intentionality"}],
    tools=tools,
    parse_tool_calls=True
)

if response.has_tool_calls():
    for tc in response.tool_calls:
        print(f"Tool: {tc.name}")
        print(f"Args: {tc.arguments}")
        # Execute tool and return results...
```

**Tool Call Format (XML):**
```xml
<minimax:tool_call>
<invoke name="search_academic_literature">
<parameter name="query">shared intentionality evolution</parameter>
<parameter name="databases">["pubmed", "google_scholar"]</parameter>
</invoke>
</minimax:tool_call>
```

### 3. Structured Response Validation

All responses are validated and structured:

```python
@dataclass
class MiniMaxResponse:
    content: str                        # Clean text (thinking/tools removed)
    thinking: Optional[ThinkingContent] # Extracted reasoning
    tool_calls: List[ToolCall]          # Parsed tool invocations
    usage: Dict[str, int]               # Token counts
    latency_ms: float                   # Response time
```

### 4. Retry Logic

Automatic retry with exponential backoff:

```python
response = client.chat(
    messages=messages,
    max_retries=3  # Default: 3 attempts
)
```

Handles:
- API timeouts
- Transient errors
- Rate limiting (with backoff)

## 📈 Integration Roadmap

### ✅ Phase 1: Setup & Validation (Week 1-2)
- [x] MiniMax-M2 client implementation
- [x] Thinking extraction
- [x] Tool calling parser
- [x] Tomasello (2012) benchmark
- [ ] **Run benchmark and validate ≥85% accuracy**
- [ ] Decision: Proceed with full integration if passed

### 📋 Phase 2: Three-Pass Integration (Week 3-4)
- [ ] Modify `THREE_PASS_MASTER_PROMPT.md` to support automation
- [ ] Create `paper_analyzer_automated.py`
- [ ] Batch processing for multiple papers
- [ ] Citation graph builder

### 📋 Phase 3: Legal Rubicon Integration (Week 5-8)
- [ ] Literature search agent with BrowseComp chains
- [ ] Auto-generate `SEARCH_LOG_*.md` entries
- [ ] Cross-disciplinary paper retrieval
- [ ] Evidence traceability system

### 📋 Phase 4: EGT Framework Integration (Week 9-12)
- [ ] Debug agent for pytest failures
- [ ] Code review automation
- [ ] Auto-documentation generation
- [ ] CI/CD integration

## 🔬 Research Applications

### Three-Pass Paper Analysis

**Problem:** Manual analysis takes 6-8 hours per paper  
**Solution:** Automate PASS 1 (5-10 min) → 10x throughput

```python
from integrations.minimax_m2 import chat

paper_text = load_paper("tomasello_2012.txt")

response = chat(f"""
Analyze this paper using Three-Pass Method (PASS 1):
{paper_text}

Answer the Five C's: Category, Context, Correctness, Contributions, Clarity.
Recommend action: READ/CITE/DISCARD/MONITOR.
Output as JSON.
""", temperature=0.3)

analysis = json.loads(response.content)
print(f"Decision: {analysis['decision']}")
```

### Legal Rubicon Literature Search

**Problem:** Cross-disciplinary search (anthropology + law + primatology)  
**Solution:** Automated browse → retrieve → cite chains

```python
tools = [
    {"name": "search_databases", ...},
    {"name": "extract_citations", ...},
    {"name": "summarize_findings", ...}
]

response = client.chat(
    messages=[{
        "role": "user",
        "content": "Find evidence for shared intentionality at 2M years ago"
    }],
    tools=tools
)

# Model will invoke tools in sequence
for tc in response.tool_calls:
    result = execute_tool(tc.name, tc.arguments)
    # Feed back to model for synthesis...
```

### EGT Framework Debugging

**Problem:** Manual debugging of NumPy/SciPy integration issues  
**Solution:** Automated diagnosis + fix proposals

```python
test_output = run_pytest("tests/egt/test_universal_predictor.py")

response = chat(f"""
Debug this pytest failure:
{test_output}

1. Read failing test
2. Read source code
3. Identify root cause
4. Propose minimal fix
5. Verify fix works
""")

# Model returns diagnosis + fix proposal
fix = parse_fix_proposal(response.content)
apply_fix(fix)
```

## 🤝 Comparison with Alternatives

| Feature | MiniMax-M2 | Claude Sonnet 4 | GPT-5 (Thinking) |
|---------|-----------|-----------------|------------------|
| **License** | ✅ MIT | ❌ Proprietary | ❌ Proprietary |
| **Cost** | ✅ $0.01/1M | ❌ $3/1M | ❌ $10-30/1M |
| **Latency** | ✅ ~500ms | ⚠️ ~1500ms | ⚠️ ~3000ms |
| **Thinking** | ✅ Visible | ❌ Hidden | ✅ Visible |
| **Agentic** | ✅ 44% BrowseComp | ❌ 12.2% | ✅ 54.9% |
| **Coding** | ✅ 46.3% Terminal | ⚠️ 36.4% | ⚠️ 43.8% |
| **Local Deploy** | ✅ Yes | ❌ No | ❌ No |
| **Context** | ✅ 128k | ✅ 200k | ✅ 128k |

**Recommendation:** MiniMax-M2 is optimal for **academic research + coding** workflows requiring transparency, local deployment, and cost efficiency.

## 📚 References

- **Model Card:** https://huggingface.co/MiniMaxAI/MiniMax-M2
- **Fork Repository:** https://github.com/adrianlerer/MiniMax-M2
- **Official Docs:** https://platform.minimax.io/docs/
- **Integration Analysis:** `law-rendezvous-point/methodology/MINIMAX_M2_INTEGRATION_ANALYSIS.md`
- **Quickstart Code:** `law-rendezvous-point/methodology/minimax_m2_quickstart.py`

## 📝 License

This integration code is MIT licensed (same as MiniMax-M2 model).

---

**Status:** ✅ Ready for Benchmark  
**Next Step:** Run `python benchmarks/tomasello_2012_benchmark.py`  
**Decision Gate:** Proceed with full integration if accuracy ≥ 85%
