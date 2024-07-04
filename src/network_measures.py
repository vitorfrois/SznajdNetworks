import networkx as nx
import numpy as np
import pandas as pd
import igraph as ig
from dataclasses import dataclass
from tqdm import tqdm
import os

n_networks = 10
BASE_NETWORK_DIR = 'data/nets/'
BASE_MEASURE_DIR = 'data/measures/'


class NetworkMeasure:
    igraph: ig.GraphBase
    nxgraph: nx.Graph
    measure_dict: dict[str, float]

    def __init__(self, network_file: str):
        self.igraph = ig.Graph.Read_Edgelist(network_file, directed=False)
        self.nxgraph = nx.Graph(self.igraph.get_edgelist())

    def get_measure_dict(self) -> dict[str, float]:
        measure_dict = {
            'clustering': self.clustering({'mode': 'zero'}),
            'closeness': self.closeness({}),
            'betweenness': self.betweenness({}),
            'average_shortest_path_lenght': self.average_shortest_path_lenght({}),
            'eigenvector': self.eigenvector({}),
            'assortativity': self.assortativity({'directed': False}),
            'information_centrality': self.information_centrality({}),
            'approximate_current_flow_betweenness_centrality': self.approximate_current_flow_betweenness_centrality({}),
        }
        return measure_dict

    def clustering(self, kwargs: dict | None = None) -> float:
        return self.igraph.transitivity_undirected(**kwargs)

    def closeness(self, kwargs: dict | None = None) -> float:
        return np.mean(self.igraph.closeness(**kwargs))

    def betweenness(self, kwargs: dict | None = None) -> float:
        return np.mean(self.igraph.betweenness(**kwargs))

    def average_shortest_path_lenght(self, kwargs: dict | None = None) -> float:
        return np.mean(self.igraph.distances(**kwargs))
    
    def eigenvector(self, kwargs: dict | None = None) -> float:
        return np.mean(self.igraph.eigenvector_centrality(**kwargs))

    def assortativity(self, kwargs: dict | None = None) -> float:
        return self.igraph.assortativity_degree(**kwargs)

    def information_centrality(self, kwargs: dict | None = None) -> float:
        return np.mean(list(nx.information_centrality(self.nxgraph, **kwargs).values()))

    def approximate_current_flow_betweenness_centrality(self, kwargs: dict | None = None) -> float:
        return np.mean(list(nx.approximate_current_flow_betweenness_centrality(self.nxgraph, **kwargs).values()))


def compute_network_measures(BASE_NETWORK_DIR: str, BASE_MEASURE_DIR: str):
    print(os.listdir(BASE_NETWORK_DIR))
    if not os.path.exists(BASE_MEASURE_DIR):
        os.makedirs(BASE_MEASURE_DIR)
    for networks_folder in tqdm(os.listdir(BASE_NETWORK_DIR)):
        measure_dict_df = {}
        measures_filename = f'{BASE_MEASURE_DIR}{networks_folder}.csv'
        network_folder = f'{BASE_NETWORK_DIR}{networks_folder}'
        if os.path.exists(measures_filename):
            continue
        for network_file in tqdm(os.listdir(network_folder), leave=False):
            network_measure = NetworkMeasure(f'{network_folder}/{network_file}')
            measure_dict = network_measure.get_measure_dict()
            measure_dict_df[network_file] = measure_dict
        measure_dict_df = pd.DataFrame(measure_dict_df).T
        measure_dict_df.to_csv(measures_filename)


if __name__ == '__main__':
    compute_network_measures(BASE_NETWORK_DIR, BASE_MEASURE_DIR)