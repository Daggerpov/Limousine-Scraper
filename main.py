from time import sleep 
from random import randint 
from selenium import webdriver 
from bs4 import BeautifulSoup
import requests, csv

def randomize_sleep(min, max):
    sleep(randint(min*100, max*100) / 100)

def web_scraper(province_territory):
    limousines = []
    
    PATH = "/home/daggerpov/Documents/GitHub/Wedding-Scraper/chromedriver"
    driver = webdriver.Chrome(PATH)
    
    driver.get('https://www.limousineworldwide.directory/search_results')
    randomize_sleep(4, 5)

    url = 'https://www.limousineworldwide.directory/search_results'
    while True:
        header = {"From": "Daniel Agapov <danielagapov1@gmail.com>"}

        response = requests.get(url, headers=header)
        if response.status_code != 200: print("Failed to get HTML:", response.status_code, response.reason); exit()

        soup = BeautifulSoup(response.text, "html5lib")

        for limo in soup.select("fieldset"):
            limousines.append(limo)
        
        try:
            next_page_button = driver.find_element_by_xpath("//a[contains(text(), 'Next page')]")
            randomize_sleep(1, 2)
            if next_page_button:
                url = next_page_button.get_attribute('href')
                next_page_button.click()
                randomize_sleep(1, 2)
        except:
            break
    driver.quit()
    return limousines

def retrieve_info(limo):
    pass

def csv_entry(province_territory, limousines): 
    limousines = web_scraper(province_territory)
    
    #clears spreadsheet
    with open(f"./limousines/limousines.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])

    for limo in limousines: 
        table = []
        table.append(retrieve_info(limo))

        with open(f"./limousines/limousines.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(table)

#this first function may seem redundant, but I need it to pass in these variables for the 
#province_territory so that the index resets for every province_territory entered. 

def scrape(province_territory):
    
    limousines = web_scraper(province_territory)
        
    csv_entry(province_territory, limousines)

    exit()