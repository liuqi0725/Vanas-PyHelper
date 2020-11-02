# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : spiderutils.py
# @Created  : 2020/11/2 6:54 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : request 相关工具包
# -------------------------------------------------------------------------------

import random,enum,json
import requests
from werkzeug.exceptions import HTTPException
from flask import abort,jsonify
from vanaspyhelper.error.RequestError import ProxyTypeNotSupport

__user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def get_user_agent(user_agent:list=None):
    """
    获取 User-Agent 随机获取一个
    :param user_agent: 自定义 user_agent list  默认 None ，从系统内置的 user_agent 中随机选择一个
    :return:
    """

    if not user_agent:
        return random.choice(user_agent)

    return random.choice(__user_agent_list)


def get_Proxy(ip:str="127.0.0.1", port:int=1080 , type:str="http"):
    """
    获取代理
    :param ip: 代理 ip 默认 127.0.0.1
    :param port:  代理端口， 默认 1080
    :param type:  代理类型， 默认 http,  备选项 socks5 。  https 启用代理均会添加
    :return:
    """
    proxies = {}

    if type.lower() == 'socks5':
        proxies['http'] = 'socks5://{}:{}'.format(ip,port)
        proxies['https'] = 'socks5://{}:{}'.format(ip,port)
    elif type.lower() == 'http':
        proxies['http'] = 'http://{}:{}'.format(ip,port)
        proxies['https'] = 'https://{}:{}'.format(ip,port)
    else:
        raise ProxyTypeNotSupport(type)

    return proxies


def E400(desc, code=400):
    """
    未知错误处理，并抛出到 error_handling 中
    :param desc: 错误信息
    :param code: 错误编码 默认 400
    :return:
    """
    exc = HTTPException()
    if isinstance(code,enum.Enum):
        exc.status_code = code.value
    else:
        exc.status_code = code
    exc.description = desc
    return error_handling(exc)

def error_handling(error):
    """
    统一错误处理
    :param error:
    :return: response
    """
    if isinstance(error, HTTPException):
        # 4xx ,5xx 错误
        result = json_res_failure(error.description , error.status_code , str(error))
    else:
        # 500 错误
        description = abort(500).mapping.description
        result = json_res_failure(description , 500 ,trace=str(error))

    # resp = jsonify(result)
    # resp.status_code = result['code']
    return render_json(result)

def render_json(jsonData):
    """
    提供给外部调用，返回 response
    :param jsonData: json 数据
    :return:
    """
    resp = jsonify(jsonData)
    if 'status_code' in jsonData:
        resp.status_code = jsonData['status_code']
    else:
        resp.status_code = 200
    return resp

def json_res_failure(desc:str,code,trace:str=""):
    """
    错误 json
    :param desc:
    :param code:
    :param trace:
    :return:
    """
    if isinstance(code,enum.Enum):
        code = code.value
    return __json_res(False,desc=desc,error_code=code , trace=trace)

def json_res_success(data:dict=None):
    """
    成功 json
    :param data:
    :return:
    """
    return __json_res(True,data=data)


def __json_res(success:bool,data:dict={},desc:str="",error_code:int=400, trace:str=""):
    """
    创建 api 通用 json 返回值
    :param desc: 说明 默认 None
    :param data: 返回数据 默认 None
    :param success: 成功与否
    :param error_code: 错误编码 默认 400
    :param trace: 错误信息 默认 None
    :return:
    """

    int_success = int(success)

    if success :
        result = {'success': int_success, 'data':data, 'description': desc}
    else:
        result = {'success': int_success, 'code': error_code, 'description': desc , 'trace': trace}

    return result


def vanas_get_token(client_id:str ,
                    client_secret:str,
                    url:str="https://token.35liuqi.com/oauth/token",
                    grant_type:str="client_credentials" , )->dict:
    """
    vanas 获取 token
    :param client_id: 客户端 id，固定值，由研发人员签发
    :param client_secret: 客户端 secret，由研发人员签发
    :param url:
    :param grant_type: client_credentials 或 password 推荐 client_credentials
    :return: 根据服务端 doc 返回
    """
    data = {'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret}
    response = requests.post(url,data)
    response.raise_for_status()
    if response is not None:
        return response.json()


def vanas_verify_token(access_token:str ,
                       client_id:str ,
                       url="https://token.35liuqi.com/verify_token")->dict:
    """
    vanas 验证 token
    :param access_token: token
    :param client_id: 客户端 id，固定值，由研发人员签发
    :param url:
    :return: 根据服务端 doc 返回
    """
    data = {'access_token':access_token,'client_id':client_id}
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    if response is not None:
        return response.json()