#!usr/bin/python3

"""
~~~~~ A Photo Editor and Slideshow Maker in Python3 Using PyQt5 ~~~~~

~~~~~~~~~ Contributors: Uzair Inamdar, Jizhou Yang, Saman Porhemmat
~~~~~~~~~ All Rights Reserved
~~~~~~~~~
~~~~~~~~~ San Francisco State University
~~~~~~~~~ Course: CSC 690
~~~~~~~~~ Final Project
~~~~~~~~~ Date: Fall 2017

This script contains our data structures according to the MVC design pattern.
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *

class editorModel:

    # Constructor
    def __init__(self):
        super().__init__()
        self.initStructure()

    def initStructure(self):
        self.labelList = [] # Holds QLabels that are placed on the timeline
        self.timelineIsEmpty = 1 # Checking if the timeline is empty or not
        self.thumbnailLengthTracker = 0
        self.durations = []
        self.durationLabels = []
        self.audioStartTimes = []       # Start times will be stored in this list
        self.audioEndTimes = []         # End times will be stored in this
        self.audioTrackQueue = []       # A queue for audio paths to play in order
        self.imageStartTimes = []
        self.imageEndTimes = []
