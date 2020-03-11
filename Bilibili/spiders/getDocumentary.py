# -*- coding: utf-8 -*-
import scrapy
import time
import json
from Bilibili.items import MovieItem

class GetDocumentarySpider(scrapy.Spider):
    name = 'getDocumentary'
    allowed_domains = ['bilibili.com']
    # start_urls = ['http://bilibili.com/']

    def __init__(self):
        self.pages=133

    def start_requests(self):
        start_urls=['https://api.bilibili.com/pgc/season/index/result?area=-1&style_id=-1&release_date=-1&season_status=-1&order=2&st=5&sort=0&page={pn}&season_type=5&pagesize=20&type=1'.format(pn=i) for i in range(1,self.pages+1)]
        for start_url in start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_documentary
            )
            time.sleep(2)


    def parse_documentary(self, response):
        datas=json.loads(response.text)
        for data in datas["data"]["list"]:
            item=MovieItem()
            item["badge"]=data["badge"] if len(data["badge"])>0 else "一般用户"
            item["pic"]=data["cover"]
            item["index_show"]=data["index_show"]
            item["media_id"]=data["media_id"]
            item["order"]=data["order"]
            item["title"]=data["title"]
            item["link"]=data["link"]
            yield item
