# coding=utf-8
import datetime
import json
import random
import os
from Common.interface_deal_alone import InterfaceDealAlone
from Common.txt_file_pub import TxtFilePath
from Logic.log_print import LogPrint


class CommonMethod:

    @ staticmethod
    def test_time_deal(md, conn, cur, start_time, end_time, result_id):
        start_time_one = start_time.strftime("%Y-%m-%d %H:%M:%S")                           # 将时间转换成对应的格式,返回值类型为str类型
        start_time_two = datetime.datetime.strptime(start_time_one, "%Y-%m-%d %H:%M:%S")    # 将str类型的时间转换成datetime类型

        end_time_one = end_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time_two = datetime.datetime.strptime(end_time_one, "%Y-%m-%d %H:%M:%S")

        result_time = end_time_two - start_time_two                         # 两个str类型的时间不能进行加减操作,所以必须先转换成datetime类型
        # 获取两个时间相差的总秒数,另外date、time和datetime类都支持与timedelta的加、减运算
        time_consuming = result_time.total_seconds()

        sql = 'update test_result_data set time_consuming = %s where result_id = %d' % \
              (time_consuming, result_id)
        md.other_operate_db(conn, cur, sql)

        return start_time_two, end_time_two

    # 用例执行完毕后根据执行结果,更新test_result_data表的sql语句
    @ staticmethod
    def sql_deal_two(md, conn, cur, field, result_id):
            sql_one = 'select %s,case_total from test_result_data where result_id = %d' % (field, result_id)
            result_two = md.select_db(conn, cur, sql_one)
            filed_num = result_two[0][0]
            case_total = result_two[0][1]

            sql_two = 'update test_result_data set %s = %d,case_total = %d where result_id = %d' \
                      % (field, filed_num + 1, case_total + 1, result_id)
            LogPrint().info("-------更新测试结果表的sql语句是-------:" + sql_two)
            md.other_operate_db(conn, cur, sql_two)

    # 关联的接口数据处理,request_data是这次接口的请求数据,result_two是所关联的接口返回的数据
    @ staticmethod
    def request_data_deal(request_data, result_two):
        # eval函数是将str类型转换为dict、list、tuple类型,如x = "{1:'a',2:'b'}"则转换为dict类型{1:'a',2:'b'},如x = "[[1,2],[3,4]]"则转换为list类型
        request_data_temp = eval(request_data)
        # json.loads函数是将json数据格式转换为字典
        response_data_temp = json.loads(result_two)
        response_data = response_data_temp['data']

        special_values = []                         # 这里是要把所有的data值是列表或字典类型的值,存入到该变量中,作为特殊的值
        # 获取data所有的值,可能是"2019"、{"goooId":102}、[11,12,13]
        values = list(response_data.values())
        for x in values:
            if isinstance(x, dict):                 # 如果data的值是dict类型,直接存入到特殊值列表中
                special_values.append(x)
            elif isinstance(x, list):               # 如果data的值是list类型,循环整个列表,将列表所有的值存入到特殊值列表中
                for z in range(len(x)):
                    special_values.append(x[z])

        keys = list(request_data_temp.keys())       # 获取接口请求的数据中所有的key值
        for i in keys:
            temp = '$' + i                          # 该参数使用场景:两个接口关联时,请求的接口参数中需要用到被关联的接口返回的结果
            temp_two = '&' + i                      # 该参数使用场景:请求的接口参数中,用到的是自定义的函数值
            temp_three = '*' + i                    # 该参数使用场景:请求的接口参数中,用到单独封装处理的接口返回值,如登录接口等
            temp_four = '~' + i                     # 该参数使用场景:txt文件内的数据赋值给接口参数中
            if temp == request_data_temp[i]:        # 如果请求的key值对应的value值是$+key的值如goodId这个key的值是$goodId
                try:
                    # response_data[i]表示先在关联接口返回的数据中,所有data的正常key值查询是否存在该key，如果有这个key的值,则赋给接口请求的这个有参数的key的值
                    request_data_temp[i] = response_data[i]
                except KeyError:                # 这里捕获异常是因为response_data[i],如果在response_data查找不到i这个key的话,会抛出该异常
                    # 在data正常的key中找不到,可能在某个key的values中找的到,如某个key的值是{"goooId":102}这种类型的,所以需要在特殊值列表中再查找一遍
                    for y in special_values:        # 循环特殊值列表,在这里查找i这个key是否存在
                        try:
                            request_data_temp[i] = y[i]
                            # 从这里开始给请求数据的未知的数据重新赋值
                        except KeyError:
                            if y == special_values[-1]:
                                LogPrint().warning("---------未查找到该key,需要赋值的参数值强制为空-------------")
                                request_data_temp[i] = ""
                            else:
                                continue
                        # 该special_values内的值可能是单纯一个值,如'www.baidu.com',这种情况使用y[i]就会报TypeError错误,不是字典所以使用y[i]报错
                        except TypeError:
                            if y == special_values[-1]:
                                LogPrint().warning("---------未查找到该key,需要赋值的参数值强制为空-------------")
                                request_data_temp[i] = ""
                            else:
                                continue
                        else:
                            # print('未捕获到该类型的错误或异常:', sys.exc_info()[0])
                            continue
                else:
                    # print('未捕获到该类型的错误或异常:', sys.exc_info()[0])
                    continue

            elif temp_two == request_data_temp[i]:
                LogPrint().info("-------自定义一个函数如随机函数,将其中的某个值赋给请求数据中的参数-------")
                # request_data_temp[i] = CommonMethod.custom_random_one()       # 赋值随机整数
                # request_data_temp[i] = CommonMethod.create_phone()            # 赋值随机电话号码数(返回的类型是str类型)

                param = CommonMethod.random_param_one()                         # 这里参数是从用户写入到random_param.txt文件中读取的内容
                request_data_temp[i] = CommonMethod.custom_random_two(param)    # 列表内的值随机一个赋值给参数值

            elif temp_three == request_data_temp[i]:
                # 如果还需要哪些封装的接口数据,在这里修改添加
                LogPrint().info("-------将单独封装处理的接口如登录接口返回值,赋值给请求数据中的参数-------")
                response_alone = InterfaceDealAlone.user_login()
                request_data_temp[i] = CommonMethod.response_alone_deal(response_alone, i)

            elif temp_four == request_data_temp[i]:     # 考虑下要不要这么做,感觉直接在请求这种类型的接口时再进行特殊处理,不用多余的这个步骤
                print("把所有txt文件内的数据都赋值给该参数,再请求该接口的时候再进行多线程启动接口,并且赋不同的值")
            else:
                continue

        # 这里返回的最后请求数据中,一个key对应的值可能是str、list或者字典类型等
        request_data_last = str(request_data_temp).replace("\'", "\"")
        return request_data_last

    # 接口返回的数据结果中,如果有转义字符,存储到数据库后转义字符会自动消失,所以需要处理转义字符,使得存储到数据库中还保存该转义字符
    @staticmethod
    def response_data_deal(resp):
        response_data_temp = json.loads(resp)
        response_data = response_data_temp["data"]

        # 返回的结果如果data内容是list,如data是[{},{},{}]这种形式的
        if isinstance(response_data, list):
            for i in response_data:                             # 循环整个list内容
                if isinstance(i, dict):                         # 如果list里面的内容是一个dict
                    key_one = list(i.keys())

                    '''
                     获得整个dict所有的key值,如果这个key值是goodsDetails,将这个key对应的values替换为其他语句,原因是我们接口返回的数据中
                     goodsDetails对应的values中包含\转义字符,而这个转义字符存入到数据库中,mysql会自动去除该转义字符,但是取出来该数据后,再进行下个接口
                     请求数据的关联时,会使用到上面request_data_deal函数,然后json.loads(result_two)转换该数据类型时报错,表示json数据格式不正确
                     '''
                    for x in key_one:
                        if x == "goodsDetails":
                            i["goodsDetails"] = "the data no to deal with"
                else:
                    continue
        # 如果返回的结果数据是dict类型,则直接拿到所有的key值即可
        elif isinstance(response_data, dict):
            key_two = list(response_data.keys())

            for i in key_two:
                if i == "goodsDetails":
                    response_data["goodsDetails"] = "the data no to deal with"

        # 以上主要是为了将goodsDetails这个key的values替换正常,这下面是要将返回的结果所有单引号变为双引号,且所有的None值都替换为空值,否则会在取出来时会报json数据格式不正确
        response_data_last = str(response_data_temp).replace("\'", "\"").replace("None", "\"\"")
        return response_data_last

    # 单独封装的接口返回值处理函数,也许数据的key值不是data而是其他类型,所以需要在这里另外处理
    @staticmethod
    def response_alone_deal(resp, param):
        response_data_temp = {}
        try:
            response_data_temp = json.loads(resp)
        except TypeError:
            LogPrint().info("-------请检查resp这个接口返回值格式和数据是否正确,如接口session过期导致等-------")
        response_data = {}
        try:
            response_data = response_data_temp["user"]
        except KeyError:
            LogPrint().info("-------user这个key值不存在于接口返回值中,请核对接口请求的正确性-------")
        return response_data[param]

    # 接口请求参数中的某个值是随机数中的一个的场景！该函数是生成一个指定范围内的整数
    @staticmethod
    def custom_random_one():
        param_random = random.randint(1, 10)
        return param_random

    # 随机生成一个电话号码
    @staticmethod
    def create_phone():
        # 第二位数字
        second = [3, 4, 5, 7, 8][random.randint(0, 4)]

        # 第三位数字
        third = {
            3: random.randint(0, 9),
            4: [5, 7, 9][random.randint(0, 2)],
            5: [i for i in range(10) if i != 4][random.randint(0, 8)],
            7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
            8: random.randint(0, 9),
        }[second]

        # 最后八位数字
        suffix = random.randint(9999999, 100000000)

        # 拼接手机号
        return "1{}{}{}".format(second, third, suffix)

    # 用户写入需要随机的参数列表到txt文件中,然后读取出来,作为下一个函数的参数使用
    @staticmethod
    def random_param_one():
        random_param_file = TxtFilePath().read_file_path('random_param')
        # txt文件的读取可配置化了,一个随机函数对应一个txt文件,增加随机函数时,需要在配置文件中增加路径名称,key值需要和函数名相同
        param_file_one = random_param_file['random_param_one']
        f = open(param_file_one, "r")  # 设置文件对象
        param_one = f.read()  # 将txt文件的所有内容读入到字符串str中
        param = param_one.split(' ')
        for i in param:
            if '\n' in i:
                param_two = i.split('\n')
                param.remove(i)
                for x in param_two:
                    param.append(x)
        f.close()  # 将文件关闭
        return param

    # param可以是一个列表、元组或字符串,choice()返回参数的一个随机项
    @staticmethod
    def custom_random_two(param):
        param_random = random.choice(param)
        return param_random

    # 这种方式的请求文件路径值是写在Request Data中, 该函数主要是为了将txt路径中的文件内容复制给request_data中,然后正常请求接口即可
    @staticmethod
    def request_type_file(request_data, num):
        file_path = request_data
        if not os.path.exists(file_path):
            LogPrint().error('第' + num + '个测试用例的文件路径配置无效，请检查[Request Data]字段配置的路径是否正确！')
        f = open(file_path, "r")            # 设置文件对象
        request_data = f.read()
        f.close()
        return request_data

