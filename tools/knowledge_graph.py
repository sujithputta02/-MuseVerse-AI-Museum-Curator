"""Knowledge Graph Generator - Creates visual connections between concepts."""
import networkx as nx
from typing import Dict, List
import matplotlib.pyplot as plt
import io
import base64

class KnowledgeGraphGenerator:
    """Tool to generate knowledge graphs from exhibition data."""
    
    def generate_graph(self, exhibition: Dict) -> Dict:
        """Generate a knowledge graph from exhibition."""
        G = nx.Graph()
        
        # Add central topic node
        topic = exhibition.get("topic", "Exhibition")
        G.add_node(topic, node_type="topic", size=3000)
        
        # Add room nodes
        for room in exhibition.get("rooms", []):
            room_title = room.get("title", "Room")
            G.add_node(room_title, node_type="room", size=2000)
            G.add_edge(topic, room_title, weight=3)
            
            # Add exhibit nodes
            for exhibit in room.get("exhibits", [])[:3]:  # Limit for clarity
                exhibit_name = exhibit.get("name", "Exhibit")[:30]
                G.add_node(exhibit_name, node_type="exhibit", size=1000)
                G.add_edge(room_title, exhibit_name, weight=2)
        
        # Add concept nodes from semantic analysis
        if "semantic_analysis" in exhibition:
            concepts = exhibition["semantic_analysis"].get("key_concepts", [])[:5]
            for concept in concepts:
                G.add_node(concept, node_type="concept", size=800)
                G.add_edge(topic, concept, weight=1)
        
        return {
            "graph": G,
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": nx.density(G),
            "description": f"Knowledge graph with {G.number_of_nodes()} concepts and {G.number_of_edges()} connections"
        }
    
    def visualize_graph(self, graph_data: Dict) -> str:
        """Create a visualization of the knowledge graph."""
        G = graph_data["graph"]
        
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        # Color nodes by type
        color_map = {
            "topic": "#8B4513",
            "room": "#D4AF37",
            "exhibit": "#F5F5DC",
            "concept": "#A0522D"
        }
        
        node_colors = [color_map.get(G.nodes[node].get("node_type", "exhibit"), "#CCCCCC") for node in G.nodes()]
        node_sizes = [G.nodes[node].get("size", 1000) for node in G.nodes()]
        
        nx.draw(G, pos, 
                node_color=node_colors,
                node_size=node_sizes,
                with_labels=True,
                font_size=8,
                font_weight='bold',
                edge_color='#CCCCCC',
                linewidths=2,
                alpha=0.9)
        
        plt.title("Exhibition Knowledge Graph", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        # Convert to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return img_str
    
    def get_graph_metrics(self, graph_data: Dict) -> Dict:
        """Calculate graph metrics."""
        G = graph_data["graph"]
        
        return {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "density": round(nx.density(G), 3),
            "average_degree": round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2),
            "connected_components": nx.number_connected_components(G),
            "diameter": nx.diameter(G) if nx.is_connected(G) else "N/A"
        }
