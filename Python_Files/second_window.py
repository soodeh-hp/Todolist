import os
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5 import uic, QtCore
from Python_Files.alarm_window import AlarmWindow
from Python_Files.calendar_window import CalendarWindow
from Python_Files.base_widgets import SmartCheckBox
from Python_Files.note_window import NoteWindow




class SecondWindow(QMainWindow):
    def __init__(self, UI):
        super(SecondWindow, self).__init__()

        # define ui file
        uic.loadUi('Ui_Files/secondwindow.ui', self)


        # Keep a reference to the main UI window
        self.ui = UI

        # define widgets
        self.add2_pushbutton = self.findChild(QPushButton, "add2_pushButton")
        self.calendar_pushbutton = self.findChild(QPushButton, "calendar_pushButton")
        self.note_pushbutton = self.findChild(QPushButton, "note_pushButton")
        self.reminder_pushbutton = self.findChild(QPushButton, "reminder_pushButton")
        self.lineedit = self.findChild(QLineEdit, "lineEdit")
        self.label = self.findChild(QLabel, "label")

        # Connect signals to handler
        self.add2_pushbutton.clicked.connect(self.addtask)
        self.note_pushbutton.clicked.connect(self.writenote)
        self.calendar_pushbutton.clicked.connect(self.setdate)
        self.reminder_pushbutton.clicked.connect(self.setreminder)




    def writenote(self):
        self.notewin = NoteWindow(self)
        self.notewin.show()



    def setdate(self):
        self.calendarwin = CalendarWindow(self)
        self.calendarwin.show()



    def setreminder(self):
        self.reminderwin = AlarmWindow(self)
        self.reminderwin.show()



    def on_alarm_set(self, hour, minute):
        self.alarm_hour = hour
        self.alarm_minute = minute
        self.label.setText(f"")



    def on_date_set(self, date_text):
        self.selected_date = date_text
        self.label.setText(f"")



    def on_note_set(self, text):
        self.note_text = text
        if text:
            self.label.setText("")



    def addtask(self):
        text = self.lineedit.text().strip()
        if not text:
            return

        # Create a new checkbox

        checkbox = SmartCheckBox(text)
        checkbox.setMinimumSize(500, 60)
        font = QFont()
        font.setPointSize(30)
        checkbox.setFont(font)

        #  apply stylesheet for  checkbox
        style_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.qss")
        checkbox.setStyleSheet(self.load_stylesheet(style_path))

        # Connect checkbox events to the main UI functions
        checkbox.stateChanged.connect(self.ui.checkbox_state)
        checkbox.textClicked.connect(self.ui.checkbox_text)

        # Add checkbox to main list
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(0, 100))
        self.ui.listwidget.addItem(item)
        self.ui.listwidget.setItemWidget(item, checkbox)

        # Collect optional data from other windows (if they were opened)
        note_text = getattr(self, "note_text", "")
        calendar_date = getattr(self, "selected_date", "")
        alarm_hour = getattr(self, "alarm_hour", None)
        alarm_minute = getattr(self, "alarm_minute", None)


        # Save the new task into the SQLite database
        with sqlite3.connect("notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO notes (title, note, calendar, alarm_hour, alarm_minute)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                text,
                note_text,
                calendar_date,
                alarm_hour,
                alarm_minute
            ))
            conn.commit()

            new_id = cursor.lastrowid


        checkbox.task_id = new_id
        checkbox.task_title = text


        # Clear input
        self.lineedit.clear()
        self.selected_date = None
        self.alarm_hour = None
        self.alarm_minute = None
        self.note_text = ""
        self.label.setText("")



    def load_stylesheet(self, path):
        # Read and return the contents of style.qss file
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
