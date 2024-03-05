import argparse
from scipy.io import savemat

from charuco_calibration import CharucoCalibration
from april_detect import AprilDetect

parser = argparse.ArgumentParser()
parser.add_argument('--path', help='path to calibration video file')
parser.add_argument('--save_path', help='path to save intrinsics parameters')
parser.add_argument('--vis', 
                    type=bool,
                    default=False, 
                    help='true if want to see rectified image')
args = parser.parse_args()

calib_vid = args.path
vis = args.vis
save_path = args.save_path

charuco = CharucoCalibration()

ret, mtx, dist, rvecs, tvecs = charuco.calibrate(calib_vid, check_calib=vis)

print("Intrinsics")
print(mtx)
print(dist)

mdic = {"K": mtx, "dist_coeff": dist[0][:3]}
savemat(save_path, mdic)
