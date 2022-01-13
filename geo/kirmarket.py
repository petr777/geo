import requests
from scrapy import Selector
import re
import ast
import pandas as pd


def get_shop_in_city(id_city, name_city):
    response = requests.get(f'https://kirmarket.ru/about/shops/?city={id_city}')
    page = Selector(text=response.text)
    shops = page.xpath('//div[@class="adress-list"]//a')
    data = []
    for shop in shops:
        item = {}
        latlon = re.findall('myMap.setCenter\((.*?)\)', shop.xpath('./@onclick').get())[0]
        latlon = ast.literal_eval(latlon)
        lat, lon = latlon
        item['x'] = float(lon)
        item['y'] = float(lat)
        item['address'] = shop.xpath('.//span[@class="street"]/text()').extract_first()
        item['city'] = name_city
        item['phone'] = shop.xpath('.//span[@class="phone"]/text()').extract_first()
        item['work-schedule'] = shop.xpath('.//span[@class="work-schedule"]/text()').extract_first()
        data.append(item)
    return data

def get_data():
    response = requests.get('https://kirmarket.ru/about/shops/')
    page = Selector(text=response.text)
    good_data = []
    for city in page.xpath('//select[@id="map-change-city"]//option'):
        id_city = city.xpath('@value').extract_first()
        id_name = city.xpath('text()').extract_first()
        data = get_shop_in_city(id_city, id_name)
        good_data.extend(data)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Кировский'
    df['holding_name'] = 'Кировский'
    return df

