# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_labeler_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MDPLabler(object):
    def setupUi(self, MDPLabler):
        MDPLabler.setObjectName(_fromUtf8("MDPLabler"))
        MDPLabler.setEnabled(True)
        MDPLabler.resize(1440, 900)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MDPLabler.sizePolicy().hasHeightForWidth())
        MDPLabler.setSizePolicy(sizePolicy)
        MDPLabler.setMinimumSize(QtCore.QSize(1440, 900))
        MDPLabler.setMaximumSize(QtCore.QSize(1440, 900))
        self.centralwidget = QtGui.QWidget(MDPLabler)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.view_im = QtGui.QLabel(self.centralwidget)
        self.view_im.setEnabled(True)
        self.view_im.setGeometry(QtCore.QRect(30, 110, 831, 651))
        self.view_im.setMinimumSize(QtCore.QSize(831, 651))
        self.view_im.setMaximumSize(QtCore.QSize(831, 651))
        self.view_im.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.view_im.setFocusPolicy(QtCore.Qt.NoFocus)
        self.view_im.setStyleSheet(_fromUtf8("QLabel#view_im {\n"
"    border-style: outset;\n"
"    border-width: 5px;\n"
"    border-color: black;\n"
"}\n"
""))
        self.view_im.setText(_fromUtf8(""))
        self.view_im.setScaledContents(True)
        self.view_im.setObjectName(_fromUtf8("view_im"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 70, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.box_dataset_path = QtGui.QPlainTextEdit(self.centralwidget)
        self.box_dataset_path.setEnabled(False)
        self.box_dataset_path.setGeometry(QtCore.QRect(110, 60, 711, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.box_dataset_path.setFont(font)
        self.box_dataset_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.box_dataset_path.setReadOnly(True)
        self.box_dataset_path.setObjectName(_fromUtf8("box_dataset_path"))
        self.btn_choose_dataset = QtGui.QPushButton(self.centralwidget)
        self.btn_choose_dataset.setGeometry(QtCore.QRect(830, 60, 41, 41))
        self.btn_choose_dataset.setObjectName(_fromUtf8("btn_choose_dataset"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QtCore.QRect(220, 10, 1041, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.slider_im = QtGui.QSlider(self.centralwidget)
        self.slider_im.setEnabled(False)
        self.slider_im.setGeometry(QtCore.QRect(40, 780, 731, 20))
        self.slider_im.setOrientation(QtCore.Qt.Horizontal)
        self.slider_im.setObjectName(_fromUtf8("slider_im"))
        self.label_frame = QtGui.QLabel(self.centralwidget)
        self.label_frame.setEnabled(False)
        self.label_frame.setGeometry(QtCore.QRect(780, 780, 71, 16))
        self.label_frame.setObjectName(_fromUtf8("label_frame"))
        self.label_iteration = QtGui.QLabel(self.centralwidget)
        self.label_iteration.setGeometry(QtCore.QRect(1010, 80, 451, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_iteration.setFont(font)
        self.label_iteration.setText(_fromUtf8(""))
        self.label_iteration.setObjectName(_fromUtf8("label_iteration"))
        self.widget_dets = QtGui.QTreeWidget(self.centralwidget)
        self.widget_dets.setEnabled(False)
        self.widget_dets.setGeometry(QtCore.QRect(900, 110, 521, 691))
        self.widget_dets.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.widget_dets.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.widget_dets.setColumnCount(7)
        self.widget_dets.setObjectName(_fromUtf8("widget_dets"))
        self.widget_dets.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget_dets.headerItem().setFont(0, font)
        self.widget_dets.headerItem().setTextAlignment(1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget_dets.headerItem().setFont(1, font)
        self.widget_dets.headerItem().setTextAlignment(2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget_dets.headerItem().setFont(2, font)
        self.widget_dets.headerItem().setTextAlignment(3, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget_dets.headerItem().setFont(3, font)
        self.widget_dets.headerItem().setTextAlignment(4, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget_dets.headerItem().setFont(4, font)
        self.widget_dets.headerItem().setTextAlignment(5, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget_dets.headerItem().setFont(5, font)
        self.widget_dets.headerItem().setTextAlignment(6, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.widget_dets.headerItem().setFont(6, font)
        self.widget_dets.header().setCascadingSectionResizes(True)
        self.widget_dets.header().setDefaultSectionSize(66)
        self.widget_dets.header().setMinimumSectionSize(66)
        self.widget_dets.header().setSortIndicatorShown(False)
        self.widget_dets.header().setStretchLastSection(False)
        self.btn_update = QtGui.QPushButton(self.centralwidget)
        self.btn_update.setEnabled(False)
        self.btn_update.setGeometry(QtCore.QRect(1120, 817, 93, 41))
        self.btn_update.setObjectName(_fromUtf8("btn_update"))
        self.btn_save_result = QtGui.QPushButton(self.centralwidget)
        self.btn_save_result.setEnabled(False)
        self.btn_save_result.setGeometry(QtCore.QRect(960, 817, 93, 41))
        self.btn_save_result.setObjectName(_fromUtf8("btn_save_result"))
        self.chbox_frame = QtGui.QCheckBox(self.centralwidget)
        self.chbox_frame.setEnabled(False)
        self.chbox_frame.setGeometry(QtCore.QRect(1240, 80, 171, 20))
        self.chbox_frame.setObjectName(_fromUtf8("chbox_frame"))
        self.btn_hide_all = QtGui.QPushButton(self.centralwidget)
        self.btn_hide_all.setEnabled(False)
        self.btn_hide_all.setGeometry(QtCore.QRect(1140, 70, 93, 31))
        self.btn_hide_all.setObjectName(_fromUtf8("btn_hide_all"))
        self.btn_pause = QtGui.QPushButton(self.centralwidget)
        self.btn_pause.setEnabled(False)
        self.btn_pause.setGeometry(QtCore.QRect(323, 821, 93, 41))
        self.btn_pause.setObjectName(_fromUtf8("btn_pause"))
        self.btn_play = QtGui.QPushButton(self.centralwidget)
        self.btn_play.setEnabled(False)
        self.btn_play.setGeometry(QtCore.QRect(197, 821, 93, 41))
        self.btn_play.setObjectName(_fromUtf8("btn_play"))
        self.btn_rewind = QtGui.QPushButton(self.centralwidget)
        self.btn_rewind.setEnabled(False)
        self.btn_rewind.setGeometry(QtCore.QRect(449, 821, 93, 41))
        self.btn_rewind.setObjectName(_fromUtf8("btn_rewind"))
        self.btn_prev = QtGui.QPushButton(self.centralwidget)
        self.btn_prev.setEnabled(False)
        self.btn_prev.setGeometry(QtCore.QRect(71, 821, 93, 41))
        self.btn_prev.setObjectName(_fromUtf8("btn_prev"))
        self.btn_succ = QtGui.QPushButton(self.centralwidget)
        self.btn_succ.setEnabled(False)
        self.btn_succ.setGeometry(QtCore.QRect(575, 821, 93, 41))
        self.btn_succ.setObjectName(_fromUtf8("btn_succ"))
        self.btn_newbox = QtGui.QPushButton(self.centralwidget)
        self.btn_newbox.setEnabled(False)
        self.btn_newbox.setGeometry(QtCore.QRect(701, 821, 93, 41))
        self.btn_newbox.setObjectName(_fromUtf8("btn_newbox"))
        self.btn_out_video = QtGui.QPushButton(self.centralwidget)
        self.btn_out_video.setEnabled(False)
        self.btn_out_video.setGeometry(QtCore.QRect(1280, 820, 93, 41))
        self.btn_out_video.setObjectName(_fromUtf8("btn_out_video"))
        MDPLabler.setCentralWidget(self.centralwidget)

        self.retranslateUi(MDPLabler)
        QtCore.QMetaObject.connectSlotsByName(MDPLabler)

    def retranslateUi(self, MDPLabler):
        MDPLabler.setWindowTitle(_translate("MDPLabler", "MainWindow", None))
        self.label.setText(_translate("MDPLabler", "Dataset path:", None))
        self.box_dataset_path.setPlainText(_translate("MDPLabler", "Please choose a valid dataset folder to start annotation...", None))
        self.btn_choose_dataset.setText(_translate("MDPLabler", "...", None))
        self.label_2.setText(_translate("MDPLabler", "MDP Labeler: An Interactive Multi-Object Tracking Dataset Annotation Tool", None))
        self.label_frame.setText(_translate("MDPLabler", "frame/total", None))
        self.widget_dets.headerItem().setText(0, _translate("MDPLabler", "frame", None))
        self.widget_dets.headerItem().setText(1, _translate("MDPLabler", "id", None))
        self.widget_dets.headerItem().setText(2, _translate("MDPLabler", "x", None))
        self.widget_dets.headerItem().setText(3, _translate("MDPLabler", "y", None))
        self.widget_dets.headerItem().setText(4, _translate("MDPLabler", "w", None))
        self.widget_dets.headerItem().setText(5, _translate("MDPLabler", "h", None))
        self.widget_dets.headerItem().setText(6, _translate("MDPLabler", "score", None))
        self.btn_update.setText(_translate("MDPLabler", "update model", None))
        self.btn_save_result.setText(_translate("MDPLabler", "save result", None))
        self.chbox_frame.setText(_translate("MDPLabler", "Show only present frame", None))
        self.btn_hide_all.setText(_translate("MDPLabler", "collapse all", None))
        self.btn_pause.setText(_translate("MDPLabler", "Pause", None))
        self.btn_play.setText(_translate("MDPLabler", "Play", None))
        self.btn_rewind.setText(_translate("MDPLabler", "Rewind", None))
        self.btn_prev.setText(_translate("MDPLabler", "<<", None))
        self.btn_succ.setText(_translate("MDPLabler", ">>", None))
        self.btn_newbox.setText(_translate("MDPLabler", "New Box", None))
        self.btn_out_video.setText(_translate("MDPLabler", "output video", None))
