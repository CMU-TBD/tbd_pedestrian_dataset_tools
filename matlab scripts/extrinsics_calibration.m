clear *;
close all;

lrc = 1;
vis_check = false;

bath_path = "scenes";
left_path = bath_path + "\n1\";
right_path = bath_path + "\n2\";
center_path = bath_path + "\n3\";

load("calib_data\real_world.mat");
txt_fname = "pt_corr.txt";
[sess, ang, flag, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8] = ...
    textread(txt_fname, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d");

num_pts = 8;
for i = 1:33
    disp(i);
    img_name = int2str(i) + ".jpg";
    if lrc == 1
        img = imread(left_path + img_name);
    elseif lrc == 2
        img = imread(right_path + img_name);
    elseif lrc == 3
        img = imread(center_path + img_name);
    end
    
    idx = (i - 1) * 3 + lrc;
    assert(sess(idx) == i);
    assert(ang(idx) == lrc);

    if (lrc == 1) && (i <= 28)
        load("calib_data\n1_1-28.mat", "cp");
        if (flag(idx) == 0)
            real_world_coords = real_left_coords;
        else
            real_world_coords = alt_left_coords;
        end
    elseif (lrc == 1) && (i > 28)
        load("calib_data\n1_29-33.mat", "cp");
        if (flag(idx) == 0)
            real_world_coords = real_left_coords;
        else
            real_world_coords = alt_left_coords;
        end
    elseif (lrc == 2)
        load("calib_data\n2_1-33.mat", "cp");
        if (flag(idx) == 0)
            real_world_coords = real_right_coords;
        else
            real_world_coords = alt_right_coords;
        end
    elseif (lrc == 3)
        load("calib_data\n3_1-33.mat", "cp");
        if (flag(idx) == 0)
            real_world_coords = real_center_coords;
        else
            real_world_coords = alt_center_coords;
        end
    end

    img_coords = [ ...
        x1(idx), y1(idx); ...
        x2(idx), y2(idx); ...
        x3(idx), y3(idx); ...
        x4(idx), y4(idx); ...
        x5(idx), y5(idx); ...
        x6(idx), y6(idx); ...
        x7(idx), y7(idx); ...
        x8(idx), y8(idx)];
    img_coords = undistortPoints(img_coords, cp);
%     img_coords(:, 2) = 1024 - img_coords(:, 2);

    A = zeros(num_pts * 2, 12);
    for j = 1:num_pts
        real_x = real_world_coords(j, 1);
        real_y = real_world_coords(j, 2);
        real_z = real_world_coords(j, 3);
        img_x = img_coords(j, 1);
        img_y = img_coords(j, 2);
        a1 = [real_x, real_y, real_z, 1, 0, 0, 0, 0, -img_x * real_x, -img_x * real_y, -img_x * real_z, -img_x];
        a2 = [0, 0, 0, 0, real_x, real_y, real_z, 1, -img_y * real_x, -img_y * real_y, -img_y * real_z, -img_y];
        A(j * 2 - 1, :) = a1;
        A(j * 2, :) = a2;
    end
    [U, S, V] = svd(A);
    cam_params = reshape(V(:,12), [4, 3])';

    if vis_check == true
        coords = [real_world_coords'; ones(1, num_pts)];
        proj_coords = cam_params * coords;
        proj_coords(1, :) = proj_coords(1, :) ./ proj_coords(3, :);
        proj_coords(2, :) = proj_coords(2, :) ./ proj_coords(3, :);
        fig = figure;
        imshow(undistortImage(img, cp));
        hold on;
        scatter(proj_coords(1,:), proj_coords(2,:), "filled");
        hold off;
        uiwait(fig);
    end

    [K, R] = rqGivens(cam_params(:, 1:3));
    T = diag(sign(diag(K)));
    K = K * T;
%     R = T * R;
    [U, S, V] = svd(cam_params);
    t = V(:,4) / V(4,4);
    t = t(1:3);

    save_name = "calib_data\" + int2str(i) + "_" + int2str(lrc) + ".mat";
    save(save_name, "cam_params", "R", "t");

end