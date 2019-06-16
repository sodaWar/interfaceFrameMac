# coding=utf-8
import time
import hashlib
import json


class InterfaceHeadDeal:
    @ staticmethod
    def unicode2str(u):
        return u if isinstance(u, str) else u.encode('utf8')

    @ staticmethod
    def get_millis():
        # 同Java System.currentTimeMillis()方法
        return str(int(round(time.time() * 1000)))

    @ staticmethod
    def get_md5hex(source):
        # 同Java md5Hex()方法
        m = hashlib.md5()
        m.update(source.encode("utf8"))
        return m.hexdigest()

    @ staticmethod
    # 接口头部处理方法,主要是部分数据需要加密处理,然后添加到头部信息内,在发送请求时一起传送头部的参数,如果接口不需要,则不用该函数处理头部信息
    def sign_headers(payload, request_data_type):
        access_key = '7ef9a26e5a32ca9699b930541875dbfb'
        secret_key = '8040c5dbf6978f315e104e5c0bca3e8e2baa4221'
        req_time = InterfaceHeadDeal().get_millis()
        sign = ''
        if request_data_type == 'Data':
            sign = ''.join([secret_key, req_time, payload])
        elif request_data_type == 'Form':
            payload2 = json.dumps(payload)
            sign = ''.join([secret_key, req_time, payload2])

        sign = InterfaceHeadDeal.get_md5hex(InterfaceHeadDeal.get_md5hex(sign))
        headers = {
            'accesskey': access_key,
            'reqtime': req_time,
            'sign': sign,
            'content-type': "application/json"
        }
        return headers


