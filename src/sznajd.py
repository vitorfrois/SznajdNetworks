# Sznajd Model
from enum import Enum
import networkx as nx
from model import DiscreteNetworkModel
from tqdm import tqdm
from matplotlib.figure import Figure

NEGATIVE = -1
POSITIVE = 1

class Sznajd(DiscreteNetworkModel):
    def __init__(self, seed = 0):
        super().__init__(seed)

    def random_network_initialization(self, positive_rate: float = 0.5) -> None:
        for node, _ in self.get_nodes():
            if self.random.random() < positive_rate:
                self.set_node_data(node, POSITIVE)
            else:
                self.set_node_data(node, NEGATIVE)

    def step(self) -> None:
        self._steps += 1
        i, j = self.get_random_edge()

        if (self.get_node_data(i) == self.get_node_data(j)):
            self.convince_neighbors(i)
            self.convince_neighbors(j)
            
    def convince_neighbors(self, node) -> None:
        neighbors = self.get_node_neighbors(node)
        opinion = self.get_node_data(node)
        probability = 1/len(neighbors)
        for neighbor in neighbors:
            if self.random.random() < probability:
                self.set_node_data(neighbor, opinion)
    
    def run_model(self, verbose: bool = False) -> None:
        for i in tqdm(range(1000)):
            self.step()
        d = self.get_summarized_dict()
        print(d)

    def draw_network(self, space_ax):
        graph = self.graph
        pos = nx.spring_layout(graph, seed=0)
        nodes = self.get_nodes()
        colors = [node[1] for node in list(nodes)]
        nx.draw(
            graph,
            ax=space_ax,
            pos=pos,
            node_color=colors,
            cmap='Set1'
        )


