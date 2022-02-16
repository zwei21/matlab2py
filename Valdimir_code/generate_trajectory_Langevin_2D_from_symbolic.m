% generate_trajectory_Langevin_from_symbolic_2D()

function traj_langevin = generate_trajectory_Langevin_from_symbolic_2D(potential_symbolic,position_initial, friction,simul_lagtime,n_steps)
% Overdampled Langevin equations

KbT = 0.5981; % KbT


% flag_plot = 1;
%%% INPUT
% x_0 = [0,0];
% simul_lagtime = 0.1;
% diffusion = 0.3;
% n_steps = 1000;

%%% Not certain it is required
tmp_vars = num2cell(symvar(potential_symbolic)); % Get all the variables used in the symbolic expression 'potential_symbolic' into a cell
n_dim = length(tmp_vars);
[x_symb,y_symb] = tmp_vars{:}; 


%%% Symbolic derivatives with respect to x and y
dpotsym_dx = diff(potential_symbolic,x_symb);
dpotsym_dy = diff(potential_symbolic,y_symb);


traj_langevin =  zeros(n_dim,n_steps);
traj_langevin(:,1) = position_initial;
for step = 2:n_steps
    
    x_symb = traj_langevin(1,step-1); % Update values of x_symb for current position
    y_symb = traj_langevin(2,step-1);
    drift = -1.*[subs(dpotsym_dx) ; subs(dpotsym_dy)]; % Evaluate the symbolic function at the current values of []_symb
    
    traj_langevin(:,step) = traj_langevin(:,step-1) + drift.*simul_lagtime/friction + randn(2,1).*sqrt(simul_lagtime*KbT/friction);
%     traj_langevin(:,step) = traj_langevin(:,step-1) + drift.*simul_lagtime + randn(2,1).*sqrt(simul_lagtime*diffusion);

end


end
