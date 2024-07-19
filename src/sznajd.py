# Sznajd Model
from enum import Enum
import networkx as nx
from model import DiscreteNetworkModel
from tqdm import tqdm
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

NEGATIVE = -1
POSITIVE = 1
OPINIONS = [NEGATIVE, POSITIVE]

class Sznajd(DiscreteNetworkModel):
    opinion_change_frequency: int
    time_series: list[dict[int, int]]

    def __init__(self, seed = None):
        super().__init__(seed)

    def reset_model(self) -> None:
        self.opinion_change_frequency = 0
        self._steps = 0
        self.random = random.Random()
        self.time_series = []

    def get_ordered_opinion_list(self, positive_rate: float = 0.5) -> list[int]:
        opinion_list = []
        n_nodes = len(self.graph)
        for i in range(int((1 - positive_rate) * n_nodes)):
            opinion_list.append(NEGATIVE)
        for i in range(int(positive_rate * n_nodes)):
            opinion_list.append(POSITIVE)
        return opinion_list

    def random_network_initialization(self, positive_rate: float = 0.5) -> None:
        " Nodes receive opinion randomically "
        for node, _ in self.get_nodes():
            if self.random.random() < positive_rate:
                self.set_node_data(node, POSITIVE)
            else:
                self.set_node_data(node, NEGATIVE)

    def direct_initialization(self, positive_rate: float = 0.5):
        " High degree nodes receive positive opinions "
        for node, opinion in zip(self.get_nodes_sorted_by_degree(), self.get_ordered_opinion_list(positive_rate)):
            self.set_node_data(node[0], opinion)

    def inverse_initialization(self, positive_rate: float = 0.5):
        " Low degree nodes receive positive opinions "
        for node, opinion in zip(reversed(self.get_nodes_sorted_by_degree()), self.get_ordered_opinion_list(positive_rate)):
            self.set_node_data(node[0], opinion)

    def step(self) -> None:
        for i in range(3):
            self.time_series.append(self.get_summarized_dict())
            self._steps += 1
            i, j = self.get_random_edge()

            if (self.get_node_data(i) == self.get_node_data(j)):
                self.convince_all_neighbors(i)
                self.convince_all_neighbors(j)
            
    def convince_neighbors(self, node) -> None:
        neighbors = self.get_node_neighbors(node)
        opinion = self.get_node_data(node)
        probability = 1/len(neighbors)
        for neighbor in neighbors:
            if self.random.random() < probability:
                self.set_node_data(neighbor, opinion)
                self.opinion_change_frequency += 1

    def convince_all_neighbors(self, node) -> None:
        neighbors = self.get_node_neighbors(node)
        opinion = self.get_node_data(node)
        for neighbor in neighbors:
            if self.get_node_data(neighbor) == opinion:
                continue
            self.opinion_change_frequency += 1
            self.set_node_data(neighbor, opinion)

    def check_consensus(self):
        return len(self.get_summarized_dict()) == 1
    
    def run_model(self, max_steps: int = 1e3, verbose: bool = False) -> tuple[int, int]:
        while not self.check_consensus() and self._steps < max_steps:
            self.step()
        return self._steps, self.opinion_change_frequency

    def draw_network(self, space_ax):
        graph = self.graph
        pos = nx.spring_layout(graph, seed=0)
        colors = [node[1] for node in list(self.get_nodes())]

        nodes = nx.draw_networkx_nodes(
            graph,
            ax=space_ax,
            pos=pos,
            node_size=100,
            node_color=colors,
            cmap='bwr'
        )

        nx.draw_networkx_edges(
            graph,
            ax=space_ax,
            pos=pos,
            width=0.05,
        )
        plt.colorbar(nodes, ax=space_ax)




