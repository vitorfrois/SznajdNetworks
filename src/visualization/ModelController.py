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
def ModelController(model, current_step, reset_counter, play_interval: int = 150):
    thread = solara.use_reactive(None)
    previous_step = solara.use_reactive(0)
    playing = solara.use_reactive(False)


    def render():
        """Infinite loop regularly mutating counter state"""
        while playing.value:
            sleep(0.5)
            do_step()

    result: solara.Result[bool] = solara.use_thread(render, dependencies=[playing.value])
    if result.error:
        raise result.error

    def do_step():
        model.step()
        previous_step.value = current_step.value
        current_step.value = model._steps

    def do_play():
        print('model is running')
        playing.value = True
        model.running = True

    def do_pause():
        print('not running')
        playing.value = False
        model.running = False

    def do_reset():
        reset_counter.value += 1

    with solara.Row():
        solara.Button(label="Step", color="primary", on_click=do_step)
        solara.Button(label="Reset", color="primary", on_click=do_reset)
        if playing.value:
            solara.Button(label="⏸︎", color="primary", on_click=do_pause)
        else:
            solara.Button(label="▶", color="primary", on_click=do_play)
