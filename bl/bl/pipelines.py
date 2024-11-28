# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# 用scrapy原生的CsvItemExporter能够让我们从编写表头以及写writerow语句中解放出来，比传统写入csv的方法更简便。
# 目标：利用CsvItemExporter把数据写入csv文件
import csv

import pymysql
from itemadapter import ItemAdapter

from scrapy.exporters import CsvItemExporter


class BlPipeline(object):
    def __init__(self):
        # a为追加写入模式，这里要用二进制的方式打开
        self.fp = open('../bilibili.csv', 'wb')
        # include_headers_line默认为True
        # 能够帮我们自动写入表头，并且在追加写入数据的时候不会造成表头重复
        self.exportre = CsvItemExporter(
            self.fp,
            include_headers_line=True,
            encoding='utf-8'
        )

    def open_spider(self, spider):
        pass

    # 向csv文件中写入数据
    def process_item(self, item, spider):
        self.exportre.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()

    # 存储进数据库（注意：修改为自己数据库的信息）
    def dbHandle(self):
        conn = pymysql.connect(
            host='localhost',
            db='bilibili',
            user='root',
            password='123456',
            charset='utf-8',
        )
        return conn


class HellospiderPipline(object):
    # 同理修改为自己数据库的信息
    def dbHandle(self):
        conn = pymysql.connect(
            host='localhost',
            db='bilibili',
            user='root',
            password='123456',
            # charset='utf-8',
        )
        return conn

    def process_item(self, item, spider):
        dbObject = self.dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE bilibili")
        sql = "insert into " \
              "bilibili(分区名称,排名,视频ID,视频标题,作者,au_href,href,点赞,投币,评论,收藏,弹幕,分享,播放,tag_name) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (
            item['rank_tab'], item['rank_num'], item['id'], item['title'], item['author'], item['au_href'],
            item['href'], item['like'], item['coin'], item['reply'], item['favorite'], item['danmaku'], item['share'],
            item['view'], item['tag_name']))
            cursor.connection.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
        dbObject.rollback()
        return item
