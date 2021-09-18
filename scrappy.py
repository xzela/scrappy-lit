'''Some module'''
from bs4 import BeautifulSoup
import coloredlogs
import logging
from queue import Queue
from threading import Thread
from time import time
import requests
import sqlite3
import signal
import sys
import time
import concurrent.futures
from urllib.parse import urlparse

DB_PATH ='./db/database.sqlite3'
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

connection = sqlite3.connect(DB_PATH, check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, link TEXT, title TEXT, content TEXT);')
cursor.execute('CREATE INDEX IF NOT EXISTS category_index ON content (category);')

def signal_handler(sig, frame):
    logging.critical('You pressed Ctrl+C! Closing Application')
    connection.close()
    sys.exit(0)

def insert_link(category, link):
    cursor.execute('SELECT * FROM content WHERE category=? AND link=?', (category, link))
    row = cursor.fetchone()
    if row and len(row) > 0:
        logging.warning("Skipping Category: %s Link: %s" % (category, link))
        return
    cursor.execute('INSERT INTO content (category, link) VALUES (?, ?)', (category, link))
    connection.commit()

def update_link(category, link, title, text):
    cursor.execute('SELECT * FROM content WHERE category=? AND link=?', (category, link))
    row = cursor.fetchone()
    if row and len(row) > 0 and not row['title']:
        id = row['id']
        cursor.execute('UPDATE content SET title=?, content=? WHERE id=?', (title, text, id))
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

def determine_articles(href, pagination, num, content):
    '''Gets a list of articles from the results page'''
    url = href
    if pagination == True:
        url += "?page=" + str(num)
    # ensure the url is using a valid scheme
    o = urlparse(url)
    parsedUrl = o.geturl()
    if o.scheme != 'https':
        parsedUrl = o._replace(scheme='https').geturl()
    req = requests.get(parsedUrl, headers=HEADERS, allow_redirects=False)
    if req.status_code == 200:
        time.sleep(2.5)
        num += 1
        soup = BeautifulSoup(req.text, 'html.parser')
        content['title'] = soup.select('h1.headline')[0].text
        content['raw_text'] = content['raw_text'] + extract_article(soup)
        return determine_articles(href, True, num, content)
    else:
        logging.warning("URL: %s Returned status code: %s", url, str(req.status_code))
    return content

def fetch_category_page(category, num):
    '''Loops through a category and determines the number of pages of articles'''
    # Fetch the initial page
    BASE_URL = 'https://www.literotica.com/c/' + str(category) + '/' + str(num) + '-page'
    logging.info("Fetching URL: %s", BASE_URL)
    page = requests.get(BASE_URL, headers=HEADERS, allow_redirects=False)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        stories = soup.find_all('div', class_='b-sl-item-r')
        links = []
        for story in stories:
            # link = story.find('h3').find('a')['href']
            links.append(story.find('h3').find('a')['href'])
            # insert_link(category, link)
        return links
    else:
        return []

def main():
    logging.info("Initializing")
    for category in CATEGORIES:
        num = 1
        links = []
        while items := fetch_category_page(category, num):
            # time.sleep(0.01)
            num += 1
            for story in items:
                links.append(story)
        for link in links:
            insert_link(category, link)
            content = determine_articles(link, False, 1, { 'raw_text': [] })
            content['text'] = ' '.join(content['raw_text'])
            content.pop('raw_text', None)
            update_link(category, link, content['title'], content['text'])

        # logging.info("Found %s Pages for %s Category" % (len(links), category))
        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     futures = []
        #     for link in links:
        #         futures.append(executor.submit(insert_link, category, link))


if __name__ == "__main__":
    format = "[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s"
    coloredlogs.install(fmt=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    main()
