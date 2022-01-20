import requests
import re
import ast
import pandas as pd

def get_data():
    good_data = []
    response = requests.get('https://shop.mgnl.ru/contacts/stores/')
    data = re.search('var shops = \{"list":(.*?)};', response.text, re.S).group(1)
    shops = ast.literal_eval(data)
    for shop in shops:
        item = dict()
        x, y = shop.get('coord').split(',')
        item['y'], item['x'] = float(x), float(y)
        item['address'] = shop.get('addr')
        item['phone'] = ';'.join(shop.get('phone', []))
        item['metro'] = shop.get('metro')
        item['option'] = ';'.join(shop.get('option', []))
        good_data.append(item)
    return good_data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Магнолия'
    df['holding_name'] = 'Магнолия'
    return df
