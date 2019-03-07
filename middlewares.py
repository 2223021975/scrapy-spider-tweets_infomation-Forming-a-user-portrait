# -*- coding: utf-8 -*-
import base64
import random
from myweibo.user_agent import agents
from myweibo.cookies import cookies
from myweibo.proxy import proxys
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class UserAgentMiddleware(UserAgentMiddleware):
    def process_request(self,request,spider):
        agent = random.choice(agents)
        request.headers.setdefault("User-Agent",agent)


class CookiesMiddleware(object):
    def process_request(self,request,spider):
        cookie = random.choice(cookies)
        request.cookies = cookie



    # def process_response(self,request):
    #     pass

# 设置代理IP
class ProxyMiddleware(object):
     def process_request(self, request, spider):
        if len(proxys) > 0:
            proxy = random.choice(proxys)
            request.meta['proxy'] = proxy
            # proxy_user_pass = "USERNAME:PASSWORD"
            # encoded_user_pass = base64.encodestring(proxy_user_pass)
            # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass