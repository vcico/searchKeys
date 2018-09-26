#!/usr/bin/python
# -*- coding:utf-8 -*-


from scripts.searchEngine import SearchEngine
from lxml import etree
import HTMLParser


class Baidu(SearchEngine):


    def __init__(self):
        # super.__init__()
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


        parser = HTMLParser.HTMLParser()
        with open('test.html', 'r') as f:
            content = f.read()
        selector = etree.HTML(content)
        rows = selector.xpath("//div[@id='content_left']/div[@class='result c-container ']")
        for row in rows:
            # print row.getchildren()
            print row.values()
            """
            nodeString = u''
            for n in row.xpath("./h3/a/node()"):
                if isinstance(n, etree._Element):
                    nodeString += parser.unescape(etree.tostring(n,encoding="UTF-8")) # print  etree.tostring(n, pretty_print=True),
                    break
                else:
                    nodeString += n
            print nodeString
            """
            # print
                # if isinstance(n,Element):
                #     print n
                # else:
                #     print "--%s--" % n
            # print etree.tostring(row.xpath("./h3/a")[0], pretty_print=True)
        #/text()
        # with open('test.html','w') as f:
        #     f.write(response.text.encode('utf-8'))



if __name__ == '__main__':
    # import sys
    # print sys.path
    b = Baidu()
    # b.search(('baidu', u'凉凉'))
    b.searchRows('http://sss')
    # for x in b.search(('baidu',u'凉凉')):
    #     print x
