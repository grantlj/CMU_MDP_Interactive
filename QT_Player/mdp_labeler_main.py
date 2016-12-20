import sys

from ui_labeler_class import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
from mdp_labeler_utils import *
import math

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

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

    def __init__(self, parent=None):
        super(class_MDP_labeler,self).__init__(parent)
        self.ui=Ui_MDPLabler()
        self.ui.setupUi(self)

        #set choose folder
        self.ui.btn_choose_dataset.clicked.connect(self.do_choose_dataset)

        #set play, pause, rewind, new bounding box
        self.ui.btn_play.clicked.connect(self.do_play)
        self.ui.btn_pause.clicked.connect(self.do_pause)
        self.ui.btn_rewind.clicked.connect(self.do_rewind)
        self.ui.btn_prev.clicked.connect(self.do_prev)
        self.ui.btn_succ.clicked.connect(self.do_succ)


        #set a global QPixmap, over it is an QPainter meant to draw bounding box
        self.img_map=QPixmap()
        self.ui.view_im.setPixmap(self.img_map)

        #set timer event
        self.video_timer.timeout.connect(self.change_frame)

        #set slider event
        self.ui.slider_im.sliderReleased.connect(self.slider_value_changed)

    #slider value changed
    def slider_value_changed(self):
        print "silder value changed..."
        tmp_im_p=self.ui.slider_im.value()
        self.dataset_instance.set_im_position(tmp_im_p)
        self.ui.view_im.setPixmap(QPixmap(self.dataset_instance.now_im_filename))
        self.ui.label_frame.setText(str(tmp_im_p) + "/" + str(self.dataset_instance.img_count))
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

    #prev button
    def do_prev(self):
        print "prev button down..."
        tmp_im_p=self.dataset_instance.im_p
        tmp_im_p-=1;tmp_im_p=max(tmp_im_p, 1)
        self.dataset_instance.set_im_position(tmp_im_p)
        self.ui.slider_im.setSliderPosition(tmp_im_p)
        self.ui.view_im.setPixmap(QPixmap(self.dataset_instance.now_im_filename))
        self.ui.label_frame.setText(str(tmp_im_p) + "/" + str(self.dataset_instance.img_count))

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

        #handle pause cases
        if (tmp_im_p==1 or tmp_im_p==self.dataset_instance.img_count):
            self.do_pause()

    # choose dataset
    def do_choose_dataset(self):
        print "choose dataset..."
        video_folder=str(QtGui.QFileDialog.getExistingDirectory(self, "Select dataset to annotate"))

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
            #enable ui
            #enable path textbox
            self.ui.box_dataset_path.setEnabled(True);self.ui.box_dataset_path.setPlainText(video_folder)
            self.ui.btn_choose_dataset.setEnabled(False)
            #generate first round results with initial model and detections
            self.finish_tracking()

    # finish tracking callback function
    def finish_tracking(self):

        #enable choose folder button
        self.ui.btn_choose_dataset.setEnabled(True)

        #increase train iteration of the instance
        self.dataset_instance.train_iteration+=1

        #then we need to parse and update the tracking result
        output_file_list_filename=os.path.join(self.dataset_instance.output_path,"output_iteration_"+str(self.dataset_instance.train_iteration)+".txt")
        print "Tracking finished..."+output_file_list_filename
        #read the tracking results
        self.dataset_instance.load_detection_results(output_file_list_filename)

        #exhibit the tracking results to show
        self.exhibit_tracking_result(self.dataset_instance)

    #exhibit tracking results, enable button, etc.
    def exhibit_tracking_result(self,dataset_instance):
        print "Exhibit tracking result..."

        #enable ui buttons, etc
        self.ui.btn_play.setEnabled(True);self.ui.btn_pause.setEnabled(True);self.ui.btn_pause.setEnabled(True)
        self.ui.btn_prev.setEnabled(True);self.ui.btn_succ.setEnabled(True);self.ui.slider_im.setEnabled(True)

        #enable frame label
        self.ui.label_frame.setEnabled(True)


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

'''
======================================
        Main program starts here.
======================================
'''

MDP_labeler_app=QtGui.QApplication(sys.argv)
MDP_labler=class_MDP_labeler()
MDP_labler.show()

sys.exit(MDP_labeler_app.exec_())

