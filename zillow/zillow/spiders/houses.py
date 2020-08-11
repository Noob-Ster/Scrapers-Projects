# -*- coding: utf-8 -*-
import scrapy
import json
from ..utils import URL, cookies_parser
from ..items import ZillowItem


class HousesSpider(scrapy.Spider):
    name = 'houses'
    allowed_domains = ['www.zillow.com']

    def start_requests(self):
        yield scrapy.Request(
            url=URL,
            callback=self.parse,
            method='GET',
            cookies=cookies_parser()
        )

    def parse_price(self, price):
        return price
        
    def parse_priceFromUnits(self, units):
        priceBeds = list()
        for unit in units:
            price = unit.get('price')
            bed = unit.get('beds')
            priceBeds.append((price,bed))
        return priceBeds

    def parse(self, response):
        item = ZillowItem()
        html = json.loads(response.body)
        hotels = html.get('searchResults').get('listResults')
        for hotel in hotels:
            item['address'] = hotel.get('address')
            item['imgSrc'] = hotel.get('imgSrc')
            item['detailUrl'] = hotel.get('detailUrl')
            item['statusType'] = hotel.get('statusType')
            item['statusText'] = hotel.get('statusText')
            item['addressStreet'] = hotel.get('addressStreet')
            item['addressState'] = hotel.get('addressState')
            item['buildingName'] = hotel.get('buildingName')
            if 'price' in hotel:
                item['price_Beds'] = self.parse_price(hotel.get('price'))
            elif 'units' in hotel:
                item['price_Beds'] = self.parse_priceFromUnits(hotel.get('units'))
                
                
            yield item
            
           
