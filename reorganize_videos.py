import shutil
import os

meta_dirs = ["n1", "n2", "n3", "n4" ,"n5", "n6"]
output_segments = "video_segments"
output_complete = "complete_videos"
for meta_dir in meta_dirs:
    dir_entries = sorted(os.listdir(meta_dir))
    dir_limit = 8
    dir_entries = dir_entries[0:dir_limit]
    for i, dir_entry in enumerate(dir_entries):
        print("====================")
        print([meta_dir, i])
        print("====================")
        folder_path = os.path.join(meta_dir, dir_entry)
        vid_entries = sorted(os.listdir(os.path.join(folder_path, "video_segments")))
        num_vids = len(vid_entries)
        for j, vid_entry in enumerate(vid_entries):
            print([j, num_vids])
            if vid_entry.endswith(".mp4"):
                vid_path = os.path.join(folder_path, "video_segments", vid_entry)
                shutil.copy(
                    vid_path, 
                    os.path.join(output_segments, f"{meta_dir}_{i}_{vid_entry}")
                )
        shutil.copy(
            os.path.join(folder_path, "stitched_video.mp4"),
            os.path.join(output_complete, f"{meta_dir}_{i}_video.mp4")
        )
         
