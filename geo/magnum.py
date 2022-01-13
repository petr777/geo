import requests
import json
from scrapy import Selector
from html_text import extract_text
import ast
import re
import pandas as pd


def get_data():
    session = requests.Session()
    resp = session.get('https://magnum.kz')
    page = Selector(text=resp.text)
    all_city = page.xpath('//a[@class="dropdown-item select-city"]/@data-city').getall()
    all_city = [json.loads(city) for city in all_city]
    csrf = page.xpath('//meta[@name="csrf-token"]/@content').get()
    good_data = []
    for city in all_city:
        city_name = city.get('name')
        data = {
            '_token': csrf,
            'city_id': city.get('id'),
        }
        session.post('https://magnum.kz/city', data=data)
        resp = session.get('https://magnum.kz/page/magaziny')
        page = Selector(text=resp.text)
        ul = page.xpath('//ul[contains(@class, "stores__addresses__list")]/li')
        for li in ul:
            item = {}
            item['city'] = city_name
            item['store_id'] = li.xpath('./@id').extract_first()
            lonlat = ast.literal_eval(li.xpath('./@data-cords').extract_first())
            item['y'] = lonlat[0]
            item['x'] = lonlat[1]
            item['phone'] = li.xpath('./@data-phone').extract_first()
            item['work_time'] = li.xpath('./@data-mod').extract_first()
            text = extract_text(li.get())
            type_shop = re.search('\((.*?)\)', text)
            if type_shop:
                item['type'] = re.search('\((.*?)\)', text)[1]
            item['address'] = text
            good_data.append(item)
    return good_data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Magnum'
    df['holding_name'] = 'Magnum'
    return df