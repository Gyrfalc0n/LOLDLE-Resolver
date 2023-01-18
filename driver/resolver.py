import time, os, requests, json
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
version = "13.1.1"
pass_all = True # - PASS ALL - (pass all champs)
wait_time = 5 # - WAIT TIME - (time to wait between champ and results)
separator = "|" # - SEPARATOR - (separator for data in data/champ_data.json)

############################

global discord_log
discord_log = ""

def log_string(message):
    global discord_log
    discord_log += "\n" + message
    print(message)
    
def get_champions_file():
    with open("lol/champions.txt", "r") as f:
        return f.read().splitlines()
    
def is_in_file(champ): # is champ already in file lol/champions.txt
    file = get_champions_file()
    for line in file:
        if line == champ:
            return True
    return False

def is_in_data(champ): # is champ already in file data/champ_data.json
    with open("data/champ_data.json", "r") as f:
        for line in f:
            if champ in line:
                return True
    return False

def update_champions():
    champs = []
    res = requests.get("https://ddragon.leagueoflegends.com/cdn/"+version+"/data/fr_FR/champion.json")
    if res.status_code != 200:
        log_string("Error getting champions list : " + str(res.status_code)) # + champ + ".png"
        return
    res = res.json()
    with open("lol/champions.txt", "a") as f:
        for champ in res["data"]:
            name = res["data"][champ]["name"]
            if not is_in_file(name):
                champs.append(name)
                log_string("New champ : " + name)
                f.writelines(name + "\n")
    if len(champs) == 0:
        log_string("No new champ")
    return champs

def split_caracteristic(caracteristic):
    if "," in caracteristic:
        return caracteristic.split(",")

############################

# -- VARIABLES --
url = "https://loldle.net/classic"
image_url = "https://ddragon.leagueoflegends.com/cdn/"+version+"/img/champion/"
if windows:
    chromedriver_path = 'driver/chromedriver.exe'
    geckodriver_path = 'driver/geckodriver.exe'
# -- CORE --
if headless:
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    if windows:
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
else:
    driver = webdriver.Firefox(executable_path=geckodriver_path)
action = ActionChains(driver)

# -- START --
new_champs = update_champions()
driver.get(url) # -- GET URL --
driver.implicitly_wait(5)
driver.find_element(By.CLASS_NAME, "fc-cta-consent").click() # -- ACCEPT COOKIES --

if pass_all:
    with open("lol/champions.txt", "r") as f:
        champs = f.read().splitlines()
        for champ in champs:
            if champ == "Swain":
                continue
            driver.find_element(By.TAG_NAME, "body").send_keys(champ)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
            time.sleep(wait_time)
            squares = driver.find_elements(By.CLASS_NAME, "square")
            nb_squares = len(squares)
            gender = squares[nb_squares-7].text
            positions = squares[nb_squares-6].text
            species = squares[nb_squares-5].text 
            resource = squares[nb_squares-4].text
            range_type = squares[nb_squares-3].text
            regions = squares[nb_squares-2].text
            release_year = squares[nb_squares-1].text
            validation = []
            for i in range(1,8):
                classe = squares[i].get_attribute("class")
                if "square-good" in classe:
                    validation.append("good")
                elif "square-bad" in classe:
                    validation.append("bad")
                elif "square-inferior" in classe:
                    validation.append("inferior")
                elif "square-superior" in classe:
                    validation.append("superior")
                    validation.append("partial")
            caracteristics = [str(gender), str(positions), str(species), str(resource), str(range_type), str(regions), str(release_year)]
            with open("data/champ_data.json", "a") as f:
                if not is_in_data(champ):
                    line = {'name': champ, 'gender' : caracteristics[0], 'positions' : caracteristics[1], 'species' : caracteristics[2], 'resource' : caracteristics[3], 'range_type' : caracteristics[4], 'regions' : caracteristics[5], 'release_year' : caracteristics[6]}
                    f.write(json.dumps(line) + "\n")
                    log_string("New champ data : " + champ)


time.sleep(3)
driver.close()