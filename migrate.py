from base import Base, engine
from houses import House
from homesteads import Homestead

if __name__ == '__main__':
    Base.metadata.create_all(engine)