# Sznajd Model
from enum import Enum
import networkx as nx
from model import DiscreteNetworkModel
from tqdm import tqdm


class Opinion(Enum):
    NEGATIVE = -1
    POSITIVE = 1

class Sznajd(DiscreteNetworkModel):
    def __init__(self, seed = 0):
        super().__init__(seed)

    def random_network_initialization(self, positive_rate: float = 0.5) -> None:
        for node, _ in self.get_nodes():
            if self.random.random() < positive_rate:
                self.set_node_data(node, Opinion.POSITIVE)
            else:
                self.set_node_data(node, Opinion.NEGATIVE)

    def step(self) -> None:
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

