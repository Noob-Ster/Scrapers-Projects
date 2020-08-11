# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

class FirmzyPipeline:

    # def open_spider(self, spider):
        # self.mydb = sqlite3.connect('Firmzy')
        # self.cursor = self.mydb.cursor()
        # self.cursor.execute(''' 
        #     CREATE TABLE Hotel (
        #         title TEXT,
        #         phone TEXT,
        #         website TEXT,
        #         address TEXT
        #     )
        # ''')
        # self.mydb.commit()


    def process_item(self, item, spider):
        # self.cursor.execute('''
        # INSERT INTO Hotel (title,phone,website,address) VALUES (?,?,?,?)
        # ''',(
        #     item.get('title'),
        #     item.get('phone'),
        #     item.get('website'),
        #     item.get('address')
        # ))

        # self.mydb.commit()
        
        return item

    # def close_spider(self, spider):
        #self.mydb.close()