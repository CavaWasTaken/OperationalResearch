import networkx as nx
import matplotlib.pyplot as plt

def create_graph_and_plot(nodes, edges, colors):
    # Create a graph
    G = nx.Graph()

    # Add nodes and edges to the graph
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Assign colors to nodes based on the colors dictionary
    node_colors = [colors.get(node, 'lightblue') for node in G.nodes()]

    plt.figure(figsize=(17, 15))
    # Draw the graph with the specified node colors
    nx.draw(G, with_labels=True, node_color=node_colors, edge_color='gray', node_size=200, font_size=10)

    plt.savefig('graph.png')

# Example input
with open('./Solutions/Solution_40Nodes_0.3Prob.txt', 'r') as file:
    lines = file.readlines()
    nodes = set()
    edges = []
    colors = {}

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
            # ex. Node 1 is colored with color 1
            parts = line.split()
            node = int(parts[1])
            color = int(parts[6])
            colors[node] = color

    print("Nodes:", nodes)
    print("\nEdges:", edges)
    unique_colors = list(set(colors.values()))
    print("\nColors used:", unique_colors)
    print("\nNumber of colors used:", len(unique_colors))


# Call the function
create_graph_and_plot(nodes, edges, colors)