import numpy as np

def generate_potential_2d_Zshape(IN_n_states,flag_visualize):
    """
    The Zshape surface is a weighted sum of 2d Normal distributions and
    exponential functions
    
    INPUT : 
    [IN_n_states] : array with integers giving the number of states is each dimension
    (IN_n_states = [100,50] then x = linspace(x_min,x_max,n_states(1)) and y = linspace(x_min,x_max,n_states(2))
    [IN_n_states] : array with integers giving the number of states is each
    """
    x_min = -2
    x_max = 2
    y_min = -1
    y_max = 3

    x = np.linspace(x_min,x_max,IN_n_states[1]);
    y = np.linspace(y_min,y_max,IN_n_states[2]);

    #---Hyper-parameters---#
    border_coeff = 1; # Coefficient of borders 
    well_coeff = 10; # Coefficient of wells (larger value makes wells deeper and barrier between them bigger)


    #---PARAMETERS OF NORMAL DISTRIBUTIONS---#
    # Section "Bivariate case" in [https://en.wikipedia.org/wiki/Multivariate_normal_distribution]
    mu_1 = [-1.5,-0.5]
    mu_2 = [1.5,2.5]
    sigm_center_well = 0.4 # Sigma of some of the wells
    covar_mat_well = np.diag(np.dot(np.ones(1,len(IN_n_states)),sigm_center_well))


    return potential_numeric, potential_symbolic, x, y