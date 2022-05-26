import sys
import os
sys.path.append('../')
from datetime import datetime
from src import generate_trajectory_Langevin_2D_from_symbolic as gen_traj
from src import generate_potential_2d_Zshape as gen_zshape
from src import generate_potential_2d_spiral as gen_spiral
import json
import multiprocessing as mp
import numpy as np
from tqdm import tqdm
from functools import partial

gen_traj_func = gen_traj.generate_trajectory_Langevin_from_symbolic_2D
gen_pot_z_func = gen_zshape.generate_potential_2d_Zshape_symbolic
gen_pot_s_func = gen_spiral.generate_potential_2d_spirals_symbolic


### Worker function ###
class workerFactory:
    def __init__(self, config):
        self.position = config["initial_Position"]
        self.friction = config["friction"]
        self.simul_lagtime = config["simul_lagtime"]
        self.n_steps = config["n_steps"]
    def work(self, name, func):
        #print("Thread " + str(name) + " Working.")
        name = str(name)
        np.random.seed()
        traj,_,_ = gen_traj_func(potential_symbolic=func,
                                 position_initial=self.position,
                                 friction=self.friction,
                                 simul_lagtime=self.simul_lagtime,
                                 n_steps=self.n_steps)
        #print("Thread " + str(name) + " Done.")
        return np.array(traj)

#worker = workerFactory(config_dict)

### Generate potential ###
def potential_factory(config):
    In_N_States = [config['metadata']['InNumStates'],config['metadata']['InNumStates']]
    if config['metadata']['zshape']:
        potential, _, _ = gen_pot_z_func(In_N_States,
                                         flag_visualize=False,
                                         flag_puresymbolic=True)
    elif config['metadata']['spiral']:
        potential, _, _ = gen_pot_s_func(In_N_States,
                                         config['metadata']['branch'],
                                         flag_visualize=False,
                                         flag_puresymbolic=True)
    return potential

#potential = potential_factory(config_dict)

### Generate Trajs ###
def traj_factory(config, save_flag=True):
    '''
    config: dict, config dict containing all the data used for generate traj
    '''
    # get parent path of current file where it called
    filepath = os.getcwd()
    # def worker
    worker = workerFactory(config)
    # def potential
    potential = potential_factory(config)
    # def number of threads to parallel
    num_threads = int(mp.cpu_count() / 2) # Half of the cores would be used to run the process
    print("Using: " + str(num_threads) + " Threads.")
    # def number of trajs to generate
    ntraj = config['metadata']['ntraj']
    # Pooling process
    pool = mp.Pool(num_threads)
    #results = [pool.apply_async(worker.work, args=(i, potential)) for i in range(ntraj)]
    results = list(tqdm(pool.imap(partial(worker.work, func=potential), range(ntraj)), total=ntraj))
    #print(type(results))
    #results = [p.get() for p in results]
    #print(type(results))
    pool.close()
    pool.join()

    results=np.array(results)
    print(results.shape)
    result_name = filepath + '/' + 'result.npy'
    if save_flag:
        np.save(result_name, results)
    return results

### UltraFunction to Use when called from module ###
class geneTraj2D:
    def __init__(self, type):
        self.type = type
        if type == 's':
            self.config = json.loads('{    "metadata": {        "zshape": false,        "spiral": true,        "auto": false,        "manual": true,        "InNumStates": 100,        "branch": 2,        "ntraj": 20    },    "initial_Position": [        0.01,        0.01    ],    "friction": 10.0,    "simul_lagtime": 0.1,    "n_steps": 10000}')
        elif type == 'z':
            self.config = json.loads('{    "metadata": {        "zshape": true,        "spiral": false,        "auto": false,        "manual": true,        "InNumStates": 100,        "branch": 2,        "ntraj": 100    },    "initial_Position": [        0.0,        1.0    ],    "friction": 5.0,    "simul_lagtime": 0.01,    "n_steps": 1000}')
    def get_config(self):
        return self.config
    def generate(self, save_f=True):
        return traj_factory(self.config, save_f)
    