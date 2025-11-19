"""
MiniMax-M2 Integration for IusMorfos Research System
====================================================

Production-ready integration of MiniMax-M2 (230B params, 10B active) for:
- Three-Pass Paper Analysis automation
- Legal Rubicon literature search
- EGT Framework debugging and development

Key Features:
- Interleaved thinking extraction (<think> tags)
- XML tool calling parsing
- Structured response validation
- Token usage tracking
- Retry logic with exponential backoff

Quick Start:
-----------
```python
from integrations.minimax_m2 import chat

# Simple chat
response = chat("Analyze this paper...")
print(response.content)

# Access thinking
if response.has_thinking():
    print(response.thinking.cleaned_thinking)

# Check usage
print(f"Tokens: {response.usage['total_tokens']}")
print(f"Latency: {response.latency_ms}ms")
```

Advanced Usage:
--------------
```python
from integrations.minimax_m2 import MiniMaxClient, MiniMaxConfig

# Custom configuration
config = MiniMaxConfig(
    api_key="your-key",
    temperature=0.3,
    max_completion_tokens=8192
)

client = MiniMaxClient(config)

# Multi-turn conversation
messages = [
    {"role": "user", "content": "What is shared intentionality?"},
]

response = client.chat(
    messages=messages,
    system_prompt="You are an expert in evolutionary anthropology.",
    extract_thinking=True
)

# Tool calling
tools = [{
    "name": "search_papers",
    "description": "Search academic databases",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "databases": {"type": "array", "items": {"type": "string"}}
        }
    }
}]

response = client.chat(
    messages=[{"role": "user", "content": "Find papers on Tomasello"}],
    tools=tools,
    parse_tool_calls=True
)

if response.has_tool_calls():
    for tool_call in response.tool_calls:
        print(f"{tool_call.name}({tool_call.arguments})")
```

Benchmarks:
----------
```bash
# Run Tomasello (2012) benchmark
cd integrations/minimax-m2/benchmarks
python tomasello_2012_benchmark.py

# Save results to JSON
python tomasello_2012_benchmark.py --save results.json

# Use local vLLM deployment
python tomasello_2012_benchmark.py --mock
```

Configuration:
-------------
Environment variables:
- MINIMAX_API_KEY: API key from https://platform.minimax.io/
- MINIMAX_BASE_URL: API base URL (default: https://api.minimax.chat/v1)
- MINIMAX_MODEL: Model name (default: MiniMax-M2)

Local vLLM deployment:
```bash
vllm serve MiniMaxAI/MiniMax-M2 \\
  --host 0.0.0.0 \\
  --port 8000 \\
  --tensor-parallel-size 2 \\
  --dtype float16 \\
  --max-model-len 128000
```

Then use mock config:
```python
config = MiniMaxConfig.mock_config()
client = MiniMaxClient(config)
```
"""

from .client import (
    MiniMaxClient,
    MiniMaxResponse,
    ThinkingContent,
    ToolCall,
    chat
)
from .config import MiniMaxConfig, get_config

__all__ = [
    "MiniMaxClient",
    "MiniMaxResponse",
    "ThinkingContent",
    "ToolCall",
    "MiniMaxConfig",
    "get_config",
    "chat"
]

__version__ = "0.1.0"
