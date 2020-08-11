# -*- coding: utf-8 -*-
import scrapy


class CountryGdpSpider(scrapy.Spider):
    name = 'country_gdp'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath('//tbody/tr')
        for row in rows:
            country = row.xpath('.//td[1]/a/text()').get() 
            link = row.xpath('.//td[1]/a/@href').get() 
            gdp = row.xpath('.//td[2]/text()').get() 
            popul = row.xpath('.//td[3]/text()').get() 
            
            yield response.follow(link, callback=self.parse_country, meta={'country_name':country, 'gdp':gdp, 'popul':popul})
        
    def parse_country(self, response):
        country_name = response.request.meta['country_name']
        gdp = response.request.meta['gdp']
        population = response.request.meta['popul']

        year = response.xpath('(//tbody)[2]/tr/td[1]/text()').getall()
        popul = response.xpath('(//tbody)[2]/tr/td[2]/text()').getall()
        year_population = [x for x in zip(year,popul)]

        yield{
            'Country_name':country_name,
            'Gdp':gdp,
            'Population': population,
            'Year and Popuation' : year_population
        }