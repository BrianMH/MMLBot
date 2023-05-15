"""
config.py

Manages configuration settings and defaults. Expects a file within the utils directory 
to exist (bot.conf) that determines some fairly basic information about the system
and adjusts various files to manage saved values.
"""
import os.path                      ## pre-config check
from . import ocr                   ## ocr ops
from . import vision                ## basic vision ops
from .controller import Controller   ## Loop Execution
from .consts import C_DEFAULT_IMGS, DEBUG_FLAG, C_OOB_POS

class FarmInfo():
    def __init__(self, fLvl: int, beautyVal: int, gemCnt: int, waruCnt: int, mobCnt: int, mobMax: int):
        self.level = fLvl
        self.beauty = beautyVal
        self.gems = gemCnt
        self.waru = waruCnt
        self.mobCnt = mobCnt
        self.maxMobs = mobMax

class Config():
    def __init__(self):
        # Essential locations (these change every run)
        maplePos, self.mapleWID = vision.getMapleRegion()
        self.maplePos = maplePos[:2] # only need top left corner pos
        self.ctrl = Controller(self.maplePos)
        self.OOBLoc = C_OOB_POS
        self.ocrParser = ocr.OCREvaluator()

        # Monster Farm specific UI locations (these are relative points)
        self.decFarmButtLoc = None
        self.myMonsterLoc = None
        self.mobLocs = list()
        self.starLoc = None

        # action locs (these are specific heights)
        self.releaseY = None
        self.nurtureY = None

        # UI elements (these are ranges that need to be parsed)
        self.levelBox = None
        self.infoBox = None

        # Store specific elements
        self.shopButtLoc = None
        self.buyLoc = None

        # Expected info structs
        self.farmInfo : FarmInfo

    ##############
    # OCR METHOD #
    ##############
    def extractCurrentFarmState(self) -> None:
        '''
            Using the config-declared regions for the lvl and general UI, returns the
            current state of the farm.
        '''
        if self.levelBox is None or self.infoBox is None:
            raise RuntimeError("Config un-initialized")
        levelImg = self.ocrParser.preprocessWithRegion(
                        vision.relBoxToAbsBox(self.levelBox, self.maplePos), 
                        C_DEFAULT_IMGS['levelAsset'])
        level = int(self.ocrParser.processImage(levelImg))
        if DEBUG_FLAG:
            print("\tAcquired level {} from image.".format(level))

        uiImg = self.ocrParser.preprocessWithRegion(
                        vision.relBoxToAbsBox(self.infoBox, self.maplePos),
                        C_DEFAULT_IMGS['UIAsset'])
        uiList = self.ocrParser.processImage(uiImg).replace("/", " ").split(" ")
        self.farmInfo = FarmInfo(level, int(uiList[0]), int(uiList[1]), int(uiList[2]),
                                 int(uiList[3]), int(uiList[4]))
        if DEBUG_FLAG:
            print("\tAcquired values {} from image.".format(uiList))

    #######################
    # CALIBRATION METHODS #
    #######################
    def calibrateDefaults(self) -> None:
        '''
            Performs the initial calibration of the bot for the Monster Farm window. These are essentially
            the operations that DO NOT require any movement.
        '''
        # keep track of flow if debug flag is up
        if DEBUG_FLAG:
            print("Calibrating on main monster life screen...")

        # find relevant center points
        self.decFarmButtLoc = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['decFarmText'])), 
                                                  self.maplePos)
        self.myMonsterLoc = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['myMobLoc'])), 
                                                self.maplePos)

        # identify UI boxes
        self.levelBox = vision.absBoxToRelBox(vision.searchFirstInstance(C_DEFAULT_IMGS['levelAsset']), self.maplePos)
        self.infoBox = vision.absBoxToRelBox(vision.searchFirstInstance(C_DEFAULT_IMGS['UIAsset']), self.maplePos)

        # finds all mob locations
        self.mobLocs = [vision.absPtToRelPt(pt, self.maplePos) for pt in 
                            vision.condensedGetCenter(vision.searchAllInstances(C_DEFAULT_IMGS['mobLock'], applyCrop = True, fromTop = False))]
        self.mobLocs.sort()

    def deriveFromDefaults(self) -> None:
        '''
            Given a set of initialized defaults, now use these coordinates to perform some further
            calibration.
        '''
        if DEBUG_FLAG:
            print("Calibrating for finer elements...")

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
        self.ctrl.moveMouseTo(self.OOBLoc)
        self.ctrl.mouseClick()
        self.ctrl.kbPressEsc()

        # Now find nurture/release locs
        self.ctrl.moveMouseTo(self.myMonsterLoc)
        self.ctrl.mouseClick()
        self.ctrl.moveMouseTo(self.mobLocs[0])
        self.ctrl.mouseRClick()
        self.releaseY = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['releaseText'])), 
                                              self.maplePos)[1]
        self.nurtureY = vision.absPtToRelPt(vision.getCenter(vision.searchFirstInstance(C_DEFAULT_IMGS['nurtureText'])), 
                                              self.maplePos)[1]
        self.ctrl.moveMouseTo(self.OOBLoc)
        self.ctrl.mouseClick()

    ############################
    # SAVING / LOADING METHODS #
    ############################
    @staticmethod
    def loadFile(confPath: str) -> 'Config':
        '''
            Loads in a config file if present.
        '''
        import pickle 
        with open(confPath, 'rb') as inFile:
            return pickle.load(inFile)

    def saveFile(self, confPath: str) -> None:
        '''
            Saves the current config object to a given path.
        '''
        import pickle
        with open(confPath, 'wb') as outFile:
            pickle.dump(self, outFile)

    def refresh(self) -> None:
        '''
            Re-initializes the maple WID/and window location for a new
            session.
        '''
        maplePos, self.mapleWID = vision.getMapleRegion()
        self.maplePos = maplePos[:2] # only need top left corner pos

    @staticmethod
    def detectAndLoadConfigFile(confPath: str = "./src/bot.conf") -> 'Config':
        # load file from memory
        if os.path.exists(confPath):
            initConfig = Config.loadFile(confPath)
            initConfig.refresh()
        else:
            initConfig = Config()
            initConfig.calibrateDefaults()
            initConfig.deriveFromDefaults()
            initConfig.saveFile(confPath)

        # Now acquire farm info
        initConfig.extractCurrentFarmState()

        return initConfig

# smoke testing
if __name__ == "__main__":
    # First test simple configuration
    curConf = Config.detectAndLoadConfigFile()
    print("Current configuration settings:\n" +
          "\tDecorate Farm Button Loc: {}\n".format(curConf.decFarmButtLoc) + 
          "\tMy Monster Button Loc: {}\n".format(curConf.myMonsterLoc) + 
          "\tLevel UI Text Area: {}\n".format(curConf.levelBox) +
          "\tInfo UI Text Area: {}\n".format(curConf.infoBox) + 
          "\tMob Entity Locations: {}\n".format(curConf.mobLocs) +
          "\n" +
          "\tMob Release Height: {}\n".format(curConf.releaseY) +
          "\tMob Nurture Height: {}\n".format(curConf.nurtureY) +
          "\n" + 
          "\tShop Button Loc: {}\n".format(curConf.shopButtLoc) +
          "\tBuy Button Loc: {}\n".format(curConf.buyLoc))
    print("\n\nRun specific configurations:\n" +
          "\tMaple WID: {}".format(curConf.mapleWID) + 
          "\tMaple Pos: {}".format(curConf.maplePos))
    
    # And now test OCR recognition of farm state
    print("\n\nAcquired Farm Stats:\n" +
          "\tFarm Level: {}\n".format(curConf.farmInfo.level) +
          "\tFarm Beauty: {}\n".format(curConf.farmInfo.beauty) + 
          "\tFarm Gems: {}\n".format(curConf.farmInfo.beauty) + 
          "\tFarm Waru: {}\n".format(curConf.farmInfo.waru) +
          "\tFarm Mob Count: {}/{}".format(curConf.farmInfo.mobCnt,
                                           curConf.farmInfo.maxMobs))