import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SheinProductsURLSpider(CrawlSpider):
    name = 'get_products_urls'
    start_urls = ['https://us.shein.com/']
    allowed_domains = ["br.shein.com", "us.shein.com"]
    
    
    
    rules = [
        Rule(LinkExtractor(allow='us.shein.com'), callback='parse_url' , follow=True)
    ]
 

    def parse_url(self, response):
        # is_product_page = response.css('.product-intro__head-sku')
        # print('is product page' , is_product_page)
        yield{
            'url': response.url
        }
   