import requests
import re
import pandas as pd
from scrapy import Selector


def pars_data(html):
    data = {}
    page = Selector(text=html)

    fragments_work_time = page.xpath(
        '//span[@class="tips"]//span[text()[contains(.,"КРУГЛОСУТОЧНО") or contains(.,"00")]]/text()'
    )
    if fragments_work_time:
        work_time = fragments_work_time.extract_first()
        work_time = work_time.strip()
        data['work_time'] = work_time

    fragments_phones = page.xpath(
        '//span[@class="tips"]/span[@class="part"]//strong/text()'
    )
    if fragments_phones:
        phones = fragments_phones.extract_first()
        phones = phones.strip()
        data['phones'] = phones
    return data


def get_data():
    response = requests.get(
        'http://www.krasyar.ru/buyers/addresses/',
    )
    all_id = re.findall('points\[(.*?)] =', response.text)
    good_data = []
    for _id in all_id:
        item = {}
        latlon = re.findall(f'points\[{_id}] = new YMaps.GeoPoint\((.*?)\);', response.text)
        if latlon:
            lat, lon = latlon[0].split(',')
            item['x'] = float(lat)
            item['y'] = float(lon)

        item['address'] = re.findall(
            f'pmark\[{_id}].name = (.*?);', response.text
        )[0].replace("'", '')

        description = re.findall(f'pmark\[{_id}].description = \'(.*?)\';', response.text)

        if description and description[0] != '':
            item.update(pars_data(description[0]))

        good_data.append(item)
    return good_data


def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Красный Яр'
    df['holding_name'] = 'Красный Яр'
    return df


