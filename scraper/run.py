import os

from bs4 import BeautifulSoup

from html_parser import ManhwaWorldParser
from setting import CACHE_FOLDER, KEEP_ALIVE, HEADER
from thread_scraper import Scraper

os.makedirs(CACHE_FOLDER,exist_ok=True)




if __name__ == '__main__':
    url = "https://manhwaworld.com/manga/skeleton-soldier-couldnt-protect-the-dungeon-016/"
    cc1 = Scraper(KEEP_ALIVE,HEADER,"cc1",CACHE_FOLDER)
    data = cc1.get_url(url)
    soup = BeautifulSoup(data,parser="html.parser",features="lxml")
    ret = ManhwaWorldParser().parse_chapters(soup=soup)
    print("OK")