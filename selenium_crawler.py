from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


def extract_urls(seed_url, chromedriver_remote):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Remote(chromedriver_remote, DesiredCapabilities.CHROME)
    browser.get(seed_url)
    time.sleep(15)
    element_list = browser.find_elements_by_tag_name('a')
    for element in element_list:
        print(element.text)
    browser.close()