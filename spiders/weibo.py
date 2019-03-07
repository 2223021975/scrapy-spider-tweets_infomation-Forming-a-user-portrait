import re
from scrapy.spider import CrawlSpider, logging
from scrapy.http import Request
import json
from myweibo.weiboID import weiboID
from myweibo.items import InformationItem,TweetsItem,FansItem,FollowsItem

class WeiBoSpider(CrawlSpider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']
    start_urls = list(set(weiboID))
    logging.getLogger("requests").setLevel(logging.WARNING)

    # 开始爬取
    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url="https://m.weibo.cn/api/container/getIndex?type=uid&value=%s"%uid,meta={'ID':uid},callback=self.parse_information)


    # 抓取个人信息
    def parse_information(self,response):
        ID = response.meta['ID']
        if len(response.body) > 50:
            informationItems = InformationItem()
            informations = json.loads(response.body)
            if informations.get('data',''):
                informationItems["_id"] = informations["data"]["userInfo"]["id"]
                informationItems["NickName"] = informations["data"]["userInfo"]["screen_name"]
                informationItems["Signature"] = informations["data"]["userInfo"]["description"]
                informationItems["Num_Tweets"] = informations["data"]["userInfo"]["statuses_count"]
                informationItems["Num_Follows"] = informations["data"]["userInfo"]["follow_count"]
                informationItems["Num_Fans"] = informations["data"]["userInfo"]["followers_count"]
                if informations["data"]["userInfo"]["gender"] == "f":
                    informationItems["gender"] = "女"
                elif informations["data"]["userInfo"]["gender"] == "m":
                    informationItems["gender"] = "男"
                yield informationItems
            # 微博入口
            tweets_container_id = informations["data"]["tabsInfo"]["tabs"][1]["containerid"]
            url_weibo = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s" % (response.meta["ID"], tweets_container_id)
            yield Request(url=url_weibo, meta={"ID": response.meta["ID"]}, callback=self.parse_Tweets,dont_filter=True)

            # 粉丝入口
            if informations.get("data", ""):
                fans_scheme = informations["data"]["fans_scheme"]
                fans_container_id = re.findall(r"containerid=(.*)", fans_scheme)
                fans_container_id[0] = fans_container_id[0].replace('fans_intimacy', 'fans')
                url_fans = "https://m.weibo.cn/api/container/getIndex?containerid=" + fans_container_id[0]
                yield Request(url=url_fans, meta={"ID": response.meta["ID"]}, callback=self.parse_fans_list, dont_filter=True)

            # 关注者入口
            if informations.get("data", ""):
                follow_scheme = informations["data"]["follow_scheme"]
                follow_container_id = re.findall(r"containerid=(.*)", follow_scheme)
                follow_container_id[0] = follow_container_id[0].replace('followersrecomm', 'followers')
                url_follow = "https://m.weibo.cn/api/container/getIndex?containerid=" + follow_container_id[0]
                yield Request(url=url_follow, meta={"ID": response.meta["ID"]}, callback=self.parse_follow_list, dont_filter=True)


    # 获取个人微博列表
    def parse_Tweets(self,response):
        if len(response.body) > 50:
            tweets = json.loads(response.body)
            ID = response.meta["ID"]
            page = ''
            containerid = ''
            if tweets.get("data", ""):
                cards = tweets["data"]["cards"]
            for i in range(1,2):
                page = i
                page = str(page)


                if tweets["data"]["cardlistInfo"].get("containerid", ""):
                    containerid = tweets["data"]["cardlistInfo"]["containerid"]
                for card in cards:
                    mblog = card.get('mblog', '')
                    if mblog:
                        tweetsItems = TweetsItem()
                        tweetsItems["_id"] = card["itemid"]
                        tweetsItems["ID"] = ID
                        #tweetsItems["Content"] = json.dumps(mblog)
                        tweetsItems["Content"] = mblog["text"]
                        tweetsItems["PubTime"] = mblog["created_at"]
                        tweetsItems["Like"] = mblog["attitudes_count"]
                        tweetsItems["Comment"] = mblog["comments_count"]
                        tweetsItems["Transfer"] = mblog["reposts_count"]
                    yield tweetsItems
                url_tweets = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s&page=%s" % (ID, containerid, page)
                yield Request(url=url_tweets, meta={"ID": ID}, callback=self.parse_Tweets, dont_filter=True)
            else:
                return
        else:
            return
        pass



    # 获取某个人粉丝列表
    def parse_fans_list(self,response):
        if len(response.body) > 50:
            fans = json.loads(response.body)
            ID = response.meta["ID"]
            containerid = ''
            since_id = ''
            if fans.get("data", ""):
                if fans["data"]["cardlistInfo"].get("since_id", ""):
                    since_id = fans["data"]["cardlistInfo"]["since_id"]
                    since_id = str(since_id)
                else:
                    return
                if fans["data"]["cardlistInfo"].get("containerid", ""):
                    containerid = fans["data"]["cardlistInfo"]["containerid"]

                cards = fans["data"]["cards"]
                for card in cards:
                    card_group = card["card_group"]
                    for element in card_group:
                        if element:
                            fansItems = FansItem()
                            fansItems["_id"] = element["user"]["id"]
                            fansItems["ID"] = ID
                            fansItems["NickName"] = element["user"]["screen_name"]
                            fansItems["Signature"] = element["user"]["description"]
                            fansItems["Num_Tweets"] = element["user"]["statuses_count"]
                            fansItems["Num_Follows"] = element["user"]["follow_count"]
                            fansItems["Num_Fans"] = element["user"]["followers_count"]
                            fansItems["profile_url"] = element["user"]["profile_url"]
                            yield fansItems
                fans_url = "https://m.weibo.cn/api/container/getIndex?containerid=%s&since_id=%s" % (containerid, since_id)
                yield Request(url=fans_url, meta={'ID': ID}, callback=self.parse_fans_list, dont_filter=True)
            else:
                return
        else:
            return


    # 获取某个人关注列表
    def parse_follow_list(self, response):
        if len(response.body) > 50:
            page = ''
            containerid = ''
            follow = json.loads(response.body)
            if follow.get("data", ""):
                if follow["data"]["cardlistInfo"].get("page", ""):
                    page = follow["data"]["cardlistInfo"]["page"]
                    page = str(page)
                else:
                    return
                if follow["data"]["cardlistInfo"].get("containerid", ""):
                    containerid = follow["data"]["cardlistInfo"]["containerid"]
            else:
                return

            ID = response.meta["ID"]
            if follow.get("data", ""):
                cards = follow["data"]["cards"]
                card_group = cards[len(cards) - 1]["card_group"]
                for card in card_group:
                    if card:
                        followsItems = FollowsItem()
                        followsItems["ID"] = ID
                        followsItems["_id"] = card["user"]["id"]
                        followsItems["NickName"] = card["user"]["screen_name"]
                        followsItems["Signature"] = card["desc1"]
                        followsItems["Num_Tweets"] = card["user"]["statuses_count"]
                        followsItems["Num_Follows"] = card["user"]["follow_count"]
                        followsItems["Num_Fans"] = card["user"]["followers_count"]
                        followsItems["profile_url"] = card["user"]["profile_url"]
                        yield followsItems
                url_follow = "https://m.weibo.cn/api/container/getIndex?containerid=%s&page=%s" % (containerid, page)
                yield Request(url=url_follow, meta={"ID": ID}, callback=self.parse_follow_list, dont_filter=True)
            else:
                return
        else:
            return
        pass
