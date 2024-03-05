clear *;
close all;

% 1. Smooth tajectories
% 2. Limit traj to range of videos
% 3. Find closest match from neighboring cameras at given frame
% 4. Also make sure ground is taken into consideration

offset_len = 6000;
traj_min_time = 10;
tracks_path = "processed_tracks\";
og_tracks_center_path = "tracks\n3\";
og_tracks_left_path = "tracks\n1\";
og_tracks_right_path = "tracks\n2\";
cam_param_path = "calib_data\";
out_path = "3d_traj\";

bdry_txt_fname = "sync_length_area.txt";
[sess, ang, flag, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6] = ...
    textread(bdry_txt_fname, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d");

directory = dir(tracks_path);
num_files = numel(directory);
for i = 1:33
    for j = 1:num_files
        fname = directory(j).name;
        fname_list = strsplit(fname , "_");
        if (fname_list(end) == "out.mat") && (str2double(fname_list(1)) == i)
            % load (undistorted and smooth) trajectories
            disp(fname);
            load(og_tracks_center_path + fname_list(1) + "_s.mat", "traj_starts", "dyn_idx_threshold");
            stat_th_c_l = dyn_idx_threshold;
            stat_th_c_h = length(traj_starts);
            load(og_tracks_left_path + fname_list(1) + "_s.mat", "traj_starts", "dyn_idx_threshold");
            stat_th_l_l = dyn_idx_threshold;
            stat_th_l_h = length(traj_starts);
            load(og_tracks_right_path + fname_list(1) + "_s.mat", "traj_starts", "dyn_idx_threshold");
            stat_th_r_l = dyn_idx_threshold;
            stat_th_r_h = length(traj_starts);
            load(tracks_path + fname);
            traj_starts_c = var1;
            trajectories_c = var2;
            traj_starts_r = var3;
            trajectories_r = var4;
            traj_starts_l = var5;
            trajectories_l = var6;
            traj_old_idx_l = var7;
            traj_old_idx_r = var8;
            traj_old_idx_c = var9;

            % load intrinsics
            if i <= 28
                load(cam_param_path + "n1_1-28.mat");
            else
                load(cam_param_path + "n1_29-33.mat");
            end
            cp_l = cp;
            load(cam_param_path + "n2_1-33.mat");
            cp_r = cp;
            load(cam_param_path + "n3_1-33.mat");
            cp_c = cp;

            % load extrinsics and camera parameters
            load(cam_param_path + fname_list(1) + "_1.mat");
            R_l = R;
            t_l = t;
            P_l = cam_params;
            load(cam_param_path + fname_list(1) + "_2.mat");
            R_r = R;
            t_r = t;
            P_r = cam_params;
            load(cam_param_path + fname_list(1) + "_3.mat");
            R_c = R;
            t_c = t;
            P_c = cam_params;

            trajectories_real = {};
            traj_starts_real = {};
            offset_st = str2double(fname_list(2)) * offset_len;
            offset_ed = offset_st + offset_len;
            bdry_idx = i * 3;
            bdry_pts = [x1(bdry_idx), y1(bdry_idx); x6(bdry_idx), y6(bdry_idx)];
            bdry_pts = undistortPoints(bdry_pts, cp_c);
            bdry_th = (bdry_pts(1, 2) + bdry_pts(2, 2)) / 2;
            num_traj = length(trajectories_c);
            for k = 1:num_traj
                traj_st = traj_starts_c{k};
                traj = trajectories_c{k};
                traj_len = size(traj, 1);
                traj_ed = traj_st + traj_len - 1;
                if traj_st > offset_ed
                    continue;
                end
                if traj_st <= offset_st
                    trunc = offset_st - traj_st + 1;
                    if trunc >= traj_len
                        continue;
                    else
                        traj_st = traj_st + trunc;
                        traj = traj((1+trunc):end, :);
                    end
                end
                if traj_ed > offset_ed
                    trunc = traj_ed - offset_ed;
                    traj = traj(1:(end-trunc), :);
                end

                [traj_st, traj] = shorten_traj(traj_st, traj, bdry_th);
                traj_len = size(traj, 1);
                if traj_len > traj_min_time
                    traj_tmp = zeros(traj_len, 3);
                    traj_new = zeros(traj_len, 3);
                    for t = 1:traj_len
                        traj_pt = traj(t, :);
                        [score_l, real_pt_l] = check_best_match(traj_pt, traj_st + t - 1, trajectories_l, traj_starts_l, P_c, P_l);
                        [score_r, real_pt_r] = check_best_match(traj_pt, traj_st + t - 1, trajectories_r, traj_starts_r, P_c, P_r);
                        if score_l < score_r
                            traj_tmp(t, :) = real_pt_l;
                        else
                            traj_tmp(t, :) = real_pt_r;
                        end
                    end
                    traj_tmp_heights = sort(traj_tmp(:, 3));
                    avg_height = mean(traj_tmp_heights(round(0.25*traj_len):round(0.75*traj_len)));
                    p1_1 = P_c(1, :);
                    p1_2 = P_c(2, :);
                    p1_3 = P_c(3, :);
                    for t = 1:traj_len
                        pos1 = traj(t, :);
                        A = [pos1(2) * p1_3 - p1_2; ...
                             p1_1 - pos1(1) * p1_3; ...
                             0, 0, 1, -avg_height]; 
                        [~, ~, V] = svd(A);
                        pos_3d = V(:,4);
                        pos_3d = [pos_3d(1) / pos_3d(4), ...
                                  pos_3d(2) / pos_3d(4), ...
                                  pos_3d(3) / pos_3d(4)];
                        traj_new(t, :) = pos_3d;
                    end
                    traj_starts_real{end + 1} = traj_st;
                    trajectories_real{end + 1} = traj_new;
                end
            end

            save(out_path + fname, "trajectories_real", "traj_starts_real");
        end
    end
end

function [new_traj_st, new_traj] = shorten_traj(traj_st, traj, bdry_th)
% delete segments where the ped is entering the door
    front_bdry = 1;
    back_bdry = size(traj, 1);
    while (front_bdry <= back_bdry) && (traj(front_bdry, 2) < bdry_th)
        front_bdry = front_bdry + 1;
    end
    while (front_bdry <= back_bdry) && (traj(back_bdry, 2) < bdry_th)
        back_bdry = back_bdry - 1;
    end
    new_traj_st = traj_st + front_bdry - 1;
    new_traj = traj(front_bdry:back_bdry, :);
end

function [best_score, real_pt] = check_best_match(pos1, time_idx, trajectories, traj_starts, P1, P2)
% find the best match point among the trajectories for the given point and
% time.
    p1_1 = P1(1, :);
    p1_2 = P1(2, :);
    p1_3 = P1(3, :);
    p2_1 = P2(1, :);
    p2_2 = P2(2, :);
    p2_3 = P2(3, :);

    z_lim_l = 100;
    z_lim_h = 1200;

    num_traj = length(trajectories);
    real_pt = [0 0 0];
    best_score = Inf;
    for i = 1:num_traj
        traj = trajectories{i};
        traj_len = size(traj, 1);
        traj_st = traj_starts{i};
        traj_ed = traj_st + traj_len - 1;
        if (time_idx >= traj_st) && (time_idx <= traj_ed)
            pos2 = traj(time_idx - traj_st + 1, :);
            A = [pos1(2) * p1_3 - p1_2;
                 p1_1 - pos1(1) * p1_3;
                 pos2(2) * p2_3 - p2_2;
                 p2_1 - pos2(1) * p2_3];
            [~, S, V] = svd(A);
            pos_3d = V(:,4);
            pos_3d = [pos_3d(1) / pos_3d(4), ...
                      pos_3d(2) / pos_3d(4), ...
                      pos_3d(3) / pos_3d(4)];
            score = S(4, 4);
            if (pos_3d(3) > z_lim_l) && (pos_3d(3) < z_lim_h) && (score < best_score)
                best_score = score;
                real_pt = pos_3d;
            end
        end
    end
end