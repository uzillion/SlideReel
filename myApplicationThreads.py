'''
~~~~~ A Photo Editor and Slideshow Maker in Python3 Using PyQt5 ~~~~~

~~~~~~~~~ Contributors: Uzair Inamdar, Jizhou Yang, Saman Porhemmat
~~~~~~~~~ All Rights Reserved
~~~~~~~~~
~~~~~~~~~ San Francisco State University
~~~~~~~~~ Course: CSC 690
~~~~~~~~~ Final Project
~~~~~~~~~ Date: Fall 2017

This script contains our thread classes for handling the playback of audio and images.
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

class audioThread(QtCore.QObject):

    newData  = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, *args, **kw):
        QtCore.QObject.__init__(self)
        self.myInit(*args, **kw)

    def playSound(self):
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(self.pathOfTheAudio))
        self.sound.setLoopCount(1)
        self.sound.play()

    def myInit(self, path):
        self.pathOfTheAudio = path


class audioHandlingThread(QtCore.QObject):

    newData  = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, *args, **kw):
        QtCore.QObject.__init__(self)
        self.myInit(*args, **kw)

    def playAudioTracks(self):
        for i in range(len(self.startTimes)):
            if i==0:
                self.thread1 = QtCore.QThread()
                self.smp = audioThread(self, self.audioQueue[i])
                self.smp.moveToThread(self.thread1)
                self.thread1.started.connect(self.smp.playSound)
                self.thread1.start()
                time.sleep(self.endTimes[i] - self.startTimes[i])
                self.thread1.terminate()
            else:
                timeDifference = self.startTimes[i] - self.endTimes[i-1]
                cwd = os.getcwd()
                silentSoundPath = cwd + "/" + "silence.wav"
                self.thread2 = QtCore.QThread()
                self.smp = audioThread(self, silentSoundPath)
                self.smp.moveToThread(self.thread2)
                self.thread2.started.connect(self.smp.playSound)
                self.thread2.start()
                time.sleep(timeDifference)
                self.thread2.terminate()
                self.thread1 = QtCore.QThread()
                self.smp = audioThread(self, self.audioQueue[i])
                self.smp.moveToThread(self.thread1)
                self.thread1.started.connect(self.smp.playSound)
                self.thread1.start()
                time.sleep(self.endTimes[i] - self.startTimes[i])
                self.thread1.terminate()

    def playSound(self):
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(self.pathOfTheAudio))
        self.sound.setLoopCount(1)
        self.sound.play()

    def myInit(self, path, strtList, endList, queue):
        self.pathOfTheAudio = path
        self.startTimes = strtList
        self.endTimes = endList
        self.audioQueue = queue


class imageThread(QtCore.QObject):
    data = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, *args, **kw):
        QtCore.QObject.__init__(self)

    def playSlides(self, parent):
        c=0
        for remaining in range(0, parent.duration+1, 1):
            parent.horizontalSlider.setValue(remaining)
            print(remaining)
            if remaining in parent.prModel.durations or remaining == 0:
                if remaining != 0 and remaining != parent.duration and parent.transition == 1:
                    for transition in range(255, -1, -5):
                        temp = parent.imageBoard.pixmap().toImage()
                        p = QPainter()
                        p.begin(temp)
                        p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
                        p.fillRect(temp.rect(), QColor(0, 0, 0, transition))
                        p.end()
                        parent.imageBoard.setPixmap(QPixmap.fromImage(temp))
                        parent.imageBoard.repaint()
                        time.sleep(1/24)

                    parent.img = QPixmap(parent.prModel.labelList[c])
                    parent.img = parent.scaleImage(parent.img)

                    for transition in range(0, 256, 5):
                        temp = parent.img.toImage()
                        p = QPainter()
                        p.begin(temp)
                        p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
                        p.fillRect(temp.rect(), QColor(0, 0, 0, transition))
                        p.end()
                        parent.imageBoard.setPixmap(QPixmap.fromImage(temp))
                        parent.imageBoard.repaint()
                        time.sleep(1/24)

                else:
                    parent.playView(c)
                c += 1
            parent.horizontalSlider.repaint()
            time.sleep(1)

        parent.isPlaying = 0
        parent.horizontalSlider.setValue(0)
        parent.playButton.setIcon(parent.style().standardIcon(QStyle.SP_MediaPlay))
        parent.playView(0)
        parent.playButton.setEnabled(True)
