# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuaNongItem(scrapy.Item):
    comment = scrapy.Field()
    pic = scrapy.Field()
    play = scrapy.Field()
    title = scrapy.Field()
    aid = scrapy.Field()
    length = scrapy.Field()
    created = scrapy.Field()


class MovieItem(scrapy.Item):
    badge=scrapy.Field()
    pic=scrapy.Field()
    index_show=scrapy.Field()
    link=scrapy.Field()
    media_id=scrapy.Field()
    order=scrapy.Field()
    title=scrapy.Field()
    cid=scrapy.Field()


class DocumentaryItem(scrapy.Field):
    badge = scrapy.Field()
    pic = scrapy.Field()
    index_show = scrapy.Field()
    link = scrapy.Field()
    media_id = scrapy.Field()
    order = scrapy.Field()
    title = scrapy.Field()