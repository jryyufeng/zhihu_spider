# -*-coding:utf-8-*- 
import pickle
import textprocessing as tp
import numpy as np

# 载入情感字典
posdict = open('./answer/posdict.txt', 'r')
negdict =open('./answer/negdict.txt', 'r')
mostdict = open('./answer/most.txt', 'r')
verydict = open('./answer/very.txt', 'r')
moredict = open('./answer/more.txt', 'r')
ishdict = open('./answer/ish.txt', 'r')
insufficientdict = open('./answer/insufficiently.txt', 'r')
inversedict = open('./answer/inverse.txt', 'r')
# 导入评论数据
review = open('./example_comment.txt', 'r')

# 判断停用词的使用
def judgeodd(num):
    if (num/2)*2 == num:
        return 'even'
    else:
        return 'odd'

# 情感分析
def sentiment_score_list(dataset):
    cuted_data=[]
    for cell in dataset:
        cuted_data.append(tp.cut_sentence_2(cell))
    count1=[]
    count2=[]
    for sents in cuted_data:                             # 遍历每一个评论
        for sent in sents:                               # 循环遍历评论中的每一个分句
            segtmp=tp.segmentation(sent,'list')          # 把句子分词，以列表返回
            i=0
            a=0
            poscount=0
            poscount2 = 0
            poscount3 = 0
            negcount=0
            negcount2 = 0
            negcount3 = 0
            for word in segtmp:
                if word in posdict:
                    poscount+=1
                    c=0
                    for w in segtmp[a:i]:
                        if w in mostdict:
                            poscount*=4.0
                        elif w in verydict:
                            poscount*=3.0
                        elif w in moredict:
                            poscount*=2.0
                        elif w in ishdict:
                            poscount/=2.0
                        elif w in insufficientdict:
                            poscount/=4.0
                        elif w in inversedict:
                            c+=1
                    if judgeodd(c)=='odd':
                        poscount*=-1
                        poscount2+=poscount
                        poscount=0
                        poscount3=poscount+poscount2+poscount3
                        poscount2=0
                    else:
                        poscount3=poscount+poscount2+poscount3
                        poscount=0
                    a=i+1
                elif word in negdict:
                    negcount+=1
                    d=0
                    for w in segtmp[a:i]:
                        if w in mostdict:
                            negcount*=4.0
                        elif w in verydict:
                            negcount*=3.0
                        elif w in moredict:
                            negcount*=2.0
                        elif w in ishdict:
                            negcount/=2.0
                        elif w in insufficientdict:
                            negcount/=4.0
                        elif w in inversedict:
                            d+=1
                    if judgeodd(d)=='odd':
                        negcount*=-1.0
                        negcount2+=negcount
                        negcount=0
                        negcount3=negcount+negcount2+negcount3
                        negcount2=0
                    else:
                        negcount3=negcount+negcount2+negcount3
                        negcount=0
                    a=i+1
                elif word=='|'.decode('utf-8') or word =='!'.decode('utf8'):
                    for w2 in segtmp[::-1]:
                        if w2 in posdict or negdict:
                            poscount3+=2
                            negcount3+=2
                            break
                i+=1
            pos_count=0
            neg_count=0
            if poscount3<0 and negcount3>0:
                neg_count+=negcount3-poscount3
                pos_count=0
            elif negcount3<0 and poscount3>0:
                pos_count=poscount3-negcount3
                neg_count=0
            elif negcount3<0 and poscount3<0:
                neg_count=-poscount3
                pos_count=-negcount3
            else:
                pos_count=poscount3
                neg_count=negcount3
            count1.append([pos_count,neg_count])
        count2.append(count1)
        count1=[]
    return count2
def sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review)
        Pos = np.sum(score_array[:,0])
        Neg = np.sum(score_array[:,1])
        AvgPos = np.mean(score_array[:,0])
        AvgNeg = np.mean(score_array[:,1])
        StdPos = np.std(score_array[:,0])
        StdNeg = np.std(score_array[:,1])
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
    return score

if __name__=='__main__':
    text=review.read()
    print sentiment_score(sentiment_score_list(text))


























