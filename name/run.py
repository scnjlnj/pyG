from config import engine
from model.juzi import JuZi
from model.pin_ju_relations import PinJuRelation
from model.pinyin_model import PinYin

if __name__ == '__main__':
    for c in [PinJuRelation,JuZi,PinYin]:
        c.__table__.create(engine)
    PinYin.init_create()