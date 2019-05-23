# # -*- coding:utf-8 -*-
# # import requests
# #
# # payload = {"name": "hongnaiwu", "age": "26"}
# #
# # ret = requests.get(url='http://httpbin.org/get', params=payload, timeout=5)
# #
# # # ret = requests.get("http://httpbin.org/get", params=payload)
# # print(ret.text)
import os
import time
import datetime
from Logic.test2 import generate_html
from Common.mysql_pub import MysqlDeal
import sys
import importlib
importlib.reload(sys)


# start_time = datetime.datetime.now()
# time.sleep(2)
# end_time = datetime.datetime.now()
#
#
# generate_html(title_content='http接口自动化测试报告',file_path='E:\\MyProgram\\InterfaceTestFrame\\Report\\report-20190425 17-58-21.html',
#            start_time=start_time, end_time=end_time, pass_num=5, fail_num=2, case_id=1, interface_name="接口测试",
#            key="dwqweq1213", request_data="{'password' : '123456'}", url='www.baidu.com',
#            request_method='post', assert_fail_reason='code', json='code = 500', test_result='fail', exception_num=0,
#            error_num=1)

print(4)