'''Some module'''
import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from lxml import html
import time

def request_page(href, num):
    '''Gets the next page'''
    link = href + "?page=" + str(num)
    req = requests.get(link, headers=headers)
    print("%s, %s" % (link, req.status_code))
    time.sleep(2.5)
    if req.status_code == 200:
        num += 1
        request_page(href, num)
    else:
        print(link + " Gave a " + str(req.status_code))

URL = "https://www.literotica.com/c/mature-sex/78-page"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
stories = soup.find_all('div', class_='b-sl-item-r')
links = []
for story in stories:
    links.append(story.find('h3').find('a')['href'])
print(links)

for link in links:
    print("STARTING===: " + link)
    request_page(link, 1)
    print("DONE WITH==: " + link)
