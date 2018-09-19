#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from scripts.searchEngine import SearchEngine


class Baidu(SearchEngine):


    def __init__(self):
        print 'this is baidu '

    def url(self,keyword,pageCount):
        urls = []
        for i in range(pageCount):
            urls.append(u"http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%s&pn=%d" % (keyword,10*i))
        return urls

    def searchRows(self,url):
        # [ {search_title: search_keyword: search_description: search_content: search_index: search_url: danger_msg: }, ]
        pass




if __name__ == '__main__':
    # import sys
    # print sys.path
    Baidu().search(('baidu',u'凉凉'))
