
import os  
 

class Config:

    config_file = 'setting.conf'
    
    config_handle = {
        'array' : ['search','result_method'],
        'integer' : ['thread_count','result_count'], #'page_count',
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
        return self.config[field].split(self.array_delimiter)

    def integerHandle(self,field):
        try:
            result = int(self.config[field])
        except ValueError,e:
            raise Exception("Configuration format error: %s Must be number " % field)
        return result

configure = Config().getConfig()


if __name__ == '__main__':
    pass