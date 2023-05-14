"""
controller.py

Manages the actual keypresses and other nonsense related to user inputs. It's pretty
much just a small wrapper around pyautogui
"""
import pyautogui
from consts import DEBUG_FLAG, CONT_MOUSE_MOVE_DUR, CONT_DELAY
from vision import relPtToAbsPt
from time import sleep

def sDec(func):
    def sleepWrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        sleep(CONT_DELAY)
        return ret
    return sleepWrapper

class Controller:
    def __init__(self, relWindowPos: tuple[int, int]):
        self.relPos = relWindowPos
        self.curPressed = False

    def moveMouseTo(self, newPos):
        pyautogui.moveTo(*relPtToAbsPt(newPos, self.relPos), CONT_MOUSE_MOVE_DUR)

    @sDec
    def mouseClick(self):
        pyautogui.click()

    def scrollUp(self):
        pyautogui.scroll(1)

    def scrollDown(self):
        pyautogui.scroll(-1)

    def kbPressEsc(self):
        pyautogui.press('esc')
    
    def kbKDEnter(self):
        pyautogui.keyDown('enter')
        self.curPressed = True
    
    def kbKUEnter(self):
        if self.curPressed:
            pyautogui.keyUp('enter')
        self.curPressed = False