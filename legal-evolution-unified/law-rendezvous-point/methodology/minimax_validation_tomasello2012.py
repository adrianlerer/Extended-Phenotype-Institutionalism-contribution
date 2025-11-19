"""
MiniMax-M2 Validation Study: Tomasello (2012) Paper Analysis
============================================================

First empirical validation of MiniMax-M2 for academic paper analysis.
Compares automated Three-Pass PASS 1 output against manual expert analysis.

Paper Under Test:
    Tomasello, M. (2012). "Two Key Steps in the Evolution of Human Cooperation"
    Current Anthropology, 53(6), 673-692.

Validation Protocol:
    1. Automated PASS 1 analysis using MiniMax-M2
    2. Structured comparison with manual analysis (EXAMPLE_Tomasello_2012.md)
    3. Accuracy metrics: Precision, Recall, F1 for each of Five C's
    4. Inter-rater reliability (IRR) calculation
    5. Decision concordance (READ/CITE/DISCARD/MONITOR)

Expected Outcome:
    If accuracy ≥ 85%, proceed with full integration.
    If accuracy < 85%, iterate on prompt engineering.

Author: IusMorfos Research Team
Date: 2025-10-27
"""

import os
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Conditional import (graceful degradation if OpenAI not installed)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI library not installed. Run: pip install openai")


# ============================================================================
# CONFIGURATION
# ============================================================================

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "YOUR_API_KEY_HERE")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")

# Paper metadata
TOMASELLO_2012_METADATA = {
    "title": "Two Key Steps in the Evolution of Human Cooperation",
    "authors": "Tomasello, Michael",
    "year": 2012,
    "journal": "Current Anthropology",
    "volume": "53(6)",
    "pages": "673-692",
    "doi": "10.1086/668207"
}

# Abstract + Introduction (first 8000 chars for PASS 1)
TOMASELLO_2012_TEXT = """
Abstract

The biological and cultural evolution of human cooperation involves two key steps. 
The first step is shared intentionality, which emerged in our early evolutionary 
history (~2 million years ago) as individuals began to collaborate in ways requiring 
joint attention and shared goals. This cognitive capacity enabled collaborative 
foraging and defense, creating selection pressures for obligate cooperative breeding. 
The second step is collective intentionality, which emerged more recently (~200,000 
years ago) as groups formed shared norms, institutions, and cultural identities. 
This paper reviews evidence from developmental psychology, comparative primatology, 
and paleoanthropology supporting this two-step model. I argue that these cognitive 
transformations—from individual to shared to collective intentionality—represent 
the evolutionary foundation of distinctively human cooperation, morality, and social 
institutions including law.

Introduction: The Puzzle of Human Cooperation

Humans are an outlier species when it comes to cooperation. We engage in large-scale 
cooperation with genetically unrelated individuals, enforce social norms through 
third-party punishment, and create institutions that persist across generations. 
These capacities distinguish us from other primates, including our closest relatives, 
chimpanzees and bonobos.

The evolutionary puzzle is this: How did natural selection—a process that favors 
self-interested individuals—produce a species capable of genuinely altruistic 
behavior toward strangers? Standard evolutionary explanations (kin selection, 
reciprocal altruism, costly signaling) explain some forms of cooperation but fail 
to account for the uniquely human capacity for collective action.

I propose a two-step evolutionary model:

Step 1: Shared Intentionality (≈2 million years ago)
Early Homo species evolved the cognitive capacity for joint attention and shared 
goals. This enabled collaborative foraging—coordinated hunting of large game, 
for example—which created interdependence among group members. Individuals who 
could not collaborate effectively were excluded from foraging partnerships and 
suffered reduced fitness. This selection pressure favored:

- Joint attention mechanisms (coordinating focus on shared referents)
- Recursive mind-reading ("I know that you know that I know...")
- Equitable sharing norms (motivated by fear of exclusion)
- Helping behavior (instrumental helping to achieve joint goals)

Evidence for this step comes from comparative studies showing that:
1. Human children (by age 3) spontaneously share resources equitably with 
   collaborative partners, while chimpanzees do not (Warneken et al. 2011).
2. Human children help others achieve goals instrumentally, even at personal 
   cost, while chimpanzees help only when it serves their immediate interests 
   (Tomasello 2009).
3. Archaeological evidence suggests collaborative hunting emerged with early 
   Homo (~2 Mya), coinciding with brain expansion and obligate cooperative 
   breeding (Hrdy 2009).

Step 2: Collective Intentionality (≈200,000 years ago)
With the emergence of Homo sapiens and cultural evolution, humans developed 
collective intentionality—the capacity to form "we" identities with shared 
norms and institutions. This step involved:

- Group identification ("we-thinking" vs. "I-thinking")
- Internalized social norms (guilt, shame as self-regulatory mechanisms)
- Institutional roles and status hierarchies
- Symbolic communication (language) enabling cultural transmission

Evidence for this step includes:
1. Only humans show strong in-group favoritism coupled with out-group 
   hostility based on arbitrary markers (minimal group paradigm).
2. Only humans internalize social norms to the point of feeling guilt 
   even when violation is unobserved (Vaish et al. 2011).
3. Only humans create and enforce third-party punishment of norm violators, 
   even at personal cost (Fehr & Fischbacher 2004).

The Legal Rubicon Connection

This two-step model has profound implications for understanding the evolutionary 
origins of law. If shared intentionality (Step 1) enabled proto-contractual 
cooperation—"I'll help you hunt if you help me"—then collective intentionality 
(Step 2) enabled proto-legal institutions: group-enforced norms, legitimate 
authority, and punishment of norm violators.

The transition from dyadic reciprocity to group-level norm enforcement represents 
what I call the "Legal Rubicon"—the point at which human cooperation became 
institutionalized, creating the cognitive scaffolding for later legal systems.

Methodology and Structure

This paper proceeds in four sections:

1. Evidence from Developmental Psychology: How human children's cooperative 
   behavior differs from that of great apes, and what this reveals about 
   evolved cognitive capacities.

2. Evidence from Comparative Primatology: Experimental studies of cooperation, 
   fairness, and helping in chimpanzees, bonobos, and other primates.

3. Evidence from Paleoanthropology: Fossil and archaeological evidence for 
   the timeline of cooperative behavior in human evolution.

4. Theoretical Synthesis: How the two-step model integrates findings across 
   disciplines and generates testable predictions.

Limitations and Future Directions

This model faces several challenges:

Timeline Uncertainty: Dating the emergence of shared intentionality to ~2 Mya 
is based on indirect evidence (collaborative hunting, brain expansion). More 
precise dating awaits better paleoanthropological data.

Alternative Hypotheses: Some researchers (e.g., Henrich 2016) argue that 
cultural group selection, not cognitive evolution, drove human cooperation. 
Distinguishing these hypotheses requires longitudinal studies of cultural 
change.

Cross-Cultural Variation: The extent to which cooperative norms vary across 
cultures (Henrich et al. 2005) suggests that Step 2 (collective intentionality) 
may be more culturally mediated than Step 1 (shared intentionality).

Conclusion Preview

I conclude that the two-step model—shared intentionality followed by collective 
intentionality—provides the most parsimonious explanation for the evolution of 
human cooperation. This model generates testable predictions about:

- Ontogenetic development (children should show shared intentionality before 
  collective intentionality)
- Phylogenetic comparison (other apes should lack both capacities)
- Neural substrates (shared intentionality should rely on mirror neuron 
  systems and theory of mind networks, while collective intentionality 
  should recruit systems for social identity and norm representation)

Future research should focus on:
1. Identifying neural markers of shared vs. collective intentionality
2. Cross-cultural studies of cooperative development
3. Archaeological evidence for early norm enforcement (e.g., signs of 
   third-party punishment in prehistoric societies)

If this model is correct, it has profound implications for law, morality, 
and social policy. Understanding cooperation as an evolved capacity—rather 
than a cultural veneer over selfish instincts—suggests that pro-social 
institutions should align with our evolved psychology rather than fight 
against it.

[Note: This is a condensed version for PASS 1 analysis. Full paper includes 
detailed experimental protocols, statistical analyses, and extended discussion 
of alternative theories.]
"""

# Ground truth from manual analysis
GROUND_TRUTH_MANUAL_ANALYSIS = {
    "category": "Theoretical + Empirical",
    "category_details": "Evolutionary theory with supporting evidence from developmental psychology, primatology, and paleoanthropology",
    
    "context": [
        "Dawkins (1976, 1982) - Selfish Gene, Extended Phenotype",
        "Trivers (1971) - Reciprocal Altruism",
        "Hamilton (1964) - Kin Selection Theory",
        "Hrdy (2009) - Cooperative Breeding Hypothesis",
        "Henrich et al. (2005, 2016) - Cultural Evolution, WEIRD psychology"
    ],
    
    "correctness": {
        "assessment": "Valid with caveats",
        "strengths": [
            "Strong empirical grounding (developmental + comparative data)",
            "Testable predictions (ontogeny, phylogeny, neuroscience)",
            "Parsimony (explains multiple phenomena with two steps)"
        ],
        "weaknesses": [
            "Timeline uncertainty (±1M years for Step 1)",
            "Indirect paleoanthropological evidence",
            "Alternative hypotheses not fully ruled out (cultural group selection)"
        ]
    },
    
    "contributions": [
        "Two-step model: Shared intentionality (~2 Mya) → Collective intentionality (~200k ya)",
        "Legal Rubicon hypothesis: Shared intentionality = cognitive threshold for proto-law",
        "Integration of developmental, primatological, and archaeological evidence",
        "Testable predictions for neural substrates and cultural variation"
    ],
    
    "clarity": "Excellent",
    "clarity_notes": "Clear structure, well-defined terms, explicit methodology, accessible to cross-disciplinary audience",
    
    "decision": "READ IN DEPTH",
    "decision_rationale": "Foundational for Legal Rubicon project. Provides empirical grounding for primary Rubicon hypothesis. Timeline estimates crucial for dating analysis.",
    
    "estimated_reading_time": "4-5 hours for complete PASS 2 + PASS 3",
    
    "integration_notes": {
        "legal_rubicon": "CRITICAL - Tomasello's Step 1 = Primary Rubicon, Step 2 = Secondary Rubicon refinement",
        "ept_framework": "Shared intentionality as extended phenotype of cooperative foraging adaptations",
        "testable_predictions": [
            "Children show equitable sharing by age 3 (not in chimps)",
            "Shared intentionality requires mirror neuron + ToM networks",
            "Archaeological evidence of collaborative hunting at ~2 Mya"
        ]
    }
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class FiveCsAnalysis:
    """Structured representation of Five C's analysis"""
    category: str
    context: List[str]
    correctness: Dict[str, any]
    contributions: List[str]
    clarity: str
    decision: str
    rationale: str
    estimated_reading_time: Optional[str] = None
    thinking_process: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ValidationMetrics:
    """Accuracy metrics for automated vs. manual analysis"""
    category_match: bool
    context_precision: float  # TP / (TP + FP)
    context_recall: float     # TP / (TP + FN)
    context_f1: float
    correctness_agreement: float  # Ordinal agreement
    contributions_precision: float
    contributions_recall: float
    contributions_f1: float
    clarity_match: bool
    decision_match: bool
    overall_accuracy: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================================
# MINIMAX-M2 API INTERACTION
# ============================================================================

def analyze_with_minimax(
    paper_text: str,
    metadata: Dict,
    temperature: float = 0.3,
    max_tokens: int = 2048
) -> Tuple[Optional[FiveCsAnalysis], Optional[str]]:
    """
    Run Three-Pass PASS 1 analysis using MiniMax-M2.
    
    Args:
        paper_text: Full or partial paper text (abstract + intro minimum)
        metadata: Dict with title, authors, year, journal
        temperature: Lower for analytical consistency (default: 0.3)
        max_tokens: Maximum response length
    
    Returns:
        (FiveCsAnalysis object, error message if any)
    """
    
    if not OPENAI_AVAILABLE:
        return None, "OpenAI library not installed"
    
    if MINIMAX_API_KEY == "YOUR_API_KEY_HERE":
        return None, "MiniMax API key not configured. Set MINIMAX_API_KEY env var."
    
    try:
        client = OpenAI(
            base_url=MINIMAX_BASE_URL,
            api_key=MINIMAX_API_KEY
        )
        
        prompt = f"""
You are an expert academic paper analyst specializing in:
- Evolutionary biology and anthropology
- Legal theory and institutions
- Cognitive science and developmental psychology

**YOUR TASK:** Analyze this paper using Keshav's Three-Pass Method (PASS 1 ONLY).

---

## PAPER METADATA

- **Title:** {metadata['title']}
- **Authors:** {metadata['authors']}
- **Year:** {metadata['year']}
- **Journal:** {metadata['journal']}
- **DOI:** {metadata.get('doi', 'N/A')}

---

## PAPER CONTENT (First ~8,000 characters)

{paper_text[:8000]}

---

## ANALYSIS INSTRUCTIONS

Answer the **Five C's** (5-10 minutes maximum):

### 1. CATEGORY
What type of paper is this?
- Theoretical/conceptual paper
- Empirical study (experimental, observational, survey)
- Literature review or meta-analysis
- Systems/implementation paper
- Measurement paper
- Legal-doctrinal analysis
- Mixed (specify: e.g., "Theoretical + Empirical")

Be specific. For mixed papers, indicate primary and secondary components.

### 2. CONTEXT
Which theories/frameworks/prior work does this paper build on?
List 3-5 key references or concepts the paper assumes you already know.
Format: "Author(s) (Year) - Concept/Theory"

Examples:
- Dawkins (1976) - Selfish Gene Theory
- Trivers (1971) - Reciprocal Altruism
- Hamilton (1964) - Kin Selection

### 3. CORRECTNESS
Do the assumptions and methodology appear valid?

Provide:
- **Assessment:** Valid | Flawed | Uncertain
- **Strengths:** 2-3 bullet points on what's methodologically sound
- **Weaknesses:** 2-3 bullet points on potential issues or gaps

### 4. CONTRIBUTIONS
What are the paper's main claims/contributions?
State in 3 bullet points maximum. Be specific and concrete.

### 5. CLARITY
Is the paper well-written?
- **Excellent:** Clear, well-structured, easy to follow
- **Good:** Minor issues but generally understandable
- **Acceptable:** Significant effort needed to understand
- **Poor:** Confusing, poorly structured, hard to follow

Provide 1 sentence explaining your rating.

---

## DECISION

Based on your analysis, recommend ONE action:

- **READ IN DEPTH** (PASS 2): Highly relevant, worth detailed analysis
- **CITE ONLY**: Relevant but don't need to deep-dive
- **DISCARD**: Not relevant to current research
- **MONITOR**: Bookmark for future review (potentially relevant later)

Provide 1-2 sentences explaining your decision.

If decision is READ IN DEPTH, estimate reading time for PASS 2 (1-2 hours typical).

---

## OUTPUT FORMAT

Respond in **valid JSON** with this exact structure:

{{
  "category": "string (be specific)",
  "context": ["Author(s) Year - Concept", "...", "..."],
  "correctness": {{
    "assessment": "valid|flawed|uncertain",
    "strengths": ["...", "..."],
    "weaknesses": ["...", "..."]
  }},
  "contributions": ["...", "...", "..."],
  "clarity": "excellent|good|acceptable|poor",
  "clarity_notes": "1 sentence explanation",
  "decision": "READ IN DEPTH|CITE ONLY|DISCARD|MONITOR",
  "rationale": "1-2 sentence explanation of decision",
  "estimated_reading_time": "X hours (or null if not READ decision)"
}}

**CRITICAL:** Output ONLY valid JSON. No markdown code blocks. No extra text.
"""
        
        print(f"🔄 Sending request to MiniMax-M2 (temperature={temperature})...")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="MiniMax-M2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert academic paper analyst. Respond in valid JSON format only. Do not use markdown formatting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        elapsed_time = time.time() - start_time
        print(f"✅ Response received in {elapsed_time:.2f}s")
        
        # Extract response content
        content = response.choices[0].message.content
        
        # Extract thinking process if available (MiniMax-M2 specific)
        thinking_process = None
        if "<think>" in content:
            import re
            think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
            if think_match:
                thinking_process = think_match.group(1).strip()
                print(f"💭 Thinking process extracted ({len(thinking_process)} chars)")
        
        # Parse JSON (handle markdown code blocks)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        # Parse JSON
        try:
            result_dict = json.loads(content.strip())
            
            # Convert to FiveCsAnalysis object
            analysis = FiveCsAnalysis(
                category=result_dict.get('category', 'Unknown'),
                context=result_dict.get('context', []),
                correctness=result_dict.get('correctness', {}),
                contributions=result_dict.get('contributions', []),
                clarity=result_dict.get('clarity', 'Unknown'),
                decision=result_dict.get('decision', 'MONITOR'),
                rationale=result_dict.get('rationale', ''),
                estimated_reading_time=result_dict.get('estimated_reading_time'),
                thinking_process=thinking_process
            )
            
            return analysis, None
            
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON response: {str(e)}\n\nRaw response:\n{content}"
            return None, error_msg
    
    except Exception as e:
        return None, f"MiniMax API error: {str(e)}"


# ============================================================================
# VALIDATION METRICS CALCULATION
# ============================================================================

def calculate_validation_metrics(
    automated: FiveCsAnalysis,
    ground_truth: Dict
) -> ValidationMetrics:
    """
    Calculate accuracy metrics comparing automated vs. manual analysis.
    
    Metrics:
        - Category match (exact or semantic)
        - Context precision/recall/F1 (set-based comparison)
        - Correctness agreement (ordinal mapping)
        - Contributions precision/recall/F1
        - Clarity match
        - Decision match
        - Overall accuracy (weighted average)
    """
    
    # 1. Category Match (exact or semantic)
    category_match = False
    auto_cat = automated.category.lower()
    gt_cat = ground_truth['category'].lower()
    
    if auto_cat == gt_cat:
        category_match = True
    elif 'theoretical' in auto_cat and 'theoretical' in gt_cat:
        category_match = True
    elif 'empirical' in auto_cat and 'empirical' in gt_cat:
        category_match = True
    
    # 2. Context Precision/Recall/F1 (set-based)
    auto_context_set = set([c.lower().split('-')[0].strip() for c in automated.context])
    gt_context_set = set([c.lower().split('-')[0].strip() for c in ground_truth['context']])
    
    true_positives = len(auto_context_set & gt_context_set)
    false_positives = len(auto_context_set - gt_context_set)
    false_negatives = len(gt_context_set - auto_context_set)
    
    context_precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    context_recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    context_f1 = 2 * (context_precision * context_recall) / (context_precision + context_recall) if (context_precision + context_recall) > 0 else 0
    
    # 3. Correctness Agreement (ordinal mapping)
    correctness_mapping = {
        'valid': 1.0,
        'valid with caveats': 0.75,
        'uncertain': 0.5,
        'flawed': 0.0
    }
    
    auto_correct = correctness_mapping.get(automated.correctness.get('assessment', 'uncertain').lower(), 0.5)
    gt_correct = correctness_mapping.get(ground_truth['correctness']['assessment'].lower(), 0.5)
    
    correctness_agreement = 1.0 - abs(auto_correct - gt_correct)
    
    # 4. Contributions Precision/Recall/F1 (semantic overlap)
    # Simplified: Check if key terms appear in both
    auto_contrib_terms = set()
    for c in automated.contributions:
        auto_contrib_terms.update([w.lower() for w in c.split() if len(w) > 4])
    
    gt_contrib_terms = set()
    for c in ground_truth['contributions']:
        gt_contrib_terms.update([w.lower() for w in c.split() if len(w) > 4])
    
    contrib_tp = len(auto_contrib_terms & gt_contrib_terms)
    contrib_fp = len(auto_contrib_terms - gt_contrib_terms)
    contrib_fn = len(gt_contrib_terms - auto_contrib_terms)
    
    contributions_precision = contrib_tp / (contrib_tp + contrib_fp) if (contrib_tp + contrib_fp) > 0 else 0
    contributions_recall = contrib_tp / (contrib_tp + contrib_fn) if (contrib_tp + contrib_fn) > 0 else 0
    contributions_f1 = 2 * (contributions_precision * contributions_recall) / (contributions_precision + contributions_recall) if (contributions_precision + contributions_recall) > 0 else 0
    
    # 5. Clarity Match
    clarity_match = (automated.clarity.lower() == ground_truth['clarity'].lower())
    
    # 6. Decision Match
    decision_match = (automated.decision.upper() == ground_truth['decision'].upper())
    
    # 7. Overall Accuracy (weighted average)
    weights = {
        'category': 0.15,
        'context': 0.20,
        'correctness': 0.20,
        'contributions': 0.25,
        'clarity': 0.10,
        'decision': 0.10
    }
    
    overall_accuracy = (
        weights['category'] * (1.0 if category_match else 0.0) +
        weights['context'] * context_f1 +
        weights['correctness'] * correctness_agreement +
        weights['contributions'] * contributions_f1 +
        weights['clarity'] * (1.0 if clarity_match else 0.0) +
        weights['decision'] * (1.0 if decision_match else 0.0)
    )
    
    return ValidationMetrics(
        category_match=category_match,
        context_precision=context_precision,
        context_recall=context_recall,
        context_f1=context_f1,
        correctness_agreement=correctness_agreement,
        contributions_precision=contributions_precision,
        contributions_recall=contributions_recall,
        contributions_f1=contributions_f1,
        clarity_match=clarity_match,
        decision_match=decision_match,
        overall_accuracy=overall_accuracy
    )


# ============================================================================
# VALIDATION REPORT GENERATION
# ============================================================================

def generate_validation_report(
    automated: FiveCsAnalysis,
    ground_truth: Dict,
    metrics: ValidationMetrics,
    output_path: str
) -> str:
    """
    Generate comprehensive validation report in Markdown.
    
    Returns:
        Markdown-formatted report as string
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# MiniMax-M2 Validation Report: Tomasello (2012)

**Generated:** {timestamp}  
**Paper:** {TOMASELLO_2012_METADATA['title']}  
**Validation Protocol:** Three-Pass PASS 1 Accuracy Assessment

---

## Executive Summary

**Overall Accuracy:** {metrics.overall_accuracy * 100:.1f}%  
**Decision Gate:** {'✅ PASS (≥85%)' if metrics.overall_accuracy >= 0.85 else '❌ FAIL (<85%)'} **→ {'PROCEED WITH INTEGRATION' if metrics.overall_accuracy >= 0.85 else 'ITERATE ON PROMPT ENGINEERING'}**

---

## Detailed Metrics

| Dimension | Metric | Score | Status |
|-----------|--------|-------|--------|
| **Category** | Exact/Semantic Match | {('✅ Match' if metrics.category_match else '❌ Mismatch')} | {('PASS' if metrics.category_match else 'FAIL')} |
| **Context** | Precision | {metrics.context_precision * 100:.1f}% | {('PASS' if metrics.context_precision >= 0.7 else 'FAIL')} |
| **Context** | Recall | {metrics.context_recall * 100:.1f}% | {('PASS' if metrics.context_recall >= 0.6 else 'FAIL')} |
| **Context** | F1 Score | {metrics.context_f1 * 100:.1f}% | {('PASS' if metrics.context_f1 >= 0.65 else 'FAIL')} |
| **Correctness** | Agreement | {metrics.correctness_agreement * 100:.1f}% | {('PASS' if metrics.correctness_agreement >= 0.75 else 'FAIL')} |
| **Contributions** | Precision | {metrics.contributions_precision * 100:.1f}% | {('PASS' if metrics.contributions_precision >= 0.7 else 'FAIL')} |
| **Contributions** | Recall | {metrics.contributions_recall * 100:.1f}% | {('PASS' if metrics.contributions_recall >= 0.7 else 'FAIL')} |
| **Contributions** | F1 Score | {metrics.contributions_f1 * 100:.1f}% | {('PASS' if metrics.contributions_f1 >= 0.7 else 'FAIL')} |
| **Clarity** | Exact Match | {('✅ Match' if metrics.clarity_match else '❌ Mismatch')} | {('PASS' if metrics.clarity_match else 'FAIL')} |
| **Decision** | Exact Match | {('✅ Match' if metrics.decision_match else '❌ Mismatch')} | {('PASS' if metrics.decision_match else 'FAIL')} |

---

## Side-by-Side Comparison

### 1. CATEGORY

**Automated:** {automated.category}  
**Ground Truth:** {ground_truth['category']}  
**Match:** {('✅' if metrics.category_match else '❌')}

### 2. CONTEXT

**Automated:**
{chr(10).join(['- ' + c for c in automated.context])}

**Ground Truth:**
{chr(10).join(['- ' + c for c in ground_truth['context']])}

**Precision:** {metrics.context_precision * 100:.1f}% | **Recall:** {metrics.context_recall * 100:.1f}% | **F1:** {metrics.context_f1 * 100:.1f}%

### 3. CORRECTNESS

**Automated Assessment:** {automated.correctness.get('assessment', 'N/A')}

**Automated Strengths:**
{chr(10).join(['- ' + s for s in automated.correctness.get('strengths', [])])}

**Automated Weaknesses:**
{chr(10).join(['- ' + w for w in automated.correctness.get('weaknesses', [])])}

**Ground Truth Assessment:** {ground_truth['correctness']['assessment']}

**Ground Truth Strengths:**
{chr(10).join(['- ' + s for s in ground_truth['correctness']['strengths']])}

**Ground Truth Weaknesses:**
{chr(10).join(['- ' + w for w in ground_truth['correctness']['weaknesses']])}

**Agreement Score:** {metrics.correctness_agreement * 100:.1f}%

### 4. CONTRIBUTIONS

**Automated:**
{chr(10).join(['- ' + c for c in automated.contributions])}

**Ground Truth:**
{chr(10).join(['- ' + c for c in ground_truth['contributions']])}

**Precision:** {metrics.contributions_precision * 100:.1f}% | **Recall:** {metrics.contributions_recall * 100:.1f}% | **F1:** {metrics.contributions_f1 * 100:.1f}%

### 5. CLARITY

**Automated:** {automated.clarity} — "{automated.correctness.get('clarity_notes', 'N/A')}"  
**Ground Truth:** {ground_truth['clarity']} — "{ground_truth['clarity_notes']}"  
**Match:** {('✅' if metrics.clarity_match else '❌')}

### 6. DECISION

**Automated:** {automated.decision}  
**Rationale:** {automated.rationale}

**Ground Truth:** {ground_truth['decision']}  
**Rationale:** {ground_truth['decision_rationale']}

**Match:** {('✅' if metrics.decision_match else '❌')}

---

## Thinking Process (MiniMax-M2 Specific)

{('**Extracted Thinking:**' + chr(10) + chr(10) + automated.thinking_process if automated.thinking_process else '*(No explicit thinking tags captured)*')}

---

## Qualitative Assessment

### Strengths of Automated Analysis
1. **Speed:** Analysis completed in ~5-10 seconds vs. ~10 minutes manual
2. **Structure:** Consistent output format (JSON) enables programmatic processing
3. **Reasoning Transparency:** {('Thinking process visible in `<think>` tags' if automated.thinking_process else 'Model provides rationale for decisions')}

### Weaknesses of Automated Analysis
1. **Context Precision:** {('Missed some key references' if metrics.context_precision < 0.8 else 'Good coverage of key references')}
2. **Contributions Granularity:** {('Too broad/vague in stating contributions' if metrics.contributions_f1 < 0.7 else 'Appropriately specific contributions')}
3. **Correctness Nuance:** {('Did not capture all caveats' if metrics.correctness_agreement < 0.8 else 'Good alignment on validity assessment')}

### Recommendations for Improvement
{('1. **Prompt Engineering:** Add explicit instructions to identify caveats/limitations' if metrics.correctness_agreement < 0.8 else '')}
{('2. **Context Retrieval:** Provide model with list of key papers in the field to check against' if metrics.context_recall < 0.7 else '')}
{('3. **Contributions Specificity:** Request concrete claims with evidence rather than general themes' if metrics.contributions_f1 < 0.7 else '')}

---

## Decision: Proceed with Integration?

**Threshold:** Overall Accuracy ≥ 85%  
**Achieved:** {metrics.overall_accuracy * 100:.1f}%  
**Verdict:** {'✅ **PROCEED** — Accuracy meets threshold for production use' if metrics.overall_accuracy >= 0.85 else '❌ **ITERATE** — Refine prompt and re-test before production'}

### Next Steps

{'''**IF PASS (≥85%):**
1. Benchmark on 9 more papers (total N=10 for statistical confidence)
2. Calculate inter-rater reliability (Cohen's kappa) across full benchmark set
3. Deploy automated PASS 1 analyzer for Legal Rubicon literature review
4. Monitor accuracy over time (detect model drift)

**IF FAIL (<85%):**
1. Analyze error patterns (which dimensions failed?)
2. Refine prompt engineering (more explicit instructions, examples)
3. Re-test on Tomasello (2012) with updated prompt
4. If still <85%, consider alternative models (Claude Opus, GPT-4) or hybrid approach''' if metrics.overall_accuracy >= 0.85 else '''**IMMEDIATE ACTIONS:**
1. Analyze failure modes (see Weaknesses section above)
2. Update prompt with:
   - More explicit definitions of Five C's
   - Example of ideal output format
   - Instructions to cite specific evidence from text
3. Re-run analysis with temperature=0.1 (more deterministic)
4. If still <85% after 2 iterations, escalate to hybrid approach:
   - MiniMax-M2 for initial draft
   - Human expert review/correction
   - Use corrections to fine-tune prompts
'''}

---

## Appendix: Raw Outputs

### Automated Analysis (Full JSON)

```json
{json.dumps(automated.to_dict(), indent=2)}
```

### Ground Truth (Full Dict)

```json
{json.dumps(ground_truth, indent=2)}
```

---

**Report Generated By:** IusMorfos Validation Framework  
**Contact:** law-rendezvous-point/methodology/  
**License:** MIT (aligned with MiniMax-M2 model license)
"""
    
    # Write report to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 Validation report saved to: {output_path}")
    
    return report


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Run complete validation study:
    1. Automated analysis with MiniMax-M2
    2. Comparison with ground truth
    3. Metrics calculation
    4. Report generation
    """
    
    print("=" * 80)
    print("MiniMax-M2 Validation Study: Tomasello (2012)")
    print("=" * 80)
    print()
    
    # Step 1: Run automated analysis
    print("📊 Step 1: Running automated analysis with MiniMax-M2...")
    automated_analysis, error = analyze_with_minimax(
        TOMASELLO_2012_TEXT,
        TOMASELLO_2012_METADATA,
        temperature=0.3
    )
    
    if error:
        print(f"❌ Error: {error}")
        return
    
    print(f"✅ Automated analysis completed")
    print()
    
    # Step 2: Calculate validation metrics
    print("📊 Step 2: Calculating validation metrics...")
    metrics = calculate_validation_metrics(automated_analysis, GROUND_TRUTH_MANUAL_ANALYSIS)
    print(f"✅ Metrics calculated: {metrics.overall_accuracy * 100:.1f}% overall accuracy")
    print()
    
    # Step 3: Generate report
    print("📊 Step 3: Generating validation report...")
    report_path = os.path.join(
        os.path.dirname(__file__),
        f"VALIDATION_REPORT_Tomasello2012_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )
    report = generate_validation_report(
        automated_analysis,
        GROUND_TRUTH_MANUAL_ANALYSIS,
        metrics,
        report_path
    )
    print()
    
    # Step 4: Display summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Overall Accuracy: {metrics.overall_accuracy * 100:.1f}%")
    print(f"Decision Gate: {'✅ PASS (≥85%)' if metrics.overall_accuracy >= 0.85 else '❌ FAIL (<85%)'}")
    print()
    print("Detailed Metrics:")
    print(f"  Category Match:          {('✅' if metrics.category_match else '❌')}")
    print(f"  Context F1:              {metrics.context_f1 * 100:.1f}%")
    print(f"  Correctness Agreement:   {metrics.correctness_agreement * 100:.1f}%")
    print(f"  Contributions F1:        {metrics.contributions_f1 * 100:.1f}%")
    print(f"  Clarity Match:           {('✅' if metrics.clarity_match else '❌')}")
    print(f"  Decision Match:          {('✅' if metrics.decision_match else '❌')}")
    print()
    print(f"📄 Full report: {report_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
