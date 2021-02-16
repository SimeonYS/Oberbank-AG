import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import OberbankItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.oberbank.at/newsroom']

    def parse(self, response):
        links = response.xpath('//a[@class="dt-a-arrow"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(OberbankItem())
        item.default_output_processor = TakeFirst()

        date = re.findall(r"\d+\.\d+\.\d+", response.xpath('//div[@class="dt-pre-headline"]//text()').get().strip())
        title = response.xpath('//h1[@class="h2"]//text()').get()
        content = response.xpath('//div[@class="dt-text dt-content-module"]//text()').getall()
        content = ' '.join([text.strip() for text in content if text.strip()][2:])

        item.add_value('date', date)
        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()
