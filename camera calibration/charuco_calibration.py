#https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html

import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

class CharucoCalibration(object):

    def __init__(self, workdir="./workdir/"):
        board_dim = 0.0365125
        marker_dim = 0.8 * board_dim

        save_board = False
        self.workdir = workdir
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        #self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.board = aruco.CharucoBoard_create(7, 5, board_dim, marker_dim, self.aruco_dict)

        if save_board:
            imboard = self.board.draw((2000, 2000))
            cv2.imwrite(self.workdir + "chessboard.tiff", imboard)

        return

    def _read_chessboards(self, images):
        """
        Charuco base pose estimation.
        """
        print("POSE ESTIMATION STARTS:")
        allCorners = []
        allIds = []
        decimator = 0
        # SUB PIXEL CORNER DETECTION CRITERION
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

        for i, frame in enumerate(images):
            print("=> Processing image {0}".format(i))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.aruco_dict)

            if len(corners)>0:
                # SUB PIXEL DETECTION
                for corner in corners:
                    cv2.cornerSubPix(gray, corner,
                                     winSize = (3,3),
                                     zeroZone = (-1,-1),
                                     criteria = criteria)
                res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,self.board)
                if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                    allCorners.append(res2[1])
                    allIds.append(res2[2])

            decimator+=1

            imsize = gray.shape
        return allCorners,allIds,imsize

    def _calibrate_camera(self, allCorners,allIds,imsize):
        """
        Calibrates the camera using the dected corners.
        """
        print("CAMERA CALIBRATION")

        cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                     [    0., 1000., imsize[1]/2.],
                                     [    0.,    0.,           1.]])

        distCoeffsInit = np.zeros((1,4))
        #flags = (cv2.CALIB_USE_INTRINSIC_GUESS+cv2.CALIB_RATIONAL_MODEL+cv2.CALIB_FIX_ASPECT_RATIO)
        flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_FIX_ASPECT_RATIO)
        (ret, camera_matrix, distortion_coefficients,
         rotation_vectors, translation_vectors,
         stdDeviationsIntrinsics, stdDeviationsExtrinsics,
         perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                          charucoCorners=allCorners,
                          charucoIds=allIds,
                          board=self.board,
                          imageSize=imsize,
                          cameraMatrix=cameraMatrixInit,
                          distCoeffs=distCoeffsInit,
                          flags=flags,
                          criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

        return ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors

    def calibrate(self, fname, is_vid=True, check_calib=False, check_idx=0):
        # fname: either video file name or directory name

        images = []
        if is_vid:
            cap = cv2.VideoCapture(fname)
            read_interval = 50
            idx = 0
            if (cap.isOpened() == False):
                print("video file read error!")
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    if idx % read_interval == 0:
                        images.append(frame)
                    idx += 1
                else:
                    print("Frame grab error!")
                    break
            cap.release()
        else:
            datadir = fname
            image_names = np.array([datadir + f for f in os.listdir(datadir) if f.endswith(".jpg") ])
            order = np.argsort([int(p.split(".")[-2].split("/")[-1]) for p in image_names])
            image_names = image_names[order]
            for im_name in image_names:
                images.append(cv2.imread(im_name))
            
        allCorners,allIds,imsize = self._read_chessboards(images)

        ret, mtx, dist, rvecs, tvecs = self._calibrate_camera(allCorners,allIds,imsize)

        if check_calib:
            if check_idx < len(images):
                plt.figure()
                frame = images[check_idx]
                img_undist = cv2.undistort(frame,mtx,dist,None)
                cv2.imwrite(self.workdir + "distorted.jpg", frame)
                cv2.imwrite(self.workdir + "undistorted.jpg", img_undist)
                plt.subplot(1,2,1)
                plt.imshow(frame)
                plt.title("Raw image")
                plt.axis("off")
                plt.subplot(1,2,2)
                plt.imshow(img_undist)
                plt.title("Corrected image")
                plt.axis("off")
                plt.show()
            else:
                print("Error: index of out of range. Not that many images.")

        return ret, mtx, dist, rvecs, tvecs

    """
    workdir = "./workdir/"
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    board = aruco.CharucoBoard_create(7, 5, 1, .8, aruco_dict)
    imboard = board.draw((2000, 2000))
    cv2.imwrite(workdir + "chessboard.tiff", imboard)
    #fig = plt.figure()
    #ax = fig.add_subplot(1,1,1)
    #plt.imshow(imboard, cmap = mpl.cm.gray, interpolation = "nearest")
    #ax.axis("off")
    #plt.show()

    datadir = "./calib/"
    images = np.array([datadir + f for f in os.listdir(datadir) if f.endswith(".jpg") ])
    order = np.argsort([int(p.split(".")[-2].split("/")[-1]) for p in images])
    images = images[order]

    allCorners,allIds,imsize=read_chessboards(images)

    ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize)

    #print(ret)
    print(mtx)
    print(dist)
    #print(rvecs)
    #print(tvecs)

    frame = cv2.imread("tag1.jpeg")
    img_undist = cv2.undistort(frame,mtx,dist,None)
    cv2.imwrite("undist.jpg", img_undist)

    i=2
    plt.figure()
    frame = cv2.imread(images[i])
    img_undist = cv2.undistort(frame,mtx,dist,None)
    plt.subplot(1,2,1)
    plt.imshow(frame)
    plt.title("Raw image")
    plt.axis("off")
    plt.subplot(1,2,2)
    plt.imshow(img_undist)
    plt.title("Corrected image")
    plt.axis("off")
    plt.show()
    """
