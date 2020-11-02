# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : utils.py
# @Created  : 2020/10/23 6:00 下午
# @Software : PyCharm
#
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
#
# @Desc     : 工具类
# -------------------------------------------------------------------------------

from werkzeug.exceptions import HTTPException
from flask import abort,jsonify
import yaml,time,enum

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


def get_timestamp()->int:
    """
    获取当前时间戳
    :return:
    """
    return int(time.time())


def openYaml(path:str):
    """
    读取 yaml 文件
    :param path:
    :return:
    """
    with open(path, 'r') as f:
        temp = yaml.load(f.read(), Loader=yaml.FullLoader)
        return temp
