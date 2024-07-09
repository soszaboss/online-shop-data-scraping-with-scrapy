# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

def list_product_details_into_dict(product_details: list):
    return [{key.strip():value.strip() for key, value in zip(product_details['keys'][:-6], product_details['values'][:-4])}]

class HmOnlineFashionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("product_details"):
            adapter['product_details'] = list_product_details_into_dict(adapter['product_details'])
        if adapter.get("descriptions"):
            adapter['descriptions'] = adapter['descriptions'].strip()
        if adapter.get("sizes"):
            adapter['sizes'] = ", ".join(adapter['sizes'])
        if adapter.get("product_name"):
            adapter['product_name'] = adapter['product_name'].strip()
        if adapter.get("fit"):
            adapter['fit'] = adapter['fit'].strip()
        if adapter.get("price"):
            adapter['price'] = adapter['price'].split(" ")[1]
        return item
