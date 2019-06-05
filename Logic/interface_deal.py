# coding=utf-8
from Logic.mail_send import MailSend
from Logic.log_print import LogPrint
from Common.interface_header_pub import InterfaceHeadDeal
from Common.method_pub import CommonMethod
from Common.mysql_pub import MysqlDeal
import json
import requests
import datetime
import os
from pyDes import *
from Config.read_config import DealCommonCfg
from requests.exceptions import Timeout
import importlib
importlib.reload(sys)


class InterfaceDeal:
    # s = requests.session()
    # s.keep_alive = False  # 关闭多余连接

    md = MysqlDeal()
    conn, cur = md.conn_db()

    dcc = DealCommonCfg()
    my_list = dcc.read_config('operating_environment')          # 获得配置文件中的信息内容
    my_dic = {}                                                 # 将获得的内容转换为字典类型
    for i in my_list:
        my_dic[i[0]] = i[1]
    host = my_dic['one_test_host']

    assert_result = ''                                          # 接口请求返回的数据断言后的结果,三种类型success、false、error
    response_last = ''                                          # 接口请求的最后结果,需要存储到数据库中的response字段的值

    def __init__(self, num, api_purpose, request_url, request_method, request_data_type, request_data,
                 check_point, test_describe, relevance_case):
        self.num = num                                          # 用例编号
        self.api_purpose = api_purpose                          # 接口名称
        self.api_host = self.host                               # 接口域名
        self.request_url = request_url                          # 接口地址
        self.request_method = request_method                    # 请求方法
        self.request_data_type = request_data_type              # 请求数据类型
        self.request_data = request_data                        # 请求数据
        self.check_point = check_point                          # 断言内容
        self.test_describe = test_describe                      # 测试描述
        self.relevance_case = relevance_case                    # 关联用例

    # 接口调用函数
    def interface_test(self):
        if self.request_method == 'POST' and self.request_data_type != 'File':
            assert_result = self.post_deal()
            return assert_result, self.response_last
        elif self.request_method == 'GET':
            assert_result = self.get_deal()
            return assert_result, self.response_last
        elif self.request_data_type == 'File':
            self.request_type_file()
        else:
            LogPrint().info("----------------请求方法或类型有误----------------")

    def post_deal(self):
        data = eval(self.request_data)                                                            # 将str类型转换成字典类型
        payload = json.dumps(data)
        headers = InterfaceHeadDeal().sign_headers(payload, self.request_data_type)
        url = self.api_host + self.request_url
        LogPrint().info('-------------调用第' + self.num + '个测试用例的接口-------------：' + url)

        try:
            response = ''
            if self.request_data_type == "Data":
                response = requests.post(url=url, data=payload, headers=headers, timeout=5)
            elif self.request_data_type == 'Form':  # 以form形式发送post请求,只需将请求的参数构造成一个字典,传入给request.post()的data参数即可
                response = requests.post(url=url, data=data, timeout=5)

            status = response.status_code
            resp1 = response.text.encode("utf-8")

            # 对接口返回的数据进行处理,如结果中存在转义字符需要存储到数据库中,则需要进行数据的相应处理
            resp2 = CommonMethod.response_data_deal(resp1)
            assert_result = self.common_code_one(status, resp2)
            self.response_last = resp2
            return assert_result

        except Timeout:
            assert_result = self.common_code_two(url)
            self.response_last = "null"
            return assert_result

    def get_deal(self):
        url = self.api_host + self.request_url
        LogPrint().info('-------------开始调用第' + self.num + '个测试用例的接口-------------：' + url)
        try:
            response = requests.get(url=url, params=self.request_data, timeout=5)
            status = response.status_code
            resp1 = response.text.encode("utf-8")
            # resp = response.read()

            if type(resp1 == "bytes"):
                resp1 = str(resp1, encoding="utf-8")
            assert_result = self.common_code_one(status, resp1)
            return assert_result

        except Timeout:
            assert_result = self.common_code_two(url)
            return assert_result

    def request_type_file(self):
        data_file = self.request_data
        if not os.path.exists(data_file):
            LogPrint().error(str(self.num) + ' ' + self.api_purpose + ' 文件路径配置无效，请检查[Request Data]字段配置的文件路径是否存在！！！')
        f_open = open(data_file, 'rb')
        # data = f_open.read()
        f_open.close()
        # request_data = '''
        return self.request_data_type

    # 公共函数,主要用于结果判断和处理
    def common_code_one(self, status, resp):
        sql = self.sql_deal('fail', resp)
        if status == 200:
            LogPrint().info('----------------返回结果成功----------------：' + resp)
            if self.check_point in resp:
                LogPrint().info('----------------测试断言结果----------------：' + '第' + str(self.num) + '个测试用例断言：通过')
                sql = self.sql_deal('success', resp)
                self.md.other_operate_db(self.conn, self.cur, sql)
                assert_result = 'success'
            else:
                LogPrint().info('----------------测试断言结果----------------：' + '第' + str(self.num) + '个测试用例断言：失败')
                self.md.other_operate_db(self.conn, self.cur, sql)
                assert_result = 'fail'

        else:
            LogPrint().error('----------------返回结果失败----------------：' + '第' + str(self.num) +
                             '个测试用例的接口请求失败!! [ ' + str(status) + ' ], ' + resp)
            assert_result = 'error'
            self.md.other_operate_db(self.conn, self.cur, sql)
        return assert_result

    def common_code_two(self, url):
        LogPrint().error('----------------返回结果失败----------------：' + '第' + str(self.num) +
                         '个测试用例的接口请求超时响应,请注意!! [ ' + url + ' ]')
        assert_result = 'error'
        # 测试结果失败的用例信息存入数据库
        sql = self.sql_deal('fail', ' ')
        self.md.other_operate_db(self.conn, self.cur, sql)

        mail_title = '接口响应超时: ' + self.api_purpose + ':' + url
        MailSend().overtime_warn(mail_title)
        return assert_result

    def sql_deal(self, result, response):
        # 如果请求的接口关联用例的值不为空,则需要从数据库中查询该关联的用例url值, A接口关联B接口后,因为A执行之前其关联的B用例接口一定执行了,所以直接从数据库中查找即可
        if int(self.relevance_case) != 0:
            sql_two = 'select url from test_case where case_id = %d order by create_time desc ' \
                      'limit 1' % int(self.relevance_case)
            result = self.md.select_db(self.cur, sql_two)
            relevance_case_url = result[0][0]               # 所关联的接口的url值,需要存储到数据库中relevance_case_url字段的值
        else:
            relevance_case_url = ""

        url = self.api_host + self.request_url

        create_time = datetime.datetime.now()
        center_temp = '\"'
        if center_temp in str(self.request_data):
            # 这里接口请求的参数中包含"符号,需要将这个符号转义,这里r的意思是原始字符串,r'\"'的意思就是\"的字符,不是转义的意思
            request_data_last = "\'" + str(self.request_data).replace(center_temp, r'\"') + "\'"
        else:
            request_data_last = "\'" + str(self.request_data) + "\'"

        if center_temp in str(self.check_point):
            check_point_last = "\'" + str(self.check_point).replace(center_temp, r'\"') + "\'"
        else:
            check_point_last = "\'" + str(self.request_data) + "\'"

        if result == 'success':
            status = 0
        else:
            status = 1
        # 这里需要将参数都加上''符号,不然在sql语句中不是string类型,如请求方法时post,在sql中需要变为'post'才正确
        sql = "insert into test_case(case_id,request_method,request_data_type,interface_name,url," \
              "request_data,assert_fail_reason,test_describe,status,response,relevance_case_url,create_time) " \
              "values(%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
              (int(self.num), "\'" + self.request_method + "\'", "\'" + self.request_data_type + "\'", "\'" +
               self.api_purpose + "\'", "\'" + url + "\'", request_data_last, check_point_last, "\'" +
               self.test_describe + "\'", status, "\'" + response + "\'", "\'" + relevance_case_url + "\'", "\'" +
               str(create_time) + "\'")
        return sql

