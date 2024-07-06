# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

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
