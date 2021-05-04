# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/vehicle_detection.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import argparse
#import datetime
from utils import detector_utils as detector_utils
from utils.cars_in_danger_utils import *
#import pandas as pd
#from datetime import date
#import xlrd
#from xlwt import Workbook
#from xlutils.copy import copy
#import numpy as np
#import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
import cv2
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import imutils
from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--display', dest='display', type=int,
                default=1, help='Display the detected images using OpenCV. This reduces FPS')
args = vars(ap.parse_args())

detection_graph, sess = detector_utils.load_inference_graph()



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Main Window")
        MainWindow.resize(852, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 852, 480))
        self.image_label.setObjectName("image_label")
        self.image_label.setScaledContents(True)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(260, 500, 300, 106))
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pause_button = QtWidgets.QPushButton(self.widget)
        self.pause_button.setObjectName("pause_button")
        self.gridLayout_2.addWidget(self.pause_button, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        self.resume_button = QtWidgets.QPushButton(self.widget)
        self.resume_button.setObjectName("resume_button")
        self.gridLayout_2.addWidget(self.resume_button, 0, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.stop_button = QtWidgets.QPushButton(self.widget)
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.widget)
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.pause_button.clicked.connect(self.pause)
        self.resume_button.clicked.connect(self.resume)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.stop_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.label_width=852
        self.label_height=480
        self.image_label.setPixmap(QtGui.QPixmap('images/vehicle_detection2.png'))

        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("safety_distance_threshold")
        self.verticalSlider.setGeometry(650,490,20,110)
        self.verticalSlider.setSliderPosition(20)
        self.verticalSlider.valueChanged['int'].connect(self.safety_distance_value)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(630, 600, 150, 20)
        self.label.setObjectName("label")
        self.label.setScaledContents(True)
        self.label.setText('Safety Distance')

        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(690, 550, 90, 30)
        self.reset_button.setObjectName("reset_button")
        self.reset_button.setText('Default Position')
        self.reset_button.clicked.connect(self.reset_safety_distance)

        self.current_safety_distance_value=.2

    def start(self):
        self.is_kill=False
        self.is_pause=False
        self.stop_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.start_button.setEnabled(False)

        score_thresh = 0.70
        #vs = cv2.VideoCapture('test_videos/video2.mp4')
        vs = VideoStream('test_videos/video2.mp4').start()
        #self.vs =cv2.VideoCapture(0)
        while True:#(vid.isOpened()):
            if not self.is_pause:
                frame = vs.read()
                frame= np.array(frame)
                h, w, ch = frame.shape
            #    print(frame.shape)
                new_width=self.label_width
                new_height=int(h*(self.label_width/w))
                frame=imutils.resize(frame,width=new_width,height=new_height)
                h, w, ch = frame.shape
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #    print(frame.shape)
                boxes, scores, classes,num_detections = detector_utils.detect_objects(
                            frame, detection_graph, sess)

                detector_utils.draw_box_on_image(
                        int(num_detections), score_thresh, scores, boxes, classes, w, h, frame)

                cars_in_danger=finding_cars_in_danger(int(num_detections), score_thresh, scores, boxes, classes, w, h,
                                                      self.current_safety_distance_value)

                locate_cars_in_danger(cars_in_danger,frame)

                frame = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
                image=frame.scaled(w, h, Qt.KeepAspectRatio)
            self.image_label.setPixmap(QtGui.QPixmap.fromImage(image))

            key = cv2.waitKey(1) & 0xFF   ### important line
            if self.is_kill:
                break

    def stop(self):
        self.is_kill=True
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.image_label.setPixmap(QtGui.QPixmap('images/vehicle_detection2.png'))

    def pause(self):
        self.is_pause=True
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(True)
    def resume(self):
        self.is_pause=False
        self.resume_button.setEnabled(False)
        self.pause_button.setEnabled(True)

    def safety_distance_value(self,value):
        self.current_safety_distance_value=value/100
        #print(self.current_safety_distance_value)

    def reset_safety_distance(self):
        self.current_safety_distance_value=.2
        self.verticalSlider.setSliderPosition(20)

    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Vehicle Detection"))
            self.image_label.setText(_translate("MainWindow", "image"))
            self.pause_button.setText(_translate("MainWindow", "Pause"))
            self.resume_button.setText(_translate("MainWindow", "Resume"))
            self.stop_button.setText(_translate("MainWindow", "Stop"))
            self.start_button.setText(_translate("MainWindow", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())












