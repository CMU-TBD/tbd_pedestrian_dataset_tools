import numpy as np
import cv2

from april_detect import AprilDetect as ad

class ExtrinsicEstimation(object):

    def __init__(self, fnames, is_vid = False):
        self.imgs = []
        for fname in fnames:
            if is_vid:
                cap = cv2.VideoCapture(fname)
                if (cap.isOpened() == False):
                    print("File read error!")
                ret, img = cap.read()
                if ret == False:
                    print("Frame grab error!")
                self.imgs.append(img)
            else:
                img = cv2.imread(fname)
                self.imgs.append(img)
        return

    def estimate(self, camera_matrix, distort, tag_size):
        april_detector = ad(camera_matrix)
        for img in self.imgs:
            img = cv2.undistort(img, camera_matrix, distort, None)
            tags = april_detector.detect_tags(img, tag_size)
            print(tags)
