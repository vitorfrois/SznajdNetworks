import networkx as nx
import solara
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from model import DiscreteNetworkModel
from sznajd import Sznajd
import reacton.ipywidgets as widgets
from time import sleep
import matplotlib.pyplot as plt
from visualization import ModelController, SpaceMatplotlib

import solara


plt.switch_backend("agg")


@solara.component
def Page():
    current_step = solara.use_reactive(0)
    reset_counter = solara.use_reactive(0)
    
    def make_model():
        model = Sznajd()
        model.set_graph(nx.erdos_renyi_graph(100, 0.2))
        model.reset_model()
        model.random_network_initialization(0.8)
        current_step.value = 0
        return model

    model = solara.use_memo(
        make_model,
        dependencies=[
            reset_counter.value
        ],
    )

    with solara.AppBar():
        solara.AppBarTitle('Sznajd Model')
    
    with solara.Sidebar():
        with solara.Card("Information", margin=1, elevation=2):
            solara.Markdown(md_text=f"Step - {current_step}")
        ModelController(model, current_step, reset_counter)

    SpaceMatplotlib(model, current_step.value)


Page()