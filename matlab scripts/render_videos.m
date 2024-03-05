clear *;
close all;

vid_test = true;
plot_test = false;

cp_file = "calib_data/n3_1-33.mat";
load(cp_file, "cp");

traj_file_path = "3d_traj/";
directory = dir(traj_file_path);
num_files = numel(directory);

parpool(6);
parfor i = 1:num_files
    name = directory(i).name;
    if endsWith(name, "out.mat")
	disp(name + " (start)");
    name_list = strsplit(name, "_");
	sess = name_list(1);
	seg = name_list(2);

        vid_name = "n3/stitched_videos_mp4/" + sess + "_" + seg + ".avi";
        save_name = "traj_vids/" + sess + "_" + seg + ".avi";

        param_files = "calib_data/" + sess + "_3.mat";
        S = load(param_files, "cam_params");
	    P = S.cam_params;
        real_traj_file = "3d_traj/" + name;
        S = load(real_traj_file, "trajectories_real", "traj_starts_real");
	    traj_starts_real = S.traj_starts_real;
	    trajectories_real = S.trajectories_real;
        num_traj = length(trajectories_real);

        traj_starts = traj_starts_real;
        trajectories = {};
        traj_file = "tests\test_traj.mat";
        for j = 1:num_traj
            traj = trajectories_real{j};
            traj_len = size(traj, 1);
            traj(:, 3) = 0;
            traj_2d = P * [traj'; ones(1, traj_len)];
            traj_2d(1, :) = traj_2d(1, :) ./ traj_2d(3, :);
            traj_2d(2, :) = traj_2d(2, :) ./ traj_2d(3, :);
            trajectories{end + 1} = traj_2d(1:2, :)';
        end
    
	offset = str2double(seg) * 6000;
    plot_trajectories(vid_name, save_name, trajectories, traj_starts, cp, offset);

	disp(name + " (finish)");
    end
end
