from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class FullLockWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.set_geometry_across_screens()
        self.setStyleSheet("background-color:#000;")

        self.label = QLabel("🔴 电脑已强制锁定")
        self.time_label = QLabel("倒计时：00分00秒")
        self.tip_label = QLabel("紧急退出：连续按 5 次 ESC")

        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color:white;")

        font2 = QFont()
        font2.setPointSize(25)
        self.time_label.setFont(font2)
        self.time_label.setStyleSheet("color:#0f0;")

        self.tip_label.setStyleSheet("color:red;")
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.tip_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def set_geometry_across_screens(self):
        screens = QApplication.screens()
        min_x = min(s.geometry().x() for s in screens)
        min_y = min(s.geometry().y() for s in screens)
        max_x = max(s.geometry().x() + s.geometry().width() for s in screens)
        max_y = max(s.geometry().y() + s.geometry().height() for s in screens)
        self.setGeometry(min_x, min_y, max_x - min_x, max_y - min_y)

    def keyPressEvent(self, e): e.accept()
    def mousePressEvent(self, e): e.accept()
    def mouseDoubleClickEvent(self, e): e.accept()
    def closeEvent(self, e): e.ignore()