import sys
import os
sys.path.append('../')
import scipy.io as scio
from datetime import datetime
from src import generate_trajectory_Langevin_2D_from_symbolic as gen_traj
from src import generate_potential_2d_Zshape as gen_zshape
from src import generate_potential_2d_spiral as gen_spiral
import json
import argparse
import multiprocessing as mp
import numpy as np

gen_traj_func = gen_traj.generate_trajectory_Langevin_from_symbolic_2D
gen_pot_z_func = gen_zshape.generate_potential_2d_Zshape_symbolic
gen_pot_s_func = gen_spiral.generate_potential_2d_spirals_symbolic
### Utils ###
def append_name(filename):
    temp_name = filename
    i = 1
    while os.path.exists(temp_name):
        temp_name = filename + "-" + str(i)
        i+=1
    return temp_name

'''
Part1: argparse settings, receiving basic command to indicate
 type of potentials, 
 para config types(auto, manual), 
 in_n_states,  
 number of branches(opt, only used when doing spiral)

 Result:
 CLIInput(dict) ->> Part2
'''
parser = argparse.ArgumentParser()

parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s version : v 0.01', help='show the version')

group = parser.add_mutually_exclusive_group()
group.add_argument("-z", "--zshape", action="store_true", help='indicating zshape potential')
group.add_argument("-s", "--spiral", action="store_true", help='indicating spiral potential')

group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-a", "--auto", action="store_true", help='Read traj generating parameters from config files')
group2.add_argument("-m", "--manual", action="store_true", help='Set traj generating parameters manually')

parser.add_argument('InNumStates', nargs='?', type=int, default=100, help='Number of States')
parser.add_argument('branch', nargs='?', type=int, default=2, help='Number of Spiral Branch')
parser.add_argument('ntraj', nargs='?', type=int, default=20, help='Number of Trajs to generate, default as 20')

args = parser.parse_args()
CLIInput = vars(args)
##DEBUG##
#print(args.zshape)
#print(args.spiral)
#print(args.InNumStates)
'''
Part2: Keyboard listeners/ config file reader, receiving data to indicate config dict of 
        position_initial, 
        friction, 
        simul_lagtime, 
        n_steps
This part also yields generating a config folder including the config file saving all the data indicated to generate the traj
The name of config folder is accurate to days and sensative to type of potential(for now its only spiral and zshape)

Result:
config_dict ->> config.json -||(saved)
config_dict, filename, filepath ->> Part3
'''
if args.manual:

    position_initial_x, position_initial_y = input("Initial Position(x,y):").split()
    initial_position = [float(position_initial_x), float(position_initial_y)]
    friction=float(input("Friction:"))
    simul_lagtime=float(input("Simulation Lagtime:"))
    n_steps=int(input("Number of Steps:"))
    ##DEBUG##
    #print(initial_position, friction, simul_lagtime, n_steps)

    if args.spiral:
        name = 'spiral'
    elif args.zshape:
        name = 'zshape'

    filepath = name + '_traj_Mconfig_' + str(datetime.now().date())

    filepath = append_name(filepath) # Judge if filepath already exist and deal with repeat condition
    print(filepath)
    os.mkdir(filepath)

    filename = filepath + '/' + name + '_traj_Mconfig_' + str(datetime.now().date()) + '.json'

    config_dict = {
        'metadata':CLIInput,
        "initial_Position":initial_position,
        "friction":friction,
        "simul_lagtime":simul_lagtime,
        "n_steps":n_steps
        }
    ##DEBUG##
    #print(config_dict.values())
    #print(filename)

    json_str = json.dumps(config_dict, indent=4)

    with open(filename, 'w') as f:  
        f.write(json_str)  
elif args.auto:
    filename = input("Please input the config.json file path:")
    filepath = os.path.abspath(os.path.dirname(filename) + os.path.sep + ".")
    ##DEBUG##
    #print(type(filename))
    with open(filename, 'r') as load_f:
        config_dict = json.load(load_f)
    #print(config_dict)

'''Part3: Call Worker Function and generate result'''

### Worker function ###
class workerFactory:
    def __init__(self, config):
        self.position = config["initial_Position"]
        self.friction = config["friction"]
        self.simul_lagtime = config["simul_lagtime"]
        self.n_steps = config["n_steps"]
    def work(self, name, func):
        print("Thread " + str(name) + " Working.")
        name = str(name)
        np.random.seed()
        traj,_,_ = gen_traj_func(potential_symbolic=func,
                                 position_initial=self.position,
                                 friction=self.friction,
                                 simul_lagtime=self.simul_lagtime,
                                 n_steps=self.n_steps)
        
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
def traj_factory(config):
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
    results = [pool.apply_async(worker.work, args=(i, potential)) for i in range(ntraj)]
    #print(type(results))
    results = [p.get() for p in results]
    #print(type(results))
    pool.close()
    pool.join()

    results=np.array(results)
    print(results.shape)
    result_name = filepath + '/' + 'result.npy'
    np.save(result_name, results)

traj_factory(config_dict)