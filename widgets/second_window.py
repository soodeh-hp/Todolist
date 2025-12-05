import os
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5 import uic, QtCore
from widgets.alarm_window import AlarmWindow
from widgets.calendar_window import CalendarWindow
from widgets.base_widgets import SmartCheckBox
from widgets.note_window import NoteWindow

class SecondWindow(QMainWindow):
    def __init__(self, UI):
        super(SecondWindow, self).__init__()

        # Load the .ui file from the "resources" folder
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "secondwindow.ui")
        uic.loadUi(ui_path, self)

        # Keep a reference to the main UI window
        self.ui = UI

        # Find widgets from the UI file by their object names
        self.add2_pushbutton = self.findChild(QPushButton, "add2_pushButton")
        self.calendar_pushbutton = self.findChild(QPushButton, "calendar_pushButton")
        self.note_pushbutton = self.findChild(QPushButton, "note_pushButton")
        self.reminder_pushbutton = self.findChild(QPushButton, "reminder_pushButton")
        self.lineedit = self.findChild(QLineEdit, "lineEdit")
        self.label = self.findChild(QLabel, "label")

        # Connect button clicks to their respective methods
        self.add2_pushbutton.clicked.connect(self.addtask)
        self.note_pushbutton.clicked.connect(self.writenote)
        self.calendar_pushbutton.clicked.connect(self.setdate)
        self.reminder_pushbutton.clicked.connect(self.setreminder)

    def writenote(self):
        # Open the Note window for writing additional notes
        self.notewin = NoteWindow(self.ui)
        self.notewin.show()

    def setdate(self):
        # Open the Calendar window to choose a date
        self.calendarwin = CalendarWindow(self.ui)
        self.calendarwin.show()

    def setreminder(self):
        # Open the Alarm window to set a reminder time
        self.reminderwin = AlarmWindow(self.ui)
        self.reminderwin.show()

    def addtask(self):
        # Get the task title from the input field
        text = self.lineedit.text().strip()
        if not text:
            # If the text is empty, stop here
            return

        # Create a new checkbox for the task
        checkbox = SmartCheckBox(text)
        checkbox.setMinimumSize(500, 60)

        # Set font size for better visibility
        font = QFont()
        font.setPointSize(30)
        checkbox.setFont(font)

        # Load and apply stylesheet for the checkbox
        style_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "style.qss")
        checkbox.setStyleSheet(self.load_stylesheet(style_path))

        # Connect checkbox events to the main UI functions
        checkbox.stateChanged.connect(self.ui.checkbox_state)
        checkbox.textClicked.connect(self.ui.checkbox_text)

        # Add the checkbox as a new item to the main list
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(0, 100))
        self.ui.listwidget.addItem(item)
        self.ui.listwidget.setItemWidget(item, checkbox)

        # Collect optional data from other windows (if they were opened)
        note_text = getattr(self.notewin, "note_text", "") if hasattr(self, "notewin") else ""
        calendar_date = getattr(self.calendarwin, "selected_date", "") if hasattr(self, "calendarwin") else ""
        alarm_hour = getattr(self.reminderwin, "alarm_hour", None) if hasattr(self, "reminderwin") else None
        alarm_minute = getattr(self.reminderwin, "alarm_minute", None) if hasattr(self, "reminderwin") else None

        # Save the new task into the SQLite database
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO notes (title, note, calendar, alarm_hour, alarm_minute)
            VALUES (?, ?, ?, ?, ?)
        """, (text, note_text, calendar_date, alarm_hour, alarm_minute))
        conn.commit()
        conn.close()

        # Clear input fields and reset temporary variables
        self.lineedit.clear()
        self.selected_date = None
        self.alarm_hour = None
        self.alarm_minute = None
        self.label.setText("")

    def load_stylesheet(self, path):
        # Read and return the contents of style.qss file
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
