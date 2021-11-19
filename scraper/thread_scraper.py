import logging
import os
import threading
import time
from datetime import datetime
import requests



class Scraper(threading.Thread):
    """
    thread scraper
    """

    def __init__(self, keep_alive,headers, name, cache_folder):
        threading.Thread.__init__(self)
        self.name = name
        self.headers = headers
        self.cache_folder = cache_folder
        self.session = self.make_session(keep_alive)
        # self.start()
    def make_session(self,keep_alive):
        s = requests.session()
        s.keep_alive = keep_alive
        return s
    def get_url(self,url):
        file_path = os.path.join(self.cache_folder, url.strip("/").rsplit("/",1)[-1] + ".html")
        try:
            with open(file_path,encoding="utf-8") as f:
                html = f.read()
        except:
            resp = self.session.get(url, headers=self.headers, verify=False)
            html = resp.text
            if resp.status_code>=400:
                logging.warning(f"url:{url} 请求失败!")
                return
            else:
                with open(file_path,"w",encoding="utf-8") as f:
                    f.write(html)
        return html
    def run(self):
        while True:
            try:
                file_path, request_id = self.queue.get()
                time.sleep(0.5)  # 等文件保存好
                StartTime = datetime.utcnow()
                CreateTime = os.stat(file_path).st_mtime
                WaitingTime = datetime.now().timestamp() - CreateTime
                logging.info(
                    f"WorkerName:{self.name} --> Task Received,File:{file_path},RequestId:{request_id},StartTime_utc:{StartTime},WaitingTime:{WaitingTime} s")
                cnt = write_db(file_path, request_id, CreateTime)
                FinishTime = datetime.utcnow()
                logging.info(
                    f"WorkerName:{self.name} --> Task Done,{cnt} rows inserted.File:{file_path},RequestId:{request_id},FinishTime_utc:{FinishTime},Duration:{(FinishTime - StartTime).seconds}")
                self.queue.task_done()
            except Exception as e:
                logging.error(f"error:{e}")
                continue  # 报错后worker继续工作

class ScraperThreadPool():
        def __init__(self, queue, size):
            logging.info("Creating data sink workers...")
            self.queue = queue
            self.pool = []
            for i in range(size):
                self.pool.append(Scraper(queue, f"Worker{i}"))
            logging.info("Workers are ready")
            logging.info("Waiting for new request files...")

        def joinAll(self):
            for thd in self.pool:
                if thd.is_alive():  thd.join()

