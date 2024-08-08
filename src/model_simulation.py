import networkx as nx
from sznajd import Sznajd
from optimized_sznajd import OptimizedSznajd
import os
from tqdm import tqdm
import numpy as np
import pandas as pd
from numba import njit

MONTE_CARLO_ITERATIONS = 100
BASE_NETWORK_DIR = 'data/nets/'
BASE_SIMULATION_DIR = 'data/simulations/'

def simulate_sznajd(BASE_NETWORK_DIR: str, BASE_SIMULATION_DIR: str):
    print(os.listdir(BASE_NETWORK_DIR))
    if not os.path.exists(BASE_SIMULATION_DIR):
        os.makedirs(BASE_SIMULATION_DIR)
    for networks_folder in tqdm(os.listdir(BASE_NETWORK_DIR), desc='Model Simulation'):
        simulations_dict_df = {}
        simulations_filename = f'{BASE_SIMULATION_DIR}{networks_folder}.csv'
        network_folder = f'{BASE_NETWORK_DIR}{networks_folder}'

        if os.path.exists(simulations_filename):
            continue

        for network_file in tqdm(os.listdir(network_folder), desc=f'Monte Carlo on {networks_folder} networks', leave=False):
            # simulation_dict = monte_carlo_simulation(f'{network_folder}/{network_file}')
            simulation_dict = model_simulation(nx.to_numpy_array(nx.read_edgelist(f'{network_folder}/{network_file}'), dtype=np.int32))
            simulations_dict_df[network_file] = simulation_dict
        simulations_dict_df = pd.DataFrame(simulations_dict_df).T
        simulations_dict_df.to_csv(simulations_filename)

def model_simulation(adjacency_matrix: np.array) -> dict[str, float]:
    result_dict = {}
    model = OptimizedSznajd()
    initialization_methods = ['random', 'direct', 'inverse']
    model.set_graph(adjacency_matrix)
    for i in range(len(initialization_methods)):
        initialization = initialization_methods[i]
        mean_consensus_time, mean_opinion_change_frequency = optimized_monte_carlo(model, initialization)
        result_dict[(initialization, 'consensus_time')] = mean_consensus_time
        result_dict[(initialization, 'opinion_change_frequency')] = mean_opinion_change_frequency
    return result_dict

@njit
def optimized_monte_carlo(model, initialization,iterations: int = MONTE_CARLO_ITERATIONS):
    consensus_time_list = np.zeros(iterations, dtype=np.int32)
    opinion_change_frequency_list = np.zeros(iterations, dtype=np.int32)
    for i in range(iterations):
        model.reset_model()
        model.network_initialization(0.8, initialization)
        consensus_time, opinion_change_frequency = model.run_model()
        consensus_time_list[i] = consensus_time
        opinion_change_frequency_list[i] = opinion_change_frequency
    return float(np.mean(consensus_time_list)), float(np.mean(opinion_change_frequency_list))
    

if __name__ == '__main__':
    simulate_sznajd(BASE_NETWORK_DIR, BASE_SIMULATION_DIR)