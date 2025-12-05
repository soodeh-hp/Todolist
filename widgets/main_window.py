import os
import sqlite3
import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QListWidget,
    QLabel, QStackedWidget, QCheckBox, QMessageBox
)
from PyQt5 import uic, QtCore
from PyQt5.QtMultimedia import QSound
from database.database_manager import create_database
from widgets.second_window import SecondWindow
from widgets.alarm_window import AlarmWindow
from widgets.calendar_window import CalendarWindow

class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ensure the database exists before doing anything with notes.
        create_database()

        # Load the .ui file from the resources folder (built with Qt Designer).
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "todolist.ui")

        uic.loadUi(ui_path, self)

        # Find widgets by objectName defined in the .ui file
        self.stackwidget = self.findChild(QStackedWidget, "stackedWidget")
        self.listwidget = self.findChild(QListWidget, "listWidget")
        self.add1_pushbutton = self.findChild(QPushButton, "add1_pushButton")
        self.textbox = self.findChild(QTextEdit, "textEdit")
        self.reminder_label = self.findChild(QLabel, "reminder_label")
        self.date_label = self.findChild(QLabel, "date_label")
        self.reminder_edit_pushButton = self.findChild(QPushButton, "reminder_edit_pushButton")
        self.date_edit_pushButton = self.findChild(QPushButton, "date_edit_pushButton")
        self.getback_pushButton = self.findChild(QPushButton, "getback_pushButton")
        self.delete_pushButton = self.findChild(QPushButton, "delete_pushButton")

        # Connect signals (user interactions) to handler methods.
        self.add1_pushbutton.clicked.connect(self.opensecond)
        self.delete_pushButton.clicked.connect(self.delete)
        self.textbox.textChanged.connect(self.update_note_in_db)
        self.reminder_edit_pushButton.clicked.connect(self.reminder_edit)
        self.date_edit_pushButton.clicked.connect(self.date_edit)
        self.getback_pushButton.clicked.connect(self.getback)

        # Alarm timer: periodically check for alarms (every 30 seconds here)
        self.alarm_timer = QtCore.QTimer(self)
        self.alarm_timer.timeout.connect(self.check_alarms)
        self.alarm_timer.start(30000)

        # set first paeg of stackedwidget as defualt
        self.stackwidget.setCurrentIndex(0)
        self.show()

   

    def getback(self):
        # Switch back to the main page of the stacked widget
        self.stackwidget.setCurrentIndex(0)

    def reminder_edit(self):
        # Open the alarm editing window.
        self.alarmwin = AlarmWindow(self)
        self.alarmwin.show()

    def date_edit(self):
        # Open the calendar window to choose a date.
        self.calendarwin = CalendarWindow(self)
        self.calendarwin.show()

    def opensecond(self):
        # Open the second window (for adding a new task/note).
        self.window2 = SecondWindow(self)
        self.window2.show()

    def update_note_in_db(self):
        # When the text in the textbox changes, save the note to the database
        if hasattr(self, "current_note_title"):
            content = self.textbox.toPlainText()
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET note=? WHERE title=?", (content, self.current_note_title))
            conn.commit()
            conn.close()

    def checkbox_state(self):
        # Called when a checkbox style/state changes. This forces a style update.
        checkbox = self.sender()
        if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
            checkbox.style().unpolish(checkbox)
            checkbox.style().polish(checkbox)

    def checkbox_text(self):
        # Called when a checkbox is activated/selected to open the corresponding note.
        checkbox = self.sender()
        if not isinstance(checkbox, QCheckBox):
            return
        title = checkbox.text()
        self.current_note_title = title
        self.stackwidget.setCurrentIndex(1)

        # Load note content, calendar date and alarm time from the database
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT note, calendar , alarm_hour, alarm_minute
            FROM notes
            WHERE title = ?
        """, (title,))
        result = cursor.fetchone()
        conn.close()

        # If the record exists, populate UI elements; otherwise clear them
        if result:
            note, date, hour, minute = result
            note = note or ""
            date = date or ""
            time_text = f"{int(hour):02d}:{int(minute):02d}" if hour is not None and minute is not None else ""

            self.textbox.setText(note)
            self.date_label.setText(date)
            self.reminder_label.setText(time_text)
        else:
            self.textbox.clear()
            self.date_label.clear()
            self.reminder_label.clear()

    def check_alarms(self):
        # Periodically run: check database for notes that have an alarm set
        # and compare with the current datetime. If match, trigger alarm
        now = datetime.datetime.now()
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, calendar, alarm_hour, alarm_minute FROM notes")
        rows = cursor.fetchall()
        conn.close()

        for title, date, hour, minute in rows:
            # Ignore entries without a set alarm time
            if hour is None or minute is None:
                continue
            # If no date stored, assume today's date string format
            if not date:
                date = now.strftime("%a %b %d %Y")
            # Compare stored date and time with current date and time.
            if date == now.strftime("%a %b %d %Y") and hour == now.hour and minute == now.minute:
                self.trigger_alarm(title)

    def trigger_alarm(self, task_title):
        # Play a sound (if available) and show a message box reminder.
        try:
            QSound.play("alarm.wav")
        except Exception:
            pass
        msg = QMessageBox(self)
        msg.setWindowTitle("Reminder")
        msg.setText(f"It's time to do: {task_title}")
        msg.setIcon(QMessageBox.Information)
        msg.addButton("Done", QMessageBox.AcceptRole)
        msg.exec_()

        # After the user dismisses the reminder, mark the corresponding
        for i in range(self.listwidget.count()):
            item = self.listwidget.item(i)
            checkbox = self.listwidget.itemWidget(item)
            if checkbox.text() == task_title:
                checkbox.setChecked(True)
                break

    def delete(self):
        # Clear UI fields for the currently selected note and delete it
        # from the database and the list widget.
        self.date_label.setText("")
        self.reminder_label.setText("")
        self.textbox.setText("")

        clicked = self.listwidget.currentRow()
        item = self.listwidget.item(clicked)
        checkbox = self.listwidget.itemWidget(item)
        note_text = checkbox.text()

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE title=?", (note_text,))
        conn.commit()
        conn.close()

        self.listwidget.takeItem(clicked)
