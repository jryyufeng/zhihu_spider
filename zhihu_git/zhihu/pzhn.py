# -*-coding:utf-8-*- 
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
from zhihu_oauth.exception import GetDataErrorException
import re
import os
import time
import sys
import numpy as np
import paint
import json
import mongDB
import url1
reload(sys)
sys.setdefaultencoding('utf8')
TOKEN_FILE='token.pkl'
#尼基系数
def gini_coef(wealths):
    cum_wealths = np.cumsum(sorted(np.append(wealths, 0)))
    sum_wealths = cum_wealths[-1]
    xarray = np.array(range(0, len(cum_wealths))) / np.float(len(cum_wealths)-1)
    yarray = cum_wealths / sum_wealths
    B = np.trapz(yarray, x=xarray)
    A = 0.5 - B
    return A / (A+B)
def clean(dir):
    pathDir = os.listdir(dir)
    for allDir in pathDir:
        os.remove(dir+'/'+allDir)
def sub_sort(array,low,high,n):
    key = array[low][n]
    while low < high:
        while low < high and array[high][n] <= key:
            high -= 1
        while low < high and array[high][n] > key:
            array[low][n] = array[high][n]
            low += 1
            array[high][n] = array[low][n]
    array[low][n] = key
    return low
def getpaint(authors,topic):
    lol = mongDB.Logger()
    for author in authors:
        dic_paint = {}
        dic_paint['name']=author.name
        dic_paint['num']=author.follower_count
        dic_paint['topic']=topic
        #######
        lol.db_table1.insert(dic_paint)
def quick_sort(array,low,high,n):
     if low < high:
        key_index = sub_sort(array,low,high,n)
        quick_sort(array,low,key_index,n)
        quick_sort(array,key_index+1,high,n)

class get():
    def __init__(self, topic):
        #"""Do nothing, by default."""
        self.qqcount=0
        self.dic_name={}
        self.ltable1=[]
        self.list_p=[]
        self.topic=topic
        self.lo= mongDB.Logger()
    def denglu(self,client):
        try:
            if os.path.isfile(TOKEN_FILE):
                client.load_token(TOKEN_FILE)
            else:
                client.login('youraccount', 'yourpassword')#输入账号密码
                client.save_token('token.pkl')
        except NeedCaptchaException:
            with open('a.gif', 'wb') as f:
                f.write(client.get_captcha())
            captcha = input('please input captcha:')
            client.login('email_or_phone', 'password', captcha)
        me=client.me()
    def findquestion(self,client):
        listd4=[]
        dicd4={}
        qcount=0
        try:
            for _,result in zip(range(10),client.search_unfold(self.topic)):
                print"-------------------",'\n'
                r=result
                rr=r.obj
                re1=re.findall("zhcls.(.*)object",str(r.obj))
                if re1[0].find('Answer')!=-1:
                    question = rr.question
                    list_name = [question.id,question.title,question.follower_count, question.comment_count, question.answer_count,
                            question.created_time,rr.question,question.updated_time]
                    self.dic_name[qcount] = list_name
                    listd4.append(list_name[4])
                    qcount +=1
                    self.qqcount+=question.answer_count

                else:
                    continue
        except:
            pass
        dicd4["niji"]=listd4
        dicd4['paint']=self.qqcount
        self.lo.save_dicname(dicd4)
        print self.dic_name
    def Analyse_question(self,dic_name):
        dic_db1={}
        list_q=[]
        count=len(dic_name)
        file = open('F:/zhihu/answer/question_top10.txt', 'w')
        file.write("question_num"+str(len(dic_name))+'\n')
        countf = 0
        if count>=10:
            quick_sort(dic_name, 0, count - 1, 4)
            for _,list1 in zip(range(10),dic_name):
                countf+=1
                dicc={}
                str1=dic_name[list1][1]
                if dic_name[list1][1].find('.') != -1:
                    dic_name[list1][1] =dic_name[list1][1].replace('.', ':')
                dicc["title"]=dic_name[list1][1]
                fileq = open("F:/zhihu/" + 'answer1' + str(countf) + "/q.txt", "w")
                fileq.write(dic_name[list1][1])
                #print countf, list_answer[8], '-----two', '\n'
                fileq.close()
                dicc["answer_num"]=dic_name[list1][4]
                dicc["create_time"]=time.asctime(time.localtime((dic_name[list1][5])))
                self.ltable1.append(dicc)
                list_q.append(dic_name[list1][6])
                # try:
                #     for _,answer in zip(range(10),dic_name[list1][8]):
                #         if answer.author.over:
                #             print(answer.author.over_reason)
                #             continue
                #         else:
                #             answer.save( 'answer1'+str(countf),answer.author.name)
                #             print '======','\n'
                #             fileq = open("F:/zhihu/" + 'answer1' + str(countf) + "/q.txt","w")
                #             fileq.write(dicc["title"])
                # except:
                #     pass
                file.write(str(str1)+'\n')
            dic_db1['topic']=self.topic
            dic_db1['top']=self.ltable1
            dic_db1['qnum']=len(dic_name)
            self.lo.save_question(dic_db1)

        else:
            for list1 in dic_name:
                countf+=1
                dicc={}
                str1 = dic_name[list1][1]
                if dic_name[list1][1].find('.') != -1:
                    dic_name[list1][1] =dic_name[list1][1].replace('.', ':')
                dicc["title"] = dic_name[list1][1]
                fileq = open("F:/zhihu/" + 'answer1' + str(countf) + "/q.txt", "w")
                fileq.write(dic_name[list1][1])
                #print countf, list_answer[8], '-----two', '\n'
                fileq.close()
                dicc["answer_num"] = dic_name[list1][4]
                dicc["create_time"] = time.asctime(time.localtime((dic_name[list1][5])))
                self.ltable1.append(dicc)
                # try:
                #     #for _,answer in zip(range(10),dic_name[list1][8]):
                #     for answer in dic_name[list1][8]:
                #         if answer.author.over:
                #             print(answer.author.over_reason)
                #             continue
                #         else:
                #             answer.save('answer1'+str(countf),answer.author.name)
                #             fileq=open("F:/zhihu/"+'answer1'+str(countf)+"/q.txt","w")
                #             fileq.write(dicc["title"])
                # except:
                #     pass
                list_q.append(dic_name[list1][6])
                file.write(str(str1) + '\n')# 核心问题
            dic_db1['topic'] = self.topic
            dic_db1['top'] = self.ltable1
            dic_db1['qnum'] = len(dic_name)
            # 存入数据库
            self.lo.save_question(dic_db1)
        file.close()
        return list_q
    def Analyse_answer(self,list_q):
        counta=1
        list_1=[]
        dicall={}
        time_get=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        list_a=[]
        list_author=[]
        for i in list_q:####################################3
            time.sleep(0.5)
            answers=i.answers
            try:
                countf=0
                for _,answer in zip(range(20),answers):#具体到一个问题的所有回答都形成一个列表
                    list_answer=[answer.id,time_get,answer.comment_count,answer.created_time,answer.voteup_count,answer.
                        thanks_count,answer.updated_time,answer.author,answer.question.title,answer.question.id]
                    list_a.append(list_answer)
                    countf+=1
                    #print list_answer[8], '-----one', '\n'
                    #answer.save('answer1' + str(countf+1), answer.author.name)
                    if countf<=10:
                        filean=open("F:/zhihu/"+'answer1' + str(countf)+'/'+list_answer[7].name+'.html',"w")
                        filean.write(answer.content)
                        filean.close()
                        #print '======', '\n'
                        # fileq = open("F:/zhihu/" + 'answer1' + str(countf) + "/q.txt", "w")
                        # fileq.write(list_answer[8])
                        # print countf,list_answer[8],'-----two','\n'
                        # fileq.close()

            except:
                pass
            if len(list_a)>600:########################
                break
            print len(list_a)
            quick_sort(list_a,0,len(list_a)-1,4)

        #分析全部回答的相关信息
        countn=0
        countv=0
        dic_paint={}
        list_lo=[]
        file_qb=open('F:/zhihu/answer/people_qb.txt', 'w')
        file_location=open('F:/zhihu/answer/p_location.txt', 'w')
        count=1
        counturl=1
        for an in list_a:
            dic_3={}
            dic_3["comment"]=an[2]
            dic_3["vote"]=an[4]
            dic_3["answerid"]=an[0]
            dic_3["questionid"]=an[9]
            str_qb = " "
            if count<=10:
                list_author.append(an[7])
                count+=1
            if an[7].name != u"匿名用户":
                dic_3['idhash']=an[7].id
                dic_3['description']=an[7].description
                if counturl <= 10:
                    url = 'https://www.zhihu.com/question/' + str(an[9]) + '/answer/' + str(an[0])
                    dic_3['people_url']=url
                    url1.zht(url, counturl, an[7].name,self.topic,'one')
                    counturl += 1

                dic_paint['num'] = an[7].follower_count
                dic_paint['topic'] = self.topic

                if an[7].gender == 0:
                    countn += 1
                    if an[7].name.find('.') != -1:
                        namestr = str(an[7].name)
                        namestr = namestr.replace('.', ':')
                        dic_3["Gender"]="man"
                        dic_3["name"] = namestr
                    else:
                        dic_3["name"]=an[7].name
                elif an[7].gender==1:
                    countv+=1
                    if an[7].name.find('.') != -1:
                        namestr = str(an[7].name)
                        namestr = namestr.replace('.', ':')
                        dic_3["Gender"] = "woman"
                        dic_3["name"] = namestr
                    else:
                        dic_3["name"] = an[7].name
                else:
                    dic_3["Gender"] = "no"
                    #str_qb+=str(countv)

                if an[7].business:
                    businestr = str(an[7].business.name)
                    if an[7].business.name.find('.') != -1:
                        businestr =businestr.replace('.', ':')
                    str_qb=str_qb+businestr
                    dic_3["job"]=businestr
                if an[7].educations:
                    for education in an[7].educations:
                        if 'school' in education:
                            schoolstr = str(education.school.name)
                            if education.school.name.find('.') != -1:
                                schoolstr = schoolstr.replace('.', ':')
                            str_qb += schoolstr
                            dic_3['school']=schoolstr
                        if 'major' in education:
                            majorstr= str(education.major.name)
                            if education.major.name.find('.') != -1:
                                majorstr = majorstr.replace('.', ':')
                            str_qb += majorstr
                            dic_3['major']=majorstr
                if an[7].locations:
                    for location in an[7].locations:
                        #print location.name
                        file_location.write(location.name)
                        locstr=location.name
                        if locstr.find('.') != -1:
                            locstr = locstr.replace('.', ':')
                        list_lo.append(locstr)
                        dic_3['location']=locstr
                list_1.append(dic_3)
            else:
                str_qb+=u"匿名用户"
                dic_3['name']="匿名用户"
                list_1.append(dic_3)
            file_qb.write(str_qb+'\n')

        countlo = {}
        for item in list_lo:
            item=str(item)
            if item.find('.')!=-1:
                item=item.replace('.', ':')
            countlo[item] = countlo.get(item, 0) + 1
        file_qb.close()
        file_location.close()
        dicall["person"] = list_1
        dicall["man_num"]=countn
        dicall["woman_num"]=countv
        dicall['location']=countlo
        dicall['topic']=self.topic
        self.lo.save_people(dicall)
        # 保存关系图数据
        self.lo.db_table1.insert(dic_paint)
        self.list_p = list_1
        # 领袖意见1
        for i in self.lo.findd("People_all", self.topic):
            dic_vtop = {}
            list_vtop = []
            for _, ii in zip(range(10), i):
                list_vtop.append(ii)
        dic_vtop['top'] = list_vtop
        dic_vtop['type'] = "ling xiu one"
        dic_vtop['topic'] = self.topic
        self.lo.save_p10(dic_vtop)

        # 领袖意见2
        list_comment = []
        for i in self.lo.findd("People_all", self.topic):
            for ii in range(len(i)):
                for j in range(ii):
                    if i[j]['comment'] < i[j + 1]['comment']:
                        i[j], i[j + 1] = i[j + 1], i[j]
            list_comment.append(i)
        for i in list_comment:
            dic_ctop = {}
            dic_ctop['top'] = i[0:10]
            dic_ctop['type'] = "liny xiu two"
            dic_ctop['topic'] = self.topic
            self.lo.save_p10(dic_ctop)
        listc = list_comment[len(list_comment) - 1][0:10]
        # print dicc
        cco = 0
        for dicc in listc:
            cco += 1
            qid = dicc['questionid']
            aid = dicc['answerid']
            namec = dicc['name']
            url2 = 'https://www.zhihu.com/question/' + str(qid) + '/answer/' + str(aid)
            url1.zht(url2, cco, namec, self.topic, 'two')
        # 保存关系图数据
        getpaint(list_author, self.topic)

