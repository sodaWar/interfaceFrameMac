import queue
import sys
from threading import Thread


# working thread
class Worker(Thread):
    worker_count = 0
    timeout = 1

    def __init__(self, work_queue, result_queue, **kwds):
        Thread.__init__(self, **kwds)
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon(True)
        self.workQueue = work_queue
        self.resultQueue = result_queue
        self.start()

    def run(self):
        """
        the get-some-work, do-some-work main loop of worker threads
        :return:
        """
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=Worker.timeout)
                res = callable(*args, **kwds)
                print("worker[%2d]: %s" % (self.id, str(res)))
                self.resultQueue.put(res)
                # time.sleep(Worker.sleep)
            except queue.Empty:
                break
            except Exception:
                print('worker[%2d]' % self.id, sys.exc_info()[:2])
                raise


class WorkerManager:
    def __init__(self, num_of_workers=10, timeout=2):
        self.workQueue = queue.Queue()
        self.resultQueue = queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruit_threads(num_of_workers)

    def _recruit_threads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue)
            self.workers.append(worker)

    def wait_for_complete(self):
        # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        print("All jobs are are completed.")

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)


# coding:utf-8
# import random
# import threading
# import time
# import queue
#
# '''
# 实现了一个生产线程，用于往队列中添加随机数10个，
# 实现了一个消费线程，分别消耗奇数随机数和偶数随机数
# '''
#
#
# class producer(threading.Thread):
#     def __init__(self, t_name, queue):
#         threading.Thread.__init__(self, name=t_name)
#         self.data = queue
#
#     def run(self):
#         for i in range(5):
#             random_num = random.randint(1, 99)
#             print("%s : %s 生产了一个随机数\033[31;0m %d \033[0m放入队列中" % (time.ctime(), self.getName(), random_num))
#             self.data.put(random_num)
#             time.sleep(1)
#         print("生产线程完成！！")
#
#
# class consumer(threading.Thread):
#     def __init__(self, t_name, queue):
#         threading.Thread.__init__(self, name=t_name)
#         self.data = queue
#
#     def run(self):
#         while True:
#             try:
#                 tmp_num = self.data.get(1, 5)  # 定义超时时间5秒,如果还不能读取到值就报Empty异常
#                 if tmp_num % 2 == 0:
#                     print("%s : %s 消耗了一个队列中的偶数随机数\033[31;0m %d \033[0m" % (time.ctime(), self.getName(), tmp_num))
#                     time.sleep(2)
#                 else:
#                     print("%s : %s 消耗了一个队列中的奇数随机数\033[31;0m %d \033[0m" % (time.ctime(), self.getName(), tmp_num))
#                     time.sleep(2)
#             except:
#                 print("消费线程完成！！")  # 一旦到达超时时间5秒，会抛异常，break退出循环
#                 break
#
#
# def main():
#     queue2 = queue.Queue(0)
#     pro = producer('Pro', queue2)
#     con = consumer('Con', queue2)
#     pro.start()
#     con.start()
#     pro.join()
#     con.join()
#     print('All threads complete!!!')
#
#
# if __name__ == '__main__':
#     main()


# import threading
# import time
#
# sm = threading.Semaphore(3)
#
#
# def connectDb():
#     sm.acquire()
#
#     print(threading.currentThread().getName()+' connecting to db...\n')
#
#     time.sleep(3)
#
#     print(threading.currentThread().getName()+' released db...\n')
#
#     sm.release()
#
#
# if __name__ == '__main__':
#     for n in range(4):
#         t = threading.Thread(target=connectDb, args=())
#         t.start()


# from concurrent.futures import ThreadPoolExecutor
# import threading
# import time
#
# # 定义一个准备作为线程任务的函数
# def action(max):
#     my_sum = 0
#     for i in range(max):
#         print(threading.current_thread().name + '  ' + str(i))
#         my_sum += i
#     return my_sum
# # 创建一个包含2条线程的线程池
# pool = ThreadPoolExecutor(max_workers=2)
# # 向线程池提交一个task, 50会作为action()函数的参数
# future1 = pool.submit(action, 50)
# # 向线程池再提交一个task, 100会作为action()函数的参数
# future2 = pool.submit(action, 100)
# # 判断future1代表的任务是否结束
# print(future1.done())
# time.sleep(3)
# # 判断future2代表的任务是否结束
# print(future2.done())
# # 查看future1代表的任务返回的结果
# print(future1.result())
# # 查看future2代表的任务返回的结果
# print(future2.result())
# # 关闭线程池
# pool.shutdown()


# from concurrent.futures import ThreadPoolExecutor
# import threading
# import time
#
# # 定义一个准备作为线程任务的函数
# def action(max):
#     my_sum = 0
#     for i in range(max):
#         print(threading.current_thread().name + '  ' + str(i))
#         my_sum += i
#     return my_sum
# # 创建一个包含2条线程的线程池
# with ThreadPoolExecutor(max_workers=2) as pool:
#     # 向线程池提交一个task, 50会作为action()函数的参数
#     future1 = pool.submit(action, 50)
#     # 向线程池再提交一个task, 100会作为action()函数的参数
#     future2 = pool.submit(action, 100)
#     def get_result(future):
#         print(future.result())
#     # 为future1添加线程完成的回调函数
#     future1.add_done_callback(get_result)
#     # 为future2添加线程完成的回调函数
#     future2.add_done_callback(get_result)
#     print('--------------')


# from concurrent.futures import ThreadPoolExecutor
# import threading
# # 定义一个准备作为线程任务的函数
#
#
# def action(max):
#     my_sum = 0
#     for i in range(max):
#         print(threading.current_thread().name + '  ' + str(i))
#         my_sum += i
#     return my_sum
#
#
# # 创建一个包含4条线程的线程池
# with ThreadPoolExecutor(max_workers=4) as pool:
#     # 使用线程执行map计算
#     # 后面元组有3个元素，因此程序启动3条线程来执行action函数
#     results = pool.map(action, (5, 10, 15, 20, 25))
#     print('--------------')
#     for r in results:
#         print(r)


"""
random.randint(a, b):用于生成一个指定范围内的整数。
其中参数a是下限，参数b是上限，生成的随机数n: a <= n <= b
random.choice(sequence)：从序列中获取一个随机元素
参数sequence表示一个有序类型（列表，元组，字符串）
该函数是用来实现可设置持续运行时间、线程数及时间间隔的多线程异步post请求功能
"""
# import http.client
# import json
# import time
# import threading
#
#
# # 创建请求函数
# def post_request(thread_num):
#     post_json = {}
# # 定义需要进行发送的数据
#     post_data = json.dumps(post_json)
#     # 定义一些文件头
#     header_data = {"content-type": "application/json"}
#     # 接口
#     url = "/v1/query"
#     # 请求服务,例如：www.baidu.com
#     host_server = ""
#     # 连接服务器
#     conn = http.client.HTTPConnection(host_server)
#     # 发送请求
#     conn.request(method="POST", url=url, body=post_data, headers=header_data)
#     # 获取请求响应
#     response = conn.getresponse()
#     # 打印请求状态
#     if response.status in range(200, 300):
#         print(u"线程" + str(thread_num) + u"状态码：" + str(response.status))
#     conn.close()
#
#
# def run(thread_num, intern_time, duration):
#     # 创建数组存放线程
#     threads = []
#     try:
#         # 创建线程
#         for i in range(1, thread_num):
#             # 针对函数创建线程
#             t = threading.Thread(target=post_request, args=(i,))
#         # 把创建的线程加入线程组
#             threads.append(t)
#     except Exception:
#         print(Exception)
#
#     try:
#         # 启动线程
#         for thread in threads:
#             thread.setDaemon(True)
#             thread.start()
#             time.sleep(intern_time)
#     # 等待所有线程结束
#         for thread in threads:
#             thread.join(duration)
#     except Exception:
#         print(Exception)
#
#
# if __name__ == '__main__':
#     star_time = time.strftime("%Y%m%d%H%M%S")
#     now = time.strftime("%Y%m%d%H%M%S")
#     duration_time = input(u"输入持续运行时间:")
#     while (star_time + str(duration_time)) != now:
#         run(10, 1, int(duration_time))
#     now = time.strftime("%Y%m%d%H%M%S")



# import request
# import socket
# from Logic.test3 import *
#
#
# def main():
#     url_list = {"sina": "http://www.sina.com.cn",
#                 "sohu": "http://www.sohu.com",
#                 "yahoo": "http://www.yahoo.com",
#                 "xiaonei": "http://www.xiaonei.com",
#                 "qihoo": "http://www.qihoo.com",
#                 "laohan": "http://www.laohan.org",
#                 "eyou": "http://www.eyou.com",
#                 "chinaren": "http://www.chinaren.com",
#                 "douban": "http://www.douban.com",
#                 "163": "http://www.163.com",
#                 "daqi": "http://www.daqi.com",
#                 "qq": "http://www.qq.com",
#                 "baidu_1": "http://www.baidu.com/s?wd=asdfasdf",
#                 "baidu_2": "http://www.baidu.com/s?wd=dddddddf",
#                 "google_1": "http://www.baidu.com/s?wd=sadfas",
#                 "google_2": "http://www.baidu.com/s?wd=sadflasd",
#                 "hainei": "http://www.hainei.com",
#                 "microsoft": "http://www.microsoft.com",
#                 "wlzuojia": "http://www.wlzuojia.com"}
#
#     # 使用线程池
#     socket.setdefaulttimeout(10)
#     print('start testing')
#     wm = WorkerManager(50)
#     for url_name in url_list.keys():
#         wm.add_job(do_get_con, url_name, url_list[url_name])
#     wm.wait_for_complete()
#     print('end testing')
#
#
# def do_get_con(url_name, url_link):
#     try:
#         fd = request.urlopen(url_link)
#         data = fd.read()
#         f_hand = open("/tmp/ttt/%s" % url_name, "w")
#         f_hand.write(data)
#         f_hand.close()
#     except Exception:
#         pass
#
#
# if __name__ == "__main__":
#     main()





# Python queue队列，实现并发，在网站多线程推荐最后也一个例子,比这货简单，但是不够规范

# encoding: utf-8

# from queue import Queue  # Queue在3.x中改成了queue
# import random
# import threading
# import time
#
#
# class Producer(threading.Thread):
#     """
#     Producer thread 制作线程
#     """
#     def __init__(self, t_name, queue):  # 传入线程名、实例化队列
#         threading.Thread.__init__(self, name=t_name)  # t_name即是threadName
#         self.data = queue
#
#     """
#     run方法 和start方法:
#     它们都是从Thread继承而来的，run()方法将在线程开启后执行，
#     可以把相关的逻辑写到run方法中（通常把run方法称为活动[Activity]）；
#     start()方法用于启动线程。
#     """
#
#     def run(self):
#         for i in range(5):  # 生成0-4五条队列
#             print("%s: %s is producing %d to the queue!" % (time.ctime(), self.getName(), i))  # 当前时间t生成编号d并加入队列
#             self.data.put(i)  # 写入队列编号
#             time.sleep(random.randrange(10) / 5)  # 随机休息一会
#         print("%s: %s producing finished!" % (time.ctime(), self.getName))  # 编号d队列完成制作
#
#
# class Consumer(threading.Thread):
#     """
#     Consumer thread 消费线程，感觉来源于COOKBOOK
#     """
#     def __init__(self, t_name, queue):
#         threading.Thread.__init__(self, name=t_name)
#         self.data = queue
#
#     def run(self):
#         for i in range(5):
#             val = self.data.get()
#             print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val))  # 编号d队列已经被消费
#             time.sleep(random.randrange(10))
#         print("%s: %s consuming finished!" % (time.ctime(), self.getName()))  # 编号d队列完成消费
#
#
# def main():
#     """
#     Main thread 主线程
#     """
#     queue = Queue()  # 队列实例化
#     producer = Producer('Pro.', queue)  # 调用对象，并传如参数线程名、实例化队列
#     consumer = Consumer('Con.', queue)  # 同上，在制造的同时进行消费
#     producer.start()  # 开始制造
#     consumer.start()  # 开始消费
#     """
#     join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
# 　　join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
#     """
#     producer.join()
#     consumer.join()
#     print('All threads terminate!')
#
#
# if __name__ == '__main__':
#     main()


# import time
# import threading
# import queue
#
#
# # 一个线程，间隔一定的时间，把一个递增的数字写入队列
# # 生产者
# class Producer(threading.Thread):
#
#     def __init__(self, work_queue):
#         super().__init__()  # 必须调用
#         self.work_queue = work_queue
#
#     def run(self):
#         num = 1
#         while True:
#             self.work_queue.put(num)
#             num = num + 1
#             time.sleep(1)  # 暂停1秒
#
#
# # 一个线程，从队列取出数字，并显示到终端
# class Printer(threading.Thread):
#
#     def __init__(self, work_queue):
#         super().__init__()  # 必须调用
#         self.work_queue = work_queue
#
#     def run(self):
#         while True:
#             num = self.work_queue.get()  # 当队列为空时，会阻塞，直到有数据
#             print(num)
#
#
# def main():
#     work_queue = queue.Queue()
#
#     producer = Producer(work_queue)
#     producer.daemon = True  # 当主线程退出时子线程也退出
#     producer.start()
#
#     printer = Printer(work_queue)
#     printer.daemon = True  # 当主线程退出时子线程也退出
#     printer.start()
#
#     work_queue.join()  # 主线程会停在这里，直到所有数字被get()，并且task_done()，因为没有调用task_done()，所在这里会一直阻塞，直到用户按^C
#
#
# if __name__ == '__main__':
#     main()


# import queue
# import threading
# import time
#
# exitFlag = 0
#
#
# class MyThread (threading.Thread):          # 这种定义类的方式是重写一个类,继承threading.Thread
#     def __init__(self, thread_id, name, q):
#         threading.Thread.__init__(self)
#         self.threadID = thread_id
#         self.name = name
#         self.q = q
#
#     def run(self):
#         print("开启线程：" + self.name + "      " + str(self.threadID))
#         process_data(self.name, self.q)
#         print("退出线程：" + self.name)
#
#
# def process_data(thread_name, q):
#     while not exitFlag:
#         queueLock.acquire()
#         if not workQueue.empty():
#             data = q.get()
#             queueLock.release()
#             print("%s processing %s" % (thread_name, data))
#         else:
#             queueLock.release()
#         time.sleep(1)
#
#
# threadList = ["线程-1", "线程-2", "线程-3", "线程-4", "线程-5", "线程-6", "线程-7"]
# nameList = [["One", "Two", "Three", "Four", "Five"], ["1", "2", "3", "4", "5"]]
# queueLock = threading.Lock()                # 返回锁对象,一旦某个线程获得了这个锁,其他的线程要想获得他就必须阻塞,直到锁被释放
# workQueue = queue.Queue(10)                 # 设置队列的大小
# threads = []                                # 线程数组,所有启动线程的列表
# threadID = 1
#
# # 创建新线程
# for tName in threadList:
#     thread = MyThread(threadID, tName, workQueue)
#     thread.start()
#     threads.append(thread)
#     threadID += 1
#
# # 填充队列
# for word in nameList:
#     queueLock.acquire()
#
#     for i in word:
#         workQueue.put(i)                    # 往队列中存放元素
#     queueLock.release()
#
# # 等待队列清空
# while not workQueue.empty():
#     pass
#
# # 通知线程是时候退出
# exitFlag = 1
#
# # 等待所有线程完成,Thread类的join()方法是用来等待子线程执行完毕以后,主线程才会再关闭,否则主线程不会等待子线程执行完毕再结束自身
# for t in threads:
#     t.join()
# print("退出主线程")
