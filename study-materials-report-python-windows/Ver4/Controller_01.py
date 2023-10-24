import sys
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from image_00 import Ui_MainWindow as Ui_Window0
from image_02 import Ui_MainWindow as Ui_Window2
from image_03 import Ui_MainWindow as Ui_Window3
import socket

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
                image_rectangle = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
                #####方塊
                gary = cv2.cvtColor(image_frame,cv2.COLOR_RGB2GRAY)
                facecascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
                facereport = facecascade.detectMultiScale(gary,1.1,4)
                bfx,bfy,bfw,bfh=0,0,0,0
                cropped_face = image_frame
                if len(facereport) > 0:
                    most = 0
                    largest_face = None
                    for (x, y, w, h) in facereport:
                         face_size = w + h
                         if face_size > most:
                             most = face_size
                             largest_face = (x, y, w, h)

                    bfx, bfy, bfw, bfh = largest_face
                    if most < 350:
                        cv2.rectangle(image_rectangle, (bfx, bfy), (bfx + bfw, bfy + bfh), (0, 0, 255), 2)
                        print("small")
                    else:
                        cv2.rectangle(image_rectangle, (bfx, bfy), (bfx + bfw, bfy + bfh), (0, 255, 0), 2)
                        cropped_face = image_frame[y-100:y+h+50, x-50:x+w+50]
                #####
                height, width, channel = image_rectangle.shape
                bytes_per_line = 3 * width
                image_rectangle =  cv2.cvtColor(image_rectangle, cv2.COLOR_BGR2RGB)
                q_image = QImage(image_rectangle.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.label_capture.setPixmap(pixmap)
                self.label_capture.setAlignment(Qt.AlignCenter)
                self.image_frame = cropped_face  

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
        photo_filename = 'captured_image.jpg'
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.connect(("172.20.10.3",1234))
            with open(photo_filename, 'rb') as file:
                image_data = file.read()
                s.sendall(image_data)
                print("图像文件已发送")
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