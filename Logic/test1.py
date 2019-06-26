from Logic.log_print import LogPrint
from Common.excel_pub import ExcelDeal
from Common.method_pub import CommonMethod
from Config.read_config import DealCommonCfg
from Common.interface_deal_alone import InterfaceDealAlone
from Logic.pressure_test_run import PressureTest
from Logic.test2 import *
from pyDes import *
import importlib
import threading
import multiprocessing
import urllib
import json
import random
import datetime
import time
import pymysql
from Logic.pressure_test_run import PressureTest
import traceback
from Common.mysql_pub import MysqlDeal
from Common.method_pub import CommonMethod
from Common.mysql_pub import MysqlDeal
from Logic.interface_deal import InterfaceDeal
from Common.method_pub import CommonMethod
importlib.reload(sys)
import requests
import threading


start_time = datetime.datetime.now()
time.sleep(2)
end_time = datetime.datetime.now()


generate_html(title_content='http接口自动化测试报告',
              file_path='/Users/hongnaiwu/MyProject/InterfaceFrame/Report/report-20190425 17-58-21.html',
              start_time=start_time, end_time=end_time, pass_num=5, fail_num=2, case_id=1, interface_name="接口测试",
              key="dwqweq1213", request_data="{'password' : '123456'}", url='www.baidu.com',
              request_method='post', assert_fail_reason='code', json='code = 500', test_result='fail', exception_num=0,
              error_num=1)



