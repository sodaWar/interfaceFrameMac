# coding=utf-8
from Logic.log_print import LogPrint
import configparser
import os


class DealCommonCfg:
    cur_path = os.path.dirname(os.path.realpath(__file__))
    cfg_path = os.path.join(cur_path, "cfg.ini")
    # 创建管理对象
    conf = configparser.ConfigParser()

    def read_config(self, section):
        conf = self.conf
        # 读ini文件
        conf.read(self.cfg_path, encoding="utf-8")  # python3
        # conf.read(self.cfg_path)  # python2
        # 获取所有的section
        # sections = conf.sections()                                         # 返回list
        # print sections
        items = conf.items(section)
        return items                                                         # list里面对象是元祖

    # 参数必须遵从section,item的顺序
    def remove_config(self, *args):
        conf = self.conf
        conf.read(self.cfg_path)                                              # 先读取配置文件
        if args.__len__() > 1 :
            # 删除一个 section中的一个 item（以键值KEY为标识）
            conf.remove_option(args[0], args[1])
            LogPrint().info("----------------删除配置文件中的item成功----------------")
        else:
            # 删除一个 section
            conf.remove_section(args[0])
            LogPrint().info("----------------删除配置文件中的section成功----------------")

    def write_config(self, section):
        # 添加一个section
        conf = self.conf
        conf.add_section(section)

        # 往select添加key和value
        conf.set(section, "sender", "yoyo1@tel.com")
        conf.set(section, "port", "265")

        conf.write(open(self.cfg_path, "a"))                                    # 追加模式写入
        LogPrint().info("----------------写入配置文件成功----------------")

    def set_config(self, section, key, value):
        conf = self.conf
        # 先读出来
        conf.read(self.cfg_path)

        # 修改section里面的值
        conf.set(section, key, value)

        conf.write(open(self.cfg_path, "r+"))                                    # r+模式
        LogPrint().info("----------------修改配置文件成功----------------")


