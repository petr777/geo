import requests
import re
import pandas as pd
from scrapy import Selector
import ast


def get_data():
    response = requests.get('https://www.anvar.kz/contacts/')
    all_shop = re.findall('BX_YMapAddPlacemark\(map, {(.*?)}, true\);' , response.text)
    good_data = []
    for shop in all_shop:
        item = dict()
        shop = ast.literal_eval('{' + shop + '}')
        item['_id'] = shop.get('ID')
        item['y'] = float(shop.get('LAT'))
        item['x'] = float(shop.get('LON'))
        html = Selector(text=shop.get('HTML'))
        item['address'] = html.xpath(
            '//div[@class="name"]/text()'
        ).extract_first().replace('Анвар-', '')
        if re.search('href="tel:(.*?)">', html.get()):
            item['phone'] = re.search('href="tel:(.*?)">', html.get())[1]
        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Анвар'
    df['holding_name'] = 'Анвар'
    return df
