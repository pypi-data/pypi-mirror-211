import ctypes
import win32gui
import win32process
import psutil
from ctypes import wintypes
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_uint),
        ("cntUsage", ctypes.c_uint),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_uint)),
        ("th32ModuleID", ctypes.c_uint),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", ctypes.c_uint),
        ("szExeFile", ctypes.c_char * wintypes.MAX_PATH)
    ]
class HIDEFAILURE(Exception):
    pass
class SHOWFAILURE(Exception):
    pass
class INVALIDPID(Exception):
    pass

def _FindWindowFromProcessID(pid):
    # Enumerate all top-level windows on the desktop
    windows = []
    def EnumWindowsProc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        return True
    win32gui.EnumWindows(EnumWindowsProc, 0)

    # Search through the list of window titles for the one that corresponds to our process
    for hwnd, title in windows:
        if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
            #print("Found window:", title)
            return hwnd

    return 0

def FindProcess(target_process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == target_process_name.lower():
            #print("Target process found.")
            return proc.info['pid']
def _HideWindow(hwnd):
    if hwnd is not None:
        win32gui.EnableWindow(hwnd, False)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except:
            pass
    else:
        raise HIDEFAILURE("Failed to get the window. The window is invalid.")
def _ShowWindow(hwnd):
    if hwnd is not None:
        win32gui.EnableWindow(hwnd, True)
        try:

            win32gui.SetForegroundWindow(hwnd)
        except:
            # exit()
            pass
    else:
        raise HIDEFAILURE("Failed to get the window. The window is invalid.")
class window:
    def __init__(self,hwnd = None, pid = None):
        self.hwnd = hwnd
        self.pid = pid
    def GetHWIDByPID(self,PID):
        try:
            self.hwnd = _FindWindowFromProcessID(PID)
            self.pid = PID
            return _FindWindowFromProcessID(PID)
        except:
            raise INVALIDPID("The requested PID is invalid.")
    def Freeze(self):
        if self.hwnd:
            _HideWindow(self.hwnd)
    def UnFreeze(self):
        if self.hwnd:
            _ShowWindow(self.hwnd)

