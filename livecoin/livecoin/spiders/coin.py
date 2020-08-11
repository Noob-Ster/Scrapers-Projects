# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['https://www.livecoin.net/en/']
    

    def __init__(self):
        chrome_option = Options()
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--headless')
        # chrome_option.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_option)
        driver.set_window_size(1311,18365)
        driver.get('https://www.livecoin.net/en')
        time.sleep(10)
        # Accept the terms & conditions
        accept_btn = driver.find_element_by_xpath('//button[text()="Accept"]').click()
        # click on the ETH tab
        eth_curr = driver.find_elements_by_class_name('filterPanelItem___2z5Gb ')[3].click()
        # wait for the tab to load
        time.sleep(5)
        try:
            while True:
                elemnt = driver.find_element_by_xpath('//button[text()="Show more"]')
                if elemnt:
                    elemnt.click()
                    time.sleep(2)
                else:
                    break
        except NoSuchElementException:
            pass
        finally:
            self.html = driver.page_source
            driver.close()


    def parse(self, response):
        resp = Selector(text=self.html)
        rows = resp.xpath('//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS ")]')
        for row in rows:
            pair = row.xpath('.//div[1]//text()').get()
            volumne = row.xpath('.//div[2]//text()').get()
            yield {
                'pair' : pair,
                'Volumne(24h)' : volumne
            }
