# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector


class ListingsSpider(scrapy.Spider):
    name = 'listings'
    allowed_domains = ['www.centris.ca/en']
    payload = {
        "startPosition": 0
    }

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(2))
            return splash:html()
        end
    '''

    def start_requests(self):
        payload = {
            "uc": 0,
            "uck": "eb460a16-91b6-478a-b753-dccc8223cd6c"
        }
        yield scrapy.Request(
            url='https://www.centris.ca/UserContext/UnLock',
            callback=self.unlock,
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            },
            body=json.dumps(payload)
        )

    def unlock(self, response):
        payload = {
            "query": {
                "UseGeographyShapes": 0,
                "Filters": [
                    {
                        "MatchType": "CityDistrictAll",
                        "Text": "Montréal (All boroughs)",
                        "Id": 5
                    }
                ],
                "FieldsValues": [
                    {
                        "fieldId": "CityDistrictAll",
                        "value": 5,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "Category",
                        "value": "Residential",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SellingType",
                        "value": "Rent",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "LandArea",
                        "value": "SquareFeet",
                        "fieldConditionId": "IsLandArea",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 0,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 1500,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    }
                ]
            },
            "isHomePage": True
        }
        yield scrapy.Request(
            url='https://www.centris.ca/property/UpdateQuery',
            callback=self.update_query,
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            },
            body=json.dumps(payload),
            dont_filter=True
        )

    def update_query(self, response):
        yield scrapy.Request(
            url='https://www.centris.ca/Property/GetInscriptions',
            callback=self.parse,
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            },
            body=json.dumps(self.payload),
            dont_filter=True

        )

    def parse(self, response):
        resp_dic = json.loads(response.body)
        html = resp_dic.get('d').get('Result').get('html')
        resp_sel = Selector(text=html)
        listings = resp_sel.xpath("//div[@class='description']")
        for listing in listings:
            city = listing.xpath(
                ".//span[@class='address']/div[contains(text(),'(')]/text()").get()
            address = listing.xpath(
                ".//span[@class='address']/div[1]/text()").get()
            beds = listing.xpath(
                './/div[contains(@class,"features")]/div[1]/text()').get()
            baths = listing.xpath(
                './/div[contains(@class,"features")]/div[2]/text()').get()
            price = listing.xpath(
                './/span[@itemprop="price"]/@content').get()
            url = listing.xpath('.//a/@href').get()

            yield {
                'city': city,
                'address': address,
                'features': f'{beds} beds,{baths} baths',
                'price': f'${price}/month',
                'url': url
            }

        count = resp_dic.get('d').get('Result').get('count')
        increment = resp_dic.get('d').get('Result').get('inscNumberPerPage')

        if self.payload['startPosition'] <= count:
            self.payload['startPosition'] += increment
            yield scrapy.Request(
                url='https://www.centris.ca/Property/GetInscriptions',
                callback=self.parse,
                method='POST',
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
                },
                body=json.dumps(self.payload),
                dont_filter=True
            )
