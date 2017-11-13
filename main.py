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
