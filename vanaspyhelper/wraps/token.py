# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : token.py
# @Created  : 2020/11/12 8:47 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     :  token 装饰器
# -------------------------------------------------------------------------------

from abc import ABC,abstractmethod
from vanaspyhelper.error.RequestError import WrongLocalVerifyTokenInsError


class VerifyTokenLocal(ABC):
    '''本地验证抽象类，由第三方实现'''

    @abstractmethod
    def verify(self, client_id, access_token)->bool:
        """

            #. 验证 token 本地方法，可以是数据库、缓存。 尽量避免少的与 token 服务器进行交互。
            #. 当 本地验证的 token，与服务器传入的 token，预期不符时，返回 False。
            #. 请在内部处理`异常`。

        """

    def upgrade(self,client_id, access_token):
        """
            验证 token 本地方法通过后，证明客户端传递的是正确的并且是新的 token。通知保存
        """


def __isTokenSuccess(verify_token_res:dict):
    """
    验证 token 是否合法
    :param verify_token_res:
    :return:
    """
    if verify_token_res["success"] == int(False):
        return False
    return True


def __need_local_verify(ins:VerifyTokenLocal=None):
    """
    ins 是否存在，是否 VerifyTokenLocal 对象
    :param ins:
    :return:
    """
    if ins is None:
        return False    # 为 None， 不需要本地验证

    if not isinstance(ins, VerifyTokenLocal):   # 有值，但是不是 VerifyTokenLocal 实体，抛出异常
        raise WrongLocalVerifyTokenInsError(ins)

    return True         # 以上都满足， 返回 True 需要本地验证


def token_required(ins:VerifyTokenLocal=None):

    """验证 token 的装饰器

        args :
            ins: 本地验证实现类实例

                #. 默认 None ， 通过 vanas-token 服务器验证
                #. 本地验证是为了避免少的与 vanas-token 服务器的交互所采用的方式
                #. 本地验证可以通过数据库，缓存对比一段时间内 access_token 的值是否相等即可快速完成验证
                #. 采用本地验证，服务需要实现 VanasPyHelper.wraps.token.VerifyTokenLocal 抽象类中的 verify 函数
    """

    def decorate(func):
        def inner(*args, **kwargs):

            from flask import request
            from vanaspyhelper.util.request import E400, vanas_verify_token, render_json

            try:
                _access_token = request.headers['access_token']
                _client_id = request.headers['client_id']

                # 如果需要本地验证，并且本地验证成功. 直接返回函数结果。 避免反复与 token server 交互
                if __need_local_verify(ins) and ins.verify(client_id=_client_id,access_token=_access_token):
                    # 返回函数返回值
                    return func(*args, **kwargs)

                # 不需要本地验证 或 本地验证失败，采用服务器验证
                _verify_token_result = vanas_verify_token(client_id=_client_id,access_token=_access_token)
                if not __isTokenSuccess(_verify_token_result):
                    # 服务器验证失败 , 以 json 数据代替被修饰的函数返回值返回给请求方
                    return render_json(_verify_token_result)

                # 服务器验证成功， 如果需要本地验证，则代表 access_token 已改变，通知客户端修改
                if __need_local_verify(ins):
                    ins.upgrade(client_id=_client_id, access_token=_access_token)

                # 返回函数返回值
                return func(*args, **kwargs)

            except KeyError:
                # 参数不对，请求没带Token
                return E400("请求 Header 中没有 access_token 和 client_id", code=3001)
        return inner
    return decorate


# def token_required(func):
#     """
#     # 验证token
#     :param func:
#     :return:
#     """
#
#     @functools.wraps(func)
#     def verify_token(*args, **kwargs):
#
#         from flask import request
#         from vanaspyhelper.util.request import E400, vanas_verify_token, render_json
#
#         try:
#             token = request.headers['access_token']
#             client_id = request.headers['client_id']
#
#             # 验证 token
#             verify_token_res = vanas_verify_token(token, client_id)
#
#             if not isTokenSuccess(verify_token_res):
#                 return render_json(verify_token_res)
#
#             return func(*args, **kwargs)
#
#         # 参数不对，请求没带Token
#         except KeyError:
#             return E400("请求 Header 中没有 access_token 和 client_id" , code=3001)
#
#     return verify_token


