import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.utils import run_as_admin

run_as_admin()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())