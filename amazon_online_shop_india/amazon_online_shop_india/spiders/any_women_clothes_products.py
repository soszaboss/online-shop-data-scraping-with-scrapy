from typing import Iterable
import scrapy
from amazon_online_shop_india.items import AmazonOnlineShopIndiaItem
from amazon_online_shop_india.functions import get_proxy_url
class AnyWomenClothesProductsSpider(scrapy.Spider):
    name = "any_women_clothes_products"
    allowed_domains = ["www.amazon.in", "proxy.scrapeops.io"]
    start_urls = ["https://www.amazon.in/s?k=women+clothes"]

    def start_requests(self):
        yield scrapy.Request(get_proxy_url(self.start_urls[0]), callback=self.parse)

    def parse(self, response):

        relative_links = response.css('h2>a::attr(href)').getall()

        for i in range(len(relative_links)):
            relative_links[i] = f'https://www.amazon.in{relative_links[i]}'

        # print(relative_links)
        requests = [scrapy.Request(get_proxy_url(link), callback=self.products_items) for link in relative_links]

        # Itérez sur les objets Request
        for request in requests:
            yield request
        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
        if next_page is not None:
            next_page = f'https://www.amazon.in{next_page}'
            yield scrapy.Request(get_proxy_url(next_page), callback=self.parse)
    
    def products_items(self, response):
        print(123)
        items = AmazonOnlineShopIndiaItem()
        items['sizes'] = response.css('.dropdownAvailable::text').getall()
        items['product_titles'] = response.css('#productTitle::text').get()
        items['prices'] = response.css('.a-price-whole::text').get()
        items['product_details'] = response.css('div.a-fixed-left-grid-col span .a-color-base::text').getall()
        items['About_this_item'] = response.css('span.a-list-item.a-size-base.a-color-base::text').getall()
        items['descriptions'] = response.css('p.description').get()
        items['img_url'] = response.css('img.a-dynamic-image.a-stretch-horizontal::attr(src)').get()

        yield items

