import logging
import threading
import time
import concurrent.futures
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}

def getUrl(url, index):
    url += "?page=" + str(index)
    logging.info("Fetching URL: %s", url)
    req = requests.get(url, headers=HEADERS, allow_redirects=False)
    if req.status_code != 200:
        return False
    return True

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        url = 'https://www.literotica.com/s/hadleys-other-cherry-ch-03'
        i = 0
        while True:
            executor.submit(getUrl, url, i)
            i += 1

