# -* encoding:utf-8 *-
import redis
from pymongo import MongoClient
import sys
sys.path.append('E:\MyProgram\InterfaceTestFrame\Config')
from Config.read_config import DealCommonCfg


class RedisDeal:
    dcc = DealCommonCfg()
    mylist = dcc.read_config('redis')  # 获得配置文件中的信息内容
    mydic = {}  # 将获得的内容转换为字典类型
    for i in mylist:
        mydic[i[0].encode('UTF-8')] = i[1].encode('UTF-8')  # 这里将获得的数据由unicode类型转换为str类型,然后存入字典中
    host = mydic['host']
    password = mydic['password']
    port = int(mydic['port'])

    def conndb(self):
        print ("正在连接redis服务器....")
        r = redis.Redis(host=self.host,port=self.port)
        print ("连接服务器成功")
        return r

    def operate(self,*dim):                                 # 这里可变参数dim至少有2个值,第一个是操作类型如set、get等,第二个是name值,第三个是value值可不传
        r = RedisDeal().conndb()
        list = []
        for i in dim:
            list.append(i)

        if list[0] == 'set':
            r.set(name=list[1],value=list[2])
        elif list[0] == 'delete':
            r.delete(list[1])
        elif list[0] == 'get':
            return r.get(name=list[1])
        else:
            print('操作类型或key值错误')

    def closedb(self):
        r = RedisDeal().conndb()
        r.connection_pool.disconnect()


class MongodbDeal:
    dcc = DealCommonCfg()
    mylist = dcc.read_config('mongodb')                          # 获得配置文件中的信息内容
    mydic = {}                                                  # 将获得的内容转换为字典类型
    for i in mylist:
        mydic[i[0].encode('UTF-8')] = i[1].encode('UTF-8')      # 这里将获得的数据由unicode类型转换为str类型,然后存入字典中
    host = mydic['host']
    password = mydic['password']
    port = int(mydic['port'])
    user = mydic['user']

    def conndb(self,db,collection):
        print ("正在连接mongodb服务器....")
        client=MongoClient(self.host,self.port)                 # 建立与数据库系统的连接

        db = client[db]                                         # 连接数据库
        db.authenticate(self.user, self.password)               # 认证用户密码
        collection = db[collection]
        print ("连接服务器成功")
        return db,collection

    def operate(self,handle,statement):                 # 这里statement格式的示例如{'id': '20190410','name': 'Jordan','age': 26,'gender': 'male'}
        md = MongodbDeal()
        db,collection = md.conndb('test_itf_one','test_itf_one')

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
            print('操作类型或执行语句错误')

    def closedb(self):
        client = MongoClient(self.host, self.port)      # 建立与数据库系统的连接
        client.close()
