import requests
import pandas as pd


def get_data():
    data = requests.get(
        'https://evroopt.by/wp-content/themes/evroopt/klaster-shop-load.php'
    ).json()

    info = pd.DataFrame(data['info'])
    features = pd.DataFrame(data['features'])
    features = features.rename(columns={'id': 'ID'})
    info = info.rename(columns={'id_post': 'ID'})
    df = pd.merge(info, features, on="ID", how="right")

    good_data = []
    for shop in df.to_dict('records'):
        item = {}
        item['ID'] = shop['ID']
        item['type'] = shop['type_x']
        item['address'] = shop['city']
        item['phone'] = shop['phone']

        item['y'], item['x'] = shop['geometry']['coordinates']
        item['y'] = float(item.pop('y'))
        item['x'] = float(item.pop('x'))

        item['work_time'] = shop['time']
        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Евроопт'
    df['holding_name'] = 'Евроторг'
    return df


