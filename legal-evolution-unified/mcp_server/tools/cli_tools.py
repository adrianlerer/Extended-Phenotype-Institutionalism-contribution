"""
CLI Calculator Tools
====================

MCP tools for Constitutional Lock-in Index calculation and analysis.

Tools:
1. calculate_cli_score - CLI + success prediction + recommendations
2. analyze_jurisdiction_complete - Complete CLI analysis with benchmarks
3. compare_multiple_jurisdictions - Batch jurisdiction comparison
4. calculate_hv_ratio - H/V ratio from constitutional components
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.types import Tool, TextContent

from src.metrics.cli_calculator import (
    calculate_cli,
    predict_reform_success_from_cli,
    calculate_h_v_from_components,
    integrated_analysis,
    compare_jurisdictions,
    BENCHMARK_JURISDICTIONS,
    CLIComponents
)


def register_cli_tools(server, config, cache, logger: logging.Logger) -> int:
    """
    Register CLI calculator tools with the MCP server.
    
    Args:
        server: MCP server instance
        config: Server configuration
        cache: Cache manager
        logger: Logger instance
    
    Returns:
        Number of tools registered
    """
    tool_count = 0
    
    # Tool 1: Calculate CLI Score
    @server.list_tools()
    async def list_calculate_cli_score() -> list[Tool]:
        return [
            Tool(
                name="calculate_cli_score",
                description=(
                    "Calculate Constitutional Lock-in Index (CLI) from 5 components and predict reform success.\n\n"
                    "**Formula**: CLI = 0.25×text_vagueness + 0.25×judicial_activism + 0.20×treaty_hierarchy + "
                    "0.15×precedent_weight + 0.15×amendment_difficulty\n\n"
                    "**Empirical Model**: Reform_Success = 0.92 - 0.89×CLI (R²=0.74, p<0.001)\n\n"
                    "**Returns**: CLI score [0,1], success probability, classification, component breakdown, "
                    "and actionable recommendations.\n\n"
                    "**Example**: calculate_cli_score(0.75, 0.95, 0.88, 0.85, 0.70) → CLI=0.826, "
                    "Success=18.5%, Classification='High Lock-in'"
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text_vagueness": {
                            "type": "number",
                            "description": "Text vagueness [0,1]: Higher = more ambiguous constitutional text",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "judicial_activism": {
                            "type": "number",
                            "description": "Judicial activism [0,1]: Higher = more active judicial review",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "treaty_hierarchy": {
                            "type": "number",
                            "description": "Treaty hierarchy [0,1]: Higher = treaties more binding",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "precedent_weight": {
                            "type": "number",
                            "description": "Precedent weight [0,1]: Higher = stronger stare decisis",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "amendment_difficulty": {
                            "type": "number",
                            "description": "Amendment difficulty [0,1]: Higher = harder to amend",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "jurisdiction_name": {
                            "type": "string",
                            "description": "Optional name of jurisdiction for reporting"
                        }
                    },
                    "required": [
                        "text_vagueness",
                        "judicial_activism",
                        "treaty_hierarchy",
                        "precedent_weight",
                        "amendment_difficulty"
                    ]
                }
            )
        ]
    
    @server.call_tool()
    async def call_calculate_cli_score(name: str, arguments: dict) -> list[TextContent]:
        """Execute CLI calculation."""
        if name != "calculate_cli_score":
            raise ValueError(f"Unknown tool: {name}")
        
        # Check cache
        cache_key = f"cli_score_{hash(frozenset(arguments.items()))}"
        if cached := cache.get("cli_tools", cache_key):
            logger.debug(f"Cache hit for {cache_key}")
            return [TextContent(type="text", text=str(cached))]
        
        try:
            # Extract components
            tv = arguments["text_vagueness"]
            ja = arguments["judicial_activism"]
            th = arguments["treaty_hierarchy"]
            pw = arguments["precedent_weight"]
            ad = arguments["amendment_difficulty"]
            jurisdiction = arguments.get("jurisdiction_name", "Unknown")
            
            # Calculate CLI
            cli = calculate_cli(tv, ja, th, pw, ad)
            
            # Get detailed components
            components = calculate_cli(tv, ja, th, pw, ad, return_components=True)
            
            # Predict reform success
            prediction = predict_reform_success_from_cli(cli)
            
            # Classify lock-in level
            if cli > 0.75:
                classification = "High Lock-in"
                risk_level = "Critical"
                recommendation = (
                    "Constitutional intervention required. System shows severe rigidity. "
                    "Reform success probability < 20%. Consider:\n"
                    "1. Targeted constitutional amendments to reduce ambiguity\n"
                    "2. Establish clear amendment procedures\n"
                    "3. Limit judicial discretion via explicit textual constraints\n"
                    "4. Review and potentially lower treaty hierarchy"
                )
            elif cli > 0.50:
                classification = "Moderate Lock-in"
                risk_level = "High"
                recommendation = (
                    "System trending toward rigidity. Reform success 20-50%. Actions:\n"
                    "1. Monitor judicial activism trends\n"
                    "2. Clarify constitutional text in key areas\n"
                    "3. Review treaty obligations for conflicts\n"
                    "4. Consider procedural reforms to ease amendments"
                )
            elif cli > 0.25:
                classification = "Low Lock-in"
                risk_level = "Moderate"
                recommendation = (
                    "System relatively flexible. Reform success 50-70%. Maintain:\n"
                    "1. Current balance of judicial review\n"
                    "2. Constitutional clarity where possible\n"
                    "3. Reasonable amendment procedures\n"
                    "4. Monitor for early warning signs of rigidity"
                )
            else:
                classification = "Goldilocks Zone"
                risk_level = "Low"
                recommendation = (
                    "Optimal flexibility! Reform success > 70%. Best practices:\n"
                    "1. Maintain constitutional clarity\n"
                    "2. Preserve balanced judicial review\n"
                    "3. Keep amendment procedures accessible but not trivial\n"
                    "4. Share institutional design lessons with other jurisdictions"
                )
            
            # Build result
            result = {
                "jurisdiction": jurisdiction,
                "cli_score": round(cli, 3),
                "reform_success_probability": f"{prediction:.1f}%",
                "classification": classification,
                "risk_level": risk_level,
                "components": {
                    "text_vagueness": round(tv, 3),
                    "judicial_activism": round(ja, 3),
                    "treaty_hierarchy": round(th, 3),
                    "precedent_weight": round(pw, 3),
                    "amendment_difficulty": round(ad, 3)
                },
                "weighted_contributions": {
                    "text_vagueness": round(0.25 * tv, 3),
                    "judicial_activism": round(0.25 * ja, 3),
                    "treaty_hierarchy": round(0.20 * th, 3),
                    "precedent_weight": round(0.15 * pw, 3),
                    "amendment_difficulty": round(0.15 * ad, 3)
                },
                "recommendation": recommendation,
                "empirical_basis": "Model: Reform_Success = 0.92 - 0.89×CLI (R²=0.74, p<0.001)"
            }
            
            # Cache result
            cache.set("cli_tools", cache_key, result)
            
            # Format output
            output = f"""
# CLI Analysis for {jurisdiction}

## Key Metrics
- **CLI Score**: {result['cli_score']} ({classification})
- **Reform Success Probability**: {result['reform_success_probability']}
- **Risk Level**: {risk_level}

## Component Breakdown
| Component | Value | Weighted Contribution |
|-----------|-------|----------------------|
| Text Vagueness | {result['components']['text_vagueness']} | {result['weighted_contributions']['text_vagueness']} |
| Judicial Activism | {result['components']['judicial_activism']} | {result['weighted_contributions']['judicial_activism']} |
| Treaty Hierarchy | {result['components']['treaty_hierarchy']} | {result['weighted_contributions']['treaty_hierarchy']} |
| Precedent Weight | {result['components']['precedent_weight']} | {result['weighted_contributions']['precedent_weight']} |
| Amendment Difficulty | {result['components']['amendment_difficulty']} | {result['weighted_contributions']['amendment_difficulty']} |

## Recommendations
{recommendation}

## Empirical Basis
{result['empirical_basis']}
"""
            
            return [TextContent(type="text", text=output)]
        
        except Exception as e:
            logger.error(f"Error calculating CLI score: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    tool_count += 1
    
    # Tool 2: Calculate H/V Ratio
    @server.list_tools()
    async def list_calculate_hv_ratio() -> list[Tool]:
        return [
            Tool(
                name="calculate_hv_ratio",
                description=(
                    "Calculate H/V (Heredity/Variation) ratio from constitutional components.\n\n"
                    "**Formula**:\n"
                    "- H (Heredity) = 0.25×(precedent + rigidity + codification + tenure)\n"
                    "- V (Variation) = 0.25×(federalism + amendment_freq + review + turnover)\n"
                    "- H/V Ratio = H / V\n\n"
                    "**Optimal Range**: 1.0 - 2.0 (Goldilocks Zone)\n"
                    "**Golden Ratio**: φ ≈ 1.618\n"
                    "**Lock-in Threshold**: > 2.5\n\n"
                    "**Returns**: H, V, H/V ratio, classification, and evolutionary assessment."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "precedent": {
                            "type": "number",
                            "description": "Precedent strength [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "rigidity": {
                            "type": "number",
                            "description": "Constitutional rigidity [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "codification": {
                            "type": "number",
                            "description": "Codification level [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "tenure": {
                            "type": "number",
                            "description": "Judicial tenure [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "federalism": {
                            "type": "number",
                            "description": "Federalism degree [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "amendment_freq": {
                            "type": "number",
                            "description": "Amendment frequency [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "review": {
                            "type": "number",
                            "description": "Judicial review scope [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "turnover": {
                            "type": "number",
                            "description": "Judicial turnover rate [0,1]",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "jurisdiction_name": {
                            "type": "string",
                            "description": "Optional jurisdiction name"
                        }
                    },
                    "required": [
                        "precedent", "rigidity", "codification", "tenure",
                        "federalism", "amendment_freq", "review", "turnover"
                    ]
                }
            )
        ]
    
    @server.call_tool()
    async def call_calculate_hv_ratio(name: str, arguments: dict) -> list[TextContent]:
        """Execute H/V ratio calculation."""
        if name != "calculate_hv_ratio":
            raise ValueError(f"Unknown tool: {name}")
        
        # Check cache
        cache_key = f"hv_ratio_{hash(frozenset(arguments.items()))}"
        if cached := cache.get("cli_tools", cache_key):
            logger.debug(f"Cache hit for {cache_key}")
            return [TextContent(type="text", text=str(cached))]
        
        try:
            # Calculate H/V
            H, V, hv_ratio = calculate_h_v_from_components(
                precedent=arguments["precedent"],
                rigidity=arguments["rigidity"],
                codification=arguments["codification"],
                tenure=arguments["tenure"],
                federalism=arguments["federalism"],
                amendment_freq=arguments["amendment_freq"],
                review=arguments["review"],
                turnover=arguments["turnover"]
            )
            
            jurisdiction = arguments.get("jurisdiction_name", "Unknown")
            
            # Classify system
            phi = 1.618
            if 1.0 <= hv_ratio <= 2.0:
                classification = "Goldilocks Zone"
                assessment = "OPTIMAL - System balances heredity and variation near golden ratio"
                success_rate = "100% (7/7 cases)"
            elif hv_ratio > 2.5:
                classification = "High Lock-in"
                assessment = "CRITICAL - Excessive heredity inhibits institutional evolution"
                success_rate = "8% (2/24 cases)"
            elif hv_ratio > 2.0:
                classification = "Moderate Lock-in"
                assessment = "WARNING - System trending toward excessive rigidity"
                success_rate = "~40% (estimated)"
            else:
                classification = "High Variation"
                assessment = "UNSTABLE - Excessive variation may reduce institutional stability"
                success_rate = "~60% (estimated)"
            
            distance_from_phi = abs(hv_ratio - phi)
            
            result = {
                "jurisdiction": jurisdiction,
                "heredity": round(H, 3),
                "variation": round(V, 3),
                "hv_ratio": round(hv_ratio, 3),
                "distance_from_golden_ratio": round(distance_from_phi, 3),
                "classification": classification,
                "assessment": assessment,
                "historical_success_rate": success_rate,
                "golden_ratio": phi
            }
            
            # Cache result
            cache.set("cli_tools", cache_key, result)
            
            # Format output
            output = f"""
# H/V Ratio Analysis for {jurisdiction}

## Key Metrics
- **Heredity (H)**: {result['heredity']}
- **Variation (V)**: {result['variation']}
- **H/V Ratio**: {result['hv_ratio']} ({classification})
- **Distance from φ (1.618)**: {result['distance_from_golden_ratio']}

## Classification
**{classification}**

{assessment}

## Historical Context
- **Success Rate for This Profile**: {success_rate}
- **Golden Ratio (φ)**: {phi}
- **Optimal Range**: 1.0 - 2.0

## Evolutionary Analysis
Systems in the Goldilocks Zone (H/V ≈ φ) exhibit:
- 100% reform success rate
- Optimal balance of stability and adaptability
- Sustainable institutional evolution

Systems with H/V > 2.5 show:
- 8% reform success rate
- Constitutional lock-in
- Resistance to beneficial change
"""
            
            return [TextContent(type="text", text=output)]
        
        except Exception as e:
            logger.error(f"Error calculating H/V ratio: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    tool_count += 1
    
    # Tool 3: Compare Multiple Jurisdictions
    @server.list_tools()
    async def list_compare_jurisdictions() -> list[Tool]:
        return [
            Tool(
                name="compare_multiple_jurisdictions",
                description=(
                    "Compare CLI scores and reform success predictions across multiple jurisdictions.\n\n"
                    "Performs batch analysis and ranking. Useful for:\n"
                    "- Regional comparisons\n"
                    "- Identifying best/worst practices\n"
                    "- Reform prioritization\n\n"
                    "**Returns**: Comparative table, rankings, and insights."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "jurisdictions": {
                            "type": "array",
                            "description": "List of jurisdictions to compare",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "text_vagueness": {"type": "number", "minimum": 0, "maximum": 1},
                                    "judicial_activism": {"type": "number", "minimum": 0, "maximum": 1},
                                    "treaty_hierarchy": {"type": "number", "minimum": 0, "maximum": 1},
                                    "precedent_weight": {"type": "number", "minimum": 0, "maximum": 1},
                                    "amendment_difficulty": {"type": "number", "minimum": 0, "maximum": 1}
                                },
                                "required": ["name", "text_vagueness", "judicial_activism", 
                                           "treaty_hierarchy", "precedent_weight", "amendment_difficulty"]
                            },
                            "minItems": 2
                        }
                    },
                    "required": ["jurisdictions"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_compare_jurisdictions(name: str, arguments: dict) -> list[TextContent]:
        """Execute multi-jurisdiction comparison."""
        if name != "compare_multiple_jurisdictions":
            raise ValueError(f"Unknown tool: {name}")
        
        try:
            jurisdictions = arguments["jurisdictions"]
            results = []
            
            for j in jurisdictions:
                cli = calculate_cli(
                    j["text_vagueness"],
                    j["judicial_activism"],
                    j["treaty_hierarchy"],
                    j["precedent_weight"],
                    j["amendment_difficulty"]
                )
                prediction = predict_reform_success_from_cli(cli)
                
                if cli > 0.75:
                    classification = "High Lock-in"
                elif cli > 0.50:
                    classification = "Moderate Lock-in"
                elif cli > 0.25:
                    classification = "Low Lock-in"
                else:
                    classification = "Goldilocks Zone"
                
                results.append({
                    "name": j["name"],
                    "cli": round(cli, 3),
                    "success_prob": round(prediction, 1),
                    "classification": classification
                })
            
            # Sort by CLI (ascending = better)
            results_sorted = sorted(results, key=lambda x: x["cli"])
            
            # Format output
            output = "# Multi-Jurisdiction Comparison\n\n## Rankings (Best to Worst)\n\n"
            output += "| Rank | Jurisdiction | CLI Score | Success Prob | Classification |\n"
            output += "|------|--------------|-----------|--------------|----------------|\n"
            
            for idx, r in enumerate(results_sorted, 1):
                emoji = "🏆" if idx == 1 else "⚠️" if idx == len(results_sorted) else "—"
                output += f"| {emoji} #{idx} | {r['name']} | {r['cli']} | {r['success_prob']}% | {r['classification']} |\n"
            
            output += "\n## Key Insights\n\n"
            best = results_sorted[0]
            worst = results_sorted[-1]
            
            output += f"- **Best**: {best['name']} (CLI={best['cli']}, {best['success_prob']}% success)\n"
            output += f"- **Worst**: {worst['name']} (CLI={worst['cli']}, {worst['success_prob']}% success)\n"
            output += f"- **CLI Range**: {worst['cli'] - best['cli']:.3f}\n"
            output += f"- **Success Gap**: {best['success_prob'] - worst['success_prob']:.1f} percentage points\n"
            
            return [TextContent(type="text", text=output)]
        
        except Exception as e:
            logger.error(f"Error comparing jurisdictions: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    tool_count += 1
    
    # Tool 4: Analyze Jurisdiction Complete (with benchmarks)
    @server.list_tools()
    async def list_analyze_jurisdiction_complete() -> list[Tool]:
        return [
            Tool(
                name="analyze_jurisdiction_complete",
                description=(
                    "Complete CLI analysis with benchmark comparisons.\n\n"
                    "Performs full analysis and compares against historical benchmarks:\n"
                    "- Argentina (CLI=0.826, High Lock-in)\n"
                    "- Brazil (CLI=0.485, Goldilocks)\n"
                    "- Spain (CLI=0.520, Moderate Lock-in)\n"
                    "- USA (CLI=0.620, Moderate Lock-in)\n\n"
                    "**Returns**: Complete analysis + contextual benchmarking."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "jurisdiction_name": {"type": "string"},
                        "text_vagueness": {"type": "number", "minimum": 0, "maximum": 1},
                        "judicial_activism": {"type": "number", "minimum": 0, "maximum": 1},
                        "treaty_hierarchy": {"type": "number", "minimum": 0, "maximum": 1},
                        "precedent_weight": {"type": "number", "minimum": 0, "maximum": 1},
                        "amendment_difficulty": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "required": ["jurisdiction_name", "text_vagueness", "judicial_activism",
                               "treaty_hierarchy", "precedent_weight", "amendment_difficulty"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_analyze_jurisdiction_complete(name: str, arguments: dict) -> list[TextContent]:
        """Execute complete jurisdiction analysis with benchmarks."""
        if name != "analyze_jurisdiction_complete":
            raise ValueError(f"Unknown tool: {name}")
        
        try:
            # First get basic CLI analysis
            cli_args = {k: v for k, v in arguments.items() if k != "jurisdiction_name"}
            cli_args["jurisdiction_name"] = arguments["jurisdiction_name"]
            
            basic_analysis = await call_calculate_cli_score("calculate_cli_score", cli_args)
            
            # Add benchmark comparison
            cli = calculate_cli(**{k: v for k, v in cli_args.items() if k != "jurisdiction_name"})
            
            benchmarks = [
                ("Argentina", 0.826, "High Lock-in"),
                ("Brazil", 0.485, "Goldilocks Zone"),
                ("Spain", 0.520, "Moderate Lock-in"),
                ("USA", 0.620, "Moderate Lock-in")
            ]
            
            closest = min(benchmarks, key=lambda b: abs(b[1] - cli))
            
            benchmark_section = f"""
## Benchmark Comparison

Your jurisdiction's CLI ({cli:.3f}) is closest to **{closest[0]}** (CLI={closest[1]}, {closest[2]}).

| Benchmark | CLI | Classification | Distance |
|-----------|-----|----------------|----------|
"""
            for b_name, b_cli, b_class in benchmarks:
                distance = abs(cli - b_cli)
                marker = "👉" if b_name == closest[0] else "  "
                benchmark_section += f"| {marker} {b_name} | {b_cli} | {b_class} | {distance:.3f} |\n"
            
            # Combine outputs
            output = basic_analysis[0].text + benchmark_section
            
            return [TextContent(type="text", text=output)]
        
        except Exception as e:
            logger.error(f"Error in complete analysis: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    tool_count += 1
    
    logger.info(f"Registered {tool_count} CLI calculator tools")
    return tool_count
