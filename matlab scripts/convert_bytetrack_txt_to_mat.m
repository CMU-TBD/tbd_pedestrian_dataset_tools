% the tracking results are on raw (distorted) images

clear *;
close all;

txtdir = "data_batch2/n1/track_results";
directory = dir(txtdir);

for f = 1:numel(directory)
    name = directory(f).name;
    [f, numel(directory)]
    if endsWith(name, '.txt')
        fname = strcat(txtdir, '/', name);
        [frame_id, ped_id, coord_x, coord_y, len_x, len_y, conf, tag_1, tag_2, tag_3] = textread(fname, '%d,%d,%f,%f,%f,%f,%f,%d,%d,%d');
        ped_id_set = unique(ped_id);
        num_ped = numel(ped_id_set);
        trajectories = cell(1, num_ped);
        traj_starts = cell(1, num_ped);
        for i = 1:num_ped
            curr_ped_frames = frame_id(ped_id == ped_id_set(i));
            curr_ped_coords = [coord_x(ped_id == ped_id_set(i)), coord_y(ped_id == ped_id_set(i))];
            curr_ped_len = [len_x(ped_id == ped_id_set(i)), len_y(ped_id == ped_id_set(i))];
            curr_ped_len(:, 1) = curr_ped_len(:, 1) / 2;
            curr_ped_coords = round(curr_ped_coords + curr_ped_len);
            traj_starts{i} = curr_ped_frames(1);
            trajectories{i} = curr_ped_coords;
        end
        tmp = strsplit(fname, ".");
        save(strcat(tmp{1}, ".mat"),"trajectories","traj_starts");
    end
end
