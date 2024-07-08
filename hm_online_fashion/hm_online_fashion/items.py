# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HmOnlineFashionItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field(seriliazer=str)
    description = scrapy.Field(seriliazer=str)
    fit = scrapy.Field(seriliazer=str)
    product_details = scrapy.Field()
    price = scrapy.Field(seriliazer=str)
    sizes = scrapy.Field()
    gender = scrapy.Field(seriliazer=str)
    color = scrapy.Field()
    image_link = scrapy.Field()
    category = scrapy.Field(seriliazer=str)
    other_img_colors_products = scrapy.Field()
