# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : fileutil.py
# @Created  : 2020/11/2 7:09 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 文件相关帮助
# -------------------------------------------------------------------------------

import os,yaml
from PIL import Image

def makeDir(dirPath , exist_ok=False):
    """
    创建目录
    :param dirPath: 文件夹路径【绝对路径】 从第一级之后用/分割
    :param exist_ok: 避免多线程执行时，创建文件夹错误 <br>
                    exist_ok False 默认值，创建时如果目标目录存在 抛出 FileExistsError <br>
                    exist_ok True 默认值，创建时如果目标目录存在,不抛出异常
    :return:
    """
    if not os.path.exists(dirPath):
        return os.makedirs(dirPath,exist_ok=exist_ok)

def fileExist(filename):
    """
    文件是否存在
    :param filename: 文件路径
    :return: 存在返回 True 不存在返回 False
    """
    return os.path.isfile(filename)

def saveFile(dirPath:str , filename:str, data):
    """
    保存文件
    :param dirPath: 文件夹路径【绝对路径】 ，从第一级之后用/分割
    :param filename: 文件名称
    :param data: 文件要写入的内容
    :return:
    """
    if not os.path.exists(dirPath):
        makeDir(dirPath,True)
    fn = os.path.join(dirPath, filename)
    with open(fn, 'wb') as f:
        f.write(data)
        f.close()
    return fn

def removeFile(filePath):
    """
    删除文件
    :param filePath:
    :return:
    """
    try:
        if os.path.exists(filePath):
            os.remove(filePath)
    except:
        print("删除文件错误! {} ".format(filePath))

def isImageBroke(image_path:str):
    """
    图片是否损坏
    :param image_path: 图片路径
    :return: 损坏:True, 未损坏:False
    """
    valid = False
    try:
        img = Image.open(image_path).load()
    except OSError:
        valid = True
    return valid

def openYaml(path:str, encoding:str='utf-8')->dict:
    """
    读取 yaml 配置
    :param path: 文件路径
    :param encoding: 字符集 默认 utf-8
    :return:
    """
    with open(path, 'r', encoding=encoding) as f:
        try:
            cfg = f.read()
            # 转化成字典数据
            cfg_d = yaml.load(cfg , Loader=yaml.FullLoader)
            return cfg_d
        finally:
            f.close()