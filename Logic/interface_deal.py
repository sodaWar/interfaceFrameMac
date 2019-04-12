# coding=utf-8
from Logic.mail_send import MailSend
from Logic.log_print import LogPrint
from Common.class_pub import InterfaceHeadDeal
import json
import requests
import os
from pyDes import *
from requests.exceptions import Timeout
reload(sys)
sys.setdefaultencoding('utf8')                                                                                          # 编码转换,转换之后默认编码格式是utf8,详细见笔记


class InterfaceDeal:
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
        data = eval(self.request_data)                           # 将str类型转换成字典类型
        payload = json.dumps(data)
        headers = InterfaceHeadDeal().sign_headers(payload, self.request_data_type)
        url = self.api_host + self.request_url
        lp = LogPrint()
        ms = MailSend()
        if self.request_method == 'POST' and self.request_data_type != 'File':
            try:
                response = ''
                if self.request_data_type == "Data":
                    response = requests.post(url=url, data=payload, headers=headers, timeout=5)
                    print(2)
                elif self.request_data_type == 'Form':  # 以form形式发送post请求,只需将请求的参数构造成一个字典,传入给request.post()的data参数即可
                    response = requests.post(url=url, data=data, timeout=5)
                    print(1)
                status = response.status_code
                resp1 = response.text
                print(status)
                print(resp1)
                resp2 = resp1.encode("utf-8")

                if status == 200:
                    if self.check_point in resp2:
                        lp.info(str(self.num) + '. ' + self.api_purpose + ' 成功, ' + str(status) + ', ' + resp2)
                    else:
                        lp.error(str(self.num) + '.' + self.api_purpose + ' 失败！！！, [ ' + str(status) + ' ], ' + resp2)
                    return status, resp2
                else:
                    lp.error(str(self.num) + ' ' + self.api_purpose + ' 失败！！！, [ ' + str(status) + ' ], ' + resp2)
                    return status, resp2
            except Timeout:
                lp.error(str(self.num) + ' .' + self.api_purpose + ':' + url + '  超时响应,请注意!!')
                mail_title = '接口响应超时: ' + self.api_purpose + ':' + url
                ms.overtime_warn(mail_title)
        elif self.request_method == 'GET':
            try:
                response = requests.get(url=self.request_url, params=self.request_data, timeout=5)
                status = response.status_code
                resp1 = response.text
                resp2 = resp1.encode("utf-8")
                # resp = response.read()
                print(status)
                print(resp2)
                return status, resp2

            except Timeout:
                lp.error(str(self.num) + ' .' + self.api_purpose + ':' + url + '超时响应,请注意!!')
                mail_title = '接口响应超时: ' + self.api_purpose + ':' + url
                ms.overtime_warn(mail_title)

        elif self.request_data_type == 'File':
            dataFile = self.request_data
            if not os.path.exists(dataFile):
                lp.error(str(self.num) + ' ' + self.api_purpose + ' 文件路径配置无效，请检查[Request Data]字段配置的文件路径是否存在！！！')
            fopen = open(dataFile, 'rb')
            data = fopen.read()
            fopen.close()
            # request_data = '''
            return self.request_data_type


