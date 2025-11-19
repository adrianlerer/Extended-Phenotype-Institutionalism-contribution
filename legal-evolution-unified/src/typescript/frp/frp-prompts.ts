// ============================================================================
// FRACTAL REASONING ENGINE — PROMPT TEMPLATES
// ============================================================================

import { DomainContext, FRPLevel } from './frp-types';

/**
 * Base FRP prompt structure (domain-agnostic)
 */
export class FRPPromptTemplates {
  
  /**
   * Generate Level 1 (Macro View) prompt
   */
  static getL1Prompt(
    input_text: string,
    question: string,
    domain_context: DomainContext,
    previous_levels?: any
  ): string {
    return `# FRACTAL REASONING — LEVEL 1: MACRO VIEW

## Your Role
You are an expert analyst conducting a **strategic panorama** assessment.

## Domain Context
- Domain: ${domain_context.domain}
- Sub-domain: ${domain_context.sub_domain || 'general'}
- Jurisdiction: ${domain_context.jurisdiction || 'not specified'}
- Industry: ${domain_context.industry || 'not specified'}

## Task
Analyze the following ${domain_context.domain} material and provide a **global perspective**.

### Input Material:
\`\`\`
${input_text}
\`\`\`

### Analysis Question:
${question}

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

<think>
[Use this space to reason through your analysis before producing the output.
Consider multiple perspectives, test assumptions, identify what's NOT said in the text.]
</think>

## Your Level 1 Analysis:`;
  }

  /**
   * Generate Level 2 (Structure) prompt
   */
  static getL2Prompt(
    input_text: string,
    question: string,
    domain_context: DomainContext,
    L1_output: string
  ): string {
    return `# FRACTAL REASONING — LEVEL 2: INNER STRUCTURE

## Context from Level 1
You previously identified:
\`\`\`
${L1_output}
\`\`\`

## Level 2 Objective: SYSTEM ARCHITECTURE

Now decompose the **internal mechanisms** that govern this system.

### Input Material:
\`\`\`
${input_text}
\`\`\`

### Analysis Question:
${question}

## What to Identify:
1. **Key pillars** — What are the 3-5 foundational components?
2. **Operating principles** — What rules/norms govern behavior?
3. **Hidden mechanisms** — What drives outcomes beneath the surface?
4. **Structural constraints** — What limits degrees of freedom?

## Domain-Specific Focus (${domain_context.domain}):
${this.getDomainSpecificL2Guidance(domain_context)}

## Output Format
Produce **1 concise paragraph** (5-7 sentences) breaking down:
- Main structural components
- How they interact to produce the system's behavior
- What makes this architecture stable or fragile

<think>
[Reason through the system's internal logic:
- What are the load-bearing elements?
- What happens if one component fails?
- Are there redundancies or single points of failure?]
</think>

## Your Level 2 Analysis:`;
  }

  /**
   * Generate Level 3 (Interactions) prompt
   */
  static getL3Prompt(
    input_text: string,
    question: string,
    domain_context: DomainContext,
    L1_output: string,
    L2_output: string
  ): string {
    return `# FRACTAL REASONING — LEVEL 3: RELATIONAL DYNAMICS

## Context from Previous Levels

**Level 1 (Macro):**
\`\`\`
${L1_output}
\`\`\`

**Level 2 (Structure):**
\`\`\`
${L2_output}
\`\`\`

## Level 3 Objective: INTERACTIONS & EMERGENCE

Now analyze **how the structural components interact** to produce emergent behavior.

### Input Material:
\`\`\`
${input_text}
\`\`\`

### Analysis Question:
${question}

## What to Reveal:
1. **Synergies** — Which components reinforce each other?
2. **Tensions** — Where do contradictions or conflicts exist?
3. **Feedback loops** — What self-reinforcing or self-correcting dynamics emerge?
4. **Paradoxes** — What appears contradictory but actually reveals deeper logic?
5. **Phase transitions** — Under what conditions does the system shift behavior?

## Domain-Specific Focus (${domain_context.domain}):
${this.getDomainSpecificL3Guidance(domain_context)}

## Output Format
Produce **1 paragraph** (6-8 sentences) explaining:
- Key interactions between structural elements
- Emergent properties not predictable from components alone
- Critical dependencies or cascading effects
- System vulnerabilities or resilience patterns

<think>
[Map the interaction dynamics:
- What happens when component A changes? How does B respond?
- Are there tipping points or thresholds?
- What's the difference between intended and actual behavior?]
</think>

## Your Level 3 Analysis:`;
  }

  /**
   * Generate Level 4 (Fractal) prompt
   */
  static getL4Prompt(
    input_text: string,
    question: string,
    domain_context: DomainContext,
    L1_output: string,
    L2_output: string,
    L3_output: string
  ): string {
    return `# FRACTAL REASONING — LEVEL 4: FRACTAL PERSPECTIVE

## Context from Previous Levels

**Level 1 (Macro):**
\`\`\`
${L1_output}
\`\`\`

**Level 2 (Structure):**
\`\`\`
${L2_output}
\`\`\`

**Level 3 (Interactions):**
\`\`\`
${L3_output}
\`\`\`

## Level 4 Objective: MEANINGFUL ZOOM (Micro Mirrors Macro)

Now identify **a concrete detail, case, or clause** that encapsulates the entire system's logic in miniature.

### Input Material:
\`\`\`
${input_text}
\`\`\`

### Analysis Question:
${question}

## What to Find:
1. **The fractal case** — A specific example, clause, phrase, or event that contains the whole system's DNA
2. **How it reflects L1-L3** — Show explicitly how this micro-case embodies:
   - The macro stakes (L1)
   - The structural principles (L2)
   - The interaction dynamics (L3)
3. **Why it matters** — What this micro-view reveals that wasn't visible at higher levels

## Domain-Specific Focus (${domain_context.domain}):
${this.getDomainSpecificL4Guidance(domain_context)}

## Output Format
Produce **1 paragraph** (6-8 sentences) that:
- Identifies the specific fractal case (quote it if possible)
- Explains how it mirrors the macro system
- Reveals insight only visible at this zoom level

Structure:
- Opening: "In [specific element], the entire [system] logic appears in miniature..."
- Middle: Explicit connections to L1, L2, L3
- Closing: What this teaches us about the whole

<think>
[Search for the fractal:
- What small detail keeps repeating at different scales?
- Where does a single sentence/clause/decision capture everything?
- What example makes abstract principles concrete?]
</think>

## Your Level 4 Analysis:`;
  }

  /**
   * Generate Level 5 (Resonance) prompt
   */
  static getL5Prompt(
    input_text: string,
    question: string,
    domain_context: DomainContext,
    L1_output: string,
    L2_output: string,
    L3_output: string,
    L4_output: string
  ): string {
    return `# FRACTAL REASONING — LEVEL 5: STRATEGIC RESONANCE

## Context from All Previous Levels

**Level 1 (Macro):**
\`\`\`
${L1_output}
\`\`\`

**Level 2 (Structure):**
\`\`\`
${L2_output}
\`\`\`

**Level 3 (Interactions):**
\`\`\`
${L3_output}
\`\`\`

**Level 4 (Fractal):**
\`\`\`
${L4_output}
\`\`\`

## Level 5 Objective: STRATEGIC RESONANCE

Extract a **meta-principle or actionable lesson** that transcends this specific case.

### Original Input:
\`\`\`
${input_text}
\`\`\`

### Analysis Question:
${question}

## What to Synthesize:
1. **The universal pattern** — What principle operates here that applies elsewhere?
2. **Actionable insight** — What should decision-makers do differently?
3. **Epistemic lesson** — What does this teach about reasoning, system design, or strategy?
4. **Transferability** — How does this apply to other domains?

## Domain-Specific Focus (${domain_context.domain}):
${this.getDomainSpecificL5Guidance(domain_context)}

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

<think>
[Synthesize across all levels:
- What pattern emerges when you view L1-L4 together?
- What would someone in a different domain learn from this?
- What's the one insight that makes this analysis valuable beyond the immediate case?]
</think>

## Your Level 5 Analysis:`;
  }

  /**
   * Domain-specific guidance for each level
   */
  private static getDomainSpecificL2Guidance(context: DomainContext): string {
    const guidance: Record<string, string> = {
      legal: `
- Identify governing legal principles (contract law doctrines, statutory frameworks)
- Map clause interdependencies
- Reveal implicit assumptions in legal language`,
      
      compliance: `
- Identify regulatory requirements and standards
- Map compliance obligations across jurisdictions
- Reveal gaps between policy and implementation`,
      
      audit: `
- Identify control mechanisms and verification procedures
- Map risk exposure across business units
- Reveal systemic vulnerabilities in governance`,
      
      risk: `
- Identify risk vectors and threat models
- Map causal chains from trigger events to impact
- Reveal hidden correlations between risks`,
      
      due_diligence: `
- Identify material facts requiring verification
- Map information asymmetries between parties
- Reveal red flags or confirmation biases`,
      
      constitutional: `
- Identify constitutional principles and sovereignty doctrines
- Map power distribution between domestic/international law
- Reveal implicit assumptions about legal hierarchy`,
      
      political: `
- Identify political narratives and framing strategies
- Map actor coalitions and opposition structures
- Reveal implicit assumptions about legitimacy and authority`
    };
    
    return guidance[context.domain] || '- Identify key structural components\n- Map their relationships\n- Reveal hidden mechanisms';
  }

  private static getDomainSpecificL3Guidance(context: DomainContext): string {
    const guidance: Record<string, string> = {
      legal: `
- Analyze clause interactions (do they create contradictions?)
- Identify perverse incentives in contract structure
- Reveal how ambiguity distributes risk asymmetrically`,
      
      compliance: `
- Analyze regulatory overlap or conflict
- Identify compliance cost cascades
- Reveal how enforcement gaps incentivize non-compliance`,
      
      audit: `
- Analyze control interactions (do they complement or conflict?)
- Identify audit fatigue effects
- Reveal how controls can mask risks instead of mitigating them`,
      
      risk: `
- Analyze risk correlation and contagion paths
- Identify risk compensation behavior
- Reveal how mitigation strategies create new risks`,
      
      due_diligence: `
- Analyze information flow bottlenecks
- Identify verification paradoxes
- Reveal how transparency can obscure material facts`,
      
      constitutional: `
- Analyze tension between sovereignty and international obligations
- Identify feedback loops between domestic politics and legal strategy
- Reveal how constitutional rhetoric masks power struggles`,
      
      political: `
- Analyze narrative competition dynamics
- Identify amplification and suppression mechanisms
- Reveal how framing shapes policy space and legitimacy`
    };
    
    return guidance[context.domain] || '- Analyze component interactions\n- Identify feedback loops\n- Reveal emergent behavior';
  }

  private static getDomainSpecificL4Guidance(context: DomainContext): string {
    const guidance: Record<string, string> = {
      legal: `
- Find a specific clause/phrase that encapsulates the contract's core tension
- Show how it reflects party power dynamics (L1), legal architecture (L2), interaction effects (L3)`,
      
      compliance: `
- Find a specific requirement that encapsulates regulatory philosophy
- Show how it reflects policy goals (L1), rule structure (L2), enforcement dynamics (L3)`,
      
      audit: `
- Find a specific control that encapsulates governance approach
- Show how it reflects business risk (L1), control framework (L2), operational reality (L3)`,
      
      risk: `
- Find a specific scenario that encapsulates risk profile
- Show how it reflects threat landscape (L1), causal structure (L2), mitigation trade-offs (L3)`,
      
      due_diligence: `
- Find a specific data point that encapsulates material issue
- Show how it reflects transaction stakes (L1), information architecture (L2), verification challenges (L3)`,
      
      constitutional: `
- Find a specific constitutional provision, treaty clause, or court decision that encapsulates the sovereignty vs. globalism tension
- Show how it reflects systemic stakes (L1), legal architecture (L2), political dynamics (L3)`,
      
      political: `
- Find a specific speech excerpt, policy statement, or rhetorical move that encapsulates the narrative strategy
- Show how it reflects political stakes (L1), framing structure (L2), coalition dynamics (L3)`
    };
    
    return guidance[context.domain] || '- Find a concrete example that mirrors the whole system\n- Explain the fractal reflection';
  }

  private static getDomainSpecificL5Guidance(context: DomainContext): string {
    const guidance: Record<string, string> = {
      legal: `
- Extract principle about contract design, risk allocation, or legal strategy
- Provide actionable guidance for drafting or negotiation`,
      
      compliance: `
- Extract principle about regulatory design or compliance strategy
- Provide actionable guidance for policy implementation`,
      
      audit: `
- Extract principle about control design or governance
- Provide actionable guidance for risk management`,
      
      risk: `
- Extract principle about risk assessment or mitigation
- Provide actionable guidance for strategic decision-making`,
      
      due_diligence: `
- Extract principle about information verification or transaction strategy
- Provide actionable guidance for deal execution`,
      
      constitutional: `
- Extract principle about constitutional change, sovereignty dynamics, or legal evolution
- Provide actionable guidance for constitutional design or treaty negotiation`,
      
      political: `
- Extract principle about narrative competition, framing effects, or legitimacy construction
- Provide actionable guidance for political strategy or communication`
    };
    
    return guidance[context.domain] || '- Extract a universal principle\n- Provide actionable guidance';
  }
}
