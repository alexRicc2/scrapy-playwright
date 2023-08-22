import scrapy
from scrapy_playwright.page import PageMethod
from shein_js_scraper.items import ProductItem
class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ["br.shein.com", "us.shein.com"]
    start_url = ['https://us.shein.com/SHEIN-SXY-Striped-and-Letter-Graphic-Tube-Top-Skirt-p-11592041-cat-1780.html', 'https://us.shein.com/SHEIN-Coolane-Newspaper-Print-Bodycon-Dress-p-12241730-cat-1727.html' ]
    def start_requests(self):
        for url in self.start_url:
            # scrapeops_url = 'https://proxy.scrapeops.io/v1/?api_key=ecca5765-d3b6-4515-bb94-f1b77da1afd1&url=' + url             
            yield scrapy.Request(url, callback=self.parse, meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    # PageMethod('wait_for_selector', 'i.iconfont.icon-close.she-close'),
                    # PageMethod('click', 'i.iconfont.icon-close.she-close'),
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod('wait_for_selector', "div.common-reviews__list"),
                    PageMethod('evaluate', 'document.querySelector("span.j-expose__review-image-tab-target").click()'),
                    PageMethod('wait_for_timeout', 5000),
                ],
                errback=self.errback
            ))

    async def parse(self, response):
        page = response.meta['playwright_page']
            
        print('***** crawling the page: ', response.url)
        
        product_sku = await page.evaluate('document.querySelector(".product-intro__head-sku")')
        if product_sku:
            
            # await page.wait_for_selector('i.icon-close.she-close')
            # await page.click('i.icon-close.she-close')
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            await page.wait_for_selector("div.common-reviews__list")
            await page.evaluate('document.querySelector("span.j-expose__review-image-tab-target").click()')
            await page.wait_for_timeout(5000)  
            product_info = await self.extract_product_info(page)
            product_images = await self.extract_product_images(page)
        
            # Yield product details along with all image URLs
            product_item = ProductItem()
            
            product_item['name'] = product_info['name']
            product_item['price'] = product_info['price']
            product_item['sku'] = product_info['sku']
            product_item['url'] = product_info['url']
            product_item['reviews_grade'] = product_info['reviews_grade']
            product_item['review_images'] = product_images
            
            yield product_item     
        
        await page.close()

    async def extract_product_images(self, page):
        last_image_src = None
        image_urls = []
        while True:  
            reviews = await page.query_selector('div.common-reviews__list')
            review_items = await reviews.query_selector_all('div.j-expose__common-reviews__list-item')
            for review_item in review_items:
                for image in await review_item.query_selector_all('img.j-review-img'):
                    image_src = await image.get_attribute('data-src')
                    last_image_src = image_src
                    if image_src and not image_src.startswith('https:'):
                        image_src = 'https:' + image_src
                    image_urls.append(image_src)
                    # Save the last image_src to check if it changes in the next page
                    
            disabled_next_reviews = await page.query_selector('span.sui-pagination__next.sui-pagination__btn-disabled')
            if disabled_next_reviews:
                break
            await page.evaluate('document.querySelector("span.sui-pagination__next").click()')
            await page.wait_for_function(f'() => !document.querySelector(\'img[data-src="{last_image_src}"]\')')
        return image_urls
        
    async def extract_product_info(self, page):
        product_name = await page.evaluate('document.querySelector(".product-intro__head-name").textContent')
        product_price = await page.evaluate('document.evaluate(\'//*[@id="goods-detail-v3"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/span\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent')
        product_sku = await page.evaluate('document.querySelector(".product-intro__head-sku").textContent')
        product_url = page.url
        review_grade_element = await page.evaluate_handle('document.evaluate(\'//*[@id="goods-detail-v3"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/span\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue')
        review_grade = await review_grade_element.get_attribute('aria-label')

        return {
            'name': product_name,
            'price': product_price,
            'sku': product_sku,
            'url': product_url,
            'reviews_grade': review_grade,
        }
    
    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
