clear all;
clc;

videoFileReader=vision.VideoFileReader('D:\Matlab\ImageProcess\MDP_Interactive\MDP_Labeler\92-2_demo_2_null\92_2_demo_2_null_tracking_vis_20170109160659.mp4');
dest_folder='D:\Matlab\ImageProcess\MDP_Interactive\MDP_Labeler\92-2_demo_2_null\Images_with_box\';
videoInfo    = info(videoFileReader);

count=0;
base_num=85
while ~isDone(videoFileReader)
    videoFrame=step(videoFileReader);
    count=count+1;
    dest_im_filename=[dest_folder,num2str(count+base_num-1),'.jpg'];
    imwrite(videoFrame,dest_im_filename);
end

count