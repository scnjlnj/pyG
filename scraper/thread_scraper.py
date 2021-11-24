import logging
import os
import socket
import threading
import time
from datetime import datetime
from urllib import request
from urllib.error import HTTPError

import requests
from urllib3.exceptions import MaxRetryError

from setting import KEEP_ALIVE, HEADER

img_download_header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}


class Scraper(threading.Thread):
    """
    thread scraper
    """
    @property
    def TASK_TYPE(self):
        return {
            "DOWNLOAD_IMAGE": self.download_image,
        }

    def __init__(self,queue,name,keep_alive,headers):
        threading.Thread.__init__(self)
        self.name = name
        self.headers = headers
        self.queue = queue
        self.session = self.make_session(keep_alive)
        self.daemon=True
        # self.start()
    def make_session(self,keep_alive):
        s = requests.session()
        s.keep_alive = keep_alive
        return s
    def get_url(self,url):
        try:
            resp = self.session.get(url, headers=self.headers,timeout=10)
            html = resp.text
            ok=True
        except MaxRetryError:
            ok=False
        if (not ok) or resp.status_code >= 400:
            try:
                req = request.Request(url, headers=self.headers)
                data = request.urlopen(req, timeout=10)
                html = data.read().decode()
            except HTTPError:
                logging.warning(f"url:{url} 请求失败!")
                return
            except socket.timeout:
                logging.warning(f"url:{url} 请求超时!")
                return
        # file_path = os.path.join(self.cache_folder, url.strip("/").rsplit("/",1)[-1] + ".html")
        # try:
        #     with open(file_path,encoding="utf-8") as f:
        #         html = f.read()
        # except:
        #     resp = self.session.get(url, headers=self.headers)
        #     html = resp.text
        #     if resp.status_code>=400:
        #         try:
        #             req = request.Request(url, headers=self.headers)
        #             data = request.urlopen(req)
        #             html = data.read().decode()
        #         except HTTPError:
        #             logging.warning(f"url:{url} 请求失败!")
        #             return
        #     with open(file_path,"w",encoding="utf-8") as f:
        #         f.write(html)
        return html
    def download_image(self,img_url,file_path,img_obj):
        try:
            ret = requests.get(url=img_url,headers = img_download_header,stream=True)
            if ret.status_code==200:
                with open(file_path,"wb") as f:
                    f.write(ret.content)
                img_obj.is_finish = True
                img_obj.size = len(ret.content)
                img_obj.save()
                return True
            else:
                raise AssertionError("请求失败")
        except Exception as e:
            print(e)
            return False
    def run(self):
        while True:
            task_type, args, retry = self.queue.get()
            try:
                StartTime = datetime.now()
                logging.info(
                    f"WorkerName:{self.name} --> Task Received,Type:{task_type},RequestId:{args},StartTime:{StartTime} s")
                ok = self.TASK_TYPE[task_type](*args)
                FinishTime = datetime.now()
                Dur = FinishTime - StartTime
                if not ok:
                    retry -= 1
                    if retry > 0:
                        self.queue.put((task_type, args, retry))
                    logging.info(f"WorkerName:{self.name} --> Task Fail,FailTime:{FinishTime},Duration:{Dur.seconds+Dur.microseconds/1000000}s")
                else:
                    logging.info(
                        f"WorkerName:{self.name} --> Task Done,FinishTime:{FinishTime},Duration:{Dur.seconds+Dur.microseconds/1000000}s")
                logging.info(
                    f"{len(self.queue.queue)} Task Remain")
                self.queue.task_done()
            except Exception as e:
                logging.error(f"error:{e}")
                continue  # 报错后worker继续工作

class ScraperThreadPool():
        def __init__(self, queue, size):
            logging.info("Creating scrape workers...")
            self.queue = queue
            self.pool = []
            for i in range(size):
                self.pool.append(Scraper(queue, f"Worker{i}", KEEP_ALIVE, HEADER))
            logging.info("Workers are ready")

        def joinAll(self):
            for thd in self.pool:
                if thd.is_alive():  thd.join()

        def startAll(self):
            for thd in self.pool:
                if not thd.is_alive():
                    thd.start()

