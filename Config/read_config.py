# coding=utf-8
import configparser
import os


class DealCommonCfg:
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "cfg.ini")
    # 创建管理对象
    conf = configparser.ConfigParser()

    def read_config(self,section):
        conf = self.conf
        # 读ini文件
        # conf.read(cfgpath, encoding="utf-8")  # python3
        conf.read(self.cfgpath)  # python2
        # 获取所有的section
        # sections = conf.sections()                                         # 返回list
        # print sections
        items = conf.items(section)
        return items                                                         # list里面对象是元祖

    # 参数必须遵从section,item的顺序
    def remove_config(self,*args):
        conf = self.conf
        conf.read(self.cfgpath)                                              # 先读取配置文件
        if args.__len__() > 1 :
            # 删除一个 section中的一个 item（以键值KEY为标识）
            conf.remove_option(args[0], args[1])
        else:
            # 删除一个 section
            conf.remove_section(args[0])

    def write_config(self,section):
        # 添加一个section
        conf = self.conf
        conf.add_section(section)

        # 往select添加key和value
        conf.set(section, "sender", "yoyo1@tel.com")
        conf.set(section, "port", "265")

        conf.write(open(self.cfgpath, "a"))                                    # 追加模式写入

    def set_config(self,section,key,value):
        conf = self.conf
        # 先读出来
        conf.read(self.cfgpath)

        # 修改section里面的值
        conf.set(section, key, value)

        conf.write(open(self.cfgpath, "r+"))                                    # r+模式


