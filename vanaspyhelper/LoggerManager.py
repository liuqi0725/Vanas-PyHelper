# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : LoggerConf.py
# @Created  : 2020/11/3 2:28 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 统一日志
# -------------------------------------------------------------------------------


import logging
from logging import handlers
from .util.file import makeDir
import os

# 模板样例
# "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"
# 2020-11-03 14:35:56,008 - /Users/alexliu/DEV/Python-DEV/VanasHMSpider/hmspider/core/LoggerConf.py[line:58] - ERROR: error hello

# [%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(name)s][%(levelname)s] %(message)s
# [2020-11-03 14:39:15,935] [LoggerConf.py] [line:59] [DEFAULT_LOG][ERROR] error hello

# [%(asctime)s] - %(pathname)s  [line:%(lineno)d] - %(levelname)s: %(message)s

# 日志输出
class Logger(object):

    # 日志级别关系映射
    level_relations = {
        "notset": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "fatal": logging.FATAL,
        "critical": logging.CRITICAL
    }

    def __init__(self, logdir:str, logname="DEFAULT_LOG", level="info", when="D",interval=1, backupCount=3,log_prefix:str=None,
                 fmt="[%(asctime)s] - %(pathname)s  [%(thread)d] [line:%(lineno)d] - %(levelname)s: %(message)s"):
        """
        创建日志
        :param logdir:  日志保存 dir 路径
        :param logname: 日志名称，可以 new 多个 Logger，名称不一样，区分日志内容,通常是 <app-name>.<module-name> 的形式 默认：DEFAULT_LOG
        :param level:   日志级别 由高到低 CRITICAL,FATAL,ERROR,WARNING,INFO,DEBUG,NOTSET 默认：INFO
        :param when:    日志文件-间隔单位 :  S:秒 , M:分 , H:时, D:天 , W0-W6:周一至周日 , midnight: 每天的凌晨 。与间隔时间interval 配合使用
        :param when:    日志文件-间隔时间 :  默认 1 与 when 配合使用，比如 when=D interval=1 代表每1 天 重新写一个新日志文件
        :param backupCount: 日文件保留数量，超过该数量其他日志丢弃
        :param fmt:     日志输出格式
        """

        self.logdir = logdir
        self.logname = logname
        self.level = level
        self.when = when
        self.interval = interval
        self.backupCount = backupCount
        self.log_prefix = log_prefix

        # 初始化 log 目录
        self._init_logpath()

        # 设置日志输出格式
        self.format_str = logging.Formatter(fmt)

        # 创建日志对象
        self.logger = logging.getLogger(logname)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))

        # 初始化 handler
        self._init_console_logHandler()
        self._init_file_logHandler()

    def _init_logpath(self):
        """
        初始化 logfile ，创建目录
        :return:
        """
        # 创建日志文件夹
        try:
            makeDir(self.logdir)
        except:
            raise

    def _init_console_logHandler(self):
        """
        初始化控制台日志
        :return:
        """
        # 设置日志在控制台输出
        streamHandler = logging.StreamHandler()
        # 设置控制台中输出日志格式
        streamHandler.setFormatter(self.format_str)

        # 将输出对象添加到logger中
        self.logger.addHandler(streamHandler)

    def _init_file_logHandler(self):
        """
        初始化输出文件日志
        :return:
        """

        if self.log_prefix is None:
            all_filename,error_filename = "all.log","error.log"
        else:
            all_filename,error_filename = "{}-all.log".format(str(self.log_prefix)),"{}-error.log".format(str(self.log_prefix))


        # 定义 2 个 handler
        # 输出 用户定义的级别以上的日志
        all_filename = os.path.join(self.logdir, all_filename)
        # 输出 error 以上级别的日志
        err_filename = os.path.join(self.logdir, error_filename)

        # 设置日志输出到文件（指定间隔时间自动生成文件的处理器  --按日生成）
        # filename：日志文件名，interval：时间间隔，when：间隔的时间单位， backupCount：备份文件个数，若超过这个数就会自动删除
        all_fileHandler = handlers.TimedRotatingFileHandler(filename=all_filename, when=self.when, interval=self.interval,
                                                        backupCount=self.backupCount, encoding="utf-8")
        # 设置日志文件中的输出格式
        all_fileHandler.setFormatter(self.format_str)


        error_fileHandler = handlers.TimedRotatingFileHandler(filename=err_filename, when=self.when, interval=self.interval,
                                                             backupCount=self.backupCount, encoding="utf-8")
        # 设置日志文件中的输出格式
        error_fileHandler.setFormatter(self.format_str)
        error_fileHandler.setLevel(self.level_relations.get("error"))

        # 将输出对象添加到logger中
        self.logger.addHandler(all_fileHandler)
        self.logger.addHandler(error_fileHandler)

    def getLogger(self):
        return self.logger

global log

# 定义全局日志对象
def init_global_logger(logdir:str , logname="DEFAULT_LOG", level="info" , log_prefix:str=None):
    global log
    log = Logger(logdir, logname=logname , level=level , log_prefix=log_prefix).getLogger()
