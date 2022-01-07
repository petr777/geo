import requests
import re
import pandas as pd
import json
import html_text


def get_data():
    params = (
        ('mid', '1tHYnXU2-QLxX6ngBdtOTer7fteYMDgaL'),
    )
    response = requests.get(
        'https://www.google.com/maps/d/viewer',
        params = params
    )

    data = re.findall('var _pageData = "\[\[(.*)]]";', response.text)[0]
    data = f'[[{data}]]'
    data = data.replace('\\', '')
    data = json.loads(data)
    data = data[1][6][0][12][0][13][0]

    good_data = []
    for row in data:
        item = {}
        item['name'] = row[5][0][1][0]
        coords = row[1][0][0]
        item['y'], item['x'] = float(coords[0]), float(coords[1])
        fragment = row[5][1][1][0].split('www.bazarstore.azn')
        item['address'] = html_text.extract_text(fragment[0])
        item['phone'] = html_text.extract_text(fragment[1]).replace('n*1900n', '')
        good_data.append(item)

    return good_data


def pd_data():
    good_data=get_data()
    df = pd.DataFrame(good_data)
    df['brand_name']='Bazarstore'
    df['holding_name']='Bazarstore'
    return df