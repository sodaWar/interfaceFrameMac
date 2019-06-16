from Common.txt_file_pub import TxtFilePath
import requests
import json


# 常用的接口,需要检查被调用的单独封装处理,如登录接口等
class InterfaceDealAlone:
    """
    这里是四种请求数据格式的请求模板,这样每次新增了需要封装的函数,只需要url和data来请求模板就行
    第一个函数的接口请求数据的格式是application/json数据格式,因此该类型的请求方式如下（这里是该类型接口的所有请求模板）
    """
    @staticmethod
    def json_template(request_data, url):
        # 将str类型转换成字典类型,这里request_data参数是str类型,格式如:'{"page":1,"pageSize":9999}'这种方式,如果直接传入字典类型,可不用eval函数转换
        data = eval(request_data)
        payload = json.dumps(data)
        headers = {'content-type': "application/json"}
        response = requests.get(url=url, data=payload, headers=headers, timeout=5)

        resp = response.text
        return resp

    # 最常见的请求方式,以form表单形式请求
    @staticmethod
    def urlencoded_template(request_data, url):
        r = requests.post(url=url, data=request_data)
        return r.text

    """
    file_path是一个文件路径,如/user/random.txt,这里的txt文件和测试用例中请求方法为txt文件的区别在于接口,这里的接口是封装好之后用于其他
    接口使用的数据,测试用例的接口没有这个作用,只是单独的一次测试而已,注意这两种方式的txt文件区别
    """
    @staticmethod
    def form_data_template(file_path, url):
        files = {'file': open(file_path, 'rb')}
        r = requests.post(url, files=files)
        return r.text

    # xml参数数据格式如"""my xml"""
    @staticmethod
    def xml_template(xml, url):
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(url=url, data=xml, headers=headers)
        return r.text

    @staticmethod
    # 该函数的接口请求数据的格式是application/x-www-form-urlencoded数据格式,因此该类型的请求方式如下(这里是登录接口)
    def user_login():
        request_data = {'session_3rd': 'F11375CE782FD5836A549E6F1B908CF6HUku02',
                        'sessionId': 'F11375CE782FD5836A549E6F1B908CF6HUku02', 'storeId': 295, 'systemType': 'diancan'}
        url = 'https://test.ydxcx.net/api/user/userMsg'
        response_alone = InterfaceDealAlone.urlencoded_template(request_data, url)
        return response_alone

    # 使用form_data_template模板函数的一个实例,这里如果增加实例,修改form_template_one这个key值即可读取到相应的txt路径信息,该函数暂时用不到
    @staticmethod
    def form_data_test():
        url = 'https://test.ydxcx.net/api/user/userMsg'
        random_param_file = TxtFilePath().read_file_path('form_data_template')
        # txt文件的读取可配置化了,一个随机函数对应一个txt文件,增加随机函数时,需要在配置文件中增加路径名称,key值需要和函数名相同
        param_file_one = random_param_file['form_template_one']
        response_alone = InterfaceDealAlone.form_data_template(param_file_one, url)
        return response_alone
