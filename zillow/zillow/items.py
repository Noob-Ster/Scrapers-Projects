# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowItem(scrapy.Item):
    address = scrapy.Field()
    imgSrc = scrapy.Field()
    detailUrl = scrapy.Field()
    statusType = scrapy.Field()
    statusText = scrapy.Field()
    price_Beds = scrapy.Field()
    addressStreet = scrapy.Field()
    addressState = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    buildingName = scrapy.Field()
