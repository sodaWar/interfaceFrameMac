# -* encoding:utf-8 *-
import pymysql
from Logic.log_print import LogPrint
from Config.read_config import DealCommonCfg


class MysqlDeal:
    dcc = DealCommonCfg()
    my_list = dcc.read_config('mysql')  # 获得配置文件中的信息内容
    my_dic = {}  # 将获得的内容转换为字典类型
    for i in my_list:
        my_dic[i[0].encode('UTF-8')] = i[1].encode('UTF-8')  # 这里将获得的数据由unicode类型转换为str类型,然后存入字典中
    host = my_dic['host']
    user = my_dic['user']
    password = my_dic['password']
    port = int(my_dic['port'])
    charset = my_dic['charset']
    db = my_dic['db']

    def conn_db(self):
        LogPrint().info("----------------正在连接mysql服务器----------------")
        conn = pymysql.connect(  # 连接数据库，其实就是建立一个pymysql.connect()的实例对象conn，该对象有commit()、rollback()、cursor（）等属性
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            charset=self.charset,
            db=self.db
        )
        LogPrint().info("----------------连接服务器成功----------------")
        cur = conn.cursor()         # 通过游标（指针）cursor的方式操作数据库，该代码作用是得到当前指向数据库的指针
        return (conn, cur)

    @ staticmethod
    def select_db(cur, sql):                                                  # 查询数据库，查询条件中需要使用传入的参数
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) == 0:
            LogPrint().info("----------------查询结束,数据库无数据----------------")
        else:
            return result

    @staticmethod
    def other_operate_db(conn, cur, sql):                                            # 增、删、改数据库的操作
        cur.execute(sql)
        conn.commit()

    @staticmethod
    def close_db(conn, cur):
        cur.close()
        conn.close()
