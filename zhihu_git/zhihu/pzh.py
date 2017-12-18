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
import SimilarityDegree
#count=0
TOKEN_FILE='token.pkl'
namen="匿名用户"
toname="医生"
#解决编码问题
reload(sys)
sys.setdefaultencoding('utf8')

#尼基系数
def gini_coef(wealths):
    cum_wealths = np.cumsum(sorted(np.append(wealths, 0)))
    sum_wealths = cum_wealths[-1]
    xarray = np.array(range(0, len(cum_wealths))) / np.float(len(cum_wealths)-1)
    yarray = cum_wealths / sum_wealths
    B = np.trapz(yarray, x=xarray)
    A = 0.5 - B
    return A / (A+B)

def maopao(array):
    for i in range(len(array)):
        for j in range(i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

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

def quick_sort(array,low,high,n):
     if low < high:
        key_index = sub_sort(array,low,high,n)
        quick_sort(array,low,key_index,n)
        quick_sort(array,key_index+1,high,n)
def clean(dir):
    pathDir = os.listdir(dir)
    for allDir in pathDir:
        os.remove(dir+'/'+allDir)
#'D:/' + u'py程序' + '/answer1'
def getpaint(authors,topic):
    list1=[]
    count=0
    lol = mongDB.Logger()
    for author in authors:
        dic_paint = {}
        dic_follow = {}
        dic_following = {}
        if author.over:
            continue
        else:
            if author.followings:
                for _,ii in zip(range(20),author.followings):
                    if ii.over:
                        name2=str(ii.over_reason)
                        continue
                    name2=str(ii.name)
                    if name2.find('.')!=-1:
                        name2=name2.replace('.',u"(点)")
                    #print name2,'----------------------------'
                    dic_following[name2]=ii.follower_count

            if author.followers:
                for _,follower in zip(range(20),author.followers):
                    if follower.over:
                        name1=str(follower.over_reason)
                        continue
                    name1=str(follower.name)
                    if name1.find('.')!=-1:
                        name1=name1.replace('.',u"(点)")
                        #print name1
                    dic_follow[name1]=follower.follower_count
            dic_paint['name']=author.name
            dic_paint['num']=author.follower_count
            dic_paint['follower']=dic_follow
            dic_paint['following']=dic_following
            dic_paint['topic']=topic
            ####################
            #js1=json.dumps(dic_paint)
            #js2=json.loads(js1)
            lol.db_table1.insert(dic_paint)


def getopic():
    topic=raw_input()########
    return topic


class get(object):
    def __init__(self):
        #"""Do nothing, by default."""
        self.qqcount=0
        self.dic_name={}
        self.ltable1=[]
        self.list_p=[]
        self.topic=getopic()
        self.lo= mongDB.Logger()
    def denglu(self,client):
        try:
            if os.path.isfile(TOKEN_FILE):
                client.load_token(TOKEN_FILE)
            else:
                client.login('+8618375419363', 'jry123456')
                client.save_token('token.pkl')
        except NeedCaptchaException:
            with open('a.gif', 'wb') as f:
                f.write(client.get_captcha())
            captcha = input('please input captcha:')
            client.login('email_or_phone', 'password', captcha)
        me=client.me()
    def findpeople(self,client):
        name=raw_input("输入名字")
        for result in client.search(name, search_type='PEOPLE'):
            people=result.obj
            #print people.headline
    #换成综合搜索
    def findquestion(self,client):
        listd4=[]
        dicd4={}
        qcount=0
        try:
            for _,result in zip(range(3),client.search_unfold(self.topic)):
                print"-------------------",'\n'
                r=result
                rr=r.obj
                re1=re.findall("zhcls.(.*)object",str(r.obj))
                if re1[0].find('Answer')!=-1:
                    question = rr.question
                    #list_name = qcount
                    list_name = [question.id,question.title,question.follower_count, question.comment_count, question.answer_count,
                            question.created_time,rr.question,question.updated_time,question.answers]
                    self.dic_name[qcount] = list_name
                    listd4.append(list_name[4])
                    qcount +=1
                    self.qqcount+=question.answer_count
                    #print dic_name[fcount][4]
                    #print rr.question.title
                else:
                    continue
        except:#SSL异常？
            pass
        dicd4["niji"]=listd4
        dicd4['paint']=self.qqcount
        self.lo.save_dicname(dicd4)
        print self.dic_name
        #self.lo.save_dicname(self.dic_name)
        #dic_name[1000]=qqcount
        #print len(dic_name)
        #quick_sort(dic_name,0,len(dic_name)-1)

    def Analyse_question(self,dic_name,qcount):
        dic_db1={}
        #print dic_name
        #核心问题挖掘
        list_q=[]
        count=len(dic_name)
        quick_sort(dic_name,0,count-1,4)
        file = open('F:/zhihu/answer/question_top10.txt', 'w')
        file.write("问题总数为："+str(len(dic_name))+'\n')
        countf = 0
        if count>=10:
            for _,list1 in zip(range(10),dic_name):
                countf+=1
                dicc={}
                str1=dic_name[list1][1]
                if dic_name[list1][1].find('.') != -1:
                    dic_name[list1][1] =dic_name[list1][1].replace('.', ':')
                dicc["title"]=dic_name[list1][1]
                dicc["回答数"]=dic_name[list1][4]
                dicc["创建时间"]=time.asctime(time.localtime((dic_name[list1][5])))

                self.ltable1.append(dicc)

                list_q.append(dic_name[list1])
                # #保存相关问题top10的回答
                try:
                    for _,answer in zip(range(5),dic_name[list1][8]):
                        if answer.author.over:
                            print(answer.author.over_reason)
                            continue###########
                            #break
                        else:
                            answer.save( 'answer1'+str(countf),answer.author.name)
                            fileq = open("F:/zhihu/" + 'answer1' + str(countf) + "/q.txt","w")
                            fileq.write(dicc["title"])
                except:
                    pass
                file.write(str(str1)+'\n')
                #print str1#核心问题
            dic_db1[self.topic]=self.ltable1
            dic_db1['qnum']=len(dic_name)
            #存入数据库
            self.lo.save_question(dic_db1)

        else:
            for list1 in dic_name:
                countf+=1
                dicc={}
                #print dic_name[list1][1]
                str1 = dic_name[list1][1]
                if dic_name[list1][1].find('.') != -1:
                    dic_name[list1][1] =dic_name[list1][1].replace('.', ':')
                dicc["title"] = dic_name[list1][1]
                dicc["回答数"] = dic_name[list1][4]
                dicc["创建时间"] = time.asctime(time.localtime((dic_name[list1][5])))
                self.ltable1.append(dicc)

                try:
                    for _,answer in zip(range(10),dic_name[list1][8]):
                        if answer.author.over:
                            print(answer.author.over_reason)
                            continue
                            #break
                        else:
                            answer.save('answer1'+str(countf),answer.author.name)
                            fileq=open("F:/zhihu/"+'answer1'+str(countf)+"/q.txt","w")
                            fileq.write(dicc["title"])
                except:
                    pass

                list_q.append(dic_name[list1])
                file.write(str(str1) + '\n')# 核心问题
            dic_db1[self.topic] = self.ltable1
            dic_db1['qnum'] = len(dic_name)
            # 存入数据库
            self.lo.save_question(dic_db1)
        file.close()

        #得到词云
        #get.Analyse_answer(self,list_q)
        return list_q
    def Analyse_answer(self,list_q):
        list_1=[]
        dict2 = {}
        dicomment={}
        dicall={}
        #print list_q[0][6].id
        time_get=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #print time_get
        list_a=[]
        list_author=[]
        list_best=[]
        for i in list_q:
            answers=i[6].answers
            try:
                for answer in answers:#具体到一个问题的所有回答都形成一个列表
                    list_answer=[answer.id,time_get,answer.comment_count,answer.created_time,answer.voteup_count,answer.
                        thanks_count,answer.updated_time,answer.author,answer.question.title,answer.question.id]
                    list_a.append(list_answer)
            except:
                pass
            if len(list_a)>=900:
                break
            print len(list_a)
            quick_sort(list_a,0,len(list_a)-1,4)

        #分析全部回答的相关信息
        countn=0
        countv=0
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

            if an[7].over:
                #print(an[7].over_reason)
                #continue
                break
            if an[7].name != u"匿名用户":
                dic_3['idhash']=an[7].id
                #print dic_3['idhash']
                dic_3['description']=an[7].description
                if counturl <= 10:
                    url = 'https://www.zhihu.com/question/' + str(an[9]) + '/answer/' + str(an[0])

                    dic_3['people_url']=url################################################

                    url1.zht(url, counturl, an[7].name,self.topic,'one')
                    counturl += 1

                if an[7].gender == 0:
                    countn += 1
                    if an[7].name.find('.') != -1:
                        namestr = str(an[7].name)
                        namestr = namestr.replace('.', ':')
                        dic_3["性别"]="男"
                        dic_3["name"] = namestr
                    else:
                        dic_3["name"]=an[7].name
                elif an[7].gender==1:
                    countv+=1
                    if an[7].name.find('.') != -1:
                        namestr = str(an[7].name)
                        namestr = namestr.replace('.', ':')
                        dic_3["性别"] = "女"
                        dic_3["name"] = namestr
                    else:
                        dic_3["name"] = an[7].name
                else:
                    dic_3["性别"] = "未填"
                    #str_qb+=str(countv)

                if an[7].business:
                    businestr = str(an[7].business.name)
                    if an[7].business.name.find('.') != -1:
                        businestr =businestr.replace('.', ':')
                    str_qb=str_qb+businestr
                    dic_3["职业"]=businestr
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
                #print str_qb

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
        #print "男性数目为：",countn
        #print "女性数目为：",countv
        print list_1
        dicall["回答者"] = list_1
        dicall["man_num"]=countn
        dicall["woman_num"]=countv
        dicall['location']=countlo
        dicall['topic']=self.topic

        self.lo.save_people(dicall)
        self.list_p = list_1

        #领袖意见1
        for i in self.lo.findd("People_all",self.topic):
            dic_vtop = {}
            list_vtop = []
            for _,ii in zip(range(10),i):
                list_vtop.append(ii)
        dic_vtop['top'] = list_vtop
        dic_vtop['type']="ling xiu one"
        dic_vtop['topic'] = self.topic
        self.lo.save_p10(dic_vtop)

        #领袖意见2
        list_comment=[]
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
        listc=list_comment[len(list_comment)-1][0:10]
        #print dicc
        cco=0
        for dicc in listc:
            cco+=1
            qid=dicc['questionid']
            aid=dicc['answerid']
            namec=dicc['name']
            url2='https://www.zhihu.com/question/' + str(qid) + '/answer/' + str(aid)

            url1.zht(url2,cco,namec, self.topic, 'two')
        #保存关系图数据
        getpaint(list_author,self.topic)

def getdic_location(list):
    dicall = {}
    for _,topic in zip(range(30),list) :
        name11=topic.name
        name1=name11
        name1=[]
        best=topic.best_answers
        for _,answer in zip(range(30),best):
            people=answer.author
            people1=people
            if people.name!=namen.decode("utf-8"):
                people1 = {}
                for _,location in zip(range(30),people.locations):
                    people1[people.name]=location.name
        name1.append(people)
        dicall[name11]=name1
    return dicall# dicall{topic_name：[best_answer_people[location]]}

def Anasly_location(dicall1):
    for file_tname in dicall1:
        file=open(file_tname+".txt",'w')

    print 'end'

def get_ptopic(list):#话题下的最佳回答者拥有最佳回答头衔的相似话题
    dicname={}
    for _,topic in zip(range(30),list) :
        name11=topic.name
        best=topic.best_answers
        for _,answer in zip(range(30),best):
            people=answer.author
            if people.name!=namen.decode("utf-8"):
                people1 = []
                for topic in people.badge.topics:
                    if topic.name.find(toname.decode("utf-8"))!=-1:
                        people1.append(topic.name)
                dicname[people.name]=people1
    return dicname

if __name__ == '__main__':
    clean('D:/' + u'py程序' + '/answer1')
    client = ZhihuClient()

    a=get()
    a.denglu(client)
    me = client.me()
    print me.id
    # a.findquestion(client)
    #
    # list_q=a.Analyse_question(a.dic_name,a.qqcount)
    #
    # a.Analyse_answer(list_q)
    # #Anasly_location(dicall1)
    # #
    # # # 得到词云回答者信息
    # # path1 = 'D:/' + u'py程序' + '/answer/people_qb.txt'
    # # hello.ciyun1(path1)
    # #
    # # #得到词云，问题信息
    # # path2='D:/' + u'py程序' + '/answer/question_top10.txt'
    # # hello.ciyun1(path2)
    # # path2 = 'D:/' + u'py程序' + '/answer/p_location.txt'
    # # hello.ciyun1(path2,'location')
    #
    # # 计算回答的基尼系数、
    # niji=a.lo.findd("Dic_name",a.topic)
    # list_qnum = []
    # list_p = []
    # list_p.append(1)
    # count0 = 0
    # for num in niji:
    #     if num == 0:
    #         count0 += 1
    #     list_qnum.append(num)
    #     # print dic_name[num][4]
    #     # print float(dic_name[num][4])/float(qcount)
    # print gini_coef(list_qnum), "没有回答的问题数为:%d" % count0
    print 'end all'













































