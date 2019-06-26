import datetime
import time
from Common.excel_pub import ExcelDeal
import threading
from Logic.mail_send import MailSend
from Logic.html_report import HtmlReport
from Common.interface_deal_alone import InterfaceDealAlone
from Logic.log_print import LogPrint
from Common.mysql_pub import MysqlDeal
from Common.method_pub import CommonMethod
from Logic.pressure_interface_deal import PressureInterfaceDeal

lock = threading.Lock()

"""
压力测试用例中Concurrent Number为并发数,All Request Number为线程数的字段;异步启动了20个线程,如果没有限制,那么可能会并发产生10或者15个等数量的线程并发压力
这时候需要在执行线程时限制每次并发执行的个数最多只能是5个的需求; 开了100个线程那么并发数就是100,所以总共需要启动100个线程的话,
而需求中并发数不一定是100，可以是10，那么就需要限制10个并发数. 所以这里并发数就是1秒同时请求的线程数（其他已启动的线程会阻塞）；
线程数就是总共启动的线程数量，最后执行完线程数的时间就是线程数量/并发数,最后的秒数就是执行的时间
"""


class PressureTest:
    md = MysqlDeal()
    conn, cur = md.conn_db()
    result_id = ''                                 # 这是pressure_test_data表中的id值,为了每次用例执行完毕后找的到所需要更新的表记录
    param_list = ['num', 'api_purpose', 'request_url', 'request_method', 'request_data_type',
                  'request_data', 'check_point', 'pressure_test_file', 'concurrent_number', 'all_request_number']

    def run_pressure_test(self, test_case_file):
        test_case_list = []                                               # 存储测试用例内容的列表
        LogPrint().info("----------------开始读取excel中的测试用例----------------")
        all_list = ExcelDeal().get_test(test_case_file, 'PressureTest')   # 将测试用例文件路径参数化,这种可以读取多个测试用例文件
        for i in all_list:
            me = dict(zip(self.param_list, i))
            test_case_list.append(me)

        md = self.md
        conn = self.conn
        cur = self.cur
        LogPrint().info("----------------执行用例前插入准备更新的表记录----------------")
        sql_one = 'insert into pressure_test_data(success_num, fail_num, error_num, case_total,create_time)' \
                  ' values (0,0,0,0,now())'

        md.other_operate_db(conn, cur, sql_one)
        sql_two = 'select result_id from pressure_test_data order by create_time desc limit 1'
        result_one = md.select_db(conn, cur, sql_two)
        result_id = result_one[0][0]

        LogPrint().info("----------------开始执行测试用例----------------")
        # 记录测试开始时间
        start_time = datetime.datetime.now()

        PressureTest().run_deal_one(result_id, test_case_list)

        # 将测试用例执行时间存入到数据库中
        time.sleep(0.5)
        end_time = datetime.datetime.now()
        start_time, end_time = CommonMethod.test_time_deal(md, conn, cur, start_time, end_time, result_id,
                                                           'PressureTest')

        LogPrint().info("----------------生成测试报告----------------")
        # filename = HtmlReport().generate_html(md, conn, cur, 'test report',
        #                                       '/Users/hongnaiwu/MyProject/InterfaceFrame/Report/report.html',
        #                                       start_time, end_time)
        #
        # # 这里'r'读模式,'w'写模式,'a'追加模式,'b'二进制模式,'+'读/写模式
        # fo = open(filename, "r+")
        # text = fo.read()
        # ms = MailSend()
        # # 发送测试报告
        # ms.send_mail(text)

    def run_deal_one(self, result_id, test_case_list):
        for x in range(len(test_case_list)):                # 循环整个测试用例
            request_data_list = PressureTest.request_deal_two(test_case_list[x]['request_data'],
                                                              test_case_list[x]['pressure_test_file'])
            pressure_num = int(test_case_list[x]['all_request_number'])

            initial_value = int(test_case_list[x]['concurrent_number'])         # 信号量对象的初始值
            sm = threading.Semaphore(initial_value)     # 创建一个信号量的对象,函数内的4是设置初始值为4,即最大同时请求的线程数不超过4
            # 创建线程数组,这是多线程请求每个测试用例需要请求的次数
            threads = []

            """
            # 如果需要传kwargs参数,如下方式:
            # t1 = threading.Thread(target=chi, kwargs={"threadName": "火锅", "name": "吃火锅"})
            # threads.append(t1)
            """

            # 循环创建线程t，并将每个创建的线程添加到线程数组中
            if pressure_num <= len(request_data_list):
                for i in range(pressure_num):
                    thread_name = 'Thread-' + str(i)
                    t = threading.Thread(target=PressureTest.run_deal_two, args=(self, thread_name, test_case_list[x],
                                                                                 request_data_list[i], result_id, sm))
                    t.start()
            # 如果总请求数比txt文件内的参数要多,则需要利用txt文件内的数循环赋值请求参数
            elif pressure_num > len(request_data_list):
                request_last_list = []                                                                  # 所有循环赋值后的参数列表
                special_num = (pressure_num + len(request_data_list) - 1)//len(request_data_list)       # 两数相除,向上取整
                # 有多少次请求,就在列表内增加多少个参数
                for y in range(special_num):
                    if y != special_num-2:
                        for i in range(len(request_data_list)):
                            request_last_list.append(request_data_list[i])

                    else:
                        special_num_two = pressure_num - (special_num-1) * len(request_data_list)
                        for i in range(special_num_two):
                            request_last_list.append(request_data_list[i])

                for i in range(pressure_num):
                    thread_name = 'Thread-' + str(i)
                    t = threading.Thread(target=PressureTest.run_deal_two, args=(self, thread_name, test_case_list[x],
                                                                                 request_last_list[i], result_id, sm))
                    threads.append(t)

            # 启动线程
            for t in threads:
                t.start()

            length = len(threading.enumerate())  # 枚举返回个列表
            LogPrint().info("----------------当前运行的线程数为：%d----------------" % length)
            """
            主线程中调用子线程的join方法,这样主线程在子线程完成之前就会一直堵塞;这里注意join()方法放置的位置,要等待所有的子线程启动并执行完毕后
            才能执行join()函数,如果直接放在start()函数后面,那么就是每启动一个线程,就必须等这个线程执行完毕后才能启动下一个线程,会一直阻塞其他
            线程的启动和执行.如果没有join()函数那么就会导致最后整个接口请求的时间有错误,因为主程序没有受到阻塞,那么就会导致程序提前执行了
            test_time_deal()这个函数,存入数据库中的time_consuming的值错误,因此要等所有子线程执行完后才能调用join()函数
            """
            for t in threads:
                t.join()

    # 单个接口请求
    def run_deal_two(self, thread_name, one_test_case, request_data_last, result_id, sm):
        sm.acquire()                # 每次调用信号量对象的acquire()函数,都会使内部计数器减1
        # print(threading.currentThread().getName() + ' request api ...\n')                     # 获得当前线程的名字,即第几个线程

        md = self.md
        conn = self.conn
        cur = self.cur

        ifd = PressureInterfaceDeal(one_test_case['num'], one_test_case['api_purpose'], one_test_case['request_url'],
                                    one_test_case['request_method'], one_test_case['request_data_type'],
                                    request_data_last, one_test_case['check_point'],
                                    one_test_case['pressure_test_file'], one_test_case['concurrent_number'],
                                    one_test_case['all_request_number'], thread_name)
        result_temp, response = ifd.p_interface_test()

        if result_temp == 'success':
            """
            这里增加互斥锁,防止多个线程同时对pressure_test_data表的数据做修改,因为每次执行测试用例,这个表内只有一条记录修改,而pressure_test_case
            表不会有影响,是因为不同的线程插入到pressure_test_case表内的记录不同,所以多个线程不会对同一个记录的数据做修改,而结果表是所有的线程
            都会对同一个记录的数据做修改,因此需要加上互斥锁,保持同步才可
            """
            lock.acquire()                                      # 创建锁,防止多个线程异步操作数据库,同时修改某个表的记录
            PressureInterfaceDeal.pressure_sql_two(one_test_case['num'], thread_name, md, conn, cur, 'success_num',
                                                   result_id)
            lock.release()                                      # 释放锁
        elif result_temp == 'fail':
            lock.acquire()
            PressureInterfaceDeal.pressure_sql_two(one_test_case['num'], thread_name, md, conn, cur, 'fail_num',
                                                   result_id)
            lock.release()
        elif result_temp == 'error':
            lock.acquire()
            PressureInterfaceDeal.pressure_sql_two(one_test_case['num'], thread_name, md, conn, cur, 'error_num',
                                                   result_id)
            lock.release()
        else:
            LogPrint().info("----------------接口断言后的结果值有误,请核对!----------------")

        time.sleep(3)

        # print(threading.currentThread().getName() + ' released request...\n')

        sm.release()                        # 每次调用信号量对象的release()函数,都会使内部计数器加1

    # 把所有txt文件内的数据都赋值给接口中该类型的参数,然后请求该接口的时候再进行多线程启动接口,并且赋不同的值!
    @staticmethod
    def request_deal_one(request_data):
        request_data_temp = eval(request_data)
        keys = list(request_data_temp.keys())                           # 获取接口请求的数据中所有的key值
        special_key = []                                     # 所有值是包含~的参数key列表
        special_key_two = []                                 # 所有值是包含&的参数key列表
        special_key_three = []                               # 所有值是包含*的参数key列表
        for i in keys:
            temp = '~' + i                                   # 该参数使用场景:请求的接口参数中,用到的是txt文件中的值,循环对参数赋值,以便用于压力测试
            temp_two = '&' + i                               # 该参数使用场景:请求的接口参数中,用到的是自定义的函数值
            temp_three = '*' + i                             # 该参数使用场景:请求的接口参数中,用到单独封装处理的接口返回值,如登录接口等
            if temp == request_data_temp[i]:
                special_key.append(i)
            elif temp_two == request_data_temp[i]:
                special_key_two.append(i)
            elif temp_three == request_data_temp[i]:
                special_key_three.append(i)
            else:
                continue
        return special_key, special_key_two, special_key_three

    @staticmethod
    def request_deal_two(request_data, pressure_test_file):
        # 请求数据中所有特殊类型的key值列表
        special_key, special_key_two, special_key_three = PressureTest.request_deal_one(request_data)

        f = open(pressure_test_file, "r")                                   # 设置文件对象
        param_one = f.read()                                                # 将txt文件的所有内容读入到字符串str中
        param = param_one.split('\n')

        special_one = []
        special_two = []                                                    # 每个key赋值相应的值,所有的情况存为一个列表

        for i in param:
            param_two = i.split(' ')                                        # 以一个空格为分隔符,所以文件中数据不能有多个空格
            for x in range(len(param_two)):
                special_key[x] = {str(special_key[x]): param_two[x]}        # 对每个key进行赋值,外套循环
                special_one.append(special_key[x])
                if x == len(param_two)-1:                                   # 一行数据赋值完毕,对下一行数据再次进行赋值,所以已赋值的数据存入列表内
                    special_two.append(special_one)
                    # 一行数据处理完后,将special_one和special_key的值都置为初始化的数据,否则在原来的基础上再操作,会出现问题
                    special_one = []
                    special_key, special_key_two, special_key_three = PressureTest.request_deal_one(request_data)

        f.close()   # 将文件关闭

        # 读取完文件内容后,再对请求数据进行处理,将文件中的内容赋值到请求数据中
        request_data = eval(request_data)
        request_data_list = []                                          # 一个接口做压测所有需要请求的线程数的请求数据列表
        for x in range(len(special_two)):                               # 相当于循环txt文件中的行数,如10行即代表要10个线程,请求10次接口
            for y in range(len(special_key)):                           # 相当于循环txt文件中的列数,作用是为了给每个请求数据中的相应key赋值
                key = special_key[y]
                request_data[key] = special_two[x][y][key]              # 将每个a包含~的参数赋值

                for z in special_key_two:                               # 将每个包含&的参数赋值
                    # 自定义一个函数如随机函数,将其中的某个值赋给请求数据中的参数
                    request_data[z] = CommonMethod.custom_random_one()                # 赋值随机整数
                    # request_data_temp[i] = CommonMethod.create_phone()              # 赋值随机电话号码数(返回的类型是str类型)

                    # param = CommonMethod.random_param_one()  # 这里参数是从用户写入到random_param.txt文件中读取的内容
                    # request_data[i] = CommonMethod.custom_random_two(param)  # 列表内的值随机一个赋值给参数值

                for k in special_key_three:                             # 将每个包含*的参数赋值
                    # 将单独封装处理的接口如登录接口返回值,赋值给请求数据中的参数
                    response_alone = InterfaceDealAlone.user_login()
                    request_data[k] = CommonMethod.response_alone_deal(response_alone, k)

                if y == len(special_key) - 1:
                    # 这里需要将请求数据转换为str类型,否则最后存入列表内的值都是最后一个dict的值,且需要将请求数据中的单引号替换为双引号
                    request_data_list.append(str(request_data).replace("\'", "\""))

        return request_data_list
