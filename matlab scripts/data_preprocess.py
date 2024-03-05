import cv2 as cv
import os
import numpy as np

def shrink_break_videos(in_name, shrink_step, target_fps, time_limit, offset):
    cap = cv.VideoCapture(in_name)
    offset_count = 0
    while cap.isOpened() and (offset_count < offset):
        ret, frame = cap.read()
        offset_count += 1

    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    assert((fps / shrink_step) == target_fps)

    name_list = in_name.split(".")
    og_name = name_list[0]
    name_count = 0
    resolution = (1280, 1024)
    fourcc = cv.VideoWriter_fourcc(*'XVID')

    count = 0
    s_count = time_limit
    while cap.isOpened() and (count < (length - offset)):
        if s_count == time_limit:
            if count > 0:
                out.release()
            out_name = og_name + "_" + str(name_count) + ".avi"
            out = cv.VideoWriter(out_name, fourcc, target_fps, resolution)
            name_count += 1
            s_count = 0

        ret, frame = cap.read()
        count += 1
        if (count % shrink_step) == 0:
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            out.write(frame)
            s_count += 1
            print("Writing {} / {} \r".format(count, length), end = "")

    out.release()
    cap.release()
    return

def shrink_txt(in_name, shrink_step, offset):
    f_read = open(in_name, "r")
    name_list = in_name.split(".")
    og_name = name_list[0]
    out_name = og_name + "_s.txt"
    f_write = open(out_name, "w")

    for line in f_read:
        data_list = line.split(",")
        f_idx = int(data_list[0])
        if f_idx < offset:
            continue
        else:
            f_idx -= offset
        if (f_idx % shrink_step) == 0:
            f_new_idx = int(f_idx / shrink_step)
            new_line = str(f_new_idx) + "," + ",".join(data_list[1:])
            f_write.write(new_line)

    f_read.close()
    f_write.close()
    return

if __name__ == "__main__":
    target_fps = 10
    time_limit = 10 * 60 * target_fps

    num_vids = 33
    base_dir_l = "n1"
    base_dir_r = "n2"
    base_dir_c = "n3"
    base_dirs = [base_dir_l, base_dir_r, base_dir_c]

    fsync = open("sync.txt", "r")
    #fsync = open("sync_tmp.txt", "r")
    for i in range(num_vids):
    #for i in [17, 18, 19, 20]:
        for j in range(3):
            line = fsync.readline()
            char_list = line.split(",")
            assert((i+1) == int(char_list[0]))
            assert((j+1) == int(char_list[1]))

            lb_directory = os.path.join(base_dirs[j], "track_results")
            lb_file = os.path.join(lb_directory, str(i+1) + ".txt")

            offset = int(char_list[2])
            print("Processing {} ...".format(lb_file))
            shrink_txt(lb_file, 6, offset)

            directory = os.path.join(base_dirs[j], "stitched_videos_mp4")
            vid_name = os.path.join(directory, str(i+1) + ".mp4")
            traj_vid_name = os.path.join(directory, str(i+1) + "_traj.avi")
            print("Processing {} ...".format(vid_name))
            shrink_break_videos(vid_name, 6, target_fps, time_limit, offset)
            print("Processing {} ...".format(traj_vid_name))
            shrink_break_videos(traj_vid_name, 3, target_fps, time_limit, int(offset / 2))


    fsync.close()
