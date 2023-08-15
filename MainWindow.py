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
        self.show_fav_now = False

        self.Exit_Button = QPushButton(self)
        self.Exit_Button.setText("ВЫХОД")
        self.Exit_Button.setFont(QtGui.QFont("intro", 20))
        self.Exit_Button.adjustSize()
        self.Exit_Button.move(self.DWIDTH - self.Exit_Button.width() -
                              100, self.DHEIGHT - self.Exit_Button.height() - 110)
        self.Exit_Button.clicked.connect(self.Exit_func)
        self.Exit_Button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")

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

        self.Alarm_list = QListWidget(self)
        self.Alarm_list.setGeometry(
            100, 100, self.DWIDTH // 2 - self.Exit_Button.width() - 140, self.DHEIGHT - 210)
        self.Alarm_list.setFont(QtGui.QFont("intro", 35))
        self.Alarm_list.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px; color: #E5CCFF")

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
                if data[i][1] == 1:
                    self.Notes_list.addItem(QListWidgetItem(data[i][0]))
                    item = self.Notes_list.item(i)
                    item.setForeground(QtGui.QColor(229, 199, 1, 205))
                    self.Notes_list.insertItem(i, item)
                else:
                    self.Notes_list.addItem(QListWidgetItem(data[i][0]))

    def Draw_input_note_menu(self, edit: bool = False):
        self.background_notes = QLabel(self)
        self.background_notes.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5); border: none; border-radius: 5px;")
        self.background_notes.setGeometry(self.Notes_list.x() + self.Notes_list.width(
        ) // 2, self.Notes_list.y(), self.Notes_list.width() // 2, self.Notes_list.height())
        self.background_notes.show()

        self.input_text_note = QLineEdit(self)
        self.input_text_note.setGeometry(self.background_notes.x() + self.background_notes.width() // 5, self.background_notes.y(
        ) + 2 * (self.background_notes.height() // 3), self.background_notes.width() - 2 * (self.background_notes.width() // 5), 30)
        self.input_text_note.setFont(QtGui.QFont("intro", 14))
        self.input_text_note.textEdited.connect(self.Fill_preview_notes)

        self.preview_note_text = QLabel(self)
        self.preview_note_text.setGeometry(self.input_text_note.x(), self.background_notes.y() + self.background_notes.height(
        ) // 6, self.input_text_note.width(), self.input_text_note.y() - 20 - (self.background_notes.y() + self.background_notes.height() // 6))
        self.preview_note_text.setFont(QtGui.QFont("intro", 12))
        self.preview_note_text.setStyleSheet("color: white;")
        self.preview_note_text.setWordWrap(True)

        if edit:
            self.last_text = ndb.Read_text_index(
                self.Notes_list.indexFromItem(self.Notes_list.currentItem()).row())
            self.input_text_note.setText(self.last_text)
            self.preview_note_text.setText(self.last_text)
        self.preview_note_text.show()
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
        if not self.note_on_work:
            self.note_on_work = True
            self.Draw_input_note_menu()
            self.input_text_note.returnPressed.connect(self.Add_note)
            self.add_note_button.clicked.connect(self.Add_note)
            self.cancel_note_button.clicked.connect(self.Cancel_note)

    def Add_note(self):
        if len(self.input_text_note.text()) != 0:
            self.Notes_list.addItem(QListWidgetItem(
                fnt(self.input_text_note.text())))
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
            self.Draw_input_note_menu(edit=True)
            self.input_text_note.returnPressed.connect(self.Edit_note)
            self.edit_note_button.clicked.connect(self.Edit_note)
            self.cancel_note_button.clicked.connect(self.Cancel_note)
            self.delete_note_button.clicked.connect(self.Delete_note)

    def Edit_note(self):
        if len(self.input_text_note.text()) == 0:
            self.Notes_list.currentItem().setText(self.last_text)
        else:
            self.Notes_list.currentItem().setText(fnt(self.input_text_note.text()))
            ndb.Edit_text_index(self.Notes_list.indexFromItem(
                self.Notes_list.currentItem()).row(), self.input_text_note.text())
            self.last_text = ""
            self.Notes_list.clear()
            self.Check_data_base("Notes")
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
        ndb.Delete_index(self.Notes_list.indexFromItem(
            self.Notes_list.currentItem()).row())
        self.Notes_list.takeItem(self.Notes_list.currentRow())
        self.Notes_list.clear()
        self.Check_data_base("Notes")
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
                if data[i][1] == 1:
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

    def Draw_input_alarm_menu(self):
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
            self.Background_alarm.x() + 10, self.Background_alarm.y() + 10, 70, 70)
        self.Alarm_preview.setText("a")
        self.Alarm_preview.setFont(QtGui.QFont("intro", 35))
        self.Alarm_preview.setStyleSheet("color: white")
        self.Alarm_preview.show()

    def Add_alarm_input(self):
        if not self.Alarm_on_work:
            self.Draw_input_alarm_menu()
            self.Alarm_on_work = True

    def Add_alarm(self):
        self.Alarm_list.addItem(QListWidgetItem())

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
