from flask import Flask, request, render_template, jsonify
import networkx as nx
import osmnx as ox
from geopy.geocoders import Nominatim
from networkx import all_simple_paths
from datetime import datetime
from chat import ask_gemini
    
app = Flask(__name__)

# Load the saved street network graph
GRAPH_FILE = "kanpur_india_graph.graphml"
G = ox.load_graphml(GRAPH_FILE)

# Initialize geocoder
geolocator = Nominatim(user_agent="shortest_path_app")

# Traffic-based speed estimation
def get_avg_speed_kmph(hour):
    if 7 <= hour < 10:      # Morning rush
        return 20
    elif 10 <= hour < 17:   # Midday
        return 30
    elif 17 <= hour < 20:   # Evening rush
        return 18
    else:                   # Night / Early morning
        return 40

@app.route('/')
def index():
    return render_template('index.html')

# AI Chatbot Endpoint (Gemini API)
@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"answer": "Please enter a question."})
    try:
        answer = ask_gemini(user_input)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

# Shortest Path Endpoint
@app.route('/shortest-path', methods=['POST'])
def shortest_path_api():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')

    try:
        # Geocode source and destination
        src_location = geolocator.geocode(source, timeout=10)
        dst_location = geolocator.geocode(destination, timeout=10)

        if not src_location or not dst_location:
            return jsonify({'error': 'Could not find one or both locations'}), 400

        # Find nearest graph nodes
        orig_node = ox.distance.nearest_nodes(G, src_location.longitude, src_location.latitude)
        dest_node = ox.distance.nearest_nodes(G, dst_location.longitude, dst_location.latitude)

        # Find shortest path
        shortest = nx.shortest_path(G, orig_node, dest_node, weight='length')
        route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in shortest]

        # Calculate total distance (in meters to kilometers)
        total_distance = nx.path_weight(G, shortest, weight='length')
        distance_km = total_distance / 1000

        # Estimate time of arrival (ETA)
        current_hour = datetime.now().hour
        avg_speed_kmph = get_avg_speed_kmph(current_hour)
        eta_minutes = (distance_km / avg_speed_kmph) * 60

        # Get 5 alternative simple paths
        k = 5
        all_paths = list(all_simple_paths(G, orig_node, dest_node, cutoff=20))[:k]
        red_edges = []
        for path in all_paths:
            coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]
            red_edges.append(coords)

        return jsonify({
            'route': route_coords,
            'edges': red_edges,
            'distance_km': distance_km,
            'eta_minutes': round(eta_minutes, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
