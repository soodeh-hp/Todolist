from PyQt5.QtWidgets import QCheckBox, QStyleOptionButton, QStyle
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent

class SmartCheckBox(QCheckBox):
    textClicked = pyqtSignal(QCheckBox)

    def mousePressEvent(self, event: QMouseEvent):
        option = QStyleOptionButton()
        self.initStyleOption(option)
        indicator_rect = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, option, self)
        if indicator_rect.contains(event.pos()):
            super().mousePressEvent(event)
        else:
            self.textClicked.emit(self)

