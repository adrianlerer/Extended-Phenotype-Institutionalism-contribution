"""
MiniMax-M2 Integration - Quick Examples
========================================

Demonstrates basic usage of MiniMax-M2 integration.

Prerequisites:
    export MINIMAX_API_KEY="your-api-key"
    
    Or use mock config for local vLLM:
    python example.py --mock
"""

import sys
import json
from pathlib import Path

# Add integrations to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from minimax_m2 import chat, MiniMaxClient, MiniMaxConfig


def example_simple_chat():
    """Example 1: Simple chat completion."""
    print("=" * 80)
    print("EXAMPLE 1: Simple Chat")
    print("=" * 80)
    
    response = chat(
        "Explain the concept of shared intentionality in human evolution in 3 sentences.",
        system_prompt="You are an expert in evolutionary anthropology."
    )
    
    print("\n📝 Response:")
    print(response.content)
    
    print(f"\n📊 Stats:")
    print(f"  Tokens: {response.usage['total_tokens']}")
    print(f"  Latency: {response.latency_ms:.0f}ms")
    
    if response.has_thinking():
        print(f"\n🤔 Thinking Process (first 200 chars):")
        print(f"  {response.thinking.cleaned_thinking[:200]}...")


def example_with_thinking():
    """Example 2: Extract thinking process."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Thinking Extraction")
    print("=" * 80)
    
    response = chat(
        "Is the Legal Rubicon hypothesis testable? Explain your reasoning.",
        system_prompt="You are a scientist analyzing research hypotheses.",
        extract_thinking=True
    )
    
    print("\n📝 Response:")
    print(response.content)
    
    if response.has_thinking():
        print(f"\n🤔 Model's Internal Reasoning:")
        print(response.thinking.cleaned_thinking)
        print(f"\n📊 Thinking tokens: ~{response.thinking.thinking_tokens}")


def example_tool_calling():
    """Example 3: Tool calling with XML parsing."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Tool Calling")
    print("=" * 80)
    
    tools = [
        {
            "name": "search_academic_papers",
            "description": "Search academic databases for papers",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query with Boolean operators"
                    },
                    "databases": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of databases to search"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    }
                },
                "required": ["query", "databases"]
            }
        }
    ]
    
    client = MiniMaxClient()
    
    response = client.chat(
        messages=[{
            "role": "user",
            "content": "Find papers about Tomasello's work on shared intentionality, search PubMed and Google Scholar."
        }],
        tools=tools,
        parse_tool_calls=True
    )
    
    print("\n📝 Response:")
    print(response.content)
    
    if response.has_tool_calls():
        print(f"\n🔧 Tool Calls Detected: {len(response.tool_calls)}")
        for i, tc in enumerate(response.tool_calls, 1):
            print(f"\n  Tool Call {i}:")
            print(f"    Function: {tc.name}")
            print(f"    Arguments:")
            for key, value in tc.arguments.items():
                print(f"      {key}: {value}")
    else:
        print("\n⚠️ No tool calls detected (model may have responded directly)")


def example_multi_turn():
    """Example 4: Multi-turn conversation."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Multi-Turn Conversation")
    print("=" * 80)
    
    client = MiniMaxClient()
    
    messages = [
        {"role": "user", "content": "What is the Legal Rubicon hypothesis?"}
    ]
    
    print("\n🗣️ Turn 1:")
    print(f"  User: {messages[0]['content']}")
    
    response1 = client.chat(
        messages=messages,
        system_prompt="You are an expert in evolutionary theory and legal institutions."
    )
    
    print(f"  Assistant: {response1.content[:200]}...")
    
    # Continue conversation
    messages.append({"role": "assistant", "content": response1.content})
    messages.append({
        "role": "user",
        "content": "How does this relate to Tomasello's two-step model?"
    })
    
    print(f"\n🗣️ Turn 2:")
    print(f"  User: {messages[2]['content']}")
    
    response2 = client.chat(messages)
    
    print(f"  Assistant: {response2.content[:200]}...")
    
    print(f"\n📊 Total tokens: {response1.usage['total_tokens'] + response2.usage['total_tokens']}")


def main():
    """Run all examples."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MiniMax-M2 Integration Examples")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock config (local vLLM deployment)"
    )
    parser.add_argument(
        "--example",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run specific example only (1-4)"
    )
    
    args = parser.parse_args()
    
    # Configure
    if args.mock:
        print("⚠️ Using MOCK configuration (local vLLM at http://localhost:8000)")
        print("Ensure vLLM is running: vllm serve MiniMaxAI/MiniMax-M2 --port 8000")
        print()
        
        # Override global config
        import minimax_m2.config as config_module
        config_module.get_config = lambda: MiniMaxConfig.mock_config()
    else:
        try:
            MiniMaxConfig.from_env()
        except ValueError as e:
            print(f"❌ Configuration error: {e}")
            print("\nTo run examples:")
            print("1. Get API key from https://platform.minimax.io/")
            print("2. Export: export MINIMAX_API_KEY='your-key-here'")
            print("3. Run: python example.py")
            print("\nOr use local vLLM:")
            print("python example.py --mock")
            sys.exit(1)
    
    # Run examples
    try:
        if args.example:
            if args.example == 1:
                example_simple_chat()
            elif args.example == 2:
                example_with_thinking()
            elif args.example == 3:
                example_tool_calling()
            elif args.example == 4:
                example_multi_turn()
        else:
            # Run all examples
            example_simple_chat()
            example_with_thinking()
            example_tool_calling()
            example_multi_turn()
        
        print("\n" + "=" * 80)
        print("✅ All examples completed successfully!")
        print("=" * 80)
        
        print("\nNext steps:")
        print("1. Run benchmark: cd benchmarks && python tomasello_2012_benchmark.py")
        print("2. Check README: cat README.md")
        print("3. Run tests: pytest tests/")
    
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
