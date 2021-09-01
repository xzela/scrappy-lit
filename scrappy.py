'''Some module'''
import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from lxml import html
import time

def extract_article(soup):
    '''Extracts the text from the article'''
    panel = soup.select('div.panel.article')[0]
    print ()
    texts = []
    paragraphs = panel.find_all('p')
    for p in paragraphs:
        texts.append(p.text)
    print(texts)
    return texts

def process_request(href, num, content):
    '''Gets the next page'''
    link = href + "?page=" + str(num)
    req = requests.get(link, headers=headers)
    if req.status_code == 200:
        time.sleep(2.5)
        num += 1
        soup = BeautifulSoup(req.text, 'html.parser')
        content.append(extract_article(soup))
        return process_request(href, num, content)
    else:
        print(link + " Gave a " + str(req.status_code))
    return content

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
# print(links)

for link in links:
    print("STARTING===: " + link)
    content = process_request(link, 1, [])
    print("FOUND %s Number Article Pages " % len(content))
    print("DONE WITH==: " + link)
