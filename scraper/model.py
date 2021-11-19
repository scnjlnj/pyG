from datetime import datetime

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
    def create_many(cls,data:list):
        if type(data)!=list:
            data = [data]
        docs = [cls(**o).full_clean().to_son() for o in data]
        succ_num = len(docs)
        try:
            cls._mongometa.collection.insert_many(docs, ordered=False)
        except BulkWriteError as e:
            err_num = len(e.details.get("writeErrors", []))
            succ_num -= err_num
        return succ_num,err_num
class Comics(BaseModel):
    class Meta:
        final = True
        collection_name = 'comics'
    url = fields.URLField(required=True,verbose_name="url地址")
    name = fields.CharField()
    parser = fields.IntegerField()
class Chapter(BaseModel):
    class Meta:
        final = True
        collection_name = 'chapters'
    url = fields.URLField(required=True,verbose_name="url地址")
    name = fields.CharField()
    index = fields.IntegerField()
    comics = fields.ReferenceField(Comics)
    img_cnts = fields.IntegerField()
    size = fields.IntegerField()
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
    user = mongo_config.username
    password = mongo_config.password
    if user and password:
        uri = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host_port}/{database}?authSource=admin"
    else:
        uri = f"mongodb://{host_port}/{database}"
    connect(uri)