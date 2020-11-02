# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : crypto.py
# @Created  : 2020/11/2 7:29 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 加密解密
# -------------------------------------------------------------------------------

from Crypto.Cipher import AES,DES3
import binascii


class DESTool():

    key = '1234567890!@#$%^'

    def __init__(self, key=None , iv=None):
        """
        :param key: 秘钥
        :param iv: 值必须是8位
        """

        if key is None:
            key = '1234567890!@#$%^'

        if iv is None:
            iv = '1234ABCD'

        self.key = key
        self.iv = iv


    def encrypt(self, text):
        """
        加密
        :param text: 内容
        :return:
        """
        des = DES3.new(self.key, DES3.MODE_OFB, self.iv)
        # 密文生成器，采用MODE_OFB加密模式
        encrypt_str = des.encrypt(text)
        # 附加上iv值是为了在解密时找到在加密时用到的随机iv,加密的密文必须是八字节的整数倍，最后部分
        # 不足八字节的，需要补位
        encrypt_str = binascii.b2a_hex(encrypt_str)  # 将二进制密文转换为16进制显示
        encrypt_data = str(encrypt_str, encoding="utf-8")
        return encrypt_data

    def decrypt(self, text):
        """
        解密
        :param text: 内容
        :return:
        """
        des = DES3.new(self.key, DES3.MODE_OFB, self.iv)
        encrypt_byte = binascii.a2b_hex(text) # 转化成 byte
        encrypt_data = des.decrypt(encrypt_byte)  # 后八位是真正的密文
        decrypt_data = str(encrypt_data, encoding="utf-8")
        return decrypt_data


class AESTool():
    # 密钥（key）, 密斯偏移量（iv） CBC模式加密

    def __init__(self , block_size:int=16 , key=None , iv:str=None):
        """
        :param block_size: 长度
        :param key: 秘钥
        :param iv: 偏移量 16 位
        """
        self.pad = lambda s: s + (block_size - len(s) % block_size) * \
                    chr(block_size - len(s) % block_size)

        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

        if key is None:
            key = '1234567890!@#$%^'

        if iv is None:
            iv = '0102030405060708'

        self.key = key
        self.iv = iv

    def encrypt(self, data):
        """
        加密
        :param data:
        :return:
        """
        data = self.pad(data)
        # 字符串补位
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.iv.encode('utf8'))
        encrypt_bytes = cipher.encrypt(data.encode('utf8'))

        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        # base64 有特殊符号
        # encrypt_str = base64.b64encode(encrypt_bytes)
        # 对byte字符串按utf-8进行解码
        # result = encrypt_str.decode('utf8')

        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        encrypt_str = binascii.b2a_hex(encrypt_bytes)  # 将二进制密文转换为16进制显示
        result = str(encrypt_str, encoding="utf-8")
        return result

    def decrypt(self, data):
        """
        解密
        :param data:
        :return:
        """
        data = data.encode('utf8')

        # 转化为 byte
        # base64 有特殊符号
        # encrypt_bytes = base64.decodebytes(data)

        encrypt_bytes = binascii.a2b_hex(data)

        # 将加密数据转换位bytes类型数据
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.iv.encode('utf8'))
        text_decrypted = cipher.decrypt(encrypt_bytes)
        # 去补位
        text_decrypted = self.unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted