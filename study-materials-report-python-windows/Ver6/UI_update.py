from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(958, 644)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 左側照片
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 481, 591))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # 建造scrollArea
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 10, 481, 591))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn) 
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

       
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 419, 589))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

       
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # 預設視窗3*3
        for i in range(3):
            self.gridLayout.setRowStretch(i, 1)
            self.gridLayout.setColumnStretch(i, 1)

       
        photo_folder = "C:/study-materials-report-python-windows/Ver6/picture"
        self.button_group = QtWidgets.QButtonGroup()  
        for i in range(30):
            photo_path = f"{photo_folder}/photo{i+1}.jpg"
            pixmap = QtGui.QPixmap(photo_path)

        
            widget_container = QtWidgets.QWidget(self.scrollAreaWidgetContents)
            widget_layout = QtWidgets.QVBoxLayout(widget_container)

            label = QtWidgets.QLabel(widget_container)

            label.setPixmap(pixmap.scaled(130, 190, QtCore.Qt.IgnoreAspectRatio))  # 調整圖片尺寸
            widget_layout.addWidget(label)

            self.radio_button = QtWidgets.QRadioButton(widget_container)
            self.radio_button.setObjectName(f"radio_button{i}")
            widget_layout.addWidget(self.radio_button)
            self.button_group.addButton(self.radio_button) 

            self.gridLayout.addWidget(widget_container, i // 3, i % 3, 1, 1)  
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        # 右側物件
        self.Label_capture = QtWidgets.QLabel(self.centralwidget)
        self.Label_capture.setGeometry(QtCore.QRect(500, 10, 441, 541))
        font = QtGui.QFont()
        font.setFamily("隨峰體")
        font.setPointSize(24)
        self.Label_capture.setFont(font)
        self.Label_capture.setScaledContents(True)
        self.Label_capture.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_capture.setObjectName("Label_capture")
        self.PushBotton_get = QtWidgets.QPushButton(self.centralwidget)
        self.PushBotton_get.setGeometry(QtCore.QRect(500, 560, 147, 41))
        self.PushBotton_get.setObjectName("PushBotton_get")
        self.PushBotton_get_2 = QtWidgets.QPushButton(self.centralwidget)
        self.PushBotton_get_2.setGeometry(QtCore.QRect(650, 560, 147, 41))
        self.PushBotton_get_2.setObjectName("PushBotton_get_2")
        self.PushBotton_get_3 = QtWidgets.QPushButton(self.centralwidget)
        self.PushBotton_get_3.setGeometry(QtCore.QRect(800, 560, 147, 41))
        self.PushBotton_get_3.setObjectName("PushBotton_get_3")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(900, 520, 31, 31))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        #拍照鍵
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(700, 490, 31, 31))
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/study-materials-report-python-windows/Ver6/captur_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(200, 200))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Label_capture.setText(_translate("MainWindow", "攝像頭"))
        self.PushBotton_get.setText(_translate("MainWindow", "hair color"))
        self.PushBotton_get_2.setText(_translate("MainWindow", "save"))
        self.PushBotton_get_3.setText(_translate("MainWindow", "上傳髮型"))
    def chang(self):
        photo_folder = "C:/study-materials-report-python-windows/Ver6/picture"
        self.button_group = QtWidgets.QButtonGroup()  
        for i in range(30):
            photo_path = f"{photo_folder}/photo{i+1}.jpg"
            pixmap = QtGui.QPixmap(photo_path)

        
            widget_container = QtWidgets.QWidget(self.scrollAreaWidgetContents)
            widget_layout = QtWidgets.QVBoxLayout(widget_container)

            label = QtWidgets.QLabel(widget_container)

            label.setPixmap(pixmap.scaled(130, 190, QtCore.Qt.IgnoreAspectRatio))  # 調整圖片尺寸
            widget_layout.addWidget(label)

            radio_button = QtWidgets.QRadioButton(widget_container)
            widget_layout.addWidget(radio_button)
            self.button_group.addButton(radio_button) 

            self.gridLayout.addWidget(widget_container, i // 3, i % 3, 1, 1)
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
