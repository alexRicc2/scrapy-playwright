import scrapy
from scrapy_playwright.page import PageMethod

class ProxySpider(scrapy.Spider):
    name = "proxy"
    allowed_domains = ["tsh-new-website.vercel.app"]
    start_urls = ["https://tsh-new-website.vercel.app"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta=dict(
                playwright=True,
                playwright_include_page=True,
                # playwright_page_methods=[
                #     PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                # ],
                errback=self.errback
            ))

    async def parse(self, response):
        page = response.meta['playwright_page']
        h1_text = await page.evaluate('document.querySelector("h1").textContent')
        yield {'h1': h1_text}
        await page.close()

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
