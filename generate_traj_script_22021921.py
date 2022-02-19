import sys
sys.path.append('../')
import scipy.io as scio
import multiprocessing as mp
import math
import datetime
import generate_potential_2d_spiral as gp2Sp
import generate_potential_2d_Zshape as gp2Zs
import generate_trajectory_Langevin_2D_from_symbolic as gt2La
import sympy as spy
import matplotlib.pyplot as plt
##############################
# Modify number of steps here##
def worker(name, potential_spiral):
    name = str(name)
    traj, _, _ = gt2La.generate_trajectory_Langevin_from_symbolic_2D(potential_symbolic=potential_spiral,position_initial=[0.01,0.01], friction=10,simul_lagtime=0.1,n_steps=1000)
    return {name:traj}

def test_main(cores, ntraj):
    potential_spiral, _, _ = gp2Sp.generate_potential_2d_spirals_symbolic(IN_n_states=[100,100],IN_number_of_branches=1,flag_visualize=False, flag_puresymbolic=True)

    start_t = datetime.datetime.now()

    num_cores = cores
    print("Local inclues: " + str(num_cores) + " Cores")

    pool = mp.Pool(num_cores)
    results = [pool.apply_async(worker, args=(i, potential_spiral)) for i in range(ntraj)]
    results = [p.get() for p in results]
    pool.close()
    pool.join()

    data_dict = {}
    for traj_data in results:
        data_dict.update(traj_data)

    filename = 'traj'+ datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S') + '.mat'
    scio.savemat(file_name=filename,mdict=data_dict)

    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("Multiprocessing consumed time: " + "{:.2f}".format(elapsed_sec) + " seconds")
    return results

if __name__ == "__main__":
    test_main(cores=10,ntraj=10)