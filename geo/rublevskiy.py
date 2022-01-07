import requests
import pandas as pd


def get_data():
    data = requests.get('https://rublevskiy.ru/gde-kupit/addresses.php?limit=500').json()
    good_data = []
    for shop in data:
        item = {}
        item['id'] = shop.get('id')
        item['address'] = shop.get('address')
        item['store_time'] = shop.get('store_time')
        item['y'] = float(shop.get('lat'))
        item['x'] = float(shop.get('lng'))
        good_data.append(item)
    return good_data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Рублёвский'
    df['holding_name'] = 'Рублёвский'
    return df
