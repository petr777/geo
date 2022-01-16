import requests
import re
import pandas as pd
from scrapy import Selector


def merge_lists(all_lng, all_lat, all_address):
    i = 0
    data = []
    while i != len(all_lng):
        item = {
            'y': float(all_lat[i].strip()),
            'x': float(all_lng[i].strip()),
            'address': all_address[i]
        }
        i += 1
        data.append(item)
    return data


def get_data():
    response = requests.get('https://rukavychka.ua/stores/')
    page = Selector(text=response.text)
    scripts = page.xpath('//script')
    for script in scripts:
        if 'var locations =' in script.get():
            row = script.get()
            all_lat = re.findall("'lat' : (.*?),", row)
            all_lng = re.findall("'lng' : (.*?),", row)
            all_address = re.findall("'address' : \"(.*?)\",", row)
            data = merge_lists(all_lng, all_lat, all_address)
            return data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Рукавичку'
    df['holding_name'] = 'Рукавичку'
    return df
