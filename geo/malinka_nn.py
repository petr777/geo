import requests
import re
import pandas as pd
import json

def get_data():
    params = (
        ('mid', '1D-D35QH4iVzx37b5mNKaJer3U8qjpjhD'),
    )
    response = requests.get(
        'https://www.google.com/maps/d/embed',
        params=params
    )
    data = re.findall('var _pageData = "\[\[(.*)]]";', response.text)[0]
    data = f'[[{data}]]'
    data = data.replace('\\', '')
    data = json.loads(data)
    data = data[1][6][0][12][0][13][0]

    good_data = []
    for row in data:
        item = {}
        item['_id'] = row[5][3][0][1][0]
        coords = row[1][0][0]
        item['y'], item['x'] = float(coords[0]), float(coords[1])

        item['address'] = row[5][3][1][1][0]
        if row[5][3][-1][0] == 'Вермя работы':
            item['work_time'] = row[5][3][-1][1][0]
        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Малинка'
    df['holding_name'] = 'Сладкая жизнь'
    return df

