clear *;
close all;

sess = "30";
seg = "0";
offset = str2double(seg) * 6000;

vid_test = true;
plot_test = false;

vid_name = "tests/" + sess + "_" + seg + ".avi";
save_name = "tests/out_" + sess + "_" + seg + ".avi";

cp_file = "calib_data/n3_1-33.mat";
load(cp_file, "cp");
param_files = "calib_data/" + sess + "_3.mat";
load(param_files);
real_traj_file = "3d_traj/" + sess + "_" + seg + "_out.mat";
load(real_traj_file);
num_traj = length(trajectories_real);

if plot_test == true
    frame_num = 593;
    colors = [0, 0, 0; 
              0,   255, 255; 
              255, 0,   255; 
              255, 255, 0; 
              255, 0,   0; 
              0,   255, 0; 
              0,   0,   255];
    num_colors = size(colors, 1);
    fig = figure;
    hold on;
    for i = 1:num_traj
        traj = trajectories_real{i};
        traj_len = size(traj, 1);
        traj_st = traj_starts_real{i};
        traj_ed = traj_st + traj_len - 1;
        if (frame_num >= traj_st) && (frame_num <= traj_ed)
            traj = traj(1:(frame_num - traj_st + 1), :);
            c = colors(mod(i, num_colors) + 1, :) / 255;
            scatter3(traj(:, 1), traj(:, 2), traj(:, 3), 10, c, "filled");
        end
    end
end

if vid_test == true
    traj_starts = traj_starts_real;
    trajectories = {};
    traj_file = "tests\test_traj.mat";
    for i = 1:num_traj
        traj = trajectories_real{i};
        traj_len = size(traj, 1);
        traj(:, 3) = 0;
        traj_2d = cam_params * [traj'; ones(1, traj_len)];
        traj_2d(1, :) = traj_2d(1, :) ./ traj_2d(3, :);
        traj_2d(2, :) = traj_2d(2, :) ./ traj_2d(3, :);
        trajectories{end + 1} = traj_2d(1:2, :)';
    end
    
    plot_trajectories(vid_name, save_name, trajectories, traj_starts, cp, offset);
end
