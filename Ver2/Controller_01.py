import sys
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
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