from bs4 import BeautifulSoup
import coloredlogs
import logging
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0s (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}

def main():
    url = 'https://literotica.com/stories/showstory.php?id=181688'
    req = requests.get(url, headers=HEADERS)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        # title1 = soup.select('h1.headline')
        # title2 = soup.select('.b-story-header h1')[0].text
        # print(title1)
        # print(title2)

        raw_text = soup.select('.b-story-body-x p')[0].text
        print(raw_text)


if __name__ == "__main__":
    format = "[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s"
    coloredlogs.install(fmt=format, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
    main()
