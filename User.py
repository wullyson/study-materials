import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_0 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_0.setGeometry(QtCore.QRect(350, 310, 93, 28))
        self.pushButton_0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_0.setAutoDefault(False)
        self.pushButton_0.setDefault(False)
        self.pushButton_0.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 40, 651, 51))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 140, 241, 371))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(480, 140, 241, 371))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_0.setText(_translate("MainWindow", "匯入圖檔"))
        self.label.setText(_translate("MainWindow", "GUI圖形介面測試第一版"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))


class MainWindowController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_0.clicked.connect(self.show_choose_window)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.choose_window = ChooseWindow()
        self.korean_window = KoreanWindow()
        self.japanese_window = JapaneseWindow()

        self.stacked_widget.addWidget(self.choose_window)
        self.stacked_widget.addWidget(self.korean_window)
        self.stacked_widget.addWidget(self.japanese_window)

    def show_choose_window(self):
        self.stacked_widget.setCurrentWidget(self.choose_window)

    def show_korean_hairstyles(self):
        self.stacked_widget.setCurrentWidget(self.korean_window)

    def show_japanese_hairstyles(self):
        self.stacked_widget.setCurrentWidget(self.japanese_window)

class ChooseWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = MainWindowController()
        self.ui.setupUi(self)  # 將 MainWindow 作為參數傳遞

        self.ui.pushButton_1.clicked.connect(self.show_korean_hairstyles)
        self.ui.pushButton_2.clicked.connect(self.show_japanese_hairstyles)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(180, 310, 111, 71))
        self.pushButton_1.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 150, 111, 71))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_1.setText(_translate("MainWindow", "韓系髮型"))
        self.pushButton_2.setText(_translate("MainWindow", "日系髮型"))

class KoreanWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("韓系髮型")
        self.setGeometry(100, 100, 800, 600)

        # 加入韓系髮型的圖片 QLabel
        self.labels = []
        for i in range(5):
            label = QtWidgets.QLabel(self)
            label.setGeometry(50 + i * 150, 50, 100, 100)
            self.labels.append(label)

        # 在這裡加載並設定韓系髮型的圖片，你可以根據需要修改路徑
        image_paths = ['KM1.jpg', 'KM2.jpg', 'KM3.jpg', 'KM4.jpg', 'KM5.jpg']
        for i, image_path in enumerate(image_paths):
            pixmap = QPixmap(image_path)
            self.labels[i].setPixmap(pixmap)
            self.labels[i].setScaledContents(True)


class JapaneseWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("日系髮型")
        self.setGeometry(100, 100, 800, 600)

        # 加入日系髮型的圖片 QLabel
        self.labels = []
        for i in range(5):
            label = QtWidgets.QLabel(self)
            label.setGeometry(50 + i * 150, 50, 100, 100)
            self.labels.append(label)

        # 在這裡加載並設定日系髮型的圖片，你可以根據需要修改路徑
        image_paths = ['JW1.jpg', 'JW2.jpg', 'JW3.jpg', 'JW4.jpg', 'JW5.jpg']
        for i, image_path in enumerate(image_paths):
            pixmap = QPixmap(image_path)
            self.labels[i].setPixmap(pixmap)
            self.labels[i].setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowController()
    window.show()
    sys.exit(app.exec_())
