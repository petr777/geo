import re
import ast
import requests
import pandas as pd


def get_data():
    response = requests.get('https://www.sm-komandor.ru/stores/map.php?locationId=&storeType=1-2-3')
    data = re.findall('var arPlacemarks = \[(.*)];', response.text)
    data = f'[{data[0]}]'
    shops = ast.literal_eval(data)

    good_data = []
    for shop in shops:
        shop['name'] = shop.pop('TITLE')
        shop['y'] = float(shop.pop('GPS_N'))
        shop['x'] = float(shop.pop('GPS_S'))

        post_code, address = shop.get('ADDRESS').split(',', 1)
        shop['post_code'] = post_code
        shop['address'] = address
        shop['full_address'] = shop.pop('ADDRESS')

        if shop['UF_STORE_TYPE'] == '1':
            shop['brand_name'] = 'Командор'
        elif shop['UF_STORE_TYPE'] == '2':
            shop['brand_name'] = 'Аллея'
        elif shop['UF_STORE_TYPE'] == '3':
            shop['brand_name'] = 'Хороший'

        del shop['UF_STORE_TYPE']
        del shop['UF_STORE_NUMBER']
        good_data.append(shop)
    return good_data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['holding_name'] = 'Командор'
    return df

