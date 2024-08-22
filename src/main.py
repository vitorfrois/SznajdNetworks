import networkx as nx
from sznajd import Sznajd
from sznajd.optimized_sznajd import OptimizedSznajd
import numpy as np
from numba import njit
from tqdm import tqdm

iterations = 100

def monte_carlo(om):
    steps_array = np.zeros(iterations)
    frequency_array = np.zeros(iterations)
    for i in tqdm(range(iterations)):
        om.random_network_initialization()
        steps, frequency = om.run_model()
        steps_array[i] = steps
        frequency_array[i] = frequency
    print(np.mean(steps_array), np.mean(frequency_array))


graph = nx.erdos_renyi_graph(1000, 0.5)

print('Traditional')
m = Sznajd()
m.set_graph(graph)
m.random_network_initialization()
m.reset_model()
monte_carlo(m)

print('Optimized')
om = OptimizedSznajd()
om.set_graph(nx.to_numpy_array(graph, dtype=np.int32))
monte_carlo(om)
