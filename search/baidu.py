#!/usr/bin/python
# -*- coding:utf-8 -*-


from scripts.searchEngine import SearchEngine
# from lxml import etree
# import HTMLParser
from config import logger
from parsel import Selector


class Baidu(SearchEngine):


    def __init__(self):
        super(Baidu, self).__init__()
        print 'this is baidu '

    def url(self,keyword,pageCount):
        logger.debug("[url] %s %s terminal generator %d pages search url " % (keyword,self.terminal,pageCount))
        urls = []
        # print self.terminal
        for i in range(pageCount):
            if self.terminal == "web":
                urls.append(u"http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%s&pn=%d" % (keyword, 10 * i))
            elif self.terminal == "wap":
                urls.append(u"https://m.baidu.com/s?pn=%d&word=%s" % (10 * i,keyword))
        return urls

    def _terminal_wap(self, url):
        """
        search_url  :::  [u'http://m.baidu.com/from=0/bd_page_type=1/ssid=0/uid=0/pu=usm%406%2Csz%401321_1004%2Cta%40utouch_2___/baiduid=6F90DA0D3E994CFDFBAEDA29E39025C8/w=0_10_/t=wap/l=3/tc?ref=www_utouch&lid=2632097706169249631&order=3&is_baidu=0&h5ad=0&tj=www_normal_3_0_10_1&vit=osres&m=8&srd=1&title=%E5%87%89%E5%87%89%E7%9A%84%E6%AD%8C%E8%AF%8D_%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93&dict=25&wd=&eqid=248716eb1656b000100000065bb858fe&w_qd=IlPT2AEptyoA_yk5uuccvAm&tcplug=1&sec=33246&di=30e5e331c8bc39bd&bdenc=1&nsrc=IlPT2AEptyoA_yixCFOxCGZb8c3JV3T5AAyNLCpZ0XSwnESzbbrgHtkfEFXeRXqJF5z7uiPQpxsHx8yh0W9m8hF2qaxktWwd8m36s_Go']
        danger_msg  :::
        search_index  :::  2
        search_title  :::  <em>凉凉</em>的歌词_百度知道
        search_description  :::  <em>凉凉</em>凉凉-(电视剧《三生三世十里桃花》片尾曲) - 张碧晨&杨宗纬作词:刘畅 作曲:谭旋编曲:韦国赟女:入夜渐...
        terminal  :::  wap
        :param url:
        :return:
        """
        logger.debug("[searchRows] xpath extract search result row %s" % url)
        # response = self.request(url,terminal='wap')
        # if response == False:
        #     return []
        # sel = Selector(text=response.text)
        with open('test_wap.html', 'r') as f:
            content = f.read()
            # f.write(response.text.encode("utf-8"))
        sel = Selector(text=content.decode("utf-8"))
        rows = []
        for node in sel.xpath("//div[@id='page-res']/div[@class='reswrap']/div[@class='resitem']"):
            self.index += 1
            row = {}
            row['search_index'] = self.index
            row['search_url'] = node.xpath("./a/@href").extract()
            contentDomPath = [
                "./a/em",
                "./a/text()",
                "./a/div[not(@class)]/em",
                "./a/div[not(@class)]/text()",
            ]
            row['search_title'] = ''.join(node.xpath('|'.join(contentDomPath)).extract())
            row['search_description'] = ''.join(node.xpath("./a/div[@class='result_title_abs']//text()|./a/div[@class='result_title_abs']//em").extract())
            row['danger_msg'] = ''
            row['terminal'] = self.terminal
            rows.append(row)
            # for key,val in row.iteritems():
            #     print key," ::: ",val
            # print '----------------\n'
        return rows

    def _terminal_web(self,url):
        """
        search_url  :::  [u'http://www.baidu.com/link?url=6GZBx6RFIHsmrwkzs2ImpILmdUCOr4S58SPmNaIVs3oQSylMIuDm69VQJCwVhuXp']
        danger_msg  :::  百度网址安全中心提醒您：该页面可能存在违法信息！
        search_index  :::  10
        search_title  :::  <em>香港金沙</em>娱乐城 - 官方授权
        search_description  :::  <em>香港金沙</em>娱乐城公众信息网是丰都县政府的官方网站,是丰都县政府服务社会公众的重要窗口、政<em>香港金沙</em>娱乐城府信息公开的第一平台、政民互动交流的重要渠道。
        terminal  :::  web
        :param url:
        :return:
        """
        logger.debug("[searchRows] xpath extract search result row %s" % url)
        response = self.request(url)
        if response == False:
            return []
        sel = Selector(text=response.text)
        # with open('test1.html', 'r') as f:
        #     content = f.read()
        # sel = Selector(text=content.decode("utf-8"))
        rows = []
        for node in sel.xpath("//div[@id='content_left']/div"):
            self.index += 1
            if "result c-container " in  node.xpath("./@class").extract():
                row = {}
                row['search_index'] = self.index
                row['search_url'] =  node.xpath("./h3/a/@href").extract()
                row['search_title'] = ''.join( node.xpath("./h3/a/node()").extract())
                contentDomPath = [
                    ".//div[@class='c-abstract']/em",
                    ".//div[@class='c-abstract']/text()",
                    ".//div[@class='c-span18 c-span-last']/font/p[not(@class)]/em",
                    ".//div[@class='c-span18 c-span-last']/font/p[not(@class)]/text()"
                ]
                row['search_description'] = ''.join(node.xpath('|'.join(contentDomPath)).extract())
                row['danger_msg'] = ''.join(node.xpath("./div[@class='unsafe_content f13']/a/text()").extract())
                row['terminal'] = self.terminal
                rows.append(row)
                # for key, val in row.iteritems():
                #     print key, " ::: ", val
                # print '----------------\n'
        return rows




if __name__ == '__main__':
    # import sys
    # print sys.path
    b = Baidu()
    b.search(('baidu', u'凉凉'))
    # print b.searchRows('http://sss')
    # for x in b.search(('baidu',u'凉凉')):
    #     print x
