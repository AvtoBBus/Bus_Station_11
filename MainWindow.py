import sys
import random
from Notes_formater import Format_note_name as fnn
import Notes_data_base as ndb
import Alarm_data_base as adb
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

        self.Exit_Button = QPushButton(self)
        self.Exit_Button.setText("ВЫХОД")
        self.Exit_Button.setFont(QtGui.QFont("intro", 20))
        self.Exit_Button.adjustSize()
        self.Exit_Button.move(self.DWIDTH - self.Exit_Button.width() -
                              100, self.DHEIGHT - self.Exit_Button.height() - 110)
        self.Exit_Button.clicked.connect(self.Exit_func)
        self.Exit_Button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")

        self.last_text = ""
        self.last_name = ""
        self.Note_on_work = False
        self.show_fav_now = False

        self.Notes_list = QListWidget(self)
        self.Notes_list.setGeometry(self.DWIDTH // 2 - 120, 100, self.DWIDTH //
                                    2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 130)
        self.Notes_list.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white;")
        self.Notes_list.setFont(QtGui.QFont("intro", 13))
        self.Check_data_base("Notes")
        self.Notes_list.itemDoubleClicked.connect(self.Edit_note_input)

        self.Add_note_button = QPushButton(self)
        self.Add_note_button.setGeometry(
            self.Notes_list.x() + self.Notes_list.width() + 5, 100, 50, 50)
        self.Add_note_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/add_button.png").scaled(35, 35)))
        self.Add_note_button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border-radius: 5px;")
        self.Add_note_button.setIconSize(QtCore.QSize(35, 35))
        self.Add_note_button.setToolTip("Добавить заметку")
        self.Add_note_button.clicked.connect(self.Add_note_input)

        self.Button_clear_notes_list = QPushButton(self)
        self.Button_clear_notes_list.setGeometry(self.Add_note_button.x(
        ), self.Add_note_button.y() + self.Add_note_button.height() + 5, 50, 50)
        self.Button_clear_notes_list.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/clear_button.png").scaled(35, 35)))
        self.Button_clear_notes_list.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border-radius: 5px;")
        self.Button_clear_notes_list.setIconSize(QtCore.QSize(35, 35))
        self.Button_clear_notes_list.setToolTip("Очистить список")
        self.Button_clear_notes_list.clicked.connect(self.Clear_notes_list)

        self.Add_note_to_favourites = QPushButton(self)
        self.Add_note_to_favourites.setGeometry(self.Button_clear_notes_list.x(
        ), self.Button_clear_notes_list.y() + self.Button_clear_notes_list.height() + 5, 50, 50)
        self.Add_note_to_favourites.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/favourite_button.png").scaled(35, 35)))
        self.Add_note_to_favourites.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border-radius: 5px;")
        self.Add_note_to_favourites.setIconSize(QtCore.QSize(35, 35))
        self.Add_note_to_favourites.setToolTip(
            "Добавить заметку в избранное\nУбрать из избранного")
        self.Add_note_to_favourites.clicked.connect(self.Add_Del_favourites)

        self.Show_favourites_button = QPushButton(self)
        self.Show_favourites_button.setGeometry(self.Add_note_to_favourites.x(
        ) + self.Add_note_to_favourites.width() + 5, self.Add_note_to_favourites.y(), 50, 50)
        self.Show_favourites_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/show_favourites_button.png").scaled(35, 35)))
        self.Show_favourites_button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border-radius: 5px;")
        self.Show_favourites_button.setIconSize(QtCore.QSize(35, 35))
        self.Show_favourites_button.setToolTip("Показать избранные заметки")
        self.Show_favourites_button.clicked.connect(self.Show_favourites)

        self.Notes_list_text = QLabel(self)
        self.Notes_list_text.setText("ЗАМЕТКИ")
        self.Notes_list_text.setFont(QtGui.QFont("intro", 20))
        self.Notes_list_text.setGeometry(
            self.DWIDTH // 2 - 120, 70, self.DWIDTH // 2 - self.Exit_Button.width(), 30)
        self.Notes_list_text.setAlignment(QtCore.Qt.AlignCenter)
        self.Notes_list_text.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white")

        self.Reminders_list = QListWidget(self)
        self.Reminders_list.setGeometry(self.DWIDTH // 2 - 120, self.DHEIGHT // 2 +
                                        30, self.DWIDTH // 2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 140)
        self.Reminders_list.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")

        self.Reminders_list_text = QLabel(self)
        self.Reminders_list_text.setText("НАПОМИНАНИЯ")
        self.Reminders_list_text.setFont(QtGui.QFont("intro", 20))
        self.Reminders_list_text.setGeometry(
            self.DWIDTH // 2 - 120, self.DHEIGHT // 2, self.DWIDTH // 2 - self.Exit_Button.width(), 30)
        self.Reminders_list_text.setAlignment(QtCore.Qt.AlignCenter)
        self.Reminders_list_text.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white")

        self.Alarm_on_work = False
        self.last_alarm_state = True

        self.Alarm_list = QListWidget(self)
        self.Alarm_list.setGeometry(
            100, 100, self.DWIDTH // 2 - self.Exit_Button.width() - 140, self.DHEIGHT - 210)
        self.Alarm_list.setFont(QtGui.QFont("intro", 35))
        self.Alarm_list.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")
        self.Check_data_base("Alarm")
        self.Alarm_list.itemDoubleClicked.connect(self.Edit_alarm_input)

        self.Add_alarm_button = QPushButton(self)
        self.Add_alarm_button.setGeometry(
            self.Alarm_list.x() - 55, self.Alarm_list.y(), 50, 50)
        self.Add_alarm_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/add_button.png").scaled(35, 35)))
        self.Add_alarm_button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border-radius: 5px;")
        self.Add_alarm_button.setIconSize(QtCore.QSize(35, 35))
        self.Add_alarm_button.setToolTip("Добавить будильник")
        self.Add_alarm_button.clicked.connect(self.Add_alarm_input)

        self.Button_clear_alarm_list = QPushButton(self)
        self.Button_clear_alarm_list = QPushButton(self)
        self.Button_clear_alarm_list.setGeometry(self.Add_alarm_button.x(
        ), self.Add_alarm_button.y() + self.Add_alarm_button.height() + 5, 50, 50)
        self.Button_clear_alarm_list.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/clear_button.png").scaled(35, 35)))
        self.Button_clear_alarm_list.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border-radius: 5px;")
        self.Button_clear_alarm_list.setIconSize(QtCore.QSize(35, 35))
        self.Button_clear_alarm_list.setToolTip("Очистить список")
        self.Button_clear_alarm_list.clicked.connect(self.Clear_alarm_list)

        self.Alarm_list_text = QLabel(self)
        self.Alarm_list_text.setText("БУДИЛЬНИКИ")
        self.Alarm_list_text.setFont(QtGui.QFont("intro", 20))
        self.Alarm_list_text.setGeometry(
            100, 70, self.Alarm_list.width(), 30)
        self.Alarm_list_text.setAlignment(QtCore.Qt.AlignCenter)
        self.Alarm_list_text.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: white")

        self.showFullScreen()

    def Exit_func(self):
        self.Exit_Button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")
        Are_U_Sure_Box = QMessageBox()
        Are_U_Sure_Box.move(self.DWIDTH // 2, self.DHEIGHT // 2)
        reply = QMessageBox.question(self, 'Уверены?',
                                     "Вы уверены что хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            Are_U_Sure_Box.close()

    def Check_data_base(self, db_type: str):
        if db_type == "Notes":
            data = ndb.Read_full()
            if len(data) == 0:
                return
            for i in range(len(data)):
                if data[i][2] == 1:
                    self.Notes_list.addItem(QListWidgetItem(data[i][0]))
                    item = self.Notes_list.item(i)
                    item.setForeground(QtGui.QColor(229, 199, 1, 205))
                    self.Notes_list.insertItem(i, item)
                else:
                    self.Notes_list.addItem(QListWidgetItem(data[i][0]))
        elif db_type == "Alarm":
            data = adb.Read_full()
            if len(data) == 0:
                return
            for i in range(len(data)):
                item = QListWidgetItem(data[i][0])
                if data[i][2] == 1:
                    item.setForeground(QtGui.QColor(102, 255, 178, 255))
                else:
                    item.setForeground(QtGui.QColor(229, 204, 255, 255))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.Alarm_list.addItem(item)

    def Draw_input_note_menu(self, edit: bool = False):
        self.background_notes = QLabel(self)
        self.background_notes.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")
        self.background_notes.setGeometry(self.Notes_list.x() + self.Notes_list.width(
        ) // 2, self.Notes_list.y(), self.Notes_list.width() // 2, self.Notes_list.height())
        self.background_notes.show()

        self.name_text = QLabel(self)
        self.name_text.setText("Name:")
        self.name_text.setGeometry(self.background_notes.x() + self.background_notes.width() // 15, self.background_notes.y(
        ) + self.background_notes.height() // 10, self.background_notes.width() // 6, 30)
        self.name_text.setFont(QtGui.QFont("intro", 13))
        self.name_text.setStyleSheet("color: white")
        self.name_text.show()

        self.text_text = QLabel(self)
        self.text_text.setText("Text:")
        self.text_text.setGeometry(self.name_text.x(), self.name_text.y(
        ) + self.name_text.height() + 5, self.background_notes.width() // 6, 30)
        self.text_text.setFont(QtGui.QFont("intro", 13))
        self.text_text.setStyleSheet("color: white")
        self.text_text.show()

        self.input_name_note = QLineEdit(self)
        self.input_name_note.setGeometry(self.name_text.x() + self.name_text.width() + 15, self.name_text.y(
        ), self.background_notes.width() - 2 * (self.background_notes.width() // 5), 30)
        self.input_name_note.setFont(QtGui.QFont("intro", 14))
        self.input_name_note.setStyleSheet(
            "background-color: rgba(224, 224, 224, 1); border: none; border-radius: 5px;")

        self.input_text_note = QTextEdit(self)
        self.input_text_note.setGeometry(self.input_name_note.x(), self.input_name_note.y(
        ) + self.input_name_note.height() + 5, self.background_notes.width() - 2 * (self.background_notes.width() // 5), self.background_notes.height() // 2)
        self.input_text_note.setFont(QtGui.QFont("intro", 14))
        self.input_text_note.textChanged.connect(self.Format_text_note)
        self.input_text_note.setStyleSheet(
            "background-color: rgba(224, 224, 224, 1); border: none; border-radius: 5px;")

        if edit:
            self.last_text = ndb.Read_text_index(
                self.Notes_list.indexFromItem(self.Notes_list.currentItem()).row())
            self.last_name = ndb.Read_name_index(
                self.Notes_list.indexFromItem(self.Notes_list.currentItem()).row())
            self.input_text_note.setText(self.last_text)
            self.input_name_note.setText(self.last_name)
        self.input_name_note.show()
        self.input_text_note.show()

        self.add_note_button = QPushButton(self)
        self.edit_note_button = QPushButton(self)
        if not edit:
            self.add_note_button.setGeometry(self.input_text_note.x(), self.input_text_note.y(
            ) + self.input_text_note.height() + 20, self.input_text_note.width() // 2 - 10, 30)
            self.add_note_button.setText("Добавить")
            self.add_note_button.show()
        else:
            self.edit_note_button.setGeometry(self.input_text_note.x(), self.input_text_note.y(
            ) + self.input_text_note.height() + 20, self.input_text_note.width() // 2 - 10, 30)
            self.edit_note_button.setText("Изменить")
            self.edit_note_button.show()

        self.cancel_note_button = QPushButton(self)
        if not edit:
            self.cancel_note_button.setGeometry(self.input_text_note.x() + self.input_text_note.width(
            ) // 2 + 10, self.add_note_button.y(), self.input_text_note.width() // 2 - 10, 30)
        else:
            self.cancel_note_button.setGeometry(self.input_text_note.x() + self.input_text_note.width(
            ) // 2 + 10, self.edit_note_button.y(), self.input_text_note.width() // 2 - 10, 30)
        self.cancel_note_button.setText("Отмена")
        self.cancel_note_button.show()

        self.delete_note_button = QPushButton(self)
        if edit:
            self.delete_note_button.setGeometry(self.input_text_note.x(), self.edit_note_button.y(
            ) + self.edit_note_button.height() + 20, self.input_text_note.width(), 30)
            self.delete_note_button.setText("Удалить заметку")
            self.delete_note_button.show()

    def Add_note_input(self):
        if not self.Note_on_work:
            self.Note_on_work = True
            self.Draw_input_note_menu()
            self.add_note_button.clicked.connect(self.Add_note)
            self.cancel_note_button.clicked.connect(self.Cancel_note)

    def Add_note(self):
        if len(self.input_name_note.text()) != 0:
            self.Notes_list.addItem(QListWidgetItem(
                fnn(self.input_name_note.text())))
            ndb.Add_to_data_base(self.input_name_note.text(),
                                 self.input_text_note.toPlainText())
        self.Cancel_note()
        self.Note_on_work = False

    def Cancel_note(self):
        self.input_text_note.clear()
        self.input_name_note.clear()

        self.name_text.close()
        self.text_text.close()
        self.input_text_note.close()
        self.input_name_note.close()
        self.background_notes.close()
        self.add_note_button.close()
        self.edit_note_button.close()
        self.cancel_note_button.close()
        self.delete_note_button.close()

        self.Note_on_work = False

    def Edit_note_input(self):
        if not self.Note_on_work:
            self.Note_on_work = True
            self.Draw_input_note_menu(edit=True)
            self.edit_note_button.clicked.connect(self.Edit_note)
            self.cancel_note_button.clicked.connect(self.Cancel_note)
            self.delete_note_button.clicked.connect(self.Delete_note)

    def Edit_note(self):
        if len(self.input_name_note.text()) == 0:
            self.Notes_list.currentItem().setText(self.last_name)
        else:
            self.Notes_list.currentItem().setText(fnn(self.input_name_note.text()))
            ndb.Edit_text_index(self.Notes_list.indexFromItem(
                self.Notes_list.currentItem()).row(), self.input_name_note.text(), self.input_text_note.toPlainText())
            self.last_text = ""
            self.last_name = ""
            self.Notes_list.clear()
            self.Check_data_base("Notes")
        self.Cancel_note()

    def Delete_note(self):
        ndb.Delete_index(self.Notes_list.currentRow())
        self.Notes_list.takeItem(self.Notes_list.currentRow())
        self.Notes_list.clear()
        self.Check_data_base("Notes")
        self.Cancel_note()
        self.Note_on_work = False

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

    def Add_Del_favourites(self):
        index = self.Notes_list.currentRow()
        if index >= 0:
            if not ndb.Check_favourite(index):
                self.Notes_list.currentItem().setForeground(QtGui.QColor(229, 199, 1, 205))
                ndb.Add_to_favourite(index, 1)
            else:
                self.Notes_list.currentItem().setForeground(QtGui.QColor(255, 255, 255))
                ndb.Add_to_favourite(index, 0)

    def Show_favourites(self):
        if not self.show_fav_now:
            self.Notes_list.clear()
            data = ndb.Read_full()
            for i in range(len(data)):
                if data[i][2] == 1:
                    self.Notes_list.addItem(QListWidgetItem(data[i][0]))
            if self.Notes_list.count() == 0:
                self.Notes_list.addItem(QListWidgetItem("Empty("))
            else:
                for i in range(self.Notes_list.count()):
                    item = self.Notes_list.item(i)
                    item.setForeground(QtGui.QColor(229, 199, 1, 205))
                    self.Notes_list.insertItem(i, item)
            self.show_fav_now = True
        else:
            self.Notes_list.clear()
            self.Check_data_base("Notes")
            self.show_fav_now = False

    def Draw_input_alarm_menu(self, edit=False):
        self.Alarm_list.setGeometry(100, 100,
                                    self.DWIDTH // 2 - self.Exit_Button.width() - 140, (self.DHEIGHT - 210) // 2)
        self.Background_alarm = QLabel(self)
        self.Background_alarm.setGeometry(self.Alarm_list.x(), self.Alarm_list.y(
        ) + self.Alarm_list.height(), self.Alarm_list.width(), self.Alarm_list.height())
        self.Background_alarm.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.77); border: none; border-radius: 5px;")
        self.Background_alarm.show()

        self.Alarm_preview = QLabel(self)
        self.Alarm_preview.setGeometry(
            self.Background_alarm.x() + self.Background_alarm.width() // 7, self.Background_alarm.y() + self.Background_alarm.height() // 6, 170, 70)
        if not edit:
            self.Alarm_preview.setText("00:00")
        else:
            self.Alarm_preview.setText(
                adb.Read_time_index(self.Alarm_list.currentRow()))
            self.last_time = self.Alarm_preview.text()
        self.Alarm_preview.setFont(QtGui.QFont("intro", 35))
        self.Alarm_preview.setStyleSheet("color: white")
        self.Alarm_preview.show()

        self.Alarm_hour_text = QLabel(self)
        self.Alarm_hour_text.setGeometry(self.Alarm_preview.x(
        ) + self.Alarm_preview.width() + 15, self.Alarm_preview.y(), 50, 30)
        self.Alarm_hour_text.setFont(QtGui.QFont("intro", 14))
        self.Alarm_hour_text.setText("HH")
        self.Alarm_hour_text.setStyleSheet("color: white")
        self.Alarm_hour_text.show()

        self.Alarm_hour_input = QComboBox(self)
        self.Alarm_hour_input.setGeometry(self.Alarm_hour_text.x(
        ), self.Alarm_hour_text.y() + self.Alarm_hour_text.height() + 5, 70, 30)
        self.Alarm_hour_input.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                        "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
        self.Alarm_hour_input.setFont(QtGui.QFont("intro", 13))
        if edit:
            self.Alarm_hour_input.setCurrentIndex(
                int(adb.Read_time_index(self.Alarm_list.currentRow()).split(":")[0]))
        self.Alarm_hour_input.setStyleSheet(
            "background-color: rgba(224, 224, 224, 0.2); border: none; border-radius: 5px;color: white")
        self.Alarm_hour_input.show()
        self.Alarm_hour_input.currentTextChanged.connect(
            self.Fill_alarm_preview)

        self.Alarm_minute_text = QLabel(self)
        self.Alarm_minute_text.setGeometry(self.Alarm_hour_input.x(
        ) + self.Alarm_hour_input.width() + 15, self.Alarm_hour_text.y(), 50, 30)
        self.Alarm_minute_text.setFont(QtGui.QFont("intro", 14))
        self.Alarm_minute_text.setText("MM")
        self.Alarm_minute_text.setStyleSheet("color: white")
        self.Alarm_minute_text.show()

        self.Alarm_minute_input = QComboBox(self)
        self.Alarm_minute_input.setGeometry(self.Alarm_minute_text.x(
        ), self.Alarm_minute_text.y() + self.Alarm_minute_text.height() + 5, 70, 30)
        self.Alarm_minute_input.addItems(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                                          "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                                          "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                                          "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
                                          "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                                          "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"])
        self.Alarm_minute_input.setFont(QtGui.QFont("intro", 13))
        self.Alarm_minute_input.setStyleSheet(
            "background-color: rgba(224, 224, 224, 0.2); border: none; border-radius: 5px;color: white")
        if edit:
            self.Alarm_minute_input.setCurrentIndex(
                int(adb.Read_time_index(self.Alarm_list.currentRow()).split(":")[1]))
        self.Alarm_minute_input.show()
        self.Alarm_minute_input.currentTextChanged.connect(
            self.Fill_alarm_preview)

        self.add_alarm_button = QPushButton(self)
        self.add_alarm_button.setGeometry(
            self.Alarm_minute_input.x() + self.Alarm_minute_input.width() + 20, self.Alarm_minute_input.y(), (self.Background_alarm.x() + self.Background_alarm.width() - self.Alarm_minute_input.x() - self.Alarm_minute_input.width()) // 2 + 10, 30)
        self.add_alarm_button.setText("Добавить будильник")
        self.add_alarm_button.setFont(QtGui.QFont("intro", 8))

        self.edit_alarm_button = QPushButton(self)
        self.edit_alarm_button.setGeometry(
            self.add_alarm_button.x(), self.add_alarm_button.y(), self.add_alarm_button.width(), self.add_alarm_button.height())
        self.edit_alarm_button.setText("Изменить")
        self.edit_alarm_button.setFont(QtGui.QFont("intro", 8))

        self.cancel_alarm_button = QPushButton(self)
        self.cancel_alarm_button.setGeometry(self.add_alarm_button.x(), self.add_alarm_button.y(
        ) + self.add_alarm_button.height() + 10, self.add_alarm_button.width(), 30)
        self.cancel_alarm_button.setText("Отменить")
        self.cancel_alarm_button.setFont(QtGui.QFont("intro", 8))
        self.cancel_alarm_button.show()

        self.delete_alarm_button = QPushButton(self)
        self.delete_alarm_button.setGeometry(self.cancel_alarm_button.x(
        ), self.cancel_alarm_button.y() + self.cancel_alarm_button.height() + 10, self.add_alarm_button.width(), 30)
        self.delete_alarm_button.setText("Удалить будильник")
        self.delete_alarm_button.setFont(QtGui.QFont("intro", 8))

        if edit:
            self.edit_alarm_button.show()
            self.delete_alarm_button.show()
        else:
            self.add_alarm_button.show()

        self.Alarm_activated = QCheckBox(self)
        self.Alarm_activated.setGeometry(self.add_alarm_button.x(
        ), self.Background_alarm.y() + 4 * (self.Background_alarm.height() // 5), 150, 50)
        self.Alarm_activated.setFont(QtGui.QFont("intro", 13))
        if edit:
            if not adb.Check_activated(self.Alarm_list.currentRow()):
                self.Alarm_activated.setChecked(False)
                self.last_alarm_state = False
                self.Alarm_activated.setText("ОТКЛЮЧЕН")
                self.Alarm_activated.setStyleSheet("color: #FF6666")
            else:
                self.Alarm_activated.setChecked(True)
                self.last_alarm_state = True
                self.Alarm_activated.setText("ВКЛЮЧЕН")
                self.Alarm_activated.setStyleSheet("color: #66FF66")
        else:
            self.Alarm_activated.setChecked(True)
            self.last_alarm_state = True
            self.Alarm_activated.setText("ВКЛЮЧЕН")
            self.Alarm_activated.setStyleSheet("color: #66FF66")
        self.Alarm_activated.show()
        self.Alarm_activated.stateChanged.connect(
            self.Change_color_alarm_activate)

    def Add_alarm_input(self):
        if not self.Alarm_on_work:
            self.Draw_input_alarm_menu()
            self.Alarm_on_work = True
            self.add_alarm_button.clicked.connect(self.Add_alarm)
            self.cancel_alarm_button.clicked.connect(self.Cancel_alarm)

    def Add_alarm(self):
        item = QListWidgetItem(self.Alarm_preview.text())
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        active = 1
        item.setForeground(QtGui.QColor(102, 255, 178, 255))
        if not self.Alarm_activated.isChecked():
            active = 0
            item.setForeground(QtGui.QColor(229, 204, 255, 255))
        self.Alarm_list.addItem(item)
        adb.Add_to_data_base(self.Alarm_preview.text(),
                             f"{random.randint(1,10)}",
                             active)
        self.Alarm_list.clear()
        self.Check_data_base("Alarm")
        self.Cancel_alarm()

    def Cancel_alarm(self):
        self.Background_alarm.close()
        self.add_alarm_button.close()
        self.edit_alarm_button.close()
        self.cancel_alarm_button.close()
        self.delete_alarm_button.close()
        self.Alarm_minute_input.close()
        self.Alarm_hour_input.close()
        self.Alarm_hour_text.close()
        self.Alarm_minute_text.close()
        self.Alarm_preview.close()
        self.Alarm_activated.close()
        self.Alarm_list.setGeometry(
            100, 100, self.DWIDTH // 2 - self.Exit_Button.width() - 140, self.DHEIGHT - 210)

        self.Alarm_on_work = False

    def Edit_alarm_input(self):
        if not self.Alarm_on_work:
            self.Alarm_on_work = True
            self.Draw_input_alarm_menu(edit=True)
            self.edit_alarm_button.clicked.connect(self.Edit_alarm)
            self.cancel_alarm_button.clicked.connect(self.Cancel_alarm)
            self.delete_alarm_button.clicked.connect(self.Delete_alarm)

    def Edit_alarm(self):
        adb.Edit_alarm_index(self.Alarm_list.currentRow(
        ), self.Alarm_preview.text(), f"{random.randint(1,10)}")
        adb.Activate_alarm(self.Alarm_list.currentRow())
        self.Alarm_list.clear()
        self.Check_data_base("Alarm")
        self.Cancel_alarm()

    def Delete_alarm(self):
        adb.Delete_index(self.Alarm_list.currentRow())
        self.Alarm_list.takeItem(self.Alarm_list.currentRow())
        self.Alarm_list.clear()
        self.Check_data_base("Alarm")
        self.Cancel_alarm()
        self.Alarm_on_work = False

    def Clear_alarm_list(self):
        Are_U_Sure_Box = QMessageBox()
        Are_U_Sure_Box.move(self.DWIDTH // 2, self.DHEIGHT // 2)
        reply = QMessageBox.question(self, 'Уверены?',
                                     "Вы уверены что хотите удалить все будильники?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.Alarm_list.clear()
            adb.Clear_data_base()
        else:
            Are_U_Sure_Box.close()

    def Format_text_note(self):
        if len(self.input_text_note.toPlainText()) > 50:
            if len(self.input_text_note.toPlainText()) > 60:
                self.input_text_note.setFont(QtGui.QFont("intro", 11))
            else:
                self.input_text_note.setFont(QtGui.QFont("intro", 12))

    def Fill_alarm_preview(self):
        self.Alarm_preview.setText(
            f"{str(self.Alarm_hour_input.currentIndex()).zfill(2)}:{str(self.Alarm_minute_input.currentIndex()).zfill(2)}")

    def Change_color_alarm_activate(self):
        if self.last_alarm_state:
            self.Alarm_activated.setChecked(False)
            self.Alarm_activated.setText("ОТКЛЮЧЕН")
            self.Alarm_activated.setStyleSheet("color: #FF6666")
            self.last_alarm_state = False
        else:
            self.Alarm_activated.setChecked(True)
            self.Alarm_activated.setText("ВКЛЮЧЕН")
            self.Alarm_activated.setStyleSheet("color: #66FF66")
            self.last_alarm_state = True

    def mouseMoveEvent(self, event):
        if event.x() > self.DWIDTH - self.Exit_Button.width() - 105 and event.x() < self.DWIDTH - 95 and event.y() > self.DHEIGHT - self.Exit_Button.height() - 115 and event.y() < self.DHEIGHT - 105:
            self.Exit_Button.setStyleSheet(
                "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: red")
        else:
            self.Exit_Button.setStyleSheet(
                "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.setObjectName("MainWindow")
    window.setStyleSheet(
        "#MainWindow{border-image:url(images/background.gif)}")
    window.show()
    sys.exit(app.exec_())
