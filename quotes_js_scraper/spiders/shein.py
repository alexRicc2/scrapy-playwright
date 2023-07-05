import scrapy
from scrapy_playwright.page import PageMethod

class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ["br.shein.com"]
    
    def start_requests(self):
        url = 'https://br.shein.com'
        yield scrapy.Request(url, callback=self.parse ,meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)')
            ],
            errback = self.errback
        ))    

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()
        
        for link in response.css('a::attr(href)'):
            yield scrapy.Request(response.urljoin(link.get()), callback=self.parse_link)

    def parse_link(self, response):
        # Process the individual link here
        yield {
            'url': response.url,
            'title': response.css('title::text').get()
        }
    
    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await  page.close()