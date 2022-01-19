import numpy as np





def generate_potential_2d_spirals(IN_n_states,IN_number_of_branches,flag_visualize):
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

    x = np.linspace(x_min,x_max,IN_n_states(1))
    y = np.linspace(y_min,y_max,IN_n_states(2))

    # Hyper Parameters
    sigma = 0.35 # Spiral
    warping_coeff = 0.01
    decrease_coeff = 0.05 # decrease how Potential decrease when we get further from center
    sinus_to_distance_coeff = 0.1

    # Instantiation
    potential_numeric = np.zeros(IN_n_states)

    # Run
    n_petals = IN_number_of_branches
    for x_id in range(IN_n_states[1]):
        for y_id in range(IN_n_states[2]):

            # Transform coordinates from (x,y) to (angle,Distance)

    return potential_numeric, potential_symbolic, x, y