########################################################################
#
# Copyright (c) 2017, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.sl as sl
import math
import numpy as np
import sys
import socket
import time

HOST = ''
PORT = 2111
PORT2 = 2112

def main():

    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    #init_params.camera_buffer_count_linux = 2
    init_params.camera_fps = 30
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use milliliter units (for depth measurements)

    print('Camera resolution', init_params.camera_resolution)
    print('Camera frame rate', init_params.camera_fps)
    print('Camera depth mode', init_params.depth_mode)

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.sensing_mode = sl.SENSING_MODE.STANDARD  # Use STANDARD sensing mode

    # Capture 50 images and depth, then stop
    i = 0
    image_l = sl.Mat()
    image_r = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()
    max_record_frames = 1000

    while not(zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS):
        continue
    zed.retrieve_image(image_l, sl.VIEW.LEFT)
    frame_width = int(image_l.get_width())
    frame_height = int(image_l.get_height())
    start_time = str(int(time.time()))

    path_output = start_time + "_data3d.svo"
    record_parameters = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.LOSSLESS)
    err = zed.enable_recording(record_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit(1)

    path_time = start_time + "time.txt"
    file_time = open(path_time, "w")

    # Code that wait for signal from server
    """
    ###########################################################
    ###########################################################
    print('Machine ready')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT2))
    s.listen(1)
    conn, addr = s.accept()
    conn.settimeout(1e-6)
    print('Waiting for signal ...')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn2, addr = s.accept()
    print('Connected to: ', addr)
    while True:
        data = conn2.recv(1024)
        if not data: break

    print('Machine start working!')

    ###########################################################
    ###########################################################
    """

    while i < max_record_frames:
        # A new image is available if grab() returns SUCCESS
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            """
            # Retrieve left image
            zed.retrieve_image(image_l, sl.VIEW.VIEW_LEFT)
            zed.retrieve_image(image_r, sl.VIEW.VIEW_RIGHT)
            # Retrieve depth map. Depth is aligned on the left image
            zed.retrieve_measure(depth, sl.MEASURE.MEASURE_DEPTH)
            # Retrieve colored point cloud. Point cloud is aligned on the left image.
            zed.retrieve_measure(point_cloud, sl.MEASURE.MEASURE_XYZRGBA)
            """

            #state = zed.record()
            #if not state["status"]:
            #    continue
            time_raw = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)
            time_raw = time_raw.data_ns // 1000
            print("Time when image is taken: {0}\n".format(time_raw))
            time_str = "{0}, {1}\n".format(i, time_raw)
            file_time.write(time_str)
            i += 1
            """
            # Get and print distance value in mm at the center of the image
            # We measure the distance camera - object using Euclidean distance
            x = round(image_l.get_width() / 2)
            y = round(image_l.get_height() / 2)
            err, point_cloud_value = point_cloud.get_value(x, y)

            distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                 point_cloud_value[1] * point_cloud_value[1] +
                                 point_cloud_value[2] * point_cloud_value[2])
            time = zed.get_timestamp(sl.TIME_REFERENCE.TIME_REFERENCE_IMAGE)

            if not np.isnan(distance) and not np.isinf(distance):
                distance = round(distance)
                print("Distance to Camera at ({0}, {1}): {2} mm\n".format(x, y, distance))
                print("Time when image is taken: {0}\n".format(time))
                # Increment the loop
                i = i + 1
            else:
                print("Can't estimate distance at this position, move the camera\n")
            sys.stdout.flush()
            """
            # check if stop signal received
            """
            ###########################################################
            ###########################################################
            try:
                data = conn.recv(1024)
                break
            except socket.timeout as e:
                continue
            ###########################################################
            ###########################################################
            """

    # Close the camera
    zed.disable_recording()
    zed.close()
    file_time.close()

if __name__ == "__main__":
    main()
