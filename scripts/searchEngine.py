#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import configure
import math
from scripts.page import Page
import requests
from abc import ABCMeta,abstractmethod,abstractproperty
import random
import time

"""
搜索引擎搜索结果统计基类
1、接收关键词参数
2、根据数量 产生搜索结果页的URL列表 ()
3、请求搜索结果页 用每一个结果去生成Page对象 记录相关信息
4、爬取目标站 / 判断是否手机端  并记录相关信息
5、把记录了搜索结果信息和目标站信息的Page对象返回 给结果处理模块
"""
class SearchEngine:

    __metaclass__ = ABCMeta

    pageSize = 10.0

    sleep = 0 # 同一个搜索引擎 每爬取一个页面休眠？秒

    terminal = '' # 终端 web或手机端  获取到的头部信息不同

    # def __init__(self):
    #     print "this is search Engine"
    @classmethod
    def setTerminal(cls,ter):
        cls.terminal = ter

    @abstractmethod
    def url(self, keyword, pageCount):
        """
        生成搜索结果列表页Url （包括翻页）
        :param keyword: 关键词
        :param pageCount: 页数
        :return: list[URL]
        """

    @abstractmethod
    def searchRows(self, url):
        """
        解析搜索结果页面
        :param url: string 查询结果url
        :return: list [ {search_title: search_keyword: search_description: search_content: search_index: search_url: danger_msg: }, ]
        """

    @classmethod
    def headers(cls):
        """
        返回获取搜索页面的头部信息
        :return: dict
        """
        userAgents = {
            "web":[
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.87 Chrome/49.0.2623.87 Safari/537.36',
                'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/45.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'
                'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'
            ],
            "wap":[
                'Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                'Mozilla/5.0 (Android; Tablet; rv:40.0) Gecko/40.0 Firefox/40.0',
                'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+',
                'Opera/9.80 (iPhone; Opera Mini/7.1.32694/27.1407; U; en) Presto/2.8.119 Version/11.10',
                'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.87 Mobile Safari/537.36',
                'Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11; IEMobile/11.0; NOKIA; Lumia 928) like Gecko',
            ]
        }
        # print "---------%s-------------" % cls.terminal
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'BAIDUID=EFF88D7D9A44E3869393D549C81548D7:FG=1; BIDUPSID=EFF88D7D9A44E3869393D549C81548D7; PSTM=1512443824; __cfduid=df63e3d278c323b0291d8f37c8ec4aa141521544166; sug=3; sugstore=1; ORIGIN=0; bdime=0; MCITY=-180%3A; BD_UPN=12314353; delPer=0; locale=zh; BD_HOME=0; H_PS_PSSID=26522_1440_21093_26350_27112',
            # 'Host': 'www.baidu.com',
            # 'Referer': 'http://baidu.com/',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(userAgents[cls.terminal])
        }

    @classmethod
    def spiderHeaders(cls):
        """
        模拟爬虫头部信息 爬取目标站 手机端
        :return: dict
        """
        userAgents = {
            "web":[
                'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
                'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36; 360Spider',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider(compatible; HaosouSpider; http://www.haosou.com/help/help_3_2.html)',
                'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
            ],
            "wap":[
                'SAMSUNG-SGH-E250/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 UP.Browser/6.2.3.3.c.1.101 (GUI) MMP/2.0 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)',
                'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            ]
        }
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': random.choice(userAgents[cls.terminal])
        }

    def pages(self, keyargs):
        """
        根据搜索结果 生成Page对象
        :param keyargs: (搜索名称,关键词) 根据配置数量生成的搜索列表页的url
        :return: yield Page
        """
        pageCount = math.ceil(configure['result_count'] / self.pageSize)
        urls = self.url(keyargs[1], int(pageCount))
        for ter in configure['terminals']:
            self.setTerminal(ter)
            for url in urls:
                self.searchRows(url)
                break
            break
                # for row in self.searchRows(url):
                #     p = Page()
                #     p['search_text'] = keyargs[1]
                #     p['search_name'] = keyargs[0]
                #     for k, v in row.items():
                #         p[k] = v
                #     yield p

    def target(self, page):
        """
        目标站结果
        :param page: Page
        :return: yield Page
        """
        content = self.request(page.url,search=False)


    def search(self, keyargs):
        """
        搜索关键词
        :param keyargs:  (搜索名称,关键词)
        :return: yield Page对象
        """
        self.pages(keyargs)
        # for page in self.pages(keyargs):
        #     print page
            # yield self.target(page)

    @classmethod
    def request(cls,url,search=True):
        """
        请求网页内容
        :param url: 网址
        :param search: 是否是搜索引擎的页面  用于获取不同的header
        :return: requests.Response | False
        """
        print "will get content of page %s " % url
        for i in range(configure['retry_count']+1):
            try:
                return requests.get(url, headers=cls.headers() if search else cls.spiderHeaders(), timeout=30)
            except requests.exceptions.RequestException,e:
                print "%s request fail:  %s" % (url, e.message)
        return False