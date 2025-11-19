"""
Legal Concept Analysis Module
Adapted from Paper 11 Political Actor Analysis for Legal Evolution Studies

This module analyzes legal concepts using network analysis, similarity matrices,
and community detection - repurposing Peralta's methodological framework for legal systems.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from sklearn.preprocessing import StandardScaler
import networkx as nx
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalConceptAnalysis:
    """
    Legal concept analysis class adapted from Political Actor analysis.
    
    Analyzes legal concepts across jurisdictions using:
    - Fitness scores (legal adaptability)
    - Network centrality (influence in citation networks)
    - Similarity matrices (conceptual proximity)
    - Community detection (legal families)
    
    Original methodology from: peralta-metamorphosis
    Adapted for: Legal Evolution Unified platform
    """
    
    def __init__(self, random_state: Optional[int] = 42):
        """
        Initialize legal concept analyzer.
        
        Parameters:
        -----------
        random_state : int, optional
            Random seed for reproducibility
        """
        self.scaler = StandardScaler()
        self.random_state = random_state
        np.random.seed(random_state)
        
        # Store analysis results
        self.concept_names = []
        self.concept_features = None
        self.similarity_matrix = None
        self.network = None
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load legal concept data.
        
        Expected CSV format:
        | concept_name | jurisdiction | fitness_score | centrality | adoption_rate | persistence | rule_of_law | institutional_quality |
        
        Parameters:
        -----------
        filepath : str
            Path to CSV file with legal concept data
            
        Returns:
        --------
        pd.DataFrame : Loaded data
        """
        logger.info(f"Loading legal concept data from {filepath}")
        
        self.data = pd.read_csv(filepath)
        self.concept_names = self.data['concept_name'].tolist()
        
        # Define feature columns for multidimensional analysis
        feature_cols = [
            'fitness_score',         # JurisRank fitness
            'centrality',            # Network centrality
            'adoption_rate',         # Transplant success rate
            'persistence',           # Temporal stability
            'rule_of_law',          # Institutional context
            'institutional_quality'  # Governance quality
        ]
        
        # Extract features (with fallback for missing columns)
        available_features = [col for col in feature_cols if col in self.data.columns]
        self.concept_features = self.data[available_features].values
        
        logger.info(f"Loaded {len(self.data)} legal concepts with {len(available_features)} features")
        
        return self.data
    
    def calculate_similarity_matrix(self, method: str = 'euclidean', 
                                   normalize: bool = True) -> pd.DataFrame:
        """
        Calculate similarity matrix between legal concepts.
        
        Uses same algorithm as Peralta's political actor similarity.
        
        Parameters:
        -----------
        method : str
            Similarity method ('euclidean', 'cosine', 'correlation')
        normalize : bool
            Whether to normalize features before calculation
            
        Returns:
        --------
        pd.DataFrame : Similarity matrix [0, 1]
        """
        logger.info(f"Calculating similarity matrix using {method} method")
        
        # Normalize features
        if normalize:
            features_normalized = self.scaler.fit_transform(self.concept_features)
        else:
            features_normalized = self.concept_features
        
        # Calculate distances/similarities
        if method == 'euclidean':
            distances = euclidean_distances(features_normalized)
            # Convert distances to similarities [0,1]
            max_dist = distances.max()
            similarities = 1 - (distances / max_dist) if max_dist > 0 else np.ones_like(distances)
            
        elif method == 'cosine':
            similarities = cosine_similarity(features_normalized)
            # Cosine similarity is already in [-1, 1], map to [0, 1]
            similarities = (similarities + 1) / 2
            
        elif method == 'correlation':
            correlations = np.corrcoef(features_normalized)
            # Map correlation [-1, 1] to similarity [0, 1]
            similarities = (correlations + 1) / 2
            
        else:
            raise ValueError(f"Unknown similarity method: {method}")
        
        # Create DataFrame with concept names as index/columns
        self.similarity_matrix = pd.DataFrame(
            similarities,
            index=self.concept_names,
            columns=self.concept_names
        )
        
        logger.info(f"Similarity matrix shape: {self.similarity_matrix.shape}")
        logger.info(f"Average similarity: {np.mean(similarities[np.triu_indices_from(similarities, k=1)]):.4f}")
        
        return self.similarity_matrix
    
    def create_network_from_similarities(self, 
                                        similarity_matrix: Optional[pd.DataFrame] = None,
                                        threshold: float = 0.7,
                                        weighted: bool = True) -> nx.Graph:
        """
        Create NetworkX graph from similarity matrix.
        
        Same method as Peralta's political actor networks.
        
        Parameters:
        -----------
        similarity_matrix : pd.DataFrame, optional
            Similarity matrix (uses self.similarity_matrix if None)
        threshold : float
            Minimum similarity to create edge (default: 0.7)
        weighted : bool
            Whether to use similarity as edge weights
            
        Returns:
        --------
        nx.Graph : Legal concept network
        """
        if similarity_matrix is None:
            if self.similarity_matrix is None:
                raise ValueError("No similarity matrix available. Run calculate_similarity_matrix() first.")
            similarity_matrix = self.similarity_matrix
        
        logger.info(f"Creating network with similarity threshold: {threshold}")
        
        G = nx.Graph()
        
        # Add nodes
        for concept in similarity_matrix.index:
            G.add_node(concept)
        
        # Add edges where similarity >= threshold
        edges_added = 0
        for i, concept1 in enumerate(similarity_matrix.index):
            for j, concept2 in enumerate(similarity_matrix.columns):
                if i < j:  # Avoid duplicates (undirected graph)
                    similarity = similarity_matrix.iloc[i, j]
                    if similarity >= threshold:
                        if weighted:
                            G.add_edge(concept1, concept2, weight=similarity)
                        else:
                            G.add_edge(concept1, concept2)
                        edges_added += 1
        
        logger.info(f"Network created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        self.network = G
        return G
    
    def calculate_network_metrics(self, G: Optional[nx.Graph] = None) -> Dict[str, Dict[str, float]]:
        """
        Calculate network centrality metrics for legal concepts.
        
        Same metrics as Peralta's political actor analysis.
        
        Parameters:
        -----------
        G : nx.Graph, optional
            Network graph (uses self.network if None)
            
        Returns:
        --------
        dict : Dictionary of centrality metrics per concept
        """
        if G is None:
            if self.network is None:
                raise ValueError("No network available. Run create_network_from_similarities() first.")
            G = self.network
        
        logger.info("Calculating network centrality metrics")
        
        metrics = {
            'degree_centrality': nx.degree_centrality(G),
            'betweenness_centrality': nx.betweenness_centrality(G),
            'closeness_centrality': nx.closeness_centrality(G),
            'eigenvector_centrality': nx.eigenvector_centrality(G, max_iter=1000),
            'clustering_coefficient': nx.clustering(G),
            'pagerank': nx.pagerank(G)
        }
        
        # Log top concepts by PageRank
        pagerank_sorted = sorted(metrics['pagerank'].items(), key=lambda x: x[1], reverse=True)
        logger.info("Top 5 concepts by PageRank:")
        for concept, score in pagerank_sorted[:5]:
            logger.info(f"  {concept}: {score:.4f}")
        
        return metrics
    
    def detect_communities(self, G: Optional[nx.Graph] = None, 
                          method: str = 'louvain') -> Dict[str, int]:
        """
        Detect communities/clusters of similar legal concepts.
        
        Same method as Peralta's political actor clustering.
        
        Parameters:
        -----------
        G : nx.Graph, optional
            Network graph (uses self.network if None)
        method : str
            Community detection method ('louvain', 'greedy', 'label_propagation')
            
        Returns:
        --------
        dict : Mapping of concept -> community_id
        """
        if G is None:
            if self.network is None:
                raise ValueError("No network available. Run create_network_from_similarities() first.")
            G = self.network
        
        logger.info(f"Detecting communities using {method} method")
        
        if method == 'louvain':
            try:
                import community as community_louvain
                partition = community_louvain.best_partition(G)
                community_map = partition
            except ImportError:
                logger.warning("python-louvain not installed, falling back to greedy method")
                method = 'greedy'
        
        if method == 'greedy':
            from networkx.algorithms import community
            communities = community.greedy_modularity_communities(G)
            community_map = {}
            for idx, comm in enumerate(communities):
                for concept in comm:
                    community_map[concept] = idx
        
        elif method == 'label_propagation':
            from networkx.algorithms import community
            communities = community.label_propagation_communities(G)
            community_map = {}
            for idx, comm in enumerate(communities):
                for concept in comm:
                    community_map[concept] = idx
        
        n_communities = len(set(community_map.values()))
        logger.info(f"Detected {n_communities} communities")
        
        # Log community sizes
        from collections import Counter
        community_sizes = Counter(community_map.values())
        for comm_id, size in sorted(community_sizes.items()):
            logger.info(f"  Community {comm_id}: {size} concepts")
        
        return community_map
    
    def compare_concepts(self, concept1: str, concept2: str) -> Dict[str, float]:
        """
        Compare two legal concepts across all dimensions.
        
        Analogous to Peralta's López Rega-Milei comparison.
        
        Parameters:
        -----------
        concept1 : str
            First concept name
        concept2 : str
            Second concept name
            
        Returns:
        --------
        dict : Comparison metrics
        """
        if self.similarity_matrix is None:
            raise ValueError("No similarity matrix available. Run calculate_similarity_matrix() first.")
        
        if concept1 not in self.similarity_matrix.index:
            raise ValueError(f"Concept '{concept1}' not found in data")
        if concept2 not in self.similarity_matrix.columns:
            raise ValueError(f"Concept '{concept2}' not found in data")
        
        # Get similarity score
        similarity = self.similarity_matrix.loc[concept1, concept2]
        
        # Get feature vectors
        idx1 = self.concept_names.index(concept1)
        idx2 = self.concept_names.index(concept2)
        
        features1 = self.concept_features[idx1]
        features2 = self.concept_features[idx2]
        
        # Calculate feature-wise differences
        feature_diff = np.abs(features1 - features2)
        
        comparison = {
            'overall_similarity': float(similarity),
            'feature_differences': {
                f'feature_{i}': float(diff) 
                for i, diff in enumerate(feature_diff)
            },
            'euclidean_distance': float(np.linalg.norm(features1 - features2)),
            'cosine_similarity': float(np.dot(features1, features2) / 
                                     (np.linalg.norm(features1) * np.linalg.norm(features2)))
        }
        
        logger.info(f"Comparison: {concept1} vs {concept2}")
        logger.info(f"  Similarity: {similarity:.4f}")
        logger.info(f"  Euclidean distance: {comparison['euclidean_distance']:.4f}")
        
        return comparison
    
    def export_to_gephi(self, G: Optional[nx.Graph] = None, 
                       filepath: str = 'legal_network.gexf'):
        """
        Export network to Gephi format for visualization.
        
        Same method as Peralta.
        
        Parameters:
        -----------
        G : nx.Graph, optional
            Network graph (uses self.network if None)
        filepath : str
            Output file path
        """
        if G is None:
            if self.network is None:
                raise ValueError("No network available. Run create_network_from_similarities() first.")
            G = self.network
        
        nx.write_gexf(G, filepath)
        logger.info(f"Network exported to {filepath} (Gephi format)")
    
    def generate_summary_report(self) -> str:
        """
        Generate comprehensive summary report of analysis.
        
        Returns:
        --------
        str : Formatted report text
        """
        report = []
        report.append("=" * 70)
        report.append("LEGAL CONCEPT ANALYSIS REPORT")
        report.append("=" * 70)
        report.append("")
        
        if self.data is not None:
            report.append(f"Dataset: {len(self.data)} legal concepts")
            report.append(f"Features: {self.concept_features.shape[1]}")
            report.append("")
        
        if self.similarity_matrix is not None:
            avg_sim = np.mean(self.similarity_matrix.values[np.triu_indices_from(self.similarity_matrix.values, k=1)])
            report.append(f"Similarity Matrix:")
            report.append(f"  Average similarity: {avg_sim:.4f}")
            report.append(f"  Min similarity: {self.similarity_matrix.values.min():.4f}")
            report.append(f"  Max similarity: {self.similarity_matrix.values.max():.4f}")
            report.append("")
        
        if self.network is not None:
            report.append(f"Network:")
            report.append(f"  Nodes: {self.network.number_of_nodes()}")
            report.append(f"  Edges: {self.network.number_of_edges()}")
            report.append(f"  Density: {nx.density(self.network):.4f}")
            report.append(f"  Average clustering: {nx.average_clustering(self.network):.4f}")
            
            if nx.is_connected(self.network):
                report.append(f"  Average path length: {nx.average_shortest_path_length(self.network):.4f}")
            else:
                report.append(f"  Connected components: {nx.number_connected_components(self.network)}")
            report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


# Helper functions for common operations
def calculate_legal_fitness(concept_data: pd.DataFrame, 
                           weights: Optional[Dict[str, float]] = None) -> pd.Series:
    """
    Calculate legal fitness score from multiple dimensions.
    
    Parameters:
    -----------
    concept_data : pd.DataFrame
        Legal concept features
    weights : dict, optional
        Feature weights (default: equal weights)
        
    Returns:
    --------
    pd.Series : Fitness scores per concept
    """
    feature_cols = ['fitness_score', 'centrality', 'adoption_rate', 
                   'persistence', 'rule_of_law', 'institutional_quality']
    
    available_features = [col for col in feature_cols if col in concept_data.columns]
    
    if weights is None:
        weights = {col: 1.0 / len(available_features) for col in available_features}
    
    # Normalize features
    scaler = StandardScaler()
    normalized = pd.DataFrame(
        scaler.fit_transform(concept_data[available_features]),
        columns=available_features,
        index=concept_data.index
    )
    
    # Calculate weighted sum
    fitness = sum(normalized[col] * weights[col] for col in available_features)
    
    return fitness
