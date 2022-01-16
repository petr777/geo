import scrapy
from scrapy.crawler import CrawlerProcess
import re
import pandas as pd
from html_text import extract_text

RESULT_DATA_SPIDER = []

class MonetkaSpider(scrapy.Spider):
    name = 'monetka'
    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 YaBrowser/19.12.0.769 Yowser/2.5 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'LOGSTATS_INTERVAL': 5.0,
    }


    def start_requests(self):
        yield scrapy.FormRequest(
            url='https://monetka.ru/city/list',
            headers={
                'x-requested-with': 'XMLHttpRequest',
            },
            formdata={
                'id': 'all',
                'active_city': '73'
            },
            callback=self.parse
        )

    def parse(self, response):
        for url_city in response.xpath('//a/@href').getall():
            yield response.follow(url_city, self.parse_city)

    def parse_city(self, response):
        item = self.parese_shop(response)

        if item != {}:
            RESULT_DATA_SPIDER.append(item)
            yield item

        for shop_url in response.xpath('//div[@class="fit"]/ul/li/a/@href'):
            yield response.follow(shop_url, self.parse_city)

    def parese_shop(self, response):
        item = {}
        coord = response.xpath('//html').re(
            'var office = new YMaps.GeoPoint\((.*?)\)'
        )
        if coord:
            y, x = re.findall("\d+\.\d+", coord[0])
            item['y'], item['x'] = float(y), float(x)
        for row in response.xpath('//div[@class="article"]/address'):
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


def pd_data():
    process = CrawlerProcess()
    process.crawl(MonetkaSpider)
    process.start()
    df = pd.DataFrame(RESULT_DATA_SPIDER)
    df['brand_name'] = 'Монетка'
    df['holding_name'] = 'ФОКУС-РИТЕЙЛ'
    return df
