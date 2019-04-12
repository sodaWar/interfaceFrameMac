# coding=utf-8
import datetime
from Common.excel_pub import ExcelDeal
from Logic.mail_send import MailSend
from Logic.html_report import HtmlReport
from Logic.interface_deal import InterfaceDeal


class RunTest:

    @ staticmethod
    def run_interface_test():
        # 记录测试开始时间
        start_time = datetime.datetime.now()

        error_case = []  # 用于保存接口返回的内容和HTTP状态码
        status = resp = ''
        my_list = []
        param_list = ['num', 'api_purpose', 'api_host', 'request_url', 'request_method', 'request_data_type',
                      'request_data', 'check_point', 'test_describe']
        all_list = ExcelDeal().get_test('E:\\MyProgram\\InterfaceTestFrame\\APICase\\TestCase.xlsx')

        for i in all_list:
            me = dict(zip(param_list, i))
            my_list.append(me)

        for x in range(len(my_list)):
            a = InterfaceDeal(my_list[x]['num'], my_list[x]['api_purpose'], my_list[x]['api_host'],
                              my_list[x]['request_url'], my_list[x]['request_method'],
                              my_list[x]['request_data_type'], my_list[x]['request_data'], my_list[x]['check_point'],
                              my_list[x]['test_describe'])
            a.interface_test()
            # if status != 200:  # 如果状态码不为200,那么证明接口产生错误,保存错误信息
            #     error_case.append((my_list[x]['num'] + '、' + my_list[x]['api_purpose'], str(status) +
            #                        my_list[x]['api_host'] + my_list[x]['request_url'], resp))
            #     continue

        # 记录测试结束时间,需要存入数据库中
        end_time = datetime.datetime.now()
        consume_time = end_time - start_time
        print consume_time
        # 生成测试报告
        filename = HtmlReport().generate_html('test report', 'E:\\MyProgram\\InterfaceTestFrame\\Report\\report.html')

        # 这里'r'读模式,'w'写模式,'a'追加模式,'b'二进制模式,'+'读/写模式
        fo = open(filename, "r+")
        text = fo.read()

        ms = MailSend()
        ms.send_mail(text)


if __name__ == '__main__':
    RunTest().run_interface_test()


