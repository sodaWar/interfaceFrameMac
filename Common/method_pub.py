# coding=utf-8
import datetime
import json


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

    # 根据用例执行情况,更新测试结果表的sql语句
    @ staticmethod
    def sql_deal_two(md, conn, cur, field, result_id):
            sql_one = 'select %s,case_total from test_result_data where result_id = %d' % (field, result_id)
            result_two = md.select_db(cur, sql_one)
            filed_num = result_two[0][0]
            case_total = result_two[0][1]

            sql_two = 'update test_result_data set %s = %d,case_total = %d where result_id = %d' \
                      % (field, filed_num + 1, case_total + 1, result_id)
            md.other_operate_db(conn, cur, sql_two)

    # 关联的接口数据处理,request_data是这次接口的请求数据,result_two是所关联的接口返回的数据
    @ staticmethod
    def request_data_deal(request_data, result_two):
        request_data_temp = eval(request_data)
        response_data_temp = json.loads(result_two)
        response_data = response_data_temp['data']

        special_values = []
        values = list(response_data.values())
        for x in values:
            if isinstance(x, dict):
                special_values.append(x)
            elif isinstance(x, list):
                for z in range(len(x)):
                    special_values.append(x[z])

        keys = list(request_data_temp.keys())
        for i in keys:
            temp = '$' + i
            if temp == request_data_temp[i]:
                try:
                    request_data_temp[i] = response_data[i]
                except KeyError:
                    for y in special_values:
                        try:
                            request_data_temp[i] = y[i]
                            # 从这里开始给请求数据的未知的数据重新赋值
                        except KeyError:
                            # print('未查找到该key')
                            continue
                        # 该special_values内的值可能是单纯一个值,如'www.baidu.com',这种情况使用y[i]就会报TypeError错误,不是字典所以使用y[i]报错
                        except TypeError:
                            continue
                        else:
                            # print('未捕获到该类型的错误或异常:', sys.exc_info()[0])
                            continue
                else:
                    # print('未捕获到该类型的错误或异常:', sys.exc_info()[0])
                    continue
            else:
                continue
        # 这里返回的最后请求数据中,一个key对应的值可能是str、list或者字典类型等

        request_data_last = str(request_data_temp).replace("\'", "\"")
        return request_data_last

    # 接口返回的数据结果中,如果有转义字符,存储到数据库后转义字符会自动消失,所以需要处理转义字符,使得存储到数据库中还保存该转义字符
    @staticmethod
    def response_data_deal(resp2):
        response_data_temp = json.loads(resp2)
        response_data = response_data_temp["data"]

        # 返回的结果如果data内容是list
        if isinstance(response_data, list):
            for i in response_data:
                if isinstance(i, dict):
                    key_one = list(i.keys())

                    for x in key_one:
                        if x == "goodsDetails":
                            i["goodsDetails"] = "the data no to deal with"
                else:
                    continue
        elif isinstance(response_data, dict):
            key_two = list(response_data.keys())

            for i in key_two:
                if i == "goodsDetails":
                    response_data["goodsDetails"] = "the data no to deal with"

        response_data_last = str(response_data_temp).replace("\'", "\"").replace("None", "\"\"")
        return response_data_last
