#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pyh2 import *
import time
import os
import sys
from Common.mysql_pub import MysqlDeal
reload(sys)
sys.setdefaultencoding('utf-8')


class HtmlReport:
    def __init__(self):
        self.title = 'test_report_page'       # 网页标签名称
        self.filename = ''                    # 结果文件名
        self.time_consuming = '00:00:00'      # 测试耗时
        self.success_num = 0                  # 测试通过的用例数
        self.fail_num = 0                     # 测试失败的用例数
        self.error_num = 0                    # 运行出错的用例数
        self.case_total = 0                   # 运行测试用例总数

    # 生成HTML报告
    def generate_html(self,head, file):
            md = MysqlDeal()
            conn, cur = md.conn_db()

            page = PyH(self.title)
            page << h1(head, align='center') # 标题居中
            # 该标签很重要,用于防止中文乱码,生成的js文件中中文正常显示,但写入是以utf-8编码写入,浏览器解释js源码默认是以gbk形式来渲染网页的,所以显示在网页会乱码,该标签就是告诉浏览器用UTF-8来渲染页面
            page << meta(charset="utf-8")

            result_five = md.select_db(cur, HtmlReport.sql_statement('time_consuming'))
            self.time_consuming = str(result_five[0][0])
            page << p('测试总耗时：' + self.time_consuming)

            # 查询测试用例总数
            result_one = md.select_db(cur,HtmlReport.sql_statement('case_total'))
            self.case_total = result_one[0][0]

            # 查询测试失败的用例数
            result_two = md.select_db(cur,HtmlReport.sql_statement('fail_num'))
            self.fail_num = result_two[0][0]

            # 查询测试通过的用例数
            result_three = md.select_db(cur,HtmlReport.sql_statement('success_num'))
            self.success_num = result_three[0][0]

            # 查询测试出错的用例数
            result_four = md.select_db(cur,HtmlReport.sql_statement('error_num'))
            self.error_num = result_four[0][0]

            page << p('测试用例数：' + str(self.case_total) + '&nbsp'*10 + '成功用例数：' + str(self.success_num) +
                      '&nbsp'*10 + '失败用例数：' + str(self.fail_num) + '&nbsp'*10 +  '出错用例数：' + str(self.error_num))
            #  表格标题caption 表格边框border 单元边沿与其内容之间的空白cellpadding 单元格之间间隔为cellspacing

            tab = table( border='1', cellpadding='1', cellspacing='0', cl='table')
            tab1 = page << tab
            tab1 << tr(td('用例ID', bgcolor='#ABABAB', align='center', style='height:70px')
                       + td('请求方法', bgcolor='#ABABAB', align='center', style='height:70px')
                       + td('请求数据类型', bgcolor='#ABABAB', align='center', style='height:70px')
                       + td('接口名称', bgcolor='#ABABAB', align='center', style='height:70px')
                       + td('接口地址', bgcolor='#ABABAB', align='center', style='height:70px')
                       + td('请求数据', bgcolor='#ABABAB', align='center', style='height:70px')
                       + td('断言内容', bgcolor='#ABABAB', align='center', style='height:70px')
                       + td('测试描述', bgcolor='#ABABAB', align='center', style='height:70px'))

            # 查询所有测试结果并记录到html文档
            query = ('SELECT case_id, request_method, request_data_type, interface_name,url,'
                     'request_data, assert_fail_reason,test_describe FROM test_problem_case')
            query_result = md.select_db(cur,query)

            for row in query_result:
                tab1 << tr(td(row[0], align='center') + td(row[1]) +
                           td(row[2]) + td(row[3], align='center') +
                           td(row[4]) + td(row[5]) + td(row[6]) + td(row[7]))

            self._set_result_filename(file)
            page.printOut(self.filename)
            md.close_db(conn, cur)
            return self.filename

    # 设置结果文件名
    def _set_result_filename(self, filename):
        self.filename = filename
        # 判断是否为目录
        if os.path.isdir(self.filename):
            raise IOError("%s must point to a file" % path)
        elif '' == self.filename:
            raise IOError('filename can not be empty')
        else:
            parent_path, ext = os.path.splitext(filename)
            tm = time.strftime('-%Y%m%d %H-%M-%S', time.localtime())
            self.filename = parent_path + tm + ext

    # sql语句的简单参数化
    @ staticmethod
    def sql_statement(name):
        sql = 'select ' + name + ' FROM test_result_data order by create_time desc'
        return sql



