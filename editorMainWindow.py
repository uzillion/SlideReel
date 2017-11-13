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
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os, sys
from programModel import *

class Ui_MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.prModel = editorModel()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #Window Size
        MainWindow.resize(1024, 768)
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
        self.actionBrightness_Contrast = QtWidgets.QAction(MainWindow)
        self.actionBrightness_Contrast.setObjectName("actionBrightness_Contrast")
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
        self.menuFile.addAction(self.actionOpen_Image)
        self.menuFile.addAction(self.actionOpen_Audio_File)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose_Image)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionPreferences)
        self.menuImage.addAction(self.actionBrightness_Contrast)
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
        self.menuFilter.addAction(self.actionPhoto_Filter)
        self.menuFilter.addAction(self.actionSharpen)
        self.menuFilter.addAction(self.actionBlur)
        self.menuShare.addAction(self.actionShare_TwitterVid)
        self.menuShare.addAction(self.actionShare_TwitterImg)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuFilter.menuAction())
        self.menubar.addAction(self.menuShare.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.setNativeMenuBar(False)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.addButton = QPushButton(self.centralwidget)
        self.addButton.setText("Add")
        self.addButton.move(160, 480)
        self.addButton.clicked.connect(self.addToTimeline)
        self.displayTimeLabel = QLabel(self.centralwidget)
        self.displayTimeLabel.move(20, 485)
        self.displayTimeLabel.setText("Display time:")
        self.displayTimeBox = QLineEdit(self.centralwidget)
        self.displayTimeBox.setGeometry(QtCore.QRect(110, 485, 50, 20))
        self.totalTimeLabel = QLabel(self.centralwidget)
        self.totalTimeLabel.move(900, 685)
        self.totalTimeLabel.setText("Total time: ")
        self.createTreeView()
        self.createBoard()
        self.createTimeline()
        self.connectButtons()

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
        self.actionBrightness_Contrast.setText(_translate("MainWindow", "Brightness/Contrast..."))
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
        # When the user double clicks on an image file on the tree bar
        self.treeView.doubleClicked.connect(self.treeFileClicked)
        # Action for File->Quit
        self.actionQuit.triggered.connect(self.quitProgram)


    # This is the tree-view, which is located on the left-hand side.
    # It is our main tool to browse folders and paths.
    def createTreeView(self):
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(20, 10, 441, 461))
        self.treeView.setObjectName("treeView")
        model = QFileSystemModel()
        #model.setRootPath(str(os.getcwd()))
        model.setRootPath('')
        self.treeView.setModel(model)
        #self.treeView.setRootIndex(model.index(str(os.getcwd())))

    # This is where the selected picture is shown.
    # We create the board using a QLabel once, and then we keep updating it
    # using other functions.
    def createBoard(self):
        self.imageBoard = QLabel(self.centralwidget)
        self.imageBoard.setStyleSheet('border: 5px solid grey')
        self.imageBoard.setGeometry(QtCore.QRect(480, 7, 531, 465))
        self.imageBoard.setObjectName('imageBoard')
        self.imageBoard.setVisible(1)

    # This method creates a timeline. It is simply just a QLabel.
    def createTimeline(self):
        self.myTimeline = QLabel(self.centralwidget)
        self.myTimeline.setStyleSheet('border: 3px solid purple; background-color: #58585b')
        self.myTimeline.setGeometry(QtCore.QRect(16, 540, 994, 130))
        self.myTimeline.setObjectName('imageBoard')

    # This is the function that is executed when the user double-clicks on a filePath
    # via treeView. This function gets the path of the image file and changes the image accordingly.
    def treeFileClicked(self, signal):
        self.filePath=self.treeView.model().filePath(signal)
        try:
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap)
            self.imageBoard.setPixmap(pixmap)
            self.imageBoard.setAlignment(Qt.AlignCenter)
        except:
            print('Not an image file! Please try another file.')
        print('Clicked: ', self.filePath)

    # This method is executed when the user clicks on the add button.
    # It basically adds the image to the timeline with the picture of the image
    # appearing on the timeline.
    def addToTimeline(self):
        # Get the display length from the text box
        displayLength = int(self.displayTimeBox.text())
        # Save the duration in the below list
        self.prModel.durations.append(displayLength)
        tmp = 0
        for each in self.prModel.durations:
            tmp +=each
        self.totalTimeLabel.setText("Total time: " + str(tmp))
        if self.prModel.timelineIsEmpty == 1:
            self.myImage = QLabel(self.centralwidget)
            self.myImage.setStyleSheet('border: 3px solid green')
            # We resize the thumbnail according to display length
            self.myImage.setGeometry(QtCore.QRect(21, 545, 30+displayLength*30, 120))
            self.myImage.raise_()
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap, 30+displayLength*30, 120)
            self.myImage.setPixmap(pixmap)
            self.myImage.setAlignment(Qt.AlignCenter)
            self.myImage.setVisible(1)
            imgDuration = QLabel(self.centralwidget)
            imgDuration.setText(str(displayLength)+ 's')
            imgDuration.move(30+displayLength*30/2,685)
            imgDuration.setVisible(1)
            self.prModel.durationLabels.append(imgDuration)
            self.prModel.labelList.append(self.myImage)
            self.prModel.timelineIsEmpty = 0
            self.prModel.thumbnailLengthTracker += 30+displayLength*30 + 21
        else:
            self.myImage = QLabel(self.centralwidget)
            self.myImage.setStyleSheet('border: 3px solid green')
            # We resize the thumbnail according to display length
            self.myImage.setGeometry(QtCore.QRect(self.prModel.thumbnailLengthTracker, 545, 30+displayLength*30, 120))
            self.myImage.raise_()
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap, 30+displayLength*30, 120)
            self.myImage.setPixmap(pixmap)
            self.myImage.setAlignment(Qt.AlignCenter)
            self.myImage.setVisible(1)
            self.prModel.labelList.append(self.myImage)
            self.prModel.thumbnailLengthTracker += 30+displayLength*30
            imgDuration = QLabel(self.centralwidget)
            imgDuration.setText(str(displayLength)+ 's')
            imgDuration.setVisible(1)
            imgDuration.move(self.prModel.thumbnailLengthTracker-(30+displayLength*30/2),685)
            self.prModel.durationLabels.append(imgDuration)

    # this method scales the images based on their widths and heights
    def scaleImage(self, img, width=521, height=455):
        try:
            self.IMAGE_HEIGHT = height
            self.IMAGE_WIDTH = width
            oldHeight = img.height()
            oldWidth = img.width()
            # We need to know whether we should scale by height or width
            # This way, we can fit images correctly
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
