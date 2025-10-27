"""
MiniMax-M2 Configuration
========================

Configuration management for MiniMax-M2 integration.

Environment variables:
    MINIMAX_API_KEY: API key from https://platform.minimax.io/
    MINIMAX_BASE_URL: API base URL (default: https://api.minimax.chat/v1)
    MINIMAX_MODEL: Model name (default: MiniMax-M2)
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class MiniMaxConfig:
    """MiniMax-M2 configuration."""
    
    api_key: str
    base_url: str = "https://api.minimax.chat/v1"
    model: str = "MiniMax-M2"
    
    # Recommended inference parameters (from official docs)
    temperature: float = 1.0
    top_p: float = 0.95
    top_k: int = 40
    
    # Context limits
    max_context_tokens: int = 128_000
    max_completion_tokens: int = 4_096
    
    @classmethod
    def from_env(cls) -> "MiniMaxConfig":
        """Load configuration from environment variables."""
        api_key = os.getenv("MINIMAX_API_KEY")
        
        if not api_key:
            raise ValueError(
                "MINIMAX_API_KEY not found in environment. "
                "Get your key from https://platform.minimax.io/"
            )
        
        return cls(
            api_key=api_key,
            base_url=os.getenv("MINIMAX_BASE_URL", cls.base_url),
            model=os.getenv("MINIMAX_MODEL", cls.model)
        )
    
    @classmethod
    def mock_config(cls) -> "MiniMaxConfig":
        """Create mock configuration for local vLLM deployment."""
        return cls(
            api_key="dummy",
            base_url="http://localhost:8000/v1",
            model="MiniMaxAI/MiniMax-M2"
        )


def get_config(use_mock: bool = False) -> MiniMaxConfig:
    """
    Get MiniMax configuration.
    
    Args:
        use_mock: If True, use mock config for local vLLM
    
    Returns:
        MiniMaxConfig instance
    """
    if use_mock:
        return MiniMaxConfig.mock_config()
    
    return MiniMaxConfig.from_env()
