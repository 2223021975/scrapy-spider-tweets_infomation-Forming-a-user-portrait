# -*- coding: utf-8 -*-

#调用命令行，进行爬取命令
from scrapy import cmdline

cmdline.execute("scrapy crawl weibo".split())
