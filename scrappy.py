'''Some module'''
from bs4 import BeautifulSoup
import requests
import sqlite3
import signal
import sys
import time


DB_PATH ='./db/database.sqlite3'
URL = "https://www.literotica.com/c/mature-sex/77-page"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}
CATEGORIES = [
    'anal-sex-stories',
    'bdsm-stories',
    'erotic-couplings',
    'erotic-horror',
    'fetish-stories',
    'first-time-sex-stories',
    'group-sex-stories',
    'lesbian-sex-stories',
    'loving-wives',
    'mature-sex',
    'adult-romance',
    'transgender-crossdressers'
]

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, link TEXT, title TEXT, content TEXT);')

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    connection.close()
    sys.exit(0)

def insert_record(category, link):
    cursor.execute('SELECT * FROM content WHERE category=? AND link=?', (category, link))
    row = cursor.fetchone()
    if row and row[0] > 0:
        print("Skipping %s %s" % (category, link))
        return
    cursor.execute('INSERT INTO content (category, link) VALUES (?, ?) ', (category, link))
    connection.commit()

signal.signal(signal.SIGINT, signal_handler)

def extract_article(soup):
    '''Extracts the text from an article page'''
    panel = soup.select('div.panel.article')[0]
    texts = []
    paragraphs = panel.find_all('p')
    for p in paragraphs:
        texts.append(p.text)
    return texts

def determine_articles(href, num, content):
    '''Gets a list of articles from the results page'''
    link = href + "?page=" + str(num)
    req = requests.get(link, headers=HEADERS, allow_redirects=False)
    if req.status_code == 200:
        time.sleep(2.5)
        num += 1
        soup = BeautifulSoup(req.text, 'html.parser')
        content['title'] = soup.select('h1.headline')[0].text
        content['raw_text'] = content['raw_text'] + extract_article(soup)
        return determine_articles(href, num, content)
    else:
        print("%s Gave a %s" % (link, str(req.status_code)))
    return content

def fetch_category_page(category, num):
    '''Loops through a category and determines the number of pages of articles'''
    # Fetch the initial page
    BASE_URL = 'https://www.literotica.com/c/' + str(category) + '/' + str(num) + '-page'
    print(BASE_URL)
    page = requests.get(BASE_URL, headers=HEADERS, allow_redirects=False)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        stories = soup.find_all('div', class_='b-sl-item-r')
        for story in stories:
            link = story.find('h3').find('a')['href']
            insert_record(category, link)
        return stories
    else:
        return []

links = []
for category in CATEGORIES:
    num = 1
    while stories := fetch_category_page(category, num):
        time.sleep(1.5)
        num += 1
        for story in stories:
            links.append(story.find('h3').find('a')['href'])
    print("Found %s Pages for %s Category" % (num, category))

# for link in links:
#     content = { 'title': '', 'raw_text': [] }
#     print("STARTING===: " + link)
#     if (link not in keys):
#         content = process_request(link, 1, content)
#         print("FOUND %s Number Article Pages " % len(content['raw_text']))
#         print("DONE WITH==: " + link)

#         with open(LINK_LOG_PATH) as json_file:
#             try:
#                 decode = json.load(json_file)
#                 json_file.close()
#             except ValueError:
#                 print('OP LOG EMPTY, Using')
#                 decode = { }
#         # print(content['raw_text'])
#         content['text'] = ' '.join(content['raw_text'])
#         content.pop('raw_text', None)
#         decode[link] = content

#         with open(LINK_LOG_PATH, 'w') as json_file:
#             json.dump(decode, json_file, indent=4)
#             json_file.close()
#         # writer = open(LINK_LOG_PATH, 'a')
#         # writer.write("%s\n" % link)
#         # writer.close()
#     else:
#         print("DUPLICATE: " + link)
