from PyQt5.QtWidgets import QApplication
from widgets.main_window import UI
from database.database_manager import create_database
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    create_database()
    window = UI()
    sys.exit(app.exec_())
