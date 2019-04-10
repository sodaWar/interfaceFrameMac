# coding=utf-8
# 使用其他文件下的类的方式,这里注意其他类的所在文件中需要有__init__.py文件,该文件为空也可以
import sys
sys.path.append('E:\MyProgram\InterfaceTestFrame\Common')
sys.path.append('E:\MyProgram\InterfaceTestFrame\Logic')
from Common.excel_pub import ExcelDeal
from Logic.mail_send import MailSend
import datetime


def main():
    # 记录测试开始时间
    start_time = datetime.datetime.now()
    error_test = ExcelDeal().runtest('E:\\MyProgram\\InterfaceTestFrame\\APICase\\TestCase.xlsx')
    # 记录测试结束时间
    end_time = datetime.datetime.now()
    consume_time = end_time - start_time
    print consume_time

    if len(error_test) > 0:
        html = '<html><body>接口自动化定期扫描,共有 ' + str(len(error_test)) + ' 个异常接口,列表如下：' + '</p><table><tr><th style="width:10px;">接口</th><th style="width:10px;">状态</th><th style="width:200px;">接口地址</th><th>接口返回值</th></tr>'
        for test in error_test:
            print(test)
            html = html + '<tr><td>' + test[0] + '</td><td>' + test[1] + '</td><td>' + test[2] + '</td></tr>'
        html = html + '</table></body></html>'
        ms = MailSend()
        ms.send_mail(html)
        # 将结果输出到文件中,其中'r'读模式、'w'写模式、'a'追加模式、'b'二进制模式、'+'读/写模式
        with open('E:\\MyProgram\\InterfaceTestFrame\\Report\\test.html', 'a') as f:
            f.writelines(html)      # write()需要传入一个字符串做为参数,writelines()既可以传入字符串又可以传入一个字符序列,但不能是数字序列


if __name__ == '__main__':
    main()


