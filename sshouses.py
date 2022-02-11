import requests, ssparser
from base import Session
from datetime import datetime
from houses import House

class HousesCrawler(object):
    def __init__(self, url):
        self.count = 0
        self.session = Session()
        self.url = url

    def crawl(self):
        page = self.get_page(self.url)
        trs = ssparser.get_trs(page)
        for tr in trs:
            ss_id = ssparser.get_id(tr)
            record = self.session.query(House) \
                .filter(House.ss_id == ss_id) \
                .first()
            if record is None:
                house = self.populate(tr, ss_id)
                self.session.add(house)
                self.session.commit()
                self.count += 1

    def get_page(self, url):
        try:
            html = requests.get('https://www.ss.com' + url)
        except Exception as e:
            print(e)
            return ''
        else:
            return html.content.decode()

    def populate(self, tr, ss_id):
        parser = ssparser.HouseParser(tr)
        house = House(ss_id=ss_id,
                      url=parser.get_url(),
                      comment=parser.get_comment(),
                      area=int(parser.get_data(4)),
                      floors=int(parser.get_data(5)),
                      rooms=int(parser.get_data(6)),
                      land=parser.get_land(),
                      unit=parser.get_unit(),
                      price=parser.get_price(),
                      created=datetime.now())
        return self.populate_extra(house)

    def populate_extra(self, house):
        parser = ssparser.ExtraParser(self.get_page(house.url))
        house.region = parser.get_td('tdo_20')
        house.county = parser.get_td('tdo_856')
        house.village = parser.get_td('tdo_368')
        house.address = parser.get_td('tdo_11')
        house.posted = parser.get_posted()
        # TODO: get amenities
        return house


if __name__ == '__main__':
    print('House crawler started at', datetime.now())
    crawler = HousesCrawler(
        '/lv/real-estate/homes-summer-residences/today-2/sell/')
    crawler.crawl()
    print('Added', crawler.count)
