"""
MiniMax-M2 Client
=================

Production-ready client for MiniMax-M2 API with:
- Structured response parsing
- Thinking extraction (interleaved thinking format)
- Tool calling support (XML parsing)
- Error handling and retries
- Token usage tracking
"""

import re
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

try:
    from openai import OpenAI, APIError, APITimeoutError
except ImportError:
    raise ImportError(
        "OpenAI package required. Install with: pip install openai"
    )

from .config import MiniMaxConfig, get_config


@dataclass
class ThinkingContent:
    """Extracted thinking content from model response."""
    raw_thinking: str
    cleaned_thinking: str
    thinking_tokens: int  # Estimated
    
    def __str__(self) -> str:
        return self.cleaned_thinking


@dataclass
class ToolCall:
    """Parsed tool call from XML format."""
    name: str
    arguments: Dict[str, Any]
    raw_xml: str
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "arguments": self.arguments
        }


@dataclass
class MiniMaxResponse:
    """Structured response from MiniMax-M2."""
    content: str
    thinking: Optional[ThinkingContent]
    tool_calls: List[ToolCall]
    usage: Dict[str, int]
    latency_ms: float
    
    def has_thinking(self) -> bool:
        return self.thinking is not None
    
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0
    
    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "thinking": asdict(self.thinking) if self.thinking else None,
            "tool_calls": [tc.to_dict() for tc in self.tool_calls],
            "usage": self.usage,
            "latency_ms": self.latency_ms
        }


class MiniMaxClient:
    """
    Production client for MiniMax-M2 API.
    
    Features:
    - Automatic thinking extraction
    - Tool calling with XML parsing
    - Retry logic with exponential backoff
    - Token usage tracking
    - Response validation
    """
    
    def __init__(self, config: Optional[MiniMaxConfig] = None):
        """
        Initialize MiniMax client.
        
        Args:
            config: MiniMaxConfig instance (default: load from env)
        """
        self.config = config or get_config()
        self.client = OpenAI(
            base_url=self.config.base_url,
            api_key=self.config.api_key
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        extract_thinking: bool = True,
        parse_tool_calls: bool = True,
        max_retries: int = 3
    ) -> MiniMaxResponse:
        """
        Send chat completion request to MiniMax-M2.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt (prepended to messages)
            tools: Optional tool definitions (OpenAI format)
            temperature: Sampling temperature (default: from config)
            max_tokens: Max completion tokens (default: from config)
            extract_thinking: Extract <think>...</think> content
            parse_tool_calls: Parse <minimax:tool_call> XML
            max_retries: Maximum retry attempts on failure
        
        Returns:
            MiniMaxResponse with structured data
        """
        # Prepend system prompt if provided
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        # Build request parameters
        params = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_completion_tokens,
            "top_p": self.config.top_p,
            "top_k": self.config.top_k
        }
        
        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"
        
        # Execute with retries
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                response = self.client.chat.completions.create(**params)
                latency_ms = (time.time() - start_time) * 1000
                
                # Extract response content
                raw_content = response.choices[0].message.content
                
                # Parse thinking
                thinking = None
                if extract_thinking:
                    thinking = self._extract_thinking(raw_content)
                
                # Parse tool calls
                tool_calls = []
                if parse_tool_calls:
                    tool_calls = self._parse_tool_calls(raw_content, tools)
                
                # Clean content (remove thinking and tool call XML)
                clean_content = self._clean_content(raw_content)
                
                # Build response
                return MiniMaxResponse(
                    content=clean_content,
                    thinking=thinking,
                    tool_calls=tool_calls,
                    usage={
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    latency_ms=latency_ms
                )
            
            except (APIError, APITimeoutError) as e:
                if attempt == max_retries - 1:
                    raise
                
                # Exponential backoff
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        raise RuntimeError("Max retries exceeded")
    
    def _extract_thinking(self, content: str) -> Optional[ThinkingContent]:
        """
        Extract thinking content from <think>...</think> tags.
        
        MiniMax-M2 uses interleaved thinking format where reasoning
        is wrapped in <think> tags. This provides transparency into
        the model's reasoning process.
        """
        pattern = r"<think>(.*?)</think>"
        matches = re.findall(pattern, content, re.DOTALL)
        
        if not matches:
            return None
        
        # Combine all thinking blocks
        raw_thinking = "\n\n---\n\n".join(matches)
        cleaned_thinking = "\n\n".join(m.strip() for m in matches)
        
        # Estimate tokens (rough: ~4 chars per token)
        thinking_tokens = len(raw_thinking) // 4
        
        return ThinkingContent(
            raw_thinking=raw_thinking,
            cleaned_thinking=cleaned_thinking,
            thinking_tokens=thinking_tokens
        )
    
    def _parse_tool_calls(
        self,
        content: str,
        tools: Optional[List[Dict]]
    ) -> List[ToolCall]:
        """
        Parse tool calls from XML format.
        
        MiniMax-M2 uses XML-based tool calling:
        <minimax:tool_call>
        <invoke name="function_name">
        <parameter name="param1">value1</parameter>
        </invoke>
        </minimax:tool_call>
        """
        if "<minimax:tool_call>" not in content:
            return []
        
        tool_calls = []
        
        # Regex patterns
        tool_call_regex = re.compile(
            r"<minimax:tool_call>(.*?)</minimax:tool_call>",
            re.DOTALL
        )
        invoke_regex = re.compile(r"<invoke name=(.*?)</invoke>", re.DOTALL)
        parameter_regex = re.compile(
            r"<parameter name=(.*?)</parameter>",
            re.DOTALL
        )
        
        # Get parameter types from tool definitions
        param_types = {}
        if tools:
            for tool in tools:
                tool_def = tool.get("function") or tool
                name = tool_def.get("name")
                params = tool_def.get("parameters", {})
                if name and "properties" in params:
                    param_types[name] = params["properties"]
        
        # Extract all tool_call blocks
        for tool_call_match in tool_call_regex.findall(content):
            # Extract all invokes in this block
            for invoke_match in invoke_regex.findall(tool_call_match):
                # Extract function name
                name_match = re.search(r'^([^>]+)', invoke_match)
                if not name_match:
                    continue
                
                function_name = name_match.group(1).strip().strip('"').strip("'")
                
                # Extract parameters
                param_dict = {}
                for match in parameter_regex.findall(invoke_match):
                    param_match = re.search(r'^([^>]+)>(.*)', match, re.DOTALL)
                    if param_match:
                        param_name = param_match.group(1).strip().strip('"').strip("'")
                        param_value = param_match.group(2).strip()
                        
                        # Type conversion based on tool definition
                        if function_name in param_types:
                            param_config = param_types[function_name].get(param_name, {})
                            param_type = param_config.get("type", "string")
                            param_value = self._convert_param_value(
                                param_value,
                                param_type
                            )
                        
                        param_dict[param_name] = param_value
                
                # Create tool call
                tool_calls.append(ToolCall(
                    name=function_name,
                    arguments=param_dict,
                    raw_xml=invoke_match
                ))
        
        return tool_calls
    
    def _convert_param_value(self, value: str, param_type: str) -> Any:
        """Convert parameter value based on expected type."""
        if value.lower() == "null":
            return None
        
        param_type = param_type.lower()
        
        if param_type in ["string", "str"]:
            return value
        elif param_type in ["integer", "int"]:
            try:
                return int(value)
            except ValueError:
                return value
        elif param_type in ["number", "float"]:
            try:
                val = float(value)
                return val if val != int(val) else int(val)
            except ValueError:
                return value
        elif param_type in ["boolean", "bool"]:
            return value.lower() in ["true", "1", "yes"]
        elif param_type in ["object", "array"]:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        else:
            # Try JSON parsing, return string if failed
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
    
    def _clean_content(self, content: str) -> str:
        """
        Remove thinking and tool call tags from content.
        
        Returns the clean text without XML markup.
        """
        # Remove thinking tags
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        
        # Remove tool call tags
        content = re.sub(
            r"<minimax:tool_call>.*?</minimax:tool_call>",
            "",
            content,
            flags=re.DOTALL
        )
        
        # Clean up extra whitespace
        content = re.sub(r"\n{3,}", "\n\n", content)
        
        return content.strip()


# Convenience function for quick usage
def chat(
    prompt: str,
    system_prompt: Optional[str] = None,
    config: Optional[MiniMaxConfig] = None,
    **kwargs
) -> MiniMaxResponse:
    """
    Quick chat completion (single user message).
    
    Args:
        prompt: User message
        system_prompt: Optional system prompt
        config: MiniMaxConfig (default: from env)
        **kwargs: Additional parameters for chat()
    
    Returns:
        MiniMaxResponse
    """
    client = MiniMaxClient(config)
    messages = [{"role": "user", "content": prompt}]
    return client.chat(messages, system_prompt=system_prompt, **kwargs)
