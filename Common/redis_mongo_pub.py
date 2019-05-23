# -* encoding:utf-8 *-
import redis
from pymongo import MongoClient
from Logic.log_print import LogPrint
from Config.read_config import DealCommonCfg


class RedisDeal:
    dcc = DealCommonCfg()
    my_list = dcc.read_config('redis')  # 获得配置文件中的信息内容
    my_dic = {}  # 将获得的内容转换为字典类型
    for i in my_list:
        my_dic[i[0]] = i[1]                                    # python3的写法,以下是python2的写法
        # my_dic[i[0].encode('UTF-8')] = i[1].encode('UTF-8')  # 这里将获得的数据由unicode类型转换为str类型,然后存入字典中
    host = my_dic['host']
    password = my_dic['password']
    port = int(my_dic['port'])

    def conn_db(self):
        LogPrint().info("----------------正在连接redis服务器----------------")
        r = redis.Redis(host=self.host,port=self.port)
        LogPrint().info("----------------连接服务器成功----------------")
        return r

    @ staticmethod
    def operate(*dim):                                      # 这里可变参数dim至少有2个值,第一个是操作类型如set、get等,第二个是name值,第三个是value值可不传
        r = RedisDeal().conn_db()
        list_one = []
        for i in dim:
            list_one.append(i)

        if list_one[0] == 'set':
            r.set(name=list_one[1],value=list_one[2])
        elif list_one[0] == 'delete':
            r.delete(list_one[1])
        elif list_one[0] == 'get':
            return r.get(name=list_one[1])
        else:
            LogPrint().info("----------------操作类型或key值错误----------------")

    @ staticmethod
    def close_db():
        r = RedisDeal().conn_db()
        r.connection_pool.disconnect()


class MongodbDeal:
    dcc = DealCommonCfg()
    my_list = dcc.read_config('mongodb')                          # 获得配置文件中的信息内容
    my_dic = {}                                                  # 将获得的内容转换为字典类型
    for i in my_list:
        my_dic[i[0]] = i[1]
        # my_dic[i[0].encode('UTF-8')] = i[1].encode('UTF-8')      # 这里将获得的数据由unicode类型转换为str类型,然后存入字典中
    host = my_dic['host']
    password = my_dic['password']
    port = int(my_dic['port'])
    user = my_dic['user']

    def conn_db(self,db,collection):
        LogPrint().info("----------------正在连接mongo服务器----------------")
        client = MongoClient(self.host,self.port)                 # 建立与数据库系统的连接

        db = client[db]                                         # 连接数据库
        db.authenticate(self.user, self.password)               # 认证用户密码
        collection = db[collection]
        LogPrint().info("----------------连接服务器成功----------------")
        return db, collection

    @ staticmethod
    # 这里statement格式的示例如{'id': '20190410','name': 'Jordan','age': 26,'gender': 'male'}
    def operate(handle, statement):
        md = MongodbDeal()
        db, collection = md.conn_db('test_itf_one', 'test_itf_one')

        if handle == 'insert':
            collection.insert_one(statement)            # 同时插入多条数据使用insert_many()方法,参数需要以列表形式传递
        elif handle == 'find':
            result = collection.find_one(statement)     # 这里find_one()查询得到的是单个结果,find()则返回一个生成器对象
            return result
        elif handle == 'delete':
            collection.remove(statement)                # 另外两个删除方法delete_one()和delete_many()
        elif handle == 'update':
            collection.update(statement)
        else:
            LogPrint().info("----------------操作类型或执行语句错误----------------")

    def close_db(self):
        client = MongoClient(self.host, self.port)      # 建立与数据库系统的连接
        client.close()
