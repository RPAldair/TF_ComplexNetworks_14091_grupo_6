"""
Example usage of the Client-Service Network Analysis module.

This script demonstrates how to:
1. Create and populate client-service networks
2. Compare networks from different time periods
3. Analyze changes in centrality, connectivity, and communities
"""

from network_analysis import (
    ClientServiceNetwork,
    NetworkMetrics,
    NetworkComparison,
    NetworkVisualization,
    comprehensive_period_comparison
)
import matplotlib.pyplot as plt


def create_example_pre_event_network():
    """Create an example network representing the pre-event period."""
    network = ClientServiceNetwork(weighted=True)
    
    # Add services with metadata
    services = [
        ('S1', {'name': 'Web Server', 'capacity': 100, 'type': 'web'}),
        ('S2', {'name': 'Database', 'capacity': 80, 'type': 'database'}),
        ('S3', {'name': 'API Gateway', 'capacity': 90, 'type': 'api'}),
        ('S4', {'name': 'Cache Server', 'capacity': 70, 'type': 'cache'}),
        ('S5', {'name': 'Auth Service', 'capacity': 85, 'type': 'auth'}),
    ]
    
    for service_id, metadata in services:
        network.add_service(service_id, metadata)
    
    # Add clients
    clients = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    for client_id in clients:
        network.add_client(client_id)
    
    # Add connections (client-service relationships with weights)
    connections = [
        ('C1', 'S1', 5.0),
        ('C1', 'S2', 3.0),
        ('C2', 'S1', 4.0),
        ('C2', 'S3', 6.0),
        ('C3', 'S2', 7.0),
        ('C3', 'S4', 2.0),
        ('C4', 'S3', 5.0),
        ('C4', 'S5', 4.0),
        ('C5', 'S1', 3.0),
        ('C5', 'S4', 5.0),
        ('C6', 'S2', 4.0),
        ('C6', 'S5', 6.0),
        ('C7', 'S3', 3.0),
        ('C7', 'S4', 4.0),
        ('C8', 'S5', 5.0),
    ]
    
    for client, service, weight in connections:
        network.add_connection(client, service, weight)
    
    return network


def create_example_post_event_network():
    """Create an example network representing the post-event period."""
    network = ClientServiceNetwork(weighted=True)
    
    # Add services with updated metadata
    services = [
        ('S1', {'name': 'Web Server', 'capacity': 120, 'type': 'web'}),
        ('S2', {'name': 'Database', 'capacity': 100, 'type': 'database'}),
        ('S3', {'name': 'API Gateway', 'capacity': 110, 'type': 'api'}),
        ('S4', {'name': 'Cache Server', 'capacity': 80, 'type': 'cache'}),
        ('S5', {'name': 'Auth Service', 'capacity': 95, 'type': 'auth'}),
        ('S6', {'name': 'Load Balancer', 'capacity': 100, 'type': 'load_balancer'}),  # New service
    ]
    
    for service_id, metadata in services:
        network.add_service(service_id, metadata)
    
    # Add clients (some new clients, representing growth)
    clients = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
    for client_id in clients:
        network.add_client(client_id)
    
    # Add connections with updated patterns (representing changed usage)
    connections = [
        ('C1', 'S1', 6.0),
        ('C1', 'S2', 4.0),
        ('C1', 'S6', 5.0),  # New connection through load balancer
        ('C2', 'S1', 5.0),
        ('C2', 'S3', 7.0),
        ('C3', 'S2', 8.0),
        ('C3', 'S4', 3.0),
        ('C3', 'S6', 4.0),  # New connection
        ('C4', 'S3', 6.0),
        ('C4', 'S5', 5.0),
        ('C5', 'S1', 4.0),
        ('C5', 'S4', 6.0),
        ('C5', 'S6', 5.0),  # New connection
        ('C6', 'S2', 5.0),
        ('C6', 'S5', 7.0),
        ('C7', 'S3', 4.0),
        ('C7', 'S4', 5.0),
        ('C8', 'S5', 6.0),
        ('C8', 'S6', 5.0),  # New connection
        ('C9', 'S1', 4.0),  # New client
        ('C9', 'S6', 5.0),
        ('C10', 'S2', 5.0),  # New client
        ('C10', 'S3', 6.0),
    ]
    
    for client, service, weight in connections:
        network.add_connection(client, service, weight)
    
    return network


def main():
    """Run the example analysis."""
    print("=" * 70)
    print("CLIENT-SERVICE NETWORK ANALYSIS - PERIOD COMPARISON EXAMPLE")
    print("=" * 70)
    print()
    
    # Create pre and post event networks
    print("Creating example networks...")
    network_pre = create_example_pre_event_network()
    network_post = create_example_post_event_network()
    
    print(f"Pre-event network: {network_pre.number_of_nodes()} nodes, {network_pre.number_of_edges()} edges")
    print(f"Post-event network: {network_post.number_of_nodes()} nodes, {network_post.number_of_edges()} edges")
    print()
    
    # Run comprehensive comparison
    results = comprehensive_period_comparison(network_pre, network_post, "example_output")
    print()
    
    # Display detailed results
    print("=" * 70)
    print("DETAILED RESULTS")
    print("=" * 70)
    print()
    
    print("STRUCTURAL TRANSFORMATIONS:")
    print("-" * 70)
    structural = results['structural_changes']
    print(f"Network growth:")
    print(f"  - New nodes: {structural['nodes_added']}")
    print(f"  - Removed nodes: {structural['nodes_removed']}")
    print(f"  - New edges: {structural['edges_added']}")
    print(f"  - Removed edges: {structural['edges_removed']}")
    print(f"  - Density change: {structural['density_change']:.4f}")
    print()
    
    if 'top_nodes_increasing_centrality' in structural:
        print("Top nodes with increasing centrality:")
        for item in structural['top_nodes_increasing_centrality']:
            print(f"  - {item['node']}: +{item['degree_change']:.4f}")
        print()
    
    print("CONNECTIVITY METRICS:")
    print("-" * 70)
    conn = results['connectivity']
    print("Pre-event:")
    for key, value in conn['pre'].items():
        print(f"  - {key}: {value}")
    print()
    print("Post-event:")
    for key, value in conn['post'].items():
        print(f"  - {key}: {value}")
    print()
    print("Changes:")
    for key, value in conn['changes'].items():
        print(f"  - {key}: {value:+.4f}" if isinstance(value, float) else f"  - {key}: {value:+d}")
    print()
    
    print("COMMUNITY STRUCTURE:")
    print("-" * 70)
    comm = results['communities']
    print(f"Pre-event communities: {comm['num_communities_pre']}")
    print(f"Post-event communities: {comm['num_communities_post']}")
    print(f"Change in number of communities: {comm['community_change']:+d}")
    print(f"Nodes with different community assignment: {comm['nodes_with_different_community']}")
    print()
    
    # Generate visualizations
    print("Generating visualizations...")
    
    # 1. Network visualizations
    fig1 = NetworkVisualization.plot_network(network_pre, "Pre-Event Network")
    fig1.savefig("example_output_network_pre.png", dpi=150, bbox_inches='tight')
    print("  - Saved: example_output_network_pre.png")
    plt.close()
    
    fig2 = NetworkVisualization.plot_network(network_post, "Post-Event Network")
    fig2.savefig("example_output_network_post.png", dpi=150, bbox_inches='tight')
    print("  - Saved: example_output_network_post.png")
    plt.close()
    
    # 2. Centrality comparison
    centrality_df = results['centrality']
    if not centrality_df.empty:
        fig3 = NetworkVisualization.plot_centrality_comparison(centrality_df, 'degree', top_n=10)
        fig3.savefig("example_output_centrality_comparison.png", dpi=150, bbox_inches='tight')
        print("  - Saved: example_output_centrality_comparison.png")
        plt.close()
    
    # 3. Community visualizations
    communities_pre = NetworkMetrics.detect_communities(network_pre)
    communities_post = NetworkMetrics.detect_communities(network_post)
    
    fig4 = NetworkVisualization.plot_community_structure(network_pre, communities_pre, 
                                                         "Pre-Event Communities")
    fig4.savefig("example_output_communities_pre.png", dpi=150, bbox_inches='tight')
    print("  - Saved: example_output_communities_pre.png")
    plt.close()
    
    fig5 = NetworkVisualization.plot_community_structure(network_post, communities_post,
                                                         "Post-Event Communities")
    fig5.savefig("example_output_communities_post.png", dpi=150, bbox_inches='tight')
    print("  - Saved: example_output_communities_post.png")
    plt.close()
    
    print()
    print("=" * 70)
    print("Analysis complete! Check the output files for detailed results.")
    print("=" * 70)


if __name__ == "__main__":
    main()
