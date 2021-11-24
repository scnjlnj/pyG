import logging
from datetime import datetime

import pymongo
from bson import ObjectId
from pymodm import MongoModel, connect, fields
from urllib.parse import quote_plus

from pymongo.errors import BulkWriteError




def local_now():
    return datetime.now()


class BaseModel(MongoModel):
    created_at = fields.DateTimeField(required=False, default=local_now, verbose_name="创建时间")
    updated_at = fields.DateTimeField(required=False, default=local_now, verbose_name="更新时间")
    is_finish = fields.BooleanField(default = False,verbose_name="是否完成")
    @classmethod
    def get_by_id(cls,objID):
        return cls.objects.get({"_id":ObjectId(objID)})
    @classmethod
    def get(cls,fillter,single=True,order_by="_id"):
        if single:
            return cls.objects.get(fillter)
        else:
            return cls.objects.raw(fillter).order_by([(order_by, pymongo.ASCENDING)])
    @classmethod
    def create_many(cls,data:list):
        if type(data)!=list:
            data = [data]
        objs = [cls(**o) for o in data]
        docs = []
        for o in objs:
            o.full_clean()
            docs.append(o.to_son())
        succ_num = len(docs)
        err_num = 0
        try:
            cls._mongometa.collection.insert_many(docs, ordered=False)
        except BulkWriteError as e:
            err_num = len(e.details.get("writeErrors", []))
            succ_num -= err_num
        return succ_num,err_num
class HTMLResource(BaseModel):
    class Meta:
        final = True
        collection_name = 'html'
        indexes = [
            pymongo.IndexModel([('url', pymongo.ASCENDING)], unique=True),
        ]
    url = fields.URLField(required=True,verbose_name="url地址")
    data = fields.BinaryField(required=True)
    @property
    def html(self):
        return self.data.decode()
class Comics(BaseModel):
    class Meta:
        final = True
        collection_name = 'comics'
    url = fields.URLField(required=True,verbose_name="url地址")
    name = fields.CharField()
    parser = fields.IntegerField()

    def check_finish(self):
        pk = self.pk
        cnt1 = Chapter.get({"comics":pk},single=False).count()
        if cnt1>0:
            qs = Chapter.get({"comics":pk,"is_finish":False},single=False)
            for chapter_obj in qs:
                chapter_obj.check_finish()
            cnt2 = Chapter.get({"comics":pk,"is_finish":True},single=False).count()
            if cnt2==cnt1:
                self.is_finish=True
                self.save()
                logging.info(f"Comics<{self.name} is finished>")
                return True
        if self.is_finish:
            self.is_finish=False
            self.save()
        logging.info(f"Comics<{self.name} is not finished yet!>")
        return False
class Chapter(BaseModel):
    class Meta:
        final = True
        collection_name = 'chapters'
    url = fields.URLField(required=True,verbose_name="url地址")
    name = fields.CharField()
    index = fields.IntegerField()
    comics = fields.ReferenceField(Comics)
    img_cnts = fields.IntegerField(blank=True)
    size = fields.IntegerField(blank=True)

    def check_finish(self):
        pk = self.pk
        cnt1 = Image.get({"chapter":pk},single=False).count()
        if cnt1>0:
            cnt2 = Image.get({"chapter":pk,"is_finish":True},single=False).count()
            if cnt2==cnt1:
                self.is_finish=True
                self.save()
                logging.info(f"Chapter<{self.name} is finished>")
                return True
        if self.is_finish:
            self.is_finish=False
            self.save()
        logging.info(f"Chapter<{self.name} is not finished yet!>")
        return False


class Image(BaseModel):
    class Meta:
        final = True
        collection_name = 'images'
    url = fields.URLField(required=True,verbose_name="url地址")
    chapter = fields.ReferenceField(Chapter)
    size = fields.IntegerField()
    index = fields.IntegerField()
    @property
    def parser(self):
        return self.chapter.comics.parser

def connect_mongo(mongo_config):
    # mongo-connect
    host_port = mongo_config.host_port
    database = mongo_config.db
    user = getattr(mongo_config,"username",None)
    password = getattr(mongo_config,"password",None)
    if user and password:
        uri = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host_port}/{database}?authSource=admin"
    else:
        uri = f"mongodb://{host_port}/{database}"
    connect(uri)

if __name__ == '__main__':
    from setting import MONGO_CONFIG
    connect_mongo(MONGO_CONFIG)
    doc = {
        "url":"https://manhwaworld.com/manga/skeleton-soldier-couldnt-protect-the-dungeon-016/",
        "name":"Skeleton Soldier Couldn’t Protect the Dungeon",
        "parser":1
    }
    Comics(**doc).save()