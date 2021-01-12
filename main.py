from time import sleep 
from random import randint 
from selenium import webdriver 
from bs4 import BeautifulSoup
import requests, csv
from selenium.webdriver.common.keys import Keys

def randomize_sleep(min, max):
    sleep(randint(min*100, max*100) / 100)

def web_scraper(category_input, area_input):    
    PATH = "/home/daggerpov/Documents/GitHub/HomeStars-Scraper/chromedriver"
    driver = webdriver.Chrome(PATH)
    
    driver.get('https://homestars.com/on/toronto/categories')
    randomize_sleep(2, 3)

    area = driver.find_element_by_xpath('//input[@class="header-search__keyword ui-autocomplete-input"]')
    
    area.click()
    randomize_sleep(1, 2)

    area.send_keys(category_input)
    randomize_sleep(1, 2)

    location = driver.find_element_by_xpath('//input[@class="header-search__location ui-autocomplete-input"]')
    
    location.clear()
    randomize_sleep(1, 2)

    location.click()
    randomize_sleep(1, 2)

    location.send_keys(area_input)
    randomize_sleep(3, 4)

    driver.find_element_by_xpath('//button[@class="header-search__button"]').click()
    randomize_sleep(4, 5)

    #clears spreadsheet
    with open(f"./companies.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])
    
    name, company_type, location_postal, phone_number, website = '', '', '', '', ''

    company_bodies = driver.find_elements_by_xpath('//div[@class="name-row"]')

    for i in range(len(company_bodies)):
        company_bodies = driver.find_elements_by_xpath('//div[@class="name-row"]')

        company = company_bodies[i]
        
        try:
            company.click() 
        except:
            driver.execute_script("arguments[0].scrollIntoView();", company)
            randomize_sleep(3, 4)
            company.click()
        
        randomize_sleep(4, 5)

        try:
            name = driver.find_element_by_css_selector('h1').text 
        except:pass

        try:
            company_type = driver.find_element_by_xpath('//div[@class="company-header-details__category"]').text
        except:pass

        try:
            location_postal = driver.find_element_by_xpath('//div[@class="company-header-details__address"]').text
        except:pass

        try:
            phone_number = driver.find_element_by_xpath('//span[@data-reactid="15"]').text
        except:pass

        try:
            website = driver.find_element_by_xpath('//a[@class="company-listing-subnav-contact__button"]').get_attribute('href')
        except:pass 

        company_info = [name, company_type, location_postal, phone_number, website]
        
        with open(f"./companies.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows([company_info])
        
        driver.execute_script("window.history.go(-1)")

        randomize_sleep(5, 6)

def scrape():
    category_input, area_input = input("category: \n"), input("area: \n")

    web_scraper(category_input, area_input)

    exit()

if __name__ == '__main__':
    scrape()

