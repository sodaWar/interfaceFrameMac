# coding=utf-8
import datetime
import time
from Common.excel_pub import ExcelDeal
from Logic.mail_send import MailSend
from Logic.html_report import HtmlReport
from Logic.log_print import LogPrint
from Common.mysql_pub import MysqlDeal
from Common.method_pub import CommonMethod
from Logic.interface_deal import InterfaceDeal      # 注意,导入的包中也会打印相应包中的日志,之后再调用类中的方法也会打印日志,所以会出现重复的日志


class RunTest:
    test_case_list = []                                    # 存储测试用例内容的列表
    result_id = ''                                         # 这是test_result_data表中的id值,为了每次用例执行完毕后找的到所需要更新的表记录
    param_list = ['num', 'api_purpose', 'request_url', 'request_method', 'request_data_type',
                  'request_data', 'encryption', 'check_point', 'test_describe', 'relevance_case']
    LogPrint().info("----------------开始读取excel中的测试用例----------------")
    all_list = ExcelDeal().get_test('/Users/hongnaiwu/MyProject/InterfaceFrame/APICase/TestCase.xlsx')
    for i in all_list:
        me = dict(zip(param_list, i))
        test_case_list.append(me)
    md = MysqlDeal()
    conn, cur = md.conn_db()

    def run_interface_test(self):
        md = self.md
        conn = self.conn
        cur = self.cur
        LogPrint().info("----------------执行用例前插入准备更新的表记录----------------")
        sql_one = 'insert into test_result_data(success_num, fail_num, error_num, case_total,create_time)' \
                  ' values (0,0,0,0,now())'

        md.other_operate_db(conn, cur, sql_one)
        sql_two = 'select result_id from test_result_data order by create_time desc limit 1'
        result_one = md.select_db(cur, sql_two)
        result_id = result_one[0][0]

        LogPrint().info("----------------开始执行测试用例----------------")
        # 记录测试开始时间
        start_time = datetime.datetime.now()

        self.run_test(result_id)

        # 将测试用例执行时间存入到数据库中
        time.sleep(0.5)
        end_time = datetime.datetime.now()
        start_time, end_time = CommonMethod.test_time_deal(md, conn, cur, start_time, end_time, result_id)

        LogPrint().info("----------------生成测试报告----------------")
        filename = HtmlReport().generate_html(md, conn, cur, 'test report',
                                              '/Users/hongnaiwu/MyProject/InterfaceFrame/Report/report.html',
                                              start_time, end_time)

        # 这里'r'读模式,'w'写模式,'a'追加模式,'b'二进制模式,'+'读/写模式
        fo = open(filename, "r+")
        text = fo.read()
        ms = MailSend()
        # 发送测试报告
        ms.send_mail(text)

    def run_test(self, result_id):
        check_list = []                                     # 用来核对某个用例是否已经执行过
        md = self.md
        conn = self.conn
        cur = self.cur
        test_case_list = self.test_case_list
        # 该值是interface_test()函数处理完接口,并且断言完毕返回的结果,需要根据该结果更新test_result_data表的内容
        result_temp = ''
        for x in range(len(test_case_list)):
            # 循环所有的测试用例,先判断该用例是否已执行过,如果不在check_list中,则代表未执行过
            if int(test_case_list[x]['num']) not in check_list:
                # 未执行过的用例,再判断下该用例是否有关联的测试用例,如果测试用例的relevance_case字段值不为0,则代表有关联的用例
                if int(test_case_list[x]['relevance_case']) != 0:
                    LogPrint().info("----------开始调用第" + test_case_list[x]['num'] + "个测试用例的接口----------")
                    # 先去执行被关联的测试用例
                    for y in range(len(test_case_list)):
                        # 如果被关联的测试用例接口未执行过,那么就需要循环到被关联的接口,让它执行一次
                        if int(test_case_list[x]['relevance_case']) not in check_list:
                            # 如果已循环到该未执行过的被关联的接口
                            if int(test_case_list[y]['num']) == int(test_case_list[x]['relevance_case']):
                                # 先执行被关联的接口
                                result_two = self.run_test2(test_case_list[x]['relevance_case'], result_id)
                                LogPrint().info("----------继续调用第" + test_case_list[x]['num'] + "个测试用例的接口----------")
                                # 执行完毕后将该用例的编号存入到检查列表中,防止再次执行
                                check_list.append(int(test_case_list[x]['relevance_case']))

                                # 处理请求接口的数据,将被关联的接口数据赋值给请求的接口数据中
                                request_data_last = CommonMethod.request_data_deal(test_case_list[x]['request_data'],
                                                                                   result_two)
                                ifd = InterfaceDeal(test_case_list[x]['num'], test_case_list[x]['api_purpose'],
                                                    test_case_list[x]['request_url'], test_case_list[x]['request_method'],
                                                    test_case_list[x]['request_data_type'], request_data_last,
                                                    test_case_list[x]['check_point'], test_case_list[x]['test_describe'],
                                                    test_case_list[x]['relevance_case'])
                                result_temp2, response = ifd.interface_test()
                                check_list.append(int(test_case_list[x]['num']))

                                LogPrint().info("----------------根据用例执行情况,开始更新测试结果表的相关数据----------------")
                                if result_temp2 == 'success':
                                    CommonMethod.sql_deal_two(md, conn, cur, 'success_num', result_id)
                                elif result_temp2 == 'fail':
                                    CommonMethod.sql_deal_two(md, conn, cur, 'fail_num', result_id)
                                elif result_temp2 == 'error':
                                    CommonMethod.sql_deal_two(md, conn, cur, 'error_num', result_id)

                            # 如果未循环到该关联的接口
                            else:
                                LogPrint().info('-----不是被关联的用例----')
                                continue

                        # 如果被关联的接口已执行过,那么就不需要用到这里的for y 的循环了
                        elif int(test_case_list[x]['relevance_case']) in check_list:
                            # 如果请求的接口未执行过
                            if int(test_case_list[x]['num']) not in check_list:
                                LogPrint().info("----------该用例所关联的接口已执行,继续调用第" + test_case_list[x]['num'] +
                                                "个测试用例的接口----------")
                                result_temp = 'execute yet'
                                sql_two = 'select response from test_case where case_id = %d order by create_time desc ' \
                                          'limit 1' % (int(test_case_list[x]['relevance_case']))
                                result = md.select_db(cur, sql_two)
                                result_two = result[0][0]

                                # 处理请求接口的数据,将被关联的接口数据赋值给请求的接口数据中
                                request_data_last = CommonMethod.request_data_deal(test_case_list[x]['request_data'],
                                                                                   result_two)
                                ifd = InterfaceDeal(test_case_list[x]['num'], test_case_list[x]['api_purpose'],
                                                    test_case_list[x]['request_url'], test_case_list[x]['request_method'],
                                                    test_case_list[x]['request_data_type'], request_data_last,
                                                    test_case_list[x]['check_point'], test_case_list[x]['test_describe'],
                                                    test_case_list[x]['relevance_case'])
                                result_temp2, response = ifd.interface_test()
                                check_list.append(int(test_case_list[x]['num']))

                                LogPrint().info("----------------根据用例执行情况,开始更新测试结果表的相关数据----------------")
                                if result_temp2 == 'success':
                                    CommonMethod.sql_deal_two(md, conn, cur, 'success_num', result_id)
                                elif result_temp2 == 'fail':
                                    CommonMethod.sql_deal_two(md, conn, cur, 'fail_num', result_id)
                                elif result_temp2 == 'error':
                                    CommonMethod.sql_deal_two(md, conn, cur, 'error_num', result_id)

                            else:
                                LogPrint().info('-----该请求接口已执行----')

                # 未执行的用例,没有关联其他的测试用例,则直接调用interface_test函数,处理该接口即可
                else:
                    ifd = InterfaceDeal(test_case_list[x]['num'], test_case_list[x]['api_purpose'],
                                        test_case_list[x]['request_url'], test_case_list[x]['request_method'],
                                        test_case_list[x]['request_data_type'], test_case_list[x]['request_data'],
                                        test_case_list[x]['check_point'], test_case_list[x]['test_describe'],
                                        test_case_list[x]['relevance_case'])
                    result_temp, response = ifd.interface_test()
            # 该用例已执行过,不需要再次执行
            else:
                LogPrint().info("----------------第" + str(test_case_list[x]['num']) + "个测试用例已执行----------------")
                continue
            check_list.append(int(test_case_list[x]['num']))

            # LogPrint().info(('-------第' + str(test_case_list[x]['num']) + '个用例的结果是-------:' + result_temp))
            LogPrint().info("----------------根据用例执行情况,开始更新测试结果表的相关数据----------------")
            if result_temp == 'success':
                CommonMethod.sql_deal_two(md, conn, cur, 'success_num', result_id)
            elif result_temp == 'fail':
                CommonMethod.sql_deal_two(md, conn, cur, 'fail_num', result_id)
            elif result_temp == 'error':
                CommonMethod.sql_deal_two(md, conn, cur, 'error_num', result_id)
            else:
                LogPrint().info("----------------被关联的测试用例结果已更新,无需再次更新----------------")

    def run_test2(self, relevance_case, result_id):
        test_case_list = self.test_case_list
        md = self.md
        conn = self.conn
        cur = self.cur
        for x in range(len(test_case_list)):
            if int(test_case_list[x]['num']) == int(relevance_case):
                LogPrint().info("----------先调用被关联的第" + str(relevance_case) + "个测试用例的接口----------")

                ifd = InterfaceDeal(test_case_list[x]['num'], test_case_list[x]['api_purpose'],
                                    test_case_list[x]['request_url'], test_case_list[x]['request_method'],
                                    test_case_list[x]['request_data_type'], test_case_list[x]['request_data'],
                                    test_case_list[x]['check_point'], test_case_list[x]['test_describe'],
                                    test_case_list[x]['relevance_case'])
                result_temp2, response = ifd.interface_test()

                LogPrint().info("----------------根据用例执行情况,开始更新测试结果表的相关数据----------------")
                if result_temp2 == 'success':
                    CommonMethod.sql_deal_two(md, conn, cur, 'success_num', result_id)
                elif result_temp2 == 'fail':
                    CommonMethod.sql_deal_two(md, conn, cur, 'fail_num', result_id)
                elif result_temp2 == 'error':
                    CommonMethod.sql_deal_two(md, conn, cur, 'error_num', result_id)
                else:
                    LogPrint().info("----------------更新测试结果表失败,原因未知----------------")

                return response
            else:
                continue


if __name__ == '__main__':
    RunTest().run_interface_test()


