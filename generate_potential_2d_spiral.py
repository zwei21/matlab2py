import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib import cm
from tqdm import tqdm
import sympy as spy

def generate_potential_2d_spirals_numeric(IN_n_states,IN_number_of_branches,flag_visualize):
    """
    The spiral surface is a modification of the Anormal distribution, which is
    a kind of generalization of the multivariate normal distribution

    INPUT : 
    [IN_n_states] : array with integers giving the number of states is each dimension
    (IN_n_states = [100,50] then x = linspace(x_min,x_max,n_states(1)) and y = linspace(x_min,x_max,n_states(2))
    [IN_n_states] : array with integers giving the number of states is each
    """
    x_min = -20
    x_max = 20
    y_min = -20
    y_max = 20

    x = np.linspace(x_min,x_max,IN_n_states[0])
    y = np.linspace(y_min,y_max,IN_n_states[1])

    # Hyper Parameters
    sigma = 0.35 # Spiral
    warping_coeff = 0.01
    decrease_coeff = 0.05 # decrease how Potential decrease when we get further from center
    sinus_to_distance_coeff = 0.1

    # Instantiation
    potential_numeric = np.zeros(IN_n_states)

    # Run
    n_petals = IN_number_of_branches
    for x_id in tqdm(range(IN_n_states[0])):
        for y_id in range(IN_n_states[1]):

            # Transform coordinates from (x,y) to (angle,Distance)
            angle = np.arctan2(x[x_id], y[y_id])
            distance_squared = x[x_id]**2 + y[y_id]**2;  # BIG MODIFICATION
            
            # Use the chosen shape function
            r = (np.sin((angle+warping_coeff*distance_squared)*n_petals)*sinus_to_distance_coeff*distance_squared+2)

            # Apply the formula
            potential_numeric[x_id,y_id] = -1*np.exp( -1/2*(1)/(sigma*r)**2)*(1+decrease_coeff*distance_squared)

    potential_numeric = potential_numeric - np.min(potential_numeric[:]) # Shift so that minimum=0
    #potential_numeric = potential_numeric/np.sum(potential_numeric[:]) # Normalize at the end because used non-normalized shape function r.

    if flag_visualize:
        x, y = np.meshgrid(x, y)
        z = potential_numeric
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        surf = ax.plot_surface(x,y,z,cmap=cm.coolwarm,\
                            linewidth=0, antialiased=False)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        fig.colorbar(surf, shrink=0.5, aspect=5)
        
    return x, y, potential_numeric


def generate_potential_2d_spirals_symbolic(IN_n_states,IN_number_of_branches,flag_visualize, flag_puresymbolic=False):
    # Sympy

    x_min = -20
    x_max = 20
    y_min = -20
    y_max = 20

    x = np.linspace(x_min,x_max,IN_n_states[0])
    y = np.linspace(y_min,y_max,IN_n_states[1])

    # Hyper Parameters
    sigma = 0.35 # Spiral
    warping_coeff = 0.01
    decrease_coeff = 0.05 # decrease how Potential decrease when we get further from center
    sinus_to_distance_coeff = 0.1

    # Instantiation
    potential_symbolic_value = np.zeros(IN_n_states)
    n_petals = IN_number_of_branches

    #--Symbolic Version of the potential--#
    # Requires Sympy

    # Symbolic variables for symbolic expression of the potential
    x_symb, y_symb = spy.symbols('x_symb, y_symb', real=True)

    # Transform coordinates from (x, y) to (angle, Distance)
    angle_symb = spy.atan2(x_symb, y_symb)
    distance_squared_symb = x_symb ** 2 + y_symb ** 2

    # Use the chosen shape function
    r_symb = (spy.sin((angle_symb + warping_coeff * distance_squared_symb) * n_petals) * sinus_to_distance_coeff * distance_squared_symb + 2)

    # Apply the formula
    # Const to multi
    mul = -1
    potential_symbolic = mul*spy.exp( -1/2*(1)/(sigma*r_symb)**2)*(1+decrease_coeff*distance_squared_symb)

    # Symbolic derivatives with respect to x and y
    dpotsym_dx = potential_symbolic.diff(x_symb)
    dpotsym_dy = potential_symbolic.diff(y_symb)
    if flag_puresymbolic:
        return potential_symbolic, dpotsym_dx, dpotsym_dy
    # Compute the expression over our discrete set of bins for checking purposes
    # x = np.linspace(x_min, x_max, IN_n_states[0])
    # y = np.linspace(y_min, y_max, IN_n_states[1])

    for x_id in tqdm(range(IN_n_states[0])):
        for y_id in range(IN_n_states[1]):
            potential_symbolic_value[x_id, y_id] = potential_symbolic.evalf(subs={x_symb:x[x_id], y_symb:y[y_id]})
            # worker <- paralleled 

    potential_symbolic_value = potential_symbolic_value - np.min(potential_symbolic_value[:]) # Shift so that minimum=0
    #potential_symbolic_value = potential_symbolic_value/np.sum(potential_symbolic_value[:]) # Normalize at the end because used non-normalized shape function r.
    
    if flag_visualize:
        x, y = np.meshgrid(x, y)
        z = potential_symbolic_value
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        surf = ax.plot_surface(x,y,z,cmap=cm.coolwarm,\
                            linewidth=0, antialiased=False)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        fig.colorbar(surf, shrink=0.5, aspect=5)

    return x, y, potential_symbolic_value, potential_symbolic
