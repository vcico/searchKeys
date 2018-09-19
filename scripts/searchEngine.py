#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import configure
import math
from scripts.page import Page
from abc import ABCMeta,abstractmethod

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

    def pages(self, urls, keyargs):
        """
        根据搜索结果 生成Page对象
        :param urls: list 根据配置数量生成的搜索列表页的url
        :return: yield Page
        """
        for url in urls:
            for row in self.searchRows(url):
                p = Page()
                p['search_text'] = keyargs[1]
                p['search_name'] = keyargs[0]
                for k, v in row.items():
                    p[k] = v
                yield p

    def target(self, page):
        """
        目标站结果
        :param page: Page
        :return: yield Page
        """

    def search(self, keyargs):
        """
        搜索关键词
        :param keyargs:  (搜索名称,关键词)
        :return: yield Page对象
        """
        pageCount = math.ceil(configure['result_count'] / self.pageSize)
        urls = self.url(keyargs[1], int(pageCount))
        for page in self.pages(urls, keyargs):
            yield self.target(page)


