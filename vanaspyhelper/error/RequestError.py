# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : RequestError.py
# @Created  : 2020/11/2 7:02 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : Request 相关错误
# -------------------------------------------------------------------------------

class RequestException(Exception):
    pass

class ProxyTypeNotSupport(RequestException):

    def __init__(self , type):
        super(ProxyTypeNotSupport,self).__init__("未知的代理类型 [{}] ,仅支持 socks5,http".format(type))