# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonOnlineShopIndiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sizes = scrapy.Field()
    product_titles = scrapy.Field(serializer=str)
    prices = scrapy.Field(serializer=float)
    product_details = scrapy.Field()
    descriptions = scrapy.Field()
    About_this_item = scrapy.Field()
    img_url = scrapy.Field(serializer=str)
