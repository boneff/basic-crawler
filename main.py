import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# TODO - add a config file for log level, log format etc.
# datetime object containing current date and time
now = datetime.now()
datetime_string = now.strftime("%Y%m%d-%H%M%S")
env = "test"

logging.basicConfig(filename='crawler-{}-{}.log'.format(datetime_string, env), encoding='utf-8', level=logging.DEBUG)
logging.info('Starting web crawler')

relative_url = "/web/20200207180731/https://en.wikipedia.org/wiki/Web_scraping"
base_url = "https://web.archive.orgzzz"
absolute_url = base_url + relative_url

def scrape_url(url):
    # TODO add more logging
    logging.debug('Fetching data from: {}'.format(url))
    try:
        req = requests.get(url)
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
    req_text = scrape_url(absolute_url)
    links_dictionary = parse_html(req_text)
    print(links_dictionary)
    for key, value in links_dictionary.items():
        if "scraping" in key:
            print(value)
