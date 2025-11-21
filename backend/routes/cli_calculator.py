"""
CLI Calculator Routes
Constitutional Lock-In Index calculation endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional
import sys
from pathlib import Path

# Add backend services to path
sys.path.append(str(Path(__file__).parent.parent))
from services.feature_registry import registry

router = APIRouter()


class CLIInput(BaseModel):
    """Input model for CLI calculation"""
    entity: str = Field(..., description="Entity name (country/jurisdiction)")
    CE: float = Field(..., ge=0.0, le=1.0, description="Constitutional Entrenchment (0-1)")
    UA: float = Field(..., ge=0.0, le=1.0, description="Unilateral Amendment difficulty (0-1)")
    JPI: float = Field(..., ge=0.0, le=1.0, description="Judicial Power Index (0-1)")
    
    @validator('CE', 'UA', 'JPI')
    def validate_range(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError("Value must be between 0.0 and 1.0")
        return v


class CLICulturalInput(BaseModel):
    """Input model for CLI_cultural calculation"""
    entity: str = Field(..., description="Entity name")
    CT1: float = Field(..., ge=0.0, le=1.0, description="Cultural Transmission - Narrative Stability")
    CT2: float = Field(..., ge=0.0, le=1.0, description="Cultural Transmission - Shock Resistance")
    CT3: float = Field(..., ge=0.0, le=1.0, description="Cultural Transmission - Policy Continuity")


class DualIndexInput(BaseModel):
    """Input model for Dual-Index analysis"""
    entity: str = Field(..., description="Entity name")
    CLI: float = Field(..., ge=0.0, le=1.0, description="Constitutional Lock-In Index")
    CLI_cultural: float = Field(..., ge=0.0, le=1.0, description="Cultural Lock-In Index")


@router.post("/calculate")
async def calculate_cli(data: CLIInput):
    """
    Calculate Constitutional Lock-In Index (CLI)
    
    Formula: CLI = 0.35 × CE + 0.40 × UA + 0.25 × JPI
    """
    # Check if feature is enabled
    feature = registry.get_feature("cli_calculator")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="CLI Calculator feature is disabled")
    
    # Calculate CLI
    cli = 0.35 * data.CE + 0.40 * data.UA + 0.25 * data.JPI
    
    # Classify
    if cli >= 0.70:
        classification = "HIGH Lock-In (Very rigid system)"
        risk_level = "high"
    elif cli >= 0.50:
        classification = "MEDIUM Lock-In (Moderately rigid)"
        risk_level = "medium"
    else:
        classification = "LOW Lock-In (Flexible system)"
        risk_level = "low"
    
    # Track usage
    registry.track_usage("cli_calculator")
    
    return {
        "entity": data.entity,
        "CLI": round(cli, 3),
        "components": {
            "CE": data.CE,
            "UA": data.UA,
            "JPI": data.JPI,
            "weighted_CE": round(data.CE * 0.35, 3),
            "weighted_UA": round(data.UA * 0.40, 3),
            "weighted_JPI": round(data.JPI * 0.25, 3)
        },
        "classification": classification,
        "risk_level": risk_level,
        "formula": "CLI = 0.35×CE + 0.40×UA + 0.25×JPI"
    }


@router.post("/calculate-cultural")
async def calculate_cli_cultural(data: CLICulturalInput):
    """
    Calculate Cultural Lock-In Index (CLI_cultural)
    
    Formula: CLI_cultural = 0.40 × CT1 + 0.30 × CT2 + 0.30 × CT3
    """
    # Check if feature is enabled
    feature = registry.get_feature("cli_cultural_calculator")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="CLI Cultural Calculator feature is disabled")
    
    # Calculate CLI_cultural
    cli_cultural = 0.40 * data.CT1 + 0.30 * data.CT2 + 0.30 * data.CT3
    
    # Classify
    if cli_cultural >= 0.70:
        strength = "Strong cultural transmission"
    elif cli_cultural >= 0.50:
        strength = "Moderate cultural transmission"
    else:
        strength = "Weak cultural transmission"
    
    # Track usage
    registry.track_usage("cli_cultural_calculator")
    
    return {
        "entity": data.entity,
        "CLI_cultural": round(cli_cultural, 3),
        "components": {
            "CT1": data.CT1,
            "CT2": data.CT2,
            "CT3": data.CT3,
            "weighted_CT1": round(data.CT1 * 0.40, 3),
            "weighted_CT2": round(data.CT2 * 0.30, 3),
            "weighted_CT3": round(data.CT3 * 0.30, 3)
        },
        "strength": strength,
        "formula": "CLI_cultural = 0.40×CT1 + 0.30×CT2 + 0.30×CT3"
    }


@router.post("/dual-index")
async def analyze_dual_index(data: DualIndexInput):
    """
    Analyze Dual-Index Framework (CLI × CLI_cultural)
    
    Classifies institutional profiles based on quadrant matrix:
    - Stable Rigidity (CLI ≥ 0.60, CLI_cultural ≥ 0.60)
    - Brittle Rigidity (CLI ≥ 0.60, CLI_cultural < 0.60)
    - Adaptive Stability (CLI < 0.60, CLI_cultural ≥ 0.60)
    - Chaotic Fragility (CLI < 0.60, CLI_cultural < 0.60)
    """
    # Check if feature is enabled
    feature = registry.get_feature("dual_index_analyzer")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="Dual-Index Analyzer feature is disabled")
    
    # Calculate interaction
    interaction = data.CLI * data.CLI_cultural
    
    # Classify profile
    if data.CLI >= 0.60 and data.CLI_cultural >= 0.60:
        profile = "Stable Rigidity"
        explanation = "High constitutional lock-in WITH strong cultural foundation. Stable but may resist necessary adaptation."
        risk = "LOW"
    elif data.CLI >= 0.60 and data.CLI_cultural < 0.60:
        profile = "Brittle Rigidity"
        explanation = "High constitutional lock-in WITHOUT cultural foundation. 'Scaffold without foundation' - HIGH COLLAPSE RISK."
        risk = "HIGH"
    elif data.CLI < 0.60 and data.CLI_cultural >= 0.60:
        profile = "Adaptive Stability"
        explanation = "Flexible institutions anchored in cultural norms. Can adapt while maintaining continuity."
        risk = "LOW"
    else:
        profile = "Chaotic Fragility"
        explanation = "Weak institutions, weak cultural transmission. Susceptible to instability."
        risk = "MEDIUM"
    
    # Collapse risk threshold check
    below_threshold = interaction < 0.30
    
    # Track usage
    registry.track_usage("dual_index_analyzer")
    
    return {
        "entity": data.entity,
        "CLI": data.CLI,
        "CLI_cultural": data.CLI_cultural,
        "interaction_score": round(interaction, 3),
        "profile": profile,
        "risk_level": risk,
        "below_collapse_threshold": below_threshold,
        "collapse_threshold": 0.30,
        "explanation": explanation,
        "quadrant": {
            "x_axis": "Constitutional Lock-In (CLI)",
            "y_axis": "Cultural Lock-In (CLI_cultural)",
            "threshold_line": "CLI × CLI_cultural = 0.30"
        }
    }


@router.get("/examples")
async def get_examples():
    """Get example CLI calculations"""
    return {
        "examples": [
            {
                "entity": "Somalia Federal",
                "CLI": 0.76,
                "CLI_cultural": 0.34,
                "profile": "Brittle Rigidity",
                "interaction": 0.26,
                "risk": "HIGH"
            },
            {
                "entity": "Somalilandia",
                "CLI": 0.54,
                "CLI_cultural": 0.70,
                "profile": "Adaptive Stability",
                "interaction": 0.38,
                "risk": "LOW"
            },
            {
                "entity": "Uruguay",
                "CLI": 0.75,
                "CLI_cultural": 0.77,
                "profile": "Stable Rigidity",
                "interaction": 0.58,
                "risk": "LOW"
            }
        ]
    }
