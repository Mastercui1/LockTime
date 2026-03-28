import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

BLOCK_KEYS = ['windows', 'alt', 'tab', 'ctrl', 'esc', 'ctrl+esc', 'ctrl+shift+esc']