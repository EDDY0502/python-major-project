from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1390, 893)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(16, 12, 1741, 901))
        self.label.setPixmap(QtGui.QPixmap("back.png"))  # use relative path
        self.label.setScaledContents(True)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 120, 701, 641))
        self.label_2.setPixmap(QtGui.QPixmap("nova.gif"))
        self.label_2.setScaledContents(True)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 700, 311, 191))
        self.label_3.setPixmap(QtGui.QPixmap("start end.gif"))
        self.label_3.setScaledContents(True)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1070, 700, 311, 191))
        self.label_4.setPixmap(QtGui.QPixmap("start end.gif"))
        self.label_4.setScaledContents(True)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 780, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background:transparent")
        self.pushButton.setText("EXIT")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1170, 780, 101, 41))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background:transparent")
        self.pushButton_2.setText("RUN")

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("NEO - Your AI Assistant")

def run_voice_assistant():
    print("NEO is running...")  # Replace this with actual code (e.g., neo.run())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.pushButton.clicked.connect(sys.exit)  # EXIT button
    ui.pushButton_2.clicked.connect(run_voice_assistant)  # RUN button

    MainWindow.show()
    sys.exit(app.exec_())
