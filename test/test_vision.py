'''
config_vision.py

Tests the vision util module
'''
from utils.vision import *
import numpy as np
import unittest

class TestVision(unittest.TestCase):
    def test_vision_tools(self):        
        # take screenshot
        mImage = takeMapleScreenshot(forceTop=True)

        # test mob areas
        testImage = np.array(mImage)[:,:,::-1].copy()
        res = [convertBoxToLPRP(absBoxToRelBox(box, getMapleRegion()[0])) for box in 
                    searchAllInstances("./ImgResources/mobAsset.png", applyCrop = True, fromTop = False)]
        assert(len(res) > 1)
        for boxCoord in cv2.groupRectangles(res, 1, eps=0.05)[0]:
            cv2.rectangle(testImage, boxCoord[0:2], boxCoord[2:4], color = (0, 255, 0), thickness = 3)
        cv2.imshow("Testing Monster Boundaries", testImage)
        cv2.waitKey(0)

        # test lvl area
        testImage = np.array(mImage)[:,:,::-1].copy()
        res = searchFirstInstance("./ImgResources/lvlAsset.png")
        assert(res is not None)
        res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
        cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
        cv2.imshow("Testing Level UI Boundary", testImage)
        cv2.waitKey(0)

        # test cost UI area
        testImage = np.array(mImage)[:,:,::-1].copy()
        res = searchFirstInstance("./ImgResources/farmUI.png")
        assert(res is not None)
        res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
        cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
        cv2.imshow("Testing Farm UI Boundary", testImage)
        cv2.waitKey(0)

        # test the textual swapping areas
        testImage = np.array(mImage)[:,:,::-1].copy()
        res = searchFirstInstance("./ImgResources/myMonsterText.png")
        assert(res is not None)
        res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
        cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
        cv2.imshow("Testing MYMOB location", testImage)
        cv2.waitKey(0)

        testImage = np.array(mImage)[:,:,::-1].copy()
        res = searchFirstInstance("./ImgResources/decorateFarmText.png")
        assert(res is not None)
        res = convertBoxToLPRP(absBoxToRelBox(res, getMapleRegion()[0]))
        cv2.rectangle(testImage, res[0:2], res[2:4], color = (0, 255, 0), thickness = 5)
        cv2.imshow("Testing Farm UI Boundary", testImage)
        cv2.waitKey(0)