function [] = plot_trajectories(vid_name, save_fname, trajectories, traj_starts, cp, offset)

    v_read = VideoReader(vid_name);
    v_write = VideoWriter(save_fname);
    v_write.FrameRate = v_read.FrameRate;
    interval = round(v_read.FrameRate / v_write.FrameRate);
    open(v_write);
    vid_idx = offset;
    num_ped = length(trajectories);
    
    ws = 3;
    colors = [255, 255, 255; 
              0,   255, 255; 
              255, 0,   255; 
              255, 255, 0; 
              255, 0,   0; 
              0,   255, 0; 
              0,   0,   255];
    num_colors = size(colors, 1);

    ped_set = zeros(1, num_ped);
    color_set = cell(1, num_ped);
    mask_set = cell(1, num_ped);
    for i = 1:num_ped
        mask_set{i} = zeros(v_read.Height, v_read.Width, 3, "uint8");
    end
    curr_pt_set = zeros(num_ped, 2);

    vid_idx = vid_idx - 1;
    for i = 1:num_ped
        if (vid_idx >= traj_starts{i}) && (vid_idx < (traj_starts{i} + size(trajectories{i}, 1)))
            traj = trajectories{i};
            for j = 1:(vid_idx - traj_starts{i} + 1)
                pt = round(traj(j, :));
                window_r = max(pt(2)-ws, 1):min(pt(2)+ws, v_read.Height);
                window_c = max(pt(1)-ws, 1):min(pt(1)+ws, v_read.Width);
                mask = ones(length(window_r), length(window_c), 3);
                mask_set{i}(window_r, window_c, :) = mask;
            end
        end
    end
    
    while hasFrame(v_read)
        if mod(vid_idx, 2500) == 0
            disp([vid_idx - offset, v_read.NumFrames]);
        end

        frame = readFrame(v_read);
        frame = undistortImage(frame, cp);
        vid_idx = vid_idx + 1;       

        for i = 1:num_ped
            if (vid_idx >= traj_starts{i}) && (vid_idx < (traj_starts{i} + size(trajectories{i}, 1)))
                if ped_set(i) == 0
                    ped_set(i) = 1;
                end
                pt = trajectories{i}(vid_idx - traj_starts{i} + 1, :);
                pt = round(pt);
   
                window_r = max(pt(2)-ws, 1):min(pt(2)+ws, v_read.Height);
                window_c = max(pt(1)-ws, 1):min(pt(1)+ws, v_read.Width);
                mask = ones(length(window_r), length(window_c), 3);
                mask_set{i}(window_r, window_c, :) = mask;
                
                curr_pt_set(i, :) = pt;
            else
                if ped_set(i) == 1
                    ped_set(i) = 0;
                end
            end
        end

        if mod(vid_idx, interval) == 0
            for i = 1:num_ped
                if ped_set(i) == 1
                    color = colors(mod(i, num_colors) + 1, :);
                    color_set{i} = color;
                    color_mask = mask_set{i};
                    color_mask(:, :, 1) = color_mask(:, :, 1) * color(1);
                    color_mask(:, :, 2) = color_mask(:, :, 2) * color(2);
                    color_mask(:, :, 3) = color_mask(:, :, 3) * color(3);
                    frame = frame .* (1 - mask_set{i}) + color_mask;
                    frame = insertText(frame, curr_pt_set(i, :), num2str(i));
                end
            end
            writeVideo(v_write, frame);
        end
    end

    close(v_write);
end

