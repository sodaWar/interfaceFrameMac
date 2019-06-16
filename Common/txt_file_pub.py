from Logic.log_print import LogPrint
from Config.read_config import DealCommonCfg


class TxtFilePath:
    """
       读取配置文件中txt文件的路径信息(不是读取txt文件内容,而是先找到txt文件的路径)
       这里测试用例中的txt文件路径不需要写入配置文件中,直接从excel表格中读取即可,不需要多此一举
       """

    @staticmethod
    def read_file_path(txt_type):
        dcc = DealCommonCfg()
        if txt_type == 'random_param':
            LogPrint().info("----------------读取配置文件中随机函数的txt文件路径信息----------------")
        elif txt_type == 'form_data_template':
            LogPrint().info("----------------读取配置文件中以form_data方式请求的函数所需的txt文件路径信息----------------")
        else:
            LogPrint().info("----------------txt的类型错误,读取不到配置文件中的路径信息----------------")

        my_list = dcc.read_config(txt_type)  # 获得配置文件中的信息内容
        my_dic = {}  # 将获得的内容转换为字典类型
        for i in my_list:
            my_dic[i[0]] = i[1]
        return my_dic
