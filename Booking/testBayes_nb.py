#coding:UTF-8
import json
from collections import Counter
from operator import itemgetter #適合處理字典或是串列資料
import codecs #操作文件，讀寫數據，涉及到非ASCII的話，最好用codes模組操作，其會自動處理不同的編碼，效果最好
import re
import jieba
import jieba.analyse
import jieba.posseg as pseg
from datetime import datetime
import numpy as np

s1 = datetime.now()

commList1 = []
commList0 = []
commList = []
train_doc_list = []
train_doc_sent_vec = []
# 讀取寫入之Json檔
with open("E:/AB104/Booking/ALL_comm1.json", 'r') as a:
    data = json.load(a)
    for j in data:
        # print j
        comm = j.get("comment_collection")
        try:
        # print type(comm)
            for i in comm:
                dict = {}
                if i.get("1") != "None":
                    dict["1"] = i.get("1").strip('\n')
                    # print dict["1"]
                    # print len(commList1)
                    if i.get("0") != "None":
                        dict["0"] = i.get("0").strip('\n')
                        commList.append(dict.copy())
                    else:
                        commList.append(dict.copy())
                else:
                    if i.get("0") != "None":
                        dict["0"] = i.get("0").strip('\n')
                        commList.append(dict.copy())
        except Exception as e:
            print e
##################################################################################
# 一個飯店的評論                                                                   #
#{u'comment_collection': None, u'hotel': None, u'address': None, u'level': None} #
#會出現error 因為 TypeError: 'NoneType' object is not iterable                    #
#################################################################################

print type(commList)
print len(commList)
# print len(train_doc_sent_vec)
for i in commList:
    print json.dumps(i, encoding="UTF-8", ensure_ascii=False)

# print train_doc_sent_vec


#Jieba
# 建立 Dict
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/userWord.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/hotelName9943.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/MRT584.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/big176239.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/big584429.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/simple109750.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/NightMarket86.txt")

# StopWords 載入
with codecs.open('E:/AB104/TextMining/JeibaDict/stop_words.txt','r', encoding='utf-8') as fs:
    stopwords = fs.read().split('\n')
print type(commList)

# print type(contentjson)
train_doc_list = []
num = []
train_doc_sent_vec = []
with open('E:/AB104/Booking/BookingJieba_textBayes.txt','w') as output:
    for content in commList:
        try:
            badline = content.get("1").upper().replace(' ','')
            # print upperline
            words_pseq = pseg.cut(badline)
            # 指定詞性版
            b = []
            for word in words_pseq:
                if word.word in stopwords or word.word == ' ':
                    continue
                if re.match('[0-9]+', word.word):
                    continue
                else:
                    b.append(word.word)
                    # print len(b)
            train_doc_list.append(b)
        except Exception as e:
            print e
            print "沒有輸入缺點!"
    train_doc_sent_vec = [1] * len(train_doc_list)
    for content in commList:
        try:
            goodline = content.get("0").upper().replace(' ','')
            print goodline
            words_pseq = pseg.cut(goodline)
            # 指定詞性版
            c = []
            for word in words_pseq:
                if word.word in stopwords or word.word == ' ':
                    continue
                if re.match('[0-9]+', word.word):
                    continue
                else:
                    c.append(word.word)
            num.append(len(c))
            print len(num)
            train_doc_list.append(c)

        except Exception as e:
            print e
            print "沒有輸入優點"
    train_doc_sent_vec = train_doc_sent_vec + [0] * len(num)
    print train_doc_sent_vec
    print len(train_doc_sent_vec)
    print len(train_doc_list)
    output.write(str(train_doc_list))
# for i in comm_List:
#     print i
print train_doc_sent_vec
print type(train_doc_sent_vec)

from sklearn.naive_bayes import GaussianNB

X = np.array(train_doc_list)
Y = train_doc_sent_vec
print X
print Y

clf = GaussianNB()
clf.fit(X, Y)

print(clf.predict([['安靜', '舒服']]))

