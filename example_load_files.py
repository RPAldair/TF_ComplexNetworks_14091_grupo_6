"""
Example: Loading networks from files and performing comparison.

This script demonstrates how to:
1. Load networks from edge list files
2. Load service metadata from CSV files
3. Perform comprehensive period comparison
"""

from network_analysis import (
    ClientServiceNetwork,
    comprehensive_period_comparison
)
import os


def main():
    print("=" * 70)
    print("EXAMPLE: LOADING NETWORKS FROM FILES")
    print("=" * 70)
    print()
    
    # Define file paths
    data_dir = "sample_data"
    pre_edgelist = os.path.join(data_dir, "network_pre.edgelist")
    post_edgelist = os.path.join(data_dir, "network_post.edgelist")
    pre_metadata = os.path.join(data_dir, "services_pre.csv")
    post_metadata = os.path.join(data_dir, "services_post.csv")
    
    # Load pre-event network
    print("Loading pre-event network...")
    network_pre = ClientServiceNetwork(weighted=True)
    network_pre.load_from_edgelist(pre_edgelist, weighted=True)
    network_pre.load_metadata(pre_metadata)
    print(f"  Loaded: {network_pre.number_of_nodes()} nodes, {network_pre.number_of_edges()} edges")
    
    # Load post-event network
    print("Loading post-event network...")
    network_post = ClientServiceNetwork(weighted=True)
    network_post.load_from_edgelist(post_edgelist, weighted=True)
    network_post.load_metadata(post_metadata)
    print(f"  Loaded: {network_post.number_of_nodes()} nodes, {network_post.number_of_edges()} edges")
    print()
    
    # Display some service metadata
    print("Sample service metadata (pre-event):")
    for service_id in ['S1', 'S2', 'S3']:
        metadata = network_pre.get_service_metadata(service_id)
        if metadata:
            print(f"  {service_id}: {metadata}")
    print()
    
    print("Sample service metadata (post-event):")
    for service_id in ['S1', 'S2', 'S6']:
        metadata = network_post.get_service_metadata(service_id)
        if metadata:
            print(f"  {service_id}: {metadata}")
    print()
    
    # Perform comprehensive comparison
    print("Performing comprehensive comparison...")
    results = comprehensive_period_comparison(
        network_pre, 
        network_post, 
        output_prefix="file_comparison"
    )
    
    print()
    print("=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)
    
    # Structural changes summary
    structural = results['structural_changes']
    print("\nStructural Changes:")
    print(f"  Growth: +{structural['nodes_added']} nodes, +{structural['edges_added']} edges")
    print(f"  Removed: -{structural['nodes_removed']} nodes, -{structural['edges_removed']} edges")
    print(f"  Density change: {structural['density_change']:.4f}")
    
    # Connectivity summary
    conn = results['connectivity']
    print("\nKey Connectivity Metrics:")
    print(f"  Pre-event density: {conn['pre']['density']:.4f}")
    print(f"  Post-event density: {conn['post']['density']:.4f}")
    if 'diameter' in conn['changes']:
        print(f"  Diameter change: {conn['changes']['diameter']:+d}")
    
    # Community summary
    comm = results['communities']
    print("\nCommunity Structure:")
    print(f"  Communities changed from {comm['num_communities_pre']} to {comm['num_communities_post']}")
    
    # Top centrality changes
    if 'top_nodes_increasing_centrality' in structural:
        print("\nTop 3 Nodes with Increased Importance:")
        for item in structural['top_nodes_increasing_centrality'][:3]:
            node_id = item['node']
            change = item['degree_change']
            metadata = network_post.get_service_metadata(node_id)
            if metadata:
                print(f"  {node_id} ({metadata.get('name', 'Unknown')}): +{change:.4f}")
            else:
                print(f"  {node_id}: +{change:.4f}")
    
    print()
    print("=" * 70)
    print("Results saved to file_comparison_centrality.csv")
    print("=" * 70)


if __name__ == "__main__":
    # Check if sample data directory exists
    if not os.path.exists("sample_data"):
        print("ERROR: sample_data directory not found!")
        print("Please run this script from the repository root directory.")
        exit(1)
    
    main()
