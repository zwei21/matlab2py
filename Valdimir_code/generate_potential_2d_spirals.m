%generate_potential_2d_Zshape.m

function [potential_numeric, potential_symbolic, x, y] = generate_potential_2d_spirals(IN_n_states,IN_number_of_branches,flag_visualize)
% Version 2021.09.16

% README :
%{
The spiral surface is a modification of the Anormal distribution, which is
a kind of generalization of the multivariate normal distribution


INPUT : 
[IN_n_states] : array with integers giving the number of states is each dimension
(IN_n_states = [100,50] then x = linspace(x_min,x_max,n_states(1)) and y = linspace(x_min,x_max,n_states(2))
[IN_n_states] : array with integers giving the number of states is each
%}

% %
% n_states = [100,100];
x_min = -20;
x_max = 20;
y_min = -20;
y_max = 20;

x = linspace(x_min,x_max,IN_n_states(1));
y = linspace(y_min,y_max,IN_n_states(2));



%%% HYPER-PARAMETERS
sigma = 0.35; % SPIRAL 
warping_coeff = 0.01;
decrease_coeff = 0.05; % decrease how Potential decrease when we get further from center
sinus_to_distance_coeff = 0.1;

%%% INSTANTIATION
potential_numeric = zeros(IN_n_states);

%%% RUN
    n_petals = IN_number_of_branches;
for x_id = 1:IN_n_states(1)
    for y_id = 1:IN_n_states(2)

        %%% Transform coordinates from (x,y) to (angle,Distance)
        angle = atan2(x(x_id),y(y_id)); 
        distance_squared = x(x_id)^2 + y(y_id)^2;  % BIG MODIFICATION
          
        %%% Use the chosen shape function
            r = (sin((angle+warping_coeff*distance_squared)*n_petals)*sinus_to_distance_coeff*distance_squared+2); 
        
        %%% Apply the formula
%         pdf_Anormal(x_id,y_id) = exp(-1/2*(distance_squared)./(sigma*r)^2); % Anormal distribution
        potential_numeric(x_id,y_id) = -1*exp( -1/2*(1)./(sigma*r)^2)*(1+decrease_coeff*distance_squared);
        
    end
end

potential_numeric = potential_numeric - min(potential_numeric(:)); % Shift so that minimum=0
potential_numeric = potential_numeric./sum(potential_numeric(:)); % Normalize at the end because used non-normalized shape function r.

if flag_visualize
    figure; hold on
    title("nb petals = "+num2str(n_petals));
    surface(potential_numeric,'EdgeAlpha',0.1);
end



%% Symbolic version of the potential 
% Requires "Symbolic Math Toolbox"

%%% Symbolic variables for symbolic expression of the potential
x_symb = sym('x_symb','real');
y_symb = sym('y_symb','real');

%%% Transform coordinates from (x,y) to (angle,Distance)
angle_symb = atan2(x_symb,y_symb); 
distance_squared_symb = x_symb^2 + y_symb^2;  % BIG MODIFICATION

%%% Use the chosen shape function
r_symb = (sin((angle_symb+warping_coeff*distance_squared_symb)*n_petals)*sinus_to_distance_coeff*distance_squared_symb+2); 

%%% Apply the formula
%         pdf_Anormal(x_id,y_id) = exp(-1/2*(distance_squared)./(sigma*r)^2); % Anormal distribution
potential_symbolic = -1*exp( -1/2*(1)./(sigma*r_symb)^2)*(1+decrease_coeff*distance_squared_symb); 

% %%% Symbolic derivatives with respect to x and y
% dpotsym_dx = diff(potential_symbolic,x_symb);
% dpotsym_dy = diff(potential_symbolic,y_symb);


% WITH THIS, we should be able to run Langevin dynamics and evaluate the
% derivatives at any point in space using the symbolic functions above.


% %%% COMPUTE THE EXPRESSION OVER OUR DISCRETE SET OF BINS FOR CHECKING PURPOSES 
% x = linspace(x_min,x_max,100);
% y = linspace(y_min,y_max,100);
% 
% Z = subs(potential_symbolic);
% 
% for x_id = 1:100
%     x_symb = x(x_id); % Update value of x_symb
%     for y_id = 1:100
%         y_symb = y(y_id);
%         Z(x_id,y_id) = subs(potential_symbolic); % Evaluate potential_symbolic using the values of x&y_symb
%     end
% end
% 
% %%% VISUALIZE
% if flag_visualize
%     figure; hold on
%     subplot(1,2,1); hold on
%         title(strcat("(numeric) spiral surface"))
%         surface(x,y,potential_numeric' - min(potential_numeric(:)))
%         xlim([x_min,x_max])
%         ylim([y_min,y_max])
%     subplot(1,2,2); hold on
%         title(strcat("(symbolic) spiral surface"))
%         surface(x,y,Z'- min(Z(:)))
%         xlim([x_min,x_max])
%         ylim([y_min,y_max])
% end

end