# This is a sample Python script.
import requests
from bs4 import BeautifulSoup

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

relative_url = "/web/20200207180731/https://en.wikipedia.org/wiki/Web_scraping"
base_url = "https://web.archive.org"
absolute_url = base_url + relative_url

def scrape_url(url):
    req = requests.get(url)
    if req.status_code == "404":
        return "An error occurred fetching content"
    return req.text

def parse_html(html):
    link_dict = {}

    soup = BeautifulSoup(html, 'html.parser')
    link_div = soup.find('div', {'class': 'div-col columns column-width'})
    if link_div is None:
        print("Target element not found")
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
    #print(links_dictionary)
