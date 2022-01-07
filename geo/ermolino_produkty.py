import requests
import pandas as pd
import json
import html_text


def get_data():
    params = (
        ('ac', 'coords'),
        ('cat', '2'),
    )
    response = requests.get(
        "https://www.ermolino-produkty.ru/magaziny",
        params=params,
        verify=False
    )
    JSON = json.loads(response.text)
    JSON = JSON.get('points')
    good_data = []
    for point in JSON:
        item = {}
        item['_id'] = point.get('id')
        coords = point.get('coords')
        item['y'] = float(coords[0])
        item['x'] = float(coords[1])
        item['region'] = point.get('region')
        item['city'] = point.get('city')
        item['address'] = html_text.extract_text(
            point.get('address')
        ).replace('\n', ' ')
        item['work_time'] = html_text.extract_text(
            point.get('vremya_raboty')
        ).replace('Время работы:', '').replace("'", '')
        good_data.append(item)

    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Продукты Ермолино'
    df['holding_name'] = 'ТМ "ЕРМОЛИНО"'
    return df



