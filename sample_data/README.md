# Sample Data Directory

This directory contains sample network data files that demonstrate the format required for loading networks from files.

## Files

### Edge List Files

- **network_pre.edgelist**: Pre-event network edge list
- **network_post.edgelist**: Post-event network edge list

Format:
```
<client_id> <service_id> <weight>
```

Example:
```
C1 S1 5.0
C2 S1 3.0
C3 S2 4.0
```

### Metadata Files

- **services_pre.csv**: Service metadata for pre-event network
- **services_post.csv**: Service metadata for post-event network

Format:
```csv
service_id,name,capacity,type,location
S1,Web Server,100,web,DataCenter-A
S2,Database,80,database,DataCenter-A
```

## Usage

Load networks using these files with the `example_load_files.py` script:

```bash
python example_load_files.py
```

Or load them programmatically:

```python
from network_analysis import ClientServiceNetwork

# Load network from edge list
network = ClientServiceNetwork(weighted=True)
network.load_from_edgelist('sample_data/network_pre.edgelist', weighted=True)

# Load metadata
network.load_metadata('sample_data/services_pre.csv')
```

## Creating Your Own Data Files

### Edge List

Create a text file with one edge per line:
- For weighted graphs: `node1 node2 weight`
- For unweighted graphs: `node1 node2`

### Metadata CSV

Create a CSV file with:
- First row: Column headers (must include `service_id`)
- Subsequent rows: One service per row with its attributes

You can add any columns you want beyond the examples shown. The only required column is `service_id`.
