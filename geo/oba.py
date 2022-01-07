import requests
import re
import pandas as pd
from faker import Faker
import json

def get_data():
    response = requests.get(
        'https://oba.az/branches/?mapjson=rv',
    )
    JSON = re.findall('var my_Coords=\[\[(.*?)]]', response.text)[0]
    JSON = f'[[{JSON}]]'
    JSON = json.loads(JSON)
    good_data = []
    for shop in JSON:
        item = {}
        item['y'] = shop[0]
        item['x'] = shop[1]
        item['name'] = shop[2]
        item['address'] = shop[3]
        good_data.append(item)
    return good_data


def pd_data():
    good_data=get_data()
    df = pd.DataFrame(good_data)
    df['brand_name']='OBA Market'
    df['holding_name']='Veysəloğlu'
    return df

