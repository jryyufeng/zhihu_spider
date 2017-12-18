# -*-coding:utf-8-*- 
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
# client = ZhihuClient()
# user = 'email_or_phone'
# pwd = 'password'
# try:
#     client.login('+8618375419363', 'jry123456')
#     print(u"登陆成功!")
# except NeedCaptchaException: # 处理要验证码的情况
#     # 保存验证码并提示输入，重新登录
#     with open('a.gif', 'wb') as f:
#         f.write(client.get_captcha())
#     captcha = input('please input captcha:')
#     client.login('email_or_phone', 'password', captcha)
#
# client.save_token('token.pkl') # 保存token


# file=open("F:/zhihu/www.txt","w")
# file.write("uef")
import threading
import start_crawl
import mongDB
threadLock = threading.Lock()
threads = []

# class myThread(threading.Thread):
#     def __init__(self, threadID, name, counter,dicc):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#         self.dicc=dicc
#     def run(self):
#         lol = mongDB.Logger()
#         print "Starting " + self.name
#         print self.dicc
#         lol.db_table7.insert(self.dicc)
#         # u = start_crawl.Using()
#         # u.Analyse()
#
#         # 获得锁，成功获得锁定后返回True
#         # 可选的timeout参数不填时将一直阻塞直到获得锁定
#         # 否则超时后将返回False
#         threadLock.acquire()
#         # 释放锁
#         threadLock.release()
# dic1={'2':['q','w','e']}
# dic2={0:1,1:3}
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1,dic1)
# thread2 = myThread(2, "Thread-2", 2,dic1)
#
# # 开启新线程
# thread1.start()
# thread2.start()
#
# # 添加线程到线程列表
# threads.append(thread1)
# threads.append(thread2)
#
# # 等待所有线程完成
# for t in threads:
#     t.join()
# print "Exiting Main Thread"
b=1
for j,_,i in zip(range(2),range(5),range(10)):
    print i
