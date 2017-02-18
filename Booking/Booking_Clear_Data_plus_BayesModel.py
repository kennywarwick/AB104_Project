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
from numpy import *

s1 = datetime.now()

commList1 = []
commList0 = []
commList = []
train_doc_list = []
train_doc_sent_vec = []
# 讀取寫入之Json檔
with open("E:/AB104/Booking/20170111_Booking_AllComm.json", 'r') as a:
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

class ClassNaiveBayes:
    #Jieba
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



    with open('E:/AB104/Booking/BookingJieba_textBayes_vec.txt','a') as f:
        f.write(str(train_doc_sent_vec))
        word_list = []
        # 正面和負面機率, 先驗機率
        p0_v = 0
        p1_v = 0
        p_ab = 0
        # 創建一個包含在所有文檔中出現不會重複詞的列表

        @staticmethod
        def create_word_list(data_list):
            # create empty set
            word_set = set([]) ### 創建一個空集合，set數據類型，返回一個不重複詞表
            for document in data_list:
                # union of the two sets(聯集)(或)
                word_set = word_set | set(document)
            return list(word_set)

        # 將輸入的單詞列表(需要訓練或是測試的)根據上面的單詞集合生成向量
        @staticmethod
        def words_to_vec(word_list, new_word_list):
           vec = [0] * len(word_list) ### 建立N個0的數字陣列
           for word in new_word_list:
               if word in word_list:
                   vec[word_list.index(word)] += 1
               else:
                   pass
                   # print("the word: %s is not in my Vocabulary!" % word)
           return vec

        # Bayes的算法，根據訓練矩陣數據和預先設定的傾向性，來得到 p0，p1 機率。
        @staticmethod
        def train_nb0(train_matrix, train_category):
            num_train_docs = len(train_matrix)
            num_words = len(train_matrix[0])
            p_ab = sum(train_category) / float(num_train_docs)
            # 創建給定長度的填滿1的數組
            p0_num = ones(num_words)
            p1_num = ones(num_words)
            p0_d = 2.0
            p1_d = 2.0
            for i in range(num_train_docs):
                if train_category[i] == 1:
                    p1_num += train_matrix[i]
                    p1_d += sum(train_matrix[i])
                else:
                    p0_num += train_matrix[i]
                    p0_d += sum(train_matrix[i])
            p1_v = log(p1_num / p1_d)
            p0_v = log(p0_num / p0_d)
            return p0_v, p1_v, p_ab

        @staticmethod
        def classify_nb(vec, p0_vec, p1_vec, p_class1):
            # element-wise mult
            p0 = sum(vec * p0_vec) + log(1.0 - p_class1)
            p1 = sum(vec * p1_vec) + log(p_class1)
            print('p0:', p0, 'p1:', p1)
            if p1 > p0:
                return 1
            else:
                return 0

        def train(self):
            # 生成單詞列表集合
            self.word_list = self.create_word_list(self.train_doc_list)
            # 訓練矩陣初始化
            train_matrix = []
            # 根劇訓練文檔進行循環
            for post_in_doc in self.train_doc_list:
                # 構建訓練矩陣，將單詞列表轉化為向量
                train_matrix.append(self.words_to_vec(self.word_list, post_in_doc))
            # 根據訓練矩陣和情感分析向量進行訓練，得到
            self.p0_v, self.p1_v, self.p_ab = self.train_nb0(array(train_matrix), array(self.train_doc_sent_vec))
        def testing_nb(self, test_word_list):
            # 對輸入的内容轉化為向量
            this_post_vec = array(self.words_to_vec(self.word_list, test_word_list))
            # 返回分類的值
            return self.classify_nb(this_post_vec, self.p0_v, self.p1_v, self.p_ab)

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 0:00:29.160000!!


