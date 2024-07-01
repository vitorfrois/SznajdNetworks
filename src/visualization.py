import networkx as nx
import solara
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from model import DiscreteNetworkModel
from sznajd import Sznajd
import reacton.ipywidgets as widgets

import solara




@solara.component
def SpaceMatplotlib(model: DiscreteNetworkModel, counter):
    print('steps: ', model._steps)
    space_fig = Figure()
    space_ax = space_fig.subplots()
    model.draw_network(space_ax)
    solara.FigureMatplotlib(space_fig, format="png")

@solara.component
def ModelController(model, current_step, reset_counter, play_interval: int = 150):
    playing = solara.use_reactive(False)
    thread = solara.use_reactive(None)
    previous_step = solara.use_reactive(0)

    def render():
        """Infinite loop regularly mutating counter state"""
        print('here', model.running)
        while model.running:
            sleep(0.2)
            do_step()

    result: solara.Result[bool] = solara.use_thread(render)
    if result.error:
        raise result.error

    def do_step():
        model.step()
        previous_step.value = current_step.value
        current_step.value = model._steps

    def do_play():
        print('model is running')
        model.running = True

    def do_pause():
        print('not running')
        model.running = False

    def do_reset():
        reset_counter.value += 1

    with solara.Row():
        solara.Button(label="Step", color="primary", on_click=do_step)
        # This style is necessary so that the play widget has almost the same
        # height as typical Solara buttons.
        solara.Style(
            """
            .widget-play {
                height: 35px;
            }
            .widget-play button {
                color: white;
                background-color: #1976D2;  // Solara blue color
            }
            """
        )
        # widgets.Play(
        #     value=0,
        #     interval=play_interval,
        #     repeat=True,
        #     show_repeat=False,
        #     on_value=on_value_play,
        #     playing=playing.value,
        #     on_playing=do_set_playing,
        # )
        solara.Button(label="Reset", color="primary", on_click=do_reset)
        # threaded_do_play is not used for now because it
        # doesn't work in Google colab. We use
        # ipywidgets.Play until it is fixed. The threading
        # version is definite a much better implementation,
        # if it works.
        solara.Button(label="▶", color="primary", on_click=do_play)
        solara.Button(label="⏸︎", color="primary", on_click=do_pause)




@solara.component
def Page():
    current_step = solara.use_reactive(0)
    reset_counter = solara.use_reactive(0)
    
    def make_model():
        model = Sznajd()
        model.set_graph(nx.erdos_renyi_graph(100, 0.5))
        model.random_network_initialization()
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