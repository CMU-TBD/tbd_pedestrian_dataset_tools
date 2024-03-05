clear *;
close all;

% 1. Smooth tajectories
% 2. Limit traj to range of videos
% 3. Find closest match from neighboring cameras at given frame
% 4. Also make sure ground is taken into consideration

offset_len = 6000;
tracks_path = "n3/track_results/";
tracks_left_path = "n1/track_results/";
tracks_right_path = "n2/track_results/";
cam_param_path = "calib_data/";
out_path = "processed_tracks/";

directory = dir(tracks_path);
num_files = numel(directory);

%parpool(3);
for i = 1:33
    for j = 1:num_files
        fname = directory(j).name;
        fname_list = strsplit(fname , "_");
        if (fname_list(end) == "out.mat") && (str2double(fname_list(1)) == i)
            % load trajectories
            disp(fname);
            S = load(tracks_path + fname, "trajectories", "traj_starts");
            trajectories_c = S.trajectories;
            traj_starts_c = S.traj_starts;
            offset_seg = str2double(fname_list(2));
            offset = offset_seg * offset_len;

            S = load(tracks_left_path + fname_list(1) + "_s.mat", "trajectories", "traj_starts");
            trajectories_l = S.trajectories;
            traj_starts_l = S.traj_starts;
            S = load(tracks_right_path + fname_list(1) + "_s.mat", "trajectories", "traj_starts");
            trajectories_r = S.trajectories;
            traj_starts_r = S.traj_starts;

            % load intrinsics
            if i <= 28
                S = load(cam_param_path + "n1_1-28.mat", "cp");
            else
                S = load(cam_param_path + "n1_29-33.mat", "cp");
            end
            cp_l = S.cp;
            S = load(cam_param_path + "n2_1-33.mat", "cp");
            cp_r = S.cp;
            S = load(cam_param_path + "n3_1-33.mat", "cp");
            cp_c = S.cp;

            % undistort and smooth trajectories
            [trajectories_l, traj_starts_l, traj_old_idx_l] = process_trajectories(trajectories_l, traj_starts_l, cp_l, offset, offset_len);
            [trajectories_r, traj_starts_r, traj_old_idx_r] = process_trajectories(trajectories_r, traj_starts_r, cp_r, offset, offset_len);
            [trajectories_c, traj_starts_c, traj_old_idx_c] = process_trajectories(trajectories_c, traj_starts_c, cp_c, offset, offset_len);
            
            mysave(out_path + fname, traj_starts_c, trajectories_c, traj_starts_r, trajectories_r, traj_starts_l, trajectories_l, traj_old_idx_l, traj_old_idx_r, traj_old_idx_c);
        end
    end
end

function [trajectories_new, traj_starts_new, traj_old_idx] = process_trajectories(trajectories, traj_starts, cp, offset, offset_len)
    trajectories_new = {};
    traj_starts_new = {};
    traj_old_idx = {};
    smooth_ws = 5;
    for i = 1:length(trajectories)
        traj = trajectories{i};
        traj_len = size(traj, 1);
        traj_st = traj_starts{i};
        traj_ed = traj_starts{i} + traj_len;
        if ((traj_st > offset) && (traj_st <= (offset + offset_len))) || ...
           ((traj_ed > offset) && (traj_ed <= (offset + offset_len)))
            traj_starts_new{end + 1} = traj_st;
            traj_old_idx{end + 1} = i;
            traj_tmp = undistortPoints(traj, cp);
            traj_smth = zeros(traj_len, 2);
            for j = 1:traj_len
                if (j <= smooth_ws) || ((traj_len - j) < smooth_ws)
                    traj_smth(j, :) = traj_tmp(j, :);
                else
                    traj_smth(j, :) = mean(traj_tmp((j-smooth_ws):(j+smooth_ws), :), 1);
                end
            end
            trajectories_new{end + 1} = traj_smth;
        end
    end
end

function [] = mysave(name, var1, var2, var3, var4, var5, var6, var7, var8, var9)
    save(name, 'var1', 'var2', 'var3', 'var4', 'var5', 'var6', 'var7', 'var8', 'var9')
end
