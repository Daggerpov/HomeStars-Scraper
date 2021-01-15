from time import sleep 
from random import randint 
from selenium import webdriver 
from bs4 import BeautifulSoup
import requests, csv
from selenium.webdriver.common.keys import Keys

def randomize_sleep(min, max):
    sleep(randint(min*100, max*100) / 100)

def scroll_down():
    #this block of code just scrolls to the bottom of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        randomize_sleep(2, 3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        randomize_sleep(0, 1)

        if new_height == last_height:
            break
        last_height = new_height

def scroll_up():
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    randomize_sleep(3, 4)

def location_input():
    location = driver.find_element_by_xpath('//input[@class="header-search__location ui-autocomplete-input"]')
    
    location.clear()
    randomize_sleep(1, 2)

    location.click()
    randomize_sleep(1, 2)

    location.send_keys(area_input)
    randomize_sleep(1, 2)

def web_scraper(category_input, area_input):    
    PATH = "/home/daggerpov/Documents/GitHub/HomeStars-Scraper/chromedriver"
    global driver
    driver = webdriver.Chrome(PATH)
    
    driver.get('https://homestars.com/on/toronto/categories')
    randomize_sleep(1, 2)

    area = driver.find_element_by_xpath('//input[@class="header-search__keyword ui-autocomplete-input"]')
    
    area.click()
    randomize_sleep(1, 2)

    area.send_keys(category_input)
    randomize_sleep(1, 2)

    location_input()

    driver.find_element_by_xpath('//button[@class="header-search__button"]').click()
    randomize_sleep(0, 1)

    #clears spreadsheet
    with open(f"./companies.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])

    amount = driver.find_element_by_xpath('//div[@class="search-page-matches__tab m--active"]')
    amount = amount.find_element_by_css_selector('a').text.split()[-1].replace('(', '').replace(')', '')
    randomize_sleep(1, 2)

    companies_info = []
    i = 0

    for i in range(int(amount)):
        print(i)

        '''scroll_down()
        driver.find_element_by_xpath('//a[@rel="start"]').click()
        randomize_sleep(1, 2)'''

        #scroll_up()
        search_button = driver.find_element_by_xpath('//button[@class="header-search__button"]')
        randomize_sleep(1, 2)
        
        location_input()

        driver.execute_script("arguments[0].scrollIntoView();", search_button)
        randomize_sleep(1, 2)

        scroll_up()

        search_button.click()
        randomize_sleep(0, 1)
        
        scroll_down()
        scroll_up()

        name, company_type, location_postal, phone_number, website = '', '', '', '', ''
        
        company_bodies = driver.find_elements_by_xpath('//div[@class="name-row"]')
        print(len(company_bodies))
        company = company_bodies[i]
        
        try:
            company.click() 
        except:
            driver.execute_script("arguments[0].scrollIntoView();", company)
            
            randomize_sleep(1, 2)
            company.click()
        
        randomize_sleep(1, 2)

        try:
            header = driver.find_element_by_xpath('//div[contains(@class, "company-header-details")]')
            name = header.find_element_by_css_selector('h1').text.replace('"', '') 
        except:pass

        try:
            company_type = driver.find_element_by_xpath('//div[contains(@class, "company-header-details__category")]').text.replace('"', '') 
        except:pass

        try:
            location_postal = driver.find_element_by_xpath('//div[contains(@class, "company-header-details__address")]').text.replace('"', '') 
        except:pass

        try:
            contact = driver.find_element_by_xpath('//button[contains(@class, "company-listing-subnav-contact__button")]') 
            phone_number = contact.find_element_by_css_selector('span').text.replace('"', '') 
        except:pass

        try:
            website = driver.find_element_by_xpath('//a[contains(@class, "company-listing-subnav-contact__button")]').get_attribute('href').replace('"', '') 
        except:pass 
        
        company_info = [name, company_type, location_postal, phone_number, website]

        print(company_info)

        empty = True 
        for i in company_info:
            if i != '':
                empty = False
                break
        #ensures no duplicates, since there are some that are inherently included on the website for some reason
        if company_info not in companies_info and empty == False:
            companies_info.append(company_info)
            
            with open(f"./companies.csv", "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows([company_info])
                
        driver.execute_script("window.history.go(-1)")

        randomize_sleep(1, 2)

def scrape():
    global area_input
    category_input, area_input = input("category: \n"), input("area: \n")

    web_scraper(category_input, area_input)

    exit()

if __name__ == '__main__':
    scrape()

