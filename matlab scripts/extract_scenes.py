import numpy as np
import cv2 as cv
import os

num_vids = 33
base_dir_l = "n1"
base_dir_r = "n2"
base_dir_c = "n3"
base_dirs = [base_dir_l, base_dir_r, base_dir_c]

for i in range(num_vids):
    print(i)
    for j in range(3):
        in_directory = os.path.join(base_dirs[j], "stitched_videos_mp4")
        out_directory = os.path.join(base_dirs[j], "scenes")

        in_name = os.path.join(in_directory, str(i+1) + ".mp4")
        out_name = os.path.join(out_directory, str(i+1) + ".jpg")
        cap = cv.VideoCapture(in_name)
        cap.set(cv.CAP_PROP_POS_FRAMES, 100)
        _, frame = cap.read()
        cv.imwrite(out_name, frame)
        cap.release()
