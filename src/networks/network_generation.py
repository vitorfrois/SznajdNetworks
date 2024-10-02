import networkx as nx
import numpy as np
import pandas as pd
import igraph as ig
from dataclasses import dataclass
from tqdm import tqdm
from itertools import combinations
import os
import random
from numba import njit

n_nodes = 1000
n_networks = 10
BASE_NETWORK_DIR = 'data/nets/'

def generate_random_graph(n: list, p: float) -> list[tuple[int, int]]:
    edge_list = []
    node_list = list(range(n))
    all_edges = list(combinations(node_list, 2))
    random.shuffle(all_edges)
    edge_list = all_edges[:int(p * len(all_edges))]
    return edge_list

def write_edge_list_file(edge_list: list, filename: str):
    with open(filename, 'w+') as file:
        file.write('\n'.join('%s %s' % x for x in edge_list))

@dataclass
class NetworkSpec:
    name: str
    function: callable
    kwargs: dict

network_list: list[NetworkSpec] = [
    NetworkSpec(
        'erdos_renyi',
        generate_random_graph,
        kwargs={'n': n_nodes, 'p': 0.1}
    )
]


def generate_networks(network_list: list[NetworkSpec], BASE_NETWORK_DIR: str, n_networks: int):
    for spec in tqdm(network_list):
        network_dir = f'{BASE_NETWORK_DIR}{spec.name}'
        if not os.path.exists(network_dir):
            os.makedirs(network_dir)
            for i in tqdm(range(n_networks), leave=False):
                n = int(random.choice([1e3, 1e4]))
                p = random.random()
                kwargs={
                    'n': n, 
                    'p': p
                }
                edge_list = spec.function(**kwargs)
                filename = f'{network_dir}/{spec.name}_{str(i)}_{p}.edgelist'
                write_edge_list_file(edge_list, filename)

if __name__ == '__main__':
    generate_networks(network_list, BASE_NETWORK_DIR, n_networks)