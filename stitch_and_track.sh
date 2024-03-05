#!/bin/bash

IN_PATH=$1
OUT_PATH=$2

for file in ${IN_PATH}/*
do
    echo ${file}
    FNAME="$(basename "${file}")"
    python stitch_videos.py -i ${file} -o ${OUT_PATH}/stitched_videos --isavi
    python stitch_videos.py -i ${file} -o ${OUT_PATH}/stitched_videos_mp4
done

gpu_idx=$3

for file in ${OUT_PATH}/stitched_videos/*
do
    echo ${file}
    cd ByteTrack
    python3 tools/inference.py -f exps/example/mot/yolox_x_mix_det.py -c pretrained/bytetrack_x_mot17.pth.tar --fp16 --fuse --save_result --fps 60 --gpu_num ${gpu_idx} --path ../${file} --output_path ../${OUT_PATH}/track_results
    cd ..
done
