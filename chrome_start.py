#!/usr/bin/env python3

import os
import shelve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# TODO: see if there's a way to obtain a session id
#       from a browser without having to start it via
#       Selenium

# TODO: find way to verify remote is active

chromedriver = os.path.expandvars('$HOME/builds/chromedriver/pkg/chromedriver/usr/bin/chromedriver')

def chrome_start(capabilities=None):
	if os.path.exists('/tmp/session.shelve'):
		info = shelve.open('/tmp/session.shelve', 'c')
		try:
			driver = webdriver.Remote(command_executor=info['executor'])
            #we don't want a loose extra browser window
            #so we close the extra one
			driver.close()
			driver.session_id = info['id']
			#easy check to see if remote is active
			driver.switch_to.new_window('tab')
			driver.close()
			return driver
		except:
			os.remove('/tmp/session.shelve')
			return chrome_start(capabilities)
	else:
		options = Options()
		options.add_experimental_option("excludeSwitches", ['enable-automation'])
		options.add_experimental_option("useAutomationExtension", [False])
		options.add_argument('--user-data-dir=' + os.path.expandvars('$HOME/.config/google-chrome/'))
		driver = webdriver.Chrome(chromedriver, options=options)
		info = shelve.open('/tmp/session.shelve')
		info['executor'] = driver.command_executor._url
		info['id'] = driver.session_id
		return driver
