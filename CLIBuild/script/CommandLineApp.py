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

args = parser.parse_args()
CLIInput = vars(args)
##DEBUG##
#print(args.zshape)
#print(args.spiral)
#print(args.InNumStates)
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

    if not os.path.exists(filepath):
        os.mkdir(filepath)

    with open(filename, 'w') as f:  
        f.write(json_str)  
elif args.auto:
    filename = input("Please input the config.json file path:")
    ##DEBUG##
    #print(type(filename))
    with open(filename, 'r') as load_f:
        config_dict = json.load(load_f)
    print(config_dict)