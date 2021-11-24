import logging
import os
import queue

from bson import ObjectId
from pymodm.errors import DoesNotExist

from html_parser import ParserMAP
from model import HTMLResource, Chapter, Image, Comics
from setting import *
from thread_scraper import ScraperThreadPool, Scraper


class Controller():
    def __init__(self,worker):
        self.queue = queue.Queue(maxsize=0)
        self.threadpool = ScraperThreadPool(queue=self.queue,size=worker)
        self.syn_scraper = Scraper(self.queue,"syn_scraper",KEEP_ALIVE,HEADER)
        # self.start_all_asyn_worker()
    def start_all_asyn_worker(self):
        self.threadpool.startAll()
        logging.info("Asyn workers are waiting for tasks...")
    def get_html(self,url):
        try:
            obj = HTMLResource.get({"url":url})
            return obj.html
        except DoesNotExist as e:
            s = self.syn_scraper
            html = s.get_url(url)
            HTMLResource(url=url,data=html.encode()).save()
            return html
    def asyn_task_download_chapter(self,chapter):
        if type(chapter) is not Chapter:
            chapter:Chapter= Chapter.get_by_id(chapter)
        chapter_id = chapter.pk
        chapter_name = chapter.name
        comics_name = chapter.comics.name
        images = Image.get({"chapter":chapter_id,"is_finish":False},single=False,order_by="index")
        os.makedirs(os.path.join(IMAGE_FOLDER,comics_name,chapter_name).replace(" ","_"),exist_ok=True)
        cnt=0
        for img in images:
            file_path = os.path.join(IMAGE_FOLDER,comics_name,chapter_name,str(img.index)+".jpg").replace(" ","_")
            task = (
                "DOWNLOAD_IMAGE",
                (img.url,file_path,img),
                IMAGE_DOWNLOAD_MAX_RETRY
            )
            self.queue.put(task)
            cnt+=1
        logging.info(f"Chapter<{chapter_name}> {cnt} of image download tasks put to queue")
        return cnt
    def save_chapter_image_urls(self,chapter_id):
        chapter_obj = Chapter.get_by_id(chapter_id)
        if Image.get({"chapter":chapter_obj.pk},single=False).count()>0:
            logging.info(f"Chapter:{chapter_obj.name} image urls already cached")
            return 0
        parser = ParserMAP[chapter_obj.comics.parser]()
        try:
            html_chapter = self.get_html(chapter_obj.url)
            logging.info(f"Successfully got chapter:{chapter_obj.name} html")
        except Exception as e:
            print(e)
            logging.info(f"Fail to get chapter:{chapter_obj.name} html")
            return -1
        ret2 = parser.get_images_list(html_chapter)
        for r in ret2:
            r["chapter"] = chapter_obj.pk
        Image.create_many(ret2)
        logging.info(f"Successfully cached chapter:{chapter_obj.name} image urls")
        return 1
    def get_chapter_ids(self, comics_id,update=False):
        c_obj = Comics.get_by_id(comics_id)
        qs = Chapter.get({"comics": c_obj.pk}, single=False)
        if not update and qs.count() > 0:
            logging.info(f"Comics:{c_obj.name} image urls already cached")
            return [x.pk for x in qs]
        else:
            try:
                html_comics = self.get_html(c_obj.url)
                logging.info(f"Successfully got comics:{c_obj.name} html")
            except Exception as e:
                print(e)
                logging.error(f"Fail to get comics:{c_obj.name} html")
                return []
            parser = ParserMAP[c_obj.parser]()
            ret = parser.get_chapters_list(html_comics)
            for r in ret:
                r["comics"] = c_obj.pk
                r["_id"] = ObjectId()
            id_set = set([x.pk for x in qs])
            Chapter.create_many([x for x in ret if x.pk not in id_set])
            logging.info(f"Successfully cached comics:{c_obj.name} chapter urls")
            return [x["_id"] for x in ret]

    def auto_check_fininsh(self, comics_id):
        c_obj = Comics.get_by_id(comics_id)
        c_obj.check_finish()


