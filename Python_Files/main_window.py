from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QListWidget,
    QLabel, QStackedWidget, QCheckBox, QMessageBox
)

import sqlite3
import datetime
from PyQt5 import uic, QtCore
from PyQt5.QtMultimedia import QSound
from Python_Files.second_window import SecondWindow
from Python_Files.alarm_window import AlarmWindow
from Python_Files.calendar_window import CalendarWindow



# Create database
with sqlite3.connect("notes.db") as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT ,
            note TEXT,
            calendar TEXT,
            alarm_hour INTEGER,
            alarm_minute INTEGER
        )
    """)

    conn.commit()



class UI(QMainWindow):
    def __init__(self):
        super(UI , self).__init__()


        # define ui file
        uic.loadUi('Ui_Files/todolist.ui', self)


        # define main window widgets

        # first page
        self.stackwidget = self.findChild(QStackedWidget, "stackedWidget")
        self.listwidget = self.findChild(QListWidget, "listWidget")
        self.add1_pushbutton = self.findChild(QPushButton, "add1_pushButton")

        # second page
        self.textbox = self.findChild(QTextEdit, "textEdit")
        self.reminder_label = self.findChild(QLabel, "reminder_label")
        self.date_label = self.findChild(QLabel, "date_label")
        self.reminder_edit_pushButton = self.findChild(QPushButton, "reminder_edit_pushButton")
        self.date_edit_pushButton = self.findChild(QPushButton, "date_edit_pushButton")
        self.getback_pushButton = self.findChild(QPushButton, "getback_pushButton")
        self.delete_pushButton = self.findChild(QPushButton, "delete_pushButton")


        # Connect signals to handler
        self.add1_pushbutton.clicked.connect(self.opensecond)
        self.delete_pushButton.clicked.connect(self.delete)
        self.textbox.textChanged.connect(self.update_note)
        self.reminder_edit_pushButton.clicked.connect(self.reminder_edit)
        self.date_edit_pushButton.clicked.connect(self.date_edit)
        self.getback_pushButton.clicked.connect(self.getback)


        # Check alarms every 30s
        self.alarm_timer = QtCore.QTimer(self)
        self.alarm_timer.timeout.connect(self.check_alarms)
        self.alarm_timer.start(30000)



        self.stackwidget.setCurrentIndex(0)
        self.show()




   

    def getback(self):
        self.stackwidget.setCurrentIndex(0)



    def reminder_edit(self):
        self.alarmwin = AlarmWindow(self)
        self.alarmwin.show()




    def date_edit(self):
        self.calendarwin = CalendarWindow(self)
        self.calendarwin.show()



    def opensecond(self):
        self.window2 = SecondWindow(self)
        self.window2.show()



    def checkbox_state(self):
        checkbox = self.sender()
        if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
            checkbox.style().polish(checkbox)



    def checkbox_text(self, checkbox):
        note_id = getattr(checkbox, "task_id", None)                 # Get note ID from checkbox
        if note_id is None:
            return

        self.current_note_id = note_id
        self.current_checkbox = checkbox

        self.stackwidget.setCurrentIndex(1)

        # Connect to database and fetch note details
        with sqlite3.connect("notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT note, calendar, alarm_hour, alarm_minute
                FROM notes
                WHERE id = ?
            """, (note_id,))
            row = cursor.fetchone()

        if row:
            note, date, hour, minute = row
            self.textbox.setText(note or "")
            self.date_label.setText(date or "")

            if hour is not None and minute is not None:                     # If reminder exists
                self.reminder_label.setText(f"{hour:02d}:{minute:02d}")
            else:
                self.reminder_label.clear()



    def check_alarms(self):
        # Get current datetime
        now = datetime.datetime.now()
        today_str = now.strftime("%a %b %d %Y")

        # Fetch notes with alarms from DB
        with sqlite3.connect("notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, calendar, alarm_hour, alarm_minute FROM notes")
            rows = cursor.fetchall()

        # Check each note alarm
        for title, date, hour, minute in rows:
            if hour is None or minute is None:                                    # Skip if no alarm time
                continue
            date = date or today_str                                              # Use today if date missing
            if date == today_str and hour == now.hour and minute == now.minute:
                self.trigger_alarm(title)                                         # Trigger alarm if match




    def trigger_alarm(self, task_title):
        # Play alarm sound if available
        try:
            QSound.play("alarm.wav")
        except Exception:
            pass

        # Show reminder message box
        msg = QMessageBox(self)
        msg.setWindowTitle("Reminder")
        msg.setText(f"It's time to do: {task_title}")
        msg.setIcon(QMessageBox.Information)
        msg.addButton("Done", QMessageBox.AcceptRole)
        msg.exec_()

        # Mark the task as done in the list
        for i in range(self.listwidget.count()):
            checkbox = self.listwidget.itemWidget(self.listwidget.item(i))
            if checkbox.text() == task_title:
                checkbox.setChecked(True)
                break




    def delete(self):
        if not hasattr(self, "current_note_id"):
            return

        # Clear UI fields
        for widget in (self.date_label, self.reminder_label, self.textbox):
            widget.clear()

        # Delete from database
        with sqlite3.connect("notes.db") as conn:
            conn.execute(
                "DELETE FROM notes WHERE id=?",
                (self.current_note_id,)
            )

        # Remove from list widget
        row = self.listwidget.currentRow()
        self.listwidget.takeItem(row)

        # Remove current note reference
        del self.current_note_id




    def update_note(self):
        if not hasattr(self, "current_note_id"):
            return

        content = self.textbox.toPlainText()

        with sqlite3.connect("notes.db") as conn:
            conn.execute(
                "UPDATE notes SET note=? WHERE id=?",
                (content, self.current_note_id)
            )




    def on_alarm_set(self, hour, minute):
        if not hasattr(self, "current_note_id"):
            return

        with sqlite3.connect("notes.db") as conn:
            conn.execute("""
                UPDATE notes
                SET alarm_hour=?, alarm_minute=?
                WHERE id=?
            """, (hour, minute, self.current_note_id))

        self.reminder_label.setText(f"{hour:02d}:{minute:02d}")




    def on_date_set(self, date_text):
        if not hasattr(self, "current_note_id"):
            return

        with sqlite3.connect("notes.db") as conn:
            conn.execute("""
                UPDATE notes
                SET calendar=?
                WHERE id=?
            """, (date_text, self.current_note_id))

        self.date_label.setText(date_text)
