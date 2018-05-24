import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QAction
import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QPixmap, QColor, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSoundEffect
import math
from  PIL import ImageFilter, Image



class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image display'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 600, 600)

        # Create a label
        label = QLabel(self)
        self.label = QLabel(self)
        self.label.setGeometry(0,0,600,600)
#        self.label.setStyleSheet("border: 10px solid blue;")

        # load image from file
        self.pixmap = QPixmap('Lena.png')
        self.img = self.pixmap.toImage()
        
        # change contrast
#        self.change_contrast(128)  
        
        # change saturation
#        self.change_saturation(0.0)
        
        # change to black and white
#        self.change_black_white()
        
        # change brightness
#        self.change_brightness(100)
        
        # blur an image
#        self.blur_image(5)
        
        # sharpen an image
        self.sharpen_image()
        
 
        # load to label
        self.label.setPixmap(self.pixmap)
#        self.label.setPixmap(QImage(img))
        self.label.setAlignment(Qt.AlignCenter)
        self.show()
    
    # contrast function, level should range from -255 to 255    
    def change_contrast(self, level):   
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
        
    # saturation function, 
    def change_saturation(self, level):
        for x in range(self.img.width()):
            for y in range(self.img.height()):
                color = QColor(self.img.pixel(x, y))
                p = math.sqrt(color.red()*color.red()*0.299 + color.green()*color.green()*0.587 + color.blue()*color.blue()*0.114) 
                r = self.truncate(p + (color.red() - p) * level)
                g = self.truncate(p + (color.green() - p) * level)
                b = self.truncate(p + (color.blue() - p) * level)
                self.img.setPixelColor(x, y, QColor(r, g, b))   
        self.pixmap.convertFromImage(self.img)
        
    # change to black & white
    def change_black_white(self):
        for x in range(self.img.width()):
            for y in range(self.img.height()): 
                color = QColor(self.img.pixel(x, y))
                gray = 0.2989 * color.red() + 0.5870 * color.green() + 0.1140 * color.blue()
                if gray > 120:   # may need to update 100
                    self.img.setPixelColor(x, y, QColor(255, 255, 255))  
                else:
                    self.img.setPixelColor(x, y, QColor(0, 0, 0))
        self.pixmap.convertFromImage(self.img)      
        
    # change brightness
    def change_brightness(self, level ):
        for x in range(self.img.width()):
            for y in range(self.img.height()): 
                color = QColor(self.img.pixel(x, y))
                r = self.truncate(color.red() + level)
                g = self.truncate(color.green() + level)
                b = self.truncate(color.blue() + level)
                self.img.setPixelColor(x, y, QColor(r, g, b))   
        self.pixmap.convertFromImage(self.img)     
                
    def truncate(self, color):
        if color < 0:
            return 0
        elif color > 255:
            return 255
        else:
            return int(color)
        
    # not working for now
    def crop_img(self):
        self.img_view.setup_crop(self.pixmap.width(), self.pixmap.height())
        dialog = editimage.CropDialog(self, self.pixmap.width(), self.pixmap.height())
        if dialog.exec_() == QDialog.Accepted:
            coords = self.img_view.get_coords()
            self.pixmap = self.pixmap.copy(*coords)
            self.load_img()
        self.img_view.rband.hide()
    
    # blur an image with PIL
    def blur_image(self, radi):
        self.img = Image.open('Lena.png')
        self.img = self.img.filter(ImageFilter.GaussianBlur(radius=radi))
        self.img.save("temp/tmp_Lena.png")
        self.pixmap = QPixmap('temp/tmp_Lena.png')
        os.remove('temp/tmp_Lena.png')
    
    
    # sharpen an image with PIL
    def sharpen_image(self):
        self.img = Image.open('Lena.png')
        self.img = self.img.filter(ImageFilter.SHARPEN())
        self.img.save("temp/tmp_Lena.png")
        self.pixmap = QPixmap('temp/tmp_Lena.png')
        os.remove('temp/tmp_Lena.png')        
    
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())





