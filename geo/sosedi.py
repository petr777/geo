import requests
from scrapy import Selector
import pandas as pd
import json


def get_data():
    response = requests.get('https://sosedi.by/shops/')
    page = Selector(text=response.text)
    data = page.xpath('//div[@data-component="Map"]/@data-initial').get()
    JSON = json.loads(data)
    good_data = []
    for shop in JSON['points']:
        item = {}
        item['city'] = shop.get('city')
        item['address'] = shop.get('adds')
        item['phone'] = shop.get('phone')
        if type(shop.get('timeWork')) == dict:
            item['work_time'] = shop.get('timeWork').get('start') + '-' + shop.get('timeWork').get('end')
        elif shop.get('timeWork'):
            item['work_time'] = '24/7'
        item['y'] = shop.get('coordinates', {}).get('lat')
        item['x'] = shop.get('coordinates', {}).get('lng')
        good_data.append(item)
    return good_data


def pd_data():
    good_data=get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] ='Соседи'
    df['holding_name']='Соседи'
    return df


