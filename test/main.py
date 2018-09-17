#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import redis
import md5
# import sys 
# reload(sys) 
# sys.setdefaultencoding( "utf-8" ) 
# ===============================
# iso-8859-1 转成 utf-8
# str.encode("iso-8859-1").decode('gbk').encode('utf8') 
# https://blog.csdn.net/kelindame/article/details/75014485 
# =================================
"""
参考
   http://www.cnblogs.com/bitpeng/p/4748872.html
编码转换 http://blog.chinaunix.net/uid-13869856-id-5747417.html
&#27979;&#35797; HTMLparser 转换成中文 https://segmentfault.com/q/1010000000379229 
redis    https://www.jianshu.com/p/2639549bedc8
"""



def getTopUrl(kw):
	"""
		获取 关键词 百度搜索首页 链接(百度跳转) 和 title
		: param string kw 搜索关键词
		: return dict(url,title)
	"""
	r = requests.get(u'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%s' % kw)
	html_doc = r.text.encode('utf-8')
	soup = BeautifulSoup(html_doc, "html.parser")
	h3 = soup.select('#content_left .result h3 a')
	tmpurl = []
	for d in h3:
		tmpurl.append((d['href'],''.join([str(content.encode('utf-8')) for content in d.contents])))
	return tmpurl
	
tmpURLs = [(u'http://www.baidu.com/link?url=gKfTMQ77G-p-wJZYP93Pq9Bw7ZA5ru8qTY5xHnh1dH7', '\xe3\x80\x90<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe3\x80\x91>\xe5\x94\xaf\xe4\xb8\x80\xe6\x8c\x87\xe5\xae\x9a\xe5\xae\x98\xe7\xbd\x91\xe9\xa6\x96\xe9\xa1\xb5*<em>\xe5\xa8\x81 \xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em> *\xe3\x80\x90\xe5\x94\xaf\xe4\xb8\x80\xe5\x85\xa5\xe5\x8f\xa3\xe3\x80\x91'), (u'http://www.baidu.com/link?url=ks39GDHvEepienIe5hbtOEvyA6dNHO9DpV_bLWlZWDy6JAXI3QX1F0L5QrY2PxZF', '\xe6\xbe\xb3\xe9\x97\xa8<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe5\xae\x98\xe6\x96\xb9\xe7\xbd\x91\xe7\xab\x99,\xe7\xba\xbf\xe4\xb8\x8a<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba\xe7\x8e\xb0\xe9\x87\x91\xe8\xb5\x8c\xe5\x8d\x9a\xe5\xbc\x80\xe6\x88\xb7\xe7\xbd\x91\xe5\x9d\x80,<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>...'), (u'http://www.baidu.com/link?url=8_M6CHl9nZS4qPy4Mf9_BpHf5_g2F5j6tuZMxc4EjrG', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\x9f\x8e-\xe8\x80\x81\xe5\x93\x81\xe7\x89\x8c,\xe5\x8d\x8e\xe4\xba\xba\xe9\xa6\x96\xe9\x80\x89,\xe5\x80\xbc\xe5\xbe\x97\xe4\xbf\xa1\xe8\xb5\x96'), (u'http://www.baidu.com/link?url=kv39lMI2iu2bOKN2tUhMiqT117r_odaCulTMI7lB3UxQZvM1ooE9DX8LPh7B9IM7', '\xe6\xbe\xb3\xe9\x97\xa8<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\xae\x98\xe7\xbd\x91_<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\xae\x98\xe7\xbd\x91_<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>'), (u'http://www.baidu.com/link?url=fm6oSGPMXvD1UGU8amtz6hKAF-pq4lozv9QLVhQ8K67_qlmaMXpeUR190kh3YuAw', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>\xe7\x99\xbb\xe5\xbd\x95\xe5\xb9\xb3\xe5\x8f\xb0'), (u'http://www.baidu.com/link?url=0PUWaCSABdRyIi6XA0oZxqdseLeGWdGRBcWZquE4m9QjNXLH85w7AOhXD8p5MixDiuLRwVfAKy4_Hia2zl8woq', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>_\xe4\xb8\xad\xe5\x9b\xbd\xe7\xa7\x91\xe5\xad\xa6\xe9\x99\xa2'), (u'http://www.baidu.com/link?url=_RbBFAl82ZB9OHvvdwU3nR9Ubp4YDX2-q8POSsL3sArOx28kpze2kMZ15Zvswjwi1DmtZmPMCObvJAPUG-gcwq', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>\xe7\xbd\x91__\xe8\x82\xa1\xe7\xa5\xa8\xe5\x85\xa5\xe9\x97\xa8\xe7\xbd\x91_\xe5\xa4\xa9\xe6\xb0\x94'), (u'http://www.baidu.com/link?url=a7zlngu2f_iiJ9bXEG_ZZbhjBRmKn7vMDzg6uXDAeuzuzNO9CrPaoPpg1kw4ob3o1-KRpKrPABNF0pBxfaNWva', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\x9c\xba\xe6\x89\x80_\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe6\x9c\x89\xe4\xbb\x80\xe4\xb9\x88\xe5\xa5\xbd\xe7\x8e\xa9\xe5\x9c\xb0\xe6\x96\xb9/\xe6\x9c\x89\xe5\x93\xaa\xe4\xba\x9b\xe5\xa5\xbd\xe7\x8e\xa9\xe7\x9a\x84/\xe6\x99\x9a\xe4\xb8\x8a\xe5\xa5\xbd\xe5\x8e\xbb\xe5\xa4\x84\xe3\x80\x90...'), (u'http://www.baidu.com/link?url=9XNy3Bc8k4Marh49O6ktF7uW-N-_pZpi0uYB_CQ32vLqqoqHPv3pkfFYYgohfQ2kixHWbBoId48npF7yLuM4t_', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>')]

def getOriginalUrl(tmpURLs):
	"""
		根据百度跳转获取真实 URL
		: param list[dict(url,title)] temUrls 百度跳转链接
		: return list[dict(url,title)] 
	"""
	originalURLs = []
	for tmpurl in tmpURLs:
		tmpPage = requests.get(tmpurl[0], allow_redirects=False)
		if tmpPage.status_code == 200:
			urlMatch = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
			originalURLs.append((urlMatch.group(1), tmpurl[1]))
		elif tmpPage.status_code == 302:
			originalURLs.append((tmpPage.headers.get('location'), tmpurl[1]))
		else:
			print 'No URL found!!: %s %s' % (tmpurl[0] ,tmpurl[1])
	return originalURLs

originUrls = [
	('http://www.lzc369.com/', '\xe3\x80\x90<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe3\x80\x91>\xe5\x94\xaf\xe4\xb8\x80\xe6\x8c\x87\xe5\xae\x9a\xe5\xae\x98\xe7\xbd\x91\xe9\xa6\x96\xe9\xa1\xb5*<em>\xe5\xa8\x81 \xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em> *\xe3\x80\x90\xe5\x94\xaf\xe4\xb8\x80\xe5\x85\xa5\xe5\x8f\xa3\xe3\x80\x91'), 
	('http://www.bjszhsfx.com/', '\xe6\xbe\xb3\xe9\x97\xa8<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe5\xae\x98\xe6\x96\xb9\xe7\xbd\x91\xe7\xab\x99,\xe7\xba\xbf\xe4\xb8\x8a<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba\xe7\x8e\xb0\xe9\x87\x91\xe8\xb5\x8c\xe5\x8d\x9a\xe5\xbc\x80\xe6\x88\xb7\xe7\xbd\x91\xe5\x9d\x80,<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>...'), 
	('https://www.v511.cc/', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\x9f\x8e-\xe8\x80\x81\xe5\x93\x81\xe7\x89\x8c,\xe5\x8d\x8e\xe4\xba\xba\xe9\xa6\x96\xe9\x80\x89,\xe5\x80\xbc\xe5\xbe\x97\xe4\xbf\xa1\xe8\xb5\x96'), 
	('http://www.xmmohan.com/', '\xe6\xbe\xb3\xe9\x97\xa8<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\xae\x98\xe7\xbd\x91_<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\xae\x98\xe7\xbd\x91_<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf</em>\xe4\xba\xba<em>\xe5\xa8\xb1\xe4\xb9\x90</em>'), 
	('http://www.90houqq.com/web1PAs197235/', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>\xe7\x99\xbb\xe5\xbd\x95\xe5\xb9\xb3\xe5\x8f\xb0'), 
	('http://www.jdwx.cn/appSpI411/11485.html', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>_\xe4\xb8\xad\xe5\x9b\xbd\xe7\xa7\x91\xe5\xad\xa6\xe9\x99\xa2'), 
	('http://www.haiyanglvyou.com/662/031234.html', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>\xe7\xbd\x91__\xe8\x82\xa1\xe7\xa5\xa8\xe5\x85\xa5\xe9\x97\xa8\xe7\xbd\x91_\xe5\xa4\xa9\xe6\xb0\x94'), 
	('http://www.lvmama.com/lvyou/play/d-weinisi3835.html', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>\xe5\x9c\xba\xe6\x89\x80_\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe6\x9c\x89\xe4\xbb\x80\xe4\xb9\x88\xe5\xa5\xbd\xe7\x8e\xa9\xe5\x9c\xb0\xe6\x96\xb9/\xe6\x9c\x89\xe5\x93\xaa\xe4\xba\x9b\xe5\xa5\xbd\xe7\x8e\xa9\xe7\x9a\x84/\xe6\x99\x9a\xe4\xb8\x8a\xe5\xa5\xbd\xe5\x8e\xbb\xe5\xa4\x84\xe3\x80\x90...'), 
	('https://www.yycaf.net/ppJJw25/227954.html', '<em>\xe5\xa8\x81\xe5\xb0\xbc\xe6\x96\xaf\xe5\xa8\xb1\xe4\xb9\x90</em>')
]
	

def getFileName(url):
	"""
	获取文件名称(根据 网址 日期)
	: param string url 网址  
	"""
	return "%s___%s.html" % (time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()),url.replace('/','_').replace(':','_'))
	
	
def getContent(originUrl):
	"""
		获取排名在百度首页网址的内容
		: param string originUrl
		: return string  网页内容
	"""
	headers = {'user-agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
	r = requests.get(originUrl,headers=headers,verify=False)
	if r.encoding == 'ISO-8859-1':
		encodings = requests.utils.get_encodings_from_content(r.text)
		if encodings:
			encoding = encodings[0]
		else:
			encoding = r.apparent_encoding
		encode_content = r.content.decode(encoding, 'replace').encode('utf-8', 'replace')
		print '='*50,originUrl, r.headers['Content-type'],'-', r.encoding ,'='*50
	elif  r.encoding in ('GBK','gbk','gb2312','GB2312'):
		print '='*50,originUrl, r.headers['Content-type'],'-', r.encoding ,'='*50
		encode_content = r.text.encode('utf-8')
	else:
		encode_content = r.text.encode('utf-8')
		print '='*50,originUrl, r.headers['Content-type'],'-', r.encoding ,'='*50
	return encode_content
	
	
	
# for originUrl in originUrls:
	# html = getContent(originUrl[0])
	# baiduKeyword = originUrl[1]
	# url = originUrl[0]
	# with open(getFileName(url),'wb') as file:
		# file.write(html)
		
		
		
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
		
		
# current_milli_time = lambda: int(round(time.time() * 1000))
		
def getPagekw(page,url):
	"""
		获取网页关键内容： title keyword description H1-H6 strong
		: param string page 网页内容
		：return 
	"""
	global r
	page.decode('utf-8')
	soup = BeautifulSoup(page, "html.parser")
	title = soup.select('head title')
	keyword = soup.find("head").find("meta",attrs={"name": "keywords"})
	description = soup.find("head").find("meta",attrs={"name": "description"})
	h = soup.find("body").find_all(["h1", "h2","h3","h4","h5","h6","strong"])
	h = [ str(_h) for _h in h  ]
	
	hkey = md5.md5(url).hexdigest()
	info = {
		'url':url,
		'title':title[0].text,
		'keyword':keyword['content'],
		'description':description['content'],
		'body':' -#- '.join(h)
		# 搜索标题下的内容
		# 搜索时是否有风险提示
	}
	r.hmset('baiduTopUrl_'+hkey,info)
	r.hincrby("baiduTopUrlList", hkey, amount=1)
	r.rpush('baiduTopTime_'+key,int(time.time()))
	# print title[0].text
	# print keyword['content']
	# print description['content']
	# print ' -#- '.join(h)
	
	
	
	# print ' -#- '.join(h)
	# print dir(bodyKeys[0].text)
	# print bodyKeys[0].text
	# print bodyKeys[0].string
	# print str(bodyKeys[0])
	# print keyword.attrs
	# print keyword['content']
	# print title[0].contents[0]
	# r.set('web_title', title[0].contents[0])
	# r.set('web_title', title[0].text)
	
	
	
	
with open('2018-04-13_11-49-49___http___www.lvmama.com_lvyou_play_d-weinisi3835.html.html','r') as file:
	getPagekw(file.read(),'http://www.lvmama.com/lvyou/play/d-weinisi3835.html.html')
	
"""
for originUrl in originUrls:
        headers = {'user-agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
        r = requests.get(originUrl[0],headers=headers,verify=False)
        # print r.encoding,':',originUrl[0]
        r.encoding = 'utf-8'
        # print r.text.encode('utf-8')
        print   isinstance(r.text, unicode),' -- ', r.encoding, ' -- ', originUrl[0], md5.md5(originUrl[0]).hexdigest()

        with open("%s.html" % md5.md5(originUrl[0]).hexdigest(),'wb') as file:
                
                if r.encoding == 'ISO-8859-1':
                        file.write(r.text.encode("iso-8859-1").decode('gbk').encode('utf8')  )
                elif r.encoding == 'utf-8':
                        file.write(r.text.encode('utf-8'))
                elif r.encoding == 'gbk' or r.encoding=='GBK':
                        file.write(r.text.encode('utf-8'))
                else:
                        print '==========%s==========' % r.encoding
          
                file.write(r.text.encode('utf-8'))
                file.write('\n'+originUrl[0])
                file.write('\n'+originUrl[1])
        #print originUrl[0]
        #print originUrl[1]
        # if r.encoding == 'utf-8':
                # print r.text.unicode()
                # print r.text.decode('gbk').encode('utf-8')
                # print '===================\n'
				
		if r.encoding == 'ISO-8859-1':
			encodings = requests.utils.get_encodings_from_content(r.text)
			if encodings:
					encoding = encodings[0]
			else:
					encoding = r.apparent_encoding
			encode_content = r.content.decode(encoding, 'replace').encode('utf-8', 'replace')
			print encode_content
			print '='*50,originUrl[0], r.headers['Content-type'],'-', r.encoding ,'='*50
		elif r.encoding == 'GBK' or r.encoding == 'gbk':
                print '='*50,originUrl[0], r.headers['Content-type'],'-', r.encoding ,'='*50
                print r.text[:1000].encode('utf-8')
        else:
                print '='*50,originUrl[0], r.headers['Content-type'],'-', r.encoding ,'='*50
"""

"""
tmpURLs = getTopUrl(u'威尼斯娱乐')
originUrls = getOriginalUrl(tmpURLs)
"""


