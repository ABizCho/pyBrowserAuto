import ctypes
import pyautogui
import time
import cv2
from ctypes import wintypes
wintypes.ULONG_PTR = wintypes.WPARAM
hllDll = ctypes.WinDLL ("User32.dll", use_last_error=True)
VK_HANGUEL = 0x15


###win32API를 이용해 영문 고정시키기 사전작업
#한 > 영
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
def get_hanguel_state():
    return hllDll.GetKeyState(VK_HANGUEL)
def change_state():
    x = INPUT(type=1 ,ki=KEYBDINPUT(wVk=VK_HANGUEL))
    y = INPUT(type=1, ki=KEYBDINPUT(wVk=VK_HANGUEL,dwFlags=2))
    hllDll.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    time.sleep(0.05)
    hllDll.SendInput(1, ctypes.byref(y), ctypes.sizeof(y))

if get_hanguel_state() == 1: #1 일경우 vk_key : 0x15(한글키)가 활성화
    change_state() #한글키 누르고(key_press) , 때기(release)
###

###main
count = 0
timePre = time.time()
timeElapsedPre = 0
while count < 1:
    timeElapsed = int(time.time() - timePre)
    if timeElapsed >= 3:
        print(timeElapsed, '초')
        pyautogui.hotkey('win','q') #윈도우창 오픈
        time.sleep(1)
        pyautogui.typewrite('chrome',interval=0.1) # 크롬을 타이핑:
        pyautogui.typewrite(['enter']) #엔터 입력
        time.sleep(1)
        if get_hanguel_state() == 1: #1 일경우 vk_key : 0x15(한글키)가 활성화
            change_state() #한글키 누르고(key_press) , 때기(release) 
        time.sleep(1)
        pyautogui.typewrite('https://nomadcoders.co/react-for-beginners/lobby', interval=0.1) #노마드코더 접속
        pyautogui.typewrite(['enter']) # enter입력
        timePre = time.time()
        break
    ###