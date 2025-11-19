// API Types for Legal Evolution Unified

export interface AnalysisRequest {
  concept_name: string;
  jurisdiction: string;
  include_genealogy?: boolean;
  include_network?: boolean;
}

export interface FitnessResult {
  fitness: number;
  ci_lower: number;
  ci_upper: number;
  p_value: number;
  significant: boolean;
  n_bootstrap_samples: number;
}

export interface GenealogicalNode {
  concept: string;
  jurisdiction: string;
  confidence: number;
  year?: number;
  influence_score?: number;
}

export interface GenealogicalGraph {
  nodes: GenealogicalNode[];
  edges: {
    source: string;
    target: string;
    weight: number;
    type: 'citation' | 'influence' | 'transplant';
  }[];
}

export interface ComprehensiveAnalysis {
  concept: string;
  jurisdiction: string;
  timestamp: string;
  fitness: FitnessResult;
  genealogy?: {
    ancestors: GenealogicalNode[];
    descendants: GenealogicalNode[];
    graph_nodes: number;
    graph_edges: number;
  };
  network?: {
    metrics: {
      pagerank?: number;
      degree_centrality?: number;
      betweenness_centrality?: number;
    };
    community: number;
    network_size: number;
  };
  summary: {
    fitness_significant: boolean;
    confidence_level: number;
    analysis_complete: boolean;
  };
}

export interface TransplantPrediction {
  concept_name: string;
  source_jurisdiction: string;
  target_jurisdiction: string;
  success_probability: number;
  confidence_interval: [number, number];
  recommendation: 'high' | 'moderate' | 'low' | 'not_recommended';
  risk_factors: string[];
  favorable_factors: string[];
  weird_classification: {
    source: 'WEIRD' | 'No-WEIRD';
    target: 'WEIRD' | 'No-WEIRD';
    compatibility_score: number;
  };
}

export interface SavedAnalysis {
  id: string;
  type: 'comprehensive' | 'transplant' | 'genealogy' | 'fitness';
  title: string;
  description?: string;
  data: ComprehensiveAnalysis | TransplantPrediction | any;
  created_at: string;
  tags: string[];
  exported_formats?: ('pdf' | 'latex' | 'json')[];
}

export interface RealityFilterResult {
  passed: boolean;
  confidence_score: number;
  verification_sources: {
    source: string;
    url?: string;
    reliability: number;
  }[];
  warnings: string[];
  hallucination_risk: 'low' | 'medium' | 'high';
}

export interface AcademicExport {
  format: 'pdf' | 'latex' | 'docx' | 'json';
  title: string;
  author?: string;
  abstract?: string;
  methodology: string;
  results: any;
  references: {
    title: string;
    authors: string[];
    year: number;
    doi?: string;
  }[];
  figures: {
    id: string;
    caption: string;
    data: any;
  }[];
}

export type AnalysisStatus = 'idle' | 'loading' | 'success' | 'error';

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  report?: string;
}
