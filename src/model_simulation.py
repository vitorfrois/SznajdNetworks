import networkx as nx
from sznajd import Sznajd
import os
from tqdm import tqdm
import numpy as np

MONTE_CARLO_ITERATIONS = 1
BASE_NETWORK_DIR = 'data/nets/'
BASE_SIMULATION_DIR = 'data/simulations/'

def simulate_sznajd(BASE_NETWORK_DIR: str, BASE_SIMULATION_DIR: str):
    print(os.listdir(BASE_NETWORK_DIR))
    if not os.path.exists(BASE_SIMULATION_DIR):
        os.makedirs(BASE_SIMULATION_DIR)
    for networks_folder in tqdm(os.listdir(BASE_NETWORK_DIR)):
        simulations_dict_df = {}
        simulations_filename = f'{BASE_SIMULATION_DIR}{networks_folder}.csv'
        network_folder = f'{BASE_NETWORK_DIR}{networks_folder}'

        if os.path.exists(simulations_filename):
            continue

        for network_file in os.listdir(network_folder):
            print(monte_carlo_simulation(f'{network_folder}/{network_file}'))
            # measure_dict = network_measure.get_measure_dict()
            # simulations_dict_df[network_file] = measure_dict
        # simulations_dict_df = pd.DataFrame(simulations_dict_df).T
        # simulations_dict_df.to_csv(simulations_filename)

def monte_carlo_simulation(network_path: str) -> dict[str, dict[str, float]]:
    result_dict = {}
    model = Sznajd()
    initialization_dict = {
        'random': model.random_network_initialization, 
        'direct': model.direct_initialization,
        'inverse': model.inverse_initialization
    }
    model.set_graph(nx.read_edgelist(network_path))
    for initialization in initialization_dict:
        initialization_dict[initialization]()
        consensus_time_list = []
        opinion_change_frequency_list = []
        for i in tqdm(range(MONTE_CARLO_ITERATIONS), leave=False):
            consensus_time, opinion_change_frequency = model.run_model()
            consensus_time_list.append(consensus_time)
            opinion_change_frequency_list.append(opinion_change_frequency)
        result_dict[initialization] = {
            'consensus_time': np.mean(consensus_time_list),
            'opinion_change_frequency': np.mean(opinion_change_frequency_list)
        }
    return result_dict



if __name__ == '__main__':
    simulate_sznajd(BASE_NETWORK_DIR, BASE_SIMULATION_DIR)