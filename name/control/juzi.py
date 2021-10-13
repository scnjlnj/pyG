import pinyin
from sqlalchemy.orm import sessionmaker

from config import engine
from model import Name_pin
from model.juzi import JuZi
from model.pin_ju_relations import PinJuRelation
from model.pinyin_model import PinYin

stop_set = {
    ",", ".", ";", ":", "?", "'", "\"", "!", "`",
    "，", "。", "；", "：", "？", "‘", "’", "”", "“", "【", "】", "（", "）", "{", "}", "—",
    "…", "《", "》", "〈", "〉", "·", "—", "、", "·"
}


class JuziContoller():
    mod = JuZi

    @classmethod
    def add_juzi(cls, data: list):
        # todo 新增句子时候考虑多音字的情况。pinyin库功能不支持多音字，后续拟使用新华字典数据集来得到汉字拼音。
        if type(data) is str:
            data = [data]
        Session = sessionmaker(bind=engine)
        session = Session()
        for j in data:
            obj = cls.mod(text=j)
            session.add(obj)
            session.flush()
            ju_id = obj.id
            for pos, zi in enumerate(j):
                if zi in stop_set:
                    continue
                else:
                    pin = pinyin.get(zi)
                    pin_id = PinYin.get_id(pin, session).id
                    session.add(PinJuRelation(pin_id=pin_id, ju_id=ju_id, position=pos, hanzi=j[pos]))
                    session.commit()
            session.close()

    @classmethod
    def pin_quote_info(cls, pin):
        pin_id = PinYin.get_id(pin).id
        relation_ju = PinJuRelation.get_pin_relations(pin_id)
        ret = {}
        for r in relation_ju:
            ret.update({r.ju_id: r.position})
        return ret

    @classmethod
    def name_quote_info(cls, name: Name_pin):
        infos = [cls.pin_quote_info(name.family_name)] + [cls.pin_quote_info(x) for x in name.given_name]
        lenth = len(infos)
        if lenth != 3:
            raise AssertionError
        sets = [set(infos[0]) & set(infos[1]),
                set(infos[0]) & set(infos[2]),
                set(infos[1]) & set(infos[2]),
                set(infos[0]) & set(infos[1]) & set(infos[2])]
        ret = []
        for ind, s in enumerate(sets):
            if ind == 0:
                pins = name.family_name.upper() + name.given_name[0].upper() + name.given_name[1]
            elif ind == 1:
                pins = name.family_name.upper() + name.given_name[0] + name.given_name[1].upper()
            elif ind == 2:
                pins = name.family_name + name.given_name[0].upper() + name.given_name[1].upper()
            else:
                pins = name.family_name.upper() + name.given_name[0].upper() + name.given_name[1].upper()
            temp = {
                "pins": pins,
                "choice": []
            }
            for j in s:
                pos = [infos[i].get(j) for i in range(lenth)]
                temp["choice"].append({"pos": pos, "ju_id": j})
            ret.append(temp)
        return ret
