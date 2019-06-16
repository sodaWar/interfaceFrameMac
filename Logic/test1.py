# from Logic.log_print import LogPrint
# from Common.excel_pub import ExcelDeal
# from Common.method_pub import CommonMethod
# from Config.read_config import DealCommonCfg
# from Common.interface_deal_alone import InterfaceDealAlone
# from Logic.pressure_test import PressureTest
# from pyDes import *
# import importlib
# import threading
# import multiprocessing
# import urllib
# import json
# import random
import pymysql
# import traceback
# from Common.mysql_pub import MysqlDeal
# from Common.method_pub import CommonMethod
from Common.mysql_pub import MysqlDeal
# from Logic.interface_deal import InterfaceDeal
# from Common.method_pub import CommonMethod
# importlib.reload(sys)
# import requests
# import threading
# import time
#
#
#
# start_time = datetime.datetime.now()
# time.sleep(2)
# end_time = datetime.datetime.now()
#
#
# generate_html(title_content='http接口自动化测试报告',file_path='/Users/hongnaiwu/MyProject/InterfaceFrame/Report/report-20190425 17-58-21.html',
#            start_time=start_time, end_time=end_time, pass_num=5, fail_num=2, case_id=1, interface_name="接口测试",
#            key="dwqweq1213", request_data="{'password' : '123456'}", url='www.baidu.com',
#            request_method='post', assert_fail_reason='code', json='code = 500', test_result='fail', exception_num=0,
#            error_num=1)



#
# def chi(threadName,name):
#     print("%s 吃着%s开始：" % (time.ctime(),threadName))
#     print("%s 吃着火锅：涮羊肉" % time.ctime())
#     time.sleep(1)
#     time.sleep(1)
#     print("%s 吃着火锅：涮牛肉" % time.ctime())
#     time.sleep(1)
#     print("%s 吃着火锅：贡丸" % time.ctime())
#     time.sleep(1)
#     print("%s 吃着%s结束--" % (time.ctime(),threadName))
#     print("%s 运行结束！"%name)

#
# def ting(threadName):
#     print("%s 哼着%s1！" % (time.ctime(),threadName))
#     time.sleep(2)
#     print("%s 哼着小曲2！" % time.ctime())
#     time.sleep(2)
#     print("%s 哼着小曲3！" % time.ctime())
#     time.sleep(2)
#     print("%s 哼着小曲4！" % time.ctime())
#     time.sleep(2)
#     print("%s 哼着小曲5！" % time.ctime())
#     time.sleep(2)
#
# # 创建线程数组
# threads = []
# # 创建线程t1，并添加到线程数组
# # t1 = threading.Thread(target=chi, args=("火锅","吃火锅",))
#
# # 传kwargs参数
# t1 = threading.Thread(target=chi, kwargs={"threadName":"火锅","name":"吃火锅"})
#
# threads.append(t1)
# # 创建线程t2，并添加到线程数组
# for i in range(3):
#     t2 = threading.Thread(target=ting,args=("小曲",))
#     threads.append(t2)
#
# if __name__ == '__main__':
#     # 启动线程
#     for t in threads:
#         t.start()
#     length = len(threading.enumerate())  # 枚举返回个列表
#     print('当前运行的线程数为：%d'%length)

