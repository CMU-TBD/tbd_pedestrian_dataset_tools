import numpy as np
import cv2

direc = "n3/output_1580759284111901/"
input_fname = direc + "video_segments/0.mp4"
bg_img_fname = direc + "avg_img.jpg"

cap = cv2.VideoCapture(input_fname)
width = int(cap.get(3))
height = int(cap.get(4))

debug_vid_fname = "processed_vid.mp4"
vid_writer = cv2.VideoWriter(debug_vid_fname, cv2.VideoWriter_fourcc(*'mp4v'),
                             60.0, (width, height))

avg_img = cv2.imread(bg_img_fname)

cnt = 0
num_frames = int(cap.get(7))
while (cap.isOpened()):
    cnt += 1
    print([cnt, num_frames], end = "\r")
    ret, frame = cap.read()
    if ret == True:
        mask = np.mean(abs(frame - avg_img), axis=2)
        mask = np.uint8(np.repeat(np.expand_dims(mask, 2), 3, axis=2))
        frame = mask # * frame
        vid_writer.write(frame)
    else:
        break

vid_writer.release()
cap.release()

