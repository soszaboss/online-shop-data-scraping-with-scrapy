# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os

def transform_size_chart(size_chart):
    keys = size_chart['keys']
    values = size_chart['values']
    num_columns = len(keys)
    
    size_chart_dict = {key: [] for key in keys}
    
    for i in range(0, len(values), num_columns):
        for j in range(num_columns):
            size_chart_dict[keys[j]].append(values[i + j])
    
    return [size_chart_dict]
class FlipkartShopPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("size_chart"):
            adapter['size_chart'] = transform_size_chart(adapter['size_chart'])
        if adapter.get("product_name"):
            adapter['product_name'] = adapter['product_name'].strip()
        if adapter.get("description"):
            adapter['description'] = adapter['description'].strip()
        return item


class MongoPipeline:
    collection_name = 'flipkart'

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