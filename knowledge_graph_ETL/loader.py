import networkx as nx
from datetime import datetime

G = nx.MultiDiGraph()

def load_triplets_to_graph(triplets):
    for t in triplets:
        sub = t['Subject']
        obj = t['Object']
        rel = t['Relationship']
        timestamp = t['Timestamp']
        
        G.add_node(sub, label=sub.split(':')[-1].strip())
        G.add_node(obj, label=obj.split(':')[-1].strip())

        G.add_edge(
            sub, 
            obj, 
            key=rel, # Use relationship type as the edge key
            relationship=rel, 
            timestamp=datetime.strptime(timestamp, '%Y-%m-%d')
        )
    return G
