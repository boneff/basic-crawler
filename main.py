from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import json
import logging
import os
import requests
import time
from tld import get_tld, exceptions
import urllib.robotparser
import mongodb

def setup():
    load_dotenv()
    # datetime object containing current date and time
    now = datetime.now()
    datetime_string = now.strftime("%Y%m%d-%H%M%S")
    env = os.getenv('ENVIRONMENT')

    logging.basicConfig(filename='./logs/crawler-{}-{}.log'.format(datetime_string, env), encoding='utf-8', level=logging.DEBUG)

def scrape_url(absolute_url, delay_time = 0.1):
    logging.info('Starting web crawler')
    logging.debug('Fetching data from: {} with delay {} seconds'.format(absolute_url, delay_time))
    time.sleep(delay_time)
    try:
        req = requests.get(absolute_url)
        if req.status_code == "404":
            logging.error('Site not found error.')
            return ''
    except requests.exceptions.ConnectionError:
        logging.error('Connection error.')
        return ''

    return req.text

def parse_html(html_string, target_element, target_class = ''):
    link_dict = {}
    target_attributes = None
    soup = BeautifulSoup(html_string, 'html.parser')
    if target_class != '':
        target_attributes = {'class': target_class}

    link_div = soup.find(target_element, target_attributes)
    if link_div is None:
        logging.error("Target element '{}' with target attributes '{}' not found".format(target_element, json.dumps(target_attributes)))
        return link_dict

    # Passing a list to find_all method
    for element in link_div.find_all('a'):
        try:
            # TODO - consider a custom formatter for BS4 instead of this simple strip
            # https://tedboy.github.io/bs4_doc/8_output.html
            element_text = element.get_text("&nbsp;", strip=True)
            link_dict[element_text] = get_normalized_url(element['href'])
        except KeyError:
            logging.error("Error getting 'href' from element {}".format(element))
            continue
        except exceptions.TldBadUrl:
            logging.error("Error normalizing 'href' from element {}".format(element))
            continue

    return link_dict

def parse_robots(url, default_delay = 0.5):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("{}robots.txt".format(url))
    rp.read()
    delay = rp.crawl_delay("*")
    can_fetch = rp.can_fetch("*", url)
    if delay is None:
        delay = default_delay

    return can_fetch, delay


def get_normalized_url(url):
    res = get_tld(url, as_object=True)
    path_list = [char for char in res.parsed_url.path]
    if len(path_list) == 0:
        final_url = res.parsed_url.scheme+'://'+res.parsed_url.netloc
    elif path_list[-1] == '/':
        final_string = ''.join(path_list[:-1])
        final_url = res.parsed_url.scheme+'://'+res.parsed_url.netloc+final_string
    else:
        final_url = url
    return final_url

# TODO - count occurences of a given link - helpful in determining link importance
def complete_crawler(seed_url, max_n = 1):
    delay_time = 1
    target_element = 'body'
    target_class = ''
    initial_url_set = set()
    initial_url_list = []
    seen_url_set = set()
    initial_url_set.add(seed_url)
    initial_url_list.append(seed_url)
    link_dictionaries = []
    while len(initial_url_set) != 0 and len(seen_url_set) < max_n:
        temp_url = initial_url_set.pop()
        if temp_url in seen_url_set:
            continue
        else:
            seen_url_set.add(temp_url)
            can_crawl, delay = parse_robots(temp_url, delay_time)
            if not can_crawl:
                logging.error("URL {} should not be crawled, skipping".format(temp_url))
                continue
            req_text = scrape_url(temp_url, delay)
            links_dictionary = parse_html(req_text, target_element, target_class)
            site_dictionary = {
                "site": temp_url,
                "urls": links_dictionary
            }
            link_dictionaries.append(site_dictionary)
            # print(links_dictionary)
    return link_dictionaries

if __name__ == '__main__':
    setup()
    connection_string = "mongodb://{}:{}@mongo:27017/".format(os.getenv('DB_USER'), os.getenv('DB_PASS'))
    print(connection_string)
    mongo_client = mongodb.init_client(connection_string)
    scraped_links = complete_crawler("http://www.dnes.bg/", 1)

    db = mongo_client["scraping"]
    collection = db["sites_collection"]
    insert_result = collection.insert_many(scraped_links)
    print(insert_result.inserted_ids)
    print(scraped_links)
