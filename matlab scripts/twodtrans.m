clear *;

rw_r = [5.3040    1.5510
    3.7920    1.3620
    4.0950   -1.0580
    5.6070   -0.8685];

R = [0, -1, 0; 1, 0, 0; 0, 0, 1];
rw = R * [rw_r'; 0, 0, 0, 0];
rw = rw(1:2, :)';

img = [410.3748  187.7648
  312.6765   25.9520
  973.6664  122.1237
  790.4821  221.3485];

A = [];
for i = 1:4
    a1 = [0, 0, 0, -rw(i, 1), -rw(i, 2), -1, img(i, 2) * rw(i, 1), img(i, 2) * rw(i, 2), img(i, 2)];
    a2 = [rw(i, 1), rw(i, 2), 1, 0, 0, 0, -img(i, 1) * rw(i, 1), -img(i, 1) * rw(i, 2), -img(i, 1)];
    a3 = [img(i, 2) * rw(i, 1), img(i, 2) * rw(i, 2), img(i, 2),  img(i, 1) * rw(i, 1), img(i, 1) * rw(i, 2), img(i, 1), 0, 0, 0];
    A = [A;a1;a2;a3];
end

[u,s,v] = svd(A);
h = reshape(v(:, 9), [3, 3])';
h = h / h(3,3);

h2 = estgeotform2d(rw, img, 'projective');
h2 = h2.A;

coords = h * [rw';1,1,1,1];
[coords(1,:) ./ coords(3, :); coords(2,:) ./ coords(3,:)]
coords = h2 * [rw';1,1,1,1];
[coords(1,:) ./ coords(3, :); coords(2,:) ./ coords(3,:)]


