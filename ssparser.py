import re
from bs4 import BeautifulSoup
from datetime import datetime

class ExtraParser(object):
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    def get_posted(self):
        tds = self.soup.findAll(class_='msg_footer')
        for td in tds:
            content = str(td.contents[0])
            if 'Datums: ' in content:
                date = content.replace('Datums: ', '')
                return datetime.strptime(date, '%d.%m.%Y %H:%M')
        return None

    def get_td(self, td_id):
        data = self.soup.find(id=td_id)
        return clear_b(str(data.contents[0])) if data else None


class HouseParser(object):
    def __init__(self, tr):
        self.tds = tr.findAll('td')
        self.tr = tr

    def get_comment(self):
        return clear_b(self.tds[2].contents[0].find('a').contents[0])

    def get_data(self, index):
        return clear_b(''.join(map(str, self.tds[index].contents)))

    def get_land(self):
        land = re.findall(r'([\d\.]+) ', self.get_data(7))
        return land[0] if len(land) else None

    def get_price(self):
        return int(re.search(r'[\d,]+', self.get_data(8)).group() \
            .replace(",", ""))

    def get_unit(self):
        land = re.findall(r' (.+)', self.get_data(7))
        return land[0] if len(land) else None

    def get_url(self):
        return self.tds[1].contents[0]['href']


def clear_b(raw):
    return str(raw).replace('<b>', '').replace('</b>', '')

def get_id(tr):
    return re.findall(r'id="tr_(\d+)"', str(tr))[0]

def get_trs(page):
    page_soup = BeautifulSoup(page, 'html.parser')
    return page_soup.find_all('tr', id=re.compile(r'^tr_\d+'))