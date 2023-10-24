# -*- coding: utf-8 -*-
import sys
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtWidgets import QFileDialog
from image_00 import Ui_MainWindow as Ui_Window0
from image_01 import Ui_MainWindow as Ui_Window1
from image_02 import Ui_MainWindow as Ui_Window2
from image_03 import Ui_MainWindow as Ui_Window3



class Window0(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Window0()
        self.ui.setupUi(self)
        self.ui.pushButton_open_window1.clicked.connect(self.open_window1)
        self.ui.pushButton.clicked.connect(self.import_image)

    def import_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, r"选择图像文件", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)
        if file_name:
            self.display_image(file_name)

    def display_image(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            print("Failed to load image:", image_path)
            return

        height, width, channel = img.shape
        bytesPerline = 3 * width
        qimg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_3.setPixmap(QPixmap.fromImage(qimg))
        self.ui.label_3.setScaledContents(True)
        self.ui.label_3.setAlignment(QtCore.Qt.AlignCenter)

    def open_window1(self):
        self.window1 = Window1()
        self.window1.show()

class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Window1()
        self.ui.setupUi(self)
        self.ui.pushButton1_open_window2.clicked.connect(self.open_window2)
        self.ui.pushButton2_open_window3.clicked.connect(self.open_window3)

    def open_window2(self):
        self.window2 = Window2()
        self.window2.show()

    def open_window3(self):
        self.window3 = Window3()
        self.window3.show()

class Window2(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.ui = Ui_Window2()
        self.ui.setupUi(self)

class Window3(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.ui = Ui_Window3()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window0 = Window0()
    window0.show()
    sys.exit(app.exec_())