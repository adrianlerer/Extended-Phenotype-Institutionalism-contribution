"""
Feature Registry System
Manages all research tools with enable/disable capabilities
SaaS-ready with usage tracking and feature descriptions
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json
from pathlib import Path
from datetime import datetime


class FeatureCategory(Enum):
    """Feature categories for organization"""
    ANALYSIS = "analysis"
    GENERATION = "generation"
    VISUALIZATION = "visualization"
    CALCULATION = "calculation"
    AI_ASSISTANT = "ai_assistant"
    METHODOLOGY = "methodology"


@dataclass
class Feature:
    """Feature/Tool definition"""
    id: str
    name: str
    description: str
    category: FeatureCategory
    enabled: bool = True
    icon: str = "🔧"
    version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)
    endpoint: Optional[str] = None
    saas_tier: str = "free"  # free, basic, pro, enterprise
    usage_count: int = 0
    last_used: Optional[str] = None
    documentation_url: Optional[str] = None
    examples: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "enabled": self.enabled,
            "icon": self.icon,
            "version": self.version,
            "dependencies": self.dependencies,
            "endpoint": self.endpoint,
            "saas_tier": self.saas_tier,
            "usage_count": self.usage_count,
            "last_used": self.last_used,
            "documentation_url": self.documentation_url,
            "examples": self.examples
        }


class FeatureRegistry:
    """
    Central registry for all research tools
    Manages feature availability, usage tracking, and SaaS tiers
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.features: Dict[str, Feature] = {}
        self.config_path = config_path or Path("config/features.json")
        self._initialize_features()
        self._load_config()
    
    def _initialize_features(self):
        """Initialize all available features"""
        
        # ANALYSIS TOOLS
        self.register(Feature(
            id="cli_calculator",
            name="Constitutional Lock-In Calculator",
            description="Calculate CLI (Constitutional Lock-In Index) using formula: CLI = 0.35×CE + 0.40×UA + 0.25×JPI. Measure constitutional rigidity for research, policy assessment, legal strategy, political analysis, and investment risk scoring.",
            category=FeatureCategory.CALCULATION,
            icon="📊",
            endpoint="/api/cli/calculate",
            saas_tier="free",
            documentation_url="/docs/cli-calculator",
            examples=[
                {"input": "CE=0.80, UA=0.85, JPI=0.55", "output": "CLI=0.76 (High rigidity - use for political risk analysis)"},
                {"input": "CE=0.65, UA=0.35, JPI=0.70", "output": "CLI=0.54 (Moderate flexibility - good for reform planning)"}
            ]
        ))
        
        self.register(Feature(
            id="cli_cultural_calculator",
            name="Cultural Lock-In Calculator",
            description="Calculate CLI_cultural using formula: CLI_cultural = 0.40×CT1 + 0.30×CT2 + 0.30×CT3. Measures cultural transmission strength via narrative stability, shock resistance, and policy continuity.",
            category=FeatureCategory.CALCULATION,
            icon="🏛️",
            endpoint="/api/cli/calculate-cultural",
            saas_tier="free",
            documentation_url="/docs/cli-cultural",
            examples=[
                {"input": "CT1=0.40, CT2=0.25, CT3=0.35", "output": "CLI_cultural=0.34 (Weak transmission)"},
                {"input": "CT1=0.70, CT2=0.65, CT3=0.75", "output": "CLI_cultural=0.70 (Strong transmission)"}
            ]
        ))
        
        self.register(Feature(
            id="dual_index_analyzer",
            name="Dual-Index Framework Analyzer",
            description="Analyze CLI × CLI_cultural interaction to classify institutional profiles: Stable Rigidity, Brittle Rigidity, Adaptive Stability, or Chaotic Fragility. Identifies collapse risk (threshold < 0.30).",
            category=FeatureCategory.ANALYSIS,
            icon="🎯",
            endpoint="/api/cli/dual-index",
            saas_tier="basic",
            dependencies=["cli_calculator", "cli_cultural_calculator"],
            documentation_url="/docs/dual-index-framework",
            examples=[
                {"input": "Somalia: CLI=0.76, CLI_cultural=0.34", "output": "Brittle Rigidity (Interaction=0.26, HIGH RISK)"},
                {"input": "Somalilandia: CLI=0.54, CLI_cultural=0.70", "output": "Adaptive Stability (Interaction=0.38, LOW RISK)"}
            ]
        ))
        
        self.register(Feature(
            id="rootfinder",
            name="Constitutional Rootfinder",
            description="Trace constitutional genealogy and identify origin clauses. For legal litigation (historical arguments), policy reform (identify stable provisions), journalism (timeline graphics), and government consulting (borrowable provisions from successful constitutions).",
            category=FeatureCategory.METHODOLOGY,
            icon="🌳",
            endpoint="/api/methodology/rootfinder",
            saas_tier="pro",
            documentation_url="/docs/rootfinder",
            examples=[
                {"input": "Art. 14 Argentine Constitution (2025)", "output": "Root: 1853, unchanged 172 years (strong legal precedent for litigation)"},
                {"input": "Freedom of expression clause", "output": "Genealogy: 1853 → 1949 → 1994 (use for reform proposals)"}
            ]
        ))
        
        # GENERATION TOOLS
        self.register(Feature(
            id="paper_builder",
            name="Professional Document Builder",
            description="Auto-generate professional documents: academic papers (SSRN/journals), policy reports (World Bank/think tanks), legal briefs (constitutional analysis), investigative journalism (long-form reports), government white papers, and investment risk reports.",
            category=FeatureCategory.GENERATION,
            icon="📄",
            endpoint="/api/papers/build",
            saas_tier="basic",
            documentation_url="/docs/paper-builder",
            examples=[
                {"input": "Academic paper", "output": "SSRN-ready manuscript, 18,000 words"},
                {"input": "Policy brief", "output": "Executive summary + full report for donors/government"}
            ]
        ))
        
        self.register(Feature(
            id="appendix_generator",
            name="Methodology Appendix Generator",
            description="Generate detailed methodology appendices (e.g., Appendix D: CLI_cultural methodology). Includes formulas, data sources, validation procedures, and limitations.",
            category=FeatureCategory.GENERATION,
            icon="📚",
            endpoint="/api/papers/appendix",
            saas_tier="free",
            dependencies=["paper_builder"],
            documentation_url="/docs/appendix-generator"
        ))
        
        # VISUALIZATION TOOLS
        self.register(Feature(
            id="cli_matrix_visualizer",
            name="CLI Matrix Visualizer",
            description="Generate CLI × CLI_cultural interaction matrix with quadrant visualization. Shows collapse risk threshold (hyperbola), country positions, and risk zones. Publication-quality 300 DPI output.",
            category=FeatureCategory.VISUALIZATION,
            icon="📈",
            endpoint="/api/figures/cli-matrix",
            saas_tier="free",
            dependencies=["dual_index_analyzer"],
            documentation_url="/docs/cli-matrix",
            examples=[
                {"input": "5 countries (Somalia, Somalilandia, Uruguay, Chile, Argentina)", "output": "Figure 3: Dual-Index Matrix (649 KB, 300 DPI PNG)"}
            ]
        ))
        
        self.register(Feature(
            id="timeline_generator",
            name="Constitutional Timeline Generator",
            description="Create timeline visualizations of constitutional events (independence, reforms, crises). Ideal for natural experiments and historical analysis.",
            category=FeatureCategory.VISUALIZATION,
            icon="📅",
            endpoint="/api/figures/timeline",
            saas_tier="free",
            documentation_url="/docs/timeline-generator",
            examples=[
                {"input": "Somalia 1960-2025", "output": "Figure 1: Natural experiment timeline (618 KB)"}
            ]
        ))
        
        self.register(Feature(
            id="correlation_plotter",
            name="CLI Correlation Plotter",
            description="Generate scatterplots showing CLI correlations with governance outcomes (Freedom House scores, conflict intensity, GDP). Statistical validation included.",
            category=FeatureCategory.VISUALIZATION,
            icon="📉",
            endpoint="/api/figures/correlations",
            saas_tier="basic",
            dependencies=["cli_calculator"],
            documentation_url="/docs/correlation-plotter",
            examples=[
                {"input": "CLI vs Freedom House", "output": "Figure 2: Negative correlation (r=-0.67, p<0.01)"}
            ]
        ))
        
        # AI ASSISTANT TOOLS
        self.register(Feature(
            id="genspark_assistant",
            name="Genspark Research Assistant",
            description="AI-powered chat interface for methodology queries. Ask about formulas, data sources, interpretation guidelines. Context-aware responses with citations.",
            category=FeatureCategory.AI_ASSISTANT,
            icon="🤖",
            endpoint="/api/chat/query",
            saas_tier="free",
            documentation_url="/docs/ai-assistant",
            examples=[
                {"input": "How is CLI_cultural calculated?", "output": "CLI_cultural = 0.40×CT1 + 0.30×CT2 + 0.30×CT3 (Source: Appendix D)"},
                {"input": "What data sources for CT1?", "output": "Constitutional preambles, World Values Survey, Afrobarometer..."}
            ]
        ))
        
        self.register(Feature(
            id="code_reviewer",
            name="AI Code Reviewer",
            description="Automated code review for statistical correctness. Verifies CLI formulas, data validation, and reproducibility. Runs on every PR.",
            category=FeatureCategory.AI_ASSISTANT,
            icon="🔍",
            endpoint="/api/review/code",
            saas_tier="basic",
            documentation_url="/docs/code-reviewer",
            examples=[
                {"input": "generate_cli.py", "output": "✅ Formula correct. ⚠️ Missing input validation for CT1 range."}
            ]
        ))
        
        self.register(Feature(
            id="root_cause_analyzer",
            name="AI Root Cause Analyzer",
            description="Automated error analysis using AI. Explains data divergences, calculation anomalies, and build failures. Suggests fixes.",
            category=FeatureCategory.AI_ASSISTANT,
            icon="🔧",
            endpoint="/api/analyze/error",
            saas_tier="pro",
            documentation_url="/docs/root-cause-analyzer",
            examples=[
                {"input": "CLI_cultural = 1.34 (out of range)", "output": "Root cause: CT1=1.10 exceeds valid range (0-1.0). Fix: Check row 3, column CT1 in cli_data.csv"}
            ]
        ))
        
        # METHODOLOGY TOOLS
        self.register(Feature(
            id="ept_analyzer",
            name="Extended Phenotype Theory Analyzer",
            description="Apply EPT framework to cultural dimensions. Analyzes how constitutional 'genes' create institutional 'extended phenotypes'. Maps cultural transmission mechanisms.",
            category=FeatureCategory.METHODOLOGY,
            icon="🧬",
            endpoint="/api/methodology/ept",
            saas_tier="pro",
            documentation_url="/docs/ept-analyzer",
            examples=[
                {"input": "Somalia federal system", "output": "EPT Analysis: Scaffold phenotype (formal structure) without foundation genes (cultural transmission)"}
            ]
        ))
        
        self.register(Feature(
            id="paleontology_tool",
            name="Constitutional Paleontology Tool",
            description="Fossil analysis of constitutional provisions. Identify 'living fossils' (provisions unchanged for 100+ years) and 'extinction events' (provisions removed). Track constitutional evolution.",
            category=FeatureCategory.METHODOLOGY,
            icon="🦴",
            endpoint="/api/methodology/paleontology",
            saas_tier="enterprise",
            documentation_url="/docs/paleontology",
            examples=[
                {"input": "Argentine Constitution Art. 14", "output": "Living fossil: 172 years unchanged (1853-2025). Survival rate: 100%"}
            ]
        ))
        
        self.register(Feature(
            id="golden_ratio_detector",
            name="Legal Evolvability Golden Ratio",
            description="Detect optimal constitutional flexibility ratios (entrenchment vs adaptability). Calculate 'golden ratio' for legal evolution (~0.618). Identify over-rigid or under-rigid systems.",
            category=FeatureCategory.METHODOLOGY,
            icon="⚖️",
            endpoint="/api/methodology/golden-ratio",
            saas_tier="enterprise",
            documentation_url="/docs/golden-ratio",
            examples=[
                {"input": "Somalia CLI=0.76", "output": "Deviation from golden ratio: +23.6% (over-rigid)"},
                {"input": "Somalilandia CLI=0.54", "output": "Deviation: -12.6% (near-optimal)"}
            ]
        ))
    
    def register(self, feature: Feature):
        """Register a new feature"""
        self.features[feature.id] = feature
    
    def enable_feature(self, feature_id: str):
        """Enable a specific feature"""
        if feature_id in self.features:
            self.features[feature_id].enabled = True
            self._save_config()
    
    def disable_feature(self, feature_id: str):
        """Disable a specific feature"""
        if feature_id in self.features:
            self.features[feature_id].enabled = False
            self._save_config()
    
    def get_feature(self, feature_id: str) -> Optional[Feature]:
        """Get a specific feature"""
        return self.features.get(feature_id)
    
    def get_enabled_features(self) -> List[Feature]:
        """Get all enabled features"""
        return [f for f in self.features.values() if f.enabled]
    
    def get_features_by_category(self, category: FeatureCategory) -> List[Feature]:
        """Get features by category"""
        return [f for f in self.features.values() if f.category == category]
    
    def get_features_by_tier(self, tier: str) -> List[Feature]:
        """Get features by SaaS tier"""
        return [f for f in self.features.values() if f.saas_tier == tier]
    
    def track_usage(self, feature_id: str):
        """Track feature usage (for SaaS analytics)"""
        if feature_id in self.features:
            self.features[feature_id].usage_count += 1
            self.features[feature_id].last_used = datetime.now().isoformat()
            self._save_config()
    
    def get_inventory(self) -> Dict[str, Any]:
        """Get complete feature inventory"""
        return {
            "total_features": len(self.features),
            "enabled_features": len(self.get_enabled_features()),
            "categories": {
                category.value: len(self.get_features_by_category(category))
                for category in FeatureCategory
            },
            "tiers": {
                "free": len(self.get_features_by_tier("free")),
                "basic": len(self.get_features_by_tier("basic")),
                "pro": len(self.get_features_by_tier("pro")),
                "enterprise": len(self.get_features_by_tier("enterprise"))
            },
            "features": {
                feature_id: feature.to_dict()
                for feature_id, feature in self.features.items()
            }
        }
    
    def _load_config(self):
        """Load feature configuration from file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                for feature_id, feature_data in config.items():
                    if feature_id in self.features:
                        self.features[feature_id].enabled = feature_data.get("enabled", True)
                        self.features[feature_id].usage_count = feature_data.get("usage_count", 0)
                        self.features[feature_id].last_used = feature_data.get("last_used")
    
    def _save_config(self):
        """Save feature configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        config = {
            feature_id: {
                "enabled": feature.enabled,
                "usage_count": feature.usage_count,
                "last_used": feature.last_used
            }
            for feature_id, feature in self.features.items()
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)


# Global registry instance
registry = FeatureRegistry()
