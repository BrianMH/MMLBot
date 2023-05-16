'''
config_bot.py

Tests the bot class for a single iteration
'''
import bot
import unittest

class BotTester(unittest.TestCase):
    def test_bot_class(self):
        botter = bot.MLBot()
        botter.buyRemainderBoxes()
        botter.openSecondhandBoxes()
        botter.nurtureAndReleaseMobs()