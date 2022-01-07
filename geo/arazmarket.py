import requests
import pandas as pd
from scrapy import Selector


def get_data():
    response = requests.get('https://www.arazmarket.az/ru/stores/')
    page = Selector(text = response.text)
    data = []
    for block in page.xpath('//div[@class="color-262626"]'):
        item = dict()
        item['type'] = block.xpath('.//div[@class="flex-fill"]/div/div/span/text()').get()
        item['address'] = block.xpath('.//span[contains(@class, "js-address")]/text()').get()
        item['work_time'] = block.xpath('.//div[@class="js-slide-body"]//span[2]/text()').get()
        item['phone'] = block.xpath('.//div[@class="js-slide-body"]//span[4]/text()').get()

        lat = block.xpath('.//div[@data-icon="map"]/@data-lat').get()
        if lat:
            item['y'] = float(lat)

        lon = block.xpath('.//div[@data-icon="map"]/@data-lng').get()
        if lon:
            item['x'] = float(lon)

        data.append(item)
    return data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Araz'
    df['holding_name'] = 'Veyseloglu'
    return df


