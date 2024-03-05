clear *;
close all;

lrc = 3;
num_pts = 6;
if num_pts == 6
    txt_fname = "sync_length_area.txt";
    [sess, ang, flag, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6] = ...
        textread(txt_fname, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d");
elseif num_pts == 8
    txt_fname = "pt_corr.txt";
    [sess, ang, flag, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8] = ...
        textread(txt_fname, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d");
end

bath_path = "scenes";
left_path = bath_path + "\n1\";
right_path = bath_path + "\n2\";
center_path = bath_path + "\n3\";

color = 'y';
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
    fig = figure;
    imshow(img);
    hold on;
    if num_pts == 6
        x = [x1(idx),x2(idx),x3(idx),x4(idx),x5(idx),x6(idx)];
        y = [y1(idx),y2(idx),y3(idx),y4(idx),y5(idx),y6(idx)];
    elseif num_pts == 8
        x = [x1(idx),x2(idx),x3(idx),x4(idx),x5(idx),x6(idx),x7(idx),x8(idx)];
        y = [y1(idx),y2(idx),y3(idx),y4(idx),y5(idx),y6(idx),y7(idx),y8(idx)];
    end
    scatter(x,y,'filled');
    text(x1(idx), y1(idx), "1", "Color", color);
    text(x2(idx), y2(idx), "2", "Color", color);
    text(x3(idx), y3(idx), "3", "Color", color);
    text(x4(idx), y4(idx), "4", "Color", color);
    text(x5(idx), y5(idx), "5", "Color", color);
    text(x6(idx), y6(idx), "6", "Color", color);
    if num_pts == 8
        text(x7(idx), y7(idx), "7", "Color", color);
        text(x8(idx), y8(idx), "8", "Color", color);
    end
    hold off;
    uiwait(fig);
end