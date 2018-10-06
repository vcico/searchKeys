#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import logging
import time
from scripts.exceptions import ConfigException

class Config:

    config_file = 'setting.conf'
    
    config_handle = {
        'array' : ['search','result_method','terminals'],
        'integer' : ['thread_count','result_count','retry_count','sleep_minute'], #'page_count',
    }

    array_in_range = {
        'search':['baidu','google','so','sogou'],
        'result_method':['redis','text','xlsx'],
        'terminals':['wap','web'],
    }
    
    array_delimiter = '|'

    def __init__(self):
        # print "%s/%s" % (os.path.dirname(os.path.realpath(__file__)),self.config_file)
        if not os.path.isfile("%s/%s" % (os.path.dirname(os.path.realpath(__file__)),self.config_file)):
            raise Exception('configure file is not exist')
        self.config = {}

    def getConfig(self):
        f = open("%s/%s" % (os.path.dirname(os.path.realpath(__file__)),self.config_file),'r')
        for line in f.readlines():
            data=line.strip()
            if len(data) != 0:
                if data[0] == '#':
                    continue
                key,value = data.split('=')
                self.config[key.strip()] = value.strip()
        return self.convConfig()
        
    def convConfig(self):
        for handle_str,fields in self.config_handle.iteritems():
            handle = getattr(self,'%sHandle' % handle_str)
            for field in fields:
                try:
                    self.config[field] = handle(field)
                except KeyError,e:
                    raise Exception("Missing configuration items: %s " % field)
        return self.config
            
    def arrayHandle(self,field):
        arr = self.config[field].split(self.array_delimiter)
        print arr
        if set(arr).difference(set(self.array_in_range[field])):
            raise ConfigException('Configuration items exceed predetermined values : %s ' % field)
        return arr

    def integerHandle(self,field):
        try:
            result = int(self.config[field])
        except ValueError,e:
            raise Exception("Configuration format error: %s Must be number " % field)
        return result


def getLogger():
    """
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    :return: logger
    """
    logger = logging.getLogger('N')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.FileHandler('../log/%s' %  time.strftime("%Y-%m-%d.log", time.localtime()))
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

configure = Config().getConfig()
logger = getLogger()

if __name__ == '__main__':
    print configure
    pass