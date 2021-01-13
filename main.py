from time import sleep 
from random import randint 
from selenium import webdriver 
from bs4 import BeautifulSoup
import requests, csv
from selenium.webdriver.common.keys import Keys

def randomize_sleep(min, max):
    sleep(randint(min*100, max*100) / 100)

def scroll_down(driver):
    #this block of code just scrolls to the bottom of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        randomize_sleep(1, 2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        randomize_sleep(2, 3)

        if new_height == last_height:
            break
        last_height = new_height

def scroll_up(driver):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    randomize_sleep(1, 2)

def web_scraper(category_input, area_input):    
    PATH = "/home/daggerpov/Documents/GitHub/HomeStars-Scraper/chromedriver"
    driver = webdriver.Chrome(PATH)
    
    driver.get('https://homestars.com/on/toronto/categories')
    randomize_sleep(1, 2)

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
    randomize_sleep(2, 3)

    driver.find_element_by_xpath('//button[@class="header-search__button"]').click()
    randomize_sleep(3, 4)

    #clears spreadsheet
    with open(f"./companies.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])
    
    name, company_type, location_postal, phone_number, website = '', '', '', '', ''

    amount = driver.find_element_by_xpath('//div[@class="search-page-matches__tab m--active"]')
    amount = amount.find_element_by_css_selector('a').text.split()[-1].replace('(', '').replace(')', '')
    randomize_sleep(3, 4)

    companies_info = []

    for i in range(int(amount)):
        scroll_down(driver)

        driver.find_element_by_xpath('//a[@rel="start"]').click()
        randomize_sleep(1, 2)

        scroll_down(driver)
        scroll_up(driver)
        
        company_bodies = driver.find_elements_by_xpath('//div[@data-reactid="7"][@class="name-row"]')
        company = company_bodies[i]
        
        try:
            company.click() 
        except:
            driver.execute_script("arguments[0].scrollIntoView();", company)
            
            randomize_sleep(2, 3)
            company.click()
        
        randomize_sleep(3, 4)

        try:
            name = driver.find_element_by_xpath('//h1[@data-reactid="9"]').text.replace('"', '') 
        except:pass

        try:
            company_type = driver.find_element_by_xpath('//div[@class="company-header-details__category"]').text.replace('"', '') 
        except:pass

        try:
            location_postal = driver.find_element_by_xpath('//div[@class="company-header-details__address"]').text.replace('"', '') 
        except:pass

        try:
            phone_number = driver.find_element_by_xpath('//span[@data-reactid="15"]').text.replace('"', '') 
        except:pass

        try:
            website = driver.find_element_by_xpath('//a[@class="company-listing-subnav-contact__button"]').get_attribute('href').replace('"', '') 
        except:pass 
        
        company_info = [name, company_type, location_postal, phone_number, website]

        if company_info not in companies_info:
            companies_info.append(company_info)
            
            with open(f"./companies.csv", "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows([company_info])
        else:
            i -= 1
        
        driver.execute_script("window.history.go(-1)")

        randomize_sleep(4, 5)



def scrape():
    category_input, area_input = input("category: \n"), input("area: \n")

    web_scraper(category_input, area_input)

    exit()

if __name__ == '__main__':
    scrape()

