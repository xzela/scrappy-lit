'''Some module'''
import requests
# from bs4 import BeautifulSoup
from lxml import html

URL = "https://www.literotica.com/c/mature-sex/78-page"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}
page = requests.get(URL, headers=headers)

tree = html.fromstring(page.content)
stories = tree.xpath('//div[@class="b-story-list"]/div/h3/a/text()')
for story in stories:
    print(story)
# soup = BeautifulSoup(page.content, 'html.parser')
# results = soup.find("div", attrs={'class': 'b-story-list'})
# print()
