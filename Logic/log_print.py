# coding=utf-8
import logging
import time
import os

# log_path是存放日志的路径
cur_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'Log')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)


class LogPrint:
    def __init__(self):
        # 文件的命名
        self.log_name = os.path.join(log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        """
        logging.getLogger(name)获取logger对象,如果不指定name则返回root对象,多次使用相同的name调用getLogger方法返回同一个logger对象
        这里获得logger对象,一个name代表一个Logger对象,函数中必须加上name,否则多线程请求接口时打印日志会重复,可能造成内存崩溃
        """
        self.logger = logging.getLogger(__name__)
        # self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 清空当前文件的logging 因为logging会包含所有的文件的logging
        logging.Logger.manager.loggerDict.pop(__name__)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        # fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


# class logPrint:
#     def dealLog(self):
#         # log_path是存放日志的路径
#         cur_path = os.path.dirname(os.path.realpath(__file__))
#         log_path = os.path.join(os.path.dirname(cur_path), 'Log')
#         # 如果不存在这个logs文件夹，就自动创建一个
#         if not os.path.exists(log_path):os.mkdir(log_path)
#
#         logname = os.path.join(log_path, '%s.log'%time.strftime('%Y_%m_%d'))
# 指定日志输出的格式和内容,format可以输出很多有用的信息,asctime是打印日志的时间,levelname是打印日志级别名称,message是打印日志信息
#         log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
#         logging.basicConfig(format=log_format, filename=logname, filemode='w', level=logging.DEBUG)
#       # 定义一个StreamHandler，将INFO级别或debug级别或者更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象,logging有一个日志处理的主对象，其它处理方式都是通过addHandler添加进去的
#         console = logging.StreamHandler()
#         console.setLevel(logging.DEBUG)
#         # console.setLevel(logging.INFO)
#         formatter = logging.Formatter(log_format)
#         console.setFormatter(formatter)
#         logging.getLogger('').addHandler(console)


# 查看注释对每个语句的解释即可
# import logging
# import os
# import time
#
#
# class Log:
#
#     def __init__(self):
#         cur_path = os.path.dirname(os.path.realpath(__file__))
#         log_path = os.path.join(os.path.dirname(cur_path), 'Log')
#         self.logger = logging.getLogger(__name__)
#
#         # 以下三行为清空上次文件
#
#         # 这为清空当前文件的logging 因为logging会包含所有的文件的logging
#
#         logging.Logger.manager.loggerDict.pop(__name__)
#
#         # 将当前文件的handlers 清空
#
#         self.logger.handlers = []
#
#         # 然后再次移除当前文件logging配置
#
#         self.logger.removeHandler(self.logger.handlers)
#
#         #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
#
#         if not self.logger.handlers:
#             # loggger 文件配置路径
#
#             self.log_name = os.path.join(log_path, '%s.log' % time.strftime('%Y_%m_%d'))
#             self.handler = logging.FileHandler(self.log_name, 'a')
#
#             # self.handler = logging.FileHandler(
#             #     os.getcwd() + '/logger/%s_log/%s_score.log' % (str(dt.date.today()), str(dt.date.today())))
#
#             # logger 配置等级
#
#             self.logger.setLevel(logging.DEBUG)
#             # logger 输出格式
#
#             formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
#
#             # 添加输出格式进入handler
#
#             self.handler.setFormatter(formatter)
#
#             # 添加文件设置金如handler
#
#             self.logger.addHandler(self.handler)
#
#         # 以下皆为重写方法 并且每次记录后清除logger
#
#     def info(self, message=None):
#         self.__init__()
#
#         self.logger.info(message)
#
#         self.logger.removeHandler(self.logger.handlers)
#
#     def debug(self, message=None):
#         self.__init__()
#
#         self.logger.debug(message)
#
#         self.logger.removeHandler(self.logger.handlers)
#
#     def warning(self, message=None):
#         self.__init__()
#
#         self.logger.warning(message)
#
#         self.logger.removeHandler(self.logger.handlers)
#
#     def error(self, message=None):
#         self.__init__()
#
#         self.logger.error(message)
#
#         self.logger.removeHandler(self.logger.handlers)
#
#     def critical(self, message=None):
#         self.__init__()
#
#         self.logger.critical(message)
#
#         self.logger.removeHandler(self.logger.handlers)
