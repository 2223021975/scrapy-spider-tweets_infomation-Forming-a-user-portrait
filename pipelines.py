# -*- coding: utf-8 -*-
import pymongo
from scrapy.exceptions import DropItem

from myweibo.items import *

class WeiboPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost',27017)
        db = client['weibo']
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]
        self.KeyTweets = db["KeyTweets"]
    def process_item(self, item, spider):
        if isinstance(item,InformationItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
                self.Information.update({'_id':item['_id']},dict(item),upsert=True)
        elif isinstance(item,TweetsItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
                self.Tweets.update({'_id':item['_id']},dict(item),upsert=True)
        elif isinstance(item,FansItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
                self.Fans.update({'_id':item['_id']},dict(item),upsert=True)
        elif isinstance(item,FollowsItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
                self.Follows.update({'_id':item['_id']},dict(item),upsert=True)
        elif isinstance(item,KeyTweetsItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
                self.KeyTweets.update({'_id':item['_id']},dict(item),upsert=True)
        return item