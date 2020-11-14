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


import time,uuid,hashlib


def get_uuid(key=None):
    """
    生成UUID
    :param key: 默认空 按照UUID-1方式生成,如果有值，者按照UUID-3规则生成。但是前提业务需保证key具有唯一性，如手机号
    :return:
    """

    '''
        Python uuid 5种算法
        1、uuid1()——基于时间戳
               由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性，
               但MAC的使用同时带来安全性问题，局域网中可以使用IP来代替MAC。
        2、uuid2()——基于分布式计算环境DCE（Python中没有这个函数）
                算法与uuid1相同，不同的是把时间戳的前4位置换为POSIX的UID。
                实际中很少用到该方法。
        3、uuid3()——基于名字的MD5散列值
                通过计算名字和命名空间的MD5散列值得到，保证了同一命名空间中不同名字的唯一性，
                和不同命名空间的唯一性，但同一命名空间的同一名字生成相同的uuid。
        4、uuid4()——基于随机数
                由伪随机数得到，有一定的重复概率，该概率可以计算出来。
        5、uuid5()——基于名字的SHA-1散列值
                算法与uuid3相同，不同的是使用 Secure Hash Algorithm 1 算法

        使用方面（官方建议）：

            首先，Python中没有基于DCE的，所以uuid2可以忽略；
            其次，uuid4存在概率性重复，由无映射性，最好不用；
            再次，若在Global的分布式计算环境下，最好用uuid1；
            最后，若有名字的唯一性要求，最好用uuid3或uuid5。
    '''
    if key is None:
        return str(uuid.uuid1()).upper()
    else:
        return str(uuid.uuid3(uuid.NAMESPACE_DNS,key)).upper()

def md5(str,upper=True):
    """
    转MD5
    :param str: 要转的字符串
    :param upper: 默认True 转大写
    :return:
    """
    m5 = hashlib.md5(str.encode("utf8"))
    m5str = m5.hexdigest()
    if upper:
        return m5str.upper()
    return m5str

def index_of(source_str:str, target_str:str):
    """
    在字符串中查找字符
    :param source_str: 字符串
    :param target_str: 查找字符
    :return:
    """
    try:
        start_index = source_str.index(target_str)
        return start_index + len(target_str)
    except:
        return -1

def get_time(format:str="%Y-%m-%d %H:%M:%S"):
    """
    获取时间字符串
    :param format: 格式化 ，默认 %Y-%m-%d %H:%M:%S 即 YYYY-MM-DD HH24:mi:ss
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_timestamp()->int:
    """
    获取当前时间戳
    :return:
    """
    return int(time.time())

def ascii_hex(len:int=16):
    """
    :param len: 2 的倍数
    :return: bytes
    """
    import os,binascii
    return binascii.hexlify(os.urandom(len))

def ascii_hex_str(len:int=16, encoding:str="utf-8"):
    """
    :param len: 2 的倍数
    :return: str
    """
    data = ascii_hex(len)
    data = str(data, encoding=encoding)
    return data