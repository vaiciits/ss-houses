from ast import Str
from base import Base
from sqlalchemy import Column, DateTime, Integer, Numeric, Sequence, String

class Homestead(Base):
    __tablename__ = 'homesteads'
    id = Column(Integer, Sequence('homesteads_id_seq'), primary_key=True)
    ss_id = Column(Integer, nullable=False)
    url = Column(String(159), nullable=False)
    comment = Column(String(100))
    region = Column(String(50))
    county = Column(String(50))
    village = Column(String(50))
    area = Column(Integer)
    floors = Column(Integer)
    land = Column(Numeric)
    unit = Column(String(3))
    price = Column(Numeric)
    posted = Column(DateTime)
    created = Column(DateTime)
