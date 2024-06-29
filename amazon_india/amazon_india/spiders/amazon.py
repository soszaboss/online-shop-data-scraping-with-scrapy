from typing import Iterable
import scrapy
from urllib.parse import urlencode
import amazon_india.settings as settings

def get_proxy_url(url: str):
    return f'https://proxy.scrapeops.io/v1/?api_key={settings.SCRAPEOPS_API_KEY}&url={url}'
class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=women+clothes"]

    def start_requests(self):
        yield scrapy.Request(
            url = get_proxy_url(self.start_urls[0]),
            callback = self.parse
        )

    def parse(self, response):
        relative_links = response.css('h2>a::attr(href)').getall()
        for i in range(len(relative_links)):
            relative_links[i] = f'https://www.amazon.in{relative_links[i]}'

        requests = [scrapy.Request(url=get_proxy_url(link), callback=self.parse_product_item) for link in relative_links]

        # Itérez sur les objets Request
        for request in requests:
            yield request

        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
        if next_page is not None:
            next_page = f'https://www.amazon.in{next_page}'
            yield scrapy.Request(url = get_proxy_url(next_page), callback=self.parse)

    def parse_product_item(self, response):
        sizes = response.css('.dropdownAvailable').getall()
        product_titles = response.css('#productTitle::text').get()
        prices = response.css('.a-price-whole::text').get()
        product_details = response.css('div.a-fixed-left-grid-col span .a-color-base::text').getall()
        descriptions = response.css('span.a-list-item.a-size-base.a-color-base::text').getall()