#!/usr/bin/python
# -*- coding:utf-8 -*-


from scripts.searchEngine import SearchEngine
# from lxml import etree
# import HTMLParser
from parsel import Selector


class Baidu(SearchEngine):


    def __init__(self):
        super(Baidu, self).__init__()
        print 'this is baidu '

    def url(self,keyword,pageCount):
        urls = []
        for i in range(pageCount):
            urls.append(u"http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%s&pn=%d" % (keyword,10*i))
        return urls


    def searchRows(self,url):
        # [ {search_title: search_keyword: search_description: search_content: search_index: search_url: danger_msg: }, ]
        # response = self.request(url)
        # selector = etree.HTML(response.text)
        with open('test1.html', 'r') as f:
            content = f.read()
        sel = Selector(text=content.decode("utf-8"))
        rows = []
        for node in sel.xpath("//div[@id='content_left']/div"):
            self.index += 1
            if "result c-container " in  node.xpath("./@class").extract():
                row = {}
                row['search_index'] = self.index
                row['search_url'] = url
                row['search_title'] = ''.join( node.xpath("./h3/a/node()").extract())
                contentDomPath = [
                    ".//div[@class='c-abstract']/em",
                    ".//div[@class='c-abstract']/text()",
                    ".//div[@class='c-span18 c-span-last']/font/p[not(@class)]/em",
                    ".//div[@class='c-span18 c-span-last']/font/p[not(@class)]/text()"
                ]
                row['search_description'] = ''.join(node.xpath('|'.join(contentDomPath)).extract())
                row['danger_msg'] = node.xpath("./div[@class='unsafe_content f13']/a/text()").extract()
                rows.append(row)
        return rows




if __name__ == '__main__':
    # import sys
    # print sys.path
    b = Baidu()
    # b.search(('baidu', u'凉凉'))
    b.searchRows('http://sss')
    # for x in b.search(('baidu',u'凉凉')):
    #     print x
