clear *;

lists = ["n1/stitched_videos_mp4", 
         "n2/stitched_videos_mp4", 
         "n3/stitched_videos_mp4"];

for i=1:3
    directory = lists(i);
    files = dir(directory);
    num_files = length(files);
    for j=1:num_files
        file = files(j);
        fname = file.name;
        if endsWith(fname, "_traj2.avi")
            fname_pre = strsplit(fname, "_");
            fname_pre = fname_pre{1};
            old_name = directory + "/" + fname;
            new_name = directory + "/" + fname_pre + "_traj.avi";
            movefile(old_name, new_name);
        end
    end
end