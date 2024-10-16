# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .functions import list_product_details_into_dict
import pymongo


class AmazonOnlineShopIndiaPipeline:
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("product_details"):
            adapter['product_details'] = list_product_details_into_dict(adapter['product_details'])
        if adapter.get("About_this_item"):
            adapter['About_this_item'] = ", ".join(adapter['About_this_item'])
        if adapter.get("descriptions"):
            adapter['descriptions'] = adapter['descriptions'].strip()
        if adapter.get("sizes"):
            adapter['sizes'] = ", ".join(adapter['sizes'])
        if adapter.get("product_titles"):
            adapter['product_titles'] = adapter['product_titles'].strip()
        if adapter.get('other_img_colors_products'):
            adapter['other_img_colors_products'] = [adapter['other_img_colors_products']]
        return item

class MongoPipeline:
    collection_name = 'amazon_online_shop_india'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item