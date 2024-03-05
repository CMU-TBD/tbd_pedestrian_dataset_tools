import os
import cv2
import numpy as np
import datetime
import argparse

parser = argparse.ArgumentParser(description='File path to the raw video files needed')

parser.add_argument('-i', '--input', dest='target_dir', required=True,
                    help='Input file path')
parser.add_argument('-f', '--filter', dest='start_char', default='output_',
                    help='Sub folder filter')
parser.add_argument('-o', '--output', dest='dest_dir', default='data_batch2',
                    help='Output directory')
parser.add_argument('-c', '--isavi', dest='isavi', default=False, action='store_true',
                    help='detemines saving format')

args = parser.parse_args()


target_dir = args.target_dir
start_char = args.start_char
dest_dir = args.dest_dir
isavi = args.isavi

if os.path.isdir(target_dir) and os.path.basename(target_dir).startswith(start_char):
    # collect the sub videos information
    vid_names = []
    for f in os.listdir(target_dir):
        if f.endswith('0.avi'):
            vid_names.append(os.path.join(target_dir, f))
    vid_frame_number = []
    for nm in vid_names:
        tmp_str = nm.split('-')
        vid_frame_number.append(int(tmp_str[-1][:-4]))
    vid_frame_number = np.array(vid_frame_number)
    index_array = np.argsort(vid_frame_number)

    # concatenate the sub videos into a temporary video
    print("concatenating videos ...")
    if isavi:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        ext = ".avi"
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        ext = ".mp4"
    tmp_path = os.path.normpath(target_dir) # get rid of trailing "/"
    tmp_str = tmp_path.split('_')
    timestamp = float(tmp_str[-1]) / 1000000
    timename = datetime.datetime.fromtimestamp(timestamp).isoformat()
    temp_fname = timename + ext
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    save_path = os.path.join(dest_dir, temp_fname)
    vid_writer = cv2.VideoWriter(save_path, fourcc, 60, (1280, 1024))
    for i in index_array:
        nm = vid_names[i]
        cap = cv2.VideoCapture(nm)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                img_1 = frame[:, :, 0]
                img_2 = frame[:, :, 1]
                img_3 = frame[:, :, 2]
                rst_img = np.array([img_3, img_2, img_1])
                rst_frame = np.transpose(rst_img, (1, 2, 0))
                vid_writer.write(rst_frame)
            else:
                break
        cap.release()
    vid_writer.release()
