#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import configure
from Queue import Queue
import search
import os
from scripts.exceptions import ConfigException
# from scripts.page import Page
from threading import Thread

def initSearch():
    """
    验证配置的搜索引擎
    :return:  boolean
    """
    searchs = {}
    for s in configure['search']:
        if not s:
            raise ConfigException('Configuration format error: search')
        try:
            searchs[s] = getattr(search,s.capitalize())()
        except AttributeError,e:
            raise ConfigException('config error. search engine processor not exist: %s' % s)
    return searchs

def pushKeyQueue():
    """
    增加页面对象队列元素
    :return: Queue
    """
    if not os.path.isfile(configure['keyword_file']):
        raise Exception('keywords file is not exist')
    f = open(configure['keyword_file'], 'r')
    for line in f.readlines():
        key = line.strip()
        if not key:
            continue
        for search_name in searchs.keys():
            keyQueue.put((search_name,key))


keyQueue = Queue()
resultQueue = Queue()
searchs = initSearch()


def worker(name,keyQueue,searchs,resultQueue):
    while True:
        item = keyQueue.get()
        resultQueue.put( "%s %s %s " % (name,item[0],item[1]))
        keyQueue.task_done()

def result(resultQueue):
    while True:
        item = resultQueue.get()
        print '--', item
        resultQueue.task_done()

for i in range(configure['thread_count']):
     t = Thread(target=worker,args=(i,keyQueue,searchs,resultQueue))
     t.daemon = True
     t.start()
t = Thread(target=result,args=(resultQueue,))
t.daemon = True
t.start()

pushKeyQueue()  # 队列增加
keyQueue.join()     # block until all tasks are done
resultQueue.join()     # block until all tasks are done

if __name__ == '__main__':
    #print configure
    # import sys
    # print sys.path
    pass

