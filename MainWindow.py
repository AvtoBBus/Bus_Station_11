import sys
import time
import os
from datetime import datetime
from typing import Any
from plyer import notification
import Send_notification
from datetime import datetime
import Text_formater
import Convert_date_time
from Read_alarm_misuc import read_alarm_music as ram
from Alarm_queue import Alarm_queue
from Reminders_queue import Reminders_queue
import Notes_data_base as ndb
import Alarm_data_base as adb
import Reminder_data_base as rdb
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtMultimedia import *


class clockThread(QtCore.QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        while True:
            self.mainwindow.clock.setText(
                QtCore.QDateTime().currentDateTime().toString('HH:mm dd/MM/yyyy'))
            time.sleep(0.5)


class alarmThread(QtCore.QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        while True:
            self.alarm_list = adb.Read_full_time()
            if len(self.alarm_list) != 0:
                aq = Alarm_queue(self.alarm_list)
                nearest_alarm = aq.get_first_in_queue()
                if nearest_alarm[1] == 1:
                    if adb.Check_activated(nearest_alarm[0]):
                        self.alarm_ring(nearest_alarm)
                aq.clear_queue()
                self.alarm_list.clear()
            time.sleep(1)

    def alarm_ring(self, nearest_alarm: list[int, int]) -> None:
        for i in range(59):
            time.sleep(1)
        self.mainwindow.Alarm_start_ring(
            nearest_alarm[0], self.alarm_list[nearest_alarm[0]])
        time.sleep(2)


class remindersThread(QtCore.QThread):
    was_active = []
    start_time = datetime.now()

    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        while True:
            if (datetime.now() - self.start_time).days == 1:
                self.was_active.clear()
                self.start_time = datetime.now()
            self.creature_date_list = rdb.Read_full_date()
            if len(self.creature_date_list) != 0:
                rem_list = rdb.Read_full()
                rq = Reminders_queue(self.convert_list(rem_list))
                if rq.get_first_every_day() != None:
                    if rq.get_first_every_day()[2] == 1:
                        self.reminder_start_ring(rq.get_first_every_day()[0])
                if rq.get_first_every_week() != None:
                    if rq.get_first_every_week()[2] == 0:
                        if self.calc_date(rq.get_first_every_day()):
                            self.reminder_start_ring(
                                rq.get_first_every_week()[0])
                if rq.get_first_every_year() != None:
                    if rq.get_first_every_year()[2] == 0:
                        if self.calc_date(rq.get_first_every_year()):
                            self.reminder_start_ring(
                                rq.get_first_every_year()[0])
                if rq.get_first_once() != None:
                    if rq.get_first_once()[2] == 0:
                        if self.calc_date(rq.get_first_once()):
                            self.reminder_start_ring(
                                rq.get_first_once()[0])
                rq.clear_queue()
            time.sleep(1)

    def reminder_start_ring(self, reminder_index: int):
        if not self.check_active(reminder_index):
            for i in range(59):
                time.sleep(1)
            self.mainwindow.Reminder_start_ring(reminder_index)
            self.was_active.append(reminder_index)
            time.sleep(5)

    def check_active(self, reminder_index: int) -> bool:
        for elem in self.was_active:
            if elem == reminder_index:
                return True
        return False

    def calc_date(self, input: list[int, str, int]) -> bool:
        le = ""
        with open("last_entry.txt", 'r', encoding="utf-8") as file:
            le = file.read()
        le = le.split("T")[0]
        le = le.replace("-", ".")
        now_date = datetime.now().isoformat().split("T")[0]
        now_date = now_date.replace("-", ".")
        if (datetime.strptime(now_date, "%Y.%m.%d") - datetime.strptime(le, "%Y.%m.%d")).days == 1:
            return True
        return False

    def convert_list(self, input_list: list[str, str, int, str]) -> list[str, str]:
        result_list = []
        for elem in input_list:
            result_list.append(elem[3].split("$"))
        return result_list


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

        self.clock = QLabel(self)
        self.clock.setObjectName("clock")
        self.clock.setGeometry(13 * self.DWIDTH // 32,
                               10, self.DHEIGHT // 4, 50)
        self.clock.setFont(QtGui.QFont("intro", 20))
        self.clockthread = clockThread(mainwindow=self)
        self.clockthread.start()
        self.clock.show()

        self.Exit_Button = QPushButton(self)
        self.Exit_Button.setText("ВЫХОД")
        self.Exit_Button.setFont(QtGui.QFont("intro", 20))
        self.Exit_Button.adjustSize()
        self.Exit_Button.move(self.DWIDTH - self.Exit_Button.width() -
                              100, self.DHEIGHT - self.Exit_Button.height() - 110)
        self.Exit_Button.clicked.connect(self.Exit_func)
        self.Exit_Button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")

        self.Setting_button = QPushButton(self)
        self.Setting_button.setObjectName("Setting_button")
        self.Setting_button.setGeometry(10, 10, 50, 50)
        self.Setting_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/setting_button.png").scaled(35, 35)))
        self.Setting_button.setIconSize(QtCore.QSize(35, 35))
        self.Setting_button.setToolTip("Настройки")
        # self.Setting_button.clicked.connect(self.Clear_notes_list)
        self.Setting_button.show()

        self.last_text = ""
        self.last_name = ""
        self.Note_on_work = False
        self.show_fav_now = False

        self.Notes_list = QListWidget(self)
        self.Notes_list.setGeometry(self.DWIDTH // 2 - 120, 100, self.DWIDTH //
                                    2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 130)
        self.Notes_list.setFont(QtGui.QFont("intro", 13))
        self.Check_data_base("Notes")
        self.Notes_list.itemDoubleClicked.connect(self.Edit_note_input)

        self.Add_note_button = QPushButton(self)
        self.Add_note_button.setObjectName("Add_button")
        self.Add_note_button.setGeometry(
            self.Notes_list.x() + self.Notes_list.width() + 5, 100, 50, 50)
        self.Add_note_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/add_button.png").scaled(35, 35)))
        self.Add_note_button.setIconSize(QtCore.QSize(35, 35))
        self.Add_note_button.setToolTip("Добавить заметку")
        self.Add_note_button.clicked.connect(self.Add_note_input)

        self.Button_clear_notes_list = QPushButton(self)
        self.Button_clear_notes_list.setObjectName("Clear_list_button")
        self.Button_clear_notes_list.setGeometry(self.Add_note_button.x(
        ), self.Add_note_button.y() + self.Add_note_button.height() + 5, 50, 50)
        self.Button_clear_notes_list.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/clear_button.png").scaled(35, 35)))
        self.Button_clear_notes_list.setIconSize(QtCore.QSize(35, 35))
        self.Button_clear_notes_list.setToolTip("Очистить список")
        self.Button_clear_notes_list.clicked.connect(self.Clear_notes_list)

        self.Add_note_to_favourites = QPushButton(self)
        self.Add_note_to_favourites.setObjectName("Add_to_favourite")
        self.Add_note_to_favourites.setGeometry(self.Button_clear_notes_list.x(
        ), self.Button_clear_notes_list.y() + self.Button_clear_notes_list.height() + 5, 50, 50)
        self.Add_note_to_favourites.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/favourite_button.png").scaled(35, 35)))
        self.Add_note_to_favourites.setIconSize(QtCore.QSize(35, 35))
        self.Add_note_to_favourites.setToolTip(
            "Добавить заметку в избранное\nУбрать из избранного")
        self.Add_note_to_favourites.clicked.connect(self.Add_Del_favourites)

        self.Show_favourites_button = QPushButton(self)
        self.Show_favourites_button.setObjectName("Show_favourites")
        self.Show_favourites_button.setGeometry(self.Add_note_to_favourites.x(
        ) + self.Add_note_to_favourites.width() + 5, self.Add_note_to_favourites.y(), 50, 50)
        self.Show_favourites_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/show_favourites_button.png").scaled(35, 35)))
        self.Show_favourites_button.setIconSize(QtCore.QSize(35, 35))
        self.Show_favourites_button.setToolTip("Показать избранные заметки")
        self.Show_favourites_button.clicked.connect(self.Show_favourites)

        self.Notes_list_text = QLabel(self)
        self.Notes_list_text.setObjectName("Zone_name")
        self.Notes_list_text.setText("ЗАМЕТКИ")
        self.Notes_list_text.setFont(QtGui.QFont("intro", 20))
        self.Notes_list_text.setGeometry(
            self.DWIDTH // 2 - 120, 70, self.DWIDTH // 2 - self.Exit_Button.width(), 30)
        self.Notes_list_text.setAlignment(QtCore.Qt.AlignCenter)

        self.Reminder_on_work = False
        self.last_reminder_state = True
        self.Reminder_player = QMediaPlayer(self)

        self.Reminders_list = QListWidget(self)
        self.Reminders_list.setGeometry(self.DWIDTH // 2 - 120, self.DHEIGHT // 2 +
                                        30, self.DWIDTH // 2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 140)
        self.Reminders_list.itemDoubleClicked.connect(self.Edit_reminder_input)
        self.Check_data_base("Reminders")

        self.reminder_thread = remindersThread(self)
        self.reminder_thread.start()

        self.Reminders_list_text = QLabel(self)
        self.Reminders_list_text.setText("НАПОМИНАНИЯ")
        self.Reminders_list_text.setObjectName("Zone_name")
        self.Reminders_list_text.setFont(QtGui.QFont("intro", 20))
        self.Reminders_list_text.setGeometry(
            self.DWIDTH // 2 - 120, self.DHEIGHT // 2, self.DWIDTH // 2 - self.Exit_Button.width(), 30)
        self.Reminders_list_text.setAlignment(QtCore.Qt.AlignCenter)

        self.Add_reminder_button = QPushButton(self)
        self.Add_reminder_button.setObjectName("Add_button")
        self.Add_reminder_button.setGeometry(self.Reminders_list.x(
        ) + self.Reminders_list.width() + 5, self.Reminders_list.y(), 50, 50)
        self.Add_reminder_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/add_button.png").scaled(35, 35)))
        self.Add_reminder_button.setIconSize(QtCore.QSize(35, 35))
        self.Add_reminder_button.setToolTip("Добавить напоминание")
        self.Add_reminder_button.clicked.connect(self.Add_reminder_input)

        self.Reminder_notification_background = QLabel(self)
        self.Reminder_notification_background.setObjectName(
            "Background_notification")
        self.Reminder_notification_background.setFont(QtGui.QFont("intro", 20))

        self.Reminder_notification_annotation = QLabel(self)
        self.Reminder_notification_annotation.setObjectName("Text_annotation")
        self.Reminder_notification_annotation.setFont(QtGui.QFont("intro", 13))
        self.Reminder_notification_annotation.setAlignment(
            QtCore.Qt.AlignCenter)
        self.Reminder_notification_annotation.setText("НАПОМИНАНИЕ")

        self.Reminder_notification_text = QLabel(self)
        self.Reminder_notification_text.setObjectName("Reminder_text")
        self.Reminder_notification_text.setFont(QtGui.QFont("intro", 13))
        self.Reminder_notification_text.setAlignment(
            QtCore.Qt.AlignCenter)
        self.Reminder_notification_text.setWordWrap(True)

        self.Reminder_close_button = QPushButton(self)
        self.Reminder_close_button.setObjectName("Stop_notification_button")
        self.Reminder_close_button.setFont(QtGui.QFont("intro", 13))
        self.Reminder_close_button.setText("ЗАКРЫТЬ")

        self.Reminder_notification_background.close()
        self.Reminder_notification_text.close()
        self.Reminder_notification_annotation.close()
        self.Reminder_close_button.close()

        self.Alarm_on_work = False
        self.Alarm_music_play = False
        self.last_alarm_state = True
        self.Alarm_music_path = os.path.abspath("alarm_sound")
        self.Alarm_player = QMediaPlayer(self)

        self.Alarm_list = QListWidget(self)
        self.Alarm_list.setGeometry(
            100, 100, self.DWIDTH // 2 - self.Exit_Button.width() - 140, self.DHEIGHT - 210)
        self.Alarm_list.setFont(QtGui.QFont("intro", 35))
        self.Check_data_base("Alarm")

        self.alarm_thread = alarmThread(mainwindow=self)
        self.alarm_thread.start()

        self.Alarm_list.itemDoubleClicked.connect(self.Edit_alarm_input)

        self.Add_alarm_button = QPushButton(self)
        self.Add_alarm_button.setObjectName("Add_button")
        self.Add_alarm_button.setGeometry(
            self.Alarm_list.x() - 55, self.Alarm_list.y(), 50, 50)
        self.Add_alarm_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/add_button.png").scaled(35, 35)))
        self.Add_alarm_button.setIconSize(QtCore.QSize(35, 35))
        self.Add_alarm_button.setToolTip("Добавить будильник")
        self.Add_alarm_button.clicked.connect(self.Add_alarm_input)

        self.Button_clear_alarm_list = QPushButton(self)
        self.Button_clear_alarm_list.setObjectName("Clear_list_button")
        self.Button_clear_alarm_list.setGeometry(self.Add_alarm_button.x(
        ), self.Add_alarm_button.y() + self.Add_alarm_button.height() + 5, 50, 50)
        self.Button_clear_alarm_list.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/clear_button.png").scaled(35, 35)))
        self.Button_clear_alarm_list.setIconSize(QtCore.QSize(35, 35))
        self.Button_clear_alarm_list.setToolTip("Очистить список")
        self.Button_clear_alarm_list.clicked.connect(self.Clear_alarm_list)

        self.Alarm_list_text = QLabel(self)
        self.Alarm_list_text.setObjectName("Zone_name")
        self.Alarm_list_text.setText("БУДИЛЬНИКИ")
        self.Alarm_list_text.setFont(QtGui.QFont("intro", 20))
        self.Alarm_list_text.setGeometry(
            100, 70, self.Alarm_list.width(), 30)
        self.Alarm_list_text.setAlignment(QtCore.Qt.AlignCenter)

        self.Alarm_notification_background = QLabel(self)
        self.Alarm_notification_background.setObjectName(
            "Background_notification")
        self.Alarm_notification_background.setGeometry(self.clock.x(
        ) + self.clock.width() + 30, -1 * self.clock.y(), self.Notes_list.x() + self.Notes_list.width() - self.clock.x() - self.clock.width() - 30, + self.clock.height())
        self.Alarm_notification_background.setFont(QtGui.QFont("intro", 18))

        self.Alarm_notification_stop_button = QPushButton(self)
        self.Alarm_notification_stop_button.setObjectName(
            "Stop_notification_button")
        self.Alarm_notification_stop_button.setGeometry(self.Alarm_notification_background.x() + self.Alarm_notification_background.width() // 2 + 20, self.Alarm_notification_background.y(
        ) + 5, self.Alarm_notification_background.width() // 2 - 40, self.Alarm_notification_background.height() - 10)
        self.Alarm_notification_stop_button.setText("Остановить")
        self.Alarm_notification_stop_button.setFont(QtGui.QFont("intro", 14))

        self.Alarm_notification_background.close()
        self.Alarm_notification_stop_button.close()

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
            with open("last_entry.txt", "w", encoding="utf-8") as file:
                file.write(datetime.now().isoformat())
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
                    item = QListWidgetItem(data[i][0])
                    item.setForeground(QtGui.QColor(229, 199, 1, 205))
                    self.Notes_list.addItem(item)
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
        elif db_type == "Reminders":
            data = rdb.Read_full()
            if len(data) == 0:
                return
            for i in range(len(data)):
                item = QListWidgetItem(Text_formater.Format_reminder(
                    data[i][0], data[i][3].split("$")[1], data[i][3].split("$")[0]))
                item.setFont(QtGui.QFont("intro", 14))
                if data[i][2] == 1:
                    item.setForeground(QtGui.QColor(102, 255, 178))
                else:
                    item.setForeground(QtGui.QColor(229, 204, 255))
                self.Reminders_list.addItem(item)

    def Draw_input_note_menu(self, edit: bool = False):
        self.Notes_list.setGeometry(self.DWIDTH // 2 - 120, 100, (self.DWIDTH //
                                    2 - self.Exit_Button.width()) // 2, self.DHEIGHT // 2 - 130)
        self.background_notes = QLabel(self)
        self.background_notes.setObjectName("Background")
        self.background_notes.setGeometry(self.Notes_list.x() + self.Notes_list.width(
        ), self.Notes_list.y(), self.Notes_list.width(), self.Notes_list.height())
        self.background_notes.show()

        self.name_text = QLabel(self)
        self.name_text.setObjectName("Text_annotation")
        self.name_text.setText("Name:")
        self.name_text.setGeometry(self.background_notes.x() + self.background_notes.width() // 15, self.background_notes.y(
        ) + self.background_notes.height() // 10, self.background_notes.width() // 6, 30)
        self.name_text.setFont(QtGui.QFont("intro", 13))
        self.name_text.show()

        self.text_text = QLabel(self)
        self.text_text.setObjectName("Text_annotation")
        self.text_text.setText("Text:")
        self.text_text.setGeometry(self.name_text.x(), self.name_text.y(
        ) + self.name_text.height() + 5, self.background_notes.width() // 6, 30)
        self.text_text.setFont(QtGui.QFont("intro", 13))
        self.text_text.show()

        self.input_name_note = QLineEdit(self)
        self.input_name_note.setGeometry(self.name_text.x() + self.name_text.width() + 15, self.name_text.y(
        ), self.background_notes.width() - 2 * (self.background_notes.width() // 5), 30)
        self.input_name_note.setFont(QtGui.QFont("intro", 14))

        self.input_text_note = QTextEdit(self)
        self.input_text_note.setGeometry(self.input_name_note.x(), self.input_name_note.y(
        ) + self.input_name_note.height() + 5, self.background_notes.width() - 2 * (self.background_notes.width() // 5), self.background_notes.height() // 2)
        self.input_text_note.setFont(QtGui.QFont("intro", 14))
        self.input_text_note.textChanged.connect(self.Format_text_input)

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
                Text_formater.Format_note_name(self.input_name_note.text())))
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

        self.Notes_list.setGeometry(self.DWIDTH // 2 - 120, 100, self.DWIDTH //
                                    2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 130)

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
            self.Notes_list.currentItem().setText(
                Text_formater.Format_note_name(self.input_name_note.text()))
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
        self.Background_alarm.setObjectName("Background")
        self.Background_alarm.setGeometry(self.Alarm_list.x(), self.Alarm_list.y(
        ) + self.Alarm_list.height(), self.Alarm_list.width(), self.Alarm_list.height())
        self.Background_alarm.show()

        self.Alarm_preview = QLabel(self)
        self.Alarm_preview.setObjectName("Text_annotation")
        self.Alarm_preview.setGeometry(
            self.Background_alarm.x() + self.Background_alarm.width() // 7, self.Background_alarm.y() + self.Background_alarm.height() // 6, 170, 70)
        if not edit:
            self.Alarm_preview.setText("00:00")
        else:
            self.Alarm_preview.setText(
                adb.Read_time_index(self.Alarm_list.currentRow()))
            self.last_time = self.Alarm_preview.text()
        self.Alarm_preview.setFont(QtGui.QFont("intro", 35))
        self.Alarm_preview.show()

        self.Alarm_hour_text = QLabel(self)
        self.Alarm_hour_text.setObjectName("Text_annotation")
        self.Alarm_hour_text.setGeometry(self.Alarm_preview.x(
        ) + self.Alarm_preview.width() + 15, self.Alarm_preview.y(), 50, 30)
        self.Alarm_hour_text.setFont(QtGui.QFont("intro", 14))
        self.Alarm_hour_text.setText("HH")
        self.Alarm_hour_text.show()

        self.Alarm_hour_input = QComboBox(self)
        self.Alarm_hour_input.setGeometry(self.Alarm_hour_text.x(
        ), self.Alarm_hour_text.y() + self.Alarm_hour_text.height() + 5, 70, 30)
        self.Alarm_hour_input.addItems(str(i).zfill(2) for i in range(0, 24))
        self.Alarm_hour_input.setFont(QtGui.QFont("intro", 13))
        if edit:
            self.Alarm_hour_input.setCurrentIndex(
                int(adb.Read_time_index(self.Alarm_list.currentRow()).split(":")[0]))
        self.Alarm_hour_input.show()
        self.Alarm_hour_input.currentTextChanged.connect(
            self.Fill_alarm_preview)

        self.Alarm_minute_text = QLabel(self)
        self.Alarm_minute_text.setObjectName("Text_annotation")
        self.Alarm_minute_text.setGeometry(self.Alarm_hour_input.x(
        ) + self.Alarm_hour_input.width() + 15, self.Alarm_hour_text.y(), 50, 30)
        self.Alarm_minute_text.setFont(QtGui.QFont("intro", 14))
        self.Alarm_minute_text.setText("MM")
        self.Alarm_minute_text.show()

        self.Alarm_minute_input = QComboBox(self)
        self.Alarm_minute_input.setGeometry(self.Alarm_minute_text.x(
        ), self.Alarm_minute_text.y() + self.Alarm_minute_text.height() + 5, 70, 30)
        self.Alarm_minute_input.addItems(str(i).zfill(2) for i in range(0, 60))
        self.Alarm_minute_input.setFont(QtGui.QFont("intro", 13))
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
        self.Alarm_activated.setObjectName("Activated_checkbox")
        self.Alarm_activated.setGeometry(self.add_alarm_button.x(
        ), self.Background_alarm.y() + 4 * (self.Background_alarm.height() // 5), 150, 50)
        self.Alarm_activated.setFont(QtGui.QFont("intro", 13))
        if edit:
            if not adb.Check_activated(self.Alarm_list.currentRow()):
                self.Alarm_activated.setChecked(False)
                self.last_alarm_state = False
                self.Alarm_activated.setText("ОТКЛЮЧЕН")
            else:
                self.Alarm_activated.setChecked(True)
                self.last_alarm_state = True
                self.Alarm_activated.setText("ВКЛЮЧЕН")
        else:
            self.Alarm_activated.setChecked(True)
            self.last_alarm_state = True
            self.Alarm_activated.setText("ВКЛЮЧЕН")
        self.Alarm_activated.show()
        self.Alarm_activated.stateChanged.connect(
            self.Change_color_activate)

        self.Alarm_change_music = QComboBox(self)
        self.Alarm_change_music.setGeometry(self.Alarm_preview.x(), self.Alarm_preview.y(
        ) + self.Alarm_preview.height() + 50, self.add_alarm_button.x() - self.Alarm_preview.x() - 50, 50)
        self.Alarm_change_music.addItems(ram(self.Alarm_music_path))
        if edit:
            self.Alarm_change_music.setCurrentText(
                adb.Read_music_index(self.Alarm_list.currentRow()))
        self.Alarm_change_music.setFont(QtGui.QFont("intro", 11))
        self.Alarm_change_music.show()
        self.Alarm_change_music.currentTextChanged.connect(self.Stop_music)

        self.Alarm_play_music_button = QPushButton(self)
        self.Alarm_play_music_button.setObjectName("Play_music_button")
        self.Alarm_play_music_button.setGeometry(
            self.Alarm_change_music.x() - 40, self.Alarm_change_music.y() + 7, 35, 35)
        self.Alarm_play_music_button.setIcon(QtGui.QIcon(
            QtGui.QPixmap("images/icon/alarm_play_music_button.png").scaled(30, 30)))
        self.Alarm_play_music_button.setIconSize(QtCore.QSize(30, 30))
        self.Alarm_play_music_button.setToolTip("Проиграть рингтон")
        self.Alarm_play_music_button.show()

        self.Alarm_play_music_button.clicked.connect(self.Play_alarm_music)

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
                             self.Alarm_change_music.currentText(),
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
        self.Alarm_player.stop()
        self.Alarm_change_music.close()
        self.Alarm_play_music_button.close()
        self.Alarm_list.setGeometry(
            100, 100, self.DWIDTH // 2 - self.Exit_Button.width() - 140, self.DHEIGHT - 210)

        self.Alarm_music_play = False
        self.Alarm_on_work = False
        self.last_alarm_state = True

    def Edit_alarm_input(self):
        if not self.Alarm_on_work:
            self.Alarm_on_work = True
            self.Draw_input_alarm_menu(edit=True)
            self.edit_alarm_button.clicked.connect(self.Edit_alarm)
            self.cancel_alarm_button.clicked.connect(self.Cancel_alarm)
            self.delete_alarm_button.clicked.connect(self.Delete_alarm)

    def Edit_alarm(self):
        if self.last_alarm_state != self.Alarm_activated.isChecked():
            adb.Activate_alarm(self.Alarm_list.currentRow())
        adb.Edit_alarm_index(self.Alarm_list.currentRow(
        ), self.Alarm_preview.text(), self.Alarm_change_music.currentText())
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

    def Play_alarm_music(self):
        if not self.Alarm_music_play:
            self.Alarm_media = QMediaContent(
                QtCore.QUrl(f"alarm_sound/{self.Alarm_change_music.currentText()}.wav"))
            self.Alarm_player.setMedia(self.Alarm_media)
            self.Alarm_player.play()
            self.Alarm_music_play = True
            self.Alarm_player.positionChanged.connect(self.Check_music_finish)
        else:
            self.Alarm_player.stop()
            self.Alarm_music_play = False

    def Alarm_start_ring(self, alarm_index: int, alarm: str):

        self.Alarm_notification_background.setText(f"Будильник {alarm}")
        self.Alarm_notification_background.show()
        self.Alarm_notification_stop_button.show()

        self.Alarm_player = QMediaPlayer(self)
        self.Alarm_media = QMediaContent(
            QtCore.QUrl(f"alarm_sound/{adb.Read_music_index(alarm_index)}.wav"))
        self.Alarm_player.setMedia(self.Alarm_media)
        self.Alarm_player.play()

        self.Alarm_notification_stop_button.clicked.connect(
            self.Alarm_stop_ring)

    def Alarm_stop_ring(self):
        self.Alarm_player.stop()
        self.Alarm_notification_background.close()
        self.Alarm_notification_stop_button.close()

    def Format_text_input(self):
        try:
            if len(self.input_text_note.toPlainText()) > 50:
                if len(self.input_text_note.toPlainText()) > 60:
                    self.input_text_note.setFont(QtGui.QFont("intro", 11))
                else:
                    self.input_text_note.setFont(QtGui.QFont("intro", 12))
        except:
            if len(self.input_text_reminder.toPlainText()) > 50:
                if len(self.input_text_reminder.toPlainText()) > 60:
                    self.input_text_reminder.setFont(QtGui.QFont("intro", 11))
                else:
                    self.input_text_reminder.setFont(QtGui.QFont("intro", 12))

    def Check_music_finish(self):
        if self.Alarm_player.position() == self.Alarm_player.duration():
            self.Alarm_player.stop()
            self.Alarm_music_play = False

    def Fill_alarm_preview(self):
        self.Alarm_preview.setText(
            f"{str(self.Alarm_hour_input.currentIndex()).zfill(2)}:{str(self.Alarm_minute_input.currentIndex()).zfill(2)}")

    def Stop_music(self):
        self.Alarm_player.stop()
        self.Alarm_music_play = False

    def Draw_input_reminder_menu(self, edit: bool = False):
        self.Reminders_list.setGeometry(self.DWIDTH // 2 - 120, self.DHEIGHT // 2 +
                                        30, (self.DWIDTH // 2 - self.Exit_Button.width()) // 2, self.DHEIGHT // 2 - 140)

        self.Background_reminder = QLabel(self)
        self.Background_reminder.setObjectName("Background")
        self.Background_reminder.setGeometry(self.Reminders_list.x() + self.Reminders_list.width(
        ), self.Reminders_list.y(), self.Reminders_list.width(), self.Reminders_list.height())
        self.Background_reminder.show()

        self.input_text_reminder = QTextEdit(self)
        self.input_text_reminder.setGeometry(
            self.Background_reminder.x() + 50, self.Background_reminder.y() + 50,  self.Background_reminder.width() - 100, 150)
        self.input_text_reminder.setFont(QtGui.QFont("intro", 14))
        if edit:
            self.input_text_reminder.setText(
                rdb.Read_text_index(self.Reminders_list.currentRow()))
        self.input_text_reminder.show()
        self.input_text_reminder.textChanged.connect(self.Format_text_input)

        self.change_reminders_type = QComboBox(self)
        self.change_reminders_type.setGeometry(self.input_text_reminder.x(
        ), self.input_text_reminder.y() + self.input_text_reminder.height() + 10,  self.input_text_reminder.width() // 2 - 5, 30)
        self.change_reminders_type.addItems(
            ["Каждый день", "День недели", "Один день в год", "Один раз"])
        if edit:
            self.change_reminders_type.setCurrentText(
                rdb.Read_type_index(self.Reminders_list.currentRow()).split("$")[0])
        self.change_reminders_type.show()
        self.change_reminders_type.currentTextChanged.connect(
            self.Change_type_reminders)

        self.change_reminder_time_in_day = QDateTimeEdit(self)
        self.change_reminder_time_in_day.setDisplayFormat("HH:mm")
        if self.change_reminders_type.currentText == "Каждый день":
            time = rdb.Read_type_index(
                self.Reminders_list.currentRow()).split("$")[1]
            self.change_reminder_time_in_day.setTime(
                QtCore.QTime(time.split(":")[0], time.split(":")[1]))
        if not edit:
            self.change_reminder_time_in_day.setGeometry(self.change_reminders_type.x() + self.change_reminders_type.width(
            ) + 10, self.change_reminders_type.y(), self.change_reminders_type.width(), 30)
            self.change_reminder_time_in_day.show()

        self.change_reminder_day_in_week = QComboBox(self)
        self.change_reminder_day_in_week.addItems(
            ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"])
        if edit:
            if self.change_reminders_type.currentText == "День недели":
                self.change_reminder_day_in_week.setCurrentText(
                    rdb.Read_type_index(self.Reminders_list.currentRow()).split("$")[1])

        today = datetime.now().date().isoformat()

        self.change_reminder_day_in_year = QDateTimeEdit(self)
        self.change_reminder_day_in_year.setDisplayFormat("dd MMMM")
        if edit:
            if self.change_reminders_type.currentText() == "Один день в год":
                date = Convert_date_time.convert_date(rdb.Read_type_index(
                    self.Reminders_list.currentRow()).split("$")[1])
                self.change_reminder_day_in_year.setDate(QtCore.QDate(
                    int(today.split("-")[0]), int(date.split()[1]), int(date.split()[0])))

        self.change_reminder_date = QDateEdit(self)
        self.change_reminder_date.setMinimumDate(QtCore.QDate(int(today.split(
            "-")[0]), (int(today.split("-")[1])), (int(today.split("-")[2]))))
        self.change_reminder_date.setGeometry(self.input_text_reminder.x(
        ), self.input_text_reminder.y() + self.input_text_reminder.height() + 10,  self.input_text_reminder.width(), 30)
        if edit:
            if self.change_reminders_type.currentText() == "Один раз":
                date = rdb.Read_type_index(
                    self.Reminders_list.currentRow()).split("$")[1].split(".")
                self.change_reminder_date.setDate(
                    QtCore.QDate(int(date[2]), int(date[1]), int(date[0])))

        self.add_reminder_button = QPushButton(self)
        self.add_reminder_button.setGeometry(self.change_reminder_date.x(
        ), self.change_reminder_date.y() + self.change_reminder_date.height() + 10, self.change_reminder_date.width() // 2 - 5, 30)
        if not edit:
            self.add_reminder_button.setText("Добавить")
            self.add_reminder_button.clicked.connect(self.Add_reminder)
        else:
            self.add_reminder_button.setText("Изменить")
            self.add_reminder_button.clicked.connect(self.Edit_reminder)
        self.add_reminder_button.show()

        self.delete_reminder_button = QPushButton(self)
        self.delete_reminder_button.setGeometry(self.add_reminder_button.x(), self.add_reminder_button.y(
        ) + self.add_reminder_button.height() + 10, self.input_text_reminder.width(), 30)
        self.delete_reminder_button.setText("Удалить напоминание")
        if edit:
            self.delete_reminder_button.show()
            self.delete_reminder_button.clicked.connect(self.Delete_reminder)

        self.Cancel_reminder_button = QPushButton(self)
        self.Cancel_reminder_button.setGeometry(
            self.add_reminder_button.x() + self.add_reminder_button.width() + 10, self.add_reminder_button.y(), self.input_text_reminder.width() // 2 - 5, 30)
        self.Cancel_reminder_button.setText("Отменить")
        self.Cancel_reminder_button.show()
        self.Cancel_reminder_button.clicked.connect(self.Cancel_reminder)

        self.Reminder_activated = QCheckBox(self)
        self.Reminder_activated.setObjectName("Activated_checkbox")
        self.Reminder_activated.setGeometry(self.Cancel_reminder_button.x(
        ), self.Background_reminder.y() + 13 * self.Background_reminder.height() // 16, 150, 50)
        self.Reminder_activated.setFont(QtGui.QFont("intro", 13))
        if edit:
            if not rdb.Check_activated(self.Reminders_list.currentRow()):
                self.Reminder_activated.setChecked(False)
                self.last_reminder_state = False
                self.Reminder_activated.setText("ОТКЛЮЧЕН")
            else:
                self.Reminder_activated.setChecked(True)
                self.last_reminder_state = True
                self.Reminder_activated.setText("ВКЛЮЧЕН")
        else:
            self.Reminder_activated.setChecked(True)
            self.last_reminder_state = True
            self.Reminder_activated.setText("ВКЛЮЧЕН")
        self.Reminder_activated.show()
        self.Reminder_activated.stateChanged.connect(
            self.Change_color_activate)

    def Add_reminder_input(self):
        if not self.Reminder_on_work:
            self.Reminder_on_work = True
            self.Draw_input_reminder_menu()

    def Add_reminder(self):
        if self.change_reminders_type.currentText() == "День недели":
            item = QListWidgetItem(Text_formater.Format_reminder(
                self.input_text_reminder.toPlainText(), self.change_reminder_day_in_week.currentText(), self.change_reminders_type.currentText()))
        elif self.change_reminders_type.currentText() == "Один день в год":
            item = QListWidgetItem(Text_formater.Format_reminder(
                self.input_text_reminder.toPlainText(), self.change_reminder_day_in_year.text(), self.change_reminders_type.currentText()))
        else:
            item = QListWidgetItem(Text_formater.Format_reminder(
                self.input_text_reminder.toPlainText(), self.change_reminder_date.text(), self.change_reminders_type.currentText()))
        item.setFont(QtGui.QFont("intro", 14))
        active = 1
        item.setForeground(QtGui.QColor(102, 255, 178, 255))
        if not self.Reminder_activated.isChecked():
            active = 0
            item.setForeground(QtGui.QColor(229, 204, 255, 255))
        self.Reminders_list.addItem(item)
        today = datetime.now().date().isoformat()
        if self.change_reminders_type.currentText() == "Каждый день":
            rdb.Add_to_data_base(self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_time_in_day.text()}", active)
        elif self.change_reminders_type.currentText() == "День недели":
            rdb.Add_to_data_base(self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_day_in_week.currentText()}", active)
        elif self.change_reminders_type.currentText() == "Один день в год":
            rdb.Add_to_data_base(self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_day_in_year.text()}", active)
        else:
            rdb.Add_to_data_base(self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_date.text()}", active)
        self.Cancel_reminder()

    def Edit_reminder_input(self):
        if not self.Reminder_on_work:
            self.Reminder_on_work = True
            self.Draw_input_reminder_menu(edit=True)
            self.Change_type_reminders()

    def Edit_reminder(self):
        today = datetime.now().date().isoformat()
        if self.change_reminders_type.currentText() == "Каждый день":
            rdb.Edit_reminder_index(self.Reminders_list.currentRow(), self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_time_in_day.text()}")
        elif self.change_reminders_type.currentText() == "День недели":
            rdb.Edit_reminder_index(self.Reminders_list.currentRow(), self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_day_in_week.currentText()}")
        elif self.change_reminders_type.currentText() == "Один день в год":
            rdb.Edit_reminder_index(self.Reminders_list.currentRow(), self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_day_in_year.text()}")
        else:
            rdb.Edit_reminder_index(self.Reminders_list.currentRow(), self.input_text_reminder.toPlainText(
            ), today, f"{self.change_reminders_type.currentText()}${self.change_reminder_date.text()}")
        if self.last_reminder_state != self.Reminder_activated.isChecked():
            rdb.Activate_remind(self.Reminders_list.currentRow())
        self.Reminders_list.clear()
        self.Check_data_base("Reminders")
        self.Cancel_reminder()

    def Delete_reminder(self):
        rdb.Delete_index(self.Reminders_list.currentRow())
        self.Reminders_list.clear()
        self.Check_data_base("Reminders")
        self.Cancel_reminder()

    def Cancel_reminder(self):
        self.Reminders_list.setGeometry(self.DWIDTH // 2 - 120, self.DHEIGHT // 2 +
                                        30, self.DWIDTH // 2 - self.Exit_Button.width(), self.DHEIGHT // 2 - 140)
        self.Background_reminder.close()
        self.add_reminder_button.close()
        self.Cancel_reminder_button.close()
        self.input_text_reminder.close()
        self.delete_reminder_button.close()
        self.Reminder_activated.close()

        self.change_reminders_type.close()
        self.change_reminder_time_in_day.close()
        self.change_reminder_date.close()
        self.change_reminder_day_in_week.close()
        self.change_reminder_day_in_year.close()

        self.Reminder_on_work = False

    def Change_type_reminders(self):
        if self.change_reminders_type.currentText() == "День недели":
            self.change_reminder_day_in_week.setGeometry(self.change_reminders_type.x() + self.change_reminders_type.width(
            ) + 10, self.change_reminders_type.y(), self.change_reminders_type.width(), 30)

            self.change_reminder_time_in_day.close()
            self.change_reminder_date.close()
            self.change_reminder_day_in_year.close()
            self.change_reminder_day_in_week.show()

        elif self.change_reminders_type.currentText() == "Один день в год":
            self.change_reminder_day_in_year.setGeometry(self.change_reminders_type.x() + self.change_reminders_type.width(
            ) + 10, self.change_reminders_type.y(), self.change_reminders_type.width(), 30)

            self.change_reminder_time_in_day.close()
            self.change_reminder_date.close()
            self.change_reminder_day_in_week.close()
            self.change_reminder_day_in_year.show()

        elif self.change_reminders_type.currentText() == "Один раз":
            self.change_reminder_date.setGeometry(self.change_reminders_type.x() + self.change_reminders_type.width(
            ) + 10, self.change_reminders_type.y(), self.change_reminders_type.width(), 30)

            self.change_reminder_time_in_day.close()
            self.change_reminder_day_in_week.close()
            self.change_reminder_day_in_year.close()
            self.change_reminder_date.show()
        else:
            self.change_reminder_time_in_day.setGeometry(self.change_reminders_type.x() + self.change_reminders_type.width(
            ) + 10, self.change_reminders_type.y(), self.change_reminders_type.width(), 30)
            self.change_reminder_date.close()
            self.change_reminder_day_in_week.close()
            self.change_reminder_day_in_year.close()
            self.change_reminder_time_in_day.show()

    def Reminder_start_ring(self, reminder_index: int):
        self.Reminder_player = QMediaPlayer(self)
        self.Reminder_media = QMediaContent(
            QtCore.QUrl(f"rem_sound/Классический.wav"))
        self.Reminder_player.setMedia(self.Reminder_media)
        self.Reminder_player.play()
        self.Reminder_notification_background.setGeometry(self.Add_reminder_button.x(
        ) + self.Add_reminder_button.width() + 10, self.Add_reminder_button.y(), 170, self.Exit_Button.y() - 15 - self.Add_reminder_button.y())
        self.Reminder_notification_annotation.setGeometry(self.Reminder_notification_background.x(
        ), self.Reminder_notification_background.y(), self.Reminder_notification_background.width(), 30)
        self.Reminder_close_button.setGeometry(self.Reminder_notification_background.x() + 5, self.Reminder_notification_background.y(
        ) + self.Reminder_notification_background.height() - 40, self.Reminder_notification_background.width() - 10, 30)
        self.Reminder_notification_text.setGeometry(self.Reminder_notification_background.x(
        ), self.Reminder_notification_annotation.y() + 15, self.Reminder_notification_background.width(), (self.Reminder_close_button.y() - 10) - (self.Reminder_notification_annotation.y() + self.Reminder_notification_annotation.height() + 10))

        self.Reminder_notification_text.setText(
            rdb.Read_text_index(reminder_index))

        self.Reminder_notification_background.show()
        self.Reminder_notification_annotation.show()
        self.Reminder_notification_text.show()
        self.Reminder_close_button.show()

        self.Reminder_close_button.clicked.connect(
            self.Reminder_stop_ring)

    def Reminder_stop_ring(self):
        self.Reminder_player.stop()
        self.Reminder_notification_background.close()
        self.Reminder_notification_annotation.close()
        self.Reminder_notification_text.close()
        self.Reminder_close_button.close()

    def Change_color_activate(self):
        try:
            if self.last_alarm_state:
                self.Alarm_activated.setChecked(False)
                self.Alarm_activated.setText("ОТКЛЮЧЕН")
            else:
                self.Alarm_activated.setChecked(True)
                self.Alarm_activated.setText("ВКЛЮЧЕН")
        except:
            if self.last_reminder_state:
                self.Reminder_activated.setChecked(False)
                self.Reminder_activated.setText("ОТКЛЮЧЕН")
            else:
                self.Reminder_activated.setChecked(True)
                self.Reminder_activated.setText("ВКЛЮЧЕН")

    def mouseMoveEvent(self, event):
        if event.x() > self.Exit_Button.x() - 5 and event.x() < self.Exit_Button.x() + self.Exit_Button.width() + 5 and event.y() > self.Exit_Button.y() - 5 and event.y() < self.Exit_Button.y() + self.Exit_Button.height() + 5:
            self.Exit_Button.setStyleSheet(
                "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: red")
        else:
            self.Exit_Button.setStyleSheet(
                "background-color: rgba(0, 0, 0, 0.3); border: none; border-radius: 5px; color: #202020")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("images/style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())
    window = Application()
    window.setObjectName("MainWindow")
    window.setStyleSheet(
        "#MainWindow{border-image:url(images/background.gif)}")
    window.show()
    sys.exit(app.exec_())
