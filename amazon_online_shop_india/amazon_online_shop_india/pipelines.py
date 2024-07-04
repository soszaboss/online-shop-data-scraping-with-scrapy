# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .functions import list_product_details_into_dict



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
        return item
