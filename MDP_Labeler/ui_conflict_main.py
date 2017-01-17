from ui_conflict_class import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
class ClassWidgetConflict(QtGui.QWidget):
    def __init__(self,parent,main_diag_instance,im_type):
        QWidget.__init__(self, parent)
        print "in init.........",im_type
        self.main_diag_instance=main_diag_instance
        self.im_type=im_type #1 is tracklet a; 2 is tracklet b

    def mouseReleaseEvent(self, QMouseEvent):
        self.main_diag_instance.ret_stat=self.im_type
        print "in select image "
        self.main_diag_instance.accept()

class ClassConflictDialog(QtGui.QDialog):

    #return stat:
    # stat=5: default
    # stat=1: select from tracklet a
    # stat=2: select from tracklet b
    # stat=3: select all from tracklet a
    # stat=4: select all from tracklet b

    ret_stat=5

    def __init__(self,fr,target_id_a,target_id_b,img_map_a,img_map_b,parent=None):
        QWidget.__init__(self, parent)

        self.ui=Ui_dialog_conflict()
        self.ui.setupUi(self)
        self.ui.view_object_a.setPixmap(img_map_a);self.ui.view_object_b.setPixmap(img_map_b)
        self.ui.centralwidget = parent
        #set text for title and button
        text=self.ui.label_title.text();text=text.replace("xxx",str(fr));self.ui.label_title.setText(text)
        text=self.ui.btn_sel_all_a.text();text=text.replace("A",str(target_id_a));self.ui.btn_sel_all_a.setText(text)
        text=self.ui.btn_sel_all_b.text();text=text.replace("B", str(target_id_b));self.ui.btn_sel_all_b.setText(text)
        text=self.ui.label_det_a.text();text=text.replace("A",str(target_id_a));self.ui.label_det_a.setText(text)
        text=self.ui.label_det_b.text();text=text.replace("B", str(target_id_b));self.ui.label_det_b.setText(text)

        self.ui.btn_sel_all_a.clicked.connect(self.do_sel_a_all)
        self.ui.btn_sel_all_b.clicked.connect(self.do_sel_b_all)
        self.ui.btn_skip.clicked.connect(self.do_skip)

        #set the click view for user to click
        self.ui.click_im_a = ClassWidgetConflict(self, self,1)
        self.ui.click_im_a.setGeometry(QtCore.QRect(90, 110, 241, 431))
        self.ui.click_im_a.setObjectName("click_im_a")
        self.ui.click_im_a.setStyleSheet("background: transparent;")
        self.ui.click_im_a.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.ui.click_im_b = ClassWidgetConflict(self, self,2)
        self.ui.click_im_b.setGeometry(QtCore.QRect(370,110, 241, 431))
        self.ui.click_im_b.setObjectName("click_im_b")
        self.ui.click_im_b.setStyleSheet("background: transparent;")
        self.ui.click_im_b.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    #select a for all
    def do_sel_a_all(self):
        print "merge all from tracklet a"
        self.ret_stat=3
        self.accept()

    #select b for all
    def do_sel_b_all(self):
        print "merge all from tracklet b"
        self.ret_stat=4
        self.accept()

    #skip all
    def do_skip(self):
        print "skip all"
        self.ret_stat=5
        self.accept()

    def get_ret_stat(self):
        return self.ret_stat





