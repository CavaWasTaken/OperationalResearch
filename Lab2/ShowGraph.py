import networkx as nx
import matplotlib.pyplot as plt

def create_graph_and_plot(nodes, edges, clique):
    # Create a graph
    G = nx.Graph()

    # Add nodes and edges to the graph
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Assign colors to nodes - red if inside the independent set, otherwise blue
    node_colors = ['red' if node in clique else 'blue' for node in G.nodes()]

    plt.figure(figsize=(17, 15))
    # Draw the graph with the specified node colors
    nx.draw(G, with_labels=True, node_color=node_colors, edge_color='gray', node_size=200, font_size=10)

    plt.savefig('graph.png')

# Example input
with open('./Solutions/Solution_20Nodes_0.3Prob.txt', 'r') as file:
    lines = file.readlines()
    nodes = set()
    edges = []
    clique = []

    for line in lines:
        if line.startswith("Edge"):
            # ex. Edge between Node 1 and Node 3
            parts = line.split()
            node1 = int(parts[3])
            node2 = int(parts[6])
            edges.append((node1, node2))
            nodes.add(node1)
            nodes.add(node2)
        elif line.startswith("Node"):
            # ex. Node 1 is in the clique
            parts = line.split()
            node = int(parts[1])
            clique.append(node)

    print("Nodes:", nodes)
    print("\nEdges:", edges)
    print("\nClique:", clique)

# Call the function
create_graph_and_plot(nodes, edges, clique)