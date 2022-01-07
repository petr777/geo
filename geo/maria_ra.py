import requests
import re
import pandas as pd
from faker import Faker
import json


def get_data():
    faker = Faker()
    headers = {
        'user-agent': faker.user_agent(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.get(
        'https://www.maria-ra.ru/o-kompanii/karta-seti/',
        headers = headers
    )

    JSON = re.findall("let \$objects = JSON.parse\('(.*?)'\);", response.text)
    shops = json.loads(JSON[0])
    good_data = []
    for item in shops:
        item['y'], item['x'] = item.pop('COORDINATE').split(',')

        item['y'] = float(item.pop('y'))
        item['x'] = float(item.pop('x'))

        item['work_time'] = item.get('STARTED_WORK') + '-' + item.get('END_WORK')
        del item['STARTED_WORK']
        del item['END_WORK']
        item['address'] = item.pop('NAME')
        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Мария-Ра'
    df['holding_name'] = 'Мария-Ра'
    return df
