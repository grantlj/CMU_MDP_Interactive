'''
====================================================================
========== The utility function for MDP Labeler=====================
====================================================================
'''

import sys
import random
import os
import time
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
from scipy import interpolate
import cv2
import mdp_interactive_train
import mdp_interactive_test
from shutil import copyfile
import json

det_file_surfix="det.txt"
img_path_surfix="Images"
model_path_surfix="model"
output_path_surfix="output"
tmp_path_surfix="tmp"

class BBX:
    def __init__(self, fr, x, y, w, h, score):
        self.fr = fr;
        self.x = round(x,1);
        self.y = round(y,1);
        self.w = round(w,1);
        self.h = round(h,1);
        self.score = round(score,3)

#the dataset class
class class_dataset:
    def __init__(self,dataset_path,img_count):
        self.dataset_root_path=dataset_path
        self.img_count=img_count
        self.img_list_path = os.path.join(self.dataset_root_path, img_path_surfix)
        self.model_path = os.path.join(self.dataset_root_path, model_path_surfix)
        self.output_path = os.path.join(self.dataset_root_path, output_path_surfix)

        self.train_iteration=0
        self.im_p=0
        self.now_im_filename=""

        #establish a temporary path to store tmp file
        self.dataset_tmp_root_path=os.path.join(self.dataset_root_path, tmp_path_surfix)
        if not os.path.exists(self.dataset_tmp_root_path):
            os.mkdir(self.dataset_tmp_root_path)

    #linear interpolation of the bounding box
    def do_interpolation(self,target_id,st_fr=None,end_fr=None):
        self.changed_person_id.add(target_id)
        tracklet=self.tracklet_dict[target_id]

        if st_fr is not None:
            print "st_fr is not none...."

        box_count=len(tracklet)
        #find mean fr,x,y,w,h for normalization
        m_fr=int(sum(x.fr for x in tracklet)/box_count);m_x=sum(x.x for x in tracklet)/box_count;m_y=sum(x.y for x in tracklet)/box_count;
        m_h=sum(x.h for x in tracklet)/box_count;m_w=sum(x.w for x in tracklet)/box_count;

        #construct interpolation function for x,y,w,h, respectively
        fr_list=[];x_list=[];y_list=[];w_list=[];h_list=[]
        #list to interpolate
        new_fr_list=[]
        for now_box in tracklet:
           fr_list.append(int(now_box.fr-m_fr));x_list.append(now_box.x-m_x);y_list.append(now_box.y-m_y);
           w_list.append(now_box.w-m_w);h_list.append(now_box.h-m_h)
        f_x=interpolate.interp1d(fr_list,x_list,'slinear');f_y=interpolate.interp1d(fr_list,y_list,'slinear');f_w=interpolate.interp1d(fr_list,w_list,'slinear');f_h=interpolate.interp1d(fr_list,h_list,'slinear')
        for i in xrange(len(fr_list)-1):
            for j in xrange(fr_list[i]+1,fr_list[i+1]):
                if st_fr is  None:
                    new_fr_list.append(j)
                elif (j>st_fr-m_fr) and (j<end_fr-m_fr):
                    new_fr_list.append(j)

        #obtain interpolation result
        new_x_list=f_x(new_fr_list);new_y_list=f_y(new_fr_list);new_w_list=f_w(new_fr_list);new_h_list=f_h(new_fr_list)

        for i in xrange(len(new_fr_list)):

            tracklet.append(BBX(new_fr_list[i]+m_fr,new_x_list[i]+m_x,new_y_list[i]+m_y,new_w_list[i]+m_w,new_h_list[i]+m_h,1.000))
        tracklet.sort(key=lambda x: x.fr)
        self.tracklet_dict[target_id]=tracklet

    #load detection file from list
    def load_detection_results(self,output_file_list_filename):
        print "Load detection results from: ", output_file_list_filename

        with open(output_file_list_filename,"r") as f:
            all_lines=f.readlines()

        tracklet_dict=dict()
        color_dict=dict();color_set=set()

        # Maintain a list of person id, which the tracklets have been manually edited by end user.
        # In this case, these tracklets are treated as the positive samples for the MDP tracking system to update
        self.changed_person_id = set()

        for now_line in all_lines:
            tmp_str=now_line.split(",")
            now_fr=int(tmp_str[0]);now_id=int(tmp_str[1]);now_x=float(tmp_str[2]);now_y=float(tmp_str[3]);now_w=float(tmp_str[4]);now_h=float(tmp_str[5]);now_score=float(tmp_str[6])
            now_bbx=BBX(now_fr,now_x,now_y,now_w,now_h,now_score)

            #add box to tracklet dict
            if not now_id in tracklet_dict:
                tracklet_dict[now_id]=[now_bbx]
                #generate a new color
                now_color,now_color_str=generate_a_unique_color(color_set);color_dict[now_id]=now_color;color_set.add(now_color_str)

            else:
                tracklet_dict[now_id].append(now_bbx)

            tracklet_dict[now_id].sort(key=lambda x: x.fr)

        self.tracklet_dict=tracklet_dict
        self.color_dict=color_dict;self.color_set=color_set

        print "Finished.."

    #user adds a new object to the dict
    def add_new_object_from_widget_paint(self,widget_paint,img_map):
        try:
            new_object_id=max(self.tracklet_dict.keys())+1
        except:
            new_object_id=1
            print "add new object error handled..."

        tmp_box=BBX(self.im_p,widget_paint.mouse_st.x(),widget_paint.mouse_st.y(),widget_paint.mouse_end.x()-widget_paint.mouse_st.x(),widget_paint.mouse_end.y()-widget_paint.mouse_st.y(),1.000)
        new_box=convert_view_cood_to_img(tmp_box,img_map,widget_paint)
        self.tracklet_dict[new_object_id]=[new_box]
        now_color,now_color_str=generate_a_unique_color(self.color_set);self.color_dict[new_object_id]=now_color;self.color_set.add(now_color_str)

        self.changed_person_id.add(new_object_id)

    #user add the bounding box to existing object tracklet
    def add_to_existing_object_from_widget_paint(self,object_id,widget_paint,img_map):
        now_object_tracklet=self.tracklet_dict[object_id]

        tmp_box = BBX(self.im_p, widget_paint.mouse_st.x(), widget_paint.mouse_st.y(),
                      widget_paint.mouse_end.x() - widget_paint.mouse_st.x(),
                      widget_paint.mouse_end.y() - widget_paint.mouse_st.y(), 1.000)
        new_box = convert_view_cood_to_img(tmp_box, img_map, widget_paint)

        existed_flag=False
        for (now_box_id,now_box) in enumerate(now_object_tracklet):
            if now_box.fr==self.im_p:
                #edit an existing bounding box
                now_box=new_box
                now_object_tracklet[now_box_id]=now_box
                existed_flag=True
                break

        #the bounding box is not existed
        if not existed_flag:
            now_object_tracklet.append(new_box)
        print "Add new bounding box done."
        now_object_tracklet.sort(key=lambda x: x.fr)

        self.changed_person_id.add(object_id)

    #user edit bounding box from widget_dets
    def update_tracklet_from_widget_det(self,object_id,widget_box_item):
        print "udpdate tracklet by editing widget detection..."
        now_object_tracklet=self.tracklet_dict[object_id]

        fr = int(widget_box_item.text(0))
        x = float(widget_box_item.text(2));y = float(widget_box_item.text(3));w = float(widget_box_item.text(4));h = float(widget_box_item.text(5))
        score = float(widget_box_item.text(6))

        new_box=BBX(fr,x,y,w,h,score)
        existed_flag = False
        for (now_box_id, now_box) in enumerate(now_object_tracklet):
            if now_box.fr == fr:
                # edit an existing bounding box
                now_object_tracklet[now_box_id] = new_box
                existed_flag = True
                break
                # the bounding box is not existed
        if not existed_flag:
            now_object_tracklet.append(new_box)
        now_object_tracklet.sort(key=lambda x:x.fr)

        self.changed_person_id.add(object_id)

    #get the start frame of a target
    def get_target_start_end_frame(self,target_id):
        tracklet=self.tracklet_dict[target_id]
        return tracklet[0].fr,tracklet[-1].fr

    #replace existing tracklet with a new one
    def replace_existing_tracklet_with_new(self,object_id,merged_box_list):
        self.tracklet_dict[object_id]=merged_box_list
        self.changed_person_id.add(object_id)
        return object_id

    #set image position
    def set_im_position(self,fr_pos):
        self.im_p=fr_pos
        self.now_im_filename="%s/%05d.jpg"%(self.img_list_path,fr_pos)

    #get the reverse of changed person id set
    def get_reverse_of_changed_person_id(self,changed_person_id_set):
        ret_set=set()
        for (tracker_id,_) in self.tracklet_dict.items():
            if not tracker_id in changed_person_id_set:
                ret_set.add(tracker_id)

        return ret_set

    #merge the dataset instance result with a tracking result outputed by a MDP tracking test
    def merge_with_tmp_tracking_output(self,tmp_tracking_output_filename):

        #first we dump all the previously annotated bounding boxes
        tmp_merge_output_filename=os.path.join(self.dataset_tmp_root_path, "tmp_merge.txt")
        self.dump_annotation_result(tmp_merge_output_filename,2)

        max_id=max([x for x in self.tracklet_dict.keys() if x not in self.changed_person_id])

        with open(tmp_tracking_output_filename,"r") as f:
            tmp_all_lines=f.readlines()

        with open(tmp_merge_output_filename, "a") as f:
            for now_line in tmp_all_lines:
                tmp_str = now_line.split(",");now_fr = int(tmp_str[0]);now_id = int(tmp_str[1]);now_x = float(tmp_str[2]);now_y = float(tmp_str[3]);now_w = float(tmp_str[4]);now_h = float(tmp_str[5]);
                now_score = float(tmp_str[6])
                now_id=now_id+max_id
                now_line = "%d,%d,%f,%f,%f,%f,%f,-1.000,-1.000,-1.000\n" % (
                now_fr, now_id, now_x, now_y, now_w, now_h, now_score)
                f.write(now_line)

        os.remove(tmp_tracking_output_filename)
        copyfile(tmp_merge_output_filename,tmp_tracking_output_filename)
        os.remove(tmp_merge_output_filename)

    #save present annotation result to file
    def dump_annotation_result(self,filename,dump_mode=0):
        #dump mode:
        # mode = 0: the default mode to dump, dump all tracking results
        # mode = 1: in training mode, dump only the annotated person in the dictionary, so that the MDP trainer can update a tracker
        # mode = 2: in testing mode, dump only the UN-annotated person in the dictionary, as the detections to the MDP tester

        print "save result to: "+filename+" with mode: "+str(dump_mode)
        all_lines=[]

        if dump_mode==1:
            tmp_exempt_id_set=self.changed_person_id
        elif dump_mode==2:
            tmp_exempt_id_set=self.get_reverse_of_changed_person_id(self.changed_person_id)

        for (track_id, tracklet) in self.tracklet_dict.items():
            #if update_tracker_mode==True:
            #    if not track_id in self.changed_person_id:
            #        continue

            if (dump_mode!=0) and (not track_id in tmp_exempt_id_set):
                continue

            for now_box in tracklet:
                now_line="%d,%d,%f,%f,%f,%f,%f,-1.000,-1.000,-1.000\n"%(now_box.fr,track_id,now_box.x,now_box.y,now_box.w,now_box.h,now_box.score)
                all_lines.append(now_line)
        with open(filename,"w") as f:
            f.writelines(all_lines)

    #dump the color of the annotation result
    def dump_annotation_color(self,filename):
        print "dump the color of the annotation results:",filename
        tmp_color_dict=dict()

        for (tracklet_id,tracklet_color) in self.color_dict.items():
            tmp_color_dict[tracklet_id]=str(tracklet_color.red())+","+str(tracklet_color.green())+","+str(tracklet_color.blue())

        json_str=json.dumps(tmp_color_dict)
        with open(filename,"w") as f:
            f.writelines(json_str)

    #delete a particular object
    def delete_an_object(self,object_id):
        print "delete an object"
        del self.tracklet_dict[object_id]
        if object_id in self.changed_person_id:
            self.changed_person_id.remove(object_id)

    #delete a particular bounding box
    def delete_a_box(self,object_id,fr):
        now_tracklet=self.tracklet_dict[object_id]
        self.changed_person_id.add(object_id)

        index = next((i for i, now_box in enumerate(now_tracklet) if now_box.fr == fr), -1)
        if (index==1):
            print "trying to delete an invalid box..."
            return

        now_tracklet.pop(index)
        now_tracklet.sort(key=lambda x: x.fr)

        if len(now_tracklet)!=0:
            self.tracklet_dict[object_id]=now_tracklet
        else:
            del self.tracklet_dict[object_id]
            self.changed_person_id.remove(object_id)

    #split a particular tracklet from a frame
    def split_a_tracklet(self,object_id,fr):
        now_tracklet=self.tracklet_dict[object_id]

        self.changed_person_id.add(object_id)

        try:
            new_object_id = max(self.tracklet_dict.keys()) + 1
        except:
            new_object_id = 1
            print "add new object error handled..."

        self.changed_person_id.add(new_object_id)

        index = next((i for i, now_box in enumerate(now_tracklet) if now_box.fr == fr), -1)
        if (index == 1):
            print "trying to split from an invalid box..."
            return 0
        new_tracklet=now_tracklet[index:]
        now_tracklet=now_tracklet[0:index]

        self.tracklet_dict[new_object_id]=new_tracklet;self.tracklet_dict[object_id]=now_tracklet
        new_color, new_color_str = generate_a_unique_color(self.color_set); self.color_dict[new_object_id] = new_color;self.color_set.add(new_color_str)
        return new_object_id

    #find bounding box via target_id and frame
    def find_bounding_box_by_id_and_frame(self,object_id,fr):
        ret_box=None
        now_tracklet=self.tracklet_dict[object_id]
        index= next((i for i, now_box in enumerate(now_tracklet) if now_box.fr == fr), -1)
        if index!=-1:
            ret_box=now_tracklet[index]
        return ret_box

    #obtain the cropped image region as pixmap
    def get_crop_img_region(self,fr,now_box):
        print "getting cropped image region..."
        rect=QRect(now_box.x,now_box.y,now_box.w,now_box.h)
        original_im=QPixmap("%s/%05d.jpg"%(self.img_list_path,fr))
        return original_im.copy(rect)

    #dump the tracking result to avi video
    def dump_tracking_video(self,vid_filename,exo_object_set):
        print vid_filename
        im_list=[]
        painter=QPainter(); pen = QPen();font = QFont();font.setPixelSize(17)

        for now_fr in xrange(1,self.img_count):
            print "Loading image frame:",now_fr
            now_im_filename="%s/%05d.jpg"%(self.img_list_path,now_fr)
            now_im=QImage(now_im_filename)
            im_list.append(now_im)

        for (track_id,tracklet) in self.tracklet_dict.items():
            print "Handling track id:",track_id
            if (track_id in exo_object_set):
                continue
            for now_bbx in tracklet:
                try:
                    now_im=im_list[now_bbx.fr-1]
                except:
                    continue
                painter.begin(now_im)
                pen.setBrush(self.color_dict[track_id]);pen.setWidth(4);painter.setPen(pen);painter.setFont(font)
                painter.drawText(QRect(now_bbx.x,now_bbx.y,now_bbx.w,now_bbx.h).topLeft(),str(track_id))
                painter.drawRect(round(now_bbx.x), round(now_bbx.y), round(now_bbx.w), round(now_bbx.h))
                painter.end()
                im_list[now_bbx.fr-1]=now_im


        #transfer to
        fourcc = cv2.VideoWriter_fourcc(*'XVID');fps=7.00
        writer = cv2.VideoWriter(str(vid_filename), fourcc, fps, (now_im.width(),now_im.height()))
        for now_fr in xrange(1,self.img_count):
            print "writing frame,",now_fr
            writer.write(convert_qimage_to_mat(im_list[now_fr-1]))
        writer.release()

        print "Finished.........write to video file..."
        pass

        #for now_fr in xrange(1,self.img_count):

        #frame=cv2.Mat(now_im.height(),now_im.width(),cv2.CV_8UC3,now_im.bits(),now_im.bytesPerLine()).clone()
        #frame=convert_qimage_to_mat(now_im)
        #cv2.namedWindow("Test")
        #cv2.imshow("Test",frame)

#generate a new unique color
def generate_a_unique_color(color_set):
    while True:
        r=random.randint(0,255);g=random.randint(0,255);b=random.randint(0,255)
        darkness=(r*299 + g*587 + b*114 + 500) / 1000
        if (darkness<70):
            continue
        tmp_str="%03d%03d%03d" % (r,g,b)

        if not tmp_str in color_set:
            break
    return QColor(r,g,b),tmp_str

#get dataset image count, differentiate whether a valid path (with Images and det.txt")
def get_dataset_img_count(dataset_root_path):
    print dataset_root_path

    img_list_path=os.path.join(dataset_root_path,img_path_surfix)
    if not os.path.exists(img_list_path):
        print "Frame folder not found..."
        return -1

    #establishing model path and output path
    model_path=os.path.join(dataset_root_path,model_path_surfix)
    if not os.path.exists(model_path):
        print "Establishing model path..."
        os.mkdir(model_path,0755)

    output_path=os.path.join(dataset_root_path,output_path_surfix)
    if not os.path.exists(output_path):
        print "Establishing ouptut path..."
        os.mkdir(output_path,0755)

    #check image count
    path, dirs, files = os.walk(img_list_path).next()
    file_count = 0
    for now_file in files:
        if ".jpg" in now_file.lower():
            file_count += 1
    print "File count: ", file_count
    return file_count

# get corresponding qstringlist from a given bounding box
def get_bbx_qstringlist(now_bbx, id):
    tmp = QStringList(str(now_bbx.fr));
    tmp.append(str(id));
    tmp.append(str(now_bbx.x));
    tmp.append(str(now_bbx.y));
    tmp.append(str(now_bbx.w));
    tmp.append(str(now_bbx.h));
    tmp.append(str(now_bbx.score))
    return tmp

#convert the coordinate in raw image to that in the image view.
def convert_img_cood_to_view(now_bbx,pixmap,widget):
    new_bbx=BBX(now_bbx.fr,now_bbx.x,now_bbx.y,now_bbx.w,now_bbx.h,now_bbx.score)
    img_w=pixmap.width();img_h=pixmap.height()
    wid_w=widget.width();wid_h=widget.height()

    new_bbx.x=round(now_bbx.x*((wid_w+0.0)/img_w),2);new_bbx.w=round(now_bbx.w*((wid_w+0.0)/img_w),2)
    new_bbx.y=round(now_bbx.y*((wid_h+0.0)/img_h),2);new_bbx.h=round(now_bbx.h*((wid_h+0.0)/img_h),2)

    return new_bbx

#convert the coordinate in the image view to that in raw image
def convert_view_cood_to_img(now_bbx,pixmap,widget):
    new_bbx = BBX(now_bbx.fr, now_bbx.x, now_bbx.y, now_bbx.w, now_bbx.h, now_bbx.score)
    img_w = pixmap.width()
    img_h = pixmap.height()
    wid_w = widget.width()
    wid_h = widget.height()
    new_bbx.x = round(now_bbx.x * (1.0/((wid_w + 0.0) / img_w)), 2)
    new_bbx.w = round(now_bbx.w * (1.0/((wid_w + 0.0) / img_w)), 2)
    new_bbx.y = round(now_bbx.y * (1.0/((wid_h + 0.0) / img_h)), 2)
    new_bbx.h = round(now_bbx.h * (1.0/((wid_h + 0.0) / img_h)), 2)

    return new_bbx

#split the "target id" form back to "id"
def get_target_id_from_widget_item(widget_item_text):
    pass
    tmp_str=widget_item_text.split(" ")
    return int(tmp_str[1])

#check whether an widget item is valid
def validate_widget_item(object_id,widget_box_item,pixmap):
    img_w = pixmap.width()
    img_h = pixmap.height()
    flag=True
    try:
        fr=int(widget_box_item.text(0));id=int(widget_box_item.text(1))
        if not id==object_id:
            flag=False
        x=float(widget_box_item.text(2)); y=float(widget_box_item.text(3)); w=float(widget_box_item.text(4)); h=float(widget_box_item.text(5))
        score=float(widget_box_item.text(6))
        if not ((x>=1 and x<=img_w) and (y>=1 and y<=img_h) and (x+w<=img_w) and (x+w>=1) and (y+h<=img_h) and (y+h>=1)):
            flag=False
    except:
        print "invalid found..."
        flag=False
       # raise
    return flag

#Converts a QImage into an opencv MAT format
def convert_qimage_to_mat(incomingImage):

    incomingImage = incomingImage.convertToFormat(4)
    width = incomingImage.width()
    height = incomingImage.height()
    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr

#Check whether existing previous annotation results
def check_exists_previous_annotation(dataset_root_path):
    print "Checking whether have existing result..."
    output_root_path=os.path.join(dataset_root_path,"output")
    p=0
    while True:
        print os.path.join(output_root_path,"output_iteration_"+str(p+1)+".txt")
        if  os.path.isfile(os.path.join(output_root_path,"output_iteration_"+str(p+1)+".txt")):
            p+=1
        else:
            break
    if p==0:
        return False
    else:
        return True

#get the iteration number from existing annotation filename
def get_previous_iteration_by_annotation_filename(now_using_base_annotation_path):
    now_using_base_annotation_path=str(now_using_base_annotation_path)
    tmp_pos_1=now_using_base_annotation_path.rindex("_")
    tmp_pos_2=now_using_base_annotation_path.rindex(".")
    return int(now_using_base_annotation_path[tmp_pos_1+1:tmp_pos_2])

#get up-to-date result with tracker and detections (using a sepearate thread...)
class thread_update_tracking_result(QThread):
    finished = pyqtSignal(['QString'])
    def __init__(self,dataset_instance,tracker_filename,track_all,parent=None):
        super(thread_update_tracking_result,self).__init__(parent)
        self.dataset_instance=dataset_instance;self.tracker_filename=tracker_filename
        self.track_all=track_all

    def run(self):
        print "generating tracking result, with dataset:  "+self.dataset_instance.dataset_root_path+"  , using tracker_filename"+self.tracker_filename
        #first we need to generate a temporary file as detection input
        tmp_annotation_filename = os.path.join(self.dataset_instance.dataset_tmp_root_path, "tmp_det_to_test.txt")
        tmp_tracking_output_filename=os.path.join(self.dataset_instance.dataset_tmp_root_path,"tmp_tracking_output.txt")

        if not self.track_all:
            #track only not annotated objects (i.e., the newly inserted ones, etc...)
            self.dataset_instance.dump_annotation_result(tmp_annotation_filename,1)
        else:
            #track all the objects
            self.dataset_instance.dump_annotation_result(tmp_annotation_filename)

        video_tester=mdp_interactive_test.initialize()
        video_tester.MDP_interactive_test(str(self.dataset_instance.dataset_root_path),str(self.tracker_filename),self.dataset_instance.img_count,str(tmp_tracking_output_filename))
        video_tester.terminate()

        #after the tracking is finished, we need to genereate the final output iteration
        if self.track_all:
            #we select to track all objects, directly show them
            print "Handling case with track all objects..."
            #directly copy to output path

        else:
            #we select to partially track not annotated objects
            print "Handling case with track not annotated objects..."
            self.dataset_instance.merge_with_tmp_tracking_output(tmp_tracking_output_filename)

        dest_filename = os.path.join(self.dataset_instance.output_path,
                                     "output_iteration_" + str(self.dataset_instance.train_iteration) + ".txt")
        copyfile(tmp_tracking_output_filename, dest_filename)
        os.remove(tmp_tracking_output_filename)
        self.finished.emit(dest_filename)

#the class of online learning a tracker.
class thread_update_tracker(QThread):
    finished=pyqtSignal()
    def __init__(self,dataset_instance,original_tracker_filename,dest_tracker_filename,train_all,parent=None):
        super(thread_update_tracker, self).__init__(parent)
        self.dataset_instance=dataset_instance;self.original_tracker_filename=original_tracker_filename;self.dest_tracker_filename=dest_tracker_filename
        self.train_all=train_all
    def run(self):
        print "In the thread of updating tracker..."

        #construct the training sample file
        tmp_annotation_filename=os.path.join(self.dataset_instance.dataset_tmp_root_path,"tmp_annotation_to_train_tracker.txt")

        if not self.train_all:
            self.dataset_instance.dump_annotation_result(tmp_annotation_filename,1)
        else:
            self.dataset_instance.dump_annotation_result(tmp_annotation_filename)
        #use the matlab interface to run the tracker trainer
        tracker_trainer = mdp_interactive_train.initialize()
        number_of_new_samples = tracker_trainer.MDP_interactive_train(str(self.dataset_instance.dataset_root_path), str(self.original_tracker_filename), self.dataset_instance.img_count, self.dataset_instance.train_iteration, str(self.dest_tracker_filename))

        tracker_trainer.terminate()
        print "Number of new training samples: ", number_of_new_samples
        self.finished.emit()











