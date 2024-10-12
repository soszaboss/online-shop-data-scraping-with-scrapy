import scrapy
from scrapy_playwright.page import PageMethod
from flipkart_shop.items import Item

class FlipkartSpider(scrapy.Spider):
    name = "flipkart_sari"
    allowed_domains = ["www.flipkart.com"]

    def start_requests(self):
        
        url = 'https://www.flipkart.com/search?q=women+sari'
        yield scrapy.Request(
            url, 
            meta=dict(
                playwright=True,
                playwright_include_page=True, 
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'a.WKTcLC'),
                ],
                errback=self.errback,
            )
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        product_links = response.css('a.WKTcLC::attr(href)').getall()
        product_links = [f'https://www.flipkart.com{link}' for link in product_links]

        for link in product_links:
            yield scrapy.Request(
                link,   
                callback=self.parse_product,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True, 
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', 'span.mEh187'),
                        PageMethod('wait_for_selector', 'span.VU-ZEz'),
                        PageMethod('wait_for_selector', 'div.Nx9bqj.CxhGGd'),
                        PageMethod('wait_for_selector', 'img._0DkuPH'),
                    ],
                    errback=self.errback,
                )
            )

        next_pages = [f'https://www.flipkart.com/search?q=women+sari&page={i}' for i in range(2, 26)]
        for next_page in next_pages:
            yield scrapy.Request(
                next_page, 
                meta=dict(
                    playwright=True,
                    playwright_include_page=True, 
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', 'a.WKTcLC'),
                    ],
                    errback=self.errback,
                )
            )

    async def parse_product(self, response):
        items = Item()
        page = response.meta["playwright_page"]

        try:
            await page.locator("li.eVrPKK.dpZEpc").click(force=True)
            items['is_size_chart'] = True 
        except:
            items['is_size_chart'] = False 
            items['size_chart'] = None
        else:
            await page.wait_for_selector("div._8mqQwQ")
            await page.wait_for_selector("td.i2HOkF")
            keys_elements = await page.locator("td.i2HOkF").all_text_contents()
            await page.wait_for_selector("td.ljobKU")
            values_elements = await page.locator("td.ljobKU").all_text_contents()

            items['size_chart'] = {'keys': keys_elements, 'values': values_elements}
            print(f"Found {len(keys_elements)} keys elements and {len(values_elements)} values elements")

        finally:
            await page.close()

            items['product_name'] = response.css('span.mEh187::text').get()
            items['description'] = response.css('span.VU-ZEz::text').get()
            items['price'] = response.css('div.Nx9bqj.CxhGGd::text').get()
            items['img_url'] = response.css('img._0DkuPH::attr(src)').get()
            items['size'] = response.css('a.CDDksN.zmLe5G.dpZEpc::text').getall()
            items['is_size'] = bool(items['size'])
            items['subcategory'] = 'Sari'
            items['category'] = 'Women'
            yield items

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

"""next page

 # try:
        #     await page.wait_for_selector("a._9QVEpD:has-text('Next')")
        # except:
        #     next_page = None
        # else:
        #     next_page = await page.locator("a._9QVEpD:has-text('Next')").get_attribute('href')
        # finally:
        #     await page.close()
# print('next_page')
        # print(next_page)
        # print('next_page_url')
        
        # if next_page is not None:
        #     next_page_url = 'https://www.flipkart.com' + next_page
        #     yield scrapy.Request(next_page_url, meta=dict(
        #                                                     playwright = True,
        #                                                     playwright_include_page = True, 
        #                                                     playwright_page_methods =[
        #                                                                                 PageMethod('wait_for_selector', 'a.WKTcLC'),
        #                                                                             ],
        #                                                                     errback=self.errback,
        #                                                         ))
"""
