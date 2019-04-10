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
    # 接口调用函数
    def interface_test(num, api_purpose, api_host, request_url, request_method, request_data_type, request_data,
                      check_point):
        data = eval(request_data)                           # 将str类型转换成字典类型
        payload = json.dumps(data)
        headers = InterfaceHeadDeal().sign_headers(payload, request_data_type)
        url = api_host + request_url
        lp = LogPrint()
        ms = MailSend()
        if request_method == 'POST' and request_data_type != 'File':
            try:
                response = ''
                if request_data_type == "Data":
                    response = requests.post(url=url, data=payload, headers=headers, timeout=5)
                    print(2)
                elif request_data_type == 'Form':  # 以form形式发送post请求,只需将请求的参数构造成一个字典,传入给request.post()的data参数即可
                    response = requests.post(url=url, data=data, timeout=5)
                    print(1)
                status = response.status_code
                resp1 = response.text
                print(status)
                print(resp1)
                resp2 = resp1.encode("utf-8")

                if status == 200:
                    if check_point in resp2:
                        lp.info(str(num) + '. ' + api_purpose + ' 成功, ' + str(status) + ', ' + resp2)
                    else:
                        lp.error(str(num) + '.' + api_purpose + ' 失败！！！, [ ' + str(status) + ' ], ' + resp2)
                    return status, resp2
                else:
                    lp.error(str(num) + ' ' + api_purpose + ' 失败！！！, [ ' + str(status) + ' ], ' + resp2)
                    return status, resp2
            except Timeout:
                lp.error(str(num) + ' .' + api_purpose + ':' + url + '  超时响应,请注意!!')
                mail_title = '接口响应超时: ' + api_purpose + ':' + url
                ms.overtime_warn(mail_title)
        elif request_method == 'GET':
            try:
                response = requests.get(url=request_url, params=request_data, timeout=5)
                status = response.status_code
                resp1 = response.text
                resp2 = resp1.encode("utf-8")
                # resp = response.read()
                print(status)
                print(resp2)
                return status, resp2

            except Timeout:
                lp.error(str(num) + ' .' + api_purpose + ':' + url + '超时响应,请注意!!')
                mail_title = '接口响应超时: ' + api_purpose + ':' + url
                ms.overtime_warn(mail_title)

        elif request_data_type == 'File':
            dataFile = request_data
            if not os.path.exists(dataFile):
                lp.error(str(num) + ' ' + api_purpose + ' 文件路径配置无效，请检查[Request Data]字段配置的文件路径是否存在！！！')
            fopen = open(dataFile, 'rb')
            data = fopen.read()
            fopen.close()
            # request_data = '''
            return request_data_type


