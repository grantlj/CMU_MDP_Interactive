import os
from shutil import *
origin_image_folder='D:/Matlab/ImageProcess/MDP_Interactive/MDP_Labeler/92-2_demo_2_null/Images_old/'
dest_image_folder='D:/Matlab/ImageProcess/MDP_Interactive/MDP_Labeler/92-2_demo_2_null/Images/'

'''
if not os.path.exists(dest_image_folder):
    os.mkdir(dest_image_folder)

base_num=85

for i in xrange(0,325+1):
    org_img_name="%s%05d.jpg"%(origin_image_folder,i)
    dest_img_name="%s%05d.jpg"%(dest_image_folder,i+base_num)
    print org_img_name
    copyfile(org_img_name,dest_img_name)
'''

origin_tracklet_filename='D:/Matlab/ImageProcess/MDP_Interactive/MDP_Labeler/92-2_demo_2_null/tracklets_origin.txt'
dst_tracklet_filename='D:/Matlab/ImageProcess/MDP_Interactive/MDP_Labeler/92-2_demo_2_null/tracklets_final.txt'

base_num=85
dst_all_lines=[]
with open(origin_tracklet_filename,"r") as f:
    org_all_lines=f.readlines()

for now_line in org_all_lines:
    tmp_str=now_line.split(",")
    tmp_str[0]=str(int(tmp_str[0])+base_num-1)
    new_str=",".join(tmp_str)
    dst_all_lines.append(new_str)
    pass

with open(dst_tracklet_filename,"w") as f:
    f.writelines(dst_all_lines)
