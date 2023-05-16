"""
ocr.py

Handles the OCR preprocessing and actual methods necessary to extract the
values from maple.
"""
import pytesseract  # OCR library
import cv2      # used for preprocessing
import numpy as np  # maintains array-like struct
from typing import Callable
from PIL import Image, ImageOps
from pyautogui import screenshot
from .consts import O_MAX_PIX_DIST, TESSERACT_PATH

##########################
# APPLICATION INTRINSICS #
##########################
# Change tesseract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH + r"tesseract.exe"

########################
# TESSERACT CONTROLLER #
########################
class OCREvaluator:
    def __init__(self, psmMode:int = 13, preprocFunc: Callable|None = None):
        # Configure options (used for eval and preprocessing)
        self.cfg = '--psm {} -c tessedit_char_whitelist="0123456789 /"'.format(psmMode)
        if preprocFunc is None:
            self.preFunc = self.defaultPreprocessing
        else:
            self.preFunc = preprocFunc

    def preprocessWithRegion(self, scrotRegion: tuple[int, int, int, int], baseImage: str) -> np.ndarray:
        '''
            Performs the "fuzzy" XOR operation between a base template image and
            an acquired screenshot corresponding to its actual location.
            Returns a structure containing the necessary numerical values with 
            some noise present.
        '''
        # grab our screenshot and convert to array
        mImg = ImageOps.grayscale(screenshot(region = scrotRegion))
        npImg = np.array(mImg).copy()

        # likewise with our base image
        baseImg = np.array(ImageOps.grayscale(Image.open(baseImage))).copy()

        # compute a mask over which to extract dissimilar output (fuzzy XOR)
        mask = (1 - np.isclose(npImg, baseImg, atol = O_MAX_PIX_DIST)).astype(np.bool_)

        return npImg*mask
    
    def processImage(self, relImg: np.ndarray) -> str:
        return pytesseract.image_to_string(relImg, config=self.cfg)
    
    @staticmethod
    def defaultPreprocessing(inImg: np.ndarray) -> np.ndarray:
        '''
            Preprocesse the image for use in the OCR algorithm. The first step
            is binarization, which isolates the most likely numerical elements.
            The second step is erosion, which removes smaller structures such as
            borders and shrinks the font from it's bold form (which can trick
            the OCR algorithm occasionally).
            This function is fairly hard-coded, but it can be overwritten if
            needed.
        '''
        binarized = cv2.threshold(cv2.medianBlur(inImg, 3), 100, 255, cv2.THRESH_BINARY)[1]
        return cv2.erode(binarized, np.ones((3, 3), np.uint8), iterations=1)
    