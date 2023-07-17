# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

    
class ProductItem(scrapy.Item): 
    # define the fields for your item
    name = scrapy.Field()
    price = scrapy.Field()
    sku = scrapy.Field()
    url = scrapy.Field()
    reviews_grade = scrapy.Field()
    review_images = scrapy.Field()