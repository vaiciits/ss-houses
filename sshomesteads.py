import requests, smtplib, ssl, ssparser
from base import Session
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from homesteads import Homestead
from params import Params

class HomesteadsCrawler(object):
    def __init__(self, url):
        self.count = 0
        self.emails = 0
        self.params = Params
        self.session = Session()
        self.url = url

    def crawl(self):
        page = self.get_page(self.url)
        trs = ssparser.get_trs(page)
        for tr in trs:
            ss_id = ssparser.get_id(tr)
            record = self.session.query(Homestead) \
                .filter(Homestead.ss_id == ss_id) \
                .first()
            if record is None:
                house = self.populate(tr, ss_id)
                self.session.add(house)
                self.session.commit()
                self.count += 1
                self.email_filter(house)

    def email_filter(self, house):
        receivers = self.params['email']['receivers']

        for receiver in receivers:
            if house.price <= receiver['price'] and house.region in receiver['regions']:
                self.send_email(house, receiver['email'])

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
        # print(parser.tds)
        house = Homestead(ss_id=ss_id,
                      url=parser.get_url(),
                      comment=parser.get_comment(),
                      area=int(parser.get_data(5)),
                      floors=int(parser.get_data(4)),
                    #   rooms=int(parser.get_data(6)),
                      land=parser.get_land(6),
                      unit=parser.get_unit(6),
                      price=parser.get_price(7),
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

    def send_email(self, house, receiver):
        url = 'https://www.ss.com' + house.url
        port = self.params['email']['port']
        sender = self.params['email']['sender']
        password = self.params['email']['password']
        email_server = self.params['email']['server']
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(email_server, port, context=context) as server:
            server.login(sender, password)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Atrasta viensēta'
            msg['From'] = sender
            msg['To'] = receiver
            plain = """\
                Sludinājuma cena: {}
                Rajons: {}
                Cena: {}
                Saite: {} """.format(house.price, house.region, house.price, url)
            html = """\
                <html>
                    <body>
                        <p>
                            Sludinājuma cena ir {} EUR<br>
                            Dzīvokļa platība ir {} m2<br>
                            Cena par m2 ir {} EUR<br>
                            Saite: {}
                        </p>
                    </body>
                </html>
                """.format(house.price, house.region, house.price, url)
            part1 = MIMEText(plain, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            server.sendmail(sender, receiver, msg.as_string())
            self.emails += 1


if __name__ == '__main__':
    print('Homestead crawler started at', datetime.now())
    crawler = HomesteadsCrawler(
        '/lv/real-estate/farms-estates/today-2/sell/')
    crawler.crawl()
    print('Added', crawler.count)
