from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import engine

Base = declarative_base()

class PinJuRelation(Base):
    __tablename__ = 'pin_ju_relations'
    __table_args__ = (Index("pin_id_index","pin_id",unique=False),
                      Index("ju_id_index","ju_id",unique=False))
    id = Column(Integer,primary_key=True,autoincrement=True)
    pin_id = Column(Integer)
    ju_id = Column(Integer)
    position = Column(Integer)
    hanzi = Column(String(1))

    @classmethod
    def get_pin_relations(cls, pin_id, session=None):
        if not session:
            Session = sessionmaker(bind=engine)
            session = Session()
            ret = session.query(cls).filter_by(pin_id=pin_id)
            session.close()
            return ret[:]
        else:
            ret = session.query(cls).filter_by(pin_id=pin_id)
            return ret[:]
