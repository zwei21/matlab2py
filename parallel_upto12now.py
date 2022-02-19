import sys
sys.path.append('../')
import multiprocessing as mp
import math
import datetime
import generate_potential_2d_spiral as gp2Sp
import generate_potential_2d_Zshape as gp2Zs
import generate_trajectory_Langevin_2D_from_symbolic as gt2La
import sympy as spy
import matplotlib.pyplot as plt

def worker(name, potential_spiral):
    traj, _, _ = gt2La.generate_trajectory_Langevin_from_symbolic_2D(potential_symbolic=potential_spiral,position_initial=[0.01,0.01], friction=10,simul_lagtime=0.1,n_steps=100)
    return {name:traj}
def test_main():
    potential_spiral, _, _ = gp2Sp.generate_potential_2d_spirals_symbolic(IN_n_states=[100,100],IN_number_of_branches=1,flag_visualize=False, flag_puresymbolic=True)
    start_t = datetime.datetime.now()
    result_s = []
    for i in range(2):
        
        traj, _, _ = gt2La.generate_trajectory_Langevin_from_symbolic_2D(potential_symbolic=potential_spiral,position_initial=[0.01,0.01], friction=10,simul_lagtime=0.1,n_steps=100)
        result_s.append(traj)
    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("单线程计算 共消耗: " + "{:.2f}".format(elapsed_sec) + " 秒")

    start_t = datetime.datetime.now()

    num_cores = 5
    print("本地计算机有: " + str(num_cores) + " 核心")
    pool = mp.Pool(num_cores)
    param_dict = {'task1': potential_spiral,
                  'task2': potential_spiral,}
                  #'task3': potential_spiral,
                  #'task4': potential_spiral,
                  #'task5': potential_spiral,}

    results = [pool.apply_async(worker, args=(name, param)) for name, param, in param_dict.items()]
    results = [p.get() for p in results]

    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("多线程计算 共消耗: " + "{:.2f}".format(elapsed_sec) + " 秒")
    return result_s, results
if __name__ == "__main__":
    test_main()