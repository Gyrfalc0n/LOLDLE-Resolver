import time, requests, json, re, random
from selenium import webdriver
from selenium.webdriver import ActionChains
from pprint import pprint
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
    res = requests.get("https://ddragon.leagueoflegends.com/cdn/"+version+"/data/en_US/champion.json")
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

def remove_space(caracteristic): # remove space just before or just after the comma
    return re.sub(r'\s*,\s*', ',', caracteristic)
############################

def get_table_role(caracteristic):
    carac = caracteristic.split('\n')
    if len(carac) == 1:
        return carac[0]
    else:
        return carac    

def get_table_carac(caracteristic): # get caracteristic table
    caracteristic = remove_space(caracteristic)
    carac = caracteristic.split(",")
    if len(carac) == 1:
        return carac[0]
    else:
        return carac
    
######## VALIDATION FUNCTIONS ########

def f_to_validate(to_validate): # return list of champ names that match with to_validate thanks to champs_data
    champs_to_return = []
    with open("data/champ_data.json", "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())
        for champ in json_data:
            if len(to_validate[0]) == 1:
                if to_validate[0][0] != champ['gender'] and to_validate[0] != []:
                    continue
            else:
                if to_validate[0] != champ['gender'] and to_validate[0] != []:
                    continue
            if len(to_validate[1]) == 1:    
                if to_validate[1][0] != champ['positions'] and to_validate[1] != []:
                    continue
            else:
                if to_validate[1] != champ['positions'] and to_validate[1] != []:
                    continue
            if len(to_validate[2]) == 1:
                if to_validate[2][0] != champ['species'] and to_validate[2] != []:
                    continue
            else:
                if to_validate[2] != champ['species'] and to_validate[2] != []:
                    continue
            if len(to_validate[3]) == 1:
                if to_validate[3][0] != champ['resource'] and to_validate[3] != []:
                    continue
            else:
                if to_validate[3] != champ['resource'] and to_validate[3] != []:
                    continue
            if len(to_validate[4]) == 1:
                if to_validate[4][0] != champ['range_type'] and to_validate[4] != []:
                    continue
            else:
                if to_validate[4] != champ['range_type'] and to_validate[4] != []:
                    continue
            if len(to_validate[5]) == 1:
                if to_validate[5][0] != champ['regions'] and to_validate[5] != []:
                    continue
            else:
                if to_validate[5] != champ['regions'] and to_validate[5] != []:
                    continue
            champs_to_return.append(champ['name'])
    return champs_to_return

def f_not_to_validate(not_to_validate): # return list of champ names that match with not_to_validate thanks to champs_data
    champs_to_return = []
    with open("data/champ_data.json", "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())
        for champ in json_data:
            if len(to_validate[0]) == 1:
                if to_validate[0][0] == champ['gender'] and to_validate[0] != []:
                    continue
            else:
                if to_validate[0] == champ['gender'] and to_validate[0] != []:
                    continue
            if len(to_validate[1]) == 1:    
                if to_validate[1][0] == champ['positions'] and to_validate[1] != []:
                    continue
            else:
                if to_validate[1] == champ['positions'] and to_validate[1] != []:
                    continue
            if len(to_validate[2]) == 1:
                if to_validate[2][0] == champ['species'] and to_validate[2] != []:
                    continue
            else:
                if to_validate[2] == champ['species'] and to_validate[2] != []:
                    continue
            if len(to_validate[3]) == 1:
                if to_validate[3][0] == champ['resource'] and to_validate[3] != []:
                    continue
            else:
                if to_validate[3] == champ['resource'] and to_validate[3] != []:
                    continue
            if len(to_validate[4]) == 1:
                if to_validate[4][0] == champ['range_type'] and to_validate[4] != []:
                    continue
            else:
                if to_validate[4] == champ['range_type'] and to_validate[4] != []:
                    continue
            if len(to_validate[5]) == 1:
                if to_validate[5][0] == champ['regions'] and to_validate[5] != []:
                    continue
            else:
                if to_validate[5] == champ['regions'] and to_validate[5] != []:
                    continue
            champs_to_return.append(champ['name'])
    return champs_to_return

def f_partial_validate(partial_validate): # return list of champ names that match with partial_validate thanks to champs_data
    pass

def f_year_validate(year_validate): # return list of champ names that match with year_validate thanks to champs_data
    champs_to_return = []
    with open("data/champ_data.json", "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())
        for champ in json_data:
            champ_year = int(champ['release_year'])
            tested_year = int(year_validate[0])
            operator = year_validate[1]
            if champ_year > tested_year and operator == "+":
                champs_to_return.append(champ['name'])
            elif champ_year < tested_year and operator == "-":
                champs_to_return.append(champ['name'])
    return champs_to_return

def merge_lists(to_validate, not_to_validate, partial_validate, year_validate, champs): # merge lists
    pass

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

#if pass_all: # if need to fill all champs infos
#    with open("lol/champions.txt", "r") as f:
#        champs = f.read().splitlines()
#        for champ in champs:
#            if is_in_data(champ):
#                continue
#            driver.find_element(By.TAG_NAME, "input").click()
#            driver.find_element(By.TAG_NAME, "body").send_keys(champ)
#            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
#            time.sleep(wait_time)
#            squares = driver.find_elements(By.CLASS_NAME, "square")
#            nb_squares = len(squares)
#            gender = squares[nb_squares-7].text
#            positions = get_table_role(squares[nb_squares-6].text)
#            species = get_table_carac(squares[nb_squares-5].text)
#            resource = squares[nb_squares-4].text
#            range_type = squares[nb_squares-3].text
#            regions = get_table_carac(squares[nb_squares-2].text)
#            release_year = squares[nb_squares-1].text
#            validation = []
#            for i in range(1,8):
#                classe = squares[i].get_attribute("class")
#                if "square-good" in classe:
#                    validation.append("good")
#                elif "square-bad" in classe:
#                    validation.append("bad")
#                elif "square-inferior" in classe:
#                    validation.append("inferior")
#                elif "square-superior" in classe:
#                    validation.append("superior")
#                    validation.append("partial")
#            caracteristics = [str(gender), positions, species, str(resource), str(range_type), regions, str(release_year)]
#            with open("data/champ_data.json", "a", encoding="utf-8") as f:
#                line = {'name': champ, 'gender' : caracteristics[0], 'positions' : caracteristics[1], 'species' : caracteristics[2], 'resource' : caracteristics[3], 'range_type' : caracteristics[4], 'regions' : caracteristics[5], 'release_year' : caracteristics[6]}
#                f.write(json.dumps(line, ensure_ascii=False) + "\n")
#                log_string("New champ data : " + champ + " - " + str(caracteristics))

global victory
victory = False
first = True
tested_champs = []
to_validate = [[],[],[],[],[],[],[]] # infos to validate
not_to_validate = [[],[],[],[],[],[],[]] # infos not to validate
partial_validate = [[],[],[],[],[],[],[]] # infos to validate partially
year_validate = [0,""]
while not victory:
    if first:
        first = False
        lines = open("lol/champions.txt").read().splitlines()
        champ = str(random.choice(lines))
    driver.find_element(By.TAG_NAME, "input").click()
    driver.find_element(By.TAG_NAME, "body").send_keys(champ)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
    tested_champs.append(champ)
    time.sleep(wait_time)
    squares = driver.find_elements(By.CLASS_NAME, "square")
    nb_squares = len(squares)
    gender = squares[nb_squares-7].text
    positions = get_table_role(squares[nb_squares-6].text)
    species = get_table_carac(squares[nb_squares-5].text)
    resource = squares[nb_squares-4].text
    range_type = squares[nb_squares-3].text
    regions = get_table_carac(squares[nb_squares-2].text)
    release_year = squares[nb_squares-1].text
    caracteristics = [gender, positions, species, resource, range_type, regions, int(release_year)]
    validation = ["","","","","","",""]
    for i in range(7,0,-1):
        classe = squares[nb_squares - i].get_attribute("class")
        if "square-good" in classe:
            validation[7-i] = "good"
        elif "square-bad" in classe:
            validation[7-i] = "bad"
        elif "square-inferior" in classe:
           validation[7-i] = "inferior"
        elif "square-superior" in classe:
            validation[7-i] = "superior"
        elif "square-partial" in classe:
            validation[7-i] = "partial"
    print("validation : " + str(validation))
    for i in range(7):
        if validation[i] == "good":
            to_validate[i].append(caracteristics[i])
        elif validation[i] == "bad":
            not_to_validate[i].append(caracteristics[i])
        elif validation[i] == "partial":
            partial_validate[i].append(caracteristics[i])
        elif validation[i] == "superior":
            year_validate[1] = "+"
            year_validate[0] = caracteristics[i]
        elif validation[i] == "inferior":
            year_validate[1] = "-"
            year_validate[0] = caracteristics[i]
        if i == 6:
            if validation[i] == "good":
                year_validate[1] = "="
                year_validate[0] = caracteristics[i]
    print("to_validate : " + str(to_validate))
    print("not_to_validate : " + str(not_to_validate))
    print("partial_validate : " + str(partial_validate))
    print("year_validate : " + str(year_validate))
    
    print(f_to_validate(to_validate))
    print(f_year_validate(year_validate))
    
    quit()
        

time.sleep(3)
driver.close()