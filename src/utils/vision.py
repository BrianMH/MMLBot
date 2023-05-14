"""
vision.py

Provides some basic support for vision based localization.
"""
from PIL.Image import Image
from time import sleep
import cv2                      ## box condensing
import pyautogui                ## SS capture
import win32gui                 ## Window searching
from consts import *

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
    '''
    relRegion, wID = getMapleRegion()
    if forceTop:
        win32gui.SetForegroundWindow(wID)    # if always on top, don't bother with this
        sleep(V_WINDOW_DELAY)                   # delay if not on top (aka if top is uncommented)
    im = pyautogui.screenshot(region=relRegion)
    im = im.resize(V_TUP_SIZE)

    return im

def cropMapleVertically(inBox: tuple[int, int, int, int], pDelta: float, *, fromTop: bool = True) -> tuple[int, int, int, int]:
    '''
        Crops a fractional portion of an input box from either the top or bottom. More specifically,
        this function converts a PIL rectangular box (left, top, width, height) into a smaller
        subset of the rectangular box (left, newTop, width, height*pDelta), where newTop is either
        the same as the original (if cropping from the top) or calculated from the bottom.
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
def absBoxToRelBox(inBox: tuple[int, int, int, int], relSpot: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    '''
        Converts a set of absolute desktop coordinates into relative coordinates.
    '''
    return (inBox[0]-relSpot[0], inBox[1]-relSpot[1], *inBox[2:])

def relBoxToAbsBox(inBox: tuple[int, int, int, int], relSpot: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    '''
        Converts a set of relative coordinates back into absolute desktop coordinates.
    '''
    return (inBox[0]+relSpot[0], inBox[1]+relSpot[1], *inBox[2:])

def absPtToRelPt(inPt: tuple[int, int], relPt: tuple[int, int]) -> tuple[int, int]:
    return (inPt[0]-relPt[0], inPt[1]-relPt[1])

def relPtToAbsPt(inPt: tuple[int, int], relPt: tuple[int, int]) -> tuple[int, int]:
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
    # lambda for calculating mids given a (left, top, right, bott) format tuple 
    findMid = lambda boxTup: ((boxTup[0]+boxTup[2])//2, (boxTup[1]+boxTup[3])//2)

    boxes = [convertBoxToLPRP(absBoxToRelBox(box, getMapleRegion()[0])) for box in inBoxes]
    condensed = cv2.groupRectangles(boxes, 1, eps=0.05)[0]
    return [findMid(cBox) for cBox in condensed]

#################
# SMOKE TESTING #
#################
if __name__ == "__main__":
    # testing imports
    import numpy as np
    
    # take screenshot
    mImage = takeMapleScreenshot(forceTop=True)

    # test mob areas
    testImage = np.array(mImage)[:,:,::-1].copy()
    res = [convertBoxToLPRP(absBoxToRelBox(box, getMapleRegion()[0])) for box in 
                searchAllInstances("./src/ImgResources/mobAsset.png", applyCrop = True, fromTop = False)]
    assert(len(res) > 1)
    for boxCoord in cv2.groupRectangles(res, 1, eps=0.05)[0]:
        cv2.rectangle(testImage, boxCoord[0:2], boxCoord[2:4], color = (0, 255, 0), thickness = 3)
    cv2.imshow("Testing Monster Boundaries", testImage)
    cv2.waitKey(0)

    # test lvl area
    testImage = np.array(mImage)[:,:,::-1].copy()
    res = searchFirstInstance("./src/ImgResources/lvlAsset.png")
    assert(res is not None)
    res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
    cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
    cv2.imshow("Testing Level UI Boundary", testImage)
    cv2.waitKey(0)

    # test cost UI area
    testImage = np.array(mImage)[:,:,::-1].copy()
    res = searchFirstInstance("./src/ImgResources/farmUI.png")
    assert(res is not None)
    res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
    cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
    cv2.imshow("Testing Farm UI Boundary", testImage)
    cv2.waitKey(0)

    # test the textual swapping areas
    testImage = np.array(mImage)[:,:,::-1].copy()
    res = searchFirstInstance("./src/ImgResources/myMonsterText.png")
    assert(res is not None)
    res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
    cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
    cv2.imshow("Testing MYMOB location", testImage)
    cv2.waitKey(0)

    testImage = np.array(mImage)[:,:,::-1].copy()
    res = searchFirstInstance("./src/ImgResources/decorateFarmText.png")
    assert(res is not None)
    res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
    cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
    cv2.imshow("Testing Farm UI Boundary", testImage)
    cv2.waitKey(0)