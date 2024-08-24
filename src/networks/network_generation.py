import networkx as nx
import numpy as np
import pandas as pd
import igraph as ig
from dataclasses import dataclass
from tqdm import tqdm
import os
import random

n_nodes = 1000
n_networks = 200
BASE_NETWORK_DIR = 'data/nets/'

@dataclass
class NetworkSpec:
    name: str
    function: callable
    kwargs: dict

network_list: list[NetworkSpec] = [
    NetworkSpec(
        'erdos_renyi',
        nx.erdos_renyi_graph,
        kwargs={'n': n_nodes, 'p': 0.01}
    )
]

def generate_networks(network_list: list[NetworkSpec], BASE_NETWORK_DIR: str, n_networks: int):
    for spec in tqdm(network_list):
        network_dir = f'{BASE_NETWORK_DIR}{spec.name}'
        if not os.path.exists(network_dir):
            os.makedirs(network_dir)
            for i in tqdm(range(n_networks), leave=False):
                kwargs={
                    'n': random.randint(1000, 1500), 
                    'p': random.random()
                }
                graph = spec.function(**kwargs)
                if not isinstance(graph, nx.Graph):
                    graph = graph.to_networkx()
                file = open(f'{network_dir}/{spec.name}_{str(i)}.edgelist', 'wb')
                nx.write_edgelist(graph, file, data=False)

if __name__ == '__main__':
    generate_networks(network_list, BASE_NETWORK_DIR, n_networks)