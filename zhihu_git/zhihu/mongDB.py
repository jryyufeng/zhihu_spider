# -*-coding:utf-8-*- 
import re
import pymongo
class Logger():
    def __init__(self):
        self.first=True
        self.mongo_client=pymongo.MongoClient('localhost',27017)

        self.db=self.mongo_client['runoob']#  王晓玮电脑需要改为data_of_h

        self.db_table1 = self.db['P_paint']
        self.db_table2=self.db['People_all']
        self.db_table3 = self.db['People_top10']
        self.db_table4 = self.db['Question_top10']
        self.db_table5=self.db['Dic_name']
        self.db_table6 = self.db['P_localtion']
        self.db_table7 = self.db['Pin']
    def save_paint(self,json1):
        self.db_table1.insert(json1)
    def save_p10(self,p10):
        self.db_table3.insert(p10)
    def save_people(self, pall):
        self.db_table2.insert(pall)
    def save_question(self, location):
        self.db_table4.insert(location)
    def save_dicname(self, dic_name):
        self.db_table5.remove()
        self.db_table5.insert(dic_name)

    def save_test(self, dic_name):
        self.db_table6.insert(dic_name)
    def shanchu(self,table):
        if(table=='P_paint'):
            self.db_table1.remove()
        elif(table=='People_all'):
            self.db_table2.remove()
        elif(table=='People_top10'):
            self.db_table3.remove()
        elif(table=='Dic_name'):
            self.db_table5.remove()
        else:
            self.db_table4.remove()
    def findd(self,table,topic):
        count=0
        list1=[]
        list2=[]
        if table=='Dic_name':
            for i in self.db_table5.find():
                return i['niji']
        elif table=='People_all':
            for i in self.db_table2.find({"topic":topic}):#此处的topic需要提供
                list1.append( i["person"])
                #print len(list1)
            return list1
        elif table=='People_top10':
            for i in self.db_table3.find():
                return i
        elif table=='Pin':
            for i in self.db_table7.find({"itstopic":topic}):
                list2.append(i)
            return list2
def maopao(array):
    for i in range(len(array)):
        for j in range(i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
if __name__=='__main__':
    #ceshi2('D:/' + u'py程序' + '/answer1/BbX5.html')
    list1=[]
    list1.append(1)
    lo=Logger()
    #lo.save_p10(list1)
    count=0
    list_comment=[]
    #print lo.findd("People_all",u"华为闪存")
    # for i in lo.findd("People_all",u"华为闪存"):
    #     dic_vtop = {}
    #     list_vtop = []
    #     for _,ii in zip(range(10),i):
    #         list_vtop.append(ii)
    #     dic_vtop['top'] = list_vtop
    #     dic_vtop['topic'] = u"华为闪存"
    #     lo.save_p10(dic_vtop)
    # for i in lo.findd("People_all", u"华为闪存"):
    #         for ii in range(len(i)):
    #             for j in range(ii):
    #                 if i[j]['comment'] < i[j + 1]['comment']:
    #                     i[j], i[j + 1] = i[j + 1], i[j]
    #         list_comment.append(i)
    # for i in list_comment:
    #     dic_ctop={}
    #     dic_ctop['top']=i[0:10]
    #     dic_ctop['type'] = "liny xiu two"
    #     dic_ctop['topic']=u"华为闪存"
    #     lo.save_p10(dic_ctop)
    # print"________________________________________"

    # for i in lo.db_table2.find({"topic":"华为闪存"}):
    #     print i
    print lo.findd("Pin",u'济南搬迁')









