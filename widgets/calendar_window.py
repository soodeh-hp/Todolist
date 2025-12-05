from PyQt5.QtWidgets import QMainWindow, QLabel, QCalendarWidget, QPushButton
from PyQt5 import uic
import sqlite3

class CalendarWindow(QMainWindow):
    def __init__(self, parent_ui=None):
        super().__init__()

        # load ui file from resources folder
        uic.loadUi("resources/calendarwindow.ui", self)


        # define widgets
        self.parent_ui = parent_ui
        self.selected_date = None
        self.label_2 = self.findChild(QLabel, "label_2")
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.setdate_pushbutton = self.findChild(QPushButton, "setdate_pushButton")

        # connect button to functions
        self.calendar.selectionChanged.connect(self.grab_date)
        self.setdate_pushbutton.clicked.connect(self.setdate)

    def grab_date(self):
        self.label_2.setText(str(self.calendar.selectedDate().toString()))

    def setdate(self):
        # get choosen date
        self.selected_date = self.calendar.selectedDate().toString()
        # close calendar window
        self.close()

        # update database and parent window
        if self.parent_ui and hasattr(self.parent_ui, "current_note_title"):
            title = self.parent_ui.current_note_title
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET calendar=? WHERE title=?", (self.selected_date, title))
            conn.commit()
            conn.close()
            self.parent_ui.date_label.setText(self.selected_date)


