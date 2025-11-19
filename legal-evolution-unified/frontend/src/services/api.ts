import axios, { AxiosInstance } from 'axios';
import type {
  AnalysisRequest,
  ComprehensiveAnalysis,
  TransplantPrediction,
  GenealogicalNode,
  FitnessResult,
  APIResponse,
} from '../types';

class LegalEvolutionAPI {
  private client: AxiosInstance;

  constructor(baseURL: string = '/api/v1') {
    this.client = axios.create({
      baseURL,
      timeout: 120000, // 2 minutes for complex analyses
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string }> {
    const { data } = await this.client.get('/health');
    return data;
  }

  // Comprehensive Analysis
  async analyzeComprehensive(
    request: AnalysisRequest
  ): Promise<APIResponse<ComprehensiveAnalysis>> {
    const { data } = await this.client.post('/analyze', request);
    return data;
  }

  async generateAnalysisReport(
    request: AnalysisRequest
  ): Promise<APIResponse<{ report: string }>> {
    const { data } = await this.client.post('/analyze/report', request);
    return data;
  }

  // Fitness Analysis (JurisRank)
  async calculateFitness(
    conceptName: string,
    jurisdiction: string
  ): Promise<APIResponse<FitnessResult>> {
    const { data } = await this.client.post('/fitness', {
      concept_name: conceptName,
      jurisdiction,
    });
    return data;
  }

  // Genealogy Analysis (RootFinder)
  async getAncestors(
    conceptName: string,
    jurisdiction: string,
    maxDepth: number = 5
  ): Promise<APIResponse<GenealogicalNode[]>> {
    const { data } = await this.client.get(
      `/genealogy/ancestors/${encodeURIComponent(conceptName)}/${encodeURIComponent(jurisdiction)}`,
      { params: { max_depth: maxDepth } }
    );
    return data;
  }

  async getDescendants(
    conceptName: string,
    jurisdiction: string,
    maxDepth: number = 5
  ): Promise<APIResponse<GenealogicalNode[]>> {
    const { data } = await this.client.get(
      `/genealogy/descendants/${encodeURIComponent(conceptName)}/${encodeURIComponent(jurisdiction)}`,
      { params: { max_depth: maxDepth } }
    );
    return data;
  }

  async validateGenealogy(
    sourceConcept: string,
    sourceJurisdiction: string,
    targetConcept: string,
    targetJurisdiction: string
  ): Promise<APIResponse<any>> {
    const { data } = await this.client.post('/genealogy/validate', {
      source_concept: sourceConcept,
      source_jurisdiction: sourceJurisdiction,
      target_concept: targetConcept,
      target_jurisdiction: targetJurisdiction,
    });
    return data;
  }

  // Transplant Prediction (Iusmorfos)
  async predictTransplant(
    conceptName: string,
    sourceJurisdiction: string,
    targetJurisdictions: string[]
  ): Promise<APIResponse<TransplantPrediction[]>> {
    const { data } = await this.client.post('/transplant/predict', {
      concept_name: conceptName,
      source_jurisdiction: sourceJurisdiction,
      target_jurisdictions: targetJurisdictions,
    });
    return data;
  }

  async predictSingleTransplant(
    conceptName: string,
    sourceJurisdiction: string,
    targetJurisdiction: string
  ): Promise<APIResponse<TransplantPrediction>> {
    const { data } = await this.client.get(
      `/transplant/predict/${encodeURIComponent(conceptName)}/${encodeURIComponent(sourceJurisdiction)}/${encodeURIComponent(targetJurisdiction)}`
    );
    return data;
  }

  // Network Analysis
  async getNetworkStatus(): Promise<APIResponse<{
    data_loaded: boolean;
    similarity_calculated: boolean;
    network_built: boolean;
    num_concepts: number;
  }>> {
    const { data } = await this.client.get('/network/status');
    return data;
  }

  async getNetworkMetrics(
    conceptName: string
  ): Promise<APIResponse<{
    concept: string;
    metrics: {
      pagerank?: number;
      degree_centrality?: number;
      betweenness_centrality?: number;
    };
  }>> {
    const { data } = await this.client.get(
      `/network/metrics/${encodeURIComponent(conceptName)}`
    );
    return data;
  }

  // Bootstrap Validation
  async bootstrapValidate(
    group1: number[],
    group2: number[],
    nIterations: number = 1000
  ): Promise<APIResponse<{
    observed_difference: number;
    mean_bootstrap: number;
    std_bootstrap: number;
    ci_95: [number, number];
    p_value: number;
    significant: boolean;
    n_iterations: number;
  }>> {
    const { data } = await this.client.post('/bootstrap/validate', {
      group1,
      group2,
      n_iterations: nIterations,
    });
    return data;
  }
}

// Export singleton instance
export const api = new LegalEvolutionAPI();
export default api;
