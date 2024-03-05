clear *;
close all;

num_pts = 8;

bath_path = "scenes";
left_path = bath_path + "\n1\";
right_path = bath_path + "\n2\";
center_path = bath_path + "\n3\";

session = "1";
img_name = session + ".jpg"
% vid_name = session + "_traj.avi";

left_img = imread(left_path + img_name);
right_img = imread(right_path + img_name);
center_img = imread(center_path + img_name);

% obj_l = VideoReader(left_path + vid_name);
% obj_l.CurrentTime = 1;
% left_img = readFrame(obj_l);
% obj_r = VideoReader(right_path + vid_name);
% obj_r.CurrentTime = 1;
% right_img = readFrame(obj_r);
% obj_c = VideoReader(center_path + vid_name);
% obj_c.CurrentTime = 1;
% center_img = readFrame(obj_c);

h = figure(1);
hold on;
montage({left_img, center_img, right_img}, "Size", [1,3]);
hold off;
%waitfor(h);

left_coords = [];
for i = 1:num_pts
    figure(2);
    imshow(left_img);
    roi = drawpoint;
    left_coords = [left_coords, roi.Position];
end

right_coords = [];
for i = 1:num_pts
    figure(2);
    imshow(right_img);
    roi = drawpoint;
    right_coords = [right_coords, roi.Position];
end

center_coords = [];
for i = 1:num_pts
    figure(2);
    imshow(center_img);
    roi = drawpoint;
    center_coords = [center_coords, roi.Position];
end

center_coords = round(center_coords);
left_coords = round(left_coords);
right_coords = round(right_coords);

disp("1:");
disp(strjoin(string(left_coords), ","));
disp("2:");
disp(strjoin(string(right_coords), ","));
disp("3:");
disp(strjoin(string(center_coords), ","));

