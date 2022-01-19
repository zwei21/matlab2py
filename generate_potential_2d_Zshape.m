%generate_potential_2d_Zshape.m

function [potential_numeric, potential_symbolic, x, y] = generate_potential_2d_Zshape(IN_n_states,flag_visualize)
% Version 2021.09.12

% README :
%{
The Zshape surface is a weighted sum of 2d Normal distributions and
exponential functions

'border_x' creates an increase of Potential at the borders of the Reaction
Coordinate
'well' creates the path, some are symmetric (well_1-2), and some are not
(well_3-5) using the covariance matrix to shape them

INPUT : 
[IN_n_states] : array with integers giving the number of states is each dimension
(IN_n_states = [100,50] then x = linspace(x_min,x_max,n_states(1)) and y = linspace(x_min,x_max,n_states(2))
[IN_n_states] : array with integers giving the number of states is each
%}

% %
% n_states = [100,100];
x_min = -2;
x_max = 2;
y_min = -1;
y_max = 3;

x = linspace(x_min,x_max,IN_n_states(1));
y = linspace(y_min,y_max,IN_n_states(2));

%%% HYPER-PARAMETERS
border_coeff = 1; % Coefficient of borders 
well_coeff = 10; % Coefficient of wells (larger value makes wells deeper and barrier between them bigger)

%%% PARAMETERS OF NORMAL DISTRIBUTIONS
% Section "Bivariate case" in [https://en.wikipedia.org/wiki/Multivariate_normal_distribution]
mu_1 = [-1.5,-0.5];
mu_2 = [1.5,2.5];
sigm_center_well = 0.4; % Sigma of some of the wells
covar_mat_well = diag(ones(1,length(IN_n_states)).*sigm_center_well);

mu_3 = [-0.5,0];
sig = [1 ,0.4].*0.7; % Flat one
ro = 0.7;
colvar_mat_3 = [ sig(1)^2 , ro*sig(1)*sig(2) ; ro*sig(1)*sig(2) , sig(2)^2 ];

mu_4 = [0,1];
sig = [1 ,1].*0.7; % Diagonal one
ro = -0.8;
colvar_mat_4 = [ sig(1)^2 , ro*sig(1)*sig(2) ; ro*sig(1)*sig(2) , sig(2)^2 ];

mu_5 = [0.5,2];
sig = [1 ,0.4].*0.7; % Flat one
ro = 0.7;
colvar_mat_5 = [ sig(1)^2 , ro*sig(1)*sig(2) ; ro*sig(1)*sig(2) , sig(2)^2 ];

%%% INSTANTIATION
potential_numeric = zeros(IN_n_states);


%%% RUN
for x_id = 1:IN_n_states(1)
    for y_id = 1:IN_n_states(2)
        
        %%% BORDERS (Potential increase to infinity outside of [x_min,x_max] and [y_min,y_max])
        border_1 = exp(x_min - x(x_id)); 
        border_2 = exp(x(x_id) - x_max); 
        border_3 = exp(y_min - y(y_id)); 
        border_4 = exp(y(y_id) - y_max); 

        %%% WELLS 
        well_1 = mvnpdf([x(x_id),y(y_id)],mu_1, covar_mat_well);
        well_2 = mvnpdf([x(x_id),y(y_id)],mu_2, covar_mat_well); 
        well_3 = mvnpdf([x(x_id),y(y_id)],mu_3, colvar_mat_3); % Numeric expression
        well_4 = mvnpdf([x(x_id),y(y_id)],mu_4, colvar_mat_4);
        well_5 = mvnpdf([x(x_id),y(y_id)],mu_5, colvar_mat_5);    
        
        border_contribution = (border_1 + border_2 + border_3 + border_4)*border_coeff;
        well_contribution = (well_1 + well_2+ well_3+ well_4 + well_5)*well_coeff;
        
        potential_numeric(x_id,y_id) = border_contribution - well_contribution;
    end
end



%% Symbolic version of the potential 
% Requires "Symbolic Math Toolbox"

%%% Symbolic variables for symbolic expression of the potential
x_symb = sym('x_symb','real')  
y_symb = sym('y_symb','real')


%%% BORDERS (Potential increase to infinity outside of [x_min,x_max] and [y_min,y_max])
b_1 = exp(x_min - x_symb);
b_2 = exp(x_symb - x_max);
b_3 = exp(y_min - y_symb);
b_4 = exp(y_symb - y_max);

%%% WELLS 
w_1 = ((2*pi)^(-1))*(det(covar_mat_well)^(-1/2))*exp((-1/2)*([x_symb,y_symb]-mu_1)*inv(covar_mat_well)*([x_symb,y_symb]-mu_1)');
w_2 = ((2*pi)^(-1))*(det(covar_mat_well)^(-1/2))*exp((-1/2)*([x_symb,y_symb]-mu_2)*inv(covar_mat_well)*([x_symb,y_symb]-mu_2)');
w_3 = ((2*pi)^(-1))*(det(colvar_mat_3)^(-1/2))*exp((-1/2)*([x_symb,y_symb]-mu_3)*inv(colvar_mat_3)*([x_symb,y_symb]-mu_3)');% Symbolic expression
w_4 = ((2*pi)^(-1))*(det(colvar_mat_4)^(-1/2))*exp((-1/2)*([x_symb,y_symb]-mu_4)*inv(colvar_mat_4)*([x_symb,y_symb]-mu_4)');% Symbolic expression
w_5 = ((2*pi)^(-1))*(det(colvar_mat_5)^(-1/2))*exp((-1/2)*([x_symb,y_symb]-mu_5)*inv(colvar_mat_5)*([x_symb,y_symb]-mu_5)');% Symbolic expression


border_constribution_symbolic = (b_1 + b_2 + b_3 + b_4)*border_coeff;
well_contribution_symbolic = (w_1 + w_2 + w_3 + w_4 + w_5)*well_coeff;

potential_symbolic = border_constribution_symbolic - well_contribution_symbolic;

% %%% Symbolic derivatives with respect to x and y
% dpotsym_dx = diff(potential_symbolic,x_symb);
% dpotsym_dy = diff(potential_symbolic,y_symb);


% WITH THIS, we should be able to run Langevin dynamics and evaluate the
% derivatives at any point in space using the symbolic functions above.


%%% COMPUTE THE EXPRESSION OVER OUR DISCRETE SET OF BINS FOR CHECKING PURPOSES 
x = linspace(x_min,x_max,100);
y = linspace(y_min,y_max,100);

Z = subs(potential_symbolic);

for x_id = 1:100
    x_symb = x(x_id); % Update value of x_symb
    for y_id = 1:100
        y_symb = y(y_id);
        Z(x_id,y_id) = subs(potential_symbolic); % Evaluate potential_symbolic using the values of x&y_symb
    end
end

%%% VISUALIZE
if flag_visualize
    figure; hold on
    subplot(1,2,1); hold on
        title(strcat("(numeric) Z-shaped surface"))
        surface(x,y,potential_numeric' - min(potential_numeric(:)))
        xlim([x_min,x_max])
        ylim([y_min,y_max])
    subplot(1,2,2); hold on
        title(strcat("(symbolic) Z-shaped surface"))
        surface(x,y,Z'- min(Z(:)))
        xlim([x_min,x_max])
        ylim([y_min,y_max])
end

end