"""
config.py

Manages configuration settings and defaults. Expects a file within the utils directory 
to exist (bot.conf) that determines some fairly basic information about the system
and adjusts various files to manage saved values.
"""
import os.path                  ## pre-config check
import vision                   ## basic vision ops
from controller import Controller   ## Loop Execution
from consts import C_DEFAULT_IMGS, DEBUG_FLAG

class Config():
    def __init__(self):
        # Essential locations (these change every run)
        maplePos, self.mapleWID = vision.getMapleRegion()
        self.maplePos = maplePos[:2] # only need top left corner pos
        self.ctrl = Controller(self.maplePos)

        # Monster Farm specific UI locations (these are relative points)
        self.decFarmButtLoc = None
        self.myMonsterLoc = None
        self.mobLocs = None
        self.starLoc = None

        # action locs (these are specific heights)
        self.releaseLoc = None
        self.nurtureLoc = None

        # UI elements (these are ranges that need to be parsed)
        self.levelBox = None
        self.infoBox = None

        # Store specific elements
        self.shopButtLoc = None
        self.buyLoc = None

    def loadFile(self, confPath: str) -> None:
        '''
            Loads in a config file if present.
        '''
        pass

    def calibrateDefaults(self) -> None:
        '''
            Performs the initial calibration of the bot for the Monster Farm window. These are essentially
            the operations that DO NOT require any movement.
        '''
        # find relevant center points
        self.decFarmButtLoc = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['decFarmText'])), 
                                                  self.maplePos)
        self.myMonsterLoc = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['myMobLoc'])), 
                                                self.maplePos)

        # identify UI boxes
        self.levelBox = vision.searchFirstInstance(C_DEFAULT_IMGS['levelAsset'])
        self.infoBox = vision.searchFirstInstance(C_DEFAULT_IMGS['UIAsset'])

        # finds all mob locations
        self.mobLocs = [vision.absPtToRelPt(pt, self.maplePos) for pt in 
                            vision.condensedGetCenter(vision.searchAllInstances(C_DEFAULT_IMGS['mobLock'], applyCrop = True, fromTop = False))]

    def deriveFromDefaults(self) -> None:
        '''
            Given a set of initialized defaults, now use these coordinates to perform some further
            calibration.
        '''
        # First move to proper place where boxes can be found
        self.ctrl.moveMouseTo(self.decFarmButtLoc)
        self.ctrl.mouseClick()
        self.shopButtLoc = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['shopButt'])), 
                                               self.maplePos)
        
        # Check shop and hover over buy button
        self.ctrl.moveMouseTo(self.shopButtLoc)
        self.ctrl.mouseClick()
        tempUsableLoc = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['usableButt'])), 
                                            self.maplePos)
        self.ctrl.moveMouseTo(tempUsableLoc)
        self.ctrl.mouseClick()
        self.buyLoc = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['midBoxAsset'])), 
                                            self.maplePos)
        self.ctrl.moveMouseTo(self.buyLoc)
        self.ctrl.moveMouseTo((10, 10))
        self.ctrl.mouseClick()
        self.ctrl.kbPressEsc()

def detectAndLoadConfigFile(confPath: str = "./src/bot.conf") -> 'Config':
    initConfig = Config()

    if os.path.exists(confPath):
        initConfig.loadFile(confPath)
    else:
        initConfig.calibrateDefaults()
        initConfig.deriveFromDefaults()

    return initConfig

# smoke test
if __name__ == "__main__":
    curConf = detectAndLoadConfigFile()
    print(curConf.decFarmButtLoc, curConf.myMonsterLoc, 
          curConf.levelBox, curConf.infoBox, curConf.mobLocs)