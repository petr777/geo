import pandas as pd
import requests


def get_data():
    headers = {
        'Host': 'www.atbmarket.com',
        'user-agent': 'ATBMarket/6.0.18 (iPad; iOS 12.5.5; Scale/2.00)',
        'accept': '*/*',
        'accept-language': 'ru',
    }
    params = (
        ('datalang', 'ru'),
    )
    response = requests.get('https://www.atbmarket.com/api2/shop/list/', headers=headers, params=params).json()
    shops = response['shops']
    good_data = []
    for shop in shops:
        del shop['region_id']
        del shop['city_id']
        del shop['is247']
        shop['x'] = float(shop.pop('long'))
        shop['y'] = float(shop.pop('lat'))
        shop['work_time'] = shop.pop('schedule')
        good_data.append(shop)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'АТБ'
    df['holding_name'] = 'АТБ-Маркет'
    return df

