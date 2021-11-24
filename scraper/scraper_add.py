from control import Controller
from model import connect_mongo
from setting import MONGO_CONFIG

connect_mongo(MONGO_CONFIG)
control = Controller(worker=5)
control.start_all_asyn_worker()
control.threadpool.joinAll()
