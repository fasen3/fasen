# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# 爬取到的数据名称按照Scrapy的模板填写
# 目标：收集爬取到数据

import scrapy


class BlItem(scrapy.Item):
    rank_tab = scrapy.Field()
    rank_num = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    au_href = scrapy.Field()
    href = scrapy.Field()
    view = scrapy.Field()
    danmaku = scrapy.Field()
    reply = scrapy.Field()
    favorite = scrapy.Field()
    coin = scrapy.Field()
    share = scrapy.Field()
    like = scrapy.Field()
    tag_name = scrapy.Field()
