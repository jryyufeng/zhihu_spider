# -*-coding:utf-8-*- 
from os import path
from scipy.misc import imread
import jieba
import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
def ciyun1(path1,back):
    text=open(path1).read()
    wordlist=jieba.cut(text)
    wl_space_split=" ".join(wordlist)
    d=path.dirname(__file__)
    if back.find('slocation')!=-1:
        print 'hh'
        nana_coloring=imread(path.join(d,"location.jpg"))
    else:
        nana_coloring = imread(path.join(d, "nihao.jpg"))
    my_wordcloud=WordCloud(
        background_color='white',                # 设置背景颜色
        mask=nana_coloring,                      # 设置背景图片
        max_words=300,                           # 设置最大实现词数
        stopwords=STOPWORDS,                     # 设置停用词
        max_font_size=80,                        # 设置字体最大值
        random_state=30,                         # 设置有多少种随机生成状态，即有多少种配色方案
        scale=3                                  # 设置分辨率
    )
    my_wordcloud.generate(wl_space_split)
    image_colors=ImageColorGenerator(nana_coloring)          #改变字体颜色
    plt.imshow(my_wordcloud)                                  #显示词云图
    plt.axis("off")                                           #是否显示x轴，y轴下标
    my_wordcloud.to_file(path.join(d,back+".jpg"))


def maopao(array):
    for i in range(len(array)):
        for j in range(i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


