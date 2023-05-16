"""
bot.py

The main bot script. The general gist of information flow in this bot will be the following:
    1) Ensure the player is in the Monster Life game.
    2) If so,
        2.1) Collect key information about the farm (gems / waru / monster count (n/M) / farm level)
        2.2) Run the following loop:
            a) Buy 99 secondhand boxes
            b) Open (M-n) boxes to fill up farm
            c) Nurture (M-n) monsters
            d) Release (M-n) monsters beginning from the right
"""
from utils.consts import DEBUG_FLAG
from utils import config, controller
from time import sleep
import pyautogui

class MLBot:
    def __init__(self, cfgLoc: str = "./config.cfg", boxCost: int = 940):
        '''
            A class that combines msot of the utilities together in order to
            provide a more user friendly API. Since this is a monster life bot,
            it won't be made very generic...

            Args:
                cfgLoc: Location to find/create the config file
        '''
        # initialize controller and configuration file
        self.config = config.Config.detectAndLoadConfigFile(cfgLoc)
        self.controller = controller.Controller(relWindowPos = self.config.maplePos)
        self.boxWaruCost = boxCost
        self.mobWindowSize = 7
        self.firstTimeFlag = True

        # Ask user for number of initial boxes prior to start
        self.curBoxCount = self.promptUserForFinalMetadata()

        # Make sure ML screen is in an adequate position for use
        self.controller.moveMouseTo(self.config.myMonsterLoc)
        self.controller.mouseClick()
        self.moveMonsterBarRight()

        # Determine the number of useful locations from config
        self.botPlayArea = min(self.mobWindowSize, 
                               self.config.farmInfo.maxMobs - self.config.farmInfo.mobCnt)

    def buyRemainderBoxes(self) -> None:
        '''
            Buy the remainder of boxes possible with the current waru count.
            This would only get run of the current number of boxes is less than
            either seven or the remainder mob size.
        '''
        if self.curBoxCount == 99:
            return
        
        self.controller.moveMouseTo(self.config.decFarmButtLoc)
        self.controller.mouseClick()
        self.controller.moveMouseTo(self.config.shopButtLoc)
        self.controller.mouseClick()
        self.controller.moveMouseTo(self.config.buyLoc)
        
        # and now buy boxes one by one til we reach the max
        while(self.config.farmInfo.waru > self.boxWaruCost and
                self.curBoxCount < 99):
            self.controller.mouseClick()
            self.controller.kbPressEnter()
            sleep(0.1)
            self.controller.kbPressEnter()

            self.curBoxCount += 1
            self.config.farmInfo.waru -= self.boxWaruCost
            sleep(0.2)

        # then exit the store
        self.controller.moveMouseTo(self.config.OOBLoc)
        self.controller.mouseClick()
        self.controller.kbPressEsc()

    def openSecondhandBoxes(self) -> bool:
        '''
            Opens a given number of secondhand boxes. If there are less boxes
            than the available play state, then this simply skips the process.
        '''
        if self.curBoxCount <= min(self.mobWindowSize, self.botPlayArea):
            return False

        self.controller.moveMouseTo(self.config.decFarmButtLoc)
        self.controller.mouseClick()
        self.controller.moveMouseTo(self.config.boxLoc)

        # key down enter and open the mobs we want
        for _ in range(self.botPlayArea):
            self.curBoxCount -= 1
            self.controller.mouseClick()
            self.controller.kbPressEnter()
            sleep(0.1)
            self.controller.kbPressEnter()
            sleep(0.1)
        return True

    def nurtureAndReleaseMobs(self) -> None:
        '''
            Nurtures and releases all of the relevant play mobs.
        '''
        # go back to mob display
        self.controller.moveMouseTo(self.config.myMonsterLoc)
        self.controller.mouseClick()

        # shift mobs into screen if necessary
        if self.firstTimeFlag:
            self.firstTimeFlag = False
            self.moveMonsterBarRight()

        # nurture
        for mobLoc in self.config.mobLocs[::-1][:self.botPlayArea]:
            self.controller.moveMouseTo(mobLoc)
            self.controller.mouseRClick()
            self.controller.moveMouseToHeight(self.config.nurtureY)
            self.controller.mouseClick()
            self.controller.kbPressEnter()
            sleep(0.2)
            self.controller.kbPressEnter()

        # then release
        for mobLoc in self.config.mobLocs[::-1][:self.botPlayArea]:
            self.controller.moveMouseTo(mobLoc)
            self.controller.mouseRClick()
            self.controller.moveMouseToHeight(self.config.releaseY)
            self.controller.mouseClick()
            self.controller.moveMouseTo(self.config.releaseCheckLoc)
            self.controller.mouseClick()
            self.controller.kbPressEnter()

    def moveMonsterBarRight(self) -> None:
        '''
            Srolls the mosnter bar as far right as possible. Determinable
            from the monster count as a full window is of size 7 mobs.
        '''
        numScrolls = max(0, self.config.farmInfo.mobCnt - self.mobWindowSize)
        print("scrolling {} times".format(self.config.farmInfo.mobCnt))
        self.controller.moveMouseTo(self.config.mobLocs[-1])
        self.controller.mouseClick()
        for _ in range(numScrolls):
            self.controller.scrollDown()

    def promptUserForFinalMetadata(self) -> int:
        '''
            In order to not have to use OCR an absurd number of times, the user
            is instead prompted for the number of initial boxes they have in order
            to keep track of it in the long run.
        '''
        userInput = input("Enter starting number of secondhand boxes: ")
        while not userInput.isdigit() or not (1 <= int(userInput) <= 99):
            userInput = input()
        return int(userInput)
    
    def executeLoop(self, maxLoops: int = -1) -> None:
        '''
            Executes the control loop until either we run out of waru or we reach
            an indicated number of execution loops.
        '''
        curLoop = 0
        while(self.config.farmInfo.waru > self.boxWaruCost and 
                    (maxLoops == -1 or curLoop < maxLoops)):
            self.buyRemainderBoxes()
            while self.openSecondhandBoxes():
                self.nurtureAndReleaseMobs()