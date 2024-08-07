# Optimized Sznajd Model
import random
from numba import njit
from numba.experimental import jitclass
import numpy as np
from numba import int32, float32, boolean

NEGATIVE = -1
POSITIVE = 1
OPINIONS = [NEGATIVE, POSITIVE]

spec = [
    ('opinion_change_frequency', int32),
    ('_steps', int32),
    ('running', boolean),
    ('graph', int32[:, :]),
    ('N', int32),
    ('opinion_array', int32[:])
]

random.seed(0)

@jitclass(spec)
class OptimizedSznajd:
    opinion_change_frequency: int
    _steps: int
    running: bool
    graph: np.array

    def __init__(self, seed = None):
        self.running = False
        self._steps = 0

    def reset_model(self) -> None:
        self.opinion_change_frequency = 0
        self._steps = 0

    def set_graph(self, adjacency_matrix: np.array):
        self.graph = adjacency_matrix
        self.N = len(adjacency_matrix)
        self.opinion_array = np.zeros(self.N, dtype=np.int32)
    
    def get_nodes(self):
        return self.opinion_array

    def reset_model(self) -> None:
        self.opinion_change_frequency = 0
        self._steps = 0

    def random_network_initialization(self, positive_rate: float = 0.5) -> None:
        " Nodes receive opinion randomically "
        nodes = self.get_nodes()
        for i in range(self.N):
            if np.random.random() < positive_rate:
                self.opinion_array[i] = POSITIVE
            else:
                self.opinion_array[i] = NEGATIVE

    def get_node_neighbors(self, node):
        return np.nonzero(self.graph[node])[0]

    def step(self) -> None:
        self._steps += 1
        i = np.random.randint(0, self.N)
        j = np.random.randint(0, self.N)

        if (self.opinion_array[i] == self.opinion_array[j]) and i != j:
            self.convince_all_neighbors(i)
            self.convince_all_neighbors(j)

    def convince_all_neighbors(self, node) -> None:
        neighbors = self.get_node_neighbors(node)
        opinion = self.opinion_array[node]
        for i in range(len(neighbors)):
            if self.opinion_array[neighbors[i]] == opinion:
                continue
            self.opinion_change_frequency += 1
            self.opinion_array[neighbors[i]] = opinion

    def check_consensus(self):
        return len(np.unique(self.opinion_array)) == 1
    
    def run_model(self, max_steps: int = 1e3, verbose: bool = False) -> tuple[int, int]:
        while not self.check_consensus() and self._steps < max_steps:
            self.step()
        return self._steps, self.opinion_change_frequency