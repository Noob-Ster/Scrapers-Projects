# -*- coding: utf-8 -*-
import scrapy
import requests

class BestsellerSpider(scrapy.Spider):
    name = 'bestseller'
    allowed_domains = ['www.glassesshop.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            })

    def parse(self, response):
        rows = response.xpath('//div[@class="row pt-lg-5"]/div')
        for row in rows: 
            picture = row.xpath('.//div[3]/a/img/@src').get()
            title = row.xpath('.//div[4]/div[2]//a/@title').get()
            price = row.xpath('.//div[4]//span/text()').get()
            yield { 
                'title' : title,
                'price' : price,
                'picture' : picture
            }
            if title != None:
                with open(f'/root/Desktop/pic/{title}','wb') as f:
                    resp = requests.get(url=picture)
                    f.write(resp.content)
                    f.close()
                    
        next_page = response.xpath("(//a[@rel='next'])[1]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                })



