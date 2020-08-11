# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ..items import FirmzyItem
# from selenium import webdriver

class HotelsSpider(scrapy.Spider):
    name = 'hotels'
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.firmy.cz/?q=prodej+kol&page=1',
            wait_time=15,
            callback=self.parse,
            #headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
            )

    def parse(self, response):
        # driver = webdriver.Chrome()
        hotels = response.xpath("//div[@class='premiseListBoxes pl-search ']/div[@data-dot='premise']")
        for hotel in hotels:
            title = hotel.xpath('.//span[@class="title"]/text()').get()
            phone = hotel.xpath('.//span[@class="premiseListPhone"]/text()').get()
            website = hotel.xpath('.//div[@class="action actionUrl"]//span[@class="actionTitle-desktop"]/text()').get()
            address1 = hotel.xpath('.//span[@class="addressWrap"]/span[1]/text()').get()
            address2 = hotel.xpath('.//span[@class="addressWrap"]/span[2]/text()').get()

            yield {
                'title' : title,
                'phone' : phone,
                'website' : website,
                'address' : f'{address1}{address2}',
                'user-agent' : response.request.headers['User-Agent']
            }
            



            link = response.xpath('//a[@id="nextBtn"]/@href').get()

            next_page = response.urljoin(link)

            if next_page:
                yield SeleniumRequest(url=next_page,wait_time=15,callback=self.parse,headers={
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
                })

            

