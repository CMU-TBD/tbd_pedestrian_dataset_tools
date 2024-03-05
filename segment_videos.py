import os
import cv2
import numpy as np

meta_vid_idx = 7
frames_file_name = 'segment_frames_id.txt'
offsets_file_name = 'segment_offsets.txt'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

start_frames = []
end_frames = []
f = open(frames_file_name, "r")
for line in f:
    line = line.rstrip()
    numbers = line.split(' - ')
    start_frames.append(int(numbers[0]))
    end_frames.append(int(numbers[1]))
num_video = len(start_frames)
f.close()

offsets = []
f = open(offsets_file_name, "r")
for line in f:
    line = line.rstrip()
    offsets.append(int(line))
f.close()
standard = offsets[2]
for i in range(len(offsets)):
    offsets[i] -= standard

dirlist = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6']
for n, node in enumerate(dirlist):
    print(node)

    id_list = []
    dir_list = []
    for cam in os.listdir(node):
        if cam.startswith('output_'):
            tmp = cam.split('_')
            id_list.append(int(tmp[1]))
            dir_list.append(cam)
    order = np.argsort(id_list)

    dirname_list = []
    for idx in order:
       dirname_list.append(node + '/' + dir_list[idx])
    dirname = dirname_list[meta_vid_idx]
    vid_filename = dirname + '/stitched_video.mp4'
    
    if 'video_segments' not in os.listdir(dirname):
        os.mkdir(dirname + '/video_segments')

    dirname = dirname + '/video_segments'
    cap = cv2.VideoCapture(vid_filename)
    offset = offsets[n]
    for i in range(num_video):
        st_frame = start_frames[i] + offset
        ed_frame = end_frames[i] + offset

        count = st_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, st_frame)
        vid_writer = cv2.VideoWriter(dirname + '/' + str(i) + '.mp4', fourcc, 60, (1280, 1024))
        while (count <= ed_frame):
            ret, frame = cap.read()
            if ret == False:
                raise Exception('Video frame read error!')
            vid_writer.write(frame)
            count += 1
        vid_writer.release()

    cap.release()
