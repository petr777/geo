import requests
import re
from scrapy import Selector
from html_text import extract_text
import pandas as pd

def get_address(response):
    all_adress = []
    page = Selector(text=response.text)
    address_shops = page.xpath('//ul[@class="public-DraftStyleDefault-ul"]//li').getall()
    address_shops = [extract_text(address) for address in address_shops]
    for address in address_shops:
        address = re.sub("^\s+|\n|\r|\s+$", '', address)
        if address[-1] == ";" or address[-1] == ".":
            all_adress.append(address[:-1])
        else:
            all_adress.append(address)
    return all_adress


def get_data():
    domain = 'https://xn--90afe6acbn3c.xn--p1ai'
    response = requests.get('https://xn--90afe6acbn3c.xn--p1ai/adriesa_maghazinov_')
    page = Selector(text=response.text)
    good_data = []
    for country in page.xpath('//ul[@class="public-DraftStyleDefault-ul"]/li'):
        url = domain + country.xpath('.//a/@href').extract_first()
        country_name = country.xpath('.//text()').extract_first()
        response = requests.get(url)
        page = Selector(text=response.text)
        if page.xpath('//ul[@class="public-DraftStyleDefault-ul"]/li//a/@href'):
            for region in page.xpath('//ul[@class="public-DraftStyleDefault-ul"]/li'):
                url = domain + region.xpath('.//a/@href').extract_first()
                region_name = region.xpath('.//text()').extract_first()
                region_name = re.search('\((.*)\)', region_name)[1].strip()
                response = requests.get(url)
                for address in get_address(response):
                    item = dict()
                    item['country'] = country_name
                    item['federal district'] = region_name
                    item['address'] = address
                    good_data.append(item)
        else:
            for address in get_address(response):
                item = dict()
                item['country'] = country_name
                item['address'] = address
                good_data.append(item)
    return good_data

def pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] = 'Доброцен'
    df['holding_name'] = 'Доброцен'
    return df

