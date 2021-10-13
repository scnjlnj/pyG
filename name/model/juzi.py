from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class JuZi(Base):
    __tablename__ = 'juzi'
    id = Column(Integer,primary_key=True,autoincrement=True)
    text = Column(String(256))