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

test_a = spy.symbols('a')
test_eq = test_a+test_a+test_a+test_a+test_a+test_a+test_a+test_a+test_a+test_a+test_a+test_a+test_a
def worker(name, a, itime):
    for i in range(itime):
        result = a.evalf(subs={'a':1});
    return {name:result}

if __name__ == '__main__':
    start_t = datetime.datetime.now()
    potential_spiral, _, _ = gp2Sp.generate_potential_2d_spirals_symbolic(IN_n_states=[100,100],IN_number_of_branches=1,flag_visualize=False, flag_puresymbolic=True)
    traj, _, _ = gt2La.generate_trajectory_Langevin_from_symbolic_2D(potential_symbolic=potential_spiral,position_initial=[0.01,0.01], friction=10,simul_lagtime=0.1,n_steps=100)
    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("单线程计算 共消耗: " + "{:.2f}".format(elapsed_sec) + " 秒")
    print(traj)
    plt.plot(traj[0], traj[1])
    plt.show()
    plt.save('sample.png')
    '''
    start_t = datetime.datetime.now()

    num_cores = 5
    print("本地计算机有: " + str(num_cores) + " 核心")
    pool = mp.Pool(num_cores)
    param_dict = {'task1': [test_eq, 100*1000*2],
                  'task2': [test_eq, 100*1000*2],
                  'task3': [test_eq, 100*1000*2],
                  'task4': [test_eq, 100*1000*2],
                  'task5': [test_eq, 100*1000*2],}

    results = [pool.apply_async(worker, args=(name, param[0], param[1])) for name, param, in param_dict.items()]
    results = [p.get() for p in results]

    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("多线程计算 共消耗: " + "{:.2f}".format(elapsed_sec) + " 秒")
    print(results)

    start_t = datetime.datetime.now()
    worker('task_ultra', test_eq, 100*2*5000)
    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("单线程计算 共消耗: " + "{:.2f}".format(elapsed_sec) + " 秒")
    print(results)
    '''
