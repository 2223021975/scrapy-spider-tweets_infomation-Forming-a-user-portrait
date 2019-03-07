# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class InformationItem(scrapy.Item):
    _id = scrapy.Field()  # 用户ID
    NickName = scrapy.Field()  # 昵称
    Signature = scrapy.Field()  # 个性签名
    Num_Tweets = scrapy.Field()  # 微博数
    Num_Follows = scrapy.Field()  # 关注数
    Num_Fans = scrapy.Field()  # 粉丝数
    gender = scrapy.Field()# 性别

class TweetsItem(scrapy.Item):
    _id = scrapy.Field() #微博ID
    ID = scrapy.Field() #用户ID
    Content = scrapy.Field() #微博内容
    PubTime = scrapy.Field() #发表时间
    Like = scrapy.Field() #点赞数
    Comment = scrapy.Field() #评论数
    Transfer = scrapy.Field() #转载数

class FansItem(scrapy.Item):
    _id = scrapy.Field() #粉丝ID
    ID = scrapy.Field() #用户ID
    NickName = scrapy.Field() #昵称
    Signature = scrapy.Field() #个性签名
    Num_Tweets = scrapy.Field() #微博数
    Num_Follows = scrapy.Field() #关注数
    Num_Fans = scrapy.Field() #粉丝数
    profile_url = scrapy.Field() #主页链接

class FollowsItem(scrapy.Item):
    _id = scrapy.Field() #好友ID
    ID = scrapy.Field() #用户ID
    NickName = scrapy.Field() #昵称
    Signature = scrapy.Field() #个性签名
    Num_Tweets = scrapy.Field() #微博数
    Num_Follows = scrapy.Field() #关注数
    Num_Fans = scrapy.Field() #粉丝数
    profile_url = scrapy.Field() #主页链接


class KeyTweetsItem(scrapy.Item):
    _id = scrapy.Field() # 微博ID
    keyword = scrapy.Field()
    ID = scrapy.Field() #用户ID
    text = scrapy.Field() #微博内容
    PubTime = scrapy.Field() #发表时间
    createtime = scrapy.Field()