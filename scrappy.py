'''Some module'''
import requests
from bs4 import BeautifulSoup
import time
import json
import os

LINK_LOG_PATH = './oplog/content.json'
URL = "https://www.literotica.com/c/mature-sex/77-page"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}

def extract_article(soup):
    '''Extracts the text from the article'''
    panel = soup.select('div.panel.article')[0]
    texts = []
    paragraphs = panel.find_all('p')
    for p in paragraphs:
        texts.append(p.text)
    return texts

def process_request(href, num, content):
    '''Gets the next page'''
    link = href + "?page=" + str(num)
    req = requests.get(link, headers=HEADERS)
    if req.status_code == 200:
        time.sleep(2.5)
        num += 1
        soup = BeautifulSoup(req.text, 'html.parser')
        content['title'] = soup.select('h1.headline')[0].text
        content['raw_text'] = content['raw_text'] + extract_article(soup)
        return process_request(href, num, content)
    else:
        print("%s Gave a %s" % (link, str(req.status_code)))
    return content

# Load up the Content JSON file
keys = []
if not os.path.exists(LINK_LOG_PATH):
    with open(LINK_LOG_PATH, 'w'): pass

with open(LINK_LOG_PATH, 'r') as content:
    try:
        keys = json.load(content).keys()
        content.close()
    except ValueError:
        print('OP LOG EMPTY, Using')
print(keys)

# Fetch the initial page
page = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(page.text, 'html.parser')
stories = soup.find_all('div', class_='b-sl-item-r')

links = []
for story in stories:
    links.append(story.find('h3').find('a')['href'])

for link in links:
    content = { 'title': '', 'raw_text': [] }
    print("STARTING===: " + link)
    if (link not in keys):
        content = process_request(link, 1, content)
        print("FOUND %s Number Article Pages " % len(content['raw_text']))
        print("DONE WITH==: " + link)

        with open(LINK_LOG_PATH) as json_file:
            try:
                decode = json.load(json_file)
                json_file.close()
            except ValueError:
                print('OP LOG EMPTY, Using')
                decode = { }
        # print(content['raw_text'])
        content['text'] = ' '.join(content['raw_text'])
        content.pop('raw_text', None)
        decode[link] = content

        with open(LINK_LOG_PATH, 'w') as json_file:
            json.dump(decode, json_file, indent=4)
            json_file.close()
        # writer = open(LINK_LOG_PATH, 'a')
        # writer.write("%s\n" % link)
        # writer.close()
    else:
        print("DUPLICATE: " + link)
