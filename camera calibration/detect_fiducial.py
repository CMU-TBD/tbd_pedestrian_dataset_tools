import numpy as np
import cv2

from charuco_calibration import CharucoCalibration as cc
from april_detect import AprilDetect as ad

if __name__ == "__main__":
    calib = cc()
    ret, cam_mat, distort, rvec, tvec = calib.calibrate("calib/calib.avi")
    april_detector = ad(cam_mat)

    file_dir = "imgs_09222021"
    fid_fname = file_dir + "/fiducial.mp4"
    tag_size = 20

    cap = cv2.VideoCapture(fid_fname)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    v_write = cv2.VideoWriter(file_dir + "/tag_output.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60, (frame_width, frame_height))
    if (cap.isOpened() == False):
        print("video file read error!")
    idx = 0
    tot_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            print([idx, tot_frames], end="\r")
            undist_frame = cv2.undistort(frame, cam_mat, distort, None)
            tags = april_detector.detect_tag(undist_frame, tag_size)
            new_frame = april_detector.draw_tags(undist_frame, tags)
            v_write.write(new_frame)
            idx += 1
        else:
            print("Frame grab error!")
            break
    cap.release()
    v_write.release()
