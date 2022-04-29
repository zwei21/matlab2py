#from generate_trajectory_Langevin_2D_from_symbolic import *
from generate_potential_2d_spiral import *
from generate_potential_2d_Zshape import *
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib import cm
from tqdm import tqdm
import sympy as spy
import time

def generate_trajectory_Langevin_from_symbolic_2D(potential_symbolic,position_initial, friction,simul_lagtime,n_steps):
    KbT = 0.5981

    # Temp vars is not required since symbolic math would include them directly
    # But it would be good to take a log as debugging propose 
    t1 = time.time()
    temp_vars = potential_symbolic.free_symbols
    print(temp_vars)
    temp_vars = list(temp_vars)
    if str(temp_vars[0]) == 'x_symb':
        x_symb, y_symb = list(temp_vars)
    else:
        y_symb, x_symb = list(temp_vars)
    print([x_symb, y_symb])
    n_dim = len(temp_vars)
    t2 = time.time()
    print('part1:', t2-t1)
    # Symbolic derivatives with respect to x and y
    # x_symb and y_symb is includeded in the potential symbolic equations that passed into this function
    t1 = time.time()
    dpotsym_dx = potential_symbolic.diff(x_symb)
    dpotsym_dy = potential_symbolic.diff(y_symb)    
    t2 = time.time()
    print('part2:', t2-t1)
    #Initialize the traj container
    t1 = time.time()
    traj_langevin = np.zeros((n_dim, n_steps))
    traj_langevin[:,0] = position_initial # Transfer indices from matlab to python: -1 each, start from 0
    t2 = time.time()
    print('part3:', t2 - t1)

    t1 = time.time()
    for step in tqdm(range(1,n_steps)):
        x_symb_val = traj_langevin[0, step-1] # Update values of x_symb for current position
        y_symb_val = traj_langevin[1, step-1]
        subs_dict = {x_symb:x_symb_val,y_symb:y_symb_val}
        drift = np.dot(-1,[dpotsym_dx.evalf(subs=subs_dict), dpotsym_dy.evalf(subs=subs_dict)])

        traj_langevin[:, step] = traj_langevin[:, step-1] + drift * simul_lagtime/friction + np.dot(np.random.randn(2,),np.sqrt(simul_lagtime*KbT/friction))
    t2 = time.time()
    print('part4:', t2-t1)
    return traj_langevin, dpotsym_dx, dpotsym_dx
