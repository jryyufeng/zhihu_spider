# -*-coding:utf-8-*- 

import jieba.posseg as pesg
import codecs
import sys
from gensim import corpora,models,similarities
import os
import re
import jieba
import mongDB

"""
获取评论数前十的问题获取相关评论内容进行相似度计算，判断是否有软广告
"""

reload(sys)
sys.setdefaultencoding('utf8')

class XiangSi():
    def __init__(self):
        #构建停用词表
        self.stop_words='F:/zhihu/stopwords.txt'
        self.stopwords=codecs.open(self.stop_words,'r',encoding='utf-8').readlines()
        self.stopwords=[w.strip()for w in self.stopwords]
        self.stop_flag=['x', 'c', 'u','d','p', 't', 'uj', 'm', 'f', 'r']
        self.questionlist=[]
#对文章进行分词、去停用词
    def tokenzation(self,filename):
        result=[]
        with open(filename,'r') as f:
            text=f.read()
            words=pesg.cut(text)#
        for word,flag in words:
            if flag not in self.stop_flag and word not in self.stopwords:
                result.append(word)
        return result
    def wenzhang(self,files):
        filenames=files
        corpus=[]
        for each in filenames:
            corpus.append(self.tokenzation(each))
        #建立词袋模型
        dictionary=corpora.Dictionary(corpus)
        doc_vectors=[dictionary.doc2bow(text) for text in corpus]
        #建立TF-IDF模型
        tfidf=models.TfidfModel(doc_vectors)
        tfidf_vectors=tfidf[doc_vectors]
        #lsi=models.LsiModel(tfidf_vectors,id2word=dictionary,num_topics=2)
        #不指定主题数
        lsi = models.LsiModel(tfidf_vectors, id2word=dictionary)
        lsi_vector=lsi[tfidf_vectors]
        #构建训练样本
        query=self.tokenzation('/example_comment.txt')
        query_bow=dictionary.doc2bow(query)
        query_lsi=lsi[query_bow]
        index=similarities.MatrixSimilarity(lsi_vector)
        sims=index[query_lsi]
        #print list(enumerate(sims))
        return list(enumerate(sims))
    def analyse_nr(self,filepath):
        listfiles=[]
        pathDir = os.listdir(filepath)
        for allDir in pathDir:
            child = os.path.join('%s%s' % (filepath, allDir))
            #child.decode('utf-8')
            listfiles.append(child)

        return listfiles
            #print child.decode('utf-8')  # .decode('gbk')是解决中文显示乱码问题
    def change(self,htmls):
        file1=open('text.txt','a')
        for html1 in htmls:
            file = open(html1, 'r')
            html = file.read()
            file.close()
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', html)
            file1.write(dd)
            # filew=open(html1,'w')
            # filew.write(dd)
        file1.close()
        clean="ss "
        file2=open('text.txt','r+')
        text=file2.read()
        file2.close()
        file3= open('text.txt', 'w')
        file3.write(" ")
        file3.close()
        return text
    def maopao(self,list1):
        j = 0
        for i in range(len(list1)):
            for j in range(len(list1) - i - 1):
                if (list1[j][1] < list1[j + 1][1]):
                    t = list1[j]
                    list1[j] = list1[j + 1]
                    list1[j + 1] = t
        print list1
    def wordeee(self,text,topic,question):
        lol=mongDB.Logger()
        dic_1={}
        dic_11={}
        from collections import Counter
        numall=0
        words=[]
        #words = [word for word in jieba.cut(text, cut_all=True) if len(word) >= 2]
        for word in jieba.cut(text,cut_all=True):
            if len(word)>=2:
                words.append(word)
                numall+=1
        c = Counter(words)
        p=0.0
        listword=[]
        for word_freq in c.most_common(20):
            word, freq = word_freq
            if str(word).find('\n')!=-1:
                pass
            else:
                listword.append(word)
                p+=float(freq) / float(numall)
        dic_1['answer_words']=listword
        dic_1['p']=p*100  #百分比
        if os.path.exists(question):
            fileq=open(question)
            qq=fileq.read()
            dic_1['title']=qq
        else:
            dic_1['title']="null"
        self.questionlist.append(dic_1)
        dic_11['questionlist']=self.questionlist
        dic_11['itstopic'] = topic

                #print word, freq
        #lol.db_table7.insert(dic_11)###########
        return dic_11
    def token1(self,text,topic):
        result=[]
        words=pesg.cut(text)#
        for word in words:
            if word in self.stopwords:
                result.append(word)
        return result

if __name__=='__main__':
    xs=XiangSi()
    # count=1
    # #files=['D:/' + u'py程序' + '/answer/1.txt','D:/' + u'py程序' + '/answer/people_top10.txt','D:/' + u'py程序' + '/answer/p_location.txt']
    # for i in range(10):
    #     files1=xs.analyse_nr('F:/zhihu/answer1'+str(count)+'/')
    #     #print files
    #     text=xs.change(files1)
    #     xs.wordeee(text,'test1')
    #     # list1=xs.wenzhang(files)
    #     # xs.maopao(list1)
    #     count+=1



