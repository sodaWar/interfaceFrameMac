# coding=utf-8
from Logic.mail_send import MailSend
from Logic.log_print import LogPrint
from Common.method_pub import CommonMethod
from Common.mysql_pub import MysqlDeal
import json
import requests
import datetime
from pyDes import *
from Config.read_config import DealCommonCfg
from requests.exceptions import Timeout
import importlib
importlib.reload(sys)


class PressureInterfaceDeal:

    md = MysqlDeal()
    conn, cur = md.conn_db()

    dcc = DealCommonCfg()
    my_list = dcc.read_config('operating_environment')          # 获得配置文件中的信息内容
    my_dic = {}                                                 # 将获得的内容转换为字典类型
    for i in my_list:
        my_dic[i[0]] = i[1]
    host = my_dic['one_test_host']

    assert_result = ''                                          # 接口请求返回的数据断言后的结果,三种类型success、fail、error
    response_last = ''                                          # 接口请求的最后结果,需要存储到数据库中的response字段的值

    def __init__(self, num, api_purpose, request_url, request_method, request_data_type, request_data,
                 check_point, pressure_test_file):
        self.num = num                                          # 用例编号
        self.api_purpose = api_purpose                          # 接口名称
        self.api_host = self.host                               # 接口域名
        self.request_url = request_url                          # 接口地址
        self.request_method = request_method                    # 请求方法
        self.request_data_type = request_data_type              # 请求数据类型
        self.request_data = request_data                        # 请求数据
        self.check_point = check_point                          # 断言内容
        self.pressure_test_file = pressure_test_file            # 用例参数所需的测试文件

    # 接口调用函数
    def p_interface_test(self):
        if self.request_method == 'POST' and self.request_data_type != 'File':
            assert_result = self.p_post_deal()
            return assert_result, self.response_last
        elif self.request_method == 'GET':
            assert_result = self.p_get_deal()
            return assert_result, self.response_last
        elif self.request_data_type == 'File':
            assert_result = self.p_post_deal()
            return assert_result, self.response_last
        else:
            LogPrint().info("----------------请求方法或类型有误----------------")

    def p_post_deal(self):
        data = eval(self.request_data)                                                            # 将str类型转换成字典类型
        payload = json.dumps(data)
        headers = {'content-type': "application/json"}
        # headers = InterfaceHeadDeal().sign_headers(payload, self.request_data_type)
        url = self.api_host + self.request_url
        LogPrint().info('-------------调用第' + self.num + '个测试用例的接口-------------：' + url)

        try:
            response = ''
            if self.request_data_type in ('Data', 'File'):
                response = requests.post(url=url, data=payload, headers=headers, timeout=5)
            elif self.request_data_type == 'Form':  # 以form形式发送post请求,只需将请求的参数构造成一个字典,传入给request.post()的data参数即可
                response = requests.post(url=url, data=data, timeout=5)

            status = response.status_code
            resp1 = response.text

            if status == 200:
                resp2 = CommonMethod.response_data_deal(resp1)  # 对接口返回的数据进行处理,如结果中存在转义字符需要存储到数据库中,则需要进行数据的相应处理
            else:
                resp2 = resp1                      # 如果接口请求是404、415等非正常的状态码,那么返回的数据就不需要进行处理,直接存入数据库中即可

            assert_result = self.p_common_code_one(status, resp2)
            self.response_last = resp2
            return assert_result

        except Timeout:
            assert_result = self.p_common_code_two(url)
            self.response_last = "null"
            return assert_result

    def p_get_deal(self):
        url = self.api_host + self.request_url
        LogPrint().info('-------------调用第' + self.num + '个测试用例的接口-------------：' + url)
        try:
            response = requests.get(url=url, params=self.request_data, timeout=5)
            status = response.status_code
            resp1 = response.text.encode("utf-8")
            # resp = response.read()

            if type(resp1 == "bytes"):
                resp1 = str(resp1, encoding="utf-8")
            assert_result = self.p_common_code_one(status, resp1)
            return assert_result

        except Timeout:
            assert_result = self.p_common_code_two(url)
            return assert_result

    # 公共函数,主要用于结果判断和处理
    def p_common_code_one(self, status, resp):
        sql = self.p_sql_deal('fail', resp)
        if status == 200:
            LogPrint().info('----------------返回结果成功----------------：' + resp)
            self.p_assert_deal(resp)
            if self.assert_result == 'success':
                LogPrint().info('----------------测试断言结果----------------：' + '第' + str(self.num) + '个测试用例断言：通过')
                sql = self.p_sql_deal('success', resp)
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
            # self.md.close_db(self.conn, self.cur)
        return assert_result

    def p_common_code_two(self, url):
        LogPrint().error('----------------返回结果失败----------------：' + '第' + str(self.num) +
                         '个测试用例的接口请求超时响应,请注意!! [ ' + url + ' ]')
        assert_result = 'error'
        # 测试结果失败的用例信息存入数据库
        sql = self.p_sql_deal('fail', ' ')
        self.md.other_operate_db(self.conn, self.cur, sql)

        mail_title = '接口响应超时: ' + self.api_purpose + ':' + url
        MailSend().overtime_warn(mail_title)
        return assert_result

    """
    断言结果函数,断言的方式有两种,一种是code和msg的值断言(包括正常和异常断言),另一种是接口关键数据断言,校验具体返回的数据字段值,所以excel中的
    check_point数据格式必须是这三种:包含code、包含msg、或者"${openId}=test"格式,最后格式的符号和预期值可以变化
    """
    def p_assert_deal(self, resp):
        check_point_list = self.check_point.split(",")
        check_result_list = []
        for i in check_point_list:                                  # check_point中可能需要多个校验的数据,所以要用逗号分隔符对字符串进行切片
            if 'code' in i or 'msg' in i:                           # 这里是判断是否是code和msg断言,前两种是正常和异常的code、msg断言
                if i in resp:
                    check_result_list.append(True)
                else:
                    check_result_list.append(False)
            else:                                                   # 这种情况是接口关键数据断言,校验具体返回的数据字段值
                # i必须是'{"openId":"$openId"}'这种格式,这里是对excel中的check_point格式进行了转换,excel中的格式必须是"${openId}>0"这种
                i_one = i.split("{")
                i_two = i_one[1].split("}")
                i_three = '$' + i_two[0]
                i_four = str({i_two[0]: i_three})
                request_data_last = CommonMethod.request_data_deal(i_four, resp)

                i_nine = i_two[1]
                i_ten = i_nine.split("\"")[0]
                if i_ten[1] != '=' and i_ten[1] != '<' and i_ten[1] != '>':
                    i_five = i_ten[0]                                                # 断言语句中的符号
                    i_six = i_ten[1:]                                                # 断言语句中的预期数据字段值
                else:
                    i_five = i_ten[:2]
                    i_six = i_ten[2:]

                i_seven = eval(request_data_last)
                i_eight = i_seven[i_two[0]]                                          # 从resp中拿出来的需要校验的实际数据字段值

                if i_five == '>':
                    check_result_list.append(str(i_eight) > str(i_six))
                elif i_five == '<':
                    check_result_list.append(str(i_eight) < str(i_six))
                elif i_five == '=':
                    check_result_list.append(str(i_eight) == str(i_six))
                elif i_five == '>=':
                    check_result_list.append(str(i_eight) >= str(i_six))
                elif i_five == '<=':
                    check_result_list.append(str(i_eight) <= str(i_six))
                elif i_five == '!=':
                    check_result_list.append(str(i_eight) != str(i_six))
                else:
                    LogPrint().info('--------断言语句中的比较符号有误,暂时只支持6种,请核对!---------')

        if False in check_result_list:
            self.assert_result = 'fail'
        else:
            self.assert_result = 'success'

    def p_sql_deal(self, result, response):
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
            status = 1
        else:
            status = 0
        # 这里需要将参数都加上''符号,不然在sql语句中不是string类型,如请求方法时post,在sql中需要变为'post'才正确
        sql = "insert into pressure_test_case(case_id,request_method,request_data_type,interface_name,url," \
              "request_data,assert_fail_reason,status,response,create_time) " \
              "values(%d,%s,%s,%s,%s,%s,%s,%d,%s,%s)" % \
              (int(self.num), "\'" + self.request_method + "\'", "\'" + self.request_data_type + "\'", "\'" +
               self.api_purpose + "\'", "\'" + url + "\'", request_data_last, check_point_last,
               status, "\'" + response + "\'", "\'" + str(create_time) + "\'")
        return sql

    # 用例执行完毕后根据执行结果,更新pressure_test_data表的sql语句
    @staticmethod
    def pressure_sql_two(md, conn, cur, field, result_id):
        sql_one = 'select %s,case_total from pressure_test_data where result_id = %d' % (field, result_id)
        result_two = md.select_db(conn, cur, sql_one)
        filed_num = result_two[0][0]
        case_total = result_two[0][1]

        sql_two = 'update pressure_test_data set %s = %d,case_total = %d where result_id = %d' \
                  % (field, filed_num + 1, case_total + 1, result_id)
        LogPrint().info("-------更新测试结果表的sql语句是-------:" + sql_two)

        md.other_operate_db(conn, cur, sql_two)
