"""Safe 3D visualization - optional enhancement that won't break the system."""
import pandas as pd

def create_timeline_3d(timeline_events):
    """Create optional 3D timeline visualization."""
    try:
        import plotly.graph_objects as go
        
        if not timeline_events or len(timeline_events) < 2:
            return None
        
        # Extract years and events
        years = []
        events = []
        descriptions = []
        
        for event in timeline_events:
            try:
                year = int(event.get('year', '0'))
                years.append(year)
                events.append(event.get('event', 'Event')[:30])
                descriptions.append(event.get('description', '')[:100])
            except:
                continue
        
        if len(years) < 2:
            return None
        
        # Create 3D scatter plot
        fig = go.Figure(data=[go.Scatter3d(
            x=years,
            y=[i for i in range(len(years))],
            z=[0] * len(years),
            mode='markers+lines+text',
            marker=dict(
                size=12,
                color=years,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Year")
            ),
            line=dict(color='#8B4513', width=3),
            text=events,
            textposition="top center",
            hovertext=descriptions,
            hoverinfo='text'
        )])
        
        fig.update_layout(
            title="Interactive 3D Timeline",
            scene=dict(
                xaxis_title="Year",
                yaxis_title="Sequence",
                zaxis_title="",
                camera=dict(eye=dict(x=1.5, y=1.5, z=0.5))
            ),
            height=500,
            showlegend=False
        )
        
        return fig
    except Exception as e:
        # Silently fail - 3D is optional
        return None

def create_concept_network_3d(concepts, connections):
    """Create optional 3D concept network."""
    try:
        import plotly.graph_objects as go
        import networkx as nx
        import numpy as np
        
        if not concepts or len(concepts) < 3:
            return None
        
        # Create network
        G = nx.Graph()
        for concept in concepts[:10]:
            G.add_node(concept)
        
        # Add some connections
        for i in range(len(concepts) - 1):
            if i < len(concepts) - 1:
                G.add_edge(concepts[i], concepts[i + 1])
        
        # Get 3D layout
        pos = nx.spring_layout(G, dim=3, seed=42)
        
        # Extract coordinates
        x_nodes = [pos[node][0] for node in G.nodes()]
        y_nodes = [pos[node][1] for node in G.nodes()]
        z_nodes = [pos[node][2] for node in G.nodes()]
        
        # Create edges
        edge_x = []
        edge_y = []
        edge_z = []
        
        for edge in G.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])
        
        # Create figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='#D4AF37', width=2),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter3d(
            x=x_nodes, y=y_nodes, z=z_nodes,
            mode='markers+text',
            marker=dict(
                size=15,
                color='#8B4513',
                line=dict(color='#D4AF37', width=2)
            ),
            text=list(G.nodes()),
            textposition="top center",
            hoverinfo='text',
            showlegend=False
        ))
        
        fig.update_layout(
            title="3D Concept Network",
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, showticklabels=False, title=''),
            ),
            height=600,
            showlegend=False
        )
        
        return fig
    except Exception as e:
        # Silently fail - 3D is optional
        return None

def create_room_flow_3d(rooms):
    """Create optional 3D room flow visualization."""
    try:
        import plotly.graph_objects as go
        
        if not rooms or len(rooms) < 2:
            return None
        
        # Create spiral layout for rooms
        import numpy as np
        
        num_rooms = len(rooms)
        t = np.linspace(0, 4*np.pi, num_rooms)
        x = t * np.cos(t)
        y = t * np.sin(t)
        z = np.linspace(0, 2, num_rooms)
        
        room_names = [r.get('title', f'Room {i+1}')[:30] for i, r in enumerate(rooms)]
        exhibit_counts = [len(r.get('exhibits', [])) for r in rooms]
        
        fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers+lines+text',
            marker=dict(
                size=[10 + count*2 for count in exhibit_counts],
                color=exhibit_counts,
                colorscale='Sunset',
                showscale=True,
                colorbar=dict(title="Exhibits")
            ),
            line=dict(color='#8B4513', width=4),
            text=room_names,
            textposition="top center",
            hovertext=[f"{name}<br>Exhibits: {count}" for name, count in zip(room_names, exhibit_counts)],
            hoverinfo='text'
        )])
        
        fig.update_layout(
            title="3D Exhibition Flow",
            scene=dict(
                xaxis_title="",
                yaxis_title="",
                zaxis_title="Progress",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            height=600,
            showlegend=False
        )
        
        return fig
    except Exception as e:
        # Silently fail - 3D is optional
        return None
