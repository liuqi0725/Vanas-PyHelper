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


def isTokenSuccess(verify_token_res:dict):
    """
    验证 token 是否合法
    :param verify_token_res:
    :return:
    """
    if verify_token_res["success"] == int(False):
        return False
    return True

def token_required(func):
    """
    # 验证token
    :param func:
    :return:
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):

        from flask import request
        from vanaspyhelper.util.request import E400, vanas_verify_token, render_json

        try:
            token = request.headers['access_token']
            client_id = request.headers['client_id']

            # 验证 token
            verify_token_res = vanas_verify_token(token, client_id)

            if not isTokenSuccess(verify_token_res):
                return render_json(verify_token_res)

            return func(*args, **kwargs)

        # 参数不对，请求没带Token
        except KeyError:
            return E400("请求 Header 中没有 access_token 和 client_id" , code=3001)

    return inner