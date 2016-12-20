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
        MDPLabler.resize(1024, 900)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MDPLabler.sizePolicy().hasHeightForWidth())
        MDPLabler.setSizePolicy(sizePolicy)
        MDPLabler.setMinimumSize(QtCore.QSize(1024, 900))
        MDPLabler.setMaximumSize(QtCore.QSize(1280, 1024))
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
        MDPLabler.setCentralWidget(self.centralwidget)

        self.retranslateUi(MDPLabler)
        QtCore.QMetaObject.connectSlotsByName(MDPLabler)

    def retranslateUi(self, MDPLabler):
        MDPLabler.setWindowTitle(_translate("MDPLabler", "MainWindow", None))
        self.label.setText(_translate("MDPLabler", "Dataset path:", None))
        self.box_dataset_path.setPlainText(_translate("MDPLabler", "Please choose a valid dataset folder to start annotation...", None))
        self.btn_choose_dataset.setText(_translate("MDPLabler", "...", None))
        self.label_frame.setText(_translate("MDPLabler", "frame/total", None))
        self.btn_pause.setText(_translate("MDPLabler", "Pause", None))
        self.btn_play.setText(_translate("MDPLabler", "Play", None))
        self.btn_rewind.setText(_translate("MDPLabler", "Rewind", None))
        self.btn_prev.setText(_translate("MDPLabler", "<<", None))
        self.btn_succ.setText(_translate("MDPLabler", ">>", None))

