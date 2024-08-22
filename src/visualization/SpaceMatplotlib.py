import networkx as nx
import solara
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from sznajd.model import DiscreteNetworkModel
from sznajd.sznajd import Sznajd
import reacton.ipywidgets as widgets
from time import sleep
import matplotlib.pyplot as plt

import solara

@solara.component
def SpaceMatplotlib(model: DiscreteNetworkModel, counter):
    space_fig = Figure(figsize=(10,5))
    space_ax = space_fig.subplots()
    model.draw_network(space_ax)
    solara.FigureMatplotlib(space_fig, format="png")