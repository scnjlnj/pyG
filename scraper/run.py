import logging
import os
import time

from bs4 import BeautifulSoup

from control import Controller
from html_parser import ManhwaWorldParser, ParserMAP
from model import Comics, connect_mongo, Chapter, Image
from setting import CACHE_FOLDER, KEEP_ALIVE, HEADER, MONGO_CONFIG, IMAGE_FOLDER
from thread_scraper import Scraper

os.makedirs(CACHE_FOLDER,exist_ok=True)
os.makedirs(IMAGE_FOLDER,exist_ok=True)
logging.getLogger().setLevel(logging.INFO)



if __name__ == '__main__':
    # url = "https://manhwaworld.com/manga/skeleton-soldier-couldnt-protect-the-dungeon-016/"
    # url2 = "https://manhwaworld.com/manga/skeleton-soldier-couldnt-protect-the-dungeon-016/chapter-1/"
    connect_mongo(MONGO_CONFIG)
    control = Controller(worker=8)
    control.start_all_asyn_worker()

    # 获取comics中chapters以及images的urls
    failure = []
    comics_id = "61976a8d94c70039df4878e7"
    chapter_ids = control.get_chapter_ids(comics_id)
    for chapter_id in chapter_ids:
        # 获取章节图片链接
        status = control.save_chapter_image_urls(chapter_id)
        if status==-1:
            failure.append(chapter_id)
            continue
        # 发布下载任务
        control.asyn_task_download_chapter(chapter_id)
        if status == 1:
            time.sleep(5)
    control.auto_check_fininsh(comics_id)
    control.threadpool.joinAll()
