"""
controller.py

Manages the actual keypresses and other nonsense related to user inputs. It's pretty
much just a small wrapper around pyautogui but one that takes into account any relative
positions passed into it.
"""
import pyautogui
from time import sleep
from .consts import CONT_MOUSE_MOVE_DUR, CONT_DELAY, CONT_SCROLL_DIST
from .vision import relPtToAbsPt

def sDec(func):
    def sleepWrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        sleep(CONT_DELAY)
        return ret
    return sleepWrapper

class Controller:
    def __init__(self, relWindowPos: tuple[int, int] = (0, 0)):
        self.relPos = relWindowPos
        self.curPressed = False

    def moveMouseTo(self, newPos) -> None:
        pyautogui.moveTo(*relPtToAbsPt(newPos, self.relPos), CONT_MOUSE_MOVE_DUR)

    def moveMouseToHeight(self, height) -> None:
        pyautogui.moveTo(*pyautogui.position(y=height+self.relPos[1]), CONT_MOUSE_MOVE_DUR)

    def setRelativePos(self, relWindowPos: tuple[int, int]) -> None:
        self.relPos = relWindowPos

    @sDec
    def mouseClick(self) -> None:
        pyautogui.click()

    @sDec
    def mouseRClick(self) -> None:
        pyautogui.click(button = "right")

    def scrollUp(self, * , amount: int = 1) -> None:
        pyautogui.scroll(amount * CONT_SCROLL_DIST)

    def scrollDown(self, * , amount:int = -1) -> None:
        pyautogui.scroll(amount * CONT_SCROLL_DIST)

    def kbPressEnter(self) -> None:
        pyautogui.press('enter')

    def kbPressEsc(self) -> None:
        pyautogui.press('esc')
    
    def kbKDEnter(self) -> None:
        pyautogui.keyDown('enter')
        self.curPressed = True
    
    def kbKUEnter(self) -> None:
        if self.curPressed:
            pyautogui.keyUp('enter')
        self.curPressed = False