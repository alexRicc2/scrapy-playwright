# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QuotesJsScraperPipeline:
    def process_item(self, item, spider):
        return item

# class ProductsScraperPipeline:
#     def process_item(self, item, spider):

#         adapter = ItemAdapter(item)
        
#         field_names = adapter.field_names()
#         images = adapter.get('images')
#         for image in images:
#             image = image 
        
#         return item