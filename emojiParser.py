import requests
from bs4 import BeautifulSoup
import sys


class Parser:

    def __init__(self, url):
        self.url = url
        self.emojis = {}

    def parseDatabase(self):
        page = requests.get(self.url)
        if page.status_code != 200:
            sys.exit(-1);
        soup = BeautifulSoup(page.text, 'lxml')
        emojis_a = soup.find('ul', class_='emoji-list')
        for emoj in emojis_a.findChildren('a', recursive=True):
            self.emojis[emoj.contents[1].lower().strip()] = emoj.next.next
        print(f'Database Loaded')

    def printEmoj(self, step):
        idx = 0
        for key, val in self.emojis.items():
            idx += 1
            if idx % step == 0:
                print('')
            print(f'\t{val}', end='')
        print('')

    def getEmogi(self, key):
        local = self.emojis.get(key)
        if local is None:
            return key
        return local
