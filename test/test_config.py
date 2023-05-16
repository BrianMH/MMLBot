'''
config_test.py

Tests the config util module
'''
from utils import config
import os
import unittest

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # delete config that already exists
        if os.path.exists("bot.conf"):
            os.remove("bot.conf")

    @classmethod
    def tearDownClass(cls):
        # delete config created from this testing
        os.remove("bot.conf")

    def test_config_creation(self):
        # create our module
        curConf = config.Config.detectAndLoadConfigFile("bot.conf")
        
        # and then print the config to allow the user to view the output
        print(str(curConf))
        print(str(curConf.farmInfo))

    def test_second_initialization(self):
        # same as above, just create the config and ensure nothing is thrown
        curConf = config.Config.detectAndLoadConfigFile("bot.conf")