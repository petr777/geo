import requests
import re
import pandas as pd
import json


def get_data():
    response = requests.get('https://www.eko.com.ua/ua/network/')
    data = re.findall('var shops = \[(.*?)];', response.text)[0]
    data = f'[{data}]'
    JSON = json.loads(data)
    good_data = []
    for shop in JSON:
        item = {}
        item['id'] = shop.get('shop_id')
        item['name'] = shop.get('shop_name')
        item['city'] = shop.get('city_name')
        item['address'] = shop.get('shop_address').strip()
        item['work_time'] = shop.get('shop_mode').strip()
        item['y'] = shop.get('shop_lng').strip()
        item['x'] = shop.get('shop_lat').strip()
        good_data.append(item)
    return good_data


def pd_data():
    good_data=get_data()
    df = pd.DataFrame(good_data)
    df['brand_name']='ЕКО маркет'
    df['holding_name']='ЕКО маркет'
    return df

