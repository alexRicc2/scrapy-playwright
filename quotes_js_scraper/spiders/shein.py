import scrapy
from scrapy_playwright.page import PageMethod

class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ["br.shein.com"]
    
    def start_requests(self):
        url = 'https://br.shein.com/SHEIN-MOD-Solid-PU-Leather-Tube-Top-p-12877530-cat-2223.html'
        yield scrapy.Request(url, callback=self.parse ,meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                PageMethod('wait_for_selector', "div.common-reviews__list")
            ],
            errback = self.errback
        ))    

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()

        reviews = response.css('div.common-reviews__list')
        for review in reviews.css('div.j-expose__common-reviews__list-item'):
            for image in review.css('img.j-review-img::attr(data-src)'):        
                yield {
                    'image': image.get()
                }
    
       
        # Click the "next" button
        await page.click('span.sui-pagination__next')
        # Wait for the new reviews to load
        await page.wait_for_selector("div.common-reviews__list")
        # Continue parsing the next page
        await self.parse(response)
    
    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await  page.close()