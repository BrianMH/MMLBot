"""
vision.py

Provides some basic support for vision based localization.
"""
from PIL.Image import Image
from time import sleep
import cv2                      ## box condensing
import pyautogui                ## SS capture
import win32gui                 ## Window searching
from .consts import V_WINDOW_DELAY, V_CONFIDENCE_VAL ,V_PRESET_CROP

#################
# BASIC METHODS #
#################
staticWID = None
def getMapleRegion() -> tuple[tuple[int, int, int, int], int]:
    '''
        Calculates the bounding area of the maple game and returns the region
        in Box coordinates. Coordinates are (left, top, width, height).
        Returns the relevant window ID as well (in case it's necessary)
    '''
    global staticWID    # keep static variable to track WID

    if staticWID is None:
        # grab all window titles
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)

        # get first window instance id
        wID = [(wID, title) for wID, title in winlist if 'maplestory' in title.lower()][0][0]
        staticWID = wID
    
    x, y, x1, y1 = win32gui.GetClientRect(staticWID)
    x, y = win32gui.ClientToScreen(staticWID, (x, y))
    x1, y1 = win32gui.ClientToScreen(staticWID, (x1 - x, y1 - y))

    return (x, y, x1, y1), staticWID

def takeMapleScreenshot(forceTop: bool = False) -> Image:
    ''' 
        Takes a screenshot of the current MapleStory screen.

        Args:
            forceTop: If true, forces the window to the front before taking an SS.
    '''
    relRegion, wID = getMapleRegion()
    if forceTop:
        win32gui.SetForegroundWindow(wID)    # if always on top, don't bother with this
        sleep(V_WINDOW_DELAY)                   # delay if not on top (aka if top is uncommented)
    im = pyautogui.screenshot(region=relRegion)

    return im

def cropMapleVertically(inBox: tuple[int, int, int, int], pDelta: float, *, fromTop: bool = True) -> tuple[int, int, int, int]:
    '''
        Crops a fractional portion of an input box from either the top or bottom. More specifically,
        this function converts a PIL rectangular box (left, top, width, height) into a smaller
        subset of the rectangular box (left, newTop, width, height*pDelta), where newTop is either
        the same as the original (if cropping from the top) or calculated from the bottom.

        Args:
            inBox: PIL rectangular coordinates
            pDelta: The amount to leave uncropped (% based)
            fromTop: Flag that determines the direction that the crop functions
    '''
    if fromTop:
        return (inBox[0], inBox[1], inBox[2], int(inBox[3]*pDelta))
    else:
        return (inBox[0], (inBox[1]+inBox[3]-int(inBox[3]*pDelta)), inBox[2], int(inBox[3]*pDelta))

##################
# SEARCH METHODS #
##################
def searchAllInstances(imgSrc: str, * , applyCrop: bool = False, fromTop: bool = True) -> list[tuple[int, int, int, int]]:
    roi = getMapleRegion()[0]
    if applyCrop:
        roi = cropMapleVertically(roi, V_PRESET_CROP, fromTop = fromTop)

    return list(pyautogui.locateAllOnScreen(imgSrc, confidence = V_CONFIDENCE_VAL, region = roi))

def searchFirstInstance(imgSrc: str) -> tuple[int, int, int, int]:
    res = pyautogui.locateOnScreen(imgSrc, confidence = V_CONFIDENCE_VAL, region = getMapleRegion()[0])
    if res is None:
        raise AssertionError("Improper search image.")
    return res

################## 
# HELPER METHODS #
##################
def absBoxToRelBox(inBox: tuple[int, int, int, int], relSpot: tuple[int, int]|tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    '''
        Converts a set of absolute desktop coordinates into relative coordinates.
    '''
    return (inBox[0]-relSpot[0], inBox[1]-relSpot[1], *inBox[2:])

def relBoxToAbsBox(inBox: tuple[int, int, int, int], relSpot: tuple[int, int]|tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    '''
        Converts a set of relative coordinates back into absolute desktop coordinates.
    '''
    return (inBox[0]+relSpot[0], inBox[1]+relSpot[1], *inBox[2:])

def absPtToRelPt(inPt: tuple[int, int], relPt: tuple[int, int]) -> tuple[int, int]:
    '''
        Same as above but only for points (no range)
    '''
    return (inPt[0]-relPt[0], inPt[1]-relPt[1])

def relPtToAbsPt(inPt: tuple[int, int], relPt: tuple[int, int]) -> tuple[int, int]:
    '''
        Same as above but only for points(no range)
    '''
    return (inPt[0]+relPt[0], inPt[1]+relPt[1])

def convertBoxToLPRP(inBox: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    '''
        Converts a set of PIL Box coordinates to Open CV based Rectangle coordinates.
            (left, top, width, height) => (left, top, right, bott)
    '''
    return (inBox[0], inBox[1], inBox[0] + inBox[2], inBox[1] + inBox[3])

def getCenter(inBox: tuple[int, int, int, int]) -> tuple[int, int]:
    '''
        Calculates the center position of a box and returns that.
    '''
    return pyautogui.center(inBox)

def condensedGetCenter(inBoxes: list[tuple[int, int, int, int]]) -> list[tuple[int, int]]:
    '''
        Given a set of points in OpenCV rectangle format, finds the midpoints (centers) of
        every single array list.

        Args:
            inBoxes: A list of rectangles in OpenCV rectangle format.
    '''
    # lambda for calculating mids given a (left, top, right, bott) format tuple 
    findMid = lambda boxTup: ((boxTup[0]+boxTup[2])//2, (boxTup[1]+boxTup[3])//2)

    boxes = [convertBoxToLPRP(box) for box in inBoxes]
    condensed = cv2.groupRectangles(boxes, 1, eps=0.05)[0]
    return [findMid(cBox) for cBox in condensed]
