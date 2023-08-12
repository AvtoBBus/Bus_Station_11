import sys
from Notes_formater import Format_note_text as fnt
import Notes_data_base as ndb
from PyQt5.QtWidgets import *
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

        self.last_text = ""
        self.note_on_work = False

        self.Exit_Button = QPushButton(self)
        self.Exit_Button.setText("ВЫХОД")
        self.Exit_Button.setFont(QtGui.QFont("intro", 20))
        self.Exit_Button.adjustSize()
        self.Exit_Button.move(self.DWIDTH - self.Exit_Button.width() - 100, self.DHEIGHT - self.Exit_Button.height() - 110)
        self.Exit_Button.clicked.connect(self.Exit_func)
        self.Exit_Button.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")

        self.Notes_list = QListWidget(self)
        self.Notes_list.setGeometry(self.DWIDTH // 2 - 120, 100, self.DWIDTH // 2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 130)
        self.Notes_list.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white;")
        self.Notes_list.setFont(QtGui.QFont("intro", 13))
        self.Check_data_base("Notes")
        self.Notes_list.itemDoubleClicked.connect(self.Edit_note_input)

        self.Button_add_note = QPushButton(self)
        self.Button_add_note.move(self.DWIDTH - 200, 100)
        self.Button_add_note.setText("add note")
        self.Button_add_note.adjustSize()
        self.Button_add_note.clicked.connect(self.Add_note_input)
        
        self.Button_clear_notes_list = QPushButton(self)
        self.Button_clear_notes_list.move(self.Button_add_note.x(), self.Button_add_note.y() + self.Button_add_note.height() + 20)
        self.Button_clear_notes_list.setText("clear list")
        self.Button_clear_notes_list.adjustSize()
        self.Button_clear_notes_list.clicked.connect(self.Clear_notes_list)

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
        reply = QMessageBox.question(self, 'Уверены?',
            "Вы уверены что хотите выйти?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            Are_U_Sure_Box.close()

    def Check_data_base(self, db_type:str):
        if db_type == "Notes":
            data = ndb.Read_full()
            if len(data) == 0:
                return
            for elem in data:
                self.Notes_list.addItem(QListWidgetItem(elem))
            
    def Draw_input_note_menu(self, edit : bool = False):
        self.background_notes = QLabel(self)
        self.background_notes.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")
        self.background_notes.setGeometry(self.Notes_list.x() + self.Notes_list.width() // 2, self.Notes_list.y(), self.Notes_list.width() // 2, self.Notes_list.height())
        self.background_notes.show()
        
        self.input_text_note = QLineEdit(self)
        self.input_text_note.setGeometry(self.background_notes.x() + self.background_notes.width() // 5, self.background_notes.y() + 2 * (self.background_notes.height() // 3), self.background_notes.width() -  2 * (self.background_notes.width() // 5), 30)
        self.input_text_note.setFont(QtGui.QFont("intro", 14))
        self.input_text_note.textEdited.connect(self.Fill_preview_notes)

        
        self.preview_note_text = QLabel(self)
        self.preview_note_text.setGeometry(self.input_text_note.x(), self.background_notes.y() + self.background_notes.height() // 6, self.input_text_note.width(), self.input_text_note.y() - 20 - (self.background_notes.y() + self.background_notes.height() // 6))
        self.preview_note_text.setFont(QtGui.QFont("intro", 12))
        self.preview_note_text.setStyleSheet("color: white;")
        self.preview_note_text.setWordWrap(True)
        

        if edit:
            self.last_text = ndb.Read_text_index(self.Notes_list.indexFromItem(self.Notes_list.currentItem()).row())
            self.input_text_note.setText(self.last_text)
            self.preview_note_text.setText(self.last_text)
        self.preview_note_text.show()
        self.input_text_note.show()

        self.add_note_button = QPushButton(self)
        self.edit_note_button = QPushButton(self)
        if not edit:
            self.add_note_button.setGeometry(self.input_text_note.x(), self.input_text_note.y() + self.input_text_note.height() + 20, self.input_text_note.width() // 2 - 10, 30)
            self.add_note_button.setText("Добавить")
            self.add_note_button.show()
        else:
            self.edit_note_button.setGeometry(self.input_text_note.x(), self.input_text_note.y() + self.input_text_note.height() + 20, self.input_text_note.width() // 2 - 10, 30)
            self.edit_note_button.setText("Изменить")
            self.edit_note_button.show()

        self.cancel_note_button = QPushButton(self)
        if not edit:
            self.cancel_note_button.setGeometry(self.input_text_note.x() + self.input_text_note.width() // 2 + 10, self.add_note_button.y(), self.input_text_note.width() // 2 - 10, 30)
        else:
            self.cancel_note_button.setGeometry(self.input_text_note.x() + self.input_text_note.width() // 2 + 10, self.edit_note_button.y(), self.input_text_note.width() // 2 - 10, 30)
        self.cancel_note_button.setText("Отмена")
        self.cancel_note_button.show()

        self.delete_note_button = QPushButton(self)
        if edit:
            self.delete_note_button.setGeometry(self.input_text_note.x(), self.edit_note_button.y() + self.edit_note_button.height() + 20, self.input_text_note.width(), 30)
            self.delete_note_button.setText("Удалить заметку")
            self.delete_note_button.show()

    def Add_note_input(self):
        if not self.note_on_work:
            self.note_on_work = True
            self.Draw_input_note_menu()
            self.input_text_note.returnPressed.connect(self.Add_note)
            self.add_note_button.clicked.connect(self.Add_note)
            self.cancel_note_button.clicked.connect(self.Cancel_note)

    def Add_note(self):
        if len(self.input_text_note.text()) != 0:
            self.Notes_list.addItem(QListWidgetItem(fnt(self.input_text_note.text())))
            ndb.Add_to_data_base(self.input_text_note.text())
        self.input_text_note.clear()
        self.input_text_note.close()
        self.preview_note_text.clear()
        self.preview_note_text.close()

        self.background_notes.close()
        self.add_note_button.close()
        self.cancel_note_button.close()
        self.note_on_work = False

    def Cancel_note(self):
        self.input_text_note.clear()
        self.input_text_note.close()
        self.preview_note_text.clear()
        self.preview_note_text.close()

        self.background_notes.close()
        self.add_note_button.close()
        self.edit_note_button.close()
        self.cancel_note_button.close()
        self.delete_note_button.close()
        
        self.note_on_work = False

    def Edit_note_input(self):
        if not self.note_on_work:
            self.note_on_work = True
            self.Draw_input_note_menu(edit = True)
            self.input_text_note.returnPressed.connect(self.Edit_note)
            self.edit_note_button.clicked.connect(self.Edit_note)
            self.cancel_note_button.clicked.connect(self.Cancel_note)
            self.delete_note_button.clicked.connect(self.Delete_note)

    def Edit_note(self):
        if len(self.input_text_note.text()) == 0:
            self.Notes_list.currentItem().setText(self.last_text)
        else:
            self.Notes_list.currentItem().setText(fnt(self.input_text_note.text()))
            ndb.Edit_text_index(self.Notes_list.indexFromItem(self.Notes_list.currentItem()).row(), self.input_text_note.text())
            self.last_text = ""
        self.input_text_note.clear()
        self.input_text_note.close()
        self.preview_note_text.clear()
        self.preview_note_text.close()

        self.background_notes.close()
        self.edit_note_button.close()
        self.cancel_note_button.close()
        self.delete_note_button.close()
        self.note_on_work = False

    def Delete_note(self):
        self.Notes_list.takeItem(self.Notes_list.currentRow())
        ndb.Delete_index(self.Notes_list.indexFromItem(self.Notes_list.currentItem()).row())
        self.input_text_note.clear()
        self.input_text_note.close()
        self.preview_note_text.clear()
        self.preview_note_text.close()

        self.background_notes.close()
        self.edit_note_button.close()
        self.cancel_note_button.close()
        self.delete_note_button.close()
        self.note_on_work = False

    def Clear_notes_list(self):
        Are_U_Sure_Box = QMessageBox()
        Are_U_Sure_Box.move(self.DWIDTH // 2, self.DHEIGHT // 2)
        reply = QMessageBox.question(self, 'Уверены?',
            "Вы уверены что хотите очистить все заметки?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.Notes_list.clear()
            ndb.Clear_data_base()
        else:
            Are_U_Sure_Box.close()

    def Fill_preview_notes(self):
        self.preview_note_text.setText(self.input_text_note.text())

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