import osmnx as ox

# Smaller and faster: choose a specific city
place = 'Kanpur, India'  # You can also try: 'Lucknow, India', 'Delhi, India', etc.
print(f"Downloading road network for: {place} (should take less than a minute)...")

# Download and save
G = ox.graph_from_place(place, network_type='drive')
ox.save_graphml(G, f"{place.lower().replace(', ', '_').replace(' ', '_')}_graph.graphml")

print("✅ GraphML file created successfully!")
