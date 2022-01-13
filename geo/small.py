import requests
import re
import pandas as pd
import json
from scrapy import Selector


def get_page(url):
    response = requests.get(url)
    page = Selector(text=response.text)
    return page


def get_data():
    shop_type = {
        1: 'Премиум магазин',
        2: 'Супермаркет',
        3: 'Дискаунтер',
        4: 'Магазин у дома',
        5: 'Головной офис',
        6: 'Магазин напитков'
    }
    page = get_page('https://small.kz/')
    cities = set(page.xpath('//div[@class="d-flex-center-between-wrap"]/form/@id').getall())
    good_data = []
    for city in cities:
        url = f'https://small.kz/ru/{city}/shops'
        page = get_page(url)
        city = page.xpath(
            '//div[@class="firstHeader"]//a[@class="popup-with-move-anim"]/span/text()'
        ).extract_first().strip()
        data = re.findall('let point_list = (.*?);', page.get())[0]
        JSON = json.loads(data)
        for shop in JSON:
            item = {}
            item['name'] = shop['name']
            item['city'] = city
            item['shop_type'] = shop_type.get(shop['shop_type'])
            item['address'] = shop['address']
            item['work_time'] = shop['working_hours']
            item['y'] = float(shop['latitude'])
            item['x'] = float(shop['longitude'])
            good_data.append(item)
    return good_data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Small'
    df['holding_name'] = 'Small'
    return df

