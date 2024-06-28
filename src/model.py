# Generic model for simulations
import networkx as nx
import random

NODE_INFO = 'node_info'

class DiscreteNetworkModel:
    running: bool
    steps: int
    graph: nx.Graph

    def __init__(self, seed = None) -> None:
        self.running = False
        self.steps = 0
        if seed:
            self.random = random.Random(seed)
        else:
            self.random = random.Random()

    def set_graph(self, graph: nx.Graph) -> None:
        self.graph = graph

    def step(self) -> None:
        pass

    def run_model(self) -> None:
        while self.running:
            self.step()

    def get_nodes(self) -> list:
        return self.graph.nodes(data=NODE_INFO)

    def get_random_node(self) -> int | tuple:
        return self.random.choice(self.get_nodes())

    def set_node_data(self, node_number: int, data: int) -> None:
        self.graph.nodes[node_number][NODE_INFO] = data

    def get_node_data(self, node_number: int) -> int:
        return self.get_nodes()[node_number]

    def get_node_neighbors(self, node) -> list:
        return list(self.graph.neighbors(node))

    def get_edges(self) -> list:
        return list(self.graph.edges)

    def get_random_edge(self) -> tuple:
        return self.random.choice(self.get_edges())

    def get_data_dict(self) -> dict:
        d = dict()
        for node, data in self.get_nodes():
            if data in d.keys():
                d[data].append(node)
            else:
                d[data] = [node]
        return d

    def get_summarized_dict(self) -> dict:
        d = self.get_data_dict()
        for key in d:
            d[key] = len(d[key])
        return d

        
