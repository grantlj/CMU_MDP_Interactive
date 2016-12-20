# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_conflict.ui'
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

class Ui_dialog_conflict(object):
    def setupUi(self, dialog_conflict):
        dialog_conflict.setObjectName(_fromUtf8("dialog_conflict"))
        dialog_conflict.resize(708, 626)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog_conflict.sizePolicy().hasHeightForWidth())
        dialog_conflict.setSizePolicy(sizePolicy)
        dialog_conflict.setMinimumSize(QtCore.QSize(708, 626))
        dialog_conflict.setMaximumSize(QtCore.QSize(708, 626))
        dialog_conflict.setStyleSheet(_fromUtf8("QLabel#view_im_a {\n"
"    border-style: outset;\n"
"    border-width: 5px;\n"
"    border-color: black;\n"
"}\n"
""))
        self.view_object_a = QtGui.QLabel(dialog_conflict)
        self.view_object_a.setGeometry(QtCore.QRect(90, 110, 241, 431))
        self.view_object_a.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.view_object_a.setMouseTracking(False)
        self.view_object_a.setFocusPolicy(QtCore.Qt.NoFocus)
        self.view_object_a.setStyleSheet(_fromUtf8("QLabel#view_object_a{\n"
"    border-style: outset;\n"
"    border-width: 5px;\n"
"    border-color: black;\n"
"}\n"
""))
        self.view_object_a.setText(_fromUtf8(""))
        self.view_object_a.setScaledContents(True)
        self.view_object_a.setObjectName(_fromUtf8("view_object_a"))
        self.view_object_b = QtGui.QLabel(dialog_conflict)
        self.view_object_b.setGeometry(QtCore.QRect(370, 110, 241, 431))
        self.view_object_b.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.view_object_b.setFocusPolicy(QtCore.Qt.NoFocus)
        self.view_object_b.setStyleSheet(_fromUtf8("QLabel#view_object_b{\n"
"    border-style: outset;\n"
"    border-width: 5px;\n"
"    border-color: black;\n"
"}\n"
""))
        self.view_object_b.setText(_fromUtf8(""))
        self.view_object_b.setScaledContents(True)
        self.view_object_b.setObjectName(_fromUtf8("view_object_b"))
        self.label_title = QtGui.QLabel(dialog_conflict)
        self.label_title.setGeometry(QtCore.QRect(70, 30, 571, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setObjectName(_fromUtf8("label_title"))
        self.btn_sel_all_a = QtGui.QPushButton(dialog_conflict)
        self.btn_sel_all_a.setGeometry(QtCore.QRect(130, 560, 151, 41))
        self.btn_sel_all_a.setObjectName(_fromUtf8("btn_sel_all_a"))
        self.btn_sel_all_b = QtGui.QPushButton(dialog_conflict)
        self.btn_sel_all_b.setGeometry(QtCore.QRect(420, 560, 150, 41))
        self.btn_sel_all_b.setObjectName(_fromUtf8("btn_sel_all_b"))
        self.btn_skip = QtGui.QPushButton(dialog_conflict)
        self.btn_skip.setGeometry(QtCore.QRect(310, 560, 81, 41))
        self.btn_skip.setObjectName(_fromUtf8("btn_skip"))
        self.label_det_a = QtGui.QLabel(dialog_conflict)
        self.label_det_a.setGeometry(QtCore.QRect(110, 80, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_det_a.setFont(font)
        self.label_det_a.setObjectName(_fromUtf8("label_det_a"))
        self.label_det_b = QtGui.QLabel(dialog_conflict)
        self.label_det_b.setGeometry(QtCore.QRect(390, 80, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_det_b.setFont(font)
        self.label_det_b.setObjectName(_fromUtf8("label_det_b"))

        self.retranslateUi(dialog_conflict)
        QtCore.QMetaObject.connectSlotsByName(dialog_conflict)

    def retranslateUi(self, dialog_conflict):
        dialog_conflict.setWindowTitle(_translate("dialog_conflict", "Dialog", None))
        self.label_title.setText(_translate("dialog_conflict", "Solve confliction in frame xxx, click on object detection to select", None))
        self.btn_sel_all_a.setText(_translate("dialog_conflict", "Merge all from tracklet A", None))
        self.btn_sel_all_b.setText(_translate("dialog_conflict", "Merge all from tracklet B", None))
        self.btn_skip.setText(_translate("dialog_conflict", "skip", None))
        self.label_det_a.setText(_translate("dialog_conflict", "Detection from tracklet A", None))
        self.label_det_b.setText(_translate("dialog_conflict", "Detection from tracklet B", None))

