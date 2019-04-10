# -* encoding:utf-8 *-
import traceback
import pymysql
import sys
sys.path.append('E:\MyProgram\InterfaceTestFrame\Config')
from Config.read_config import DealCommonCfg


class MysqlDeal:
    dcc = DealCommonCfg()
    mylist = dcc.read_config('mysql')  # 获得配置文件中的信息内容
    mydic = {}  # 将获得的内容转换为字典类型
    for i in mylist:
        mydic[i[0].encode('UTF-8')] = i[1].encode('UTF-8')  # 这里将获得的数据由unicode类型转换为str类型,然后存入字典中
    host = mydic['host']
    user = mydic['user']
    password = mydic['password']
    port = int(mydic['port'])
    charset = mydic['charset']
    db = mydic['db']

    # 自定义的异常，抛出后用来捕获
    def myexcept(self,len):
        if len < 1:
            raise Exception("IDNullError", len)

    def conndb(self):
        print ("正在连接mysql服务器....")
        conn = pymysql.connect(  # 连接数据库，其实就是建立一个pymysql.connect()的实例对象conn，该对象有commit()、rollback()、cursor（）等属性
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            charset=self.charset,
            db=self.db
        )
        print ("连接服务器成功")
        cur = conn.cursor()         # 通过游标（指针）cursor的方式操作数据库，该代码作用是得到当前指向数据库的指针
        return (conn, cur)

    def selectdb(sql):                                                  # 查询数据库，查询条件中需要使用传入的参数
        cur,conn = MysqlDeal().conndb()
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) == 0:
            print ("查询结束,数据库无数据")
        else:
            return result

    def other_operatedb(sql):                                            # 增、删、改数据库的操作
        cur, conn = MysqlDeal().conndb()
        cur.execute(sql)
        conn.commit()

    def closedb(self):
        cur, conn = MysqlDeal().conndb()
        cur.close()
        conn.close()
