addpath(genpath('./')) % Add current folder and all subfolders to Workspace 

%% PARAMETERS
n_states = [200,200];
n_branches = 2;

%% GENERATE 2D SURFACE 

flag_visualize = 1;
%[potential_numeric, potential_symbolic, x , y] = generate_potential_2d_Zshape(n_states,flag_visualize);
[potential_numeric, potential_symbolic, x , y] = generate_potential_2d_spirals(n_states,n_branches, flag_visualize);
%[potential_numeric, potential_symbolic, x, y] = generate_potential_2d_concentric(n_states, flag_visualize); % Funny potential (Concentric circles (wells) around the global minimum
% [potential_numeric, potential_symbolic, x, y] = generate_potential_2d_Rosenbook(IN_n_states,flag_visualize)

%% GENERATE TRAJECTORY
% Overdamped Lagevin dynamics 
% (See paper "Position-Dependent Diffusion from Biased Simulations and Markov State Model Analysis" from F.Sicard et.al. (2021)
position_initial = [0.1,0.1];
friction = 10;
simul_lagtime = 0.25;
n_steps = 5000;

traj_langevin = generate_trajectory_Langevin_2D_from_symbolic(potential_symbolic, position_initial, friction, simul_lagtime,n_steps);

% % ALTERNATIVE - Monte Carlo simulation
% max_distance_MC = 0.1;
% boundaries = [[x(1),x(end)];[y(1),y(end)]];
% traj_MC = generate_trajectory_MC_2D_from_symbolic(potential_symbolic,n_steps,position_initial,max_distance_MC,boundaries);



%% VISUALIZE Trajectory on 2D

%EXAMPLE TRAJECTORY OUT OF THE FOR LOOP

traj_to_visualize = traj_langevin;
% traj_to_visualize = traj_MC;

figure; hold on
surface(x,y,potential_numeric','FaceAlpha',0.5,'EdgeAlpha',0)
%p=plot3(traj_to_visualize(1,:),traj_to_visualize(2,:),ones(1,length(traj_to_visualize(1,:))).*max(potential_numeric(:)),'o-','Color','k','MarkerSize',1,'MarkerEdgeColor','k','MarkerFaceColor','k','DisplayName','Sampled ');
%p.Color(4) = 0.2;
% scatter(traj_langevin(1,:),traj_langevin(2,:),2,'filled','MarkerFaceColor','k');
xlim([x(1),x(end)])
ylim([y(1),y(end)])


%% Generate Multiple trajs 

n_trajs = 250;
all_trajs = zeros(2, n_steps, n_trajs);
tic
for i = 1:n_trajs
    k = string(i);
    disp(["Creating Simulation number ", k])
    traj_langevin = generate_trajectory_Langevin_2D_from_symbolic(potential_symbolic, position_initial, friction, simul_lagtime,n_steps);
    traj_to_visualize = traj_langevin;
    p=plot3(traj_to_visualize(1,:),traj_to_visualize(2,:),ones(1,length(traj_to_visualize(1,:))).*max(potential_numeric(:)),'o-','Color','k','MarkerSize',1,'MarkerEdgeColor','k','MarkerFaceColor','k','DisplayName','Sampled ');
    all_trajs(:,:,i) = traj_langevin;
    p.Color(4) = 0.2;
end 
toc

%% Saving the values to a file 

writematrix(all_trajs, "data_spiral/2D_spiral_less_deep.csv")

