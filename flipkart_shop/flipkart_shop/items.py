# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    img_url = scrapy.Field()
    size = scrapy.Field()
    size_chart = scrapy.Field()
    is_size = scrapy.Field()
    is_size_chart = scrapy.Field()
    subcategory = scrapy.Field()
    category = scrapy.Field()
