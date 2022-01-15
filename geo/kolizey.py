import requests
import re
import pandas as pd


def get_data():
    response = requests.get('http://kolizey-kolbasi-uga.ru/gde-kupit/')
    placemarks = re.findall('.add\(myPlacemar(.*?)\)', response.text)
    good_data = []
    for placemark in placemarks:
        data = re.findall(
            placemark + ' = new ymaps.Placemark\(\[(.*?)], \{(.*?)},', response.text, re.S
        )
        for lonlat, row in data:
            item = dict()
            lat, lon = lonlat.split(',')
            item['x'] = float(lon)
            item['y'] = float(lat)
            item['name'] = re.search("name: '(.*)',", row).group(1)
            item['address'] = re.search("address: '(.*)',", row).group(1)
            item['phone'] = re.search("phone: '(.*)',", row).group(1)
            item['work_time'] = re.search("operating_mode: '(.*)',", row).group(1)
            good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Колизей'
    df['holding_name'] = 'Колизей'
    return df
