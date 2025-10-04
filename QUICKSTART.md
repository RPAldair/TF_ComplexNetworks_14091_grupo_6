# Quick Start Guide

Get started with client-service network analysis in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/RPAldair/TF_ComplexNetworks_14091_grupo_6.git
cd TF_ComplexNetworks_14091_grupo_6

# Install dependencies
pip install -r requirements.txt
```

## Run Examples

### 1. Basic Example (Programmatic)

```bash
python example_usage.py
```

This will:
- Create two sample networks (pre and post event)
- Perform comprehensive comparison
- Generate visualizations
- Save detailed results to CSV

**Output files:**
- `example_output_centrality.csv`: Centrality metrics comparison
- `example_output_network_pre.png`: Pre-event network visualization
- `example_output_network_post.png`: Post-event network visualization
- `example_output_centrality_comparison.png`: Centrality changes chart
- `example_output_communities_pre.png`: Pre-event communities
- `example_output_communities_post.png`: Post-event communities

### 2. File Loading Example

```bash
python example_load_files.py
```

This demonstrates:
- Loading networks from edge list files
- Loading service metadata from CSV files
- Performing analysis on file-based data

### 3. Interactive Jupyter Notebook

```bash
jupyter notebook example_notebook.ipynb
```

This provides:
- Step-by-step interactive analysis
- Cell-by-cell execution
- Inline visualizations
- Detailed explanations

## Basic Usage

### Create a Simple Network

```python
from network_analysis import ClientServiceNetwork

# Create network
network = ClientServiceNetwork(weighted=True)

# Add services
network.add_service('S1', {'name': 'Web Server', 'capacity': 100})

# Add clients
network.add_client('C1')

# Add connection
network.add_connection('C1', 'S1', weight=5.0)

print(f"Network: {network.number_of_nodes()} nodes")
```

### Compare Two Periods

```python
from network_analysis import comprehensive_period_comparison

# Create pre-event network
network_pre = ClientServiceNetwork(weighted=True)
# ... add nodes and edges ...

# Create post-event network
network_post = ClientServiceNetwork(weighted=True)
# ... add nodes and edges ...

# Compare
results = comprehensive_period_comparison(network_pre, network_post)

# Access results
print("Centrality changes:", results['centrality'])
print("Connectivity changes:", results['connectivity'])
print("Community changes:", results['communities'])
print("Structural changes:", results['structural_changes'])
```

### Load from Files

```python
from network_analysis import ClientServiceNetwork

# Load network
network = ClientServiceNetwork(weighted=True)
network.load_from_edgelist('sample_data/network_pre.edgelist', weighted=True)
network.load_metadata('sample_data/services_pre.csv')

# Access metadata
metadata = network.get_service_metadata('S1')
print(metadata)
```

## What You Get

### Centrality Analysis
- **Degree Centrality**: Number of connections
- **Betweenness Centrality**: Importance as intermediary
- **Closeness Centrality**: Accessibility from other nodes
- **Eigenvector Centrality**: Importance based on connected nodes

### Connectivity Metrics
- **Density**: How interconnected the network is
- **Diameter**: Longest shortest path
- **Average Shortest Path**: Average distance between nodes
- **Clustering Coefficient**: Tendency to form clusters
- **Number of Components**: Connected subgraphs

### Community Detection
- **Louvain Method**: Modularity optimization
- **Label Propagation**: Fast community detection
- **Greedy Modularity**: Alternative method

### Comparison Results
- **Structural Changes**: Added/removed nodes and edges
- **Centrality Changes**: How node importance changed
- **Connectivity Changes**: How network efficiency changed
- **Community Changes**: How network structure evolved

## File Formats

### Edge List (.edgelist or .txt)
```
C1 S1 5.0
C2 S1 3.0
C3 S2 4.0
```

### Metadata (.csv)
```csv
service_id,name,capacity,type
S1,Web Server,100,web
S2,Database,80,database
```

## Next Steps

- Read the [README.md](README.md) for comprehensive documentation
- Check [TUTORIAL.md](TUTORIAL.md) for detailed examples
- Explore [sample_data/](sample_data/) for file format examples
- Modify example scripts for your own data

## Common Use Cases

### 1. Analyze Service Migration
Compare network before and after migrating services to cloud or new infrastructure.

### 2. Impact of Service Outage
Analyze how network structure changed after a service failure or degradation.

### 3. Growth Analysis
Track how the network evolved as new clients or services were added.

### 4. Optimization Impact
Measure the effect of load balancers, caches, or other optimizations.

### 5. Security Analysis
Identify critical services and potential single points of failure.

## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'networkx'`
- **Solution:** Run `pip install -r requirements.txt`

**Problem:** Eigenvector centrality warnings
- **Solution:** This is normal for some network structures. Values default to 0.

**Problem:** `python-louvain` not found
- **Solution:** Install with `pip install python-louvain` or use alternative methods

**Problem:** Graphs appear empty
- **Solution:** Ensure edge list has correct format (node1 node2 weight)

## Need Help?

- Check the [TUTORIAL.md](TUTORIAL.md) for detailed guidance
- Review example scripts for working code
- Consult [NetworkX documentation](https://networkx.org/) for graph theory concepts

## Quick Reference

```python
# Import
from network_analysis import (
    ClientServiceNetwork,
    NetworkMetrics,
    NetworkComparison,
    NetworkVisualization,
    comprehensive_period_comparison
)

# Create network
net = ClientServiceNetwork(weighted=True)
net.add_service('S1', {'name': 'Service 1'})
net.add_client('C1')
net.add_connection('C1', 'S1', 5.0)

# Calculate metrics
centrality = NetworkMetrics.calculate_centrality(net)
connectivity = NetworkMetrics.calculate_connectivity(net)
communities = NetworkMetrics.detect_communities(net)

# Compare networks
results = comprehensive_period_comparison(net_pre, net_post)

# Visualize
import matplotlib.pyplot as plt
NetworkVisualization.plot_network(net, "My Network")
plt.show()
```

Happy analyzing! 🎉
