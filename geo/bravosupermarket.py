import requests
import pandas as pd
import json
import html_text

def get_data():
    response = requests.get('https://www.bravosupermarket.az/v1/api/stores', verify=False)
    JSON = json.loads(response.text)
    good_data = []
    for shop in JSON['data']:
        item = {}
        item['name'] = html_text.extract_text(shop.pop('name'))
        item['type'] = html_text.extract_text(shop.pop('format'))
        item['address'] = html_text.extract_text(shop.pop('address'))
        item['phone'] = html_text.extract_text(shop.pop('phone'))
        item['work_time'] = html_text.extract_text(shop.pop('work_times'))

        item['x'] = shop.pop('longitude')
        item['y'] = shop.pop('latitude')

        if item["y"] == "40°21'54.6" and item["x"] == "49°57'33.6":
            item['x'] = 49.959333
            item['y'] = 40.365167

        item['x'] = float(item.pop('x'))
        item['y'] = float(item.pop('y'))

        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'BRAVO'
    df['holding_name'] = 'BRAVO'
    return df


