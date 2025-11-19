"""
Unit tests for MiniMax-M2 client
================================

Tests for:
- Configuration management
- Thinking extraction
- Tool call parsing
- Response validation
"""

import pytest
import json
from unittest.mock import Mock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from client import (
    MiniMaxClient,
    MiniMaxResponse,
    ThinkingContent,
    ToolCall
)
from config import MiniMaxConfig


class TestConfig:
    """Test configuration management."""
    
    def test_mock_config(self):
        """Test mock configuration for local vLLM."""
        config = MiniMaxConfig.mock_config()
        
        assert config.api_key == "dummy"
        assert config.base_url == "http://localhost:8000/v1"
        assert "MiniMax" in config.model
    
    def test_default_parameters(self):
        """Test default inference parameters."""
        config = MiniMaxConfig.mock_config()
        
        assert config.temperature == 1.0
        assert config.top_p == 0.95
        assert config.top_k == 40
        assert config.max_context_tokens == 128_000


class TestThinkingExtraction:
    """Test thinking content extraction."""
    
    def test_extract_thinking_single_block(self):
        """Test extraction of single thinking block."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        Let me analyze this.
        <think>
        This is a theoretical paper building on Tomasello's work.
        The two-step model is well-supported by evidence.
        </think>
        Based on my analysis, this is a theoretical paper.
        """
        
        thinking = client._extract_thinking(content)
        
        assert thinking is not None
        assert "Tomasello" in thinking.cleaned_thinking
        assert "two-step model" in thinking.cleaned_thinking
        assert thinking.thinking_tokens > 0
    
    def test_extract_thinking_multiple_blocks(self):
        """Test extraction of multiple thinking blocks."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        <think>First block of reasoning.</think>
        Some text.
        <think>Second block of reasoning.</think>
        """
        
        thinking = client._extract_thinking(content)
        
        assert thinking is not None
        assert "First block" in thinking.raw_thinking
        assert "Second block" in thinking.raw_thinking
        assert "---" in thinking.raw_thinking  # Separator
    
    def test_no_thinking(self):
        """Test when no thinking blocks present."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = "Just regular content without thinking."
        
        thinking = client._extract_thinking(content)
        
        assert thinking is None


class TestToolCallParsing:
    """Test XML tool call parsing."""
    
    def test_parse_single_tool_call(self):
        """Test parsing single tool invocation."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        <minimax:tool_call>
        <invoke name="search_papers">
        <parameter name="query">shared intentionality</parameter>
        <parameter name="max_results">10</parameter>
        </invoke>
        </minimax:tool_call>
        """
        
        tools = [{
            "name": "search_papers",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer"}
                }
            }
        }]
        
        tool_calls = client._parse_tool_calls(content, tools)
        
        assert len(tool_calls) == 1
        assert tool_calls[0].name == "search_papers"
        assert tool_calls[0].arguments["query"] == "shared intentionality"
        assert tool_calls[0].arguments["max_results"] == 10  # Converted to int
    
    def test_parse_multiple_tool_calls(self):
        """Test parsing multiple tool invocations."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        <minimax:tool_call>
        <invoke name="search_papers">
        <parameter name="query">Tomasello</parameter>
        </invoke>
        <invoke name="extract_metadata">
        <parameter name="paper_id">doi:10.1234</parameter>
        </invoke>
        </minimax:tool_call>
        """
        
        tools = [
            {"name": "search_papers", "parameters": {"type": "object", "properties": {}}},
            {"name": "extract_metadata", "parameters": {"type": "object", "properties": {}}}
        ]
        
        tool_calls = client._parse_tool_calls(content, tools)
        
        assert len(tool_calls) == 2
        assert tool_calls[0].name == "search_papers"
        assert tool_calls[1].name == "extract_metadata"
    
    def test_parse_array_parameter(self):
        """Test parsing array parameter (JSON)."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        <minimax:tool_call>
        <invoke name="search_databases">
        <parameter name="databases">["pubmed", "google_scholar"]</parameter>
        </invoke>
        </minimax:tool_call>
        """
        
        tools = [{
            "name": "search_databases",
            "parameters": {
                "type": "object",
                "properties": {
                    "databases": {"type": "array"}
                }
            }
        }]
        
        tool_calls = client._parse_tool_calls(content, tools)
        
        assert len(tool_calls) == 1
        assert isinstance(tool_calls[0].arguments["databases"], list)
        assert "pubmed" in tool_calls[0].arguments["databases"]
    
    def test_no_tool_calls(self):
        """Test when no tool calls present."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = "Just regular text without tool calls."
        
        tool_calls = client._parse_tool_calls(content, None)
        
        assert len(tool_calls) == 0


class TestContentCleaning:
    """Test content cleaning (remove thinking/tools)."""
    
    def test_clean_thinking(self):
        """Test removal of thinking tags."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        Here is my analysis.
        <think>Internal reasoning here.</think>
        The final answer is X.
        """
        
        clean = client._clean_content(content)
        
        assert "<think>" not in clean
        assert "</think>" not in clean
        assert "Here is my analysis" in clean
        assert "The final answer is X" in clean
        assert "Internal reasoning" not in clean
    
    def test_clean_tool_calls(self):
        """Test removal of tool call tags."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        Let me search for papers.
        <minimax:tool_call>
        <invoke name="search">...</invoke>
        </minimax:tool_call>
        Here are the results.
        """
        
        clean = client._clean_content(content)
        
        assert "<minimax:tool_call>" not in clean
        assert "<invoke" not in clean
        assert "Let me search" in clean
        assert "Here are the results" in clean
    
    def test_clean_multiple_blocks(self):
        """Test cleaning multiple thinking/tool blocks."""
        client = MiniMaxClient(MiniMaxConfig.mock_config())
        
        content = """
        <think>Reasoning 1</think>
        Text A
        <minimax:tool_call><invoke name="x"></invoke></minimax:tool_call>
        Text B
        <think>Reasoning 2</think>
        Text C
        """
        
        clean = client._clean_content(content)
        
        assert "Reasoning" not in clean
        assert "<think>" not in clean
        assert "<minimax:tool_call>" not in clean
        assert "Text A" in clean
        assert "Text B" in clean
        assert "Text C" in clean


class TestMiniMaxResponse:
    """Test MiniMaxResponse dataclass."""
    
    def test_has_thinking(self):
        """Test has_thinking() method."""
        thinking = ThinkingContent(
            raw_thinking="raw",
            cleaned_thinking="clean",
            thinking_tokens=100
        )
        
        response_with = MiniMaxResponse(
            content="content",
            thinking=thinking,
            tool_calls=[],
            usage={},
            latency_ms=500.0
        )
        
        response_without = MiniMaxResponse(
            content="content",
            thinking=None,
            tool_calls=[],
            usage={},
            latency_ms=500.0
        )
        
        assert response_with.has_thinking() is True
        assert response_without.has_thinking() is False
    
    def test_has_tool_calls(self):
        """Test has_tool_calls() method."""
        tool_call = ToolCall(
            name="search",
            arguments={"query": "test"},
            raw_xml="<invoke>...</invoke>"
        )
        
        response_with = MiniMaxResponse(
            content="content",
            thinking=None,
            tool_calls=[tool_call],
            usage={},
            latency_ms=500.0
        )
        
        response_without = MiniMaxResponse(
            content="content",
            thinking=None,
            tool_calls=[],
            usage={},
            latency_ms=500.0
        )
        
        assert response_with.has_tool_calls() is True
        assert response_without.has_tool_calls() is False
    
    def test_to_dict(self):
        """Test serialization to dict."""
        thinking = ThinkingContent("raw", "clean", 100)
        tool_call = ToolCall("search", {"query": "test"}, "raw_xml")
        
        response = MiniMaxResponse(
            content="test content",
            thinking=thinking,
            tool_calls=[tool_call],
            usage={"total_tokens": 1000},
            latency_ms=500.5
        )
        
        data = response.to_dict()
        
        assert data["content"] == "test content"
        assert data["thinking"]["cleaned_thinking"] == "clean"
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["name"] == "search"
        assert data["usage"]["total_tokens"] == 1000
        assert data["latency_ms"] == 500.5


# Integration test (requires API key or mock)
class TestIntegration:
    """Integration tests (skip if no API key)."""
    
    @pytest.mark.skip(reason="Requires MINIMAX_API_KEY or running vLLM")
    def test_simple_chat(self):
        """Test simple chat completion."""
        from integrations.minimax_m2 import chat
        
        response = chat(
            "What is 2+2?",
            system_prompt="You are a helpful math assistant."
        )
        
        assert response.content is not None
        assert len(response.content) > 0
        assert response.usage["total_tokens"] > 0
        assert response.latency_ms > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
