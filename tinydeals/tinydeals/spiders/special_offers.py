# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com']
    start_urls = ['https://www.tinydeal.com/specials.html']

    def parse(self, response):
        rows = response.xpath('//ul[@class="productlisting-ul"]/div/li')
        for row in rows:
            link = response.urljoin(row.xpath('.//a[2]/@href').get()) 
            title = row.xpath('.//a[2]/text()').get() 
            special_price = row.xpath('.//div[2]/span[1]/text()').get() 
            normal_price = row.xpath('.//div[2]/span[2]/text()').get()
            yield {
                'Title': title,
                'Special Price' : special_price,
                'Normal Price' : normal_price,
                'Link' : link
            } 
        next_page = response.xpath('//a[@class="nextPage"]/@href').get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
