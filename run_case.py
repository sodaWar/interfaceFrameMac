# coding=utf-8
import datetime
import time
from Common.excel_pub import ExcelDeal
from Logic.mail_send import MailSend
from Logic.html_report import HtmlReport
from Logic.log_print import LogPrint
from Common.mysql_pub import MysqlDeal
from Common.method_pub import Common_Method
from Logic.interface_deal import InterfaceDeal      # 注意,导入的包中也会打印相应包中的日志,之后再调用类中的方法也会打印日志,所以会出现重复的日志


class RunTest:

    @ staticmethod
    def run_interface_test():
        my_list = []
        param_list = ['num', 'api_purpose', 'api_host', 'request_url', 'request_method', 'request_data_type',
                      'request_data', 'encryption', 'check_point', 'test_describe']
        LogPrint().info("----------------开始读取excel中的测试用例----------------")
        all_list = ExcelDeal().get_test('E:\\MyProgram\\InterfaceTestFrame\\APICase\\TestCase2.xlsx')
        for i in all_list:
            me = dict(zip(param_list, i))
            my_list.append(me)

        LogPrint().info("----------------执行用例前插入准备更新的表记录----------------")
        sql_one = 'insert into test_result_data(success_num, fail_num, error_num, case_total,create_time)' \
                  ' values (0,0,0,0,now())'
        md = MysqlDeal()
        conn, cur = md.conn_db()
        md.other_operate_db(conn, cur, sql_one)
        sql_two = 'select result_id from test_result_data order by create_time desc limit 1'
        result_one = md.select_db(cur, sql_two)
        result_id = result_one[0][0]

        LogPrint().info("----------------开始执行测试用例----------------")
        # 记录测试开始时间
        start_time = datetime.datetime.now()

        for x in range(len(my_list)):
            ifd = InterfaceDeal(my_list[x]['num'], my_list[x]['api_purpose'], my_list[x]['api_host'],
                                my_list[x]['request_url'], my_list[x]['request_method'],
                                my_list[x]['request_data_type'], my_list[x]['request_data'], my_list[x]['check_point'],
                                my_list[x]['test_describe'])
            result_temp = ifd.interface_test()

            LogPrint().info("----------------根据用例执行情况,开始更新测试结果表的相关数据----------------")
            if result_temp == 'success':
                Common_Method.sql_deal_two(md, conn, cur, 'success_num', result_id)
            elif result_temp == 'fail':
                Common_Method.sql_deal_two(md, conn, cur, 'fail_num', result_id)
            elif result_temp == 'error':
                Common_Method.sql_deal_two(md, conn, cur, 'error_num', result_id)
            else:
                print 'wait!!'

        # 将测试用例执行时间存入到数据库中
        time.sleep(0.5)
        end_time = datetime.datetime.now()
        start_time, end_time = Common_Method.test_time_deal(md, conn, cur, start_time, end_time, result_id)

        LogPrint().info("----------------生成测试报告----------------")
        filename = HtmlReport().generate_html(md, conn, cur, 'test report',
                                              'E:\\MyProgram\\InterfaceTestFrame\\Report\\report.html',
                                              start_time, end_time)

        # 这里'r'读模式,'w'写模式,'a'追加模式,'b'二进制模式,'+'读/写模式
        fo = open(filename, "r+")
        text = fo.read()
        ms = MailSend()
        # 发送测试报告
        ms.send_mail(text)


if __name__ == '__main__':
    RunTest().run_interface_test()


