# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def list_product_details_into_dict(product_details:list):
    return {product_details[i]: product_details[i + 1] for i in range(0, len(product_details), 2)}

class AmazonIndiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
