from time import sleep 
from random import randint 
from selenium import webdriver 
from bs4 import BeautifulSoup
import requests, csv

def randomize_sleep(min, max):
    sleep(randint(min*100, max*100) / 100)

def web_scraper():    
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
    
    limousines_links = [x.get_attribute('href') for x in driver.find_elements_by_xpath('//a[@class="center-block"]')]
    randomize_sleep(3, 4)
    
    return limousines_links, driver

def retrieve_info(limo_link, driver):    
    driver.get(limo_link)
    randomize_sleep(5, 6)

    header = {"From": "Daniel Agapov <danielagapov1@gmail.com>"}

    response = requests.get(limo_link, headers=header)
    if response.status_code != 200: 
        print("Failed to get HTML:", response.status_code, response.reason) #no exit
        name, company_type, location, phone_number, website = '', '', '', '', ''

    else:
        soup = BeautifulSoup(response.text, "html5lib")

        try:
            name = driver.find_element_by_xpath('//h1[@class="bold inline-block"]').text
        except:name=''

        try:
            company_type = soup.select("span.profile-header-top-category")[0].text
        except:company_type=''

        try:
            location = soup.select("span.profile-header-location")[0].text[1:]
        except:location=''

        try:
            driver.find_element_by_xpath('//div[@class="myphoneHide"]').click()
            randomize_sleep(2, 3)
            phone_number = driver.find_element_by_css_selector("a.btn-block > u").text
        except:phone_number=''

        try:
            website = driver.find_element_by_xpath('//a[@class="weblink"][@title="website"][@rel="nofollow"][@itemprop="url"]').get_attribute('href')
        except:website = ''

    return [name, company_type, location, phone_number, website]

def csv_entry(limousines_links, driver):
    #clears spreadsheet
    with open(f"./limousines.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])

    #takes out " from strings and appends limo info to the empty csv file
    for limo_link in limousines_links: 
        with open(f"./limousines.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows([retrieve_info(limo_link, driver)])

def scrape():
    limousines_links, driver = web_scraper()
        
    csv_entry(limousines_links, driver)

if __name__ == '__main__':
    scrape()

