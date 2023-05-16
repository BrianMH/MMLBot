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
from utils import config, controller, vision

class MLBot:
    def __init__(self, cfgLoc: str = "./config.cfg"):
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

##############
# SMOKE TEST #
##############
if __name__ == "__main__":
    # Creation is really the only test needed for this example
    bot = MLBot()