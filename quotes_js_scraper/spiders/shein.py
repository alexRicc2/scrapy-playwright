import scrapy
from scrapy_playwright.page import PageMethod
from time import sleep
class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ["br.shein.com"]

    def start_requests(self):
        url = 'https://br.shein.com/SHEIN-MOD-Solid-PU-Leather-Tube-Top-p-12877530-cat-2223.html'
        yield scrapy.Request(url, callback=self.parse, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'i.icon-close.she-close'),
                PageMethod('click', 'i.icon-close.she-close'),
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                PageMethod('wait_for_selector', "div.common-reviews__list"),
                PageMethod('evaluate', 'document.querySelector("span.sui-pagination__next").click()'),
                PageMethod('wait_for_timeout', 10000)
            ],
            errback=self.errback
        ))

    async def parse(self, response):
        page = response.meta['playwright_page']

        reviews = response.css('div.common-reviews__list')
        for review in reviews.css('div.j-expose__common-reviews__list-item'):
            for image in review.css('img.j-review-img::attr(data-src)'):
                yield {
                    'image': image.get()
                }

        reviews_with_image = response.css('span.j-expose__review-image-tab-target::text').get()
        print(' ******* reviews with image span text: ', reviews_with_image)

       
        next_reviews = await page.evaluate('document.querySelector("span.sui-pagination__next")')
        if next_reviews:
            await page.evaluate('document.querySelector("span.sui-pagination__next").click()')
            yield scrapy.Request(response.url, callback=self.parse, meta=response.meta)

        await page.close()

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
