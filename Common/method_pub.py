# coding=utf-8
import datetime


class Common_Method:
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