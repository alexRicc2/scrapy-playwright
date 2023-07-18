import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SheinProductsURLSpider(CrawlSpider):
    name = 'get_products_urls'
    start_urls = ['https://us.shein.com/']
    allowed_domains = ["br.shein.com", "us.shein.com"]
    rules = (
        Rule(LinkExtractor(allow='us.shein.com'), callback='parse_url' , follow=True, process_request='set_playwright_true'),
    )
    def set_playwright_true(self, request, response):
        request.meta["playwright"] = True
        return request

    def start_requests(self):
        yield scrapy.Request(
            url='https://us.shein.com/',
            meta={"playwright": True}
        )
        return super().start_requests()
 

    def parse_url(self, response):
        yield{
            'url': response.url
        }
   