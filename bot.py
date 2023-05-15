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
from src.utils import config, controller

#################
# BOT EXECUTION #
#################
if __name__ == "__main__":
    # Prompt for user to enter ML
    print("Enter Monster Life and move to the top-left of the display.\nEnter y when ready...")
    userInput = input()
    while userInput.strip() != 'y':
        userInput = input()

    # Acquire settings and update it if necessary
    curCfg = config.Config.detectAndLoadConfigFile()

    # Begin loop until either lvl 40 or completely broke.
    