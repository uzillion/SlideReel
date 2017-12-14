'''
~~~~~ A Photo Editor and Slideshow Maker in Python3 Using PyQt5 ~~~~~

~~~~~~~~~ Contributors: Uzair Inamdar, Jizhou Yang, Saman Porhemmat
~~~~~~~~~ All Rights Reserved
~~~~~~~~~
~~~~~~~~~ San Francisco State University
~~~~~~~~~ Course: CSC 690
~~~~~~~~~ Final Project
~~~~~~~~~ Date: Fall 2017

This script implements the Video class in which we render the video of the slideshow.
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog, QStyle, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QColor, QImage, QPainter
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from programModel import *
from PIL import ImageFilter, Image, ImageEnhance
import os, sys, time, threading, sched, requests, urllib.request, shutil
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QObject, pyqtSignal, QEvent
from threading import Timer
import cv2
import numpy as np
import io
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QBuffer

class Video(QtCore.QObject):
    def __init__(self, parent=None, *args, **kw):
        QtCore.QObject.__init__(self)
        self.parent = parent

    def output(self):
        fps, duration = 24, self.parent.duration
        p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r', '25', '-i', '-', '-vcodec', 'mpeg4', '-qscale', '5', '-r', '25', 'video.avi'], stdin=PIPE)

        c=0
        remaining = 0.00
        while remaining <= self.parent.duration:
            self.parent.horizontalSlider.setValue(remaining)
            if remaining in self.parent.prModel.durations or remaining == 0:
                if remaining != 0 and remaining != self.parent.duration and self.parent.transition == 1:
                    for transition in range(255, -1, -5):
                        temp = self.parent.imageBoard.pixmap().toImage()
                        painter = QPainter()
                        painter.begin(temp)
                        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
                        painter.fillRect(temp.rect(), QColor(0, 0, 0, transition))
                        painter.end()
                        self.parent.imageBoard.setPixmap(QPixmap.fromImage(temp))
                        self.parent.imageBoard.repaint()
                        img = self.parent.convertToImage(self.parent.imageBoard.pixmap())
                        img.save(p.stdin, 'JPEG')
                        time.sleep(0.04)

                    self.parent.img = QPixmap(self.parent.prModel.labelList[c])
                    self.parent.img = self.parent.scaleImage(self.parent.img)

                    for transition in range(0, 256, 5):
                        temp = self.parent.img.toImage()
                        painter = QPainter()
                        painter.begin(temp)
                        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
                        painter.fillRect(temp.rect(), QColor(0, 0, 0, transition))
                        painter.end()
                        self.parent.imageBoard.setPixmap(QPixmap.fromImage(temp))
                        self.parent.imageBoard.repaint()
                        img = self.parent.convertToImage(self.parent.imageBoard.pixmap())
                        img.save(p.stdin, 'JPEG')
                        time.sleep(0.04)

                else:
                    self.parent.playView(c)
                    img = self.parent.convertToImage(self.parent.imageBoard.pixmap())
                    img.save(p.stdin, 'JPEG')
                c += 1
            else:
                img = self.parent.convertToImage(self.parent.imageBoard.pixmap())
                img.save(p.stdin, 'JPEG')
            self.parent.horizontalSlider.repaint()
            remaining *= 100000.000
            remaining = round(remaining)
            print("remaining (*100000):{}".format(remaining))
            remaining += 4000.000
            print("remaining (+4000):{}".format(remaining))
            temp = remaining%4.000
            print("temp:{}".format(temp))
            remaining = remaining - temp
            remaining /= 100000.000
            print("remaining:{}".format(remaining))
            time.sleep(0.04)

        p.stdin.close()
        p.wait()
        self.parent.isPlaying = 0
        self.parent.horizontalSlider.setValue(0)
        self.parent.playButton.setIcon(self.parent.style().standardIcon(QStyle.SP_MediaPlay))
        self.parent.playView(0)
        self.parent.playButton.setEnabled(True)
