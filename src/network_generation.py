import networkx as nx
import numpy as np
import pandas as pd
import igraph as ig
from dataclasses import dataclass
from tqdm import tqdm
import os

n_nodes = 1000
n_networks = 10
BASE_NETWORK_DIR = 'data/nets/'

@dataclass
class NetworkSpec:
    name: str
    function: callable
    kwargs: dict

network_list: list[NetworkSpec] = [
    NetworkSpec(
        'barabasi_linear',
        ig.Graph.Barabasi,
        kwargs={
            'n': n_nodes, 'm': 5, 
            'outpref': True, 
            'directed': False, 
            'power': 1.0, 
            'zero_appeal': 1, 
            'implementation': "psumtree", 
            'start_from': None
        }
    ),
    NetworkSpec(
        'barabasi_nonlinear_05',
        ig.Graph.Barabasi,
        kwargs={
            'n': n_nodes, 'm': 5, 
            'outpref': True, 
            'directed': False, 
            'power': 0.5, 
            'zero_appeal': 1, 
            'implementation': "psumtree", 
            'start_from': None
        }
    ),
    NetworkSpec(
        'barabasi_nonlinear_15',
        ig.Graph.Barabasi,
        kwargs={
            'n': n_nodes, 'm': 5, 
            'outpref': True, 
            'directed': False, 
            'power': 1.5, 
            'zero_appeal': 1, 
            'implementation': "psumtree", 
            'start_from': None
        }
    ),
    NetworkSpec(
        'waxman',
        nx.waxman_graph,
        kwargs={
            'n': n_nodes, 
            'beta': 0.12, 
            'alpha': 0.1, 
            'L': None, 
            'domain': (0, 0, 1, 1), 
            'metric': None, 
            'seed': None
        }
    ),
    NetworkSpec(
        'erdos_renyi',
        nx.erdos_renyi_graph,
        kwargs={'n': n_nodes, 'p': 0.01}
    ),
    NetworkSpec(
        'LFR',
        nx.LFR_benchmark_graph,
        kwargs={
            'n': n_nodes, 
            'tau1': 3, 
            'tau2': 1.5, 
            'mu': 0.1, 
            'average_degree': 10, 
            'min_degree': None, 
            'max_degree': None, 
            'min_community': 100, 
            'max_community': None, 
            'tol': 1e-07, 
            'max_iters': 500,
            'seed': 10
        }
    ),
    NetworkSpec(
        'watts-strogatz',
        nx.watts_strogatz_graph, 
        kwargs={
            'n': n_nodes,
            'k': 10,
            'p': 0.01
        }
    )
]


# n_redes=100
# degree=10
# os.makedirs("nets/Regular/", exist_ok=True)
# for i in range(n_redes):
#     G=nx.random_regular_graph(degree,1000)
#     fh1 = open("nets/Regular/Regular" + str(i) + '.edgelist', "wb")
#     nx.write_edgelist(G, fh1)

# # Complex network: Linear
# k_avg = 10
# for j in range(n_redes):
#     G = nx.path_graph(n)
#     # Calculate the total number of edges needed to achieve the desired average degree
#     m = int(k_avg * n / 2)
    
#     # Add or remove edges to adjust the degree sequence
#     if m > G.number_of_edges():
#         # Add edges to increase the average degree
#         num_edges_to_add = m - G.number_of_edges()
#         nodes = list(G.nodes())
#         for i in range(num_edges_to_add):
#             # Choose two nodes at random and add an edge between them
#             u, v = np.random.choice(nodes, size=2, replace=False)
#             G.add_edge(u, v)
  
#     else:
#         # Remove edges to decrease the average degree
#         num_edges_to_remove = G.number_of_edges() - m
#         edges = list(G.edges())
#         for i in range(num_edges_to_remove):
#             # Choose an edge at random and remove it
#             u, v = np.random.choice(edges)
#             G.remove_edge(u, v)

#     # Verify that the resulting graph has the desired average degree
#     k_avg_actual = sum(dict(G.degree()).values()) / n
#     print("Desired average degree: ", k_avg)
#     print("Actual average degree: ", k_avg_actual)
#     os.makedirs("nets/Linear/", exist_ok=True)
#     fh1 = open("nets/Linear/Linear" + str(j) + '.edgelist', "wb")

#     nx.write_edgelist(G, fh1)

def generate_networks(network_list: list[NetworkSpec], BASE_NETWORK_DIR: str, n_networks: int):
    for spec in network_list:
        network_dir = f'{BASE_NETWORK_DIR}{spec.name}'
        if not os.path.exists(network_dir):
            print(f'Generating {spec.name}')
            os.makedirs(network_dir)
            for i in tqdm(range(n_networks)):
                graph = spec.function(**spec.kwargs)
                if not isinstance(graph, nx.Graph):
                    graph = graph.to_networkx()
                file = open(f'{network_dir}/{spec.name}_{str(i)}.adj', 'wb')
                nx.write_edgelist(graph, file, data=False)

if __name__ == '__main__':
    generate_networks(network_list, BASE_NETWORK_DIR, n_networks)