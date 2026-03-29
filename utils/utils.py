import ctypes
import sys

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

BLOCK_KEYS = ['windows', 'alt', 'tab', 'ctrl', 'esc', 'ctrl+esc', 'ctrl+shift+esc']