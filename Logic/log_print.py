# coding=utf-8
import logging,time
import os

# class logPrint:
#     def dealLog(self):
#         # log_path是存放日志的路径
#         cur_path = os.path.dirname(os.path.realpath(__file__))
#         log_path = os.path.join(os.path.dirname(cur_path), 'Log')
#         # 如果不存在这个logs文件夹，就自动创建一个
#         if not os.path.exists(log_path):os.mkdir(log_path)
#
#         logname = os.path.join(log_path, '%s.log'%time.strftime('%Y_%m_%d'))
#
#         log_format = '[%(asctime)s] [%(levelname)s] %(message)s'  # 指定日志输出的格式和内容,format可以输出很多有用的信息,asctime是打印日志的时间,levelname是打印日志级别名称,message是打印日志信息
#         logging.basicConfig(format=log_format, filename=logname, filemode='w', level=logging.DEBUG)
#         # 定义一个StreamHandler，将INFO级别或debug级别或者更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象,logging有一个日志处理的主对象，其它处理方式都是通过addHandler添加进去的
#         console = logging.StreamHandler()
#         console.setLevel(logging.DEBUG)
#         # console.setLevel(logging.INFO)
#         formatter = logging.Formatter(log_format)
#         console.setFormatter(formatter)
#         logging.getLogger('').addHandler(console)

# log_path是存放日志的路径
cur_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'Log')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):os.mkdir(log_path)


class LogPrint():
    def __init__(self):
        # 文件的命名
        self.logname = os.path.join(log_path, '%s.log'%time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a')  # 追加模式  这个是python2的
        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
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

