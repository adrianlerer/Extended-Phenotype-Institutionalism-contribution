"""
FRP Real Cases Demo - Testing with Actual Constitutional Narratives
====================================================================

Demonstrates the power of Fractal Reasoning Protocol (FRP) using real cases
from the dataset with OpenRouter API integration.

Author: Legal Evolution Project
Date: 2025-11-01
"""

import os
import sys
import pandas as pd
from pathlib import Path
from openai import OpenAI
from datetime import datetime
from typing import List, Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.analysis.frp import create_constitutional_analyzer, FRPAnalysis
from src.analysis.complexity_heuristics import ComplexityScorer


# ============================================================================
# OPENROUTER SETUP
# ============================================================================

def load_env():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value


def create_openrouter_client():
    """Initialize OpenRouter client"""
    load_env()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    return client


def ai_callback(prompt: str, model: str = "anthropic/claude-3.5-sonnet") -> str:
    """
    AI callback for FRP analysis using OpenRouter.
    
    Models available:
    - anthropic/claude-3.5-sonnet (best for analysis)
    - openai/gpt-4-turbo
    - google/gemini-pro-1.5
    - minimax/minimax-01
    """
    client = create_openrouter_client()
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in constitutional law and political analysis. Provide deep, nuanced analysis following the precise instructions given."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.3  # Lower temp for analytical consistency
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"❌ API Error: {e}")
        return f"[API Error: {str(e)}]"


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_case_simple(case: Dict) -> Dict:
    """Simple complexity scoring (baseline)"""
    scorer = ComplexityScorer(language='es')
    narrative = case['Sov_Narrative']
    
    result = scorer.score_narrative(narrative)
    
    return {
        'case_id': case['Case_ID'],
        'country': case['Country'],
        'conflict_type': case['Conflict_Type'],
        'c_score': result['score'],
        'confidence': result['confidence'],
        'features': result['features'],
        'explanation': result['explanation']
    }


def analyze_case_frp(case: Dict, levels: List[str] = ['L1', 'L2', 'L3']) -> FRPAnalysis:
    """Full FRP analysis with AI"""
    analyzer = create_constitutional_analyzer()
    narrative = case['Sov_Narrative']
    
    # Get C score first for context
    scorer = ComplexityScorer(language='es')
    c_score = scorer.score_narrative(narrative)['score']
    
    question = f"""Analyze the strategic framing and constitutional complexity of this {case['Conflict_Type']} narrative from {case['Country']} ({case['Year']}).

Context: This narrative scores C={c_score:.1f} on our complexity scale (1=simple binary, 10=highly nuanced).

Focus on:
1. What sovereignty doctrine is being invoked?
2. What legal/political structures underpin the argument?
3. How do rhetorical elements interact to persuade?
"""
    
    analysis = analyzer.analyze_narrative(
        narrative,
        question,
        levels=levels,
        ai_callback=ai_callback
    )
    
    return analysis


def compare_analyses(simple: Dict, frp: FRPAnalysis) -> str:
    """Generate comparison report"""
    report = f"""
# 🔍 COMPARATIVE ANALYSIS: {simple['case_id']}

## Case Context
- **Country**: {simple['country']}
- **Conflict Type**: {simple['conflict_type']}
- **Narrative Complexity (C)**: {simple['c_score']:.2f}/10
- **Confidence**: {simple['confidence']:.0f}%

---

## 📊 BASELINE: Simple Heuristic Scoring

### Quantitative Features Detected
"""
    
    features = simple['features']
    report += f"- **Binary markers**: {features['binary_markers']} occurrences\n"
    report += f"- **Technical terms**: {features['technical_terms']} occurrences\n"
    report += f"- **Emotional words**: {features['emotional_words']} occurrences\n"
    report += f"- **Avg sentence length**: {features['avg_sentence_length']:.1f} words\n"
    report += f"- **Subordinate clauses**: {features['subordinate_clauses']} clauses\n\n"
    
    report += f"### Heuristic Explanation\n{simple['explanation']}\n\n"
    
    report += "---\n\n"
    report += "## 🧠 ENHANCED: Fractal Reasoning Protocol (FRP)\n\n"
    
    for level in frp.levels:
        report += f"### {level.title}\n\n"
        report += f"{level.content}\n\n"
        report += "---\n\n"
    
    report += """
## 💡 KEY IMPROVEMENTS: What FRP Reveals Beyond Scoring

### 1. **Strategic Context** (L1 - Macro View)
- Simple scoring: Counts linguistic markers
- **FRP adds**: Identifies systemic stakes, power dynamics, why this matters NOW

### 2. **Structural Depth** (L2 - Inner Architecture)
- Simple scoring: Detects technical terms vs binary framing
- **FRP adds**: Maps the 3-5 foundational pillars, reveals hidden mechanisms, shows constraints

### 3. **Interaction Dynamics** (L3 - Relational Analysis)
- Simple scoring: Cannot detect interaction effects
- **FRP adds**: Synergies, tensions, feedback loops, paradoxes, phase transitions

### 4. **Fractal Insight** (L4 - Micro Mirrors Macro)
- Simple scoring: No concept of fractal patterns
- **FRP adds**: Identifies specific phrase/clause that encapsulates entire argument in miniature

### 5. **Transferable Wisdom** (L5 - Strategic Resonance)
- Simple scoring: No meta-level synthesis
- **FRP adds**: Extracts universal principle applicable across domains, actionable lessons

---

## 🎯 VALUE PROPOSITION

**Heuristic Scoring**: Quick, scalable, quantitative → Good for **filtering** 60 cases

**FRP Analysis**: Deep, qualitative, strategic → Essential for **understanding** the top 5-10 cases

**Combined Power**: Use C scores to identify high-complexity cases, then FRP for deep-dive analysis.

---

**Generated**: {datetime.now().isoformat()}
"""
    
    return report


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*80)
    print("🧠 FRACTAL REASONING PROTOCOL - REAL CASES DEMO")
    print("="*80)
    print("\nTesting FRP with actual constitutional conflict narratives")
    print("Comparing simple heuristic scoring vs multi-level FRP analysis\n")
    
    # Load test cases
    print("📂 Loading test cases...")
    df = pd.read_csv('data/raw/test_5cases.csv')
    print(f"   ✓ Loaded {len(df)} cases\n")
    
    # Select 2 representative cases for demo (to save API calls)
    selected_cases = [
        'UK-EU-2016',  # Brexit - high profile, binary framing
        'USA-ICC-2002'  # ICC rejection - complex legal argument
    ]
    
    print(f"📋 Analyzing {len(selected_cases)} cases with FRP:")
    for case_id in selected_cases:
        print(f"   • {case_id}")
    print()
    
    # Create output directory
    output_dir = Path('data/processed/frp_demo')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Analyze each case
    for case_id in selected_cases:
        print(f"\n{'='*80}")
        print(f"🔍 CASE: {case_id}")
        print(f"{'='*80}\n")
        
        case = df[df['Case_ID'] == case_id].iloc[0].to_dict()
        
        # Step 1: Simple scoring
        print("1️⃣  Running baseline heuristic scoring...")
        simple_result = analyze_case_simple(case)
        print(f"   ✓ C Score: {simple_result['c_score']:.2f}/10")
        print(f"   ✓ Confidence: {simple_result['confidence']:.0f}%\n")
        
        # Step 2: FRP analysis (L1-L3 for speed)
        print("2️⃣  Running FRP analysis (L1-L3) with AI...")
        print("   [Calling OpenRouter API - this may take 30-60s]\n")
        
        try:
            frp_result = analyze_case_frp(case, levels=['L1', 'L2', 'L3'])
            print("   ✓ L1 (Macro View) - Complete")
            print("   ✓ L2 (Structure) - Complete")
            print("   ✓ L3 (Interactions) - Complete\n")
            
            # Step 3: Generate comparison
            print("3️⃣  Generating comparative analysis...")
            comparison = compare_analyses(simple_result, frp_result)
            
            # Save outputs
            md_file = output_dir / f"{case_id}_comparison.md"
            json_file = output_dir / f"{case_id}_frp_analysis.json"
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(comparison)
            
            frp_result.to_json(str(json_file))
            
            print(f"   ✓ Saved: {md_file}")
            print(f"   ✓ Saved: {json_file}\n")
            
            # Print preview
            print("📄 PREVIEW - FRP L1 (Macro View):")
            print("-" * 80)
            preview = frp_result.levels[0].content[:400]
            print(preview + "...\n")
            
        except Exception as e:
            print(f"   ❌ Error during FRP analysis: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE")
    print("="*80)
    print(f"\n📁 Results saved to: {output_dir}/")
    print("\n📊 Files generated:")
    for f in output_dir.glob("*.md"):
        print(f"   • {f.name}")
    
    print("\n💡 Next steps:")
    print("   1. Review the .md comparison files")
    print("   2. Evaluate if FRP adds value beyond C scores")
    print("   3. Decide: use FRP for all 60 cases or just top 10?")
    print("   4. Consider: L1-L3 (fast) vs L1-L5 (deep) tradeoff\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
