import numpy as np
import scipy.stats as stats
#----Utils----#


def generate_potential_2d_Zshape_numeric(IN_n_states,flag_visualize):
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

    x = np.linspace(x_min,x_max,IN_n_states[0]);
    y = np.linspace(y_min,y_max,IN_n_states[1]);

    #---Hyper-parameters---#
    border_coeff = 1; # Coefficient of borders 
    well_coeff = 10; # Coefficient of wells (larger value makes wells deeper and barrier between them bigger)


    #---PARAMETERS OF NORMAL DISTRIBUTIONS---#
    # Section "Bivariate case" in [https://en.wikipedia.org/wiki/Multivariate_normal_distribution]
    mu_1 = [-1.5,-0.5]
    mu_2 = [1.5,2.5]
    sigm_center_well = 0.4 # Sigma of some of the wells, sigm for sigma
    covar_mat_well = np.diag(np.dot(np.ones((1,len(IN_n_states)),sigm_center_well))

    mu_3 = [-0.5, 0]
    sig = [0.7, 0.28] # Origion: [1, 0.4] * 0.7 = result, flat one
    ro = 0.7
    colvar_mat_3 = [[sig(1)**2, ro*sig(1)*sig(2)],[ro*sig(1)*sig(2), sig(2)**2]]

    mu_4 = [0, 1]
    sig = [0.7, 0.7] # Origion: [1, 1] * 0.7, Diagonal one
    ro = -0.8
    colvar_mat_4 = [[sig(1)**2, ro*sig(1)*sig(2)],[ro*sig(1)*sig(2), sig(2)**2]]

    mu_5 = [0.5, 2]
    sig = [0.7, 0.28] # Origion: [1, 0.4] * 0.7 = result, flat one
    ro = 0.7
    colvar_mat_5 = [[sig(1)**2, ro*sig(1)*sig(2)],[ro*sig(1)*sig(2), sig(2)**2]]

    #---INSTANTIATION---#
    potential_numeric = np.zeros(IN_n_states)

    #---Run---#
    for x_id in range(IN_n_states[1]):
        for y_id in range(IN_n_states[2]):

            #--Borders (Potential increase to infinity outside of [x_min,x_max] and [y_min,y_max])--#
            border_1 = np.exp(x_min - x(x_id))
            border_2 = np.exp(x(x_id) - x_max)
            border_3 = np.exp(y_min - y(y_id))
            border_4 = np.exp(y(y_id) - y_max)

            #--WELLS--# # This requires multivariate normal distribution generating function
            well_1 = stats.multivariate_normal([x[x_id],y[y_id]],mu_1, covar_mat_well)
            well_2 = stats.multivariate_normal([x[x_id],y[y_id]],mu_2, covar_mat_well)
            well_3 = stats.multivariate_normal([x[x_id],y[y_id]],mu_3, colvar_mat_3) # Numeric expression
            well_4 = stats.multivariate_normal([x[x_id],y[y_id]],mu_4, colvar_mat_4)
            well_5 = stats.multivariate_normal([x[x_id],y[y_id]],mu_5, colvar_mat_5)  

            border_contribution = (border_1 + border_2 + border_3 + border_4) * border_coeff
            well_contribution = (well_1 + well_2+ well_3+ well_4 + well_5) * well_coeff

            potential_numeric[x_id,y_id] = border_contribution - well_contribution

    return potential_numeric, x, y

    # Sympy
    # TODO