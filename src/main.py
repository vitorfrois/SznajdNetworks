import networkx as nx
from sznajd import Sznajd

m = Sznajd()
m.set_graph(nx.erdos_renyi_graph(100, 0.5))
m.random_network_initialization()
m.run_model()