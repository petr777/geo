import requests
from scrapy import Selector
import re
from html_text import extract_text
import pandas as pd


def parese_shop(url):
    response = requests.get(url)
    if response.ok:
        page = Selector(text=response.text)
        item = {}
        coord = page.xpath('//html').re(
            'var office = new YMaps.GeoPoint\((.*?)\)'
        )
        if coord:
            y, x = re.findall("\d+\.\d+", coord[0])
            item['y'], item['x'] = float(y), float(x)
        for row in page.xpath('//div[@class="article"]/address'):
            if 'Почтовый адрес:' in row.get():
                item['addres'] = extract_text(
                    row.xpath('./p/text()').extract_first()
                )
            if 'Формат:' in row.get():
                item['type'] = extract_text(
                    row.xpath('./p/text()').extract_first()
                )
            if 'Режим работы:' in row.get():
                item['type'] = extract_text(
                    row.xpath('./p/text()').extract_first()
                )
        return item



def get_endpoint_shop():
    session = requests.session()
    data = {
        'id': 'all',
        'active_city': '1'
    }
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }

    response = session.post(
        'https://monetka.ru/city/list',
        headers=headers,
        data=data
    )
    page = Selector(text=response.text)

    # Все города кроме областных центров
    cities = page.xpath('//a/@href').getall()
    for url_city in cities:
        url_city = 'https://monetka.ru' + url_city
        response = session.get(url_city)
        page = Selector(text=response.text)
        shop_in_city = page.xpath('//div[@class="layer shop_list_layer"]//div[@class="fit"]//a/@href')
        if shop_in_city:
            shops = ('https://monetka.ru' + url for url in shop_in_city.getall())
            yield from shops
        else:
            yield url_city

    # Областные центры
    response = session.get('https://monetka.ru/shops_map')
    page = Selector(text=response.text)

    region = page.xpath('//div[@id="city_layer"]//li/a/@href').getall()
    for url in region:
        url = 'https://monetka.ru' + url
        session.get(url)
        region_slug = url.split('/')[-2]
        response = session.get(f'https://monetka.ru/{region_slug}/shops_map')
        page = Selector(text=response.text)
        shops = (
            'https://monetka.ru' + url
            for url in page.xpath('//div[@class="layer shop_list_layer"]//li/a/@href').getall()
        )
        yield from shops


def get_data():
    good_data = []
    uniq_url = set()
    for url in get_endpoint_shop():
        if url not in uniq_url:
            item = parese_shop(url)
            uniq_url.add(url)
            if item:
                good_data.append(item)
        print(len(good_data))
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df.drop_duplicates()
    df['brand_name'] = 'Монетка'
    df['holding_name'] = 'ФОКУС-РИТЕЙЛ'
    return df

