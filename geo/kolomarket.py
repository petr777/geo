import requests
import re
import pandas as pd
import json


def get_data():
    response = requests.get(
        'https://kolomarket.com.ua/ru/our-shops/',
    )
    data = re.findall('var shopsList = \[(.*?)}]', response.text)[0]
    data = '['+ data + '}]'
    JSON = json.loads(data)
    good_data = []
    for row in JSON:
        for shop in row['cityShopsList']:
            item = dict()
            item['address'] = shop[0]
            item['y'] = float(shop[1])
            item['x'] = float(shop[2])
            item['work_time'] = f'{shop[3]} - {shop[4]}'
            good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'КОЛО'
    df['holding_name'] = 'АРИТЕЙЛ'
    return df

