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
This piece of code handles the view. Basically, it is responsible primarily for the
graphical user interface of the application. It is invoked by main.py.
"""
import os, sys, time, threading, sched, requests, urllib.request, shutil, io, cv2, wave
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog, QStyle, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QColor, QImage, QPainter
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from programModel import *
from PIL import ImageFilter, Image, ImageEnhance
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QObject, pyqtSignal, QEvent
from threading import Timer
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QBuffer
from subprocess import Popen, PIPE
from social.share import *
from myApplicationThreads import *
from myVideoHandler import *
#pip3 install pygame
#pip3 install playsound
#pip3 install -U PyObjC

class Ui_MainWindow(QWidget):

    # Constructor
    def __init__(self):
        super().__init__()
        self.prModel = editorModel()
        self.duration = 0
        self.isPlaying = 0
        self.transition = 1
        twitter = Twitter()
        facebook = Facebook()

    def setupUi(self, MainWindow):
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
        self.actionShare_TwitterVid.setObjectName("actionShare_TwitterVid")
        self.actionShare_TwitterImg = QtWidgets.QAction(MainWindow)
        self.actionShare_TwitterImg.setObjectName("actionShare_TwitterImg")
        self.actionShare_FacebookVid = QtWidgets.QAction(MainWindow)
        self.actionShare_FacebookVid.setObjectName("actionShare_FacebookVid")
        self.actionShare_FacebookImg = QtWidgets.QAction(MainWindow)
        self.actionShare_FacebookImg.setObjectName("actionShare_FacebookImg")

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
        self.menuShare.addAction(self.actionShare_FacebookVid)
        self.menuShare.addAction(self.actionShare_FacebookImg)

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
        self.addButton.setGeometry(QtCore.QRect(17, 480, 100, 22))
        self.addButton.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #ec8722")

        # Creating the add_audio button.
        # This button is responsible to add images to the timeline
        self.addAudioButton = QPushButton(self.centralwidget)
        self.addAudioButton.setText("Add Audio")
        self.addAudioButton.setGeometry(QtCore.QRect(17, 713, 100, 22))
        self.addAudioButton.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #ec8722")

        # Creating the play button.
        # When the user clicks on this button, all the images with their
        # respective durations should be shown and played.
        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setGeometry(QtCore.QRect(823, 480, 50, 22))
        self.playButton.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #ec8722")
        #self.playButton.move(745.5, 480)

        self.makeMovieButton = QPushButton(self.centralwidget)
        self.makeMovieButton.setEnabled(True)
        self.makeMovieButton.setText("Render Video")
        self.makeMovieButton.setGeometry(QtCore.QRect(880, 480, 130, 22))
        self.makeMovieButton.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #ec8722")

        # Creating Start time labels and text boxes for Images
        self.imgStartTimeLabel = QLabel(self.centralwidget)
        self.imgStartTimeLabel.move(150, 483)
        self.imgStartTimeLabel.setText("Start time:")
        self.imgStartTimeBox = QLineEdit(self.centralwidget)
        self.imgStartTimeBox.setGeometry(QtCore.QRect(220, 480, 50, 24))
        self.imgStartTimeBox.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #2a84e5")

        # Creating End time labels and text boxes for Images
        self.imgEndTimeLabel = QLabel(self.centralwidget)
        self.imgEndTimeLabel.move(280, 483)
        self.imgEndTimeLabel.setText("End time:")
        self.imgEndTimeBox = QLineEdit(self.centralwidget)
        self.imgEndTimeBox.setGeometry(QtCore.QRect(340, 480, 50, 24))
        self.imgEndTimeBox.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #2a84e5")

        # Creating Start time labels and text boxes for audio files
        self.audioStartTimeLabel = QLabel(self.centralwidget)
        self.audioStartTimeLabel.move(150, 719)
        self.audioStartTimeLabel.setText("Start time:")
        self.audioStartTimeBox = QLineEdit(self.centralwidget)
        self.audioStartTimeBox.setGeometry(QtCore.QRect(220, 715, 50, 24))
        self.audioStartTimeBox.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #2a84e5")

        # Creating End time labels and text boxes for audio files
        self.audioEndTimeLabel = QLabel(self.centralwidget)
        self.audioEndTimeLabel.move(280, 719)
        self.audioEndTimeLabel.setText("End time:")
        self.audioEndTimeBox = QLineEdit(self.centralwidget)
        self.audioEndTimeBox.setGeometry(QtCore.QRect(340, 715, 50, 24))
        self.audioEndTimeBox.setStyleSheet("border-radius: 5; border: 2px solid blue; border-color: #2a84e5")

        # This is our comboBox for switching views.
        # There are two options: Tree-View and Thumbnail-View
        self.myCombo = QComboBox(self.centralwidget)
        self.myCombo.addItem("Tree-view Mode (Local)")
        self.myCombo.addItem("Thumbnail-view Mode (Online)")
        self.myCombo.setStyleSheet("border-radius: 2; border: 2px solid blue; border-color: #2a84e5")
        self.myCombo.move(490, 480)
        self.myCombo.setGeometry(QtCore.QRect(480, 480, 250, 24))
        self.myCombo.activated[str].connect(self.comboBoxMethod)

        self.createTimeline()
        self.createAudioTimeline()
        self.createSlider()
        self.myImage = QLabel(self.centralwidget)
        self.myAudio = QLabel(self.centralwidget)
        self.createTreeView()
        self.createPalet()
        self.createBoard()
        self.connectButtons()

        # pixel positions for crop
        self.startpos = [0, 0]
        self.endpos = [0, 0]
        self.isCropOn = False
        os.system('cls' if os.name == 'nt' else 'clear')

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
        self.actionShare_FacebookVid.setText(_translate("MainWindow", "Share Video on Facebook"))
        self.actionShare_FacebookImg.setText(_translate("MainWindow", "Share Image on Facebook"))

    def connectButtons(self):
        self.treeView.doubleClicked.connect(self.treeFileClicked)               # Action for double-clicking images
        self.actionQuit.triggered.connect(self.quitProgram)                     # Action for Quit
        self.playButton.clicked.connect(self.play)                              # Action for Play Button
        self.addButton.clicked.connect(self.addToTimeline)                      # Action for adding images to timeline
        self.addAudioButton.clicked.connect(self.addAudioToTimeline)            # Action for adding audio files to timeline
        self.actionBrightness.triggered.connect(self.change_brightness)         # Action for brightness
        self.actionContrast.triggered.connect(self.change_contrast)             # Action for contrast
        self.actionHue_Saturation.triggered.connect(self.change_saturation)     # Action for saturation
        self.actionBlack_White.triggered.connect(self.blackwhite)               # Action for black and white
        self.actionBlur.triggered.connect(self.blur)                            # Action to blur the image
        self.actionSharpen.triggered.connect(self.sharpen)                      # Action to sharpen the image
        self.actionOpen_Audio_File.triggered.connect(self.importAudio)          # Action for Open Audio...
        self.actionOpen_Image.triggered.connect(self.importImage)               # Action for Open Image...
        self.actionShare_TwitterImg.triggered.connect(self.shareTwitterImage)   # Action for sharing an image on Twitter
        self.actionShare_TwitterVid.triggered.connect(self.shareTwitterVideo)   # Action for sharing a video on Twitter
        self.actionShare_FacebookImg.triggered.connect(self.shareFacebookImage) # Action for sharing an image on Facebook
        self.actionShare_FacebookVid.triggered.connect(self.shareFacebookVideo) # Action for sharing a video on Facebook
        self.makeMovieButton.clicked.connect(self.writeToFrame)                 # Action for making the movie
        self.actionCrop.triggered.connect(self.cropimg)                         # Action for croping the image
        self.actionSave.triggered.connect(self.savefile)                        # Action for saving an image on the local hard drive

    # This is the tree-view, which is located on the left-hand side.
    # It is our main tool to browse folders and paths.
    def createTreeView(self):
         self.treeView = QtWidgets.QTreeView(self.centralwidget)
         self.treeView.setGeometry(QtCore.QRect(20, 10, 441, 461))
         self.treeView.setObjectName("treeView")
         model = QFileSystemModel()
         model.setRootPath('')
         self.treeView.setModel(model)

    # This method shares the selected image on twitter
    def shareTwitterImage(self):
        twitter.authorize()
        twitter.postImage("")

    # This method shares the created slideshow on Twitter
    def shareTwitterVideo(self):
        twitter.authorize()

    # This method shares the selected image on facebook
    def shareFacebookImage(self):
        print("The image was shared on Facebook. Yay!")
        #self.createFinalAudioFile()

    # This method shares the created slideshow on Facebook
    def shareFacebookVideo(self):
        print("The video was shared on Facebook. Yay!")

    # Creating a palet for searching images on the database of Flickr
    def createPalet(self):
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setObjectName("Palet")
        self.frame.setStyleSheet('#Palet { border: 5px solid grey; border-color: #2a84e5}')
        self.frame.setGeometry(20, 7, 450, 465)
        self.palet = QtWidgets.QGridLayout(self.frame)
        self.palet.addWidget(QLineEdit(), 0, 0, 1, 2)
        self.palet.addWidget(QPushButton("Search"), 0, 2)
        self.palet.itemAt(1).widget().clicked.connect(self.searchImages)
        self.frame.setVisible(False)

    # Trims audio files
    def trimAudioFile(self, infile, outfilename, start_ms, end_ms):
        width = infile.getsampwidth()
        rate = infile.getframerate()
        fpms = rate // 1000 # frames per ms
        length = (end_ms - start_ms) * fpms
        start_index = start_ms * fpms
        out = wave.open(outfilename, "wb")
        out.setparams((infile.getnchannels(), width, rate, length, infile.getcomptype(), infile.getcompname()))
        infile.rewind()
        anchor = infile.tell()
        infile.setpos(anchor + start_index)
        out.writeframes(infile.readframes(int(length)))

    # Makes the final audio Files
    def createFinalAudioFile(self):
        iterNum = len(self.prModel.audioStartTimes)
        infiles = []
        outfile = "finalAudioFile.wav"
        k=0
        # First we want to slice each audio file
        for i in range(iterNum):
            if i==0:
                self.trimAudioFile(wave.open(str(self.prModel.audioTrackQueue[i]), "rb"), "audioOut" + str(k)+ ".wav", self.prModel.audioStartTimes[i]*1000, self.prModel.audioEndTimes[i]*1000)
                infiles.append("audioOut" + str(k)+ ".wav")
                k = k+1
            else:
                timeDifference = self.prModel.audioStartTimes[i] - self.prModel.audioEndTimes[i-1]
                if timeDifference==0:
                    self.trimAudioFile(wave.open(str(self.prModel.audioTrackQueue[i]), "rb"), "audioOut" + str(k)+ ".wav", 0, (self.prModel.audioEndTimes[i]*1000)- (self.prModel.audioStartTimes[i]*1000))
                    infiles.append("audioOut" + str(k)+ ".wav")
                    k = k+1
                else:
                    self.trimAudioFile(wave.open("silence2.wav", "rb"), "audioOut" + str(k)+ ".wav", 0, timeDifference*1000)
                    infiles.append("audioOut" + str(k)+ ".wav")
                    k = k+1
                    self.trimAudioFile(wave.open(str(self.prModel.audioTrackQueue[i]), "rb"), "audioOut" + str(k)+ ".wav", 0, (self.prModel.audioEndTimes[i]*1000)- (self.prModel.audioStartTimes[i]*1000))
                    infiles.append("audioOut" + str(k)+ ".wav")
                    k = k+1

        # Then, when we have all sliced audio files, we merge them together.
        data= []
        for infile in infiles:
            w = wave.open(infile, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()

        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        for i in range(len(infiles)):
            output.writeframes(data[i][1])
        output.close()

        # merging the video and audio at the end
        #os.system('ffmpeg -i finalVideo.mp4 -i piano-melody.wav -vcodec copy finalOutput.mp4')

        # Cleaning up
        for i in range(len(infiles)):
            os.remove(infiles[i])

    # This method basically is called whenever the status of the comboBox is changed.
    def comboBoxMethod(self, text):
        if text=="Tree-view Mode (Local)":
            self.frame.setVisible(False)
            self.treeView.setVisible(True)
        else:
            self.frame.setVisible(True)
            self.treeView.setVisible(False)

    # When the user clicks on the play button, this method is invoked.
    def play(self):
        if len(self.prModel.imageStartTimes)==0:
            print("You have not added images to play.")
            return
        # Stores the checkpoints at which image needs to change in imageboard
        changeList = []

        # To start showing image at 0th second
        changeList.append(0)
        total = 0
        c = 0
        self.handleAudio()
        self.playButton.setEnabled(False)
        self.isPlaying = 1
        self.myThread = QtCore.QThread()
        self.task = imageThread(self)
        self.task.moveToThread(self.myThread)
        self.myThread.started.connect(lambda: self.task.playSlides(self))
        self.myThread.start()

    # This method is used for searching Flickr's database
    def searchImages(self, query):
        self.searchedImages = []
        try:
            shutil.rmtree("./cache")
        except:
            pass
        try:
            os.mkdir('./cache')
        except:
            pass
        query = self.palet.itemAt(0).widget().text()
        req = 'https://api.flickr.com/services/rest/'
        req = req + '?method=flickr.photos.search'
        req = req + '&per_page=9'
        req = req + '&format=json&nojsoncallback=1&extras=geo'
        req = req + '&api_key=83a6ef0d071350b24c6e8689e0078093'
        req = req + '&tags='+query
        res = requests.get(req).json()
        imageList = res['photos']
        print('=========================================================')
        for img in imageList['photo']:
            imgPath = "https://farm"+str(img['farm'])+".staticflickr.com/"+str(img['server'])+"/"+str(img['id'])+"_"+str(img['secret'])+".jpg"
            print(imgPath)
            urllib.request.urlretrieve(imgPath, "./cache/"+str(img['id'])+"_"+str(img['secret'])+".jpg")
        print('=========================================================')
        for file_ in os.listdir("./cache"):
            self.searchedImages.append("./cache/"+file_)
        self.drawImages()


    def drawImages(self):
        c = 0
        for i in range(1, 4):
            for j in range(0, 3):
                self.palet.addWidget(QLabel(), i, j)
                image = QPixmap(self.searchedImages[c])
                self.palet.itemAt(((3*i)+j)-1).widget().setPixmap(image.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.palet.itemAt(((3*i)+j)-1).widget().setStyleSheet("border: 2px solid black")
                clickable(self.palet.itemAt(((3*i)+j)-1).widget()).connect(self.indexOfLabel)
                c += 1


    def indexOfLabel(self, label):
        index = self.palet.indexOf(label)
        self.showSelected(index)

    def showSelected(self, index):
        self.filePath=self.searchedImages[index-2]
        try:
            self.pixmap = QPixmap(self.filePath)
            self.pixmap = self.scaleImage(self.pixmap)
            self.imageBoard.setPixmap(self.pixmap)
            self.imageBoard.setAlignment(Qt.AlignCenter)
        except:
            print('Not an image file! Please try another file.')
        print('Clicked: ', self.filePath)


    # This is where the selected picture is shown
    # We create the board using a QLabel once, and then we keep updating it
    # using other functions.
    def createBoard(self):
        self.imageBoard = QLabel(self.centralwidget)
        self.imageBoard.setStyleSheet('border: 5px solid grey; border-color: #2a84e5')
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
        self.horizontalSlider.setGeometry(QtCore.QRect(0, 0, 994, 40))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setRange(0,60)
        self.animation = QPropertyAnimation(self.horizontalSlider)
        self.animation.setStartValue(self.horizontalSlider.minimum())

    # This is our timeline, where we place images on.
    # We are using a QFrame to imitate the feeling of an actual timeline.
    def createTimeline(self):
        self.timeline = QtWidgets.QFrame(self.centralwidget)
        self.timeline.setGeometry(QtCore.QRect(16, 512, 994, 130))
        self.timeline.setStyleSheet("background-color: rgb(186, 186, 186); border-radius: 5; border: 2px solid blue; border-color: #694f92")
        self.timeline.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.timeline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.timeline.setObjectName("Timeline")

    # This is our timeline for the audio QFileSystemModel
    # We are using a QFrame as well.
    def createAudioTimeline(self):
        self.audiotimeline = QtWidgets.QFrame(self.centralwidget)
        self.audiotimeline.setGeometry(QtCore.QRect(16, 655, 994, 50))
        self.audiotimeline.setStyleSheet("background-color: rgb(186, 186, 186); border-radius: 5; border: 2px solid blue; border-color: #694f92")
        self.audiotimeline.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.audiotimeline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.audiotimeline.setObjectName("audioTimeline")

    def playView(self, imgIndex):
        try:
            self.img = QPixmap(self.prModel.labelList[imgIndex])
            self.img = self.scaleImage(self.img)
            self.imageBoard.setPixmap(self.img)
            self.imageBoard.setAlignment(Qt.AlignCenter)
        except:
            pass

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

    # This method adds images and places them on the timeline.
    def addToTimeline(self):
        if self.prModel.oneImageImported==0:
            print("You have not imported any image to place on the timeline. Please add an image first.")
            return
        if len(self.imgStartTimeBox.text()) == 0:
            print("You have not set the start time of the image.")
            return
        if len(self.imgEndTimeBox.text()) == 0:
            print("You have not set the end time of the image.")
            return
        startTime = int(self.imgStartTimeBox.text())
        endTime = int(self.imgEndTimeBox.text())
        displayLength = endTime - startTime
        imgProp = ((displayLength/60)*985)
        self.prModel.imageStartTimes.append(startTime)
        self.prModel.imageEndTimes.append(endTime)
        self.duration = endTime
        if self.prModel.timelineIsEmpty == 1:
            self.myImage.setGeometry(QtCore.QRect(16.41*(startTime+1), 550, imgProp, 85))
            pixmap = QPixmap(self.filePath)
            pixmap = self.scaleImage(pixmap, imgProp, 85)
            self.myImage.setPixmap(pixmap)
            self.myImage.setAlignment(Qt.AlignCenter)
            self.myImage.setVisible(1)
            self.prModel.timelineIsEmpty = 0
            self.prModel.thumbnailLengthTracker += imgProp + 16.41
            imgDuration = QLabel(self.centralwidget)
            imgDuration.setText(str(displayLength)+ 's')
            imgDuration.move(imgProp/2,685)
        else:
            self.myImage = QLabel(self.centralwidget)
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
            imgDuration.move(self.prModel.thumbnailLengthTracker-(imgProp/2),685)
        self.prModel.labelList.append(self.filePath)
        self.prModel.durations.append(endTime)
        self.prModel.durationLabels.append(displayLength)

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

    # This method checks with the user whether the user wants to close the program or not
    def quitProgram(self):
        choice = QMessageBox.question(self, 'Exit', "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            print('Application closed successfully.')
            sys.exit()

    # This method opens a dialog box for importing an audio file
    def importAudio(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.audioPath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;mp3 Files (*.mp3);;WMA Files (*.wma);;WAVE Files (*.wave)", options=options)
        if self.audioPath:
            print(self.audioPath)
            self.prModel.audioTrackQueue.append(self.audioPath)

    # This method adds the audio and puts on the timeline.
    def addAudioToTimeline(self):
        if len(self.audioStartTimeBox.text()) == 0:
            print("You have not set the start time of the audio.")
            return
        if len(self.audioEndTimeBox.text()) == 0:
            print("You have not set the end time of the audio.")
            return
        try:
            if self.prModel.timelineIsEmpty == 1:
                startTime = int(self.audioStartTimeBox.text())
                endTime = int(self.audioEndTimeBox.text())
                self.prModel.audioStartTimes.append(startTime)
                self.prModel.audioEndTimes.append(endTime)
                displayLength = endTime - startTime
                imgProp = ((displayLength/60)*985)
                self.myAudio.setGeometry(QtCore.QRect(16.41*(startTime+1), 656, imgProp, 48))
                self.myAudio.setAlignment(Qt.AlignCenter)
                self.myAudio.setStyleSheet('border: 2px solid red; border-radius: 5')
                self.myAudio.setText(str(self.audioPath))
                self.myAudio.setVisible(1)
                self.prModel.timelineIsEmpty = 0
                self.prModel.thumbnailLengthTracker += imgProp + 16.41
            else:
                startTime = int(self.audioStartTimeBox.text())
                endTime = int(self.audioEndTimeBox.text())
                self.prModel.audioStartTimes.append(startTime)
                self.prModel.audioEndTimes.append(endTime)
                displayLength = endTime - startTime
                imgProp = ((displayLength/60)*985)
                self.myAudio = QLabel(self.centralwidget)
                self.myAudio.setStyleSheet('border: 2px solid red; border-radius: 5')
                self.myAudio.setGeometry(QtCore.QRect(16.41*(startTime+1), 656, imgProp, 48))
                self.myAudio.setText(str(self.audioPath))
                self.myAudio.setAlignment(Qt.AlignCenter)
                self.myAudio.setVisible(1)
                self.prModel.thumbnailLengthTracker += imgProp
        except:
            print("Something happened while adding the audio file to the timeline!")

    # Spawning a thread for handling the audio within the app
    def handleAudio(self):
        self.testThread = QtCore.QThread()
        self.a1 = audioHandlingThread(self, self.audioPath, self.prModel.audioStartTimes, self.prModel.audioEndTimes, self.prModel.audioTrackQueue )
        self.a1.moveToThread(self.testThread)
        self.testThread.started.connect(self.a1.playAudioTracks)
        self.testThread.start()

    # This method makes the slideshow
    def writeToFrame(self):
        if len(self.prModel.imageStartTimes)==0:
            print("You have not added images to Render.")
            return
        self.vThread = QtCore.QThread()
        duration = self.duration
        self.vOutput = Video(self)
        self.vOutput.moveToThread(self.vThread)
        self.vThread.started.connect(self.vOutput.output)
        self.vThread.start()

    def convertToImage(self, pixmap):
        img = pixmap.toImage()
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        img.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        return pil_im

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
            self.prModel.oneImageImported = 1
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
        self.pixmap.save(self.filePath+"01")

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
        cropped = self.pixmap.copy(self.startpos[0], self.startpos[1], self.endpos[0] - self.startpos[0], self.endpos[1] - self.startpos[1])
        self.imageBoard.setPixmap(cropped)
        self.imageBoard.setAlignment(Qt.AlignCenter)
        self.isCropOn = False
        QApplication.restoreOverrideCursor()

def clickable(widget):      # Making QLabels clickable
    class Filter(QObject):      # Filtering through only QObjects
        clicked = pyqtSignal([QLabel])      # Creating signal object and including QLabel object in it
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonPress:
                    if obj.rect().contains(event.pos()):    # If position of click is in the QObjects area
                        self.clicked.emit(obj)      # Emit Signal
                        return True   # Clicked object recognizable
            return False       # Clicked Object blocked by filter
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
