from PyQt5.QtWidgets import QApplication
from Python_Files.main_window import UI
import sys



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()

