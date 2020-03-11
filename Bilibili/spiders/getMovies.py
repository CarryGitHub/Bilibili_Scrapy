# -*- coding: utf-8 -*-
import scrapy
import time
import json
from Bilibili.items import MovieItem

class GetmoviesSpider(scrapy.Spider):
    name = 'getMovies'
    allowed_domains = ['bilibili.com']
    # start_urls = ['http://bilibili.com/']
    def __init__(self):
        self.pages=104

    def start_requests(self):
        start_urls=['https://api.bilibili.com/pgc/season/index/result?area=-1&style_id=-1&release_date=-1&season_status=-1&order=2&st=2&sort=0&page={pn}&season_type=2&pagesize=20&type=1'.format(pn=i) for i in range(1,self.pages+1)]
        for start_url in start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_movie
            )
            time.sleep(2)


    def parse_movie(self, response):
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
            yield scrapy.Request(
                url=item["link"],
                callback=self.get_cid,
                meta=item
            )

    def get_cid(self,response):
        item=response.meta
        cid=response.css('script')[5].re_first('\"cid\":(\d+),')
        item["cid"]=cid
        yield item