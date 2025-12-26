from PyQt5.QtWidgets import QMainWindow, QLabel, QCalendarWidget, QPushButton
from PyQt5 import uic




class CalendarWindow(QMainWindow):
    def __init__(self, parent_ui=None):
        super(CalendarWindow , self).__init__()

        self.parent_ui = parent_ui

        # load ui file
        uic.loadUi("Ui_Files/calendarwindow.ui", self)

        # define widgets
        self.label_2 = self.findChild(QLabel, "label_2")
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.setdate_pushbutton = self.findChild(QPushButton, "setdate_pushButton")

        # connect button to functions
        self.calendar.selectionChanged.connect(self.grab_date)
        self.setdate_pushbutton.clicked.connect(self.setdate)




    def grab_date(self):
        date_str = self.calendar.selectedDate().toString("ddd MMM dd yyyy")
        self.label_2.setText(date_str)



    def setdate(self):
        date_str = self.calendar.selectedDate().toString("ddd MMM dd yyyy")

        if self.parent_ui and hasattr(self.parent_ui, "on_date_set"):
            self.parent_ui.on_date_set(date_str)

        self.close()