import os
import pandas as pd
import json

data_folder = os.path.join(os.path.dirname(__file__), 'data')
results_folder = os.path.join(os.path.dirname(__file__), 'results')
folder_name = 'very_big_very_instance'

# read data
distances = pd.read_csv(os.path.join(data_folder, folder_name, 'distances.csv'), header=None)
service = pd.read_csv(os.path.join(data_folder, folder_name, 'service.csv'), header=None)
# read json
with open(os.path.join(data_folder, folder_name, 'weights.json'), 'r') as f:
    weights = json.load(f)

# read results
X = pd.read_csv(os.path.join(results_folder, folder_name, 'deposit_locations.csv'), header=None)
Y = pd.read_csv(os.path.join(results_folder, folder_name, 'path.csv'), header=None)

# warehouse cost
warehouse_cost = weights['construction'] * X.values.sum()

# penalty cost for unserved supermarkets
open_warehouses = X.values.flatten().astype(int) 
service_matrix = service.values
served = (service_matrix.T @ open_warehouses) > 0 
penalty_cost = weights['missed_supermarket'] * (~served).sum()

# travel cost
travel_cost = weights['travel'] * (Y.values * distances.values).sum()

# total cost
total_cost = warehouse_cost + penalty_cost + travel_cost

print(f"Warehouse Cost: {warehouse_cost}")
print(f"Penalty Cost: {penalty_cost}")
print(f"Travel Cost: {travel_cost}")
print(f"Total Cost: {total_cost}")

# create a graph to visualize the results
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

N = Y.shape[0]  # Number of nodes (warehouses + company)

# Add nodes (label 0 as "Company", others as "W1", "W2", ...)
labels = {0: "C"}
for i in range(1, N):
    labels[i] = f"W{i}"

G.add_nodes_from(labels.keys())

# Add edges where Y[i][j] == 1
for i in range(N):
    for j in range(N):
        if Y.iloc[i, j] == 1:
            G.add_edge(i, j)

# Draw the graph
pos = nx.circular_layout(G)

# Draw nodes with labels
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=150)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

# Draw directed edges with arrows
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.1')

plt.title("Vehicle Route: Company and Warehouses")
plt.axis('off')
plt.savefig(os.path.join(results_folder, folder_name, 'route_graph.png'))