from dt_apriltags import Detector
import numpy
import os
import cv2
from cv2 import imshow

"""
visualization = True

at_detector = Detector(families='tagStandard41h12',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

print("\n\nTESTING WITH A SAMPLE IMAGE")

img = cv2.imread("undist.jpg", cv2.IMREAD_GRAYSCALE)
cameraMatrix = numpy.array([[806.01,0,640],[0, 806.01,512],[0,0,1]])
camera_params = ( cameraMatrix[0,0], cameraMatrix[1,1], cameraMatrix[0,2], cameraMatrix[1,2] )

if visualization:
    cv2.imshow('Original image',img)

tags = at_detector.detect(img, True, camera_params, 41)
print(tags)

color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

for tag in tags:
    for idx in range(len(tag.corners)):
        cv2.line(color_img, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

    cv2.putText(color_img, str(tag.tag_id),
                org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                color=(0, 0, 255))

if visualization:
    cv2.imshow('Detected tags', color_img)

    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
"""

class AprilDetect(object):

    def __init__(self, camera_matrix, family='tagStandard41h12', workdir='./workdir/'):
        # camera matrix: intrinsic matrix
        self.workdir = workdir
        self.at_detector = Detector(families=family,
                            nthreads=1,
                            quad_decimate=1.0,
                            quad_sigma=0.0,
                            refine_edges=1,
                            decode_sharpening=0.25,
                            debug=0)
        self.camera_params = ( camera_matrix[0,0], camera_matrix[1,1], 
                               camera_matrix[0,2], camera_matrix[1,2] )
        return

    def draw_tags(self, color_img, tags):
        for tag in tags:
            for idx in range(len(tag.corners)):
                cv2.line(color_img, tuple(tag.corners[idx-1, :].astype(int)), 
                                    tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

            cv2.putText(color_img, str(tag.tag_id),
                        org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.8,
                        color=(0, 0, 255))
        return color_img

    def detect_tag(self, img, tag_size, estimate_pose = False, visualization = None):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        tags = self.at_detector.detect(img, estimate_pose, self.camera_params, tag_size)

        if not (visualization is None):
            color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            color_img = self.draw_tags(color_img, tags)
            #cv2.imshow('Detected tags', color_img)
            cv2.imwrite(self.workdir + visualization + '.jpg', color_img)

            #k = cv2.waitKey(0)
            #if k == 27:         # wait for ESC key to exit
            #    cv2.destroyAllWindows()
            return tags, color_img
        else:
            return tags, None

