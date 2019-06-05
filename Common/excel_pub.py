# coding=utf-8
from Logic.log_print import LogPrint
import json
import hashlib
import os
import xlrd                                                                                                             # 操作xlsx文件的库
import base64                                                                                                           # 生成的编码可逆,速度快,生成ascii字符,但是容易破解,仅适用于加密非关键信息的场合
from pyDes import *                                                                                                     # 使用pydes库进行des加密


class ExcelDeal:
    # 获取excel文件中的测试用例
    @ staticmethod
    def get_test(case):
        # join()函数是连接字符串数组,os.path.join()函数是将多个路径组合后返回,os.getcwd()是返回当前进程的工作目录,testcase是测试用例文件的目录地址
        case = os.path.join(os.getcwd(), case)
        if not os.path.exists(case):
            lp = LogPrint()
            lp.error('----------------测试用例文件不存在!!----------------')
            sys.exit()
        test_case = xlrd.open_workbook(case)  # 打开文件
        table = test_case.sheet_by_index(0)  # 根据shell索引获取sheet内容
        pwd = '123456'
        all_list = []

        for i in range(1, table.nrows):  # 循环行列表数据,table.nrows是获取行数
            # table.cell().value获取某个单元格的内容值,该方法第一个参数是行数,第二个参数是列数
            # 这里判断测试用例的active是否是活跃的,活跃的代表可测试,不活跃的代表不测试,所以添加的时候需要选择用例是否活跃
            if table.cell(i, 10).value.replace('\n', '').replace('\r', '') != 'Yes':
                continue
            num = str(int(table.cell(i, 0).value)).replace('\n', '').replace('\r', '')
            api_purpose = table.cell(i, 1).value.replace('\n', '').replace('\r', '')
            request_url = table.cell(i, 2).value.replace('\n', '').replace('\r', '')
            request_method = table.cell(i, 3).value.replace('\n', '').replace('\r', '')
            request_data_type = table.cell(i, 4).value.replace('\n', '').replace('\r', '')
            request_data = table.cell(i, 5).value.replace('\n', '').replace('\r', '')
            encryption = table.cell(i, 6).value.replace('\n', '').replace('\r', '')
            check_point = table.cell(i, 7).value.replace('\n', '').replace('\r', '')
            test_describe = table.cell(i, 8).value.replace('\n', '').replace('\r', '')
            relevance_case = str(int(table.cell(i, 9).value)).replace('\n', '').replace('\r', '')
            # relevance_case = table.cell(i, 9).value.replace('\n', '').replace('\r', '').split(';')

            if encryption == 'MD5':  # 如果数据采用md5加密，便先将数据加密,这里加密的密码需要跟不同接口的session有关系
                request_data = json.loads(request_data)
                request_data['pwd'] = hashlib.md5().update(request_data['pwd']).hexdigest()

            elif encryption == 'DES':  # 数据采用des加密
                k = des('secretKEY', padmode=PAD_PKCS5)
                request_data = base64.b64encode(k.encrypt(json.dumps(pwd)))
            param_list = [num, api_purpose, request_url, request_method, request_data_type, request_data,
                          encryption, check_point, test_describe, relevance_case]
            all_list.append(param_list)
        return all_list

