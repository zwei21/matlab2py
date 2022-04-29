import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib import cm
from tqdm import tqdm
import sympy as spy
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
    covar_mat_well = np.diag(np.dot(np.ones((len(IN_n_states))),sigm_center_well))
    ###Debugging
    #print(covar_mat_well)

    mu_3 = [-0.5, 0]
    sig = [0.7, 0.28] # Origion: [1, 0.4] * 0.7 = result, flat one
    ro = 0.7
    colvar_mat_3 = [[sig[0]**2, ro*sig[0]*sig[1]],[ro*sig[0]*sig[1], sig[1]**2]]

    mu_4 = [0, 1]
    sig = [0.7, 0.7] # Origion: [1, 1] * 0.7, Diagonal one
    ro = -0.8
    colvar_mat_4 = [[sig[0]**2, ro*sig[0]*sig[1]],[ro*sig[0]*sig[1], sig[1]**2]]

    mu_5 = [0.5, 2]
    sig = [0.7, 0.28] # Origion: [1, 0.4] * 0.7 = result, flat one
    ro = 0.7
    colvar_mat_5 = [[sig[0]**2, ro*sig[0]*sig[1]],[ro*sig[0]*sig[1], sig[1]**2]]

    #---INSTANTIATION---#
    potential_numeric = np.zeros(IN_n_states)

    #---Run---#
    for x_id in tqdm(range(IN_n_states[0])):
        for y_id in range(IN_n_states[1]):

            #--Borders (Potential increase to infinity outside of [x_min,x_max] and [y_min,y_max])--#
            border_1 = np.exp(x_min - x[x_id])
            border_2 = np.exp(x[x_id] - x_max)
            border_3 = np.exp(y_min - y[y_id])
            border_4 = np.exp(y[y_id] - y_max)

            #--WELLS--# # This requires multivariate normal distribution generating function
            well_1 = stats.multivariate_normal.pdf(x=[x[x_id],y[y_id]],mean=mu_1, cov=covar_mat_well)
            well_2 = stats.multivariate_normal.pdf(x=[x[x_id],y[y_id]],mean=mu_2, cov=covar_mat_well)
            well_3 = stats.multivariate_normal.pdf(x=[x[x_id],y[y_id]],mean=mu_3, cov=colvar_mat_3) # Numeric expression
            well_4 = stats.multivariate_normal.pdf(x=[x[x_id],y[y_id]],mean=mu_4, cov=colvar_mat_4)
            well_5 = stats.multivariate_normal.pdf(x=[x[x_id],y[y_id]],mean=mu_5, cov=colvar_mat_5)  

            border_contribution = (border_1 + border_2 + border_3 + border_4) * border_coeff
            well_contribution = (well_1 + well_2+ well_3+ well_4 + well_5) * well_coeff

            potential_numeric[x_id,y_id] = border_contribution - well_contribution
            
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
        ax.view_init(90, 90)
        fig.colorbar(surf, shrink=0.5, aspect=5)
    return potential_numeric, x, y

    # Sympy
def generate_potential_2d_Zshape_symbolic(IN_n_states,flag_visualize, flag_puresymbolic):
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
    mu_1 = np.array([-1.5,-0.5]).reshape(2,1)
    mu_2 = np.array([1.5,2.5]).reshape(2,1)
    sigm_center_well = 0.4 # Sigma of some of the wells, sigm for sigma
    covar_mat_well = np.diag(np.dot(np.ones((len(IN_n_states))),sigm_center_well))
    ###Debugging
    #print(covar_mat_well)

    mu_3 = np.array([-0.5, 0]).reshape(2,1)
    sig = np.array([0.7, 0.28]).reshape(2,1) # Origion: [1, 0.4] * 0.7 = result, flat one
    ro = 0.7
    colvar_mat_3 = np.array([[sig[0]**2, ro*sig[0]*sig[1]],[ro*sig[0]*sig[1], sig[1]**2]]).reshape(2,2)

    mu_4 = np.array([0, 1]).reshape(2,1)
    sig = np.array([0.7, 0.7]).reshape(2,1) # Origion: [1, 1] * 0.7, Diagonal one
    ro = -0.8
    colvar_mat_4 = np.array([[sig[0]**2, ro*sig[0]*sig[1]],[ro*sig[0]*sig[1], sig[1]**2]]).reshape(2,2)

    mu_5 = np.array([0.5, 2]).reshape(2,1)
    sig = np.array([0.7, 0.28]).reshape(2,1) # Origion: [1, 0.4] * 0.7 = result, flat one
    ro = 0.7
    colvar_mat_5 = np.array([[sig[0]**2, ro*sig[0]*sig[1]],[ro*sig[0]*sig[1], sig[1]**2]]).reshape(2,2)

    # Symbolic Settings #
    x_symb, y_symb = spy.symbols('x_symb, y_symb', real=True)
    vec_symb = spy.Matrix([x_symb,y_symb])
    # BORDERS (Potential increase to infinity outside of [x_min,x_max] and [y_min,y_max])
    b_1 = spy.exp(x_min - x_symb)
    b_2 = spy.exp(x_symb - x_max)
    b_3 = spy.exp(y_min - y_symb)
    b_4 = spy.exp(y_symb - y_max)
    w_1 = ((2*np.pi)**(-1))*(np.linalg.det(covar_mat_well)**(-1/2))*spy.exp((-1/2)*(vec_symb-mu_1).T*np.linalg.inv(covar_mat_well)*(vec_symb-mu_1))

    # WELLS
    w_1 = ((2*np.pi)**(-1))*(np.linalg.det(covar_mat_well)**(-1/2))*spy.exp((-1/2)*(vec_symb-mu_1).T*np.linalg.inv(covar_mat_well)*(vec_symb-mu_1))
    w_2 = ((2*np.pi)**(-1))*(np.linalg.det(covar_mat_well)**(-1/2))*spy.exp((-1/2)*(vec_symb-mu_2).T*np.linalg.inv(covar_mat_well)*(vec_symb-mu_2))
    
    w_3 = ((2*np.pi)**(-1))*(np.linalg.det(colvar_mat_3)**(-1/2))*spy.exp((-1/2)*(vec_symb-mu_3).T*np.linalg.inv(colvar_mat_3)*(vec_symb-mu_3))
    
    w_4 = ((2*np.pi)**(-1))*(np.linalg.det(colvar_mat_4)**(-1/2))*spy.exp((-1/2)*(vec_symb-mu_4).T*np.linalg.inv(colvar_mat_4)*(vec_symb-mu_4))
    w_5 = ((2*np.pi)**(-1))*(np.linalg.det(colvar_mat_5)**(-1/2))*spy.exp((-1/2)*(vec_symb-mu_5).T*np.linalg.inv(colvar_mat_5)*(vec_symb-mu_5))
    
    # Border & Well Construction
    border_constribution_symbolic = (b_1 + b_2 + b_3 + b_4)*border_coeff
    well_contribution_symbolic = (w_1[0] + w_2[0] + w_3[0] + w_4[0] + w_5[0])*well_coeff
    
    # Build of Potential Symbolic
    potential_symbolic = border_constribution_symbolic - well_contribution_symbolic
    
    # Symbolic Derivatives with respect to x and y
    dpotsym_dx = potential_symbolic.diff(x_symb)
    dpotsym_dy = potential_symbolic.diff(y_symb)
    if flag_puresymbolic:
        return potential_symbolic, dpotsym_dx, dpotsym_dy
    """
    % WITH THIS, we should be able to run Langevin dynamics and evaluate the
    % derivatives at any point in space using the symbolic functions above.
    """
    
    # COMPUTE THE EXPRESSION OVER OUR DISCRETE SET OF BINS FOR CHECKING PURPOSES 
    ## Instantiation ##
    potential_symbolic_value = np.zeros(IN_n_states) # which is, Z in Valdimir's code
    ## Loop Calculation ##
    for x_id in range(IN_n_states[0]):
        for y_id in range(IN_n_states[1]):
            potential_symbolic_value[x_id, y_id] = potential_symbolic.evalf(subs={x_symb:x[x_id], y_symb:y[y_id]})
            # worker <- paralleled 

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
        ax.view_init(90, 90)
        fig.colorbar(surf, shrink=0.5, aspect=5)

    return x, y, potential_symbolic_value, potential_symbolic