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

if __name__ == "__main__":
    