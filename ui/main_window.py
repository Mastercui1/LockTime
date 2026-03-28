from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QFont
import threading
import time
from datetime import datetime, timedelta
import keyboard

from ui.lock_window import FullLockWindow
from urlBlock.urlBlocker import HostsBlock
from appBlock.appBlocker import AppBlocker, block_app_list
from utils.utils import is_admin, BLOCK_KEYS

class Signal(QObject):
    update_time = pyqtSignal(str)
    lock_finished = pyqtSignal()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电脑管控工具 - 锁屏+网址+应用屏蔽")
        self.setFixedSize(600, 720)

        self.signal = Signal()
        self.signal.lock_finished.connect(self.unlock_pc)
        self.signal.update_time.connect(self.update_lock_time)
        self.is_locked = False
        self.lock_window = None

        self.init_ui()
        self.start_esc_thread()
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

        lock_group = QGroupBox("🔒 全屏定时锁屏")
        lock_layout = QVBoxLayout()
        self.lock_input = QLineEdit()
        self.lock_input.setPlaceholderText("锁定时长（分钟）")
        self.lock_time_label = QLabel("剩余锁定时间：00分00秒")
        self.lock_btn = QPushButton("开始锁定")
        self.lock_btn.setStyleSheet("background:red;color:white;padding:10px;")
        lock_layout.addWidget(self.lock_input)
        lock_layout.addWidget(self.lock_time_label)
        lock_layout.addWidget(self.lock_btn)
        lock_group.setLayout(lock_layout)
        layout.addWidget(lock_group)

        url_group = QGroupBox("🌐 网址屏蔽")
        url_layout = QVBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入域名：douyin.com")
        self.url_add_btn = QPushButton("添加并屏蔽网址")
        self.url_del_btn = QPushButton("删除并解除网址")
        self.url_list = QListWidget()
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.url_add_btn)
        url_layout.addWidget(self.url_del_btn)
        url_layout.addWidget(self.url_list)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        app_group = QGroupBox("🚫 应用屏蔽（仅启动时扫描）")
        app_layout = QVBoxLayout()
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("WeChat.exe、msedge.exe")
        self.app_add_btn = QPushButton("添加并屏蔽应用")
        self.app_del_btn = QPushButton("删除并解除应用")
        self.app_list = QListWidget()
        self.app_tip = QLabel("✅ 0CPU占用，仅进程启动时检查")
        self.app_tip.setStyleSheet("color:green")
        app_layout.addWidget(self.app_input)
        app_layout.addWidget(self.app_add_btn)
        app_layout.addWidget(self.app_del_btn)
        app_layout.addWidget(self.app_list)
        app_layout.addWidget(self.app_tip)
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)

        self.lock_btn.clicked.connect(self.start_lock)
        self.url_add_btn.clicked.connect(self.add_url)
        self.url_del_btn.clicked.connect(self.del_url)
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

    def add_url(self):
        domain = self.url_input.text().strip()
        if not domain: return
        HostsBlock.block_domain(domain)
        self.url_list.addItem(domain)
        self.url_input.clear()

    def del_url(self):
        item = self.url_list.currentItem()
        if not item: return
        domain = item.text()
        HostsBlock.unblock_domain(domain)
        self.url_list.takeItem(self.url_list.currentRow())

    def start_lock(self):
        try:
            t = float(self.lock_input.text())
            if t <=0: return
        except:
            QMessageBox.warning(self,"错误","请输入数字")
            return
        self.is_locked = True
        self.lock_btn.setEnabled(False)
        for k in BLOCK_KEYS:
            try:keyboard.block_key(k)
            except:pass
        self.lock_window = FullLockWindow()
        threading.Thread(target=self.count_thread, args=(t,), daemon=True).start()

    def count_thread(self, m):
        end = datetime.now() + timedelta(minutes=m)
        while self.is_locked:
            rem = (end - datetime.now()).total_seconds()
            if rem <=0:
                self.signal.lock_finished.emit()
                break
            mm = int(rem//60)
            ss = int(rem%60)
            self.signal.update_time.emit(f"{mm:02d}分{ss:02d}")
            time.sleep(1)

    def update_lock_time(self, t):
        self.lock_time_label.setText(f"剩余锁定时间：{t}")
        if self.lock_window:
            self.lock_window.time_label.setText(f"倒计时：{t}")

    def unlock_pc(self):
        self.is_locked = False
        keyboard.unhook_all()
        if self.lock_window:
            self.lock_window.close()
        self.lock_btn.setEnabled(True)

    def start_esc_thread(self):
        def check():
            exit_count = 0
            while True:
                if keyboard.is_pressed('esc'):
                    exit_count +=1
                    time.sleep(0.3)
                    if exit_count >=5 and self.is_locked:
                        self.signal.lock_finished.emit()
                    if exit_count >=5:
                        exit_count =0
                time.sleep(0.1)
        threading.Thread(target=check, daemon=True).start()

    def closeEvent(self, e):
        from appBlock.appBlocker import app_monitor_running
        app_monitor_running = False
        keyboard.unhook_all()
        e.accept()