import scrapy


class AlibabaItemsSpider(scrapy.Spider):
    name = "alibaba_items"
    allowed_domains = ["www.alibaba.com"]
    start_urls = ["https://www.alibaba.com/"]

    def parse(self, response):
        pass
