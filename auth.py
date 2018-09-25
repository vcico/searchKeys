#!/usr/bin/python
# -*- coding:utf-8 -*-

from Crypto.Cipher import AES
import json
import time
import requests
import wmi


class Auth:

    # 加密与解密所使用的密钥，长度必须是16的倍数
    secret_key = "ThisIs SecretKey"
    # 要加密的明文数据，长度必须是16的倍数
    #plain_data = "Hello, World123!"
    # IV参数，长度必须是16的倍数
    iv_param = 'This is an IV456'

    def __init__(self):
        pass

    def init_data(self,auth_key):
        data = {
            'last_time': int(time.time()),
            'auth_key':auth_key,
            'errors':[], # 过期时间 30天 那么连续30天都是错误 就有30个错误信息，每次成功验证后 错误都清空
            # 1, 请求api失败 2, 服务超时需要续费 3 api请求到的数据非数字
            'error_time':0, # 连续错误的首个错误的时间 每次成功验证后 错误时间都清空
        }
        self.write(data)

    def write(self,data):
        """
        写入加密数据到文件
        :param data: dict
        :return: boolean
        """
        data = json.dumps(data)
        s = len(data)% 16
        if s:
            data += " "* (16 - s )
        # print "%d - %d - %d" % (s,16 - s,len(data) )
        # print data,"$"
        with open('auth','w') as f:
            f.write(self.encrypt(data))
        return True

    def read(self):
        """
        从文件读取数据
        :return:  dict
        """
        with open('auth',"r") as f:
            data = f.read()
        data = self.decipher(data).strip()
        return json.loads(data)


    def encrypt(self,plain_data):
        # 数据加密 # 要加密的明文数据，长度必须是16的倍数
        aes = AES.new(self.secret_key, AES.MODE_CBC, self.iv_param)
        #cipher_data = aes1.encrypt(plain_data)
        #print('cipher data: ', cipher_data)
        return aes.encrypt(plain_data)

    def decipher(self,cipher_data):
        # 数据解密
        aes = AES.new(self.secret_key, AES.MODE_CBC, self.iv_param)
        #plain_data2 = aes2.decrypt(cipher_data)  # 解密后的明文数据
        #print('plain text: ', plain_data2)
        return aes.decrypt(cipher_data)

    def token_response(self,token):
        headers = {'user-agent': 'key-app/0.0.1'}
        try:
            r = requests.post('http://itbook.fun/keyapp', headers=headers, data={'token': token}, timeout=20)
            return r
        except Exception,e:
            return False

    def verify(self):
        """
         验证权限
        :todo  无妨访问API 发送邮箱给作者
        :return:
        """
        try:
            data = self.read()
        except Exception,e:
            print "Permission verification failed: auth file read failed. Please contact the service provider.\n"
            return False
        v = False
        r = self.token_response(data['auth_key'])
        if r == False:
            data['errors'].append(1)
            # email to author
        else:
            try:
                timeout = int(r.text)
                if timeout > int(time.time()):
                    data['errors'] = []
                    data['last_time'] = int(time.time())
                    v = True
                else:
                    data['errors'].append(2)
            except ValueError,e:
                data['errors'].append(3)
                # email to author
        self.write(data)
        if v == False:
            if len(data['errors']) > 30:
                raise Exception(" Over 30 days probation period. Please contact the service provider.")
            print "Warning:: Permission verification failed. 30 days without verification will be expired.\n"
        return v

def main_board_identify():
    """
    主板标识
    :see: https://blog.csdn.net/fengmm521/article/details/79468677
    :return:
    """
    c = wmi.WMI()
    boards = ''
    for board_id in c.Win32_BaseBoard():
        boards += board_id.qualifiers['UUID'][1:-1]
        boards += board_id.SerialNumber
        boards += board_id.Manufacturer
        boards += board_id.Product
    return boards

if __name__ == '__main__':
    # a = Auth()
    # m = a.encrypt("Hello, World123!")
    # print m
    # print a.decipher(m)
    # a.write("this is an example")
    # a.init_data('abcdefg1234567890')
    # print a.read()
    # Main_board()
    pass

