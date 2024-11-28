#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-22 9:17
# @Author  : SHANNON
# @File    : start.py
# @Description :通常启动Scrapy都是在shell或者cmd命令中进行。为了方便启动或者进行debug测试，创建一个start.py用来控制启动

from scrapy import cmdline

cmdline.execute('scrapy crawl bi'.split())

# cmdline.execute("scrapy crawl field -o item.csv -t csv".split())