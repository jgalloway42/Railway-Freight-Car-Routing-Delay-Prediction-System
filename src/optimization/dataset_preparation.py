"""
Railway Dataset Preparation Guide
==================================

This guide covers obtaining and preparing datasets for the railway optimization project.
"""
import sys
from pathlib import Path

# Add project root to path for imports
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.generic.preamble import (
    raw_data, processed_data, interim_data,
    figures_path
)


# =====================================================================
# OPTION 1: SYNTHETIC REALISTIC DATA (RECOMMENDED FOR LEARNING)
# =====================================================================



def generate_synthetic_railway_network():
    """
    Generate a realistic synthetic railway network for testing.
    This is the FASTEST way to get started and allows full control.
    """
    import networkx as nx
    import random
    import json
    
    # Network parameters
    num_yards = 20  # Major rail yards
    num_connections = 50  # Rail connections
    num_commodities = 4  # Freight types
    
    # Create directed graph
    G = nx.gnm_random_graph(n=num_yards, m=num_connections, directed=True, seed=42)
    
    # Assign realistic attributes
    yard_names = [f"Yard_{chr(65+i//26)}{chr(65+i%26)}" for i in range(num_yards)]
    commodity_types = ['Coal', 'Grain', 'Containers', 'Chemicals']
    
    # Node attributes (yards)
    for node_id, name in enumerate(yard_names):
        G.nodes[node_id]['name'] = name
        G.nodes[node_id]['lat'] = 35 + random.uniform(-10, 10)
        G.nodes[node_id]['lon'] = -100 + random.uniform(-20, 20)
        G.nodes[node_id]['capacity'] = random.randint(50, 200)
    
    # Edge attributes (rail connections)
    for (u, v) in G.edges():
        G[u][v]['capacity'] = random.randint(50, 150)
        G[u][v]['distance'] = random.randint(100, 500)  # miles
        G[u][v]['base_cost'] = random.randint(5, 25)
        # Commodity-specific multipliers
        G[u][v]['cost_multipliers'] = {
            'Coal': 1.0,
            'Grain': 1.2,
            'Containers': 1.5,
            'Chemicals': 2.0
        }
    
    # Generate freight demands
    demands = []
    for _ in range(30):  # 30 shipments
        origin = random.randint(0, num_yards-1)
        destination = random.randint(0, num_yards-1)
        if origin != destination:
            demands.append({
                'commodity': random.choice(commodity_types),
                'origin': origin,
                'destination': destination,
                'amount': random.randint(20, 100),
                'priority': random.choice(['high', 'medium', 'low']),
                'deadline': random.randint(12, 72)  # hours
            })
    
    # Save to files using preamble paths
    import pickle
    network_file = Path(raw_data) / 'network_graph.pkl'
    demands_file = Path(raw_data) / 'demands.json'

    with open(network_file, 'wb') as f:
        pickle.dump(G, f)

    with open(demands_file, 'w') as f:
        json.dump(demands, f, indent=2)

    print(f"✓ Generated network: {num_yards} yards, {G.number_of_edges()} connections")
    print(f"✓ Generated {len(demands)} freight demands")
    print(f"✓ Saved to {raw_data}/")
    
    return G, demands


# =====================================================================
# OPTION 2: OPENSTREETMAP RAILWAY DATA
# =====================================================================

def fetch_osm_railway_data(bbox=None):
    """
    Fetch real railway network from OpenStreetMap.
    
    Args:
        bbox: (south, west, north, east) bounding box for area of interest
              Example: (32, -120, 42, -100) for western US
    
    Requires: pip install osmnx --break-system-packages
    """
    try:
        import osmnx as ox
        import networkx as nx
    except ImportError:
        print("⚠️  Please install osmnx: pip install osmnx --break-system-packages")
        return None
    
    if bbox is None:
        # Default: Kansas/Missouri area (major BNSF territory)
        bbox = (38, -96, 40, -94)
    
    print(f"📡 Fetching railway data from OpenStreetMap...")
    print(f"   Bounding box: {bbox}")
    
    # Fetch railway network
    # OSM queries can be slow - use small area for testing
    G = ox.graph_from_bbox(
        north=bbox[2], south=bbox[0],
        east=bbox[3], west=bbox[1],
        network_type='all',
        custom_filter='["railway"~"rail"]'
    )
    
    print(f"✓ Fetched {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Convert to directed graph if needed
    if not G.is_directed():
        G = G.to_directed()
    
    # Add capacity estimates based on track class
    for (u, v, k) in G.edges(keys=True):
        # Estimate capacity based on real rail properties
        G[u][v][k]['capacity'] = 100  # Default
        G[u][v][k]['base_cost'] = 10
    
    # Save using preamble paths
    import pickle
    osm_file = Path(raw_data) / 'osm_railway_network.pkl'

    with open(osm_file, 'wb') as f:
        pickle.dump(G, f)

    print(f"✓ Saved to {osm_file}")
    
    return G


# =====================================================================
# OPTION 3: BUREAU OF TRANSPORTATION STATISTICS
# =====================================================================

def fetch_bts_freight_data():
    """
    Fetch freight flow data from Bureau of Transportation Statistics.
    
    Source: https://www.bts.gov/faf
    Freight Analysis Framework (FAF) provides commodity flows between regions.
    
    Manual steps:
    1. Visit https://www.bts.gov/faf
    2. Download FAF5 database (CSV format)
    3. Place in data/raw/bts_freight.csv
    
    This provides:
    - Origin-destination pairs (by region)
    - Commodity types
    - Tonnage estimates
    """
    import pandas as pd

    bts_file = Path(raw_data) / 'bts_freight.csv'

    try:
        df = pd.read_csv(bts_file)
        print(f"✓ Loaded BTS freight data: {len(df)} records")
        print(f"  Columns: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        print(f"⚠️  BTS data not found at {bts_file}")
        print("   Download from: https://www.bts.gov/faf")
        return None


# =====================================================================
# RECOMMENDED APPROACH FOR DAY 1
# =====================================================================

def prepare_day1_dataset():
    """
    Recommended: Start with synthetic data for quick iteration.
    This gives you full control and fast debugging.
    """
    import networkx as nx
    
    print("=" * 60)
    print("RAILWAY DATASET PREPARATION")
    print("=" * 60)
    
    print("\n🎯 Generating synthetic railway network...")
    G, demands = generate_synthetic_railway_network()
    
    # Display summary statistics
    print("\n📊 Network Statistics:")
    print(f"  Nodes (yards): {G.number_of_nodes()}")
    print(f"  Edges (tracks): {G.number_of_edges()}")
    print(f"  Avg degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.1f}")
    print(f"  Network density: {nx.density(G):.3f}")
    
    print("\n🚂 Demand Statistics:")
    commodity_counts = {}
    for d in demands:
        c = d['commodity']
        commodity_counts[c] = commodity_counts.get(c, 0) + 1
    
    for commodity, count in commodity_counts.items():
        print(f"  {commodity}: {count} shipments")
    
    total_volume = sum(d['amount'] for d in demands)
    print(f"\n  Total freight volume: {total_volume} units")
    
    print("\n✅ Dataset ready for Day 2 optimization model!")
    print("\n" + "=" * 60)
    
    return G, demands


# =====================================================================
# DATASET VISUALIZATION (OPTIONAL)
# =====================================================================

def visualize_network(G):
    """Create a simple visualization of the network."""
    import matplotlib.pyplot as plt
    import networkx as nx
    
    plt.figure(figsize=(12, 8))
    
    # Get positions from lat/lon if available
    pos = {}
    for node in G.nodes():
        if 'lat' in G.nodes[node] and 'lon' in G.nodes[node]:
            pos[node] = (G.nodes[node]['lon'], G.nodes[node]['lat'])
        else:
            pos = nx.spring_layout(G)  # Fallback
            break
    
    # Draw network
    nx.draw(G, pos, 
            node_size=300,
            node_color='lightblue',
            edge_color='gray',
            arrows=True,
            arrowsize=10,
            with_labels=True,
            font_size=8)
    
    plt.title("Railway Network Topology")
    plt.tight_layout()

    # Save to figures path from preamble
    viz_file = Path(figures_path) / 'network_visualization.png'
    plt.savefig(viz_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved visualization to {viz_file}")
    plt.close()


# =====================================================================
# MAIN EXECUTION
# =====================================================================

if __name__ == "__main__":
    # Ensure directories exist using preamble paths
    import os
    os.makedirs(raw_data, exist_ok=True)
    os.makedirs(processed_data, exist_ok=True)
    os.makedirs(figures_path, exist_ok=True)

    # Generate dataset
    G, demands = prepare_day1_dataset()

    # Optional: visualize
    try:
        import matplotlib
        visualize_network(G)
    except ImportError:
        print("\n⚠️  matplotlib not installed - skipping visualization")
        print("   Install with: pip install matplotlib --break-system-packages")
