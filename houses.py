from base import Base
from sqlalchemy import Column, DateTime, Integer, Numeric, Sequence, String

class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, Sequence('houses_id_seq'), primary_key=True)
    ss_id = Column(Integer, nullable=False)
    url = Column(String(150), nullable=False)
    comment = Column(String(100))
    region = Column(String(50))
    county = Column(String(50))
    village = Column(String(50))
    address = Column(String(50))
    area = Column(Integer)
    floors = Column(Integer)
    rooms = Column(Integer)
    land = Column(Numeric)
    unit = Column(String(3))
    price = Column(Numeric)
    posted = Column(DateTime)
    created = Column(DateTime)
