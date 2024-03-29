clear *;
close all;

load('C:\Users\allan\Desktop\HDCv2\calib_data\1_1.mat');
R1 = R;
t1 = t;
load('C:\Users\allan\Desktop\HDCv2\calib_data\1_2.mat');
R2 = R;
t2 = t;
load('C:\Users\allan\Desktop\HDCv2\calib_data\1_3.mat');
R3 = R;
t3 = t;

scale = 500;
trans1_x = R1 \ [1;0;0] * scale + t1;
trans2_x = R2 \ [1;0;0] * scale + t2;
trans3_x = R3 \ [1;0;0] * scale + t3;
trans1_y = R1 \ [0;1;0] * scale + t1;
trans2_y = R2 \ [0;1;0] * scale + t2;
trans3_y = R3 \ [0;1;0] * scale + t3;
trans1_z = R1 \ [0;0;1] * scale + t1;
trans2_z = R2 \ [0;0;1] * scale + t2;
trans3_z = R3 \ [0;0;1] * scale + t3;
trans_x = [trans1_x, trans2_x, trans3_x];
trans_y = [trans1_y, trans2_y, trans3_y];
trans_z = [trans1_z, trans2_z, trans3_z];
origins = [t1, t2, t3, [0;0;0]];
scatter3(trans_x(1,:), trans_x(2,:), trans_x(3,:), "b", "filled");
hold on;
scatter3(trans_y(1,:), trans_y(2,:), trans_y(3,:), "r", "filled");
scatter3(trans_z(1,:), trans_z(2,:), trans_z(3,:), "g", "filled");
scatter3(origins(1,:), origins(2,:), origins(3,:), "k", "filled");axis equal;
