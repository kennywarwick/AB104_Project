#coding:UTF-8
## Step 2 ## Bayes Model Trainning Data
import json
import codecs #操作文件，讀寫數據，涉及到非ASCII的話，最好用codes模組操作，其會自動處理不同的編碼，效果最好
import re
import jieba.analyse
import jieba.posseg as pseg
from datetime import datetime
from numpy import *

s1 = datetime.now()
# 建立 Dict
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/userWord.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/hotelName9943.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/MRT584.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/big176239.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/big584429.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/simple109750.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/NightMarket86.txt")
jieba.load_userdict("E:/AB104/TextMining/JeibaDict/pttcontent.txt")
# StopWords 載入
with codecs.open('E:/AB104/TextMining/JeibaDict/stop_words.txt','r', encoding='utf-8') as fs:
    stopwords = fs.read().split('\n')

# 匯入需 Jieba 之資料
with open("E:/AB104/AlgorithmTest/ALL_comms_0&1.json", 'r') as a:
    commList = json.load(a)

commList_Jieba = []

for content in commList:
    try:
        line = content.get("comments").upper().replace(' ','')
        mark = content.get("mark")
        words_pseq = pseg.cut(line)
        # 指定詞性版
        comments_dict = {}
        comm = ""
        for word in words_pseq:
            if word.word in stopwords or word.word == ' ' or word.word == None:
                continue
            if re.match('[0-9]+', word.word):
                continue
            else:
                comm += (word.word + " ")
        comments_dict["comments"] = comm
        comments_dict["mark"] = mark
        commList_Jieba.append(comments_dict)
    except Exception as e:
        print e
print type(commList_Jieba)
comm = json.dumps(commList_Jieba, ensure_ascii=False)
with open('E:/AB104/AlgorithmTest/Jieba_Booking.json', 'w') as output:
    output.write(comm.encode("utf-8"))

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 0:08:36.160000!!