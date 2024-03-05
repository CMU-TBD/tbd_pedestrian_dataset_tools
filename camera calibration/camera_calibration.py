import numpy as np
import cv2, os

from charuco_calibration import CharucoCalibration
from april_detect import AprilDetect

def save_calib_params(path, vid_name):

    calib_vid = os.path.join(path, vid_name)

    vis = False

    charuco = CharucoCalibration()

    ret, mtx, dist, rvecs, tvecs = charuco.calibrate(calib_vid, is_vid=True, check_calib=vis)

    print("Intrinsics")
    print(ret)
    print(mtx)
    print(dist)

    name_list = vid_name.split(".")
    txt_name = name_list[0]
    txt = os.path.join(path, "{}_mtx.txt".format(txt_name))
    np.savetxt(txt, mtx)
    txt = os.path.join(path, "{}_dist.txt".format(txt_name))
    np.savetxt(txt, dist)

    return

if __name__ == "__main__":
    path = "dset_calib"
    for fname in os.listdir(path):
        if fname.endswith('.avi'):
            save_calib_params(path, fname)


"""
april = AprilDetect(mtx)

num_vid = 11
for i in range(num_vid):
    tag_vid = "camera_test2/{}_{}.avi".format(cam_idx, i + 1)
    cap = cv2.VideoCapture(tag_vid)
    _, frame = cap.read()
    frame = cv2.undistort(frame, mtx, dist, None)
    tags, _ = april.detect_tag(frame, 42, estimate_pose=True, 
                               visualization="{}_{}.jpg".format(cam_idx, i + 1))
    cap.release()

cart_idx = 1
cart_vid = "camera_test3/cart_{}/stitched_video.mp4".format(cart_idx)
cap = cv2.VideoCapture(cart_vid)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
out = cv2.VideoWriter("camera_test3/cart_{}/detected.mp4".format(cart_idx),
                      cv2.VideoWriter_fourcc('M','P','4','V'), 
                      60, 
                      (frame_width,frame_height))
idx = 0
while (cap.isOpened()):
    print('{} / {} \r'.format(idx, frame_cnt))
    ret, frame = cap.read()
    frame = cv2.undistort(frame, mtx, dist, None)
    tags, frame = april.detect_tag(frame, 26, estimate_pose=True, 
                                   visualization="cart.jpg")
    out.write(frame)
    idx += 1

cap.release()
out.release()
"""
