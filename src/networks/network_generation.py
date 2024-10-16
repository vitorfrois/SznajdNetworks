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
BASE_NETWORK_DIR = 'src/data/nets/'

@dataclass
class NetworkSpec:
    name: str
    function: callable
    kwargs: dict

network_list: list[NetworkSpec] = [
    NetworkSpec(
        'erdos_renyi',
        ig.Graph.Erdos_Renyi,
        kwargs=None
    )
]

def generate_networks(network_list: list[NetworkSpec], BASE_NETWORK_DIR: str, n_networks: int):
    for spec in tqdm(network_list):
        network_dir = f'{BASE_NETWORK_DIR}{spec.name}'
        if not os.path.exists(network_dir):
            os.makedirs(network_dir)
            for i in tqdm(range(n_networks), leave=False):
                p = random.random()
                kwargs={
                    'n': int(random.choice([1e2, 1e3, 1e4])), 
                    'p': p,
                    'directed': False
                }
                graph = spec.function(**kwargs)
                with open(f'{network_dir}/{spec.name}_{str(i)}_p{p:.4f}.edgelist', 'wb') as file:
                    graph.write(file, format="edgelist")

if __name__ == '__main__':
    generate_networks(network_list, BASE_NETWORK_DIR, n_networks)