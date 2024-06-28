# Generic model for simulations
import networkx as nx

NODE_INFO = 'node_info'

class DiscreteNetworkModel:
    running: bool
    steps: int
    graph: nx.Graph

    def __init__(self) -> None:
        self.running = False
        self.steps = 0

    def set_graph(self, graph: nx.Graph) -> None:
        self.graph = graph

    def step(self) -> None:
        pass

    def run_model(self) -> None:
        while self.running:
            self.step()

    def set_node_data(self, node_number: int, data: int) -> None:
        self.graph.nodes[node_number][NODE_INFO] = data

    def get_node_data(self, node_number: int) -> int:
        return self.graph.nodes[node_number][NODE_INFO]

    def get_data_dict(self) -> dict[str, nx.Node]:
        d = dict()
        for node, data in self.graph.nodes():
            if data in d.keys():
                d[data].append(node)
            else:
                d[data] = [node]
