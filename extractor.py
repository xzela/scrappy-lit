''' Extracts stories from the database '''
import coloredlogs
import logging
import os
import sqlite3

DB_PATH ='./db/database.sqlite3'
FILE_PATH = './extractions'

connection = sqlite3.connect(DB_PATH, check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

def main():
    category = 'anal-sex-stories'
    file_name = FILE_PATH + '/' + category
    cursor.execute('SELECT * FROM content WHERE category="anal-sex-stories"')
    with open(file_name, 'w+') as file:
        for row in cursor:
            if not row['content']:
                logging.info('SKIPING %s because it is empty', row['link'])
                continue
            logging.info('Writing %s to file', row['link'])
            file.write(row['content'] + '\n')
    file.close()
    connection.close()

if __name__ == "__main__":
    format = "[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s"
    coloredlogs.install(fmt=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    main()

