import cv2 as cv
import os
import numpy as np

directories = ["n1/stitched_videos_mp4",
               "n2/stitched_videos_mp4",
               "n3/stitched_videos_mp4"]

for directory in directories:
    files = os.listdir(directory)
    for f in files:
        if f.endswith(".mp4"):
            print("Processing {} ...".format(f))
            cap = cv.VideoCapture(os.path.join(directory, f))
            length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
            fourcc = cv.VideoWriter_fourcc(*'XVID')
            name_list = f.split(".")
            out_name = os.path.join(directory, name_list[0] + ".avi")
            out = cv.VideoWriter(out_name, fourcc, 60, (1280, 1024))
            count = 0
            while cap.isOpened() and (count < length):
                ret, frame = cap.read()
                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                out.write(frame)
                print("Writing {} / {} \r".format(count, length), end = "")
                count += 1
            out.release()
            cap.release()
