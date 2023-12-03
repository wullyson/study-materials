import sys
import typing
import cv2
import shutil
import os
from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtGui import QImage, QPixmap,QIcon,QPainter,QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel,QLayout,QVBoxLayout,QFileDialog,QColorDialog,QButtonGroup

from PyQt5.QtCore import QTimer, Qt
from UI_update import Ui_MainWindow as UI_newwindow
import socket
from sender import sender 
from receive import receive

class Window0(QMainWindow):
    def __init__(self):
        self.situation=True
        self.pictu = False
        super().__init__()
        self.ui = UI_newwindow()
        self.ui.i = 16
        self.ui.setupUi(self)
        self.ui.PushBotton_get.clicked.connect(self.cloro_choses) 
        self.ui.PushBotton_get_2.clicked.connect(self.save_pictur)  
        self.ui.PushBotton_get_3.clicked.connect(self.date_upload)
        self.ui.pushButton.clicked.connect(self.date_upload)
        self.ui.pushButton_2.clicked.connect(self.newicon)
        self.ui.radio_button.clicked.connect(self.send)
        self.label_capture = self.findChild(QLabel, "Label_capture")
        self.Label_after = self.findChild(QLabel,"Label_after")
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
                facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                facereport = facecascade.detectMultiScale(gary,1.1,3)
                bfx,bfy,bfw,bfh=0,0,0,0
                cropped_face = image_frame
                if len(facereport) == 1:
                    self.pictu = True
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
                        self.pictu = False
                    else:
                        cv2.rectangle(image_rectangle, (bfx, bfy), (bfx + bfw, bfy + bfh), (0, 255, 0), 2)
                        # cropped_face = image_frame[y-90:y+h+60, x-80:x+w+107]

                elif len(facereport) > 1 :
                    self.pictu = False
                else :
                    self.pictu = False
                #####
                height, width, channel = image_rectangle.shape
                bytes_per_line = 3 * width
                image_rectangle =  cv2.cvtColor(image_rectangle, cv2.COLOR_BGR2RGB)
                q_image = QImage(image_rectangle.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.label_capture.setPixmap(pixmap)
                self.label_capture.setAlignment(Qt.AlignCenter)
                self.image_frame = image_frame
    def capture_and_display_image(self):
        if self.pictu == True:
            self.is_paused = True
            if self.image_frame is not None:         
                image_rgb = cv2.cvtColor(self.image_frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite('captured_image.jpg', image_rgb)
                self.update_frame()
                self.label_capture.setPixmap(QPixmap('captured_image.jpg'))
    def newicon(self):
        if self.situation :
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("C:/Users/dickh/Downloads\\../../../study-materials-report-python-windows/Ver6/canel_ICON.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_2.setIcon(icon)
            self.capture_and_display_image()
            self.situation=False
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("C:/Users/dickh/Downloads\\../../../study-materials-report-python-windows/Ver6/captur_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_2.setIcon(icon)
            self.is_paused = False
            self.situation=True
    def save_pictur(self):
        directory_path = QFileDialog.getExistingDirectory(self, '选择資料夾')
        if directory_path:
            image_file_path = 'C:/study-materials-report-python-windows/Ver6/receive_image.jpg'
            destination_path = os.path.join(directory_path, 'save.jpg')
            shutil.copyfile(image_file_path, destination_path)
    def pause_resume_camera(self):
        self.is_paused = False
    def cloro_choses(self):
        color =QColorDialog.getColor()
        print(color)
    def date_upload(self):
        sender_object = self.sender()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '选择照片', '', 'Images (*.png *.xpm *.jpg *.jpeg *.bmp)')
        button_name = sender_object.objectName() 
        if button_name == 'pushButton' :
            if file_path:
                destination_directory = 'C:/study-materials-report-python-windows/Ver6' 
                destination_path = os.path.join(destination_directory, 'captured_upload.png')
                shutil.copyfile(file_path, destination_path)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("C:/Users/dickh/Downloads\\../../../study-materials-report-python-windows/Ver6/canel_ICON.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.pushButton_2.setIcon(icon)
                qpixmap = QPixmap()
                qpixmap.load('C:/study-materials-report-python-windows/Ver6/captured_upload.png')#更換電腦或檔案位置記得改
                self.label_capture.setPixmap(qpixmap)
                self.is_paused = True
                self.situation=False
        elif button_name == 'PushBotton_get_3':
                if file_path:
                    destination_directory = 'C:/study-materials-report-python-windows/Ver6/picture' 
                    destination_path = os.path.join(destination_directory, f'photo{self.ui.i}.jpg')
                    self.ui.i=self.ui.i+1
                    shutil.copyfile(file_path, destination_path)
                    photo_path=f'C:/study-materials-report-python-windows/Ver6/picture/photo{self.ui.i}'
                    pixmap = QtGui.QPixmap(photo_path)
                    self.ui.chang()
    def on_fab_click(self):
        print('Floating Action Button Clicked!')
    def send(self,event):
        print("1")
        if self.is_paused :
            sender()
            receive()
            self.is_paused = True
            self.label_capture.setPixmap(QPixmap('receive_image.jpg'))
            self.vid_cam.release()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window0 = Window0()
    window0.show()
    sys.exit(app.exec_())