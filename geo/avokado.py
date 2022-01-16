import requests
import re
import pandas as pd


def get_data():
    response = requests.get('https://xn--80aafj2axd.xn--p1ai/partners/', verify=False)
    data = re.findall('new ymaps.Placemark\(\[(.*?)], \{(.*?)},', response.text, re.S)

    good_data =[]
    for lonlat, row in data:
        item = dict()
        lat, lon = lonlat.split(',')
        item['x'] = float(lon)
        item['y'] = float(lat)
        item['work_time'] = re.search('hintContent: "(.*)",', row).group(1)
        item['work_time'] = item['work_time'] + re.search('balloonContent: "(.*)",', row).group(1)
        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Авокадо'
    df['holding_name'] = 'Сладкая жизнь'
    return df


from pandas import ExcelWriter

df = pd_data()
writer = ExcelWriter(f'test.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()
