clear *;
close all;

K = [8.335785146896855622e+02 0.000000000000000000e+00 6.438625261682303744e+02
0.000000000000000000e+00 8.335785146896855622e+02 5.128115964245195073e+02
0.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00
];
dist = [-3.633885875223855089e-01 1.879531475760448100e-01 1.266859148986722652e-03 9.066027148124454049e-04 -6.014107701684617141e-02];
lrc = 3;
bath_path = "scenes";
left_path = bath_path + "\n1\";
right_path = bath_path + "\n2\";
center_path = bath_path + "\n3\";

cp = cameraParameters('K', K, ...
                      'ImageSize', [1024, 1280], ...
                      'radialDistortion', [dist(1), dist(2), dist(5)], ...
                      'tangentialDistortion', [dist(4), dist(3)]);

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
    img_un = undistortImage(img, cp);
    imshow(img_un);
    uiwait(fig);
end