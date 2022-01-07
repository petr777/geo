import re
import requests
import pandas as pd

def get_data():
    response = requests.get('https://svetofor-nsk.ru/shops.html')
    id_markers = re.findall('var latlng(.*?)=', response.text)
    good_data = []
    for _id in id_markers:
        item = dict()
        item[_id] = _id
        latlng = re.findall(
            f'var latlng{_id}= \[(.*?)];', response.text)[0]
        lat, lon = latlng.split(',')
        item = {
            'y': float(lon.strip()),
            'x': float(lat.strip()),
        }
        address = re.findall(
            f'marker{_id}.properties.set\("zhymTitle", "(.*?)"\);',
            response.text
        )
        if address:
            item['address'] = address[0].strip()

        good_data.append(item)
    return good_data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Светофор'
    df['holding_name'] = 'Светофор Групп'
    return df
