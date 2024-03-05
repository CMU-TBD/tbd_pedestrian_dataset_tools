import cv2
import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat

import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

score_thresh = 0.4

def overlay_pred(outputs, frame, visualize):
    instances = outputs['instances'].to('cpu')
    pred_boxes = instances.pred_boxes.tensor.numpy()
    scores = instances.scores.numpy()
    pred_classes = instances.pred_classes.numpy()
    num_instances = len(scores)

    proc_centers = []
    for i in range(num_instances):
        if (scores[i] >= score_thresh) and (pred_classes[i] == 0):
            pbox = pred_boxes[i]
            x = int((pbox[0] + pbox[2]) / 2)
            y = int((pbox[1] + pbox[3]) / 2)
            proc_centers.append([x, y])
            if visualize:
                cv2.circle(frame, (x, y), 5, (255, 0, 0), 3)
        
    return frame, proc_centers

def run_predictor(fname, predictor, visualize=False):
    output_sequence = []

    cap = cv2.VideoCapture(fname)
    width = int(cap.get(3))
    height = int(cap.get(4))

    if visualize:
        debug_vid_fname = "debug.mp4"
        vid_writer = cv2.VideoWriter(debug_vid_fname, cv2.VideoWriter_fourcc(*'mp4v'), 
                                     60.0, (width, height))

    cnt = 0
    num_frames = int(cap.get(7))
    while (cap.isOpened()):
        cnt += 1
        print([cnt, num_frames], end = "\r")
        ret, frame = cap.read()
        if ret == True:
            outputs = predictor(frame)
            proc_frame, proc_outputs = overlay_pred(outputs, frame, visualize)
            output_sequence.append(proc_outputs)
            if visualize:
                vid_writer.write(proc_frame)
        else:
            break

    if visualize:
        vid_writer.release()
    cap.release()

    return output_sequence

if __name__ == "__main__":

    visualize = False

    cfg = get_cfg()
    # add project-specific config (e.g., TensorMask) here 
    # if you're not running a model in detectron2's core library
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-Detection/retinanet_R_101_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = score_thresh  # set threshold for this model
    # Find a model from detectron2's model zoo. 
    # You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_101_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)

    fname = "n3/output_1581357733994012/video_segments/37.mp4"
    pred_seq = run_predictor(fname, predictor, visualize=True)
    exit()

    lft_dir_entries = sorted(os.listdir("n1"))
    rgt_dir_entries = sorted(os.listdir("n2"))
    ctr_dir_entries = sorted(os.listdir("n3"))
    num_entries = len(lft_dir_entries)
    for i in range(num_entries):
        print(i)
        vid_entries = sorted(os.listdir("n1/" + lft_dir_entries[i] + "/video_segments"))
        #vid_entries = ["stitched_video.mp4"]
        num_vids = len(vid_entries)
        for j in range(num_vids):
            print([j, num_vids - 1])
            vid_num = vid_entries[j].split('.')[0]

            lft_fname = "n1/" + lft_dir_entries[i] + "/video_segments/" + vid_entries[j]
            rgt_fname = "n2/" + rgt_dir_entries[i] + "/video_segments/" + vid_entries[j]
            ctr_fname = "n3/" + ctr_dir_entries[i] + "/video_segments/" + vid_entries[j]
            #lft_fname = "n1/" + lft_dir_entries[i] + "/" + vid_entries[j]
            #rgt_fname = "n2/" + rgt_dir_entries[i] + "/" + vid_entries[j]
            #ctr_fname = "n3/" + ctr_dir_entries[i] + "/" + vid_entries[j]

            lft_pred_seq = run_predictor(lft_fname, predictor, visualize)
            rgt_pred_seq = run_predictor(rgt_fname, predictor, visualize)
            ctr_pred_seq = run_predictor(ctr_fname, predictor, visualize)
            save_dict = {"left_ped_pts": lft_pred_seq,
                         "right_ped_pts": rgt_pred_seq,
                         "center_ped_pts": ctr_pred_seq}
            savemat("ped_predictions/" + str(i) + "_" + vid_num + ".mat", save_dict)
            #savemat("pedstitch_predictions/" + str(i) + "_" + vid_num + ".mat", save_dict)

