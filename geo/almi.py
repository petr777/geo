import requests
import re
import pandas as pd


def get_data():
    response = requests.get('http://almi.by/shops/')
    lats = re.findall('var lat = (.*?);', response.text)
    lons = re.findall('var lon = (.*?);', response.text)
    names = re.findall("\['name'] = '(.*?)';", response.text)
    address = re.findall("\['address'] = '(.*?)';", response.text)

    i = 0
    data = []
    while i != len(lats):
        item = {
            'x': lats[i].strip(),
            'y': lons[i].strip(),
            'name': names[i],
            'address': address[i]
        }
        i += 1
        data.append(item)
    return data

def pd_data():
    good_data=get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] ='АЛМИ'
    df['holding_name']='FMCG'
    return df

