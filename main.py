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

        if new_height == last_height:
            break
        last_height = new_height

def scroll_down_slightly():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    randomize_sleep(2, 3)

def scroll_up():
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    randomize_sleep(1, 2)

def location_input():
    location = driver.find_element_by_xpath('//input[@class="header-search__location ui-autocomplete-input"]')
    
    location.clear()
    randomize_sleep(1, 2)

    location.click()
    randomize_sleep(1, 2)

    location.send_keys(area_input)
    randomize_sleep(1, 2)

def load_results():
    search_button = driver.find_element_by_xpath('//button[@class="header-search__button"]')
    randomize_sleep(1, 2)

    driver.execute_script("arguments[0].scrollIntoView();", search_button)
    randomize_sleep(1, 2)

    scroll_up()
    
    location_input()

    search_button.click()
    randomize_sleep(0, 1)

def web_scraper(category_input, area_input):    
    PATH = "/home/daggerpov/Documents/GitHub/HomeStars-Scraper/chromedriver"
    global driver
    driver = webdriver.Chrome(PATH)
    
    driver.get('https://homestars.com/on/toronto/categories')
    randomize_sleep(1, 2)

    filename = 'plumbing_vancouver'

    area = driver.find_element_by_xpath('//input[@class="header-search__keyword ui-autocomplete-input"][@id="header_keyword_search"]')
    
    area.click()
    randomize_sleep(1, 2)

    area.send_keys(category_input)
    randomize_sleep(1, 2)

    location_input()

    driver.find_element_by_xpath('//button[@class="header-search__button"]').click()
    randomize_sleep(0, 1)

    #clears spreadsheet
    with open(f"./{filename}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])

    load_results()
    scroll_down()
    scroll_up()

    '''amount = driver.find_element_by_xpath('//div[@class="search-page-matches__tab m--active"]')
    amount = amount.find_element_by_css_selector('a').text.split()[-1].replace('(', '').replace(')', '')'''
    company_bodies = driver.find_elements_by_xpath('//div[@class="name-row"]')
    
    randomize_sleep(1, 2)

    companies_info = []

    duplicates = 0

    for i in range(len(company_bodies)):
        load_results()

        name, company_type, location_postal, phone_number, website = '', '', '', '', ''
        
        while True:
            try:
                company_bodies = driver.find_elements_by_xpath('//div[@class="name-row"]')
                company = company_bodies[i]
                break
            except:
                scroll_down_slightly()
                randomize_sleep(1, 2)
        try:
            company.click() 
        except:
            driver.execute_script("arguments[0].scrollIntoView();", company)
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

        empty = True 
        for element in company_info:
            if element != '':
                empty = False
                break
        if empty == True:
            print("empty")
        #ensures no duplicates, since there are some that are inherently included on the website for some reason
        if company_info not in companies_info and empty == False:
            companies_info.append(company_info)
            
            with open(f"./{filename}.csv", "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows([company_info])
        elif company_info in companies_info and empty == False:
            duplicates += 1
        else:
            print("empty (probably)")
                
        driver.execute_script("window.history.go(-1)")

        randomize_sleep(1, 2)
    print(f"duplicates: {duplicates}")

    driver.quit()

def scrape():
    global area_input
    category_input, area_input = input("category: "), input("area: ")

    web_scraper(category_input, area_input)

if __name__ == '__main__':
    scrape()

