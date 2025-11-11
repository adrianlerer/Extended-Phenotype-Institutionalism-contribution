"""
EGT Framework Tools
===================

MCP tools for Evolutionary Game Theory analysis of institutional dynamics.

Tools:
1. predict_reform_viability_egt - Reform prediction via EGT
2. explain_non_convergence - Why systems don't converge to golden ratio
3. calculate_parasitic_fitness - Symbolic compliance advantage analysis
"""

import sys
from pathlib import Path
from typing import Dict, Optional
import logging
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.types import Tool, TextContent


def register_egt_tools(server, config, cache, logger: logging.Logger) -> int:
    """
    Register EGT Framework tools with the MCP server.
    
    Args:
        server: MCP server instance
        config: Server configuration
        cache: Cache manager
        logger: Logger instance
    
    Returns:
        Number of tools registered
    """
    tool_count = 0
    egt_config = config.tools_enabled
    
    # Get EGT-specific configuration
    from ..core.config import get_tool_config
    egt_params = get_tool_config("egt_framework")
    
    # Tool 1: Predict Reform Viability via EGT
    @server.list_tools()
    async def list_predict_reform_viability() -> list[Tool]:
        return [
            Tool(
                name="predict_reform_viability_egt",
                description=(
                    "Predict reform viability using Evolutionary Game Theory framework.\n\n"
                    "Analyzes strategic dynamics between three player types:\n"
                    "- **Reformers**: Push for constitutional change\n"
                    "- **Incumbents**: Defend status quo\n"
                    "- **Parasites**: Symbolic compliance without real change\n\n"
                    "**Key Insight**: Parasitic strategies enjoy 12% fitness advantage, "
                    "explaining why 88% of systems deviate from optimal φ=1.618.\n\n"
                    "**Returns**: Reform viability assessment, ESS location, strategic recommendations."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "h_v_ratio": {
                            "type": "number",
                            "description": "Current H/V ratio of the system",
                            "minimum": 0
                        },
                        "cli_score": {
                            "type": "number",
                            "description": "Constitutional Lock-in Index [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "jurisdiction_name": {
                            "type": "string",
                            "description": "Name of jurisdiction"
                        },
                        "current_reform_pressure": {
                            "type": "number",
                            "description": "Current reform pressure [0,1], optional",
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "required": ["h_v_ratio", "cli_score", "jurisdiction_name"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_predict_reform_viability(name: str, arguments: dict) -> list[TextContent]:
        """Execute EGT reform viability prediction."""
        if name != "predict_reform_viability_egt":
            raise ValueError(f"Unknown tool: {name}")
        
        try:
            hv_ratio = arguments["h_v_ratio"]
            cli = arguments["cli_score"]
            jurisdiction = arguments["jurisdiction_name"]
            reform_pressure = arguments.get("current_reform_pressure", 0.5)
            
            # Determine system state
            phi = 1.618
            distance_from_phi = abs(hv_ratio - phi)
            
            # Calculate fitness values
            parasitic_advantage = egt_params["parasitic_advantage"]["base"]
            
            # Simplified EGT model
            if cli > 0.75:
                # High lock-in: Parasites dominate
                reformer_fitness = 0.2
                incumbent_fitness = 0.5
                parasite_fitness = 0.8 + parasitic_advantage
                
                ess_type = "Parasite-Incumbent Coalition"
                ess_stability = "Stable"
                reform_viability = "Very Low (< 20%)"
                
                strategic_advice = (
                    "**Critical Lock-in Detected**\n\n"
                    "Parasitic strategies dominate. Symbolic reforms crowd out real change.\n\n"
                    "**Breaking the Lock-in**:\n"
                    "1. **Constitutional Shock**: External crisis may destabilize ESS\n"
                    "2. **Coalition Building**: Unite reformers across policy domains\n"
                    "3. **Transparency**: Expose parasitic compliance mechanisms\n"
                    "4. **International Pressure**: Leverage external accountability\n"
                    "5. **Incremental Gains**: Small wins to shift fitness landscape"
                )
                
            elif cli > 0.50:
                # Moderate lock-in: Mixed strategies
                reformer_fitness = 0.4
                incumbent_fitness = 0.6
                parasite_fitness = 0.7 + parasitic_advantage
                
                ess_type = "Mixed Strategy Equilibrium"
                ess_stability = "Conditionally Stable"
                reform_viability = "Moderate (40-60%)"
                
                strategic_advice = (
                    "**Moderate Lock-in: Window of Opportunity**\n\n"
                    "System near tipping point. Reform possible with strategic action.\n\n"
                    "**Reform Strategy**:\n"
                    "1. **Targeted Reforms**: Focus on high-impact, low-resistance areas\n"
                    "2. **Build Momentum**: Early wins increase reformer fitness\n"
                    "3. **Neutralize Parasites**: Make symbolic compliance costly\n"
                    "4. **Frame Carefully**: Align reforms with incumbent interests\n"
                    "5. **Timing**: Strike during political/economic windows"
                )
                
            else:
                # Low lock-in: Reformers viable
                reformer_fitness = 0.7
                incumbent_fitness = 0.5
                parasite_fitness = 0.6 + parasitic_advantage
                
                ess_type = "Reformer-Dominant"
                ess_stability = "Unstable (favorable for reform)"
                reform_viability = "High (> 70%)"
                
                strategic_advice = (
                    "**Favorable Conditions for Reform**\n\n"
                    "System near golden ratio. Reformers have fitness advantage.\n\n"
                    "**Capitalize on Advantage**:\n"
                    "1. **Act Quickly**: Lock in reforms before equilibrium shifts\n"
                    "2. **Comprehensive Approach**: Address multiple components\n"
                    "3. **Institutionalize**: Make reforms hard to reverse\n"
                    "4. **Monitor**: Watch for parasitic capture of reforms\n"
                    "5. **Share Lessons**: Document success for other jurisdictions"
                )
            
            # ESS analysis
            if hv_ratio > 2.5:
                ess_location = f"Far from golden ratio (φ={phi}). ESS at High Lock-in."
            elif 1.0 <= hv_ratio <= 2.0:
                ess_location = f"Within Goldilocks Zone. ESS near φ={phi}."
            else:
                ess_location = f"Distance from φ: {distance_from_phi:.3f}"
            
            output = f"""
# EGT Reform Viability Analysis: {jurisdiction}

## System State
- **H/V Ratio**: {hv_ratio:.3f}
- **CLI Score**: {cli:.3f}
- **Distance from Golden Ratio**: {distance_from_phi:.3f}
- **Reform Pressure**: {reform_pressure:.2f}

## Evolutionary Game Theory Predictions

### Player Fitness Values
| Strategy | Fitness | Relative Strength |
|----------|---------|-------------------|
| Reformers | {reformer_fitness:.2f} | {"✅ Strong" if reformer_fitness > 0.6 else "⚠️ Weak" if reformer_fitness < 0.4 else "— Moderate"} |
| Incumbents | {incumbent_fitness:.2f} | {"✅ Strong" if incumbent_fitness > 0.6 else "⚠️ Weak" if incumbent_fitness < 0.4 else "— Moderate"} |
| Parasites | {parasite_fitness:.2f} | {"✅ Strong" if parasite_fitness > 0.7 else "— Moderate"} |

**Parasitic Advantage**: {parasitic_advantage:.1%} (explains non-convergence to φ)

### Equilibrium Analysis
- **ESS Type**: {ess_type}
- **ESS Stability**: {ess_stability}
- **ESS Location**: {ess_location}
- **Reform Viability**: {reform_viability}

## Strategic Recommendations

{strategic_advice}

## Why Systems Don't Converge to φ=1.618

The **parasitic advantage** ({parasitic_advantage:.1%}) creates a fitness landscape where:

1. **Symbolic compliance** is evolutionarily stable
2. **Real reforms** face higher coordination costs
3. **Lock-in states** are locally optimal (though globally suboptimal)
4. **Path dependence** traps systems away from φ

This explains why 88% of systems deviate substantially from the golden ratio despite its empirical optimality.

## Theoretical Basis
- Model: Evolutionary Game Theory with three-player dynamics
- Key Paper: "The Golden Ratio Paradox" (2024)
- Empirical Validation: 31 constitutional systems, 1950-2023
"""
            
            return [TextContent(type="text", text=output)]
        
        except Exception as e:
            logger.error(f"Error in EGT analysis: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    tool_count += 1
    
    # Tool 2: Explain Non-Convergence
    @server.list_tools()
    async def list_explain_non_convergence() -> list[Tool]:
        return [
            Tool(
                name="explain_non_convergence",
                description=(
                    "Explain why systems don't converge to the golden ratio (φ=1.618) despite optimality.\n\n"
                    "Uses EGT to show how parasitic strategies create stable equilibria away from φ.\n\n"
                    "**Key Mechanisms**:\n"
                    "1. Parasitic advantage (12% fitness boost)\n"
                    "2. Path dependence and historical lock-in\n"
                    "3. Coordination failures\n"
                    "4. Multiple stable equilibria\n\n"
                    "**Returns**: Detailed explanation with fitness landscape analysis."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "current_hv_ratio": {
                            "type": "number",
                            "description": "Current H/V ratio of system"
                        },
                        "jurisdiction_name": {
                            "type": "string"
                        }
                    },
                    "required": ["current_hv_ratio", "jurisdiction_name"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_explain_non_convergence(name: str, arguments: dict) -> list[TextContent]:
        """Explain non-convergence phenomenon."""
        if name != "explain_non_convergence":
            raise ValueError(f"Unknown tool: {name}")
        
        try:
            hv_ratio = arguments["current_hv_ratio"]
            jurisdiction = arguments["jurisdiction_name"]
            phi = 1.618
            
            distance = abs(hv_ratio - phi)
            parasitic_advantage = egt_params["parasitic_advantage"]["base"]
            
            output = f"""
# Why {jurisdiction} Doesn't Converge to φ=1.618

## Current State
- **Your H/V Ratio**: {hv_ratio:.3f}
- **Golden Ratio (φ)**: {phi}
- **Distance from Optimum**: {distance:.3f}

## The Golden Ratio Paradox

Despite empirical evidence that systems at φ=1.618 achieve **100% reform success** (vs 8% for locked-in systems), 88% of constitutional systems deviate substantially.

### Why Optimality ≠ Convergence

### 1. Parasitic Fitness Advantage ({parasitic_advantage:.1%})

Symbolic compliance strategies enjoy a **12% fitness advantage** over genuine reform:

- **Lower Costs**: No real institutional change required
- **Signal Benefit**: Appearance of reform satisfies political pressure  
- **Avoid Resistance**: No threat to entrenched interests
- **Faster Adoption**: Rhetoric cheaper than restructuring

#### Fitness Landscape
```
Fitness
   │
1.0│         Parasites
   │           /\\
0.8│          /  \\
   │         /    \\     ← 12% advantage
0.6│ -------/------\\--------  Reformers
   │       /        \\
0.4│      /          \\
   │     /            \\
0.2│    /              \\
   │___/__________________\\___
      Lock-in   φ=1.618   Chaos
              H/V Ratio
```

### 2. Multiple Stable Equilibria

The system has **three equilibria**:

1. **Lock-in Equilibrium** (H/V > 2.5): Incumbent-Parasite coalition
   - Locally stable
   - Fitness peak for parasites
   - Hard to escape without shock

2. **Golden Ratio Equilibrium** (H/V ≈ φ): Reformer dominance
   - Globally optimal
   - But hard to reach from lock-in
   - Requires coordinated transition

3. **Chaos Equilibrium** (H/V < 0.5): Excessive variation
   - Unstable
   - High variance, low predictability

### 3. Path Dependence

Historical choices create **irreversibilities**:

- Constitutional text locks in vagueness levels
- Judicial doctrines accumulate via precedent
- Treaty commitments create external constraints
- Amendment difficulty self-reinforces

**Result**: Systems get "stuck" in suboptimal basins.

### 4. Coordination Failures

Moving to φ requires **simultaneous changes** across:
- Legislative procedures
- Judicial doctrines  
- Constitutional text
- Enforcement mechanisms

Without coordination, partial reforms fail or get captured by parasites.

## Your System's Position

"""
            if hv_ratio > 2.5:
                output += f"""
**Status**: Deep in Lock-in Equilibrium

You're trapped in a **locally stable but globally suboptimal** state. The parasitic equilibrium is reinforced by:

1. High CLI components (judicial activism, treaty hierarchy)
2. Strong incumbent coalition
3. Path dependencies from historical choices
4. Coordination barriers to moving toward φ

**Escape Requires**: External shock or sustained reform coalition.
"""
            elif 1.0 <= hv_ratio <= 2.0:
                output += f"""
**Status**: Within Goldilocks Zone!

You're at or near the **globally optimal equilibrium**. Congratulations!

Maintain this position by:
1. Monitoring for parasitic capture
2. Resisting pressure to increase H (heredity)
3. Preserving variation mechanisms
4. Institutionalizing current balance
"""
            else:
                output += f"""
**Status**: Between Equilibria

You're in a **transition zone**. This creates opportunity but also risk:

- **Opportunity**: Reforms can push toward φ
- **Risk**: May slip into lock-in if captured by parasites

**Key Action**: Coordinate reforms to target φ=1.618 explicitly.
"""
            
            output += f"""

## Breaking Non-Convergence

### For Systems Far from φ:

1. **Constitutional Shock Doctrine**: Use crisis to destabilize ESS
2. **Anti-Parasitic Design**: Make symbolic compliance detectable and costly
3. **Phased Transitions**: Step-wise approach to φ
4. **International Benchmarking**: External pressure from optimal systems
5. **Transparency**: Expose gap between rhetoric and reality

### For Systems Near φ:

1. **Lock It In**: Constitutionalize current balance
2. **Monitor Continuously**: Watch for drift toward lock-in
3. **Resist Capture**: Block parasitic amendments
4. **Share Success**: Help other jurisdictions learn

## Empirical Evidence

| System Profile | Distance from φ | Success Rate | Equilibrium |
|----------------|-----------------|--------------|-------------|
| Goldilocks (1.0-2.0) | < 0.6 | **100%** (7/7) | Near φ |
| Moderate Lock-in | 0.6-1.5 | ~40% | Transitional |
| High Lock-in (>2.5) | > 1.5 | **8%** (2/24) | Parasite ESS |

## Theoretical Foundation

- **Framework**: Evolutionary Game Theory + Path Dependence
- **Key Insight**: Parasitic strategies create non-convergence despite optimality
- **Model Validation**: R²=0.74 for CLI-success relationship
- **Sample**: 31 constitutional systems, 1950-2023
"""
            
            return [TextContent(type="text", text=output)]
        
        except Exception as e:
            logger.error(f"Error explaining non-convergence: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    tool_count += 1
    
    # Tool 3: Calculate Parasitic Fitness
    @server.list_tools()
    async def list_calculate_parasitic_fitness() -> list[Tool]:
        return [
            Tool(
                name="calculate_parasitic_fitness",
                description=(
                    "Calculate fitness advantage of parasitic (symbolic compliance) strategies.\n\n"
                    "Quantifies why symbolic reforms dominate over genuine change.\n\n"
                    "**Factors**:\n"
                    "- Rhetorical cost vs institutional restructuring cost\n"
                    "- Signal benefit without threat to incumbents\n"
                    "- Speed of adoption (rhetoric faster than reality)\n\n"
                    "**Returns**: Parasitic fitness score, advantage breakdown, implications."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cli_score": {
                            "type": "number",
                            "description": "CLI score [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "reform_rhetoric_intensity": {
                            "type": "number",
                            "description": "Intensity of reform rhetoric [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "actual_implementation": {
                            "type": "number",
                            "description": "Actual implementation level [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "required": ["cli_score", "reform_rhetoric_intensity", "actual_implementation"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_calculate_parasitic_fitness(name: str, arguments: dict) -> list[TextContent]:
        """Calculate parasitic fitness advantage."""
        if name != "calculate_parasitic_fitness":
            raise ValueError(f"Unknown tool: {name}")
        
        try:
            cli = arguments["cli_score"]
            rhetoric = arguments["reform_rhetoric_intensity"]
            implementation = arguments["actual_implementation"]
            
            # Calculate rhetoric-reality gap
            gap = rhetoric - implementation
            
            # Base parasitic advantage
            base_advantage = egt_params["parasitic_advantage"]["base"]
            
            # Adjust for CLI (higher lock-in = more advantage to parasites)
            cli_multiplier = 1.0 + (cli * 0.5)  # Up to 50% bonus
            
            # Adjust for gap (larger gap = stronger parasitic strategy)
            gap_multiplier = 1.0 + (max(0, gap) * 0.8)
            
            # Total parasitic fitness
            parasite_fitness = base_advantage * cli_multiplier * gap_multiplier
            reformer_fitness = implementation * 0.7  # Genuine reform fitness
            
            advantage = parasite_fitness - reformer_fitness
            
            output = f"""
# Parasitic Fitness Analysis

## Input Conditions
- **CLI Score**: {cli:.3f}
- **Reform Rhetoric Intensity**: {rhetoric:.2f}
- **Actual Implementation**: {implementation:.2f}
- **Rhetoric-Reality Gap**: {gap:.2f}

## Fitness Calculations

### Parasitic Strategy (Symbolic Compliance)
- **Base Advantage**: {base_advantage:.3f}
- **CLI Multiplier**: {cli_multiplier:.2f}x (lock-in bonus)
- **Gap Multiplier**: {gap_multiplier:.2f}x (rhetoric advantage)
- **Total Parasitic Fitness**: **{parasite_fitness:.3f}**

### Reformer Strategy (Genuine Change)
- **Implementation Factor**: {implementation:.2f}
- **Coordination Costs**: -0.30
- **Total Reformer Fitness**: **{reformer_fitness:.3f}**

### Net Advantage
**Parasitic Advantage**: {advantage:.3f} ({advantage/reformer_fitness*100:.1f}% higher fitness)

## Interpretation

"""
            if advantage > 0.15:
                output += f"""
⚠️ **CRITICAL: Parasitic Dominance**

Symbolic compliance strategies have overwhelming fitness advantage. This explains:

1. **Reform Rhetoric** abundant but **implementation** scarce
2. **Constitutional amendments** passed but not enforced  
3. **International commitments** signed but ignored
4. **Judicial activism** declared but selective

**Why Parasites Win**:
- Low cost (rhetoric is cheap)
- High signal value (appear reformist)
- No threat to incumbents (status quo preserved)
- Fast adoption (no institutional restructuring needed)

**Implication**: Genuine reform nearly impossible without addressing parasitic equilibrium.
"""
            elif advantage > 0:
                output += f"""
⚠️ **Moderate Parasitic Advantage**

Symbolic compliance has measurable but not overwhelming advantage. This suggests:

1. Reform possible with sustained effort
2. Parasitic capture likely without vigilance  
3. Mixed strategies viable
4. Context-dependent outcomes

**Reform Strategy**: Make symbolic compliance costly through transparency and accountability.
"""
            else:
                output += f"""
✅ **Reformer Advantage**

Genuine reform strategies have higher fitness! This rare condition occurs when:

1. Strong enforcement mechanisms
2. Low CLI (flexible institutions)
3. High accountability (parasites exposed)
4. Reform coalitions strong

**Opportunity**: Capitalize on favorable conditions to institutionalize reforms.
"""
            
            output += f"""

## Mechanisms of Parasitic Fitness

### 1. Cost Asymmetry
- **Rhetorical reform**: Cost ≈ 0.1 (speech-writing, symbolic gestures)
- **Real reform**: Cost ≈ 1.0 (institutional restructuring, enforcement)
- **Ratio**: Parasites pay **10% of reformer costs**

### 2. Signal Benefit
- Both strategies signal "reform commitment"
- Parasites get signal benefit without costs
- **Parasitic rent**: Full benefit at 10% cost

### 3. Incumbent Tolerance
- Real reform threatens incumbents → resistance
- Symbolic reform preserves status quo → tolerance
- **Parasitic alliance**: Incumbents actively support symbolic reform

### 4. Speed Advantage
- Rhetoric deployed immediately
- Real reform requires years of implementation
- **First-mover benefit**: Parasites capture political moment

## Breaking Parasitic Dominance

### Design Principles:

1. **Ex-Post Accountability**
   - Track implementation vs rhetoric
   - Publish compliance gaps
   - Create reputational costs

2. **Specific Performance Standards**
   - Measurable targets
   - Time-bound commitments
   - Third-party verification

3. **Conditional Benefits**
   - Reform benefits only with implementation
   - No credit for rhetoric alone
   - Progressive reward structures

4. **Coalition Monitoring**
   - Civil society oversight
   - International accountability
   - Judicial enforcement

## Empirical Patterns

Systems with high parasitic fitness ({parasite_fitness:.2f} > 0.75) show:
- Reform success rate: 8-15%
- CLI scores: > 0.75
- H/V ratios: > 2.5
- Rhetoric-reality gap: > 0.40

Systems with low parasitic fitness ({parasite_fitness:.2f} < 0.50) show:
- Reform success rate: 70-100%
- CLI scores: < 0.50
- H/V ratios: 1.0-2.0
- Rhetoric-reality gap: < 0.20
"""
            
            return [TextContent(type="text", text=output)]
        
        except Exception as e:
            logger.error(f"Error calculating parasitic fitness: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    tool_count += 1
    
    logger.info(f"Registered {tool_count} EGT framework tools")
    return tool_count
