# coding=utf-8
from Logic.mail_send import MailSend
from Logic.log_print import LogPrint
from Common.interface_header_pub import InterfaceHeadDeal
from Common.mysql_pub import MysqlDeal
import json
import requests
import datetime
import os
from pyDes import *
from requests.exceptions import Timeout
reload(sys)
# 编码转换,转换之后默认编码格式是utf8,详细见笔记
sys.setdefaultencoding('utf8')


class InterfaceDeal:
    md = MysqlDeal()
    conn, cur = md.conn_db()
    global_temp = ''

    def __init__(self, num, api_purpose, api_host, request_url, request_method, request_data_type, request_data,
                 check_point, test_describe):
        self.num = num                                          # 用例编号
        self.api_purpose = api_purpose                          # 接口名称
        self.api_host = api_host                                # 接口域名
        self.request_url = request_url                          # 接口地址
        self.request_method = request_method                    # 请求方法
        self.request_data_type = request_data_type              # 请求数据类型
        self.request_data = request_data                        # 请求数据
        self.check_point = check_point                          # 断言内容
        self.test_describe = test_describe                      # 测试描述

    # 接口调用函数
    def interface_test(self):
        if self.request_method == 'POST' and self.request_data_type != 'File':
            global_two = self.post_deal()
            return global_two
        elif self.request_method == 'GET':
            global_two = self.get_deal()
            return global_two
        elif self.request_data_type == 'File':
            self.request_type_file()
        else:
            print ''

    def post_deal(self):
        data = eval(self.request_data)  # 将str类型转换成字典类型
        payload = json.dumps(data)
        headers = InterfaceHeadDeal().sign_headers(payload, self.request_data_type)
        url = self.api_host + self.request_url
        LogPrint().info('----------------开始调用接口----------------：' + url)

        try:
            response = ''
            if self.request_data_type == "Data":
                response = requests.post(url=url, data=payload, headers=headers, timeout=5)
            elif self.request_data_type == 'Form':  # 以form形式发送post请求,只需将请求的参数构造成一个字典,传入给request.post()的data参数即可
                response = requests.post(url=url, data=data, timeout=5)

            status = response.status_code
            resp1 = response.text
            resp2 = resp1.encode("utf-8")

            global_one = self.common_code_one(status, resp2)
            return global_one

        except Timeout:
            global_one = self.common_code_two(url)
            return global_one

    def get_deal(self):
        url = self.api_host + self.request_url
        LogPrint().info('----------------开始调用接口----------------：' + url)
        try:
            response = requests.get(url=self.request_url, params=self.request_data, timeout=5)
            status = response.status_code
            resp1 = response.text
            resp2 = resp1.encode("utf-8")
            # resp = response.read()

            global_one = self.common_code_one(status, resp2)
            return global_one

        except Timeout:
            global_one = self.common_code_two(url)
            return global_one

    def request_type_file(self):
        data_file = self.request_data
        if not os.path.exists(data_file):
            LogPrint().error(str(self.num) + ' ' + self.api_purpose + ' 文件路径配置无效，请检查[Request Data]字段配置的文件路径是否存在！！！')
        f_open = open(data_file, 'rb')
        # data = f_open.read()
        f_open.close()
        # request_data = '''
        return self.request_data_type

    # 公共函数
    def common_code_one(self, status, resp2):
        sql = self.sql_deal_one()
        if status == 200:
            LogPrint().info('----------------返回结果成功----------------：' + resp2)
            if self.check_point in resp2:
                LogPrint().info('----------------测试断言结果----------------：' + '第' + str(self.num) + '个测试用例断言：通过')
                global_temp = 'success'
            else:
                LogPrint().info('----------------测试断言结果----------------：' + '第' + str(self.num) + '个测试用例断言：失败')
                self.md.other_operate_db(self.conn, self.cur, sql)
                global_temp = 'fail'

        else:
            LogPrint().error('----------------返回结果失败----------------：' + '第' + str(self.num) +
                             '个测试用例的接口请求失败!! [ ' + str(status) + ' ], ' + resp2)
            global_temp = 'error'
            self.md.other_operate_db(self.conn, self.cur, sql)
        return global_temp

    def common_code_two(self, url):
        LogPrint().error('----------------返回结果失败----------------：' + '第' + str(self.num) +
                         '个测试用例的接口请求超时响应,请注意!! [ ' + url + ' ]')
        global_temp = 'error'
        # 测试结果失败的用例信息存入数据库
        sql = self.sql_deal_one()
        self.md.other_operate_db(self.conn, self.cur, sql)

        mail_title = '接口响应超时: ' + self.api_purpose + ':' + url
        MailSend().overtime_warn(mail_title)
        return global_temp

    def sql_deal_one(self):
        url = self.api_host + self.request_url

        create_time = datetime.datetime.now()
        my_one = '\"'
        if my_one in str(self.request_data):
            # 这里接口请求的参数中包含"符号,需要将这个符号转义,这里r的意思是原始字符串,r'\"'的意思就是\"的字符,不是转义的意思
            my_two = "\'" + str(self.request_data).replace(my_one, r'\"') + "\'"
        else:
            my_two = "\'" + str(self.request_data) + "\'"

        if my_one in str(self.check_point):
            my_three = "\'" + str(self.check_point).replace(my_one, r'\"') + "\'"
        else:
            my_three = "\'" + str(self.request_data) + "\'"

        # 这里需要将参数都加上''符号,不然在sql语句中不是string类型,如请求方法时post,在sql中需要变为'post'才正确
        sql = "insert into test_problem_case(case_id,request_method,request_data_type,interface_name,url," \
              "request_data,assert_fail_reason,create_time,test_describe) " \
              "values(%d,%s,%s,%s,%s,%s,%s,%s,%s)" % \
              (int(self.num), "\'" + self.request_method + "\'", "\'" + self.request_data_type + "\'", "\'" +
               self.api_purpose + "\'", "\'" + url + "\'", my_two, my_three,
               "\'" + str(create_time) + "\'", "\'" + self.test_describe + "\'")
        return sql


