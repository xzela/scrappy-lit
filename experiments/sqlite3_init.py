import signal
import sqlite3
import sys

DB_PATH = './db/database.sqlite3'
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, link TEXT, title TEXT, content TEXT);')

def insert_record(category, link):
    cursor.execute('SELECT * FROM content WHERE category=? AND link=?', (category, link))
    row = cursor.fetchone()
    print(row)
    if row and row[0] > 0:
        print("Skipping %s %s" % (category, link))
        return
    else:
         print("Would have wrote %s %s" % (category, link))

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    connection.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


category = 'anal-sex-stories'
link = 'https://www.literotica.com/s/b-is-also-for-barbie-doll'

insert_record(category, link);
