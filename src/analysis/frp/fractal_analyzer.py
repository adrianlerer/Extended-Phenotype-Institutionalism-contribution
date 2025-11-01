"""
Fractal Reasoning Protocol (FRP) Analyzer
==========================================

Python integration for multi-level narrative analysis using FRP methodology.
Designed to work with InteractiveCoder and complexity_heuristics modules.

Author: Legal Evolution Project
Date: 2025-11-01
"""

import json
import os
from typing import Dict, List, Optional, Literal, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import pandas as pd


# ============================================================================
# TYPE DEFINITIONS (mirroring TypeScript types)
# ============================================================================

@dataclass
class DomainContext:
    """Domain context for FRP analysis"""
    domain: Literal['legal', 'compliance', 'audit', 'risk', 'due_diligence', 'constitutional', 'political']
    sub_domain: Optional[str] = None
    jurisdiction: Optional[str] = None
    industry: Optional[str] = None
    additional_context: Optional[Dict[str, Any]] = None


@dataclass
class FRPLevelOutput:
    """Individual level output"""
    level: Literal['L1', 'L2', 'L3', 'L4', 'L5']
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class FRPAnalysis:
    """Complete FRP analysis result"""
    input_text: str
    question: str
    domain_context: DomainContext
    levels: List[FRPLevelOutput]
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        result = asdict(self)
        result['domain_context'] = asdict(self.domain_context)
        result['levels'] = [asdict(level) for level in self.levels]
        return result
    
    def to_json(self, filepath: str):
        """Save analysis to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def to_markdown(self) -> str:
        """Export analysis as formatted markdown"""
        md = f"# Fractal Reasoning Analysis\n\n"
        md += f"**Generated:** {self.timestamp}\n\n"
        md += f"**Domain:** {self.domain_context.domain}\n\n"
        
        if self.domain_context.sub_domain:
            md += f"**Sub-domain:** {self.domain_context.sub_domain}\n\n"
        
        md += f"## Analysis Question\n\n{self.question}\n\n"
        md += f"## Input Material\n\n```\n{self.input_text[:500]}...\n```\n\n"
        md += "---\n\n"
        
        for level in self.levels:
            md += f"## {level.title}\n\n"
            md += f"{level.content}\n\n"
            
            if level.metadata and level.metadata.get('key_insights'):
                md += "**Key Insights:**\n"
                for insight in level.metadata['key_insights']:
                    md += f"- {insight}\n"
                md += "\n"
            
            md += "---\n\n"
        
        return md


# ============================================================================
# FRP PROMPT TEMPLATES (Python version)
# ============================================================================

class FRPPromptGenerator:
    """Generate FRP prompts for AI analysis"""
    
    LEVEL_DEFINITIONS = {
        'L1': {
            'title': 'Macro View (Strategic Panorama)',
            'objective': 'Provide high-level overview of what\'s at stake',
            'typical_length': '3-5 sentences'
        },
        'L2': {
            'title': 'Inner Structure (System Architecture)',
            'objective': 'Decompose internal mechanisms and structural components',
            'typical_length': '1 paragraph (5-7 sentences)'
        },
        'L3': {
            'title': 'Interactions (Relational Dynamics)',
            'objective': 'Analyze component interactions and emergent behavior',
            'typical_length': '1 paragraph (6-8 sentences)'
        },
        'L4': {
            'title': 'Fractal Perspective (Meaningful Zoom)',
            'objective': 'Identify concrete detail that encapsulates entire system',
            'typical_length': '1 paragraph (6-8 sentences)'
        },
        'L5': {
            'title': 'Strategic Resonance (Transferable Wisdom)',
            'objective': 'Extract universal principle and actionable lessons',
            'typical_length': '1 paragraph (4-6 sentences)'
        }
    }
    
    @staticmethod
    def get_l1_prompt(input_text: str, question: str, domain_context: DomainContext) -> str:
        """Generate Level 1 (Macro View) prompt"""
        return f"""# FRACTAL REASONING — LEVEL 1: MACRO VIEW

## Your Role
You are an expert analyst conducting a **strategic panorama** assessment.

## Domain Context
- Domain: {domain_context.domain}
- Sub-domain: {domain_context.sub_domain or 'general'}
- Jurisdiction: {domain_context.jurisdiction or 'not specified'}
- Industry: {domain_context.industry or 'not specified'}

## Task
Analyze the following {domain_context.domain} material and provide a **global perspective**.

### Input Material:
```
{input_text}
```

### Analysis Question:
{question}

## Level 1 Objective: MACRO VIEW (Strategic Panorama)

Provide a high-level overview answering:
1. **What's at stake here?** — Why does this matter systemically?
2. **Why now?** — What makes this relevant in current context?
3. **Who's affected?** — What parties, interests, or systems are involved?
4. **Global implications** — What are the second-order effects?

## Output Format
Produce **3-5 sentences** that synthesize the global picture.

Use this structure:
- First sentence: Core issue identification
- Middle sentences: Stakeholder implications and systemic relevance
- Final sentence: Why this matters beyond the immediate context

## Reasoning Requirements
- Maintain objectivity — describe reality, not aspirations
- Identify invisible forces — power dynamics, incentives, constraints
- Connect to broader trends — regulatory shifts, market evolution, precedent

## Your Level 1 Analysis:"""
    
    @staticmethod
    def get_l2_prompt(input_text: str, question: str, domain_context: DomainContext, l1_output: str) -> str:
        """Generate Level 2 (Structure) prompt"""
        domain_guidance = FRPPromptGenerator._get_domain_l2_guidance(domain_context.domain)
        
        return f"""# FRACTAL REASONING — LEVEL 2: INNER STRUCTURE

## Context from Level 1
You previously identified:
```
{l1_output}
```

## Level 2 Objective: SYSTEM ARCHITECTURE

Now decompose the **internal mechanisms** that govern this system.

### Input Material:
```
{input_text}
```

### Analysis Question:
{question}

## What to Identify:
1. **Key pillars** — What are the 3-5 foundational components?
2. **Operating principles** — What rules/norms govern behavior?
3. **Hidden mechanisms** — What drives outcomes beneath the surface?
4. **Structural constraints** — What limits degrees of freedom?

## Domain-Specific Focus ({domain_context.domain}):
{domain_guidance}

## Output Format
Produce **1 concise paragraph** (5-7 sentences) breaking down:
- Main structural components
- How they interact to produce the system's behavior
- What makes this architecture stable or fragile

## Your Level 2 Analysis:"""
    
    @staticmethod
    def get_l3_prompt(input_text: str, question: str, domain_context: DomainContext, 
                      l1_output: str, l2_output: str) -> str:
        """Generate Level 3 (Interactions) prompt"""
        domain_guidance = FRPPromptGenerator._get_domain_l3_guidance(domain_context.domain)
        
        return f"""# FRACTAL REASONING — LEVEL 3: RELATIONAL DYNAMICS

## Context from Previous Levels

**Level 1 (Macro):**
```
{l1_output}
```

**Level 2 (Structure):**
```
{l2_output}
```

## Level 3 Objective: INTERACTIONS & EMERGENCE

Now analyze **how the structural components interact** to produce emergent behavior.

### Input Material:
```
{input_text}
```

### Analysis Question:
{question}

## What to Reveal:
1. **Synergies** — Which components reinforce each other?
2. **Tensions** — Where do contradictions or conflicts exist?
3. **Feedback loops** — What self-reinforcing or self-correcting dynamics emerge?
4. **Paradoxes** — What appears contradictory but actually reveals deeper logic?
5. **Phase transitions** — Under what conditions does the system shift behavior?

## Domain-Specific Focus ({domain_context.domain}):
{domain_guidance}

## Output Format
Produce **1 paragraph** (6-8 sentences) explaining:
- Key interactions between structural elements
- Emergent properties not predictable from components alone
- Critical dependencies or cascading effects
- System vulnerabilities or resilience patterns

## Your Level 3 Analysis:"""
    
    @staticmethod
    def get_l4_prompt(input_text: str, question: str, domain_context: DomainContext,
                      l1_output: str, l2_output: str, l3_output: str) -> str:
        """Generate Level 4 (Fractal) prompt"""
        domain_guidance = FRPPromptGenerator._get_domain_l4_guidance(domain_context.domain)
        
        return f"""# FRACTAL REASONING — LEVEL 4: FRACTAL PERSPECTIVE

## Context from Previous Levels

**Level 1 (Macro):**
```
{l1_output}
```

**Level 2 (Structure):**
```
{l2_output}
```

**Level 3 (Interactions):**
```
{l3_output}
```

## Level 4 Objective: MEANINGFUL ZOOM (Micro Mirrors Macro)

Now identify **a concrete detail, case, or clause** that encapsulates the entire system's logic in miniature.

### Input Material:
```
{input_text}
```

### Analysis Question:
{question}

## What to Find:
1. **The fractal case** — A specific example, clause, phrase, or event that contains the whole system's DNA
2. **How it reflects L1-L3** — Show explicitly how this micro-case embodies:
   - The macro stakes (L1)
   - The structural principles (L2)
   - The interaction dynamics (L3)
3. **Why it matters** — What this micro-view reveals that wasn't visible at higher levels

## Domain-Specific Focus ({domain_context.domain}):
{domain_guidance}

## Output Format
Produce **1 paragraph** (6-8 sentences) that:
- Identifies the specific fractal case (quote it if possible)
- Explains how it mirrors the macro system
- Reveals insight only visible at this zoom level

Structure:
- Opening: "In [specific element], the entire [system] logic appears in miniature..."
- Middle: Explicit connections to L1, L2, L3
- Closing: What this teaches us about the whole

## Your Level 4 Analysis:"""
    
    @staticmethod
    def get_l5_prompt(input_text: str, question: str, domain_context: DomainContext,
                      l1_output: str, l2_output: str, l3_output: str, l4_output: str) -> str:
        """Generate Level 5 (Resonance) prompt"""
        domain_guidance = FRPPromptGenerator._get_domain_l5_guidance(domain_context.domain)
        
        return f"""# FRACTAL REASONING — LEVEL 5: STRATEGIC RESONANCE

## Context from All Previous Levels

**Level 1 (Macro):**
```
{l1_output}
```

**Level 2 (Structure):**
```
{l2_output}
```

**Level 3 (Interactions):**
```
{l3_output}
```

**Level 4 (Fractal):**
```
{l4_output}
```

## Level 5 Objective: STRATEGIC RESONANCE

Extract a **meta-principle or actionable lesson** that transcends this specific case.

### Original Input:
```
{input_text}
```

### Analysis Question:
{question}

## What to Synthesize:
1. **The universal pattern** — What principle operates here that applies elsewhere?
2. **Actionable insight** — What should decision-makers do differently?
3. **Epistemic lesson** — What does this teach about reasoning, system design, or strategy?
4. **Transferability** — How does this apply to other domains?

## Domain-Specific Focus ({domain_context.domain}):
{domain_guidance}

## Output Format
Produce **1 closing paragraph** (4-6 sentences) that:
- States the transferable principle clearly
- Connects it back to the specific case
- Provides actionable guidance
- Hints at broader applications

Structure:
- Opening: "The core lesson: [universal principle]"
- Middle: How this manifests in the analyzed case
- Closing: Practical implication or strategic takeaway

## Your Level 5 Analysis:"""
    
    # Domain-specific guidance methods
    @staticmethod
    def _get_domain_l2_guidance(domain: str) -> str:
        guidance = {
            'constitutional': """
- Identify constitutional principles and sovereignty doctrines
- Map power distribution between domestic/international law
- Reveal implicit assumptions about legal hierarchy""",
            'political': """
- Identify political narratives and framing strategies
- Map actor coalitions and opposition structures
- Reveal implicit assumptions about legitimacy and authority""",
            'legal': """
- Identify governing legal principles (contract law doctrines, statutory frameworks)
- Map clause interdependencies
- Reveal implicit assumptions in legal language"""
        }
        return guidance.get(domain, "- Identify key structural components\n- Map their relationships\n- Reveal hidden mechanisms")
    
    @staticmethod
    def _get_domain_l3_guidance(domain: str) -> str:
        guidance = {
            'constitutional': """
- Analyze tension between sovereignty and international obligations
- Identify feedback loops between domestic politics and legal strategy
- Reveal how constitutional rhetoric masks power struggles""",
            'political': """
- Analyze narrative competition dynamics
- Identify amplification and suppression mechanisms
- Reveal how framing shapes policy space and legitimacy""",
            'legal': """
- Analyze clause interactions (do they create contradictions?)
- Identify perverse incentives in contract structure
- Reveal how ambiguity distributes risk asymmetrically"""
        }
        return guidance.get(domain, "- Analyze component interactions\n- Identify feedback loops\n- Reveal emergent behavior")
    
    @staticmethod
    def _get_domain_l4_guidance(domain: str) -> str:
        guidance = {
            'constitutional': """
- Find a specific constitutional provision, treaty clause, or court decision that encapsulates the sovereignty vs. globalism tension
- Show how it reflects systemic stakes (L1), legal architecture (L2), political dynamics (L3)""",
            'political': """
- Find a specific speech excerpt, policy statement, or rhetorical move that encapsulates the narrative strategy
- Show how it reflects political stakes (L1), framing structure (L2), coalition dynamics (L3)""",
            'legal': """
- Find a specific clause/phrase that encapsulates the contract's core tension
- Show how it reflects party power dynamics (L1), legal architecture (L2), interaction effects (L3)"""
        }
        return guidance.get(domain, "- Find a concrete example that mirrors the whole system\n- Explain the fractal reflection")
    
    @staticmethod
    def _get_domain_l5_guidance(domain: str) -> str:
        guidance = {
            'constitutional': """
- Extract principle about constitutional change, sovereignty dynamics, or legal evolution
- Provide actionable guidance for constitutional design or treaty negotiation""",
            'political': """
- Extract principle about narrative competition, framing effects, or legitimacy construction
- Provide actionable guidance for political strategy or communication""",
            'legal': """
- Extract principle about contract design, risk allocation, or legal strategy
- Provide actionable guidance for drafting or negotiation"""
        }
        return guidance.get(domain, "- Extract a universal principle\n- Provide actionable guidance")


# ============================================================================
# FRACTAL ANALYZER (Main Interface)
# ============================================================================

class FractalAnalyzer:
    """
    Main interface for conducting FRP analysis on narratives.
    
    Integrates with InteractiveCoder and complexity_heuristics for
    multi-level narrative analysis.
    """
    
    def __init__(self, domain_context: DomainContext):
        """
        Initialize analyzer with domain context.
        
        Args:
            domain_context: Domain-specific configuration
        """
        self.domain_context = domain_context
        self.prompt_generator = FRPPromptGenerator()
    
    def analyze_narrative(
        self,
        narrative_text: str,
        question: str,
        levels: List[str] = ['L1', 'L2', 'L3', 'L4', 'L5'],
        ai_callback: Optional[callable] = None
    ) -> FRPAnalysis:
        """
        Conduct multi-level FRP analysis on narrative.
        
        Args:
            narrative_text: The text to analyze
            question: Analysis question/focus
            levels: Which levels to execute (default: all 5)
            ai_callback: Function to call AI model (signature: prompt -> response)
        
        Returns:
            FRPAnalysis object with all level outputs
        """
        level_outputs = []
        previous_outputs = {}
        
        for level in levels:
            prompt = self._generate_prompt(
                level, 
                narrative_text, 
                question, 
                previous_outputs
            )
            
            # If AI callback provided, use it; otherwise return prompts only
            if ai_callback:
                response = ai_callback(prompt)
            else:
                response = f"[AI response for {level} would go here - provide ai_callback to execute]"
            
            level_output = FRPLevelOutput(
                level=level,
                title=self.prompt_generator.LEVEL_DEFINITIONS[level]['title'],
                content=response,
                metadata={
                    'prompt_length': len(prompt),
                    'response_length': len(response)
                }
            )
            
            level_outputs.append(level_output)
            previous_outputs[level] = response
        
        return FRPAnalysis(
            input_text=narrative_text,
            question=question,
            domain_context=self.domain_context,
            levels=level_outputs,
            timestamp=datetime.now().isoformat(),
            metadata={
                'levels_executed': levels,
                'total_levels': len(levels)
            }
        )
    
    def _generate_prompt(
        self, 
        level: str, 
        input_text: str, 
        question: str, 
        previous_outputs: Dict[str, str]
    ) -> str:
        """Generate prompt for specific level"""
        if level == 'L1':
            return self.prompt_generator.get_l1_prompt(input_text, question, self.domain_context)
        elif level == 'L2':
            return self.prompt_generator.get_l2_prompt(
                input_text, question, self.domain_context, previous_outputs.get('L1', '')
            )
        elif level == 'L3':
            return self.prompt_generator.get_l3_prompt(
                input_text, question, self.domain_context, 
                previous_outputs.get('L1', ''), previous_outputs.get('L2', '')
            )
        elif level == 'L4':
            return self.prompt_generator.get_l4_prompt(
                input_text, question, self.domain_context,
                previous_outputs.get('L1', ''), previous_outputs.get('L2', ''), previous_outputs.get('L3', '')
            )
        elif level == 'L5':
            return self.prompt_generator.get_l5_prompt(
                input_text, question, self.domain_context,
                previous_outputs.get('L1', ''), previous_outputs.get('L2', ''), 
                previous_outputs.get('L3', ''), previous_outputs.get('L4', '')
            )
        else:
            raise ValueError(f"Invalid level: {level}")
    
    def batch_analyze_dataset(
        self,
        df: pd.DataFrame,
        text_column: str,
        question_template: str = "Analyze the complexity and strategic implications of this {domain} narrative.",
        output_dir: str = 'data/processed/frp_analysis',
        ai_callback: Optional[callable] = None
    ) -> pd.DataFrame:
        """
        Batch analyze multiple narratives in dataset.
        
        Args:
            df: DataFrame with narratives
            text_column: Column containing narrative text
            question_template: Analysis question template
            output_dir: Directory to save individual analyses
            ai_callback: AI model callback function
        
        Returns:
            DataFrame with FRP analysis results appended
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for idx, row in df.iterrows():
            narrative = row[text_column]
            question = question_template.format(domain=self.domain_context.domain)
            
            analysis = self.analyze_narrative(narrative, question, ai_callback=ai_callback)
            
            # Save individual analysis
            output_file = os.path.join(output_dir, f"frp_analysis_{idx}.json")
            analysis.to_json(output_file)
            
            # Extract key metrics
            result = {
                'index': idx,
                'L1_length': len(analysis.levels[0].content) if len(analysis.levels) > 0 else 0,
                'L2_length': len(analysis.levels[1].content) if len(analysis.levels) > 1 else 0,
                'L3_length': len(analysis.levels[2].content) if len(analysis.levels) > 2 else 0,
                'L4_length': len(analysis.levels[3].content) if len(analysis.levels) > 3 else 0,
                'L5_length': len(analysis.levels[4].content) if len(analysis.levels) > 4 else 0,
                'analysis_file': output_file
            }
            results.append(result)
        
        results_df = pd.DataFrame(results)
        return df.join(results_df.set_index('index'))


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_constitutional_analyzer() -> FractalAnalyzer:
    """Create analyzer configured for constitutional narratives"""
    context = DomainContext(
        domain='constitutional',
        sub_domain='sovereignty_vs_globalism',
        jurisdiction='comparative',
        additional_context={
            'focus': 'narrative complexity and strategic framing'
        }
    )
    return FractalAnalyzer(context)


def create_political_analyzer() -> FractalAnalyzer:
    """Create analyzer configured for political narratives"""
    context = DomainContext(
        domain='political',
        sub_domain='constitutional_conflict',
        additional_context={
            'focus': 'framing strategies and legitimacy construction'
        }
    )
    return FractalAnalyzer(context)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    # Example: Analyze a sovereignty narrative
    analyzer = create_constitutional_analyzer()
    
    test_narrative = """
    Our nation's sovereignty is under threat from international tribunals that 
    seek to impose their will on our democratic institutions. We must defend our 
    constitutional order against these external pressures that undermine the voice 
    of our people and their elected representatives.
    """
    
    question = "Analyze the complexity and strategic framing of this sovereignty narrative."
    
    # Generate prompts (without AI execution)
    analysis = analyzer.analyze_narrative(
        test_narrative,
        question,
        levels=['L1', 'L2', 'L3']
    )
    
    # Export as markdown
    print(analysis.to_markdown())
    
    # Save as JSON
    # analysis.to_json('test_frp_analysis.json')
