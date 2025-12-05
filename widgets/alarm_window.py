from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QStackedWidget, QDial
from PyQt5 import uic
import sqlite3

class AlarmWindow(QMainWindow):
    def __init__(self, parent_ui=None):
        super().__init__()

        # load ui file from resources folder
        uic.loadUi("resources/alarmwindow.ui", self)

        # define widgets and instance variabels
        self.parent_ui = parent_ui
        self.alarm_hour = None
        self.alarm_minute = None

        self.hour_pushbutton = self.findChild(QPushButton, "hour_pushButton")
        self.minute_pushbutton = self.findChild(QPushButton, "minute_pushButton")
        self.setalarm_pushbutton = self.findChild(QPushButton, "setalarm_pushButton")
        self.hour_dial = self.findChild(QDial, "hour_dial")
        self.minute_dial = self.findChild(QDial, "minute_dial")
        self.stackwidget = self.findChild(QStackedWidget, "stackedWidget")

        # designe dial 
        self.hour_dial.setRange(1, 12)
        self.hour_dial.setNotchesVisible(True)
        self.minute_dial.setRange(0, 59)
        self.minute_dial.setNotchesVisible(True)

        # connect buttons to stacked widegets pages
        self.hour_pushbutton.clicked.connect(lambda: self.stackwidget.setCurrentIndex(0))
        self.minute_pushbutton.clicked.connect(lambda: self.stackwidget.setCurrentIndex(1))
        self.stackwidget.setCurrentIndex(0)

        # connect buttons to their functions
        self.hour_dial.valueChanged.connect(self.hour_dialer)
        self.minute_dial.valueChanged.connect(self.minute_dialer)
        self.setalarm_pushbutton.clicked.connect(self.setalarm)


    def hour_dialer(self):
        self.hour_pushbutton.setText(str(self.hour_dial.value()))

    def minute_dialer(self):
        self.minute_pushbutton.setText(str(self.minute_dial.value()))

    def setalarm(self):
        self.alarm_hour = self.hour_dial.value()
        self.alarm_minute = self.minute_dial.value()
        self.close()
        
        # update database and parent window
        if self.parent_ui and hasattr(self.parent_ui, "current_note_title"):
            title = self.parent_ui.current_note_title
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET alarm_hour=?, alarm_minute=? WHERE title=?",
                           (self.alarm_hour, self.alarm_minute, title))
            conn.commit()
            conn.close()
            self.parent_ui.reminder_label.setText(f"{self.alarm_hour:02d}:{self.alarm_minute:02d}")





