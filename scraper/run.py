import os

from bs4 import BeautifulSoup

from html_parser import ManhwaWorldParser
from model import Comics, connect_mongo, Chapter, Image
from setting import CACHE_FOLDER, KEEP_ALIVE, HEADER, MONGO_CONFIG
from thread_scraper import Scraper

os.makedirs(CACHE_FOLDER,exist_ok=True)




if __name__ == '__main__':
    # url = "https://manhwaworld.com/manga/skeleton-soldier-couldnt-protect-the-dungeon-016/"
    # url2 = "https://manhwaworld.com/manga/skeleton-soldier-couldnt-protect-the-dungeon-016/chapter-1/"
    connect_mongo(MONGO_CONFIG)
    comics_id = "61976a8d94c70039df4878e7"
    comics_obj = Comics.get_by_id(comics_id)
    url = comics_obj.url
    cc1 = Scraper(KEEP_ALIVE,HEADER,"cc1",CACHE_FOLDER)
    html_comics = cc1.get_url(url)
    ret = ManhwaWorldParser().get_chapters_list(html_comics)
    for r in ret:
        r["comics"] = comics_obj.pk
    Chapter.create_many(ret)
    # # 获取图片链接
    # html_chapter = cc1.get_url(ret[0]["url"])
    # ret2 = ManhwaWorldParser().get_chapters_list(html_comics)
    # for r in ret2:
    #     r["comics"] = comics_obj.pk
    # Image.create_many(ret2)
    print("OK")