"""
Network Analyzer - IusSpace Dimensions 7 & 8

Dimension 7: Network Topology (Graph Density)
- Measures how interconnected the legal system is
- Graph density = actual edges / possible edges
- Somalia: 0.12 (fragmented), Somaliland: 0.68 (cohesive)

Dimension 8: Constitutional Centrality
- Measures how central the constitution is in the legal network
- Betweenness centrality: fraction of shortest paths through constitution
- Somalia: 0.35 (peripheral), Somaliland: 0.85 (hub)

These dimensions capture the structure of the iusespacio (legal space):
- Nodes: Legal norms (constitution, laws, court rulings, customs)
- Edges: Citations, modifications, hierarchies
- Strong networks: High density + high constitutional centrality
- Weak networks: Low density + low constitutional centrality

Key Finding (IusSpace Paper):
- Network topology predicts reform success
- High-density systems: reforms diffuse faster (2.1x)
- High-centrality constitutions: reforms more coherent (87% consistency)
- Fragmented systems: reforms fail 68% of time
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class NodeType(Enum):
    """Types of nodes in legal network."""
    CONSTITUTION = "constitution"
    CONSTITUTIONAL_AMENDMENT = "constitutional_amendment"
    STATUTE = "statute"                 # Congressional/Parliamentary law
    REGULATION = "regulation"           # Executive/Administrative rule
    COURT_RULING = "court_ruling"       # Judicial decisions
    CUSTOMARY_LAW = "customary_law"     # Traditional/customary norms
    INTERNATIONAL_TREATY = "international_treaty"
    REGIONAL_LAW = "regional_law"       # State/provincial law


class EdgeType(Enum):
    """Types of edges in legal network."""
    CITES = "cites"                     # Document A cites document B
    MODIFIES = "modifies"               # Document A amends document B
    REPEALS = "repeals"                 # Document A repeals document B
    HIERARCHY = "hierarchy"             # Document A subordinate to B
    INTERPRETS = "interprets"           # Court ruling interprets law
    IMPLEMENTS = "implements"           # Regulation implements statute
    DERIVES_FROM = "derives_from"       # Customary law recognized in written law


@dataclass
class LegalNode:
    """
    A node in the legal network.
    """
    node_id: str
    node_type: NodeType
    title: str
    date: datetime
    authority: str  # Legislative, executive, judicial, customary
    text: Optional[str] = None
    
    # Metadata
    jurisdiction: Optional[str] = None
    topic: Optional[str] = None
    status: str = "active"  # active, repealed, superseded


@dataclass
class LegalEdge:
    """
    An edge in the legal network.
    """
    source_id: str
    target_id: str
    edge_type: EdgeType
    date: datetime
    description: Optional[str] = None
    weight: float = 1.0  # Strength of connection


class NetworkAnalyzer:
    """
    Analyzes legal network topology and constitutional centrality.
    
    Methodology:
    1. Construct directed graph from legal corpus
    2. Calculate graph density (D7)
    3. Calculate betweenness centrality for constitution (D8)
    4. Compute additional network metrics
    5. Identify structural vulnerabilities
    
    Output:
    - Network Density (D7): 0.0-1.0
    - Constitutional Centrality (D8): 0.0-1.0
    - Community structure
    - Critical nodes (bridges)
    - Fragmentation index
    """
    
    def __init__(self):
        """Initialize Network Analyzer."""
        
        # Edge type weights (some connections stronger than others)
        self.edge_weights = {
            EdgeType.HIERARCHY: 1.5,      # Strong connection
            EdgeType.MODIFIES: 1.3,
            EdgeType.INTERPRETS: 1.2,
            EdgeType.CITES: 1.0,          # Baseline
            EdgeType.IMPLEMENTS: 1.1,
            EdgeType.DERIVES_FROM: 0.9,
            EdgeType.REPEALS: 0.5         # Negative connection
        }
    
    def construct_graph(
        self,
        nodes: List[LegalNode],
        edges: List[LegalEdge]
    ) -> nx.DiGraph:
        """
        Construct directed graph from legal corpus.
        
        Args:
            nodes: List of legal documents
            edges: List of connections between documents
        
        Returns:
            NetworkX directed graph
        """
        G = nx.DiGraph()
        
        # Add nodes
        for node in nodes:
            G.add_node(
                node.node_id,
                node_type=node.node_type.value,
                title=node.title,
                date=node.date,
                authority=node.authority,
                jurisdiction=node.jurisdiction,
                topic=node.topic,
                status=node.status
            )
        
        # Add edges
        for edge in edges:
            weight = self.edge_weights.get(edge.edge_type, 1.0) * edge.weight
            
            G.add_edge(
                edge.source_id,
                edge.target_id,
                edge_type=edge.edge_type.value,
                date=edge.date,
                weight=weight,
                description=edge.description
            )
        
        return G
    
    def analyze_topology(
        self,
        graph: nx.DiGraph,
        constitution_id: str
    ) -> Dict:
        """
        Complete network topology analysis.
        
        Args:
            graph: Legal network graph
            constitution_id: Node ID of constitution
        
        Returns:
            Dict with D7, D8, and additional metrics
        """
        if len(graph.nodes) == 0:
            return self._empty_result()
        
        # Dimension 7: Network Density
        density = self._calculate_density(graph)
        
        # Dimension 8: Constitutional Centrality
        if constitution_id in graph.nodes:
            centrality = self._calculate_constitutional_centrality(
                graph, constitution_id
            )
        else:
            centrality = 0.0
        
        # Additional metrics
        clustering = self._calculate_clustering(graph)
        communities = self._detect_communities(graph)
        fragmentation = self._calculate_fragmentation(graph)
        critical_nodes = self._identify_critical_nodes(graph)
        
        # Structural assessment
        health_score = self._assess_network_health(
            density, centrality, fragmentation
        )
        
        return {
            'network_density': float(density),          # D7
            'constitutional_centrality': float(centrality),  # D8
            'node_count': len(graph.nodes),
            'edge_count': len(graph.edges),
            'avg_degree': float(np.mean([d for n, d in graph.degree()])),
            'clustering_coefficient': float(clustering),
            'community_count': len(communities),
            'fragmentation_index': float(fragmentation),
            'critical_nodes': critical_nodes,
            'health_score': float(health_score),
            'interpretation': self._interpret_topology(density, centrality, health_score)
        }
    
    def _calculate_density(self, graph: nx.DiGraph) -> float:
        """
        Calculate network density (Dimension 7).
        
        Density = actual_edges / possible_edges
        For directed graph: possible_edges = n * (n - 1)
        """
        n = len(graph.nodes)
        
        if n <= 1:
            return 0.0
        
        possible_edges = n * (n - 1)
        actual_edges = len(graph.edges)
        
        density = actual_edges / possible_edges
        
        return density
    
    def _calculate_constitutional_centrality(
        self,
        graph: nx.DiGraph,
        constitution_id: str
    ) -> float:
        """
        Calculate betweenness centrality of constitution (Dimension 8).
        
        Betweenness = fraction of shortest paths that pass through constitution
        High values (0.7-1.0): Constitution is hub
        Low values (0.0-0.3): Constitution is peripheral
        """
        try:
            # Calculate betweenness centrality for all nodes
            centrality_dict = nx.betweenness_centrality(graph, normalized=True)
            
            # Get constitution's centrality
            constitution_centrality = centrality_dict.get(constitution_id, 0.0)
            
            return constitution_centrality
        
        except:
            # Graph may be disconnected or have other issues
            return 0.0
    
    def _calculate_clustering(self, graph: nx.DiGraph) -> float:
        """
        Calculate clustering coefficient.
        
        Measures how much nodes tend to cluster together.
        High clustering: tight-knit legal communities
        Low clustering: dispersed legal system
        """
        try:
            # Convert to undirected for clustering
            undirected = graph.to_undirected()
            clustering = nx.average_clustering(undirected)
            return clustering
        except:
            return 0.0
    
    def _detect_communities(self, graph: nx.DiGraph) -> List[Set[str]]:
        """
        Detect communities in legal network.
        
        Communities = clusters of densely connected norms
        Examples: criminal law cluster, civil law cluster, etc.
        """
        try:
            # Convert to undirected
            undirected = graph.to_undirected()
            
            # Use greedy modularity communities
            communities = list(nx.community.greedy_modularity_communities(undirected))
            
            return communities
        except:
            return []
    
    def _calculate_fragmentation(self, graph: nx.DiGraph) -> float:
        """
        Calculate fragmentation index.
        
        Fragmentation = 1 - (size of largest component / total nodes)
        0.0 = fully connected, 1.0 = completely fragmented
        """
        if len(graph.nodes) == 0:
            return 0.0
        
        # Find strongly connected components
        components = list(nx.strongly_connected_components(graph))
        
        if not components:
            return 1.0
        
        largest_component_size = max(len(c) for c in components)
        total_nodes = len(graph.nodes)
        
        fragmentation = 1.0 - (largest_component_size / total_nodes)
        
        return fragmentation
    
    def _identify_critical_nodes(
        self,
        graph: nx.DiGraph,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Identify critical nodes (bridges) in network.
        
        Critical nodes = nodes whose removal would fragment network
        These are vulnerable points in legal system
        """
        try:
            # Calculate articulation points
            undirected = graph.to_undirected()
            articulation_points = list(nx.articulation_points(undirected))
            
            # Calculate betweenness for ranking
            centrality = nx.betweenness_centrality(graph, normalized=True)
            
            # Rank critical nodes
            critical = []
            for node_id in articulation_points[:top_n]:
                node_data = graph.nodes[node_id]
                critical.append({
                    'node_id': node_id,
                    'title': node_data.get('title', 'Unknown'),
                    'node_type': node_data.get('node_type', 'unknown'),
                    'centrality': float(centrality.get(node_id, 0.0))
                })
            
            # Sort by centrality
            critical.sort(key=lambda x: x['centrality'], reverse=True)
            
            return critical[:top_n]
        
        except:
            return []
    
    def _assess_network_health(
        self,
        density: float,
        centrality: float,
        fragmentation: float
    ) -> float:
        """
        Assess overall network health (0.0-1.0).
        
        Healthy network:
        - High density (0.5+)
        - High constitutional centrality (0.6+)
        - Low fragmentation (0.2-)
        """
        # Weights for each factor
        density_weight = 0.40
        centrality_weight = 0.35
        fragmentation_weight = 0.25
        
        # Density score (higher is better)
        density_score = density
        
        # Centrality score (higher is better)
        centrality_score = centrality
        
        # Fragmentation score (lower is better, so invert)
        fragmentation_score = 1.0 - fragmentation
        
        # Weighted average
        health = (
            density_weight * density_score +
            centrality_weight * centrality_score +
            fragmentation_weight * fragmentation_score
        )
        
        return np.clip(health, 0.0, 1.0)
    
    def _interpret_topology(
        self,
        density: float,
        centrality: float,
        health: float
    ) -> str:
        """
        Human-readable interpretation of network topology.
        """
        # Density interpretation
        if density >= 0.6:
            density_desc = "highly interconnected"
        elif density >= 0.4:
            density_desc = "moderately connected"
        elif density >= 0.2:
            density_desc = "loosely connected"
        else:
            density_desc = "fragmented"
        
        # Centrality interpretation
        if centrality >= 0.7:
            centrality_desc = "strong constitutional hub"
        elif centrality >= 0.5:
            centrality_desc = "moderate constitutional centrality"
        elif centrality >= 0.3:
            centrality_desc = "weak constitutional centrality"
        else:
            centrality_desc = "peripheral constitution"
        
        # Health interpretation
        if health >= 0.7:
            health_desc = "Excellent"
        elif health >= 0.5:
            health_desc = "Good"
        elif health >= 0.3:
            health_desc = "Fair"
        else:
            health_desc = "Poor"
        
        return (
            f"{health_desc} network health (D7={density:.2f}, D8={centrality:.2f}). "
            f"Legal system is {density_desc} with {centrality_desc}."
        )
    
    def _empty_result(self) -> Dict:
        """Return empty result when no data available."""
        return {
            'network_density': 0.0,
            'constitutional_centrality': 0.0,
            'node_count': 0,
            'edge_count': 0,
            'avg_degree': 0.0,
            'clustering_coefficient': 0.0,
            'community_count': 0,
            'fragmentation_index': 1.0,
            'critical_nodes': [],
            'health_score': 0.0,
            'interpretation': "No network data available"
        }
    
    def compare_networks(
        self,
        country1: str,
        graph1: nx.DiGraph,
        constitution1_id: str,
        country2: str,
        graph2: nx.DiGraph,
        constitution2_id: str
    ) -> Dict:
        """
        Compare network topology between two legal systems.
        """
        analysis1 = self.analyze_topology(graph1, constitution1_id)
        analysis2 = self.analyze_topology(graph2, constitution2_id)
        
        # Calculate differences
        density_diff = analysis1['network_density'] - analysis2['network_density']
        centrality_diff = analysis1['constitutional_centrality'] - analysis2['constitutional_centrality']
        health_diff = analysis1['health_score'] - analysis2['health_score']
        
        # Determine which is stronger
        if health_diff > 0.1:
            stronger = country1
            weaker = country2
        elif health_diff < -0.1:
            stronger = country2
            weaker = country1
        else:
            stronger = None
            weaker = None
        
        return {
            'country1': country1,
            'country1_analysis': analysis1,
            'country2': country2,
            'country2_analysis': analysis2,
            'density_difference': float(density_diff),
            'centrality_difference': float(centrality_diff),
            'health_difference': float(health_diff),
            'stronger_network': stronger,
            'weaker_network': weaker,
            'interpretation': self._interpret_comparison(
                country1, country2, stronger, health_diff
            )
        }
    
    def _interpret_comparison(
        self,
        country1: str,
        country2: str,
        stronger: Optional[str],
        health_diff: float
    ) -> str:
        """Interpret network comparison."""
        if stronger is None:
            return f"{country1} and {country2} have similar network health."
        
        magnitude = "significantly" if abs(health_diff) > 0.3 else "moderately"
        
        return (
            f"{stronger} has a {magnitude} stronger legal network "
            f"(health difference: {abs(health_diff):.2f}). "
            f"Reforms in {stronger} are more likely to diffuse successfully."
        )


# Example usage
if __name__ == "__main__":
    # Create sample legal networks
    
    # Somalia: Fragmented system (low density, low centrality)
    somalia_nodes = [
        LegalNode("const_1977", NodeType.CONSTITUTION, "Constitution 1977", datetime(1977, 1, 1), "legislative"),
        LegalNode("law_01", NodeType.STATUTE, "Civil Code", datetime(1980, 1, 1), "legislative"),
        LegalNode("law_02", NodeType.STATUTE, "Criminal Code", datetime(1982, 1, 1), "legislative"),
        LegalNode("custom_01", NodeType.CUSTOMARY_LAW, "Xeer (Traditional Law)", datetime(1900, 1, 1), "customary"),
        LegalNode("ruling_01", NodeType.COURT_RULING, "Supreme Court Ruling 1985", datetime(1985, 1, 1), "judicial"),
    ]
    
    somalia_edges = [
        LegalEdge("law_01", "const_1977", EdgeType.HIERARCHY, datetime(1980, 1, 1)),
        LegalEdge("law_02", "const_1977", EdgeType.HIERARCHY, datetime(1982, 1, 1)),
        # Note: Customary law operates separately, few connections
    ]
    
    # Somaliland: Cohesive system (high density, high centrality)
    somaliland_nodes = [
        LegalNode("const_2001", NodeType.CONSTITUTION, "Constitution 2001", datetime(2001, 5, 31), "legislative"),
        LegalNode("law_01", NodeType.STATUTE, "Civil Procedure Law", datetime(2002, 1, 1), "legislative"),
        LegalNode("law_02", NodeType.STATUTE, "Criminal Code", datetime(2003, 1, 1), "legislative"),
        LegalNode("custom_01", NodeType.CUSTOMARY_LAW, "Xeer (Codified)", datetime(2002, 6, 1), "customary"),
        LegalNode("ruling_01", NodeType.COURT_RULING, "Supreme Court Ruling 2005", datetime(2005, 1, 1), "judicial"),
        LegalNode("law_03", NodeType.STATUTE, "Land Law", datetime(2004, 1, 1), "legislative"),
        LegalNode("ruling_02", NodeType.COURT_RULING, "Constitutional Review 2010", datetime(2010, 1, 1), "judicial"),
    ]
    
    somaliland_edges = [
        LegalEdge("law_01", "const_2001", EdgeType.HIERARCHY, datetime(2002, 1, 1)),
        LegalEdge("law_02", "const_2001", EdgeType.HIERARCHY, datetime(2003, 1, 1)),
        LegalEdge("law_03", "const_2001", EdgeType.HIERARCHY, datetime(2004, 1, 1)),
        LegalEdge("custom_01", "const_2001", EdgeType.DERIVES_FROM, datetime(2002, 6, 1)),
        LegalEdge("ruling_01", "law_01", EdgeType.INTERPRETS, datetime(2005, 1, 1)),
        LegalEdge("ruling_01", "const_2001", EdgeType.INTERPRETS, datetime(2005, 1, 1)),
        LegalEdge("ruling_02", "const_2001", EdgeType.INTERPRETS, datetime(2010, 1, 1)),
        LegalEdge("law_01", "law_02", EdgeType.CITES, datetime(2002, 1, 1)),
        LegalEdge("law_03", "custom_01", EdgeType.CITES, datetime(2004, 1, 1)),
    ]
    
    # Initialize analyzer
    analyzer = NetworkAnalyzer()
    
    # Construct graphs
    somalia_graph = analyzer.construct_graph(somalia_nodes, somalia_edges)
    somaliland_graph = analyzer.construct_graph(somaliland_nodes, somaliland_edges)
    
    print("=" * 80)
    print("Legal Network Topology Analysis")
    print("=" * 80)
    
    # Analyze Somalia
    print("\n1. Somalia:")
    print("-" * 80)
    somalia_analysis = analyzer.analyze_topology(somalia_graph, "const_1977")
    print(f"Network Density (D7): {somalia_analysis['network_density']:.3f}")
    print(f"Constitutional Centrality (D8): {somalia_analysis['constitutional_centrality']:.3f}")
    print(f"Nodes: {somalia_analysis['node_count']}, Edges: {somalia_analysis['edge_count']}")
    print(f"Fragmentation: {somalia_analysis['fragmentation_index']:.3f}")
    print(f"Health Score: {somalia_analysis['health_score']:.3f}")
    print(f"\n{somalia_analysis['interpretation']}")
    
    # Analyze Somaliland
    print("\n2. Somaliland:")
    print("-" * 80)
    somaliland_analysis = analyzer.analyze_topology(somaliland_graph, "const_2001")
    print(f"Network Density (D7): {somaliland_analysis['network_density']:.3f}")
    print(f"Constitutional Centrality (D8): {somaliland_analysis['constitutional_centrality']:.3f}")
    print(f"Nodes: {somaliland_analysis['node_count']}, Edges: {somaliland_analysis['edge_count']}")
    print(f"Fragmentation: {somaliland_analysis['fragmentation_index']:.3f}")
    print(f"Health Score: {somaliland_analysis['health_score']:.3f}")
    print(f"\n{somaliland_analysis['interpretation']}")
    
    # Compare
    print("\n3. Comparison:")
    print("-" * 80)
    comparison = analyzer.compare_networks(
        "Somalia", somalia_graph, "const_1977",
        "Somaliland", somaliland_graph, "const_2001"
    )
    print(f"Density Difference: {comparison['density_difference']:.3f}")
    print(f"Centrality Difference: {comparison['centrality_difference']:.3f}")
    print(f"Health Difference: {comparison['health_difference']:.3f}")
    print(f"Stronger Network: {comparison['stronger_network']}")
    print(f"\n{comparison['interpretation']}")
