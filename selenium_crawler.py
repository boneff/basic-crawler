from selenium import webdriver
import time


def extract_urls(seed_url, chromedriver_location):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    chromedriver = chromedriver_location
    browser = webdriver.Chrome(chromedriver, options=option)
    browser.get(seed_url)
    time.sleep(15)
    element_list = browser.find_elements_by_tag_name('a')
    for element in element_list:
        print(element.text)
    browser.close()