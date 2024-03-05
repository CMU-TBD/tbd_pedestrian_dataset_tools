clear *;
close all;

traj_dir = "3d_traj/";
directory = dir(traj_dir);
num_files = numel(directory);

sys_time_on = true;

curr_fps = 10;
target_fps = 10;
max_duration = 10 * 60;

frame_multiplier = 1;

traj_len_list = [];
traj_spd_list = [];
traj_den_list = [];

for i = 1:num_files
    name = directory(i).name;
    if endsWith(name, "_out.mat")
        disp(name);
        name_list = strsplit(name, "_");
        sess = name_list(1);
        seg = name_list(2);
        offset = round(str2double(seg) * 10 * 60 * target_fps);

        S = load(traj_dir + name, "trajectories_real", "traj_starts_real");
        traj_starts = S.traj_starts_real;
        trajectories = S.trajectories_real;
        num_traj = length(trajectories);

        if sys_time_on == true
            svo_time = 1675358798060104;
            rgb_frame_ref = 917 + 6000;
            time_st = svo_time - round(rgb_frame_ref / 10 * 1e6) + round(offset / 10 * 1e6);
            time_inc = round(1 / target_fps * 1e6);
        end

        if sys_time_on == true
            write_name = "tbd_data/" + sess + "_" + seg + "_t.txt";
        else
            write_name = "tbd_data/" + sess + "_" + seg + ".txt";
        end
        
        fID = fopen(write_name,  "w");

        time = 0;
        count = 0;
        traj_den = [];
        while time < max_duration
            frame_idx = round(time * curr_fps) + 1 + str2double(seg) * 6000;
            ped_count = 0;
            for j = 1:num_traj
                traj_st = traj_starts{j};
                traj = trajectories{j};
                traj_len = size(traj, 1);
                traj_ed = traj_st + traj_len - 1;
                if (frame_idx >= traj_st) && (frame_idx <= traj_ed)
                    frame = count * frame_multiplier;
                    ped = j;
                    x = traj(frame_idx - traj_st + 1, 1) / 1000;
                    y = traj(frame_idx - traj_st + 1, 2) / 1000;
                    if sys_time_on == true
                        fprintf(fID, "%d %.1f %.1f %.10f %.10f\n", [time_st + time_inc * count, offset + frame, ped, x, y]);
                    else
                        fprintf(fID, "%.1f %.1f %.10f %.10f\n", [offset + frame, ped, x, y]);
                    end
                    ped_count = ped_count + 1;
                end
            end
            count = count + 1;
            time = time + 1 / target_fps;
        end
        

        fclose(fID);
    end
end