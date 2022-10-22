from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import logging
import os
import requests

relative_url = "/web/20200207180731/https://en.wikipedia.org/wiki/Web_scraping"
base_url = "https://web.archive.org"

def setup():
    load_dotenv()
    # datetime object containing current date and time
    now = datetime.now()
    datetime_string = now.strftime("%Y%m%d-%H%M%S")
    env = os.getenv('ENVIRONMENT')

    logging.basicConfig(filename='./logs/crawler-{}-{}.log'.format(datetime_string, env), encoding='utf-8', level=logging.DEBUG)

def scrape_url(base_url, relative_url):
    absolute_url = base_url + relative_url

    logging.info('Starting web crawler')
    logging.debug('Fetching data from: {}'.format(absolute_url))
    try:
        req = requests.get(absolute_url)
        if req.status_code == "404":
            logging.error('Site not found error.')
            return ''
    except requests.exceptions.ConnectionError:
        logging.error('Connection error.')
        return ''

    return req.text

def parse_html(html):
    link_dict = {}

    soup = BeautifulSoup(html, 'html.parser')
    target_element = 'div'
    target_class = 'div-col columns column-width'
    link_div = soup.find(target_element, {'class': target_class})
    if link_div is None:
        logging.error("Target element '{}' with class '{}' not found".format(target_element, target_class))
        return link_dict

    # Passing a list to find_all method
    for element in link_div.find_all('a'):
        link_dict[element.get_text()] = base_url + element['href']

    return link_dict

if __name__ == '__main__':
    setup()
    req_text = scrape_url(base_url, relative_url)
    links_dictionary = parse_html(req_text)
    print(links_dictionary)
    for key, value in links_dictionary.items():
        if "scraping" in key:
            print(value)
