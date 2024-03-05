import os
import cv2
import numpy as np

target_dir = 'n6'

for f in os.listdir(target_dir):
    if os.path.isdir(target_dir + '/' + f) and f.startswith('output_'):
        print(f)
        avg_created = False
        for f2 in os.listdir(target_dir + '/' + f):
            if f2.endswith('.avi'):
                cap = cv2.VideoCapture(target_dir + '/' + f + '/' + f2)
                while(cap.isOpened()):
                    ret, frame = cap.read()
                    if ret == True:
                        frame = np.float32(frame)
                        if not avg_created:
                            avg_img = frame
                            avg_count = 1
                            avg_created = True
                        else:
                            avg_count += 1
                            avg_img += (frame - avg_img) / avg_count
                    else:
                        break
                cap.release()
        if avg_created:
            avg_img = np.uint8(np.round(avg_img))
            cv2.imwrite(target_dir + '/' + f + '/avg_img.jpg', avg_img)
