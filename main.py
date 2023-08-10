import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QMainWindow, QListWidget, QLabel
from PyQt5 import QtGui
from PyQt5 import QtCore


class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        desktop = QApplication.desktop()
        self.DHEIGHT = desktop.height()
        self.DWIDTH = desktop.width()
        self.setWindowTitle('app')
        
        self.Exit_Button = QPushButton(self)
        self.Exit_Button.setText("ВЫХОД")
        self.Exit_Button.setFont(QtGui.QFont("intro", 20))
        self.Exit_Button.adjustSize()
        self.Exit_Button.move(self.DWIDTH - self.Exit_Button.width() - 100, self.DHEIGHT - self.Exit_Button.height() - 110)
        self.Exit_Button.clicked.connect(self.Exit_func)
        self.Exit_Button.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")

        self.Notes_list = QListWidget(self)
        self.Notes_list.setGeometry(self.DWIDTH // 2 - 120, 100, self.DWIDTH // 2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 130)
        self.Notes_list.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")
        
        self.Notes_list_text = QLabel(self)
        self.Notes_list_text.setText("ЗАМЕТКИ")
        self.Notes_list_text.setFont(QtGui.QFont("intro", 20))
        self.Notes_list_text.setGeometry(self.DWIDTH // 2 - 120, 70, self.DWIDTH // 2 - self.Exit_Button.width(), 30)
        self.Notes_list_text.setAlignment(QtCore.Qt.AlignCenter)
        self.Notes_list_text.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white")

        self.Reminders_list = QListWidget(self)
        self.Reminders_list.setGeometry(self.DWIDTH // 2 - 120, self.DHEIGHT // 2 + 30, self.DWIDTH // 2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 140)
        self.Reminders_list.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")

        self.Reminders_list_text = QLabel(self)
        self.Reminders_list_text.setText("НАПОМИНАНИЯ")
        self.Reminders_list_text.setFont(QtGui.QFont("intro", 20))
        self.Reminders_list_text.setGeometry(self.DWIDTH // 2 - 120, self.DHEIGHT // 2, self.DWIDTH // 2 - self.Exit_Button.width(), 30)
        self.Reminders_list_text.setAlignment(QtCore.Qt.AlignCenter)
        self.Reminders_list_text.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white")

        self.Alarm_list = QListWidget(self)
        self.Alarm_list.setGeometry(100, 100, self.DWIDTH // 2 - self.Exit_Button.width() - 140, self.DHEIGHT - 210)
        self.Alarm_list.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")

        self.Alarm_list_text = QLabel(self)
        self.Alarm_list_text.setText("БУДИЛЬНИКИ")
        self.Alarm_list_text.setFont(QtGui.QFont("intro", 20))
        self.Alarm_list_text.setGeometry(100, 70, self.DWIDTH // 2 - self.Exit_Button.width() - 140, 30)
        self.Alarm_list_text.setAlignment(QtCore.Qt.AlignCenter)
        self.Alarm_list_text.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white")

        self.showFullScreen()

    def Exit_func(self):
        self.Exit_Button.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020") 
        Are_U_Sure_Box = QMessageBox()
        Are_U_Sure_Box.move(self.DWIDTH // 2, self.DHEIGHT // 2)
        Are_U_Sure_Box
        reply = QMessageBox.question(self, 'Уверены?',
            "Вы уверены что хотите выйти?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            Are_U_Sure_Box.close()

    def mouseMoveEvent(self, event):
        if event.x() > self.DWIDTH - self.Exit_Button.width() - 105 and event.x() < self.DWIDTH - 95 and event.y() > self.DHEIGHT - self.Exit_Button.height() - 115 and event.y() < self.DHEIGHT - 105:
            self.Exit_Button.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: red")
        else:
            self.Exit_Button.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.setObjectName("MainWindow")
    window.setStyleSheet(
        "#MainWindow{border-image:url(images/background.gif)}")
    window.show()
    sys.exit(app.exec_())