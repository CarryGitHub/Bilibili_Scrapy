# -*- coding: utf-8 -*-
import scrapy
import pymongo
import time

class DanmuSpider(scrapy.Spider):
    name = 'danmu'
    allowed_domains = ['bilibili.com']
    # start_urls = ['https://www.bilibili.com/video/av88149130']
    start_url='https://www.bilibili.com/video/av'

    def start_requests(self):
        client=pymongo.MongoClient(host='localhost',port=27017)
        db=client.Bilibili
        collection = db.MuYuVedioInfo
        datas=collection.find({},{'aid':1,'_id':0}).sort('aid',pymongo.ASCENDING)
        for data in datas:
            url=self.start_url+str(data["aid"])
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
            time.sleep(2)
        client.close()

    def parse(self, response):
        link=response.css('script').re_first('\"cid\":(.*?),')
        link='http://comment.bilibili.com/{}.xml'.format(link)
        yield scrapy.Request(
            url=link,
            callback=self.parse_comments
        )

    def parse_comments(self,response):
        comments=response.css('d::text').extract()
        f=open('MuYudanmu.txt','a',encoding='utf-8')
        f.write('\n'+response.url)
        f.write('\n')
        f.write('\n'.join(comments))
        f.close()