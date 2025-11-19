"""
Unified Legal Evolution Pipeline

Integrates all analysis tools:
- Peralta: Bootstrap validation, network analysis, visualization
- JurisRank: Legal fitness scoring
- RootFinder: Genealogy tracking
- Iusmorfos: Transplant prediction

Provides single entry point for comprehensive legal concept analysis.
"""

import pandas as pd
import networkx as nx
from typing import Dict, List, Optional, Tuple
import logging

# Core Peralta modules
from code.analysis import LegalConceptAnalysis
from code.bootstrap import BootstrapValidator
# Note: visualization imported on demand (large module)

# Enhanced legal engines
from src.engines.enhanced_jurisrank import EnhancedJurisRank
from src.engines.rootfinder_adapter import RootFinderAdapter
from src.engines.iusmorfos_predictor import IusmorfosPredictor

logger = logging.getLogger(__name__)


class LegalEvolutionPipeline:
    """
    Comprehensive legal evolution analysis pipeline.
    
    Integrates:
    - Network analysis (Peralta)
    - Bootstrap validation (Peralta)
    - Legal fitness (JurisRank)
    - Genealogy tracking (RootFinder)
    - Transplant prediction (Iusmorfos)
    """
    
    def __init__(self, db=None, n_bootstrap: int = 1000):
        """
        Initialize unified pipeline.
        
        Parameters:
        -----------
        db : Database connection
            Connection to legal database
        n_bootstrap : int
            Bootstrap iterations for validation
        """
        logger.info("Initializing Legal Evolution Unified Pipeline")
        
        # Core Peralta modules
        self.analyzer = LegalConceptAnalysis()
        self.validator = BootstrapValidator(n_iterations=n_bootstrap)
        self.visualizer = None  # Loaded on demand
        
        # Enhanced legal tools
        self.jurisrank = EnhancedJurisRank(db=db, n_bootstrap_iterations=n_bootstrap)
        self.rootfinder = RootFinderAdapter(db=db)
        self.iusmorfos = IusmorfosPredictor(db=db, n_bootstrap=n_bootstrap)
        
        self.db = db
        
        logger.info("Pipeline initialized successfully")
    
    def load_visualization(self):
        """Load visualization module on demand (it's large)."""
        if self.visualizer is None:
            from code.visualization import PoliticalVisualization
            # Adapt for legal concepts
            self.visualizer = PoliticalVisualization()
            logger.info("Visualization module loaded")
    
    def comprehensive_analysis(
        self,
        concept_name: str,
        jurisdiction: str,
        include_genealogy: bool = True,
        include_network: bool = True
    ) -> Dict:
        """
        Perform comprehensive analysis of a legal concept.
        
        Integrates all analysis tools into unified report.
        
        Parameters:
        -----------
        concept_name : str
            Legal concept to analyze
        jurisdiction : str
            Jurisdiction context
        include_genealogy : bool
            Include genealogical analysis
        include_network : bool
            Include network analysis (requires dataset)
            
        Returns:
        --------
        dict : Comprehensive analysis results
        """
        logger.info(f"=== COMPREHENSIVE ANALYSIS: {concept_name} @ {jurisdiction} ===")
        
        results = {
            'concept': concept_name,
            'jurisdiction': jurisdiction,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        # 1. Legal Fitness (JurisRank + Bootstrap)
        logger.info("Step 1/4: Calculating legal fitness...")
        fitness = self.jurisrank.calculate_fitness_with_validation(
            concept_name, 
            jurisdiction
        )
        results['fitness'] = fitness
        logger.info(f"  Fitness: {fitness['fitness']:.4f} (CI: [{fitness['ci_lower']:.4f}, {fitness['ci_upper']:.4f}])")
        
        # 2. Genealogy Analysis (RootFinder)
        if include_genealogy:
            logger.info("Step 2/4: Tracing genealogy...")
            ancestors = self.rootfinder.find_conceptual_ancestors(
                concept_name, 
                jurisdiction
            )
            descendants = self.rootfinder.find_conceptual_descendants(
                concept_name, 
                jurisdiction
            )
            genealogy_graph = self.rootfinder.build_genealogy_graph(
                concept_name,
                jurisdiction,
                bidirectional=True
            )
            results['genealogy'] = {
                'ancestors': ancestors,
                'descendants': descendants,
                'graph_nodes': genealogy_graph.number_of_nodes(),
                'graph_edges': genealogy_graph.number_of_edges()
            }
            logger.info(f"  Genealogy: {len(ancestors)} ancestors, {len(descendants)} descendants")
        
        # 3. Network Analysis (Peralta) - requires dataset
        if include_network and self.analyzer.data is not None:
            logger.info("Step 3/4: Analyzing concept network...")
            if self.analyzer.similarity_matrix is None:
                self.analyzer.calculate_similarity_matrix()
            if self.analyzer.network is None:
                self.analyzer.create_network_from_similarities(threshold=0.7)
            
            metrics = self.analyzer.calculate_network_metrics()
            communities = self.analyzer.detect_communities()
            
            # Get metrics for this specific concept
            concept_metrics = {
                metric_name: metric_values.get(concept_name, 0.0)
                for metric_name, metric_values in metrics.items()
            }
            
            results['network'] = {
                'metrics': concept_metrics,
                'community': communities.get(concept_name, -1),
                'network_size': self.analyzer.network.number_of_nodes()
            }
            logger.info(f"  Network: PageRank={concept_metrics.get('pagerank', 0):.4f}")
        
        # 4. Summary Statistics
        logger.info("Step 4/4: Generating summary...")
        results['summary'] = {
            'fitness_significant': fitness['significant'],
            'confidence_level': 0.95,
            'analysis_complete': True
        }
        
        logger.info("=== ANALYSIS COMPLETE ===")
        
        return results
    
    def predict_transplant(
        self,
        concept_name: str,
        source_jurisdiction: str,
        target_jurisdiction: str
    ) -> Dict:
        """
        Predict transplant success using Iusmorfos.
        
        Parameters:
        -----------
        concept_name : str
            Legal concept
        source_jurisdiction : str
            Source jurisdiction
        target_jurisdiction : str
            Target jurisdiction
            
        Returns:
        --------
        dict : Transplant prediction
        """
        logger.info(f"Predicting transplant: {concept_name} from {source_jurisdiction} to {target_jurisdiction}")
        
        prediction = self.iusmorfos.predict_transplant_success(
            concept_name,
            source_jurisdiction,
            target_jurisdiction
        )
        
        return prediction
    
    def compare_transplant_targets(
        self,
        concept_name: str,
        source_jurisdiction: str,
        target_jurisdictions: List[str]
    ) -> pd.DataFrame:
        """
        Compare multiple potential transplant targets.
        
        Parameters:
        -----------
        concept_name : str
        source_jurisdiction : str
        target_jurisdictions : list
            
        Returns:
        --------
        pd.DataFrame : Comparison table
        """
        logger.info(f"Comparing {len(target_jurisdictions)} transplant targets for {concept_name}")
        
        return self.iusmorfos.compare_multiple_targets(
            concept_name,
            source_jurisdiction,
            target_jurisdictions
        )
    
    def validate_genealogical_hypothesis(
        self,
        source_concept: Tuple[str, str],
        target_concept: Tuple[str, str]
    ) -> Dict:
        """
        Validate hypothesis that concepts are genealogically related.
        
        Uses RootFinder + Peralta bootstrap validation.
        
        Parameters:
        -----------
        source_concept : tuple
            (concept_name, jurisdiction)
        target_concept : tuple
            (concept_name, jurisdiction)
            
        Returns:
        --------
        dict : Validation results
        """
        logger.info(f"Validating genealogical hypothesis: {source_concept} -> {target_concept}")
        
        validation = self.rootfinder.validate_transplant_hypothesis(
            source_concept,
            target_concept
        )
        
        return validation
    
    def generate_integrated_report(
        self,
        concept_name: str,
        jurisdiction: str,
        include_genealogy: bool = True,
        include_network: bool = False
    ) -> str:
        """
        Generate comprehensive integrated report.
        
        Parameters:
        -----------
        concept_name : str
        jurisdiction : str
        include_genealogy : bool
        include_network : bool
            
        Returns:
        --------
        str : Formatted report
        """
        logger.info("Generating integrated report...")
        
        # Run comprehensive analysis
        analysis = self.comprehensive_analysis(
            concept_name,
            jurisdiction,
            include_genealogy=include_genealogy,
            include_network=include_network
        )
        
        # Build report
        report = []
        report.append("=" * 80)
        report.append("LEGAL EVOLUTION UNIFIED - INTEGRATED ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Concept: {concept_name}")
        report.append(f"Jurisdiction: {jurisdiction}")
        report.append(f"Analysis timestamp: {analysis['timestamp']}")
        report.append("")
        
        # Fitness section
        fitness = analysis['fitness']
        report.append("═" * 80)
        report.append("1. LEGAL FITNESS (JurisRank + Bootstrap Validation)")
        report.append("═" * 80)
        report.append(f"  Fitness Score: {fitness['fitness']:.4f}")
        report.append(f"  95% Confidence Interval: [{fitness['ci_lower']:.4f}, {fitness['ci_upper']:.4f}]")
        report.append(f"  Statistical Significance: {'YES' if fitness['significant'] else 'NO'} (p={fitness['p_value']:.4f})")
        report.append(f"  Bootstrap Iterations: {fitness['n_bootstrap_samples']}")
        report.append("")
        
        # Genealogy section
        if 'genealogy' in analysis:
            genealogy = analysis['genealogy']
            report.append("═" * 80)
            report.append("2. GENEALOGY (RootFinder)")
            report.append("═" * 80)
            report.append(f"  Ancestors: {len(genealogy['ancestors'])}")
            report.append(f"  Descendants: {len(genealogy['descendants'])}")
            report.append(f"  Genealogy Graph: {genealogy['graph_nodes']} nodes, {genealogy['graph_edges']} edges")
            report.append("")
            
            if genealogy['ancestors']:
                report.append("  Top Ancestors:")
                for anc in genealogy['ancestors'][:3]:
                    report.append(f"    • {anc['concept']} @ {anc['jurisdiction']} (confidence: {anc['confidence']:.2f})")
            report.append("")
        
        # Network section
        if 'network' in analysis:
            network = analysis['network']
            report.append("═" * 80)
            report.append("3. NETWORK POSITION (Peralta Analysis)")
            report.append("═" * 80)
            metrics = network['metrics']
            report.append(f"  PageRank: {metrics.get('pagerank', 0):.6f}")
            report.append(f"  Degree Centrality: {metrics.get('degree_centrality', 0):.4f}")
            report.append(f"  Betweenness Centrality: {metrics.get('betweenness_centrality', 0):.4f}")
            report.append(f"  Community: {network['community']}")
            report.append(f"  Network Size: {network['network_size']} concepts")
            report.append("")
        
        # Summary
        report.append("═" * 80)
        report.append("SUMMARY")
        report.append("═" * 80)
        summary = analysis['summary']
        report.append(f"  Analysis Complete: {'✓' if summary['analysis_complete'] else '✗'}")
        report.append(f"  Fitness Validated: {'✓' if summary['fitness_significant'] else '✗'}")
        report.append(f"  Confidence Level: {summary['confidence_level']:.0%}")
        report.append("")
        report.append("=" * 80)
        report.append("Generated by Legal Evolution Unified Pipeline")
        report.append("Methodology: Peralta + JurisRank + RootFinder + Iusmorfos")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_results(
        self,
        results: Dict,
        output_dir: str = './results',
        formats: List[str] = ['json', 'html']
    ):
        """
        Export analysis results in multiple formats.
        
        Parameters:
        -----------
        results : dict
            Analysis results
        output_dir : str
            Output directory
        formats : list
            Export formats ('json', 'html', 'gephi')
        """
        import json
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        
        concept = results['concept']
        jurisdiction = results['jurisdiction']
        base_filename = f"{concept}_{jurisdiction}".replace(' ', '_')
        
        # JSON export
        if 'json' in formats:
            json_path = os.path.join(output_dir, f"{base_filename}.json")
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results exported to {json_path}")
        
        # HTML export
        if 'html' in formats:
            html_path = os.path.join(output_dir, f"{base_filename}.html")
            report = self.generate_integrated_report(concept, jurisdiction)
            with open(html_path, 'w') as f:
                f.write(f"<html><body><pre>{report}</pre></body></html>")
            logger.info(f"Report exported to {html_path}")
        
        # Gephi export (network)
        if 'gephi' in formats and self.analyzer.network is not None:
            gephi_path = os.path.join(output_dir, f"{base_filename}_network.gexf")
            self.analyzer.export_to_gephi(filepath=gephi_path)
            logger.info(f"Network exported to {gephi_path}")
