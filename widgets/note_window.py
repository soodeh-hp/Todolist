from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton
from PyQt5 import uic
import sqlite3

class NoteWindow(QMainWindow):
    def __init__(self, parent_ui=None):
        super().__init__()

        # load ui file (this ui file is in the reseources folder)
        uic.loadUi("resources/notewindow.ui", self)

        # define widgets 
        self.parent_ui = parent_ui
        self.note_text = ""
        self.textbox = self.findChild(QTextEdit, "textEdit")
        self.setnote_pushbutton = self.findChild(QPushButton, "setnote_pushButton")

        # text edit designe
        self.textbox.setPlaceholderText("type your notes . . .")
        self.textbox.setAcceptRichText(True)

        # clicke to button
        self.setnote_pushbutton.clicked.connect(self.save_note)


    def save_note(self):
        # get text from text edit
        self.note_text = self.textbox.toPlainText()
        # close notewindow
        self.close()

        # update database and parent window
        if self.parent_ui and hasattr(self.parent_ui, "current_note_title"):
            title = self.parent_ui.current_note_title
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET note=? WHERE title=?", (self.note_text, title))
            conn.commit()
            conn.close()
            self.parent_ui.textbox.setText(self.note_text)


