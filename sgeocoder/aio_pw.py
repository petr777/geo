import asyncio
from playwright.async_api import async_playwright
from collections import deque
import pandas as pd
from scrapy import Selector
import re


async def main():
    df = pd.read_excel('Доброцен.xlsx')
    good_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
        )
        page = await browser.new_page()
        await page.goto("https://yandex.ru/maps")

        for item in df.to_dict('records'):
            full_address = f"{item.get('country')} {item.get('address')}"
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
            good_data.append(item)
            print(len(good_data), item)

        await browser.close()


    from pandas import ExcelWriter

    df = pd.DataFrame(good_data)
    writer = ExcelWriter(f'_Доброцен.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()

    return 'ok'

asyncio.run(main())