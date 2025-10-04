"""
Client-Service Network Analysis Module

This module provides functionality for analyzing client-service networks,
including comparison between different time periods (pre vs. post event).
"""

import networkx as nx
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import matplotlib.pyplot as plt
from collections import defaultdict


class ClientServiceNetwork:
    """
    Represents a client-service network with metadata support.
    
    Attributes:
        graph: NetworkX graph object
        metadata: Dictionary containing service metadata
        weighted: Boolean indicating if edges are weighted
    """
    
    def __init__(self, weighted: bool = True):
        """
        Initialize a client-service network.
        
        Args:
            weighted: If True, edges can have weights. Default is True.
        """
        self.graph = nx.Graph() if not weighted else nx.Graph()
        self.metadata = {}
        self.weighted = weighted
        
    def add_service(self, service_id: str, metadata: Dict[str, Any] = None):
        """
        Add a service node to the network.
        
        Args:
            service_id: Unique identifier for the service
            metadata: Dictionary containing service metadata
        """
        self.graph.add_node(service_id, node_type='service')
        if metadata:
            self.metadata[service_id] = metadata
            
    def add_client(self, client_id: str):
        """
        Add a client node to the network.
        
        Args:
            client_id: Unique identifier for the client
        """
        self.graph.add_node(client_id, node_type='client')
        
    def add_connection(self, client_id: str, service_id: str, weight: float = 1.0):
        """
        Add a connection between a client and a service.
        
        Args:
            client_id: Client identifier
            service_id: Service identifier
            weight: Connection weight (default: 1.0)
        """
        if self.weighted:
            self.graph.add_edge(client_id, service_id, weight=weight)
        else:
            self.graph.add_edge(client_id, service_id)
            
    def load_from_edgelist(self, filepath: str, weighted: bool = None):
        """
        Load network from an edge list file.
        
        Args:
            filepath: Path to edge list file
            weighted: Override weighted setting
        """
        if weighted is not None:
            self.weighted = weighted
            
        if self.weighted:
            self.graph = nx.read_weighted_edgelist(filepath)
        else:
            self.graph = nx.read_edgelist(filepath)
            
    def load_metadata(self, filepath: str):
        """
        Load service metadata from a CSV file.
        
        Args:
            filepath: Path to metadata CSV file
        """
        df = pd.read_csv(filepath)
        for _, row in df.iterrows():
            service_id = row['service_id']
            metadata = row.to_dict()
            del metadata['service_id']
            self.metadata[service_id] = metadata
            
    def get_service_metadata(self, service_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific service.
        
        Args:
            service_id: Service identifier
            
        Returns:
            Dictionary containing service metadata
        """
        return self.metadata.get(service_id, {})
    
    def number_of_nodes(self) -> int:
        """Return the number of nodes in the network."""
        return self.graph.number_of_nodes()
    
    def number_of_edges(self) -> int:
        """Return the number of edges in the network."""
        return self.graph.number_of_edges()


class NetworkMetrics:
    """
    Calculate various network metrics for analysis.
    """
    
    @staticmethod
    def calculate_centrality(network: ClientServiceNetwork) -> Dict[str, Dict[str, float]]:
        """
        Calculate various centrality metrics for all nodes.
        
        Args:
            network: ClientServiceNetwork instance
            
        Returns:
            Dictionary containing different centrality measures
        """
        metrics = {
            'degree': nx.degree_centrality(network.graph),
            'betweenness': nx.betweenness_centrality(network.graph),
            'closeness': nx.closeness_centrality(network.graph),
        }
        
        # Eigenvector centrality may not converge for all graphs
        try:
            metrics['eigenvector'] = nx.eigenvector_centrality(network.graph, max_iter=1000)
        except:
            metrics['eigenvector'] = {node: 0.0 for node in network.graph.nodes()}
            
        return metrics
    
    @staticmethod
    def calculate_connectivity(network: ClientServiceNetwork) -> Dict[str, Any]:
        """
        Calculate connectivity metrics.
        
        Args:
            network: ClientServiceNetwork instance
            
        Returns:
            Dictionary containing connectivity metrics
        """
        metrics = {
            'is_connected': nx.is_connected(network.graph),
            'number_of_components': nx.number_connected_components(network.graph),
            'average_clustering': nx.average_clustering(network.graph),
            'density': nx.density(network.graph),
        }
        
        if metrics['is_connected']:
            metrics['diameter'] = nx.diameter(network.graph)
            metrics['average_shortest_path'] = nx.average_shortest_path_length(network.graph)
        else:
            # For disconnected graphs, calculate for largest component
            largest_cc = max(nx.connected_components(network.graph), key=len)
            subgraph = network.graph.subgraph(largest_cc)
            metrics['diameter_largest_component'] = nx.diameter(subgraph)
            metrics['average_shortest_path_largest_component'] = nx.average_shortest_path_length(subgraph)
            
        return metrics
    
    @staticmethod
    def detect_communities(network: ClientServiceNetwork, method: str = 'louvain') -> Dict[str, int]:
        """
        Detect communities in the network.
        
        Args:
            network: ClientServiceNetwork instance
            method: Community detection method ('louvain', 'greedy', 'label_propagation')
            
        Returns:
            Dictionary mapping nodes to community IDs
        """
        if method == 'louvain':
            try:
                import community as community_louvain
                communities = community_louvain.best_partition(network.graph)
            except ImportError:
                # Fallback to greedy modularity if python-louvain not available
                method = 'greedy'
        
        if method == 'greedy':
            communities_generator = nx.community.greedy_modularity_communities(network.graph)
            communities = {}
            for idx, comm in enumerate(communities_generator):
                for node in comm:
                    communities[node] = idx
                    
        elif method == 'label_propagation':
            communities_generator = nx.community.label_propagation_communities(network.graph)
            communities = {}
            for idx, comm in enumerate(communities_generator):
                for node in comm:
                    communities[node] = idx
                    
        return communities


class NetworkComparison:
    """
    Compare networks from different time periods.
    """
    
    @staticmethod
    def compare_centrality(network_pre: ClientServiceNetwork, 
                          network_post: ClientServiceNetwork) -> pd.DataFrame:
        """
        Compare centrality metrics between two networks.
        
        Args:
            network_pre: Network before the event
            network_post: Network after the event
            
        Returns:
            DataFrame with centrality comparisons
        """
        centrality_pre = NetworkMetrics.calculate_centrality(network_pre)
        centrality_post = NetworkMetrics.calculate_centrality(network_post)
        
        # Get common nodes
        common_nodes = set(network_pre.graph.nodes()) & set(network_post.graph.nodes())
        
        results = []
        for node in common_nodes:
            row = {'node': node}
            for metric in ['degree', 'betweenness', 'closeness', 'eigenvector']:
                pre_value = centrality_pre[metric].get(node, 0)
                post_value = centrality_post[metric].get(node, 0)
                row[f'{metric}_pre'] = pre_value
                row[f'{metric}_post'] = post_value
                row[f'{metric}_change'] = post_value - pre_value
                if pre_value != 0:
                    row[f'{metric}_change_pct'] = ((post_value - pre_value) / pre_value) * 100
                else:
                    row[f'{metric}_change_pct'] = 0 if post_value == 0 else float('inf')
            results.append(row)
            
        return pd.DataFrame(results)
    
    @staticmethod
    def compare_connectivity(network_pre: ClientServiceNetwork,
                           network_post: ClientServiceNetwork) -> Dict[str, Any]:
        """
        Compare connectivity metrics between two networks.
        
        Args:
            network_pre: Network before the event
            network_post: Network after the event
            
        Returns:
            Dictionary with connectivity comparisons
        """
        connectivity_pre = NetworkMetrics.calculate_connectivity(network_pre)
        connectivity_post = NetworkMetrics.calculate_connectivity(network_post)
        
        comparison = {
            'pre': connectivity_pre,
            'post': connectivity_post,
            'changes': {}
        }
        
        # Calculate changes for numeric metrics
        for key in connectivity_pre:
            if isinstance(connectivity_pre[key], (int, float)):
                if isinstance(connectivity_post.get(key), (int, float)):
                    change = connectivity_post[key] - connectivity_pre[key]
                    comparison['changes'][key] = change
                    
        return comparison
    
    @staticmethod
    def compare_communities(network_pre: ClientServiceNetwork,
                          network_post: ClientServiceNetwork,
                          method: str = 'louvain') -> Dict[str, Any]:
        """
        Compare community structure between two networks.
        
        Args:
            network_pre: Network before the event
            network_post: Network after the event
            method: Community detection method
            
        Returns:
            Dictionary with community comparison results
        """
        communities_pre = NetworkMetrics.detect_communities(network_pre, method)
        communities_post = NetworkMetrics.detect_communities(network_post, method)
        
        # Count number of communities
        num_communities_pre = len(set(communities_pre.values()))
        num_communities_post = len(set(communities_post.values()))
        
        # Get common nodes
        common_nodes = set(communities_pre.keys()) & set(communities_post.keys())
        
        # Calculate how many nodes changed communities
        nodes_changed = 0
        for node in common_nodes:
            # This is a simplified check - communities IDs may not align
            if communities_pre[node] != communities_post[node]:
                nodes_changed += 1
        
        return {
            'num_communities_pre': num_communities_pre,
            'num_communities_post': num_communities_post,
            'community_change': num_communities_post - num_communities_pre,
            'common_nodes': len(common_nodes),
            'nodes_with_different_community': nodes_changed,
            'communities_pre': communities_pre,
            'communities_post': communities_post
        }
    
    @staticmethod
    def identify_structural_changes(network_pre: ClientServiceNetwork,
                                   network_post: ClientServiceNetwork) -> Dict[str, Any]:
        """
        Identify key structural transformations between networks.
        
        Args:
            network_pre: Network before the event
            network_post: Network after the event
            
        Returns:
            Dictionary with structural change analysis
        """
        # Node and edge changes
        nodes_pre = set(network_pre.graph.nodes())
        nodes_post = set(network_post.graph.nodes())
        edges_pre = set(network_pre.graph.edges())
        edges_post = set(network_post.graph.edges())
        
        new_nodes = nodes_post - nodes_pre
        removed_nodes = nodes_pre - nodes_post
        new_edges = edges_post - edges_pre
        removed_edges = edges_pre - edges_post
        
        # Get top nodes by centrality change
        centrality_comparison = NetworkComparison.compare_centrality(network_pre, network_post)
        
        structural_changes = {
            'nodes_added': len(new_nodes),
            'nodes_removed': len(removed_nodes),
            'edges_added': len(new_edges),
            'edges_removed': len(removed_edges),
            'new_nodes_list': list(new_nodes)[:10],  # Limit to top 10
            'removed_nodes_list': list(removed_nodes)[:10],
            'density_change': nx.density(network_post.graph) - nx.density(network_pre.graph),
        }
        
        # Top nodes with increased centrality
        if not centrality_comparison.empty:
            top_increasing = centrality_comparison.nlargest(5, 'degree_change')
            top_decreasing = centrality_comparison.nsmallest(5, 'degree_change')
            
            structural_changes['top_nodes_increasing_centrality'] = top_increasing[['node', 'degree_change']].to_dict('records')
            structural_changes['top_nodes_decreasing_centrality'] = top_decreasing[['node', 'degree_change']].to_dict('records')
        
        return structural_changes


class NetworkVisualization:
    """
    Visualization tools for network analysis.
    """
    
    @staticmethod
    def plot_network(network: ClientServiceNetwork, 
                     title: str = "Client-Service Network",
                     node_colors: Dict[str, str] = None,
                     figsize: Tuple[int, int] = (12, 8)):
        """
        Plot the network using matplotlib.
        
        Args:
            network: ClientServiceNetwork instance
            title: Plot title
            node_colors: Dictionary mapping nodes to colors
            figsize: Figure size tuple
        """
        plt.figure(figsize=figsize)
        
        # Layout
        pos = nx.spring_layout(network.graph, k=0.5, iterations=50)
        
        # Node colors
        if node_colors is None:
            node_colors_list = ['lightblue' for _ in network.graph.nodes()]
        else:
            node_colors_list = [node_colors.get(node, 'lightblue') for node in network.graph.nodes()]
        
        # Draw
        nx.draw_networkx_nodes(network.graph, pos, node_color=node_colors_list, 
                              node_size=300, alpha=0.8)
        nx.draw_networkx_edges(network.graph, pos, alpha=0.5)
        nx.draw_networkx_labels(network.graph, pos, font_size=8)
        
        if network.weighted:
            edge_labels = nx.get_edge_attributes(network.graph, 'weight')
            nx.draw_networkx_edge_labels(network.graph, pos, edge_labels, font_size=6)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        return plt
    
    @staticmethod
    def plot_centrality_comparison(centrality_df: pd.DataFrame,
                                   metric: str = 'degree',
                                   top_n: int = 10):
        """
        Plot centrality comparison between pre and post networks.
        
        Args:
            centrality_df: DataFrame from compare_centrality
            metric: Centrality metric to plot
            top_n: Number of top nodes to display
        """
        # Get top nodes by absolute change
        top_changes = centrality_df.nlargest(top_n, f'{metric}_change', keep='all')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pre vs Post values
        x = range(len(top_changes))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], top_changes[f'{metric}_pre'], 
                width, label='Pre-event', alpha=0.8)
        ax1.bar([i + width/2 for i in x], top_changes[f'{metric}_post'], 
                width, label='Post-event', alpha=0.8)
        ax1.set_xlabel('Nodes')
        ax1.set_ylabel(f'{metric.capitalize()} Centrality')
        ax1.set_title(f'Top {top_n} Nodes by {metric.capitalize()} Centrality Change')
        ax1.set_xticks(x)
        ax1.set_xticklabels(top_changes['node'], rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Change values
        colors = ['green' if x > 0 else 'red' for x in top_changes[f'{metric}_change']]
        ax2.bar(x, top_changes[f'{metric}_change'], color=colors, alpha=0.8)
        ax2.set_xlabel('Nodes')
        ax2.set_ylabel(f'{metric.capitalize()} Centrality Change')
        ax2.set_title(f'Absolute Change in {metric.capitalize()} Centrality')
        ax2.set_xticks(x)
        ax2.set_xticklabels(top_changes['node'], rotation=45, ha='right')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return plt
    
    @staticmethod
    def plot_community_structure(network: ClientServiceNetwork,
                                communities: Dict[str, int],
                                title: str = "Network Communities"):
        """
        Plot network with community colors.
        
        Args:
            network: ClientServiceNetwork instance
            communities: Dictionary mapping nodes to community IDs
            title: Plot title
        """
        plt.figure(figsize=(12, 8))
        
        # Layout
        pos = nx.spring_layout(network.graph, k=0.5, iterations=50)
        
        # Color by community
        unique_communities = set(communities.values())
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_communities)))
        community_colors = {comm: colors[i] for i, comm in enumerate(unique_communities)}
        
        node_colors = [community_colors[communities[node]] for node in network.graph.nodes()]
        
        # Draw
        nx.draw_networkx_nodes(network.graph, pos, node_color=node_colors,
                              node_size=300, alpha=0.8)
        nx.draw_networkx_edges(network.graph, pos, alpha=0.3)
        nx.draw_networkx_labels(network.graph, pos, font_size=8)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        return plt


def comprehensive_period_comparison(network_pre: ClientServiceNetwork,
                                    network_post: ClientServiceNetwork,
                                    output_prefix: str = "comparison") -> Dict[str, Any]:
    """
    Perform comprehensive comparison between pre and post event networks.
    
    Args:
        network_pre: Network before the event
        network_post: Network after the event
        output_prefix: Prefix for output files
        
    Returns:
        Dictionary containing all comparison results
    """
    print("Starting comprehensive network comparison...")
    
    # 1. Centrality comparison
    print("1. Analyzing centrality changes...")
    centrality_comparison = NetworkComparison.compare_centrality(network_pre, network_post)
    centrality_comparison.to_csv(f"{output_prefix}_centrality.csv", index=False)
    print(f"   - Centrality comparison saved to {output_prefix}_centrality.csv")
    
    # 2. Connectivity comparison
    print("2. Analyzing connectivity changes...")
    connectivity_comparison = NetworkComparison.compare_connectivity(network_pre, network_post)
    print(f"   - Pre-event connectivity: {connectivity_comparison['pre']}")
    print(f"   - Post-event connectivity: {connectivity_comparison['post']}")
    print(f"   - Changes: {connectivity_comparison['changes']}")
    
    # 3. Community comparison
    print("3. Analyzing community structure changes...")
    community_comparison = NetworkComparison.compare_communities(network_pre, network_post)
    print(f"   - Communities pre-event: {community_comparison['num_communities_pre']}")
    print(f"   - Communities post-event: {community_comparison['num_communities_post']}")
    print(f"   - Community change: {community_comparison['community_change']}")
    
    # 4. Structural transformations
    print("4. Identifying structural transformations...")
    structural_changes = NetworkComparison.identify_structural_changes(network_pre, network_post)
    print(f"   - Nodes added: {structural_changes['nodes_added']}")
    print(f"   - Nodes removed: {structural_changes['nodes_removed']}")
    print(f"   - Edges added: {structural_changes['edges_added']}")
    print(f"   - Edges removed: {structural_changes['edges_removed']}")
    
    # Compile all results
    results = {
        'centrality': centrality_comparison,
        'connectivity': connectivity_comparison,
        'communities': community_comparison,
        'structural_changes': structural_changes
    }
    
    print("\nComparison complete!")
    return results
