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

class RequestResolverError(RequestException):

    def __init__(self,url:str):
        super(RequestResolverError,self).__init__("网页解析错误 URL=[{}]".format(url))

class DownloadFileGetStreamError(RequestException):

    def __init__(self,url:str):
        super(DownloadFileGetStreamError,self).__init__("请求文件下载 stream 错误 URL=[{}]".format(url))

class DownloadTimeout(RequestException):

    def __init__(self,url:str):
        super(DownloadTimeout,self).__init__("下载文件错误 URL=[{}]".format(url))

class SendRequestError(RequestException):

    def __init__(self, url: str , ex:Exception):
        super(SendRequestError, self).__init__("下载文件错误 URL=[{}]".format(url) , ex)



class WrongLocalVerifyTokenInsError(Exception):

    '''错误的本地验证 token 实体'''

    def __init__(self, ins):
        msg = "\n 本地验证 token 实体错误！！ @token_required 装饰器只接收 VerifyTokenLocal 实例，但是您传入的是: {} 。" \
              "\n 本地验证 token 说明：" \
              "\n   如果您在使用 @token_required 装饰器时，需要调用您服务的 token 验证方法。" \
              "\n   请在您的服务中用 from vanaspyhelper.wraps.token import VerifyTokenLocal 导入 `VerifyTokenLocal` 抽象类，并实现 verify 函数。" \
              "\n   当您服务的验证方法失败时，仍然会通过 Vanas-Token 服务器进行验证。" \
              "\n   当验证通过后会调用 `VerifyTokenLocal` 抽象类实体，通知 upgrade【如无更新需要可不实现】 函数更新本地 token。".format(str(type(ins)))
        super(WrongLocalVerifyTokenInsError, self).__init__(msg)