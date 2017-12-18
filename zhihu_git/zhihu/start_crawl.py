# -*-coding:utf-8-*- 
import pzhn
import mongDB
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
import cloud
import SimilarityDegree
import paint
import shutil #文件模块
import os
import emotion
import textprocessing
from pinyin import PinYin
class Using():
    def __init__(self):
        self.aa=pzhn.get("")#输入话题
        self.xs=SimilarityDegree.XiangSi()
        self.lo1=mongDB.Logger()
    def Analyse(self):
        client = ZhihuClient()
        self.aa.denglu(client)
        self.aa.findquestion(client)
        print'------------find','\n'
        list_q = self.aa.Analyse_question(self.aa.dic_name)
        print'----------q','\n'
        self.aa.Analyse_answer(list_q)#最慢
        print'-------------a','\n'
    def getciyun(self):
        # 得到词云回答者信息
        test1 = PinYin()
        test1.load_word()
        str1 = str(test1.hanzi2pinyin_split(string=str(self.aa.topic), split="-"))
        path1 =  'F:/zhihu/answer/people_qb.txt'
        cloud.ciyun1(path1,str1+'people')
        #得到词云，问题信息
        path2='F:/zhihu/answer/question_top10.txt'
        cloud.ciyun1(path2,str1+'question')
        path2 =  'F:/zhihu/answer/p_location.txt'
        cloud.ciyun1(path2,str1+'slocation')
    def niji(self):
        # 计算回答的基尼系数、
        niji = self.aa.lo.findd("Dic_name", self.aa.topic)
        list_qnum = []
        list_p = []
        list_p.append(1)
        count0 = 0
        aaa=0
        for i in self.lo1.db_table5.find():
           aaa=i['paint']
        for num in niji:
            if num == 0:
                count0 += 1
            list_qnum.append(num)
            list_p.append(float(num)/float(aaa))
        paint.zhitu(list_p)
        print pzhn.gini_coef(list_qnum), "do have answer is:%d" % count0

    def xiangsidu(self):
        lol = mongDB.Logger()
        count = 1
        dic_11={}
        for i in range(10):
            files1 = self.xs.analyse_nr('F:/zhihu/answer1' +str(count)+ '/')
            #print files1
            text = self.xs.change(files1)
            dic_11=self.xs.wordeee(text, self.aa.topic,'F:/zhihu/answer1' +str(count)+ '/'+"q.txt")
            count += 1
            #print dic_11
        lol.db_table7.insert(dic_11)  ###########
    def all_steps(self):
        #pzh.clean('F:/zhihu/answer1')
        if os.path.exists("F:/zhihu/answer11")==False:
            for i in range(10):
                os.mkdir("F:/zhihu/answer1"+str(i+1))
        if os.path.exists("F:/zhihu/answer11"):
            for i in range(10):
                pzhn.clean("F:/zhihu/answer1"+str(i+1))
        self.Analyse()  # 分析话题下的问题和回答得到，领袖意见/核心问题存入数据库，并形成绘图所需文件
        print'----------------Analyse','\n'
        self.niji()  # 得到尼基系数及劳伦兹曲线
        print'----------------niji','\n'
        self.getciyun()  # 得到词云
        print'----------------cloud', '\n'
        self.xiangsidu()  # 得到高频词汇并存入数据库的Pin表
        return 100
if __name__=='__main__':
    u=Using()
    u.all_steps()
