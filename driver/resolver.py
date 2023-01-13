import time, os
from selenium import webdriver
from collections import Counter
from selenium.webdriver import ActionChains
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

############# VARIABLE TO MODIFY ###############

headless = False # - HEADLESS - (no browser)
discord = True
windows = True
webhook = ""

############################

global discord_log
discord_log = ""

def log_string(message):
    global discord_log
    discord_log += "\n" + message

# -- DEBUG --
debug_time = False
word_to_check = ""

# -- VARIABLES --
url = "https://loldle.net/classic"
if windows:
    chromedriver_path = 'driver/chromedriver.exe'
    geckodriver_path = 'driver/geckodriver.exe'
# -- CORE --
if headless:
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    if windows:
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
else:
    driver = webdriver.Firefox(executable_path=geckodriver_path)
action = ActionChains(driver)
driver.get(url)
#driver.maximize_window()
driver.implicitly_wait(5)

# Time
start_time = time.time()
global timerr
timerr = time.time()

while True:
    pass