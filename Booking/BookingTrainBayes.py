#coding:UTF-8
import codecs
import re

import jieba.analyse
import jieba.posseg as pseg

import Booking_Clear_Data_plus_BayesModel

nb = Booking_Clear_Data_plus_BayesModel.ClassNaiveBayes()

nb.train()

tt = ["沒问题，非常好。要挑毛病的话，就是整栋楼冷清了点，许多配套，商店，都沒开始。个別服务员冷漠了点，这点需要和另一家大仓久和学习下。本人偏住台北几家五星，一些微的感受很明显，大仓的各个岗位服务员，都是推滿笑容，有着日式的细致，文华则略高冷，W也是，不过本人非常重视健康中心，这点文华非常好，強过大仓。展开更多"]
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/userWord.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/hotelName9943.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/MRT584.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/big176239.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/big584429.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/simple109750.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/NightMarket86.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/pttcontent.txt")

# StopWords 載入
with codecs.open('E:/AB104/TextMining/JeibaDict/stop_words.txt', 'r', encoding='utf-8') as fs:
    stopwords = fs.read().split('\n')

try:
    badline = tt.upper().replace(' ', '')
    # print upperline
    words_pseq = pseg.cut(badline)
    # 指定詞性版
    test_list1 = []
    for word in words_pseq:
        if word.word in stopwords or word.word == ' ':
            continue
        if re.match('[0-9]+', word.word):
            continue
        else:
            test_list1.append(word.word)
except Exception as e :
    print e
# GOOD: 0 ; BAD: 1

print(test_list1, 'classified as: ', nb.testing_nb([x.decode('utf-8') for x in test_list1]))

test_list = ['安靜', '舒服', '新穎']
print(test_list, 'classified as: ', nb.testing_nb([x.decode('utf-8') for x in test_list]))

test_list = ['環境', '乾淨']
print(test_list, 'classified as: ', nb.testing_nb([x.decode('utf-8') for x in test_list]))

test_list = ['硬','灰塵']
print(test_list, 'classified as: ', nb.testing_nb([x.decode('utf-8') for x in test_list]))

test_list = ['硬','灰塵']
print(test_list, 'classified as: ', nb.testing_nb([x.decode('utf-8') for x in test_list]))



