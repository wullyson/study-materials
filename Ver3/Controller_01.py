import sys
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from image_00 import Ui_MainWindow as Ui_Window0
from image_02 import Ui_MainWindow as Ui_Window2
from image_03 import Ui_MainWindow as Ui_Window3


class Window0(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Window0()
        self.ui.setupUi(self)
        self.ui.PushBotton_get.clicked.connect(self.capture_and_display_image) 
        self.ui.PushBotton_cancel.clicked.connect(self.pause_resume_camera) 
        self.ui.PushBotton_correct.clicked.connect(self.closeEvent)
        self.ui.PushBotton_jp.clicked.connect(self.open_window2)
        self.ui.PushBotton_kr.clicked.connect(self.open_window3)
        
        self.label_capture = self.findChild(QLabel, "Label_capture")
        self.vid_cam = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)
        self.image_frame = None  
        self.is_paused = False
        
    def update_frame(self):
        if not self.is_paused:
            ret, image_frame = self.vid_cam.read()
            if ret:
                image_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
                height, width, channel = image_frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(image_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.label_capture.setPixmap(pixmap)
                self.label_capture.setAlignment(Qt.AlignCenter)
                self.image_frame = image_frame  

    def capture_and_display_image(self):
        self.is_paused = True
        if self.image_frame is not None:         
            image_rgb = cv2.cvtColor(self.image_frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite('captured_image.jpg', image_rgb)
            self.update_frame()
            self.label_capture.setPixmap(QPixmap('captured_image.jpg'))

    def pause_resume_camera(self):
        self.is_paused = False

    def closeEvent(self,event):
        self.vid_cam.release()    

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