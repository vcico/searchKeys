#!/usr/bin/python
# -*- coding:utf-8 -*-


class PageMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print cls
        print name
        print bases
        print attrs
        return type.__new__(cls, name, bases, attrs)

"""
页面对象
根据搜索引擎搜索的单个结果：是否报危险，TDK， 搜索标题下的排名，整体内容等 生成页面对象
访问目标站 判断 wap
记录目标站的结果
"""
class Page:

    __metaclass__ = PageMetaclass

    search_title = ''
    search_keyword = ''
    search_description = ''
    search_content = ''
    search_index = ''

    danger_msg = ''
    is_wap = ''

    title = ''
    keyword = ''
    description = ''

    # 模板页面 内容中的 H 或 strong 重点标签
    focus  = ''


if __name__ == '__main__':
    a = Page()
