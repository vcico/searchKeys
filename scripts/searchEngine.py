#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import configure
import math
from scripts.page import Page
import requests
from abc import ABCMeta,abstractmethod,abstractproperty
import random

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
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        }

    @classmethod
    def spiderHeaders(cls):
        """
        模拟爬虫头部信息 爬取目标站 手机端
        :return: dict
        """
        userAgents = [
            'SAMSUNG-SGH-E250/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 UP.Browser/6.2.3.3.c.1.101 (GUI) MMP/2.0 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)',
            'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        ]
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': random.choice(userAgents)
        }

    def pages(self, keyargs):
        """
        根据搜索结果 生成Page对象
        :param keyargs: (搜索名称,关键词) 根据配置数量生成的搜索列表页的url
        :return: yield Page
        """
        pageCount = math.ceil(configure['result_count'] / self.pageSize)
        urls = self.url(keyargs[1], int(pageCount))
        for url in urls:
            self.searchRows(url)
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
        try:
            requests.get(url, headers=cls.headers() if search else cls.spiderHeaders(), timeout=30)
        except requests.exceptions.RequestException,e:
            print "%s request fail:  %s" % (url, e.message)