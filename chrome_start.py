#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

chromedriver = os.path.expandvars('$HOME/builds/chromedriver/pkg/chromedriver/usr/bin/chromedriver')

def chrome_start(capabilities=None):
	options = Options()
	options.add_experimental_option("excludeSwitches", ['enable-automation'])
	options.add_experimental_option("useAutomationExtension", [False])
	options.add_argument('--user-data-dir=' + os.path.expandvars('$HOME/.config/google-chrome/'))
	return webdriver.Chrome(chromedriver, options=options)
