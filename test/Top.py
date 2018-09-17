#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import redis
import md5



class Top:
	
	r = redis.Redis(host='localhost', port=6379, decode_responses=True)
	
	def __init__(self):
		self.kw = ''
		
	def getTopUrl(self):
		"""
			获取 关键词 百度搜索首页 链接(百度跳转) 和 title
			: param string kw 搜索关键词
			: return dict(url,title)
		"""
		# print self.kw
		if self.kw == '':
			raise AttributeError('关键词属性不能为空')
		req = requests.get(u'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%s' % self.kw)
		html_doc = req.text.encode('utf-8')
		soup = BeautifulSoup(html_doc, "html.parser")
		results = soup.select('#content_left .result')
		# unsafe = soup.select('#content_left .result unsafe_content a')
		i=1
		for result in results:
			# print result
			title = result.find('h3').find('a')
			unsafe = result.find('div',class_='unsafe_content')
			if unsafe:
				unsafe = unsafe.find('a')
			print title
			print unsafe
			title_text = ''.join([str(content.encode('utf-8')) for content in title.contents])
			data = (title['href'],title_text,'' if unsafe==None else unsafe.text,i)
			i+=1
			yield data
		
	def getOriginalUrl(self):
		"""
			根据百度跳转获取真实 URL
			: param list[dict(url,title,safeTip)] temUrls 百度跳转链接
			: return list[dict(url,title,safeTip)] 
		"""
		originalURLs = []
		for tmpurl in self.getTopUrl():
			tmpPage = requests.get(tmpurl[0], allow_redirects=False)
			if tmpPage.status_code == 200:
				urlMatch = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
				originalURLs.append((urlMatch.group(1), tmpurl[1],tmpurl[2],tmpurl[3]))
			elif tmpPage.status_code == 302:
				originalURLs.append((tmpPage.headers.get('location'), tmpurl[1],tmpurl[2],tmpurl[3]))
			else:
				print 'No URL found!!: %s %s' % (tmpurl[0] ,tmpurl[1])
		return originalURLs
		
		
	def getContent(self,originUrl):
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
		
	def getPagekw(self,page):
		"""
			获取网页关键内容： title keyword description H1-H6 strong
			: param string page 网页内容
			：return 
		"""
		page.decode('utf-8')
		soup = BeautifulSoup(page, "html.parser")
		title = soup.select('head title')
		keyword = soup.find("head").find("meta",attrs={"name": "keywords"})
		description = soup.find("head").find("meta",attrs={"name": "description"})
		h = soup.find("body").find_all(["h1", "h2","h3","h4","h5","h6","strong"])
		h = [ str(_h) for _h in h  ]
		return (title[0].text,keyword['content'],description['content'],' -#- '.join(h))
	
	
	def run(self):
		urls = self.getOriginalUrl()
		print urls
		for urlInfo in urls:
			hkey = md5.md5(urlInfo[0]).hexdigest()
			if(self.r.hexists('baiduTopUrlList', hkey)):
				self.r.hincrby("baiduTopUrlList", hkey, amount=1)
				self.r.rpush('baiduTopTime_'+hkey,int(time.time()))
			else:
				html = self.getContent(urlInfo[0])
				with open('%s.html' % hkey,'wb') as file:
					file.write(html)
				content = self.getPagekw(html)
				info = {
					'title':content[0],
					'keyword':content[1],
					'description':content[2],
					'body':content[3],
					'baiduTitle' : urlInfo[1],  # 搜索标题下的内容
					'safeTip': urlInfo[2], # 搜索时是否有风险提示
					'sort':urlInfo[3], # 排名
					'url':urlInfo[0],
				}
				self.r.hmset('baiduTopUrl_'+hkey,info)
				self.r.hincrby("baiduTopUrlList", hkey, amount=1)
				self.r.rpush('baiduTopTime_'+hkey,int(time.time()))
		
		
		
		
if __name__ == '__main__':
	t = Top()
	t.kw = u'威尼斯娱乐'
	t.run()
		
		
		
		
		
		