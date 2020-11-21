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

import functools
from abc import ABCMeta,ABC,abstractmethod

from vanaspyhelper.error.RequestError import WrongLocalVerifyTokenInsError


def isTokenSuccess(verify_token_res:dict):
    """
    验证 token 是否合法
    :param verify_token_res:
    :return:
    """
    if verify_token_res["success"] == int(False):
        return False
    return True

class VerifyTokenLocal(ABC):

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

def token_required(local_verify_token_ins:VerifyTokenLocal=None):

    """验证 token 的装饰器

        args :
            local_verify_token_ins: 本地验证实现类实例

                #. 默认 None ， 通过 vanas-token 服务器验证
                #. 本地验证是为了避免少的与 vanas-token 服务器的交互所采用的方式
                #. 本地验证可以通过数据库，缓存对比一段时间内 access_token 的值是否相等即可快速完成验证
                #. 采用本地验证，服务需要实现 VanasPyHelper.wraps.token.VerifyTokenLocal 抽象类中的 verify 函数
    """

    def verify(func):
        def inner(*args, **kwargs):

            from flask import request
            from vanaspyhelper.util.request import E400, vanas_verify_token, render_json

            try:
                # token = request.headers['access_token']
                # client_id = request.headers['client_id']
                token = "11"
                client_id = "2"

                # 查看 redis 中是否有该访问 web 的 token，避免反复与 token 服务器交互
                if local_verify_token_ins is not None:

                    if not isinstance(local_verify_token_ins,VerifyTokenLocal):
                        raise WrongLocalVerifyTokenInsError(local_verify_token_ins)

                    # 本地验证成功，直接进入函数
                    if local_verify_token_ins.verify(client_id=client_id,access_token=token):
                        return func(*args, **kwargs)

                # 本地验证失败，采用服务器验证
                verify_token_res = vanas_verify_token(token, client_id)
                if not isTokenSuccess(verify_token_res):
                    return render_json(verify_token_res)

                # 通知本地 保存
                if local_verify_token_ins is not None:

                    if not isinstance(local_verify_token_ins,VerifyTokenLocal):
                        raise WrongLocalVerifyTokenInsError(local_verify_token_ins)

                    # 本地验证成功，通知本地 保存
                    if local_verify_token_ins.verify(token, client_id):
                        local_verify_token_ins.upgrade(client_id=client_id, access_token=token)

                return func(*args, **kwargs)

            # 参数不对，请求没带Token
            except KeyError:
                return E400("请求 Header 中没有 access_token 和 client_id", code=3001)
        return inner
    return verify


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


