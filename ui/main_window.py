from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QFont
import threading
import time
from datetime import datetime, timedelta
import keyboard

from appBlock.appBlocker import AppBlocker, block_app_list
from utils.utils import is_admin, BLOCK_KEYS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电脑管控工具 - 应用屏蔽")
        self.setFixedSize(600, 720)
        self.init_ui()
        self.show_admin_status()
        AppBlocker.start_watcher()

    def init_ui(self):
        main = QWidget()
        self.setCentralWidget(main)
        layout = QVBoxLayout(main)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.admin_label = QLabel("")
        layout.addWidget(self.admin_label)

        app_group = QGroupBox("🚫 应用屏蔽")
        app_layout = QVBoxLayout()
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("WeChat.exe、msedge.exe")
        self.app_add_btn = QPushButton("添加并屏蔽应用")
        self.app_del_btn = QPushButton("删除并解除应用")
        self.app_list = QListWidget()
        app_layout.addWidget(self.app_input)
        app_layout.addWidget(self.app_add_btn)
        app_layout.addWidget(self.app_del_btn)
        app_layout.addWidget(self.app_list)
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)

        self.app_add_btn.clicked.connect(self.add_app)
        self.app_del_btn.clicked.connect(self.del_app)

    def show_admin_status(self):
        if is_admin():
            self.admin_label.setText("✅ 已管理员运行")
            self.admin_label.setStyleSheet("color:green;font-weight:bold;")
        else:
            self.admin_label.setText("❌ 未管理员运行")
            self.admin_label.setStyleSheet("color:red;font-weight:bold;")

    def add_app(self):
        app = self.app_input.text().strip()
        if not app:
            QMessageBox.warning(self,"提示","请输入进程名")
            return
        if app in block_app_list:
            QMessageBox.warning(self,"提示","已添加")
            return
        block_app_list.append(app)
        self.app_list.addItem(app)
        self.app_input.clear()

    def del_app(self):
        item = self.app_list.currentItem()
        if not item:
            QMessageBox.warning(self,"提示","请选择")
            return
        app = item.text()
        block_app_list.remove(app)
        self.app_list.takeItem(self.app_list.currentRow())

    def closeEvent(self, e):
        from appBlock.appBlocker import app_monitor_running
        app_monitor_running = False