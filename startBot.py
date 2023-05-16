"""
startBot.py

Wrapper that begins the bot and handles a few initial user prompts.
"""
import bot

#################
# BOT EXECUTION #
#################
if __name__ == "__main__":
    # Prompt for user to enter ML
    print("Enter Monster Life and move to the top-left of the display.\nEnter y when ready...")
    userInput = input()
    while userInput.strip() != 'y':
        userInput = input()

    curBot = bot.MLBot()
    curBot.executeLoop()