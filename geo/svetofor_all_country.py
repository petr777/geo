import scrapy
from scrapy.crawler import CrawlerProcess
import re
import pandas as pd


svetofor_all_country_result = []

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 YaBrowser/19.12.0.769 Yowser/2.5 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'LOGSTATS_INTERVAL': 5.0,
    }

    start_urls = [
        'https://svetoformagazin.com/ru/',
        'https://svetoformagazin.com/by/',
        'https://svetoformagazin.com/kz/',
        'https://svetoformagazin.com/ua/'
    ]
    good_data = []

    def parse(self, response):
        url_shop = response.xpath('//table[@class="table table-bordered"]//tr/td/a/@href').getall()
        for url in url_shop:
            yield response.follow(url, self.parse_shop)

        for next_page in response.xpath("//ul[@class='pagination']//a[contains(text(),'»')]/@href"):
            yield response.follow(next_page, self.parse)

    def parse_shop(self, response):
        item = {}
        for li in response.xpath("//ul[@class='list-unstyled']//li"):
            if 'Населенный пункт:' in li.get():
                item['country'] = li.xpath('./ul/li/a/text()').get().replace(' »', '')

            if 'Почтовый адрес:' in li.get():
                item['address'] = li.xpath('./strong/text()').get()

            if 'Координаты:' in li.get():
                lonalt = li.xpath('./strong/text()').get()
                y, x = re.findall("\d+\.\d+", lonalt)
                item['y'], item['x'] = float(y), float(x)
            if 'Время работы:' in li.get():
                item['work_time'] = li.xpath('./strong/text()').get()

            if 'Телефон:' in li.get():
                item['phone'] = li.xpath('./strong/text()').get()

        svetofor_all_country_result.append(item)

def pd_data():
    process = CrawlerProcess()
    process.crawl(BlogSpider)
    process.start()
    df = pd.DataFrame(svetofor_all_country_result)
    df['brand_name'] = 'Светофор'
    df['holding_name'] = 'Светофор Групп'
    return df
