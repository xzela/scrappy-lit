'''Some module'''
import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from lxml import html

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
