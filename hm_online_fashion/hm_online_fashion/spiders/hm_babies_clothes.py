from typing import Any
import scrapy
from scrapy_playwright.page import PageMethod
from hm_online_fashion.items import HmOnlineFashionItem

class HmSpider(scrapy.Spider):
    name = "hm_babies_clothes"
    allowed_domains = ["www2.hm.com"]
 
          
    def start_requests(self):
        url = "https://www2.hm.com/en_in/sale/baby.html?sort=stock&image-size=small&image=stillLife&offset=0&page-size=278"
        yield scrapy.Request(
            url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'a.link'),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)")
                ],
                errback=self.errback,
            )
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.wait_for_timeout(3000)


        while True:
            # Sélectionner le bouton "Load more products" et sortir de la boucle s'il n'est plus dans le DOM
            load_more_button = await page.locator("button.button.js-load-more").element_handle()
            if not load_more_button or not await load_more_button.is_visible():
                await page.wait_for_timeout(2000)
                break
            
            # Scroller vers le bas de la page
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

            # Cliquer sur le bouton "Load more products" après avoir scrollé en bas
            await load_more_button.click(force=True)
            
            # Attendre que les produits soient chargés
            await page.wait_for_timeout(2000)


            # Récupérer les nouveaux liens des produits
            new_links = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a.link')).map(a => a.href);
            }''')


            for link in new_links:
                yield scrapy.Request(
                                        link,   
                                        # headers=get_random_header(header_list),
                                        callback=self.parse_product,
                                        meta=dict(
                                            playwright=True,
                                            playwright_include_page=True, 
                                            playwright_page_methods=[
                                                # PageMethod('wait_for_timeout', 60000),
                                                PageMethod('wait_for_selector', 'div.inner'),
                                                PageMethod('wait_for_selector', 'li.list-item'),
                                                PageMethod('wait_for_selector', 'a.filter-option.miniature'),
                                                PageMethod('wait_for_selector', 'button#toggle-descriptionAccordion'),
                                                # PageMethod('click', 'button#toggle-descriptionAccordion')

                                            ],
                                            errback=self.errback,
                                        )
                                    )
        await page.close()

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        # await page.wait_for_timeout(40000)
        items = HmOnlineFashionItem()
        items['product_name'] = await page.locator("h1.ProductName-module--productTitle__3ryCJ").text_content()
        items['description'] = await page.locator("p.d1cd7b.b475fe.e2b79d").text_content()
        items['fit'] = await page.evaluate('''
                                                document.evaluate(
                                                    '//*[@id="section-descriptionAccordion"]/div/div/dl/div[9]/dd',
                                                    document,
                                                    null,
                                                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                                                    null
                                                ).singleNodeValue.textContent
                                            ''')

        items['price'] = await page.locator("span.edbe20.ac3d9e.c8e3aa.e29fbf").text_content()
        items['sizes'] = await page.evaluate("""
                                        () => {
                                                return Array.from(document.querySelectorAll('.SizeButtonGroup-module--buttonInput__2nAE1'))
                                                .map(size => size.id);
                                            }
                                        """
                                        )
        items['product_details'] = {
                                    'keys': await page.evaluate("""
                                        () => {
                                                return Array.from(document.querySelectorAll('dt.fa226d.c0e4fd'))
                                                .map(key => key.textContent);
                                            }
                                        """
                                        ),
                                    'values': await page.evaluate("""
                                        () => {
                                                return Array.from(document.querySelectorAll('dd.d1cd7b.a09145'))
                                                .map(value => value.textContent);
                                            }
                                        """
                                        ),
                                    
                                    }
        items['color'] = await page.evaluate("""
                                        () => {
                                                return Array.from(document.querySelectorAll('a.filter-option'))
                                                .map(color => color.getAttribute("title"));
                                            }
                                        """
                                        )
        other_img_colors_products = response.css('a.filter-option.miniature img::attr(src)').getall()
        items['image_link'] = response.css('div.product-detail-main-image-container img::attr(src)').get()
        try:
            items['other_img_colors_products'] = {key:value for key,value in zip(items['color'][1::], other_img_colors_products)}
        except:
            items['other_img_colors_products'] = None
        items['category'] = "Kids"
        await page.close()
        yield items
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()