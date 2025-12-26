from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton
from PyQt5 import uic




class NoteWindow(QMainWindow):
    def __init__(self, parent_ui=None):
        super(NoteWindow, self).__init__()

        self.parent_ui = parent_ui

        # load ui file
        uic.loadUi("Ui_Files/notewindow.ui", self)

        # define widgets
        self.textbox = self.findChild(QTextEdit, "textEdit")
        self.setnote_pushbutton = self.findChild(QPushButton, "setnote_pushButton")

        # text edit designe
        self.textbox.setPlaceholderText("type your notes . . .")
        self.textbox.setAcceptRichText(True)

        # clicke to button
        self.setnote_pushbutton.clicked.connect(self.save_note)


    def save_note(self):
        note_text = self.textbox.toPlainText()

        if self.parent_ui and hasattr(self.parent_ui, "on_note_set"):
            self.parent_ui.on_note_set(note_text)

        self.close()