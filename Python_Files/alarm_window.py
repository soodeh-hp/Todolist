from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QStackedWidget, QDial, QComboBox
from PyQt5 import uic


class AlarmWindow(QMainWindow):
    def __init__(self ,parent_ui=None ):
        super(AlarmWindow,self).__init__()

        self.parent_ui = parent_ui
        # load ui file from assets folder
        uic.loadUi("Ui_Files/alarmwindow.ui", self)


        # define widgets
        self.background_label = self.findChild(QLabel, "background_label")
        self.colon_label = self.findChild(QLabel, "colon_label")
        self.hour_pushbutton = self.findChild(QPushButton, "hour_pushButton")
        self.minute_pushbutton = self.findChild(QPushButton, "minute_pushButton")
        self.setalarm_pushbutton = self.findChild(QPushButton, "setalarm_pushButton")
        self.hour_dial = self.findChild(QDial, "hour_dial")
        self.minute_dial = self.findChild(QDial, "minute_dial")
        self.comboBox = self.findChild(QComboBox, "comboBox")
        self.stackwidget = self.findChild(QStackedWidget, "stackedWidget")

        # design dial
        self.hour_dial.setRange(1, 12)
        self.hour_dial.setNotchesVisible(True)
        self.minute_dial.setRange(0, 59)
        self.minute_dial.setNotchesVisible(True)

        # connect buttons to stacked widgets pages
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
        alarm_hour = self.hour_dial.value()
        alarm_minute = self.minute_dial.value()

        if self.parent_ui and hasattr(self.parent_ui, "on_alarm_set"):
            self.parent_ui.on_alarm_set(alarm_hour, alarm_minute)

        self.close()





