import threading
import time
import os
import wmi

block_app_list = []
app_monitor_running = False

class AppBlocker:
    @staticmethod
    def watch_process_creation():
        global app_monitor_running
        c = wmi.WMI()
        process_watcher = c.Win32_Process.watch_for("creation")
        
        while app_monitor_running:
            try:
                new_process = process_watcher(timeout_ms=1000)
                if not new_process:
                    continue
                name = new_process.Name.lower()
                pid = new_process.ProcessId
                for blocked in block_app_list:
                    if blocked.lower() == name:
                        try:
                            os.kill(pid, 9)
                        except:
                            pass
                        break
            except wmi.x_wmi_timed_out:
                continue
            except:
                time.sleep(1)

    @staticmethod
    def start_watcher():
        global app_monitor_running
        app_monitor_running = True
        threading.Thread(target=AppBlocker.watch_process_creation, daemon=True).start()