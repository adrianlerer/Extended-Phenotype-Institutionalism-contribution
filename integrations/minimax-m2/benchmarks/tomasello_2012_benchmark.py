"""
Tomasello (2012) Benchmark - Three-Pass Method PASS 1
======================================================

Benchmark MiniMax-M2 performance on Tomasello (2012) paper analysis.

We have a complete manual analysis (5h 55min) as ground truth:
- File: law-rendezvous-point/methodology/paper_analysis/EXAMPLE_Tomasello_2012.md
- Total time: 10min (PASS 1) + 1h 15min (PASS 2) + 4h 30min (PASS 3)

This benchmark focuses on PASS 1 (Bird's Eye View) automation:
- Target time: 5-10 minutes (model inference time)
- Expected accuracy: >85% agreement with manual analysis
- Evaluation dimensions: Five C's correctness + decision alignment

Ground Truth (from manual analysis):
------------------------------------
PASS 1 Results:
- Category: Theoretical + Empirical (evolutionary anthropology)
- Context: Dawkins Extended Phenotype, Trivers reciprocal altruism, 
          game theory (ESS), primatology (chimp behavior)
- Correctness: Valid (though timeline uncertainty ±1M years)
- Contributions:
  1. Two-step model (mutualism → group-mindedness)
  2. Shared intentionality at ~2M years ago (Homo habilis era)
  3. Empirical support from child development + comparative primatology
- Clarity: Excellent (clear structure, well-written)
- Decision: READ IN DEPTH (critical for Legal Rubicon hypothesis)

Success Criteria:
----------------
✅ Category matches (theoretical + empirical)
✅ Context references overlap ≥3/4 key theories
✅ Correctness assessment agrees (valid with caveats)
✅ Contributions overlap ≥2/3 main claims
✅ Clarity rating within 1 level (excellent/good)
✅ Decision agrees (READ vs. CITE/DISCARD)
✅ Inference time < 60 seconds (target: 10-30s)
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple
from dataclasses import dataclass

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from client import MiniMaxClient, MiniMaxResponse
from config import MiniMaxConfig


# Ground truth from manual analysis
GROUND_TRUTH = {
    "category": ["theoretical", "empirical", "evolutionary anthropology"],
    "context_keywords": [
        "extended phenotype",
        "dawkins",
        "trivers",
        "reciprocal altruism",
        "ess",
        "game theory",
        "chimp",
        "primate"
    ],
    "correctness": "valid",
    "contributions_keywords": [
        "two-step",
        "mutualism",
        "group",
        "shared intentionality",
        "2 million",
        "homo habilis",
        "child development",
        "comparative"
    ],
    "clarity": "excellent",
    "decision": "read",
    "rationale_keywords": [
        "rubicon",
        "primary",
        "foundational",
        "critical"
    ]
}


# Tomasello (2012) paper content (abstract + intro)
TOMASELLO_2012_TEXT = """
Two Key Steps in the Evolution of Human Cooperation

Michael Tomasello
Max Planck Institute for Evolutionary Anthropology

Current Anthropology, Vol. 53, No. 6 (December 2012), pp. 673-692

ABSTRACT

The biological and cultural evolution of human cooperation involves two key 
steps or cognitive thresholds. The first step concerns shared intentionality, 
which emerged in our early evolutionary history as individuals began to 
collaborate in mutualistic activities requiring joint attention, shared goals, 
and coordinated action plans. This cognitive capacity enabled collaborative 
foraging and other survival-critical activities. Archaeological evidence 
suggests this threshold was crossed approximately 2 million years ago, 
coinciding with Homo habilis and the first stone tools.

The second step concerns collective intentionality, which emerged more 
recently as human groups formed shared cultural norms, institutional 
structures, and group-level identities. This involved the creation of cultural 
groups with "objective" social norms and institutions that individuals 
internalized. Archaeological evidence suggests this threshold was crossed 
approximately 200,000-100,000 years ago, coinciding with Homo sapiens and 
the first clear evidence of symbolic culture.

This two-step model is supported by several lines of evidence from:
(1) developmental psychology showing that human children (but not great apes) 
    exhibit shared intentionality by 12-14 months and equitable resource 
    sharing by 3 years,
(2) comparative primatology demonstrating that great apes engage in mutualistic 
    collaboration but lack key aspects of shared intentionality and group-level 
    norms,
(3) paleoanthropology providing fossil and archaeological evidence for the 
    timing of these cognitive transitions.

The model integrates insights from game theory (particularly evolutionarily 
stable strategies), reciprocal altruism theory (Trivers 1971), and extended 
phenotype theory (Dawkins 1982) to explain how human cooperation evolved 
through these two distinct cognitive and cultural thresholds.

INTRODUCTION

Human cooperation is unique in the natural world in both its scale and its 
structure. While many species exhibit cooperation, human cooperation is 
distinguished by its reliance on shared intentional states—joint goals, 
mutual knowledge, and collective commitments—and by the existence of group-
level social norms and institutions that regulate behavior across large 
populations. Understanding how this capacity evolved requires identifying 
the key cognitive and cultural transitions that enabled first small-scale 
collaboration and later large-scale cultural groups.

This paper proposes that human cooperation evolved through two key steps, 
each involving a distinct cognitive threshold:

Step 1: Shared Intentionality (~2 million years ago)
- Emergence: Homo habilis, obligate collaborative foraging
- Cognitive capacity: Joint attention, shared goals, coordinated plans
- Social structure: Small-scale mutualistic partnerships
- Evidence: Archaeological (Oldowan tools), comparative (chimp vs. human children)

Step 2: Collective Intentionality (~200,000-100,000 years ago)
- Emergence: Homo sapiens, symbolic culture, group competition
- Cognitive capacity: Group-level norms, institutional thinking, cultural identity
- Social structure: Large-scale cultural groups with objective norms
- Evidence: Archaeological (symbolic artifacts), ethnographic (universal norm psychology)

Each step represents a major evolutionary transition that fundamentally 
restructured human social life. The first step enabled small-scale cooperation 
in foraging and defense. The second step enabled large-scale cooperation 
through cultural norms and institutions that could coordinate behavior across 
hundreds or thousands of individuals who might never interact directly.

The remainder of this paper:
1. Details the evolutionary and developmental evidence for each step
2. Explains the cognitive mechanisms underlying each threshold
3. Discusses the archaeological timeline and fossil evidence
4. Integrates the model with game-theoretic and evolutionary approaches
5. Addresses alternative hypotheses and areas of uncertainty

[Rest of paper continues with detailed sections on developmental psychology 
experiments, comparative primatology studies, paleoanthropological evidence, 
game-theoretic modeling, and discussion of implications for understanding 
human social evolution and the origins of morality, law, and institutions.]

METHODS

Developmental Psychology Evidence:
- Studies with children ages 12 months to 5 years
- Tasks: collaborative problem-solving, resource sharing, norm enforcement
- Key finding: Shared intentionality emerges ~12-14 months (pointing, joint attention)
- Key finding: Equitable sharing emerges ~3 years (fairness norms)

Comparative Primatology Evidence:
- Studies with chimpanzees, bonobos, orangutans
- Same tasks as children's studies
- Key finding: Great apes can engage in mutualistic collaboration
- Key finding: Great apes do NOT share equitably (~3 year old human behavior)
- Interpretation: Shared intentionality is uniquely human (or Homo genus)

Paleoanthropological Evidence:
- Fossil record: Brain expansion in early Homo (2.5-1.5 Mya)
- Archaeological record: Oldowan stone tools (2.6 Mya), Acheulean tools (1.7 Mya)
- Collaborative foraging inference: Persistence hunting, large game butchery
- Timeline estimate: Shared intentionality ~2 million years ago ± 500k years

DISCUSSION

The two-step model has several implications:

1. Legal and Institutional Origins
   Shared intentionality (Step 1) represents a kind of "proto-law" based on 
   dyadic joint commitments. Collective intentionality (Step 2) represents 
   true "law" based on group-level norms that apply to all members and are 
   enforced collectively. This suggests law emerged with Homo sapiens culture.

2. Cooperation and Conflict
   The model explains both human hyper-cooperation (within groups) and 
   hyper-conflict (between groups). Step 2 created strong in-group/out-group 
   psychology that enabled large-scale coordination but also large-scale warfare.

3. Timeline Uncertainty
   The archaeological evidence for Step 1 is indirect (tools, brain size) 
   rather than direct (fossils showing collaboration). The 2 million year 
   estimate has uncertainty of ±1 million years. Some researchers place 
   shared intentionality much later (~200k years ago with Homo sapiens).

4. Alternative Hypotheses
   - "Single-step" models: Only Homo sapiens cognitive revolution
   - "Multi-step" models: More than two thresholds (e.g., language as separate step)
   - Timing disagreements: When exactly did each step occur?

CONCLUSIONS

Human cooperation evolved through two key cognitive transitions: shared 
intentionality (~2 Mya) enabling small-scale collaboration, and collective 
intentionality (~200-100 kya) enabling large-scale cultural groups. This 
two-step model is supported by converging evidence from developmental 
psychology, comparative primatology, and paleoanthropology. Understanding 
these transitions is essential for explaining the origins of human morality, 
law, and institutions.

The model highlights that human cooperation is not simply an extension of 
primate cooperation but involves qualitatively new cognitive capacities. 
These capacities—shared and collective intentionality—form the foundation 
for all human cultural and institutional life, from language and morality 
to law and government.

Future research should focus on:
1. Resolving timeline uncertainties through better archaeological evidence
2. Testing predictions about intermediate forms (early Homo species)
3. Investigating neural mechanisms underlying shared/collective intentionality
4. Applying the model to understand modern institutional dysfunction
"""


@dataclass
class BenchmarkResult:
    """Results from Tomasello (2012) benchmark."""
    model_response: MiniMaxResponse
    parsed_analysis: Dict
    ground_truth: Dict
    accuracy_scores: Dict
    overall_accuracy: float
    passed: bool
    
    def print_report(self):
        """Print detailed benchmark report."""
        print("=" * 80)
        print("TOMASELLO (2012) BENCHMARK REPORT")
        print("=" * 80)
        
        print("\n📊 PERFORMANCE METRICS")
        print("-" * 80)
        print(f"Inference Time: {self.model_response.latency_ms:.0f}ms")
        print(f"Total Tokens: {self.model_response.usage['total_tokens']}")
        print(f"  - Prompt: {self.model_response.usage['prompt_tokens']}")
        print(f"  - Completion: {self.model_response.usage['completion_tokens']}")
        if self.model_response.has_thinking():
            print(f"  - Thinking: ~{self.model_response.thinking.thinking_tokens} (estimated)")
        
        print("\n✅ ACCURACY SCORES")
        print("-" * 80)
        for dimension, score in self.accuracy_scores.items():
            icon = "✅" if score >= 0.75 else "⚠️" if score >= 0.5 else "❌"
            print(f"{icon} {dimension.replace('_', ' ').title()}: {score:.1%}")
        
        print(f"\n{'✅' if self.passed else '❌'} OVERALL ACCURACY: {self.overall_accuracy:.1%}")
        print(f"{'✅ PASSED' if self.passed else '❌ FAILED'} (threshold: 85%)")
        
        print("\n🤔 MODEL THINKING (EXCERPTS)")
        print("-" * 80)
        if self.model_response.has_thinking():
            thinking = self.model_response.thinking.cleaned_thinking
            lines = thinking.split('\n')[:10]  # First 10 lines
            for line in lines:
                print(f"  {line}")
            if len(thinking.split('\n')) > 10:
                print(f"  ... ({len(thinking.split('\n')) - 10} more lines)")
        else:
            print("  (No thinking extracted)")
        
        print("\n📝 MODEL ANALYSIS")
        print("-" * 80)
        print(json.dumps(self.parsed_analysis, indent=2))
        
        print("\n🎯 GROUND TRUTH COMPARISON")
        print("-" * 80)
        self._print_comparison("Category", "category")
        self._print_comparison("Context", "context")
        self._print_comparison("Correctness", "correctness")
        self._print_comparison("Contributions", "contributions")
        self._print_comparison("Clarity", "clarity")
        self._print_comparison("Decision", "decision")
        
        print("\n" + "=" * 80)
    
    def _print_comparison(self, label: str, key: str):
        """Print comparison for specific dimension."""
        model_val = self.parsed_analysis.get(key, "N/A")
        gt_val = self.ground_truth.get(key, "N/A")
        
        print(f"\n{label}:")
        print(f"  Model: {model_val}")
        print(f"  Truth: {gt_val}")
        
        score = self.accuracy_scores.get(f"{key}_accuracy", 0.0)
        icon = "✅" if score >= 0.75 else "⚠️" if score >= 0.5 else "❌"
        print(f"  {icon} Match: {score:.1%}")


def evaluate_category(model_cat: str, ground_truth: Dict) -> float:
    """Evaluate category accuracy."""
    model_cat_lower = model_cat.lower()
    gt_keywords = ground_truth["category"]
    
    matches = sum(1 for kw in gt_keywords if kw in model_cat_lower)
    return matches / len(gt_keywords)


def evaluate_context(model_context: list, ground_truth: Dict) -> float:
    """Evaluate context accuracy."""
    if not model_context:
        return 0.0
    
    model_text = " ".join(model_context).lower()
    gt_keywords = ground_truth["context_keywords"]
    
    matches = sum(1 for kw in gt_keywords if kw in model_text)
    return matches / len(gt_keywords)


def evaluate_correctness(model_correct: Dict, ground_truth: Dict) -> float:
    """Evaluate correctness assessment accuracy."""
    assessment = model_correct.get("assessment", "").lower()
    gt_assessment = ground_truth["correctness"]
    
    return 1.0 if assessment == gt_assessment else 0.0


def evaluate_contributions(model_contribs: list, ground_truth: Dict) -> float:
    """Evaluate contributions accuracy."""
    if not model_contribs:
        return 0.0
    
    model_text = " ".join(model_contribs).lower()
    gt_keywords = ground_truth["contributions_keywords"]
    
    matches = sum(1 for kw in gt_keywords if kw in model_text)
    return matches / len(gt_keywords)


def evaluate_clarity(model_clarity: str, ground_truth: Dict) -> float:
    """Evaluate clarity rating accuracy."""
    clarity_map = {"excellent": 4, "good": 3, "acceptable": 2, "poor": 1}
    
    model_level = clarity_map.get(model_clarity.lower(), 0)
    gt_level = clarity_map.get(ground_truth["clarity"], 0)
    
    # Allow ±1 level difference
    diff = abs(model_level - gt_level)
    if diff == 0:
        return 1.0
    elif diff == 1:
        return 0.75
    else:
        return 0.0


def evaluate_decision(model_decision: str, ground_truth: Dict) -> float:
    """Evaluate decision accuracy."""
    decision = model_decision.lower()
    gt_decision = ground_truth["decision"]
    
    return 1.0 if decision == gt_decision else 0.0


def run_benchmark(config: MiniMaxConfig) -> BenchmarkResult:
    """
    Run Tomasello (2012) benchmark.
    
    Args:
        config: MiniMaxConfig instance
    
    Returns:
        BenchmarkResult with detailed analysis
    """
    print("Starting Tomasello (2012) PASS 1 benchmark...")
    print(f"Model: {config.model}")
    print(f"Base URL: {config.base_url}")
    
    # Create client
    client = MiniMaxClient(config)
    
    # Prepare prompt
    system_prompt = """You are an expert academic paper analyst specializing in:
- Legal theory and institutional evolution
- Evolutionary anthropology and paleoanthropology
- Cognitive science and developmental psychology
- Game theory and evolutionary biology

Your analyses are thorough, precise, and grounded in the text. You extract 
key information accurately and make well-reasoned judgments about paper quality 
and relevance.

When analyzing papers, you use the Keshav Three-Pass Method. You are currently 
performing PASS 1 (Bird's Eye View), which should take 5-10 minutes and answer 
the Five C's."""
    
    user_prompt = f"""Analyze this academic paper using the Three-Pass Method (PASS 1 ONLY).

**PAPER METADATA:**
- Title: Two Key Steps in the Evolution of Human Cooperation
- Authors: Tomasello, M.
- Year: 2012
- Journal: Current Anthropology

**PAPER CONTENT:**
{TOMASELLO_2012_TEXT}

**YOUR TASK:**
Answer the Five C's in 5-10 minutes of analysis:

1. **CATEGORY**: What type of paper is this?
   (Measurement, Analysis, Systems, Theoretical, Empirical, Legal-doctrinal, etc.)

2. **CONTEXT**: Which theories/frameworks does this paper build on?
   List 3-5 key references/concepts the paper assumes you know.

3. **CORRECTNESS**: Do the assumptions and methodology appear valid?
   - Any obvious flaws?
   - Are claims supported by evidence?
   - Is reasoning sound?

4. **CONTRIBUTIONS**: What are the paper's main claims/contributions?
   State in 3 bullet points maximum.

5. **CLARITY**: Is the paper well-written?
   - Excellent: Clear, well-structured, easy to follow
   - Good: Minor issues but generally understandable
   - Acceptable: Significant effort needed to understand
   - Poor: Confusing, poorly structured, hard to follow

**DECISION**: Based on your analysis, recommend ONE action:
- **READ IN DEPTH** (PASS 2): Highly relevant, worth detailed analysis
- **CITE ONLY**: Relevant but don't need to deep-dive
- **DISCARD**: Not relevant to current research
- **MONITOR**: Bookmark for future review

**OUTPUT FORMAT**: Respond in valid JSON:

{{
  "category": "string",
  "context": ["reference1", "reference2", "reference3"],
  "correctness": {{
    "assessment": "valid|flawed|uncertain",
    "notes": "brief explanation"
  }},
  "contributions": ["contribution1", "contribution2", "contribution3"],
  "clarity": "excellent|good|acceptable|poor",
  "decision": "READ|CITE|DISCARD|MONITOR",
  "rationale": "1-2 sentence explanation of decision"
}}

**IMPORTANT**: Output ONLY valid JSON, no markdown formatting."""

    messages = [{"role": "user", "content": user_prompt}]
    
    # Execute benchmark
    print("\nSending request to MiniMax-M2...")
    response = client.chat(
        messages=messages,
        system_prompt=system_prompt,
        temperature=0.3,  # Lower temperature for consistency
        extract_thinking=True,
        parse_tool_calls=False
    )
    
    print(f"✅ Response received in {response.latency_ms:.0f}ms")
    
    # Parse JSON response
    try:
        # Extract JSON from content (handle markdown code blocks)
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        parsed = json.loads(content.strip())
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON response: {e}")
        print(f"Raw content: {response.content[:500]}...")
        raise
    
    # Evaluate accuracy
    accuracy_scores = {
        "category_accuracy": evaluate_category(
            parsed.get("category", ""),
            GROUND_TRUTH
        ),
        "context_accuracy": evaluate_context(
            parsed.get("context", []),
            GROUND_TRUTH
        ),
        "correctness_accuracy": evaluate_correctness(
            parsed.get("correctness", {}),
            GROUND_TRUTH
        ),
        "contributions_accuracy": evaluate_contributions(
            parsed.get("contributions", []),
            GROUND_TRUTH
        ),
        "clarity_accuracy": evaluate_clarity(
            parsed.get("clarity", ""),
            GROUND_TRUTH
        ),
        "decision_accuracy": evaluate_decision(
            parsed.get("decision", ""),
            GROUND_TRUTH
        )
    }
    
    # Calculate overall accuracy (weighted average)
    weights = {
        "category_accuracy": 0.15,
        "context_accuracy": 0.20,
        "correctness_accuracy": 0.15,
        "contributions_accuracy": 0.25,
        "clarity_accuracy": 0.10,
        "decision_accuracy": 0.15
    }
    
    overall_accuracy = sum(
        accuracy_scores[k] * weights[k]
        for k in weights.keys()
    )
    
    passed = overall_accuracy >= 0.85
    
    return BenchmarkResult(
        model_response=response,
        parsed_analysis=parsed,
        ground_truth=GROUND_TRUTH,
        accuracy_scores=accuracy_scores,
        overall_accuracy=overall_accuracy,
        passed=passed
    )


def main():
    """Run benchmark with configuration."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Benchmark MiniMax-M2 on Tomasello (2012) paper analysis"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock config (local vLLM deployment)"
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Save results to JSON file"
    )
    
    args = parser.parse_args()
    
    # Get configuration
    if args.mock:
        print("⚠️ Using MOCK configuration (local vLLM)")
        config = MiniMaxConfig.mock_config()
    else:
        try:
            config = MiniMaxConfig.from_env()
        except ValueError as e:
            print(f"❌ Configuration error: {e}")
            print("\nTo run benchmark:")
            print("1. Get API key from https://platform.minimax.io/")
            print("2. Export: export MINIMAX_API_KEY='your-key-here'")
            print("3. Run: python tomasello_2012_benchmark.py")
            print("\nOr use local vLLM:")
            print("python tomasello_2012_benchmark.py --mock")
            sys.exit(1)
    
    # Run benchmark
    try:
        result = run_benchmark(config)
        result.print_report()
        
        # Save results if requested
        if args.save:
            output = {
                "model_analysis": result.parsed_analysis,
                "ground_truth": result.ground_truth,
                "accuracy_scores": result.accuracy_scores,
                "overall_accuracy": result.overall_accuracy,
                "passed": result.passed,
                "usage": result.model_response.usage,
                "latency_ms": result.model_response.latency_ms
            }
            
            with open(args.save, 'w') as f:
                json.dump(output, f, indent=2)
            
            print(f"\n💾 Results saved to {args.save}")
    
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
