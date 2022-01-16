import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import re
import requests
from scrapy import Selector
from html_text import extract_text


def get_data():
    response = requests.get('http://www.tc-kupetz.ru/index/ru/shop/')
    page = Selector(text=response.text)
    good_data = []
    for shop in page.xpath('//div[@id="item"]'):
        item = dict()
        address = shop.xpath('./div[@class="title"]/strong/text()')
        if address:
            item['address'] = address.extract_first()
        else:
            continue
        rows = extract_text(shop.xpath('./div[@style="DISPLAY: none"]').get())
        rows = rows.split('\n')
        for row in rows:
            if 'Часы работы:' in row:
                item['work_time'] = re.sub('Часы работы: ', '', row)
        good_data.append(item)
    return good_data



async def main():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    new_good_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
        )
        page = await browser.new_page()
        await page.goto("https://yandex.ru/maps")

        for item in df.to_dict('records'):
            full_address = f"Екатеренбург {item.get('address')}"
            await page.fill('//input[@type="search"]', full_address)
            await page.keyboard.down("Enter")
            await asyncio.sleep(0.5)
            content = await page.content()
            html = Selector(text=content)
            coord = html.xpath(
                '//div[@class="toponym-card-title-view__coords-badge"]/text()'
            ).extract_first()
            if not coord:
                full_address = ''.join(full_address.split(',')[:-1])
                await page.fill('//input[@type="search"]', full_address)
                await page.keyboard.down("Enter")
                await asyncio.sleep(0.5)
                content = await page.content()
                html = Selector(text=content)
                coord = html.xpath(
                    '//div[@class="toponym-card-title-view__coords-badge"]/text()'
                ).extract_first()

            if coord:
                x, y = re.findall("\d+\.\d+", coord)
                item['x'] = float(y)
                item['y'] = float(x)
            new_good_data.append(item)
            print(len(new_good_data), item)

        await browser.close()


    from pandas import ExcelWriter

    df = pd.DataFrame(new_good_data)
    df['brand_name'] = 'Купец'
    df['holding_name'] = 'Купец̆'
    writer = ExcelWriter(f'Купец.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()

    return 'ok'

asyncio.run(main())