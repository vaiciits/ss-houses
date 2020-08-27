from params import Params
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgres://' + Params['db-ssflats']['user'] +
    ':' + Params['db-ssflats']['password'] + '@' +
    Params['db-ssflats']['host'] + ':' +
    str(Params['db-ssflats']['port']) + '/' +
    Params['db-ssflats']['database'])

Session = sessionmaker(bind=engine)

Base = declarative_base()