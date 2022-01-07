import requests
import pandas as pd
import json


def get_data():
    response = requests.get('https://www.bravosupermarket.az/v1/api/stores', verify=False)
    JSON = json.loads(response.text)
    good_data = []
    for shop in JSON['data']:
        item = {}
        item['name'] = shop.pop('name')
        item['type'] = shop.pop('format')
        item['address'] = shop.pop('address')
        item['phone'] = shop.pop('phone')
        item['work_time'] = shop.pop('work_times')

        item['y'] = shop.pop('longitude')
        item['x'] = shop.pop('latitude')
        if item["y"] == "49°57'33.6" and item["x"] == "40°21'54.6":
            item['y'] = 49.959333
            item['x'] = 40.365167

        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'BRAVO'
    df['holding_name'] = 'BRAVO'
    return df