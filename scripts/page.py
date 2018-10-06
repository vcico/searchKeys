#!/usr/bin/python
# -*- coding:utf-8 -*-

class Field():
    """Container of field metadata"""

class ItemMetaclass(type):
    def __new__(cls, name, bases, attrs):
        x_class = type.__new__(cls,'x_'+name,bases,attrs)
        fields = getattr(x_class,"fields",{})
        new_attrs = {}
        for n in dir(x_class):
            v = getattr(x_class,n)
            if isinstance(v,Field):
                fields[n] = None
            elif n in attrs:
                new_attrs[n] = attrs[n]
        new_attrs['fields'] = fields
        new_attrs['_class'] = x_class
        return type.__new__(cls, name, bases, new_attrs)

"""
页面对象
是否报危险，TDK， 搜索标题下的排名，整体内容等 生成页面对象
访问目标站 判断 wap
记录目标站的结果
"""
class Page():

    __metaclass__ = ItemMetaclass

    search_text = Field() # 搜索的文字
    search_name = Field() # 搜索引擎的名称
    terminal = Field() # 终端 web 或 wap

    search_title = Field()
    search_keyword = Field()
    search_description = Field()
    search_content = Field()
    search_index = Field()
    search_url = Field()# 跳转到目标站的网址
    danger_msg = Field()

    is_wap = Field()
    url = Field()
    title = Field()
    keyword = Field()
    description = Field()
    focus  = Field() # 模板页面 内容中的 H 或 strong 重点标签

    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
        if key in self.fields:
            self.fields[key] = value
        else:
            raise KeyError("%s does not support field: %s" %
                (self.__class__.__name__, key))

    def __delitem__(self, key):
        del self.fields[key]

    def __iter__(self):
        return iter(self.fields)

    def __str__(self):
        # print type(self['search_text'])
        # print type(self['search_name'].decode('utf-8'))  #
        return "<Page %s %s %s %d>" %  (self['search_name'],self['terminal'], self['search_text'].encode("utf-8") ,self['search_index'])
        # return u"<Page %s %s>" % (self['search_text'], self['search_name'].decode('utf-8'))

if __name__ == '__main__':
    pass
    # a = Page()
    # a['focus'] = "fdafdfaf"
    # for k in a:
    #     print a.fields[k]
    # print
    # print ( Field(x='d') )