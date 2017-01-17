import sys

from ui_labeler_class import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
from ui_conflict_main import *
import math
from QProgressIndicator import *
from mdp_interactive_test import *
from mdp_labeler_utils import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# we reimplement the QLabel class so that we can re-write the paintEvent function with QPainter

class ClassWidgetPaint(QtGui.QWidget):
    def __init__(self,parent,main_wind_instance):
        QWidget.__init__(self,parent)
        self.main_wind_instance=main_wind_instance

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.widget_paint_context_menu)

    mouse_pressed=False
    right_mouse_pressed=False

    #get target id by mouse position
    def get_target_id_by_position(self,position):
        ret_id=-1;min_dist=sys.maxint
        x=position.x();y=position.y()
        for (target_id,now_box) in self.shown_box_dict.items():
            if (x>=now_box.x and x<=now_box.x+now_box.w and y>=now_box.y and y<=now_box.y+now_box.h):
                dist=math.hypot(x-now_box.x,y-now_box.y)
                if dist<min_dist:
                    min_dist=dist
                    ret_id=target_id
        return ret_id

    #request the context menu
    def widget_paint_context_menu(self,position):
        print "in context menu request...."
        if not self.right_mouse_pressed:
            print "invalid context menu request"
            return

        target_id=self.get_target_id_by_position(position)
        print "widget context menu target id:",target_id

        menu = QMenu()


        # menu list:
        # 1. focus on target
        # 2. hide target
        # 3. Target box interpolation
        # 4. split tracklet from the bounding box
        # 5. delete the bounding box
        # 6. delete target

        hide_all_action=menu.addAction("Hide all targets")
        show_all_action=menu.addAction("Show all targets")

        menu.addSeparator()
        if target_id!=-1:
            focus_action=menu.addAction("Focus on target "+str(target_id))
            hide_action=menu.addAction("Hide target "+str(target_id))
            interpolation_action=menu.addAction("Target box interpolation")
            merge_action=menu.addAction("Merge target tracklet with...")
            split_action=menu.addAction("Split tracklet from the bounding box "+str(target_id))
            delete_box_action = menu.addAction("Delete bounding box " + str(target_id))
            delete_target_action=menu.addAction("Delete target "+str(target_id))

        action = menu.exec_(self.mapToGlobal(position))
        #finished...
        if action==hide_all_action:
            for (track_id, tracklet) in self.main_wind_instance.dataset_instance.tracklet_dict.items():
                self.main_wind_instance.exc_object_set.add(track_id)

        if action==show_all_action:
            self.main_wind_instance.exc_object_set.clear()

        if target_id==-1:
            self.main_wind_instance.load_tracklet_to_widget()
            self.update()
            return

        if action==focus_action:
            self.main_wind_instance.focus_on_target(target_id)

        if action==hide_action:
            self.main_wind_instance.exc_object_set.add(target_id)

        if action==delete_box_action:
            self.main_wind_instance.delete_a_box(target_id,self.main_wind_instance.dataset_instance.im_p)

        if action==delete_target_action:
            self.main_wind_instance.user_delete_an_object(target_id)

        if action==split_action:
            self.main_wind_instance.dataset_instance.split_a_tracklet(target_id,self.main_wind_instance.dataset_instance.im_p)

        if action==interpolation_action:
            self.main_wind_instance.dataset_instance.do_interpolation(target_id)

        if action==merge_action:
            num, ok = QInputDialog.getInt(self.main_wind_instance, "Merge with...", "Merge with which target?")
            if ok:
                if self.main_wind_instance.dataset_instance.tracklet_dict.has_key(num):
                    self.main_wind_instance.tracklet_merge(target_id,num)
                else:
                    QMessageBox.warning(self.main_wind_instance, 'Error target id', 'The input traget id is invalid!', QMessageBox.Cancel)

        if action!=merge_action:
            self.main_wind_instance.load_tracklet_to_widget()
            self.update()

        self.right_mouse_pressed=False

    def draw_bounding_box(self,dataset_instance):

        #a temporary dict which stores the present shown bounding box information
        self.shown_box_dict=dict()

        painter=QtGui.QPainter()
        #start painting
        painter.begin(self)
        pen=QtGui.QPen()
        font=QFont()
        font.setPixelSize(17)
        for (track_id, tracklet) in dataset_instance.tracklet_dict.items():
            if (track_id in self.main_wind_instance.exc_object_set):
                continue
            for now_bbx in tracklet:
                if now_bbx.fr == dataset_instance.im_p:
                    #convert x,y,w,h in video data to that of image view
                    now_bbx=convert_img_cood_to_view(now_bbx,self.main_wind_instance.img_map,self)
                    pen.setBrush(dataset_instance.color_dict[track_id]);pen.setWidth(4);painter.setPen(pen)
                    painter.setFont(font)
                    painter.drawText(QRect(now_bbx.x,now_bbx.y,now_bbx.w,now_bbx.h).topLeft(),str(track_id))
                    painter.drawRect(round(now_bbx.x), round(now_bbx.y), round(now_bbx.w), round(now_bbx.h))
                    self.shown_box_dict[track_id]=now_bbx
                    break

        #finish painting
        painter.end()

    def paintEvent(self, QPaintEvent):
        #test communication function
        if not (self.main_wind_instance.dataset_instance is None):

            if self.main_wind_instance.dataset_instance.im_p==0:
                return
           # print "paint event, fr:", self.main_wind_instance.dataset_instance.im_p

            #exhibits the bounding boxes...
            dataset_instance=self.main_wind_instance.dataset_instance
            self.draw_bounding_box(dataset_instance)

            #draw the user annotated bounding box
            if self.mouse_pressed:
                painter=QtGui.QPainter()
                painter.begin(self);pen=QtGui.QPen();pen.setWidth(2);pen.setBrush(Qt.red)
                painter.setPen(pen)
                tmp_x=self.mouse_st.x();tmp_y=self.mouse_st.y();tmp_w=self.mouse_end.x()-tmp_x;tmp_h=self.mouse_end.y()-tmp_y
                painter.drawRect(QRect(tmp_x,tmp_y,tmp_w,tmp_h))
                painter.end()
                #self.main_wind_instance.load_tracklet_to_widget()

        else:
            print "paint event, invalid callback, passby..."

    #we not implement the function for user annotation
    def mousePressEvent(self, QMouseEvent):
        #we first check whether the im_view has valid image and the player is in the pause state
        if self.main_wind_instance.player_state==0:
            print "in pause state"
            if QMouseEvent.button()==Qt.LeftButton:
                self.mouse_pressed=True
                self.main_wind_instance.ui.btn_newbox.setEnabled(False)
                self.mouse_st=QMouseEvent.pos()
                self.mouse_end=QMouseEvent.pos()
                self.update()
            elif QMouseEvent.button()==Qt.RightButton:
                print "right button down...."
                self.right_mouse_pressed=True

        else:
            print "invalid state"

    def mouseMoveEvent(self, QMouseEvent):
        if self.mouse_pressed:
            #the mouse is pressed, therefore it is a valid movement
            print "valid movement"
            self.mouse_end=QMouseEvent.pos()
            self.update()
        else:
            print "invalid movement"

    def mouseReleaseEvent(self, QMouseEvent):
        if self.mouse_pressed:
            print "valid mouse released...."
            self.mouse_pressed=False
            if not self.mouse_end==self.mouse_st:
                self.main_wind_instance.ui.btn_newbox.setEnabled(True)
        elif self.right_mouse_pressed:
            print "valid right mouse released..."
        else:
            print "invalid mouse released..."

# the main class
class class_MDP_labeler(QtGui.QMainWindow):
    dataset_instance=None

    video_timer=QTimer(); video_timer_order=1  #1: play, -1: rewind
    frame_rate=7

    #we  need to define a state variable for the player as player_state
    # player_state=0: pasue/idle
    # player_state=1: play in forward order
    # player_state=2: play in backward order
    # player_state=-1: no dataset loaded, initial state

    player_state=-1

    #the initial pre-trained model path
    initial_model_path="default.mat"
    def __init__(self, parent=None):
        super(class_MDP_labeler,self).__init__(parent)
        self.ui=Ui_MDPLabler()
        self.ui.setupUi(self)

        #set the paint widget
        self.ui.widget_paint = ClassWidgetPaint(self.ui.centralwidget,self)
        self.ui.widget_paint.setGeometry(QtCore.QRect(30, 110, 831, 651))
        self.ui.widget_paint.setObjectName(_fromUtf8("widget_paint"))
        self.ui.widget_paint.setStyleSheet(_fromUtf8("background: transparent;"))

        #set button signal-slot pairs
       # self.ui.btn_exit.clicked.connect(self.do_exit)
       # self.ui.btn_about.clicked.connect(self.do_about)

        #set choose folder
        self.ui.btn_choose_dataset.clicked.connect(self.do_choose_dataset)

        #set play, pause, rewind, new bounding box
        self.ui.btn_play.clicked.connect(self.do_play)
        self.ui.btn_pause.clicked.connect(self.do_pause)
        self.ui.btn_rewind.clicked.connect(self.do_rewind)
        self.ui.btn_newbox.clicked.connect(self.do_new_box)
        self.ui.btn_prev.clicked.connect(self.do_prev)
        self.ui.btn_succ.clicked.connect(self.do_succ)
        self.ui.btn_save_result.clicked.connect(self.do_save_result)
        self.ui.btn_out_video.clicked.connect(self.do_output_video)
        self.ui.btn_update.clicked.connect(self.do_update_model)
        self.ui.btn_do_track.clicked.connect(self.do_track)

        #set a global QPixmap, over it is an QPainter meant to draw bounding box
        self.img_map=QPixmap()
        self.ui.view_im.setPixmap(self.img_map)

        #set timer event
        self.video_timer.timeout.connect(self.change_frame)

        #set slider event
        self.ui.slider_im.sliderReleased.connect(self.slider_value_changed)

        #set detection widget item changed event, along with the button of show only present frame
        self.ui.widget_dets.itemChanged.connect(self.widget_dets_item_changed)
        self.ui.widget_dets.itemCollapsed.connect(self.widget_dets_item_collapsed)
        self.ui.widget_dets.itemExpanded.connect(self.widget_dets_item_expanded)
        self.ui.widget_dets.itemDoubleClicked.connect(self.widget_dets_item_double_clicked)
        self.ui.widget_dets.itemClicked.connect(self.widget_dets_item_clicked)
        #set the custom context menu for widget objects
        self.ui.widget_dets.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.widget_dets.customContextMenuRequested.connect(self.widget_det_context_menu)

        #select the multiple selection option
        self.ui.widget_dets.itemSelectionChanged.connect(self.widget_det_item_selection_changed)

        #a flag specifies whether updating widget_dets
        self.in_update_widget_dets=False
        self.in_spin_mode=False

        self.ui.chbox_frame.stateChanged.connect(self.frame_only_box_changed)
        self.ui.btn_hide_all.clicked.connect(self.do_hide_all)

    #item selection changed
    def widget_det_item_selection_changed(self):
        print "item selection changed...."

        #larger than 2 selected, no matter what happens, exit!!!
        if len(self.ui.widget_dets.selectedItems())>2:
            self.ui.widget_dets.clearSelection()
            return

        self.multi_item_selection = True
        self.multi_box_selection = True

        #check whether two person are selected
        for now_sel_item in self.ui.widget_dets.selectedItems():
            print "sel:",now_sel_item
            try:
                get_target_id_from_widget_item(now_sel_item.text(0))
            except:
                #not multi person selected....
                self.multi_item_selection=False

        if self.multi_item_selection:
            #confirmed is multi item selected....
            print "confirmed multi target selection"
            return

        #for the case of two bounding boxes are selected
        for now_sel_item in self.ui.widget_dets.selectedItems():
            try:
                get_target_id_from_widget_item(now_sel_item.parent().text(0))
            except:
                self.multi_box_selection=False

        if self.multi_box_selection:
            print "confirmed multi box selection"
        else:
            self.ui.widget_dets.clearSelection()

    #save results
    def do_save_result(self):
        #print "save present result..."
        time_str=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        default_file_name=self.dataset_instance.dataset_root_path+"/annotation_"+time_str+".txt"
        file_path=QFileDialog.getSaveFileName(self,"Save annotation file",default_file_name,"annotation files (*.txt)")
        if file_path!="":
            self.dataset_instance.dump_annotation_result(file_path)
        else:
            print "User does not make a valid selection..."
    #hide button event
    def do_hide_all(self):
        print "collapse/expand all button down..."
        if (self.ui.btn_hide_all.text()=="collapse all"):
            #collapse all tracklet
            self.ui.btn_hide_all.setText("expand all")
            for (track_id, tracklet) in self.dataset_instance.tracklet_dict.items():
                self.exc_object_set.add(track_id)
        else:
            #expand all tracklet
            self.ui.btn_hide_all.setText("collapse all")
            self.exc_object_set.clear()

        self.load_tracklet_to_widget()
        self.ui.widget_paint.update()

    #show only present frame detection check box changed
    def frame_only_box_changed(self):
        #reload the detection tracklet
        self.load_tracklet_to_widget()

    #the context menu for widget detection
    def widget_det_context_menu(self,position):
        if len(self.ui.widget_dets.selectedItems())==0:
            #check whether it is a valid detection item
            tmp_item=self.ui.widget_dets.itemAt(position)
            if tmp_item.columnCount()>1:
                self.widget_det_context_menu_single_detection(position,tmp_item)
            return

        if len(self.ui.widget_dets.selectedItems())==1:
            self.widget_det_context_menu_single_item(position)
        elif len(self.ui.widget_dets.selectedItems())==2 and self.multi_item_selection:
            self.widget_det_context_menu_multi_item(position)
        elif len(self.ui.widget_dets.selectedItems())==2 and self.multi_box_selection:
            print "multi box selected..."
            self.widget_det_context_menu_multi_box(position)

    #multiple box context menu
    def widget_det_context_menu_multi_box(self,position):
        menu=QMenu()

        target_id=int(get_target_id_from_widget_item(self.ui.widget_dets.selectedItems()[0].parent().text(0)))
        if not (target_id==get_target_id_from_widget_item(self.ui.widget_dets.selectedItems()[1].parent().text(0))):
            QMessageBox.warning(self, 'Error data', 'The bounding boxes do not belong to same target!', QMessageBox.Cancel)
            return

        box_1 = self.ui.widget_dets.selectedItems()[0];box_2 = self.ui.widget_dets.selectedItems()[1]
        box_1_fr = int(box_1.text(0)); box_2_fr = int(box_2.text(0))

        if box_1_fr>box_2_fr:
            box_1_fr,box_2_fr=box_2_fr,box_1_fr

        link_action=menu.addAction("Target box interpolation from "+str(box_1_fr)+" to "+str(box_2_fr))
        delete_action=menu.addAction("Delete target box from "+str(box_1_fr)+" to "+str(box_2_fr))
        action=menu.exec_(self.ui.widget_dets.mapToGlobal(position))

        if action==link_action:
            print "in interpolate between bounding box...."
            self.dataset_instance.do_interpolation(target_id,box_1_fr,box_2_fr)

        elif action==delete_action:
            print "in delete operation..."
            self.delete_multiple_box(target_id,box_1_fr,box_2_fr)


        self.load_tracklet_to_widget()
        self.ui.widget_paint.update()

    #context menu on a single detection
    def widget_det_context_menu_single_detection(self,position,tmp_item):
        menu=QMenu()
        delete_action=menu.addAction("Delete the bounding box")
        split_action=menu.addAction("Split tracklet from the box")
        object_id = int(tmp_item.text(1));fr = int(tmp_item.text(0))
        action=menu.exec_(self.ui.widget_dets.mapToGlobal(position))
        if action==delete_action:
            print "Delete bounding box from context menu..."
            self.delete_a_box(object_id,fr)

        elif action==split_action:
            print "Split bounding box from context menu..."
            new_object_id=self.dataset_instance.split_a_tracklet(object_id,fr)
        self.load_tracklet_to_widget()
        self.ui.widget_paint.update()

    #context menu multiple item selected
    def widget_det_context_menu_multi_item(self,position):
        print "multi selected...into merge mode..."
        menu=QMenu()
        target_1=self.ui.widget_dets.selectedItems()[0];target_2=self.ui.widget_dets.selectedItems()[1]
        target_1_id=get_target_id_from_widget_item(target_1.text(0));target_2_id=get_target_id_from_widget_item(target_2.text(0))
        merge_action=menu.addAction("Merge tracklet "+str(target_1_id)+" with "+str(target_2_id)+" ...")
        action=menu.exec_(self.ui.widget_dets.mapToGlobal(position))
        if merge_action==action:
            print "in merge...."
            self.tracklet_merge(target_1_id,target_2_id)

    def tracklet_merge(self,target_a_id,target_b_id):

        st_a,end_a=self.dataset_instance.get_target_start_end_frame(target_a_id);st_b,end_b=self.dataset_instance.get_target_start_end_frame(target_b_id)
        start_fr=min(st_a,st_b);end_fr=max(end_a,end_b)
        merged_box_list=[]

        flag_interpolate=False
        ret_stat=5

        for fr in xrange(start_fr,end_fr+1):
            print "handle merge of frame: ",fr
            now_box_a=self.dataset_instance.find_bounding_box_by_id_and_frame(target_a_id,fr);now_box_b=self.dataset_instance.find_bounding_box_by_id_and_frame(target_b_id,fr)
            if (not(now_box_a is None)) and (not(now_box_b is None)):
                #handling the confliction case
                print "handling confliction at frame :",fr

                #get cropped object instance
                img_map_a=self.dataset_instance.get_crop_img_region(fr,now_box_a);img_map_b=self.dataset_instance.get_crop_img_region(fr,now_box_b)
                conf_diag=ClassConflictDialog(fr,target_a_id,target_b_id,img_map_a,img_map_b,self.ui.centralwidget)

                #user already choose to skip, directly merge
                if ret_stat==3:
                    merged_box_list.append(now_box_a)
                    continue
                if ret_stat==4:
                    merged_box_list.append(now_box_b)
                    continue

                #otherwise let user to choose get the return value
                if (conf_diag.exec_()):
                    #already obtain the return value
                    ret_stat=conf_diag.get_ret_stat()
                    if ret_stat==1 or ret_stat==3:
                        #merge from a
                        merged_box_list.append(now_box_a)
                    if ret_stat==2 or ret_stat==4:
                        #merge from b
                        merged_box_list.append(now_box_b)
                    if ret_stat==5:
                        flag_interpolate=True

                continue
            if not (now_box_a is None):
                # merge from tracklet a
                merged_box_list.append(now_box_a)
            elif not (now_box_b is None):
                # merge from tracklet b
                merged_box_list.append(now_box_b)
            else:
                #None in present frame
                flag_interpolate=True

         #merge to a longer existing tracklet

        #merge into a longer tracklet and delete another one
        if (end_a-st_a>end_b-st_b):
            new_target_id=self.dataset_instance.replace_existing_tracklet_with_new(target_a_id,merged_box_list)
            self.dataset_instance.delete_an_object(target_b_id)
        else:
            new_target_id=self.dataset_instance.replace_existing_tracklet_with_new(target_b_id,merged_box_list)
            self.dataset_instance.delete_an_object(target_a_id)

        #need interpolation
        if flag_interpolate:
            print "need interpolating...."
            reply=QMessageBox.question(self,"Target interpolation?","There is gap among merged tracklet, conduct interpolation?",QMessageBox.Yes|QMessageBox.No)
            if reply==QMessageBox.Yes:
                print "user choose interpolation..."
                self.dataset_instance.do_interpolation(new_target_id)

        #update the gui
        try:
            self.exc_object_set.remove(new_target_id)
        except:
            pass
        self.ui.widget_paint.update()
        self.load_tracklet_to_widget()

    #delete a box
    def delete_a_box(self,object_id,fr):
        reply = QMessageBox.question(self, "Delete the bounding box?",
                                     "Are you sure to delete the box of target "+str(object_id)+" in frame "+str(fr)+"?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply==QMessageBox.Yes:
            print "reply of delete a box is true"
            self.dataset_instance.delete_a_box(object_id, fr)

    #delete multiple boxes
    def delete_multiple_box(self,object_id,fr_1,fr_2):
        reply = QMessageBox.question(self, "Delete multiple bounding boxes?",
                                     "Are you sure to delete the box of target " + str(object_id) + " from frame " + str(
                                         fr_1) +" to frame "+str(fr_2)+ "?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply==QMessageBox.Yes:
            print "reply of delete series of boxes is true"
            for fr in xrange(fr_1,fr_2+1):
                self.dataset_instance.delete_a_box(object_id,fr)

    #focus on target
    def focus_on_target(self,now_target_id):
        for (track_id, tracklet) in self.dataset_instance.tracklet_dict.items():
            self.exc_object_set.add(track_id)
        self.exc_object_set.remove(now_target_id)

    #user delete an traget
    def user_delete_an_object(self,now_target_id):
        reply=QMessageBox.question(self,"Delete a target?","Are you sure to delete target "+str(now_target_id)+"?",QMessageBox.Yes | QMessageBox.No)
        if reply==QMessageBox.Yes:
            self.dataset_instance.delete_an_object(now_target_id)

    #context menu with single item selected....(interpolation etc...)
    def widget_det_context_menu_single_item(self,position):

        now_tracklet=self.ui.widget_dets.selectedItems()[0]
        try:
            now_target_id=get_target_id_from_widget_item(now_tracklet.text(0))
            print " context target id,",now_target_id
        except:
            #invalid call
            return
        menu=QMenu()
        link_action=menu.addAction("Target box interpolation")
        show_only_action=menu.addAction("Focus on target")
        delete_action=menu.addAction("Delete target")
        action=menu.exec_(self.ui.widget_dets.mapToGlobal(position))

        if action==link_action:
            #linear interpolation for now_target_id
            self.dataset_instance.do_interpolation(now_target_id)

        if action==show_only_action:
            try:
                print "show only: ",now_target_id
                self.focus_on_target(now_target_id)
            except:
                return

        if action==delete_action:
            self.user_delete_an_object(now_target_id)

        self.load_tracklet_to_widget()
        self.ui.widget_paint.update()

    #there is expand or collapse event happened in the widget detection
    def widget_dets_item_collapsed(self,now_tracklet):
        try:
            now_target_id=get_target_id_from_widget_item(now_tracklet.text(0))
            self.exc_object_set.add(now_target_id)
        except:
            return
        self.ui.widget_paint.update()

        print "widget detection item collapsed..."

    def widget_dets_item_expanded(self,now_tracklet):

        # we also need to specify whether the expanded is conducted by the load_tracklet_to_widget function
        # or conducted by user operation.
        if self.in_update_widget_dets==True:
            return

        try:
            now_target_id=get_target_id_from_widget_item(now_tracklet.text(0))
            if now_target_id in self.exc_object_set:
                self.exc_object_set.remove(now_target_id)
        except:
            return
        self.ui.widget_paint.update()
        print "widget detection item expanded..."

    #confirm the spin mode changes
    def confirm_spin_mode_changes(self):
        self.in_spin_mode=False
        print "confirm spin mode changes value:",self.spin_item_value
        self.spin_item.setText(self.spin_col, str(self.spin_item_value))
        #self.widget_dets_item_changed(self.spin_item)
        self.ui.widget_paint.update()
        pass

    #detection widget item one-shot clicked, whether confirm the change and exit the spin mode
    def widget_dets_item_clicked(self,tmp_item,tmp_col):
        #is an invalid single click

        if (tmp_item.columnCount()>1 and tmp_col==0):
            #a frame is selected
            self.ui.slider_im.setValue(int(tmp_item.text(tmp_col)))
            self.slider_value_changed()

        if not self.in_spin_mode:
            return
        #is an event elicited by actually the double clicked
        if (tmp_item==self.spin_item and tmp_col==self.spin_col):
            return
        print "Confirm spin mode changes..."
        self.confirm_spin_mode_changes()
        self.load_tracklet_to_widget()

    #spin box value changed
    def spin_box_value_changed(self,value):
        print "spin box value changed...."
        if not self.in_spin_mode:
            print "invalid spin box value changes..."
            return
        self.spin_item_value=str(value)

    #detection widget item double clicked
    def widget_dets_item_double_clicked(self,item_selected,col_selected):
        print "item is double clicked..."
        try:
            now_tracklet=item_selected.parent()
            now_target_id=get_target_id_from_widget_item(now_tracklet.text(0))
        except:
            print "invalid double clicked..."
            return
        print "valid double clicked... "
        #now x,y,w,h column, not able to adjust via spinning...
        if not (col_selected>=2 and col_selected<=5):
            return

        test_type=self.ui.widget_dets.itemWidget(item_selected,col_selected)
        print test_type
        org_content=item_selected.text(col_selected)
        now_spin_box=QDoubleSpinBox()
        #get the valid range
        if (col_selected==2 or col_selected==4):
            #x,w
            range_max=self.img_map.width()
        else:
            #y,h
            range_max = self.img_map.height()
        now_spin_box.setRange(1,range_max);now_spin_box.setSingleStep(1.0);now_spin_box.setValue(float(org_content))
        now_spin_box.valueChanged.connect(self.spin_box_value_changed)
        self.ui.widget_dets.setItemWidget(item_selected,col_selected,now_spin_box)

        self.in_spin_mode=True
        self.spin_item=item_selected;self.spin_col=col_selected;self.spin_item_value=org_content;self.spin_item_id=int(item_selected.text(1))
        print "Double clicked finished..."
        pass

    #detection widget item chagned event
    def widget_dets_item_changed(self, col_selected, col):
        print "widget detection item changed..."
        try:
            now_target_id=int(col_selected.text(1))
        except:
            now_target_id=self.spin_item_id
        if validate_widget_item(now_target_id,col_selected,self.img_map) and col!=0:
            self.dataset_instance.update_tracklet_from_widget_det(now_target_id,col_selected)
            self.load_tracklet_to_widget()
        else:
            print "invalid box"
            QMessageBox.warning(self,'Error data','The input data is invalid!',QMessageBox.Cancel)
            self.load_tracklet_to_widget()

        #update the painting interface
        self.ui.widget_paint.update()

    #slider value changed
    def slider_value_changed(self):
        print "silder value changed..."
        tmp_im_p=self.ui.slider_im.value()
        self.dataset_instance.set_im_position(tmp_im_p)
        self.ui.view_im.setPixmap(QPixmap(self.dataset_instance.now_im_filename))
        self.ui.label_frame.setText(str(tmp_im_p) + "/" + str(self.dataset_instance.img_count))
        self.ui.btn_newbox.setEnabled(False)
        self.load_tracklet_to_widget()
    #play button
    def do_play(self):
        print "play button down..."
        #disable play, rewind
        self.ui.btn_play.setEnabled(False);self.ui.btn_rewind.setEnabled(False)
        #enable pause
        self.ui.btn_pause.setEnabled(True);self.video_timer_order=1;self.video_timer.start(1000/self.frame_rate)
        self.player_state = 1 #set state variable to forward playing mode

    #pause button
    def do_pause(self):
        print "pause button down..."

        #disable pause
        self.ui.btn_pause.setEnabled(False)
        #enable play and rewind
        self.ui.btn_play.setEnabled(True);self.ui.btn_rewind.setEnabled(True)
        #disable timer
        self.video_timer.stop()
        self.player_state=0 #set the state variable to pause

    #succ button
    def do_succ(self):
        print "succ button down..."
        tmp_im_p=self.dataset_instance.im_p
        tmp_im_p+=1;tmp_im_p=min(tmp_im_p, self.dataset_instance.img_count)
        self.dataset_instance.set_im_position(tmp_im_p)
        self.ui.slider_im.setSliderPosition(tmp_im_p)
        self.ui.view_im.setPixmap(QPixmap(self.dataset_instance.now_im_filename))
        self.ui.label_frame.setText(str(tmp_im_p) + "/" + str(self.dataset_instance.img_count))
        self.ui.btn_newbox.setEnabled(False)
        self.load_tracklet_to_widget()

    #prev button
    def do_prev(self):
        print "prev button down..."
        tmp_im_p=self.dataset_instance.im_p
        tmp_im_p-=1;tmp_im_p=max(tmp_im_p, 1)
        self.dataset_instance.set_im_position(tmp_im_p)
        self.ui.slider_im.setSliderPosition(tmp_im_p)
        self.ui.view_im.setPixmap(QPixmap(self.dataset_instance.now_im_filename))
        self.ui.label_frame.setText(str(tmp_im_p) + "/" + str(self.dataset_instance.img_count))
        self.ui.btn_newbox.setEnabled(False)
        self.load_tracklet_to_widget()

    #rewind button
    def do_rewind(self):
        print "rewind button down..."
        self.ui.btn_play.setEnabled(False);self.ui.btn_rewind.setEnabled(False)
        self.ui.btn_pause.setEnabled(True)
        self.video_timer_order=-1;self.video_timer.start(1000/self.frame_rate)
        self.player_state=2 #set the state variable to rewind state

    #change frame, the timer event
    def change_frame(self):

        #handle next/prev frame and boundary cases
        tmp_im_p=self.dataset_instance.im_p
        tmp_im_p+=self.video_timer_order
        tmp_im_p = max(1, tmp_im_p)
        tmp_im_p = min(tmp_im_p, self.dataset_instance.img_count)

        #update dataset instance
        self.dataset_instance.set_im_position(tmp_im_p)
        self.ui.slider_im.setSliderPosition(tmp_im_p)
        print "change frame: "+str(self.dataset_instance.im_p)
        #update image in view
        self.ui.view_im.setPixmap(QPixmap(self.dataset_instance.now_im_filename))

        self.ui.label_frame.setText(str(tmp_im_p)+"/" + str(self.dataset_instance.img_count))
        self.ui.btn_newbox.setEnabled(False)

        #handle pause cases
        if (tmp_im_p==1 or tmp_im_p==self.dataset_instance.img_count):
            self.do_pause()

        self.load_tracklet_to_widget()

    # choose dataset
    def do_choose_dataset(self):
        print "choose dataset..."
        video_folder=str(QtGui.QFileDialog.getExistingDirectory(self, "Select a dataset to annotate"))

        #check whether valid dataset
        file_count=get_dataset_img_count(video_folder)

        if file_count==-1:
            #invalid path
            print "invalid path..."
            QMessageBox.warning(self,self.tr("Not valid path"),self.tr("This is not a valid path containing the dataset..."))

        else:
            #initialize the dataset instance
            self.dataset_instance=class_dataset(video_folder,file_count)
            #a valid dataset
            print "a valid path..."

            #self.now_using_model_path=self.initial_model_path
            #let user to select a initial tracker model
            self.now_using_model_path=QFileDialog.getOpenFileName(self,"Open an existing tracker",self.initial_model_path,"tracker (*.mat)")

            # enable ui
            # enable path textbox
            self.ui.box_dataset_path.setEnabled(True);self.ui.box_dataset_path.setPlainText(video_folder)
            self.ui.btn_choose_dataset.setEnabled(False)

            #check whether to use existing tracking result OR generate a result from detection result
            has_previous_result=check_exists_previous_annotation(self.dataset_instance.dataset_root_path)

            #if exist, let user to select for initialization, otherwise initialize from null
            if has_previous_result:
                has_previous_result = QMessageBox.question(self, "Use existing annotation result?",
                                             "Do you want to start with an existing tracking annotation?",
                                             QMessageBox.Yes | QMessageBox.No)
            if has_previous_result==QMessageBox.Yes:
                self.now_using_base_annotation_path=QFileDialog.getOpenFileName(self,"Open an existing annotation file",self.dataset_instance.dataset_root_path+"/output/","txt (*.txt)")
                prev_ite=get_previous_iteration_by_annotation_filename(self.now_using_base_annotation_path)
                self.dataset_instance.train_iteration=prev_ite
            else:
                self.now_using_base_annotation_path="null_det.txt"
                self.dataset_instance.train_iteration=0

            self.finish_tracking()

    #do track
    def do_track(self):
        print "Conduct tracking..."

        track_all=QMessageBox.question(self, "Track all targets?",
                                             "Do you want to re-treack annotated tracklets?",
                                             QMessageBox.Yes | QMessageBox.No)

        if track_all==QMessageBox.Yes:
            track_all=True
        else:
            track_all=False

        self.ui.centralwidget.setEnabled(False)
        self.progress_bar = QProgressIndicator(self.ui.centralwidget)
        self.progress_bar.setAnimationDelay(70)
        self.progress_bar.startAnimation()

        self.update_tracking_result_instance = thread_update_tracking_result(self.dataset_instance,
                                                                             self.now_using_model_path,track_all)
        self.update_tracking_result_instance.finished.connect(self.finish_tracking)
        self.update_tracking_result_instance.start()

        print "Finished tracking..."


    # finish tracking callback function
    def finish_tracking(self, output_file_list_filename=None):

        # the exclusive set, when the traget in this list, the result will not be exhibited
        self.exc_object_set = set()

        try:
            self.progress_bar.close()
            self.ui.centralwidget.setEnabled(True)
        except:
            pass
        #enable choose folder button
        self.ui.btn_choose_dataset.setEnabled(True)

        #increase train iteration of the instance
        self.dataset_instance.train_iteration+=1


        if output_file_list_filename is None:
            output_file_list_filename=self.now_using_base_annotation_path
        else:
            output_file_list_filename=str(output_file_list_filename)

        print "Tracking finished..." + output_file_list_filename
        #read the tracking results
        self.dataset_instance.load_detection_results(output_file_list_filename)

        #exhibit the tracking results to show
        self.exhibit_tracking_result(self.dataset_instance)

    #exhibit tracking results, enable button, etc.
    def exhibit_tracking_result(self,dataset_instance):
        print "Exhibit tracking result..."

        #enable ui buttons, etc
        self.ui.btn_play.setEnabled(True);self.ui.btn_pause.setEnabled(True);self.ui.btn_pause.setEnabled(True)
        self.ui.btn_prev.setEnabled(True);self.ui.btn_succ.setEnabled(True);self.ui.btn_hide_all.setEnabled(True)
        self.ui.slider_im.setEnabled(True);self.ui.widget_dets.setEnabled(True)
        self.ui.btn_out_video.setEnabled(True);self.ui.btn_update.setEnabled(True);self.ui.btn_do_track.setEnabled(True)
        self.ui.chbox_frame.setEnabled(True);self.ui.btn_save_result.setEnabled(True)

        #enable frame label
        self.ui.label_frame.setEnabled(True)

        #update training iteration
        self.ui.label_iteration.setText("Iteration: "+str(self.dataset_instance.train_iteration))

        #load tracking result to widget
        self.load_tracklet_to_widget()

        #play video, enable video player
        self.ui.label_frame.setText("1/"+str(self.dataset_instance.img_count))
        self.dataset_instance.set_im_position(1)

        #show the first image
        self.ui.view_im.setPixmap(QPixmap(self.dataset_instance.now_im_filename))
        self.img_map.load(self.dataset_instance.now_im_filename)

        #draw bounding box on the painter
        #self.draw_bounding_box()

        self.ui.slider_im.setSliderPosition(1)
        self.ui.slider_im.setMaximum(dataset_instance.img_count)
        self.player_state=0

    #edit an human annotated bounding box
    def do_new_box(self):
        print "new bounding box"
        num, ok = QInputDialog.getInt(self, "New Box", "object id (0 for a new object)")
        if ok:
            #add the new bounding box
            if (num==0):
                pass  #case with adding a new bounding box
                self.dataset_instance.add_new_object_from_widget_paint(self.ui.widget_paint,self.img_map)
                self.ui.widget_paint.update()
                #update widget detection
                self.load_tracklet_to_widget()
            else:
                pass  #case with editing a existing bounding box
                self.dataset_instance.add_to_existing_object_from_widget_paint(num,self.ui.widget_paint,self.img_map)
                self.ui.widget_paint.update()
                #update widget detection
                self.load_tracklet_to_widget()

    #load tracklet to widget
    def load_tracklet_to_widget(self):
        self.in_update_widget_dets=True
        #flag of show only now frame
        only_now=self.ui.chbox_frame.isChecked()
        self.ui.widget_dets.clear()
        widget_items=QTreeWidgetItem(self.ui.widget_dets,QStringList(QString("tracklets")))
        widget_items.setExpanded(True)
        for (track_id, tracklet) in self.dataset_instance.tracklet_dict.items():

           # print "Loading tracklet, id:", track_id
            now_person_items=QTreeWidgetItem(None, QStringList(QString("target " + str(track_id))))

            now_person_should_appear=False
            for now_bbx in tracklet:
                tmp_bbx_item=QTreeWidgetItem(None,get_bbx_qstringlist(now_bbx,track_id))

                tmp_bbx_item.setExpanded(True)
                tmp_bbx_item.setFlags(tmp_bbx_item.flags()|Qt.ItemIsEditable)

                #set color

                tmp_bbx_item.setBackgroundColor(0,self.dataset_instance.color_dict[track_id]);tmp_bbx_item.setBackgroundColor(1,self.dataset_instance.color_dict[track_id]);
                tmp_bbx_item.setBackgroundColor(2, self.dataset_instance.color_dict[track_id]);tmp_bbx_item.setBackgroundColor(3,self.dataset_instance.color_dict[track_id]);
                tmp_bbx_item.setBackgroundColor(4, self.dataset_instance.color_dict[track_id]);tmp_bbx_item.setBackgroundColor(5,self.dataset_instance.color_dict[track_id]);tmp_bbx_item.setBackgroundColor(6,self.dataset_instance.color_dict[track_id]);

                if not only_now:
                    # show all objects
                    now_person_items.addChild(tmp_bbx_item)
                    now_person_should_appear=True
                else:
                    #show only present frame objects
                    if now_bbx.fr==self.dataset_instance.im_p:
                        #check whether present object in this frame
                        now_person_items.addChild(tmp_bbx_item)
                        now_person_should_appear = True
            if now_person_should_appear:
                now_person_items.setBackgroundColor(0,self.dataset_instance.color_dict[track_id])
                widget_items.addChild(now_person_items)

                if not track_id in self.exc_object_set:
                    now_person_items.setExpanded(True)

        #set the spinning box for the widget_detection.
        #self.set_spinning_effect_for_widget_dets()

        self.in_update_widget_dets = False
        print "Finished..."

    #output the video
    def do_output_video(self):
        print "output video...."
        self.ui.btn_out_video.setEnabled(False)
        self.ui.btn_out_video.setText("saving...")
        time_str=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        default_file_name=self.dataset_instance.dataset_root_path+"/tracking_vis_"+time_str+".avi"
        file_path=QFileDialog.getSaveFileName(self,"Save video file",default_file_name,"video (*.avi)")

        if file_path=="":
            print "User does not make a valid selection..."
        else:
            self.dataset_instance.dump_tracking_video(file_path,self.exc_object_set)

        self.ui.btn_out_video.setEnabled(True)
        self.ui.btn_out_video.setText("output video")

    #update the model
    def do_update_model(self):
        train_all = QMessageBox.question(self, "Train all targets?",
                                         "Do you want to re-train with annotated tracklets?",
                                         QMessageBox.Yes | QMessageBox.No)

        if train_all == QMessageBox.Yes:
            train_all = True
        else:
            train_all = False

        print "Update the tracking model..."

        default_file_path = self.dataset_instance.dataset_root_path + "/tracker_after_iteration_" + str(self.dataset_instance.train_iteration) + ".mat"
        output_tracker_filepath = QFileDialog.getSaveFileName(self, "Save updated tracker file at ", default_file_path, "tracker (*.mat)")

        print "Save model at: ",output_tracker_filepath

        # the thread of updating the tracker
        self.ui.btn_update.setEnabled(False)
        self.update_tracker_instance = thread_update_tracker(self.dataset_instance,self.now_using_model_path,output_tracker_filepath,train_all)

        #update model
        self.now_using_model_path=output_tracker_filepath
        self.update_tracker_instance.finished.connect(self.finish_updating)
        self.update_tracker_instance.start()

        self.ui.centralwidget.setEnabled(False)
        self.progress_bar = QProgressIndicator(self.ui.centralwidget)
        self.progress_bar.setAnimationDelay(70)
        self.progress_bar.startAnimation()

    #finish updating model callback function
    def finish_updating(self):
        print "Finish updating..."
        self.ui.centralwidget.setEnabled(True)
        self.progress_bar.close()
'''
======================================
        Main program starts here.
======================================
'''

MDP_labeler_app=QtGui.QApplication(sys.argv)
MDP_labler=class_MDP_labeler()
MDP_labler.show()

sys.exit(MDP_labeler_app.exec_())

