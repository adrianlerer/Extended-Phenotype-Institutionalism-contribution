// ============================================================================
// FRACTAL REASONING ENGINE — TYPE DEFINITIONS
// ============================================================================

/**
 * Domain context for FRP analysis
 */
export interface DomainContext {
  domain: 'legal' | 'compliance' | 'audit' | 'risk' | 'due_diligence' | 'constitutional' | 'political';
  sub_domain?: string;
  jurisdiction?: string;
  industry?: string;
  additional_context?: Record<string, any>;
}

/**
 * Fractal Reasoning Protocol levels
 */
export type FRPLevel = 'L1' | 'L2' | 'L3' | 'L4' | 'L5';

/**
 * Individual level output
 */
export interface FRPLevelOutput {
  level: FRPLevel;
  title: string;
  content: string;
  metadata?: {
    reasoning_steps?: string;
    confidence?: number;
    key_insights?: string[];
  };
}

/**
 * Complete FRP analysis result
 */
export interface FRPAnalysis {
  input_text: string;
  question: string;
  domain_context: DomainContext;
  levels: FRPLevelOutput[];
  timestamp: string;
  metadata?: {
    total_reasoning_time_ms?: number;
    model_used?: string;
    quality_score?: number;
  };
}

/**
 * FRP configuration
 */
export interface FRPConfig {
  domain_context: DomainContext;
  levels_to_execute: FRPLevel[];
  output_format: 'structured' | 'narrative' | 'compact';
  include_reasoning?: boolean;
  model_preferences?: {
    preferred_model?: string;
    temperature?: number;
    max_tokens?: number;
  };
}

/**
 * FRP prompt parameters
 */
export interface FRPPromptParams {
  input_text: string;
  question: string;
  domain_context: DomainContext;
  previous_levels?: Partial<Record<FRPLevel, string>>;
}

/**
 * Level metadata
 */
export interface LevelMetadata {
  level: FRPLevel;
  title: string;
  objective: string;
  typical_length: string;
  focus_areas: string[];
}

/**
 * FRP level definitions
 */
export const FRP_LEVEL_DEFINITIONS: Record<FRPLevel, LevelMetadata> = {
  L1: {
    level: 'L1',
    title: 'Macro View (Strategic Panorama)',
    objective: 'Provide high-level overview of what\'s at stake',
    typical_length: '3-5 sentences',
    focus_areas: ['Core issue', 'Stakeholder implications', 'Systemic relevance', 'Context']
  },
  L2: {
    level: 'L2',
    title: 'Inner Structure (System Architecture)',
    objective: 'Decompose internal mechanisms and structural components',
    typical_length: '1 paragraph (5-7 sentences)',
    focus_areas: ['Key pillars', 'Operating principles', 'Hidden mechanisms', 'Constraints']
  },
  L3: {
    level: 'L3',
    title: 'Interactions (Relational Dynamics)',
    objective: 'Analyze component interactions and emergent behavior',
    typical_length: '1 paragraph (6-8 sentences)',
    focus_areas: ['Synergies', 'Tensions', 'Feedback loops', 'Phase transitions']
  },
  L4: {
    level: 'L4',
    title: 'Fractal Perspective (Meaningful Zoom)',
    objective: 'Identify concrete detail that encapsulates entire system',
    typical_length: '1 paragraph (6-8 sentences)',
    focus_areas: ['Fractal case', 'Micro-macro reflection', 'Hidden insights']
  },
  L5: {
    level: 'L5',
    title: 'Strategic Resonance (Transferable Wisdom)',
    objective: 'Extract universal principle and actionable lessons',
    typical_length: '1 paragraph (4-6 sentences)',
    focus_areas: ['Universal pattern', 'Actionable insight', 'Transferability']
  }
};

/**
 * Domain-specific analysis focus
 */
export interface DomainAnalysisFocus {
  domain: string;
  L2_focus: string[];
  L3_focus: string[];
  L4_focus: string[];
  L5_focus: string[];
}

/**
 * Extended domain context for constitutional/political analysis
 */
export interface ConstitutionalContext extends DomainContext {
  domain: 'constitutional' | 'political';
  conflict_type?: 'treaty_challenge' | 'membership_withdrawal' | 'jurisdiction_dispute' | 'sovereignty_claim';
  narrative_type?: 'sovereignty' | 'globalism';
  case_id?: string;
  year?: number;
}
