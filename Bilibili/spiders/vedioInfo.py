# -*- coding: utf-8 -*-
import scrapy
import json
from Bilibili.items import HuaNongItem
import time

class BilibiliSpider(scrapy.Spider):
    name = 'vedioInfo'
    allowed_domains = ['bilibili.com']

    def start_requests(self):
        Mid=927587     # up主mid
        Pages=32
        start_urls=['https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn={pn}&keyword=&order=pubdate&jsonp=jsonp'.format(mid=Mid,pn=i) for i in range(1,Pages+1)]
        for url in start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
            time.sleep(2)



    def parse(self, response):
        data=json.loads(response.text)
        items=data["data"]["list"]["vlist"]
        for item in items:
            info=HuaNongItem()
            info["comment"]=item["comment"]
            info["pic"]=item["pic"]
            info["play"]=item["play"]
            info["title"]=item["title"]
            info["aid"]=item["aid"]
            info["length"]=item["length"]
            info["created"]=item["created"]
            yield info