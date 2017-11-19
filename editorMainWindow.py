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
This piece of code handles the view. Basically, it is responsible for the
graphical user interface of the application. It is invoked by main.py.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog, QStyle, QFileDialog
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt
import os, sys, time
from programModel import *
from PIL import ImageFilter, Image, ImageEnhance
import time
import pygame
import _thread
import threading
#pip3 install pygame
#pip3 install playsound
#pip3 install -U PyObjC
from playsound import playsound

class Ui_MainWindow(QWidget):

    # Constructor
    def __init__(self):
        super().__init__()
        self.prModel = editorModel()
        self.duration = 0
        self.isPlaying = 0

    def setupUi(self, MainWindow):

        # Initiate self pixmap
        self.pixmap =QPixmap()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)     # Window size
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuImage = QtWidgets.QMenu(self.menubar)
        self.menuImage.setObjectName("menuImage")
        self.menuFilter = QtWidgets.QMenu(self.menubar)
        self.menuFilter.setObjectName("menuFilter")
        self.menuShare = QtWidgets.QMenu(self.menubar)
        self.menuShare.setObjectName("menuShare")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setAcceptDrops(False)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_Image = QtWidgets.QAction(MainWindow)
        self.actionOpen_Image.setObjectName("actionOpen_Image")
        self.actionOpen_Audio_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Audio_File.setObjectName("actionOpen_Audio_File")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionClose_Image = QtWidgets.QAction(MainWindow)
        self.actionClose_Image.setObjectName("actionClose_Image")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSelect_All = QtWidgets.QAction(MainWindow)
        self.actionSelect_All.setObjectName("actionSelect_All")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionBrightness = QtWidgets.QAction(MainWindow)
        self.actionBrightness.setObjectName("actionBrightness")
        self.actionContrast = QtWidgets.QAction(MainWindow)
        self.actionContrast.setObjectName("actionContrast")
        self.actionExposure = QtWidgets.QAction(MainWindow)
        self.actionExposure.setObjectName("actionExposure")
        self.actionVibrance = QtWidgets.QAction(MainWindow)
        self.actionVibrance.setObjectName("actionVibrance")
        self.actionHue_Saturation = QtWidgets.QAction(MainWindow)
        self.actionHue_Saturation.setObjectName("actionHue_Saturation")
        self.actionColor_Balance = QtWidgets.QAction(MainWindow)
        self.actionColor_Balance.setObjectName("actionColor_Balance")
        self.actionBlack_White = QtWidgets.QAction(MainWindow)
        self.actionBlack_White.setObjectName("actionBlack_White")
        self.actionResize = QtWidgets.QAction(MainWindow)
        self.actionResize.setObjectName("actionResize")
        self.actionCrop = QtWidgets.QAction(MainWindow)
        self.actionCrop.setObjectName("actionCrop")
        self.actionPhoto_Filter = QtWidgets.QAction(MainWindow)
        self.actionPhoto_Filter.setObjectName("actionPhoto_Filter")
        self.actionSharpen = QtWidgets.QAction(MainWindow)
        self.actionSharpen.setObjectName("actionSharpen")
        self.actionBlur = QtWidgets.QAction(MainWindow)
        self.actionBlur.setObjectName("actionBlur")
        self.actionShare_TwitterVid = QtWidgets.QAction(MainWindow)
        self.actionBlur.setObjectName("actionShare_TwitterVid")
        self.actionShare_TwitterImg = QtWidgets.QAction(MainWindow)
        self.actionBlur.setObjectName("actionShare_TwitterImg")

        # Adding action for the item under the File menu
        self.menuFile.addAction(self.actionOpen_Image)
        self.menuFile.addAction(self.actionOpen_Audio_File)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose_Image)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        # Adding action for the item under the Edit menu
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionPreferences)

        # Adding action for the item under the Image menu
        self.menuImage.addAction(self.actionBrightness)
        self.menuImage.addAction(self.actionContrast)
        self.menuImage.addAction(self.actionExposure)
        self.menuImage.addSeparator()
        self.menuImage.addAction(self.actionVibrance)
        self.menuImage.addAction(self.actionHue_Saturation)
        self.menuImage.addSeparator()
        self.menuImage.addAction(self.actionColor_Balance)
        self.menuImage.addAction(self.actionBlack_White)
        self.menuImage.addSeparator()
        self.menuImage.addAction(self.actionResize)
        self.menuImage.addAction(self.actionCrop)

        # Adding action for the item under the Filter menu
        self.menuFilter.addAction(self.actionPhoto_Filter)
        self.menuFilter.addAction(self.actionSharpen)
        self.menuFilter.addAction(self.actionBlur)

        # Adding action for the item under the Share menu
        self.menuShare.addAction(self.actionShare_TwitterVid)
        self.menuShare.addAction(self.actionShare_TwitterImg)

        # Adding action for the actual menubar
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuFilter.menuAction())
        self.menubar.addAction(self.menuShare.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.setNativeMenuBar(False)

        # Setting the names of the items of menubar
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Creating the add button.
        # This button is responsible to add images to the timeline
        self.addButton = QPushButton(self.centralwidget)
        self.addButton.setText("Add Image")
        self.addButton.move(160, 480)

        # Creating the add_audio button.
        # This button is responsible to add images to the timeline
        self.addAudioButton = QPushButton(self.centralwidget)
        self.addAudioButton.setText("Add Audio")
        self.addAudioButton.move(290, 705)

        # Creating the play button.
        # When the user clicks on this button, all the images with their
        # respective durations should be shown and played.
        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.move(745.5, 480)

        # Creating the play button.
        # When the user clicks on this button, all the images with their
        # respective durations should be shown and played.
        self.playAudioButton = QPushButton(self.centralwidget)
        self.playAudioButton.setEnabled(True)
        self.playAudioButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playAudioButton.move(390, 705)

        # Creating the display time label.
        # This label is used to just describe the textbox lcoated next to it.
        self.displayTimeLabel = QLabel(self.centralwidget)
        self.displayTimeLabel.move(20, 485)
        self.displayTimeLabel.setText("Display time:")
        self.displayTimeBox = QLineEdit(self.centralwidget)
        self.displayTimeBox.setGeometry(QtCore.QRect(110, 485, 50, 20))

        # Creating Start time labels and text boxes for Images
        self.imgStartTimeLabel = QLabel(self.centralwidget)
        self.imgStartTimeLabel.move(280, 485)
        self.imgStartTimeLabel.setText("Start time:")
        self.imgStartTimeBox = QLineEdit(self.centralwidget)
        self.imgStartTimeBox.setGeometry(QtCore.QRect(350, 485, 50, 20))

        # Creating End time labels and text boxes for Images
        self.imgEndTimeLabel = QLabel(self.centralwidget)
        self.imgEndTimeLabel.move(410, 485)
        self.imgEndTimeLabel.setText("End time:")
        self.imgEndTimeBox = QLineEdit(self.centralwidget)
        self.imgEndTimeBox.setGeometry(QtCore.QRect(470, 485, 50, 20))

        # Creating Start time labels and text boxes for audio files
        self.audioStartTimeLabel = QLabel(self.centralwidget)
        self.audioStartTimeLabel.move(20, 709)
        self.audioStartTimeLabel.setText("Start time:")
        self.audioStartTimeBox = QLineEdit(self.centralwidget)
        self.audioStartTimeBox.setGeometry(QtCore.QRect(90, 709, 50, 20))

        # Creating End time labels and text boxes for audio files
        self.audioEndTimeLabel = QLabel(self.centralwidget)
        self.audioEndTimeLabel.move(170, 709)
        self.audioEndTimeLabel.setText("End time:")
        self.audioEndTimeBox = QLineEdit(self.centralwidget)
        self.audioEndTimeBox.setGeometry(QtCore.QRect(240, 709, 50, 20))

        # This is the Total Time label.
        # We need to show the total time of the slideshow using this label.
        self.totalTimeLabel = QLabel(self.centralwidget)
        self.totalTimeLabel.move(900, 710)
        self.totalTimeLabel.setText("Total time: ")
        self.durationLabel = QLabel(self.centralwidget)
        self.durationLabel.move(970, 710)
        self.durationLabel.setText("0")
        self.durationLabel.setFixedWidth(20)

        self.createTimeline()
        self.createAudioTimeline()
        self.createSlider()
        self.myImage = QLabel(self.centralwidget)
        self.myAudio = QLabel(self.centralwidget)
        self.createTreeView()
        self.createBoard()
        self.connectButtons()
    
        # pixel positions for crop
        self.startpos = [0, 0]
        self.endpos = [0, 0]
        self.isCropOn = False

    def play(self):
        changeList = []
        changeList.append(0)
        total = 0
        c = 0
        print(self.duration)
        # self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.playButton.setEnabled(False)
        self.isPlaying = 1
        for durations in self.prModel.durations:
            changeList.append(total + durations)
            total = changeList[len(changeList)-1]
        changeList.pop()
        # self.animation.setDuration(self.duration*1000)
        # self.animation.updateState(self.update)
        # self.animation.setEndValue(self.horizontalSlider.setValue(self.duration))
        # self.animation.start()
        for remaining in range(0, self.duration+1, 1):
            # sys.stdout.write("\r")
            # sys.stdout.write("{:2d}".format(remaining))
            # sys.stdout.flush()
            self.horizontalSlider.setValue(remaining)
            if remaining in changeList:
                self.playView(c)
                c += 1
            self.horizontalSlider.repaint()
            time.sleep(1)
        self.isPlaying = 0
        self.horizontalSlider.setValue(0)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playView(0)
        self.playButton.setEnabled(True)


    def getValue(self):
        print(self.horizontalSlider.value())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Editor & Slideshow maker"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuImage.setTitle(_translate("MainWindow", "Image"))
        self.menuFilter.setTitle(_translate("MainWindow", "Filter"))
        self.menuShare.setTitle(_translate("MainWindow", "Share"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen_Image.setText(_translate("MainWindow", "Open Image..."))
        self.actionOpen_Audio_File.setText(_translate("MainWindow", "Open Audio File..."))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionClose_Image.setText(_translate("MainWindow", "Close Image"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionSelect_All.setText(_translate("MainWindow", "Select All"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences..."))
        self.actionBrightness.setText(_translate("MainWindow", "Brightness..."))
        self.actionContrast.setText(_translate("MainWindow", "Contrast..."))
        self.actionExposure.setText(_translate("MainWindow", "Exposure..."))
        self.actionVibrance.setText(_translate("MainWindow", "Vibrance..."))
        self.actionHue_Saturation.setText(_translate("MainWindow", "Hue/Saturation..."))
        self.actionColor_Balance.setText(_translate("MainWindow", "Color Balance..."))
        self.actionBlack_White.setText(_translate("MainWindow", "Black & White"))
        self.actionResize.setText(_translate("MainWindow", "Resize..."))
        self.actionCrop.setText(_translate("MainWindow", "Crop..."))
        self.actionPhoto_Filter.setText(_translate("MainWindow", "Photo Filter..."))
        self.actionSharpen.setText(_translate("MainWindow", "Sharpen..."))
        self.actionBlur.setText(_translate("MainWindow", "Blur..."))
        self.actionShare_TwitterVid.setText(_translate("MainWindow", "Share Video on Twitter"))
        self.actionShare_TwitterImg.setText(_translate("MainWindow", "Share Image on Twitter"))

    def connectButtons(self):
        self.treeView.doubleClicked.connect(self.treeFileClicked)          # Action for double-clicking images
        self.actionQuit.triggered.connect(self.quitProgram)                # Action for Quit
        self.playButton.clicked.connect(self.play)                         # Action for Play Button
        self.playAudioButton.clicked.connect(self.playSound)               # Action for Play Audio Button
        self.addButton.clicked.connect(self.addd)                 # Action for adding images to timeline
        self.addAudioButton.clicked.connect(self.addAudioToTimeline)       # Action for adding audio files to timeline
        self.actionBrightness.triggered.connect(self.change_brightness)    # Action for brightness
        self.actionContrast.triggered.connect(self.change_contrast)        # Action for contrast
        self.actionHue_Saturation.triggered.connect(self.change_saturation)# Action for saturation
        self.actionBlack_White.triggered.connect(self.blackwhite)          # Action for black and white
        self.actionBlur.triggered.connect(self.blur)                       # Action to blur the image
        self.actionSharpen.triggered.connect(self.sharpen)                 # Action to sharpen the image
        self.actionOpen_Audio_File.triggered.connect(self.importAudio)     # Action for Open Audio...
        self.actionOpen_Image.triggered.connect(self.importImage)          # Action for Open Image...
        self.actionSharpen.triggered.connect(self.sharpen)                 # Action to sharpen the image
        self.actionColor_Balance.triggered.connect(self.balance)           # Action to color balance
        self.actionResize.triggered.connect(self.myresize)                 # Action to resize image
        self.actionSave.triggered.connect(self.savefile)                   # Action to save image
        self.actionCrop.triggered.connect(self.cropimg)                    # Action to crop image

    # This is the tree-view, which is located on the left-hand side.
    # It is our main tool to browse folders and paths.
    def createTreeView(self):
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(20, 10, 441, 461))
        self.treeView.setObjectName("treeView")
        model = QFileSystemModel()
        model.setRootPath('')
        self.treeView.setModel(model)

    # This is where the selected picture is shown.
    # We create the board using a QLabel once, and then we keep updating it
    # using other functions.
    def createBoard(self):
        self.imageBoard = QLabel(self.centralwidget)
        self.imageBoard.setStyleSheet('border: 5px solid grey')
        self.imageBoard.setGeometry(QtCore.QRect(480, 7, 531, 465))
        self.imageBoard.setObjectName('imageBoard')
        self.imageBoard.setVisible(1)
    # connect the imageBoard with mouse click event for crop
        self.imageBoard.mousePressEvent = self.mclick1
        self.imageBoard.mouseReleaseEvent = self.mrelease1

    # This is our timeline, where we place images on.
    # We are using a QFrame to imitate the feeling of an actual timeline.
    def createTimeline(self):
        self.timeline = QtWidgets.QFrame(self.centralwidget)
        self.timeline.setGeometry(QtCore.QRect(16, 512, 994, 130))
        self.timeline.setStyleSheet("background-color: rgb(186, 186, 186)")
        self.timeline.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.timeline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.timeline.setObjectName("Timeline")

    # This is our timeline for the audio QFileSystemModel
    # We are using a QFrame as well.
    def createAudioTimeline(self):
        self.audiotimeline = QtWidgets.QFrame(self.centralwidget)
        self.audiotimeline.setGeometry(QtCore.QRect(16, 655, 994, 50))
        self.audiotimeline.setStyleSheet("background-color: rgb(186, 186, 186)")
        self.audiotimeline.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.audiotimeline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.audiotimeline.setObjectName("audioTimeline")

    # This is the slider located on the timeline.
    # We use it to track the duration of images when they are being played.
    def createSlider(self):
        self.horizontalSlider = QtWidgets.QSlider(self.timeline)
        self.horizontalSlider.setCursor(Qt.SizeHorCursor)
        self.horizontalSlider.setGeometry(QtCore.QRect(0, 0, 997, 40))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setRange(0,60)
        self.animation = QPropertyAnimation(self.horizontalSlider)
        self.animation.setStartValue(self.horizontalSlider.minimum())
        # self.horizontalSlider.sliderMoved.connect(self.getValue)

    def playView(self, imgIndex):
        self.img = QPixmap(self.prModel.labelList[imgIndex])
        self.img = self.scaleImage(self.img)
        self.imageBoard.setPixmap(self.img)
        self.imageBoard.setAlignment(Qt.AlignCenter)

    # This is the function that is executed when the user double-clicks on a filePath
    # via treeView. This function gets the path of the image file and changes the image accordingly.
    def treeFileClicked(self, signal):
        self.filePath=self.treeView.model().filePath(signal)
        try:
            self.pixmap = QPixmap(self.filePath)
            self.pixmap = self.scaleImage(self.pixmap)
            self.imageBoard.setPixmap(self.pixmap)
            self.imageBoard.setAlignment(Qt.AlignCenter)
        except:
            print('Not an image file! Please try another file.')
        print('Clicked: ', self.filePath)

    # This method is executed when the user clicks on the add button.
    # It basically adds the image to the timeline with the picture of the image
    # appearing on the timeline.
    def addd(self):
        if self.prModel.timelineIsEmpty == 1:
            startTime = int(self.imgStartTimeBox.text())
            endTime = int(self.imgEndTimeBox.text())
            displayLength = endTime - startTime
            imgProp = ((displayLength/60)*985)
            self.myImage.setGeometry(QtCore.QRect(16.41*(startTime+1), 550, imgProp, 85))
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap, imgProp, 85)
            self.myImage.setPixmap(pixmap)
            self.myImage.setAlignment(Qt.AlignCenter)
            #self.myImage.setStyleSheet('border: 3px solid green')
            self.myImage.setVisible(1)
            self.prModel.timelineIsEmpty = 0
            self.prModel.thumbnailLengthTracker += imgProp + 16.41
            imgDuration = QLabel(self.centralwidget)
            imgDuration.setText(str(displayLength)+ 's')
            imgDuration.move(imgProp/2,685)
            #imgDuration.setVisible(1)
        else:
            startTime = int(self.imgStartTimeBox.text())
            endTime = int(self.imgEndTimeBox.text())
            displayLength = endTime - startTime
            imgProp = ((displayLength/60)*985)
            self.myImage = QLabel(self.centralwidget)
            #self.myImage.setStyleSheet('border: 3px solid green')
            # We resize the thumbnail according to display length
            self.myImage.setGeometry(QtCore.QRect(16.41*(startTime+1), 550, imgProp, 85))
            self.myImage.raise_()
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap, imgProp, 85)
            self.myImage.setPixmap(pixmap)
            self.myImage.setAlignment(Qt.AlignCenter)
            self.myImage.setVisible(1)
            self.prModel.thumbnailLengthTracker += imgProp
            imgDuration = QLabel(self.centralwidget)
            imgDuration.setText(str(displayLength)+ 's')
            #imgDuration.setVisible(1)
            imgDuration.move(self.prModel.thumbnailLengthTracker-(imgProp/2),685)

        self.prModel.labelList.append(self.filePath)
        self.prModel.durationLabels.append(endTime - startTime)


    def addToTimeline(self):
        # Get the display length from the text box
        displayLength = int(self.displayTimeBox.text())
        imgProp = ((displayLength/60)*985)

        # Save the duration in the below list
        self.prModel.durations.append(displayLength)
        self.duration += displayLength
        self.durationLabel.setText(str(self.duration))
        if self.prModel.timelineIsEmpty == 1:
            imgProp = ((displayLength/60)*985)
            self.myImage.setGeometry(QtCore.QRect(21, 580, imgProp, 85))
            # self.myImage.raise_()
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap, imgProp, 85)
            self.myImage.setPixmap(pixmap)
            self.myImage.setAlignment(Qt.AlignCenter)
            #self.myImage.setStyleSheet('border: 3px solid green')
            self.myImage.setVisible(1)
            imgDuration = QLabel(self.centralwidget)
            imgDuration.setText(str(displayLength)+ 's')
            imgDuration.move(imgProp/2,685)
            imgDuration.setVisible(1)
            #self.prModel.durationLabels.append(imgDuration)
            #self.prModel.labelList.append(self.myImage)
            self.prModel.timelineIsEmpty = 0
            self.prModel.thumbnailLengthTracker += imgProp + 21
        else:
            self.myImage = QLabel(self.centralwidget)
            #self.myImage.setStyleSheet('border: 3px solid green')
            # We resize the thumbnail according to display length
            self.myImage.setGeometry(QtCore.QRect(self.prModel.thumbnailLengthTracker, 580, imgProp, 85))
            self.myImage.raise_()
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap, imgProp, 85)
            self.myImage.setPixmap(pixmap)
            self.myImage.setAlignment(Qt.AlignCenter)
            self.myImage.setVisible(1)
            #self.prModel.labelList.append(self.myImage)
            self.prModel.thumbnailLengthTracker += imgProp
            imgDuration = QLabel(self.centralwidget)
            imgDuration.setText(str(displayLength)+ 's')
            imgDuration.setVisible(1)
            imgDuration.move(self.prModel.thumbnailLengthTracker-(imgProp/2),685)
            #self.prModel.durationLabels.append(imgDuration)

        self.prModel.labelList.append(self.filePath)
        self.prModel.durationLabels.append(imgDuration)

    # This method scales the images based on their widths and heights
    def scaleImage(self, img, width=521, height=455):
        try:
            self.IMAGE_HEIGHT = height
            self.IMAGE_WIDTH = width
            oldHeight = img.height()
            oldWidth = img.width()
            # We need to know whether we should scale by height or width.
            # This way, we can fit images correctly.
            if (oldHeight > oldWidth):
                newWidth = (self.IMAGE_HEIGHT * oldWidth) / oldHeight
                temp = img.scaled(newWidth, self.IMAGE_HEIGHT)
                return temp
            else:
                newHeight = (self.IMAGE_WIDTH * oldHeight) / oldWidth
                temp = img.scaled(self.IMAGE_WIDTH, newHeight)
                return temp
        except:
            print('Unable to scale the image. Program is exiting now...')
            sys.exit()

    def quitProgram(self):
        choice = QMessageBox.question(self, 'Exit', "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            print('Application closed successfully.')
            sys.exit()

    def importAudio(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.audioPath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;mp3 Files (*.mp3);;WMA Files (*.wma);;WAVE Files (*.wave)", options=options)
        if self.audioPath:
            print(self.audioPath)

    def addAudioToTimeline(self):
        if self.prModel.timelineIsEmpty == 1:
            startTime = int(self.audioStartTimeBox.text())
            endTime = int(self.audioEndTimeBox.text())
            displayLength = endTime - startTime
            imgProp = ((displayLength/60)*985)
            self.myAudio.setGeometry(QtCore.QRect(16.41*(startTime+1), 656, imgProp, 48))
            self.myAudio.setAlignment(Qt.AlignCenter)
            self.myAudio.setStyleSheet('border: 2px solid red')
            self.myAudio.setText(str(self.audioPath))
            self.myAudio.setVisible(1)
            self.prModel.timelineIsEmpty = 0
            self.prModel.thumbnailLengthTracker += imgProp + 16.41
        else:
            startTime = int(self.audioStartTimeBox.text())
            endTime = int(self.audioEndTimeBox.text())
            displayLength = endTime - startTime
            imgProp = ((displayLength/60)*985)
            self.myAudio = QLabel(self.centralwidget)
            self.myAudio.setStyleSheet('border: 2px solid red')
            self.myAudio.setGeometry(QtCore.QRect(16.41*(startTime+1), 656, imgProp, 48))
            self.myAudio.setText(str(self.audioPath))
            self.myAudio.setAlignment(Qt.AlignCenter)
            self.myAudio.setVisible(1)
            self.prModel.thumbnailLengthTracker += imgProp

    def playSound(self):
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(self.audioPath))
        self.sound.setLoopCount(QSoundEffect.Infinite)
        self.sound.play()
        start_time=time.time()
        end_time = start_time + 5
        #while True:
        #    if time.time() == end_time:
        #        break
        #while time.time() < start_time + 5:
        #    pass
        #self.sound.stop()
        #playsound(self.audioPath, block = False)
        #playsound(None)

        #pygame.init()
        #pygame.mixer.init()
        #sounda= pygame.mixer.Sound(self.audioPath)
        #sounda.play()

    def importImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imgPath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;jpg Files (*.jpg);;jpeg Files (*.jpeg);;bmp Files (*.bmp)", options=options)
        if imgPath:
            print(imgPath)
            self.filePath = imgPath
        try:
            self.pixmap = QPixmap(imgPath)
            self.pixmap = self.scaleImage(self.pixmap)
            self.imageBoard.setPixmap(self.pixmap)
            self.imageBoard.setAlignment(Qt.AlignCenter)
        except:
            print('Not an image file! Please try another file.')

    # adjust brightness UI dialog
    def change_brightness(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter brightness value (-255 ~ 255):')
        if ok:
            self.change_brightness_core(float(text))

    # adjust brightness core function
    def change_brightness_core(self, level):
        self.img = self.pixmap.toImage()
        for x in range(self.img.width()):
            for y in range(self.img.height()):
                color = QColor(self.img.pixel(x, y))
                r = self.truncate(color.red() + level)
                g = self.truncate(color.green() + level)
                b = self.truncate(color.blue() + level)
                self.img.setPixelColor(x, y, QColor(r, g, b))
        self.pixmap.convertFromImage(self.img)
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)

    # adjust saturation UI dialog
    def change_saturation(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter saturation value (-1.0, 0, 0.5, ...):')
        if ok:
            self.change_saturation_core(float(text))

    # adjust saturation core function
    def change_saturation_core(self, level):
        self.pixmap.save('temp/temp.png')
        self.img = Image.open('temp/temp.png')
        converter = ImageEnhance.Color(self.img)
        img2 = converter.enhance(level)
        img2.save('temp/temp.png')
        self.pixmap = QPixmap('temp/temp.png')
        os.remove('temp/temp.png')
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)

    # adjust contrast UI dialog
    def change_contrast(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter contrast value (-255 ~ 255):')
        if ok:
            self.change_contrast_core(float(text))

    # adjust contrast core function
    def change_contrast_core(self, level):
        self.img = self.pixmap.toImage()
        factor = float((259 * (level + 255)) / (255 * (259 - level)))
        for x in range(self.img.width()):
            for y in range(self.img.height()):
                color = QColor(self.img.pixel(x, y))
    #                print(factor * (color.red()-128) + 128)
                r = self.truncate(factor * (color.red()-128) + 128)
                g = self.truncate(factor * (color.green()-128) + 128)
                b = self.truncate(factor * (color.blue()-128) + 128)
                self.img.setPixelColor(x, y, QColor(r, g, b))
        self.pixmap.convertFromImage(self.img)
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)

    # change to black and white UI dialog
    def blackwhite(self):
        choice = QMessageBox.question(self, 'Cancel', "Change image to black and white?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.blackwhite_core()

    # change image to black and white
    def blackwhite_core(self):
        self.img = self.pixmap.toImage()
        for x in range(self.img.width()):
            for y in range(self.img.height()):
                color = QColor(self.img.pixel(x, y))
                gray = 0.2989 * color.red() + 0.5870 * color.green() + 0.1140 * color.blue()
                if gray > 120:   # may need to update 100
                    self.img.setPixelColor(x, y, QColor(255, 255, 255))
                else:
                    self.img.setPixelColor(x, y, QColor(0, 0, 0))
        self.pixmap.convertFromImage(self.img)
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)

    # truncate color values >255 or <0
    def truncate(self, color):
        if color < 0:
            return 0
        elif color > 255:
            return 255
        else:
            return int(color)

    # blur image UI dialog
    def blur(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter a value for blur degree :')
        if ok:
            self.blur_core(float(text))

    # blur image core function
    def blur_core(self, radi):
        self.pixmap.save('temp/temp.png')
        self.img = Image.open('temp/temp.png')
        self.img = self.img.filter(ImageFilter.GaussianBlur(radius=radi))
        self.img.save('temp/temp.png')
        self.pixmap = QPixmap('temp/temp.png')
        os.remove('temp/temp.png')
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)

    # sharpen the image UI dialog
    def sharpen(self):
        choice = QMessageBox.question(self, 'Cancel', "Sharpen the image?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.sharpen_core()

    # sharpen the image core function
    def sharpen_core(self):
        level = 2.0    # default level for sharpen the image
        self.pixmap.save('temp/temp.png')
        self.img = Image.open('temp/temp.png')
        enhancer = ImageEnhance.Sharpness(self.img)
        self.img = enhancer.enhance(level)
        self.img.save('temp/temp.png') 
        self.pixmap = QPixmap('temp/temp.png') 
        os.remove('temp/temp.png')  
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)       
        
    # adjust color balance
    def balance(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter balance value (0.0 ~ 1.0):')
        if ok:
            self.balance_core(float(text))       

    # color balance core function
    def balance_core(self, level):
        self.pixmap.save('temp/temp.png')
        self.img = Image.open('temp/temp.png')
        enhancer = ImageEnhance.Color(self.img)
        self.img = enhancer.enhance(level)
        self.img.save('temp/temp.png') 
        self.pixmap = QPixmap('temp/temp.png') 
        os.remove('temp/temp.png')  
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)     

    # resize iamge UI dialog
    def myresize(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter a new width (1-512px):')
        if ok:
            self.myresize_core(float(text))       

    # resize core function
    def myresize_core(self, width):
        self.pixmap = self.pixmap.scaledToWidth(width)
        self.imageBoard.setPixmap(self.pixmap)
        self.imageBoard.setAlignment(Qt.AlignCenter)    

    # save file UI dialog    
    def savefile(self):
        choice = QMessageBox.question(self, 'Cancel', "Save and overwrite the image?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.save_core()        

    # save file core function
    def save_core(self):
        self.pixmap.save(self.filePath)

    # crop function
    def cropimg(self):
        self.isCropOn = True
        QApplication.setOverrideCursor(Qt.CrossCursor)

    # mouse click event to record start position for crop
    def mclick1(self, event):
        self.startpos[0] = event.pos().x()
        self.startpos[1] = event.pos().y()

    # mouse release event to record end position for crop
    def mrelease1(self, event):
        if not self.isCropOn:
            return
        self.endpos[0] = event.pos().x()
        self.endpos[1] = event.pos().y()
        # crop the image
        cropped = self.pixmap.copy(self.startpos[0], self.startpos[1], self.endpos[0], self.endpos[1])
        self.imageBoard.setPixmap(cropped)
        self.imageBoard.setAlignment(Qt.AlignCenter)
        self.isCropOn = False
        QApplication.restoreOverrideCursor()



