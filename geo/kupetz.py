import re
import requests
from scrapy import Selector
from html_text import extract_text
import pandas as pd


def get_data():
    response = requests.get('http://www.tc-kupetz.ru/index/ru/shop/')
    page = Selector(text=response.text)
    good_data = []
    for shop in page.xpath('//div[@id="item"]'):
        item = dict()
        address = shop.xpath('./div[@class="title"]/strong/text()')
        if address:
            item['address'] = address.extract_first()
        else:
            continue
        rows = extract_text(shop.xpath('./div[@style="DISPLAY: none"]').get())
        rows = rows.split('\n')
        for row in rows:
            if 'Часы работы:' in row:
                item['work_time'] = re.sub('Часы работы: ', '', row)
        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Купец'
    df['holding_name'] = 'Купец̆'
    return df