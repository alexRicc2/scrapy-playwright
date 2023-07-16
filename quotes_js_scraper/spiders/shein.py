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
                PageMethod('evaluate', 'document.querySelector("span.j-expose__review-image-tab-target").click()'),
                PageMethod('evaluate', 'document.querySelector("span.sui-pagination__next").click()'),
                PageMethod('wait_for_timeout', 10000),
                # PageMethod('wait_for_function', '() => document.querySelector("div.common-reviews__list").getAttribute("data-expose-id") !== "0-6231182960-1688956208551-w22112207014-23-3-66-recsrch_sort:A|recsrch_tag:A-1-reviews"'),
            ],
            errback=self.errback
        ))

    async def parse(self, response):
        page = response.meta['playwright_page']
        loopIndexPage = 0
        while True:  
            reviews = await page.query_selector_all('div.common-reviews__list')
            for review in reviews:
                image = await review.query_selector('img.j-review-img')
                image_src = await image.get_attribute('data-src')
                yield {
                    'image': image_src
                }
            print('loop: ', loopIndexPage)
            loopIndexPage += 1
            disabled_next_reviews = await page.query_selector('span.sui-pagination__next.sui-pagination__btn-disabled')
            if disabled_next_reviews:
                break

            await page.evaluate('document.querySelector("span.sui-pagination__next").click()')
            await page.wait_for_timeout(5000)

        await page.close()

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
