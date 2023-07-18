import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SipSpider(CrawlSpider):
    name = 'sip'
    allowed_domain =  ['sipwhiskey.com']
    start_urls = ['http://sipwhiskey.com/']
    
    rules = (
        Rule(LinkExtractor(allow='collections', deny='products')),
        Rule(LinkExtractor(allow='producst'), callback='parse_item')
    )
    def parse_item(self, response):
        yield {
            'name': response.css('h1.title::text').get()
        }

    