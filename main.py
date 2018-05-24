'''
~~~~~ A Photo Editor and Slideshow Maker in Python3 Using PyQt5 ~~~~~

~~~~~~~~~ Contributors: Uzair Inamdar, Jizhou Yang, Saman Porhemmat
~~~~~~~~~ All Rights Reserved
~~~~~~~~~
~~~~~~~~~ San Francisco State University
~~~~~~~~~ Course: CSC 690
~~~~~~~~~ Final Project
~~~~~~~~~ Date: Fall 2017

This is our main class, the starting point of the program. In order to run the application,
simply execute the following command:

python3 main.py

Please note that the execution of the application is contingent upon a few libraries. Refer to
the readme file included with the program for more information.
'''

from editorMainWindow import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui
import sys

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # Build GUI
        self.myGui = Ui_MainWindow()
        self.myGui.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
