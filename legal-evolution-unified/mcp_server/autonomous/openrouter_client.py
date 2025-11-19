"""
OpenRouter Client for Autonomous Legal Analysis
Enables LLM-powered extraction and analysis of legal documents
"""

import os
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI

class OpenRouterClient:
    """Client for OpenRouter API (access to Claude, GPT-4, etc.)"""
    
    def __init__(self, api_key: Optional[str] = None, budget_usd: float = 5.0):
        """
        Initialize OpenRouter client.
        
        Args:
            api_key: OpenRouter API key (reads from .env if not provided)
            budget_usd: Maximum spending limit
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Set OPENROUTER_API_KEY env var.")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        
        self.budget_usd = budget_usd
        self.spent_usd = 0.0
        self.default_model = "anthropic/claude-3.5-sonnet"
    
    def extract_citations(self, case_text: str) -> Dict[str, Any]:
        """
        Extract all case citations from legal text using LLM.
        
        Args:
            case_text: Full text of legal case
        
        Returns:
            Dict with extracted citations and metadata
        """
        if self.spent_usd >= self.budget_usd:
            return {"error": "Budget limit exceeded", "citations": []}
        
        prompt = f"""Extract ALL case citations from this legal text. Return JSON format:
{{
    "citations": [
        {{
            "case_name": "...",
            "year": ...,
            "court": "...",
            "citation_type": "explicit/implicit"
        }}
    ]
}}

Legal text:
{case_text[:8000]}  # Limit to 8k chars (~$0.01)
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1  # Low temperature for factual extraction
            )
            
            # Estimate cost: ~$0.01-0.03 per call
            self.spent_usd += 0.02
            
            result = json.loads(response.choices[0].message.content)
            result["cost_usd"] = 0.02
            result["model"] = self.default_model
            
            return result
            
        except Exception as e:
            return {"error": str(e), "citations": []}
    
    def classify_doctrine(self, case_text: str) -> Dict[str, Any]:
        """
        Classify doctrinal approach of a case (textualism, purposivism, etc.)
        
        Args:
            case_text: Full text or excerpt
        
        Returns:
            Dict with doctrine classification and confidence
        """
        if self.spent_usd >= self.budget_usd:
            return {"error": "Budget limit exceeded"}
        
        prompt = f"""Classify the constitutional interpretation doctrine used in this case. 
Return JSON:
{{
    "primary_doctrine": "originalismo/textualismo/purposivismo/living_constitution",
    "confidence": 0.0-1.0,
    "evidence": ["quote1", "quote2"],
    "secondary_doctrines": ["..."]
}}

Case text:
{case_text[:6000]}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            
            self.spent_usd += 0.015
            
            result = json.loads(response.choices[0].message.content)
            result["cost_usd"] = 0.015
            
            return result
            
        except Exception as e:
            return {"error": str(e), "primary_doctrine": "unknown"}
    
    def analyze_case_for_cli(self, case_text: str, constitutional_text: str) -> Dict[str, Any]:
        """
        Analyze case to score CLI components (Judicial Activism, Precedent Weight, etc.)
        
        Args:
            case_text: Judicial decision text
            constitutional_text: Relevant constitutional provisions
        
        Returns:
            Dict with CLI component scores and reasoning
        """
        if self.spent_usd >= self.budget_usd:
            return {"error": "Budget limit exceeded"}
        
        prompt = f"""Analyze this case to score CLI (Constitutional Lock-in Index) components.
Return JSON with scores 0.0-1.0:
{{
    "judicial_activism": {{
        "score": 0.0-1.0,
        "reasoning": "..."
    }},
    "precedent_weight": {{
        "score": 0.0-1.0,
        "reasoning": "..."
    }},
    "text_vagueness": {{
        "score": 0.0-1.0,
        "reasoning": "..."
    }}
}}

Constitutional text:
{constitutional_text[:2000]}

Case text:
{case_text[:5000]}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.2
            )
            
            self.spent_usd += 0.025
            
            result = json.loads(response.choices[0].message.content)
            result["cost_usd"] = 0.025
            result["total_spent_usd"] = self.spent_usd
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_budget_status(self) -> Dict[str, float]:
        """Get current budget usage"""
        return {
            "budget_usd": self.budget_usd,
            "spent_usd": self.spent_usd,
            "remaining_usd": self.budget_usd - self.spent_usd,
            "usage_percent": (self.spent_usd / self.budget_usd) * 100
        }

