'''
config_ocr.py

Tests the OCR util module
'''
from utils.ocr import OCREvaluator
import cv2
import unittest

class TestOCR(unittest.TestCase):
    def test_active_OCR(self):
        from utils.vision import searchFirstInstance

        # This tests the algorithm manually with part of the UI that has
        # the most text associated with it.
        ocrEv = OCREvaluator()
        rectCoords = searchFirstInstance("./ImgResources/farmUI.png")
        res = ocrEv.preprocessWithRegion(rectCoords, "./ImgResources/farmUI.png")

        # Now detect and see what it reads and show what was viewed
        print("Detected text is {}".format(ocrEv.processImage(res)))
        cv2.imshow("Test UI Elem", OCREvaluator.defaultPreprocessing(res))

        # Then do the same for the other UI element that needs reading
        rectCoords = searchFirstInstance("./ImgResources/lvlAsset.png")
        res = ocrEv.preprocessWithRegion(rectCoords, "./ImgResources/lvlAsset.png")
        print("Detected text is Lv. {}".format(ocrEv.processImage(res)))
        cv2.imshow("Test Lv Elem", OCREvaluator.defaultPreprocessing(res))
        cv2.waitKey(0)