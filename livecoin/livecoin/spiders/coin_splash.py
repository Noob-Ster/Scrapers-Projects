import scrapy
from scrapy_splash import SplashRequest
class CoinSpiderSplash(scrapy.Spider):
    name = 'coin_splash'
    allowed_domains = ['www.livecoin.net/en']
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            splash:go(url)
            splash:wait(10)
            eth_curr = splash:select_all('.filterPanelItem___2z5Gb ')
            eth_curr[4]:mouse_click()
            splash:wait(5)
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.livecoin.net/en',callback=self.parse,endpoint='execute',args={
            'lua_source' : self.script
        })


    def parse(self, response):
        rows = response.xpath('//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS ")]')
        for row in rows:
            pair = row.xpath('.//div[1]//text()').get()
            volumne = row.xpath('.//div[2]//text()').get()
            yield {
                'pair' : pair,
                'Volumne(24h)' : volumne
            }