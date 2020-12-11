from time import sleep 
from random import randint 
from selenium import webdriver 
from bs4 import BeautifulSoup
import requests, csv

def randomize_sleep(min, max):
    sleep(randint(min*100, max*100) / 100)

def web_scraper():
    limousines = []
    
    PATH = "/home/daggerpov/Documents/GitHub/Limousine-Scraper/chromedriver"
    driver = webdriver.Chrome(PATH)
    
    driver.get('https://www.limousineworldwide.directory/search_results')
    randomize_sleep(4, 5)

    while True:
        try:
            driver.find_element_by_xpath('//div[@class="btn btn-primary btn-block btn-lg bold clickToLoadMoreBtn"]').click()
            randomize_sleep(4, 5)
        except:
            break
    
    sel_limousines = driver.find_elements_by_xpath('//div[@class="grid_element"]')

    for limo in sel_limousines:
        print(limo)
        exit()

    '''url = 'https://www.limousineworldwide.directory/search_results'
    while True:
        header = {"From": "Daniel Agapov <danielagapov1@gmail.com>"}

        response = requests.get(url, headers=header)
        if response.status_code != 200: print("Failed to get HTML:", response.status_code, response.reason); exit()

        soup = BeautifulSoup(response.text, "html5lib")

        for limo in sel_limousines:
            limousines.append(limo)'''

    driver.quit()
    return limousines

def retrieve_info(limo):
    pass

def csv_entry(limousines): 
    limousines = web_scraper()
    
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

def scrape():
    
    limousines = web_scraper()
        
    #csv_entry(limousines)

    exit()

def main():
    scrape()

if __name__ == '__main__':
    main()

