#coding:UTF-8
## Step ALL ## Bayes Model TestData
import codecs #操作文件，讀寫數據，涉及到非ASCII的話，最好用codes模組操作，其會自動處理不同的編碼，效果最好
import re
import jieba.analyse
import jieba.posseg as pseg
from sklearn.naive_bayes import MultinomialNB
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
import json
from sklearn.model_selection import train_test_split
from datetime import datetime

s1 = datetime.now()

############################################################
##                      進行檢測之文章                       #
############################################################

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

commList_Jieba = []
with open("E:/All_Comments_final.json", 'r') as a:
    Testdata = json.load(a)
    for content in Testdata:
        try:
            comment = content["comment_collection"]
            # print comment
            for j in comment:
                try:
                    words_pseq = pseg.cut(j["comment"])
                    # 指定詞性版
                    comments_dict = {}
                    comm = ""
                    noun = ""
                    for word in words_pseq:
                        if word.word in stopwords or word.word == ' ':
                            continue
                        if re.match('[0-9]+', word.word):
                            continue
                        else:
                            comm += (word.word + " ")

                            if (word.flag == u"n") or (word.flag == u"ns") :   ## 還須確定為名詞、動名詞
                                noun += (word.word + " ")
                                # noun.append(word.word + " ")
                    hotel =   content["hotel"]
                    address = content["address"]
                    comments_dict["comments"] = comm
                    comments_dict["hotel"] = hotel
                    comments_dict["address"] = address
                    comments_dict["noun"] = noun
                    commList_Jieba.append(comments_dict)
                except Exception as e:
                    print e
        except Exception as e:
            # print "No comments"
            continue
# print type(commList_Jieba)
# print commList_Jieba

############################################################
##                        Model設置                        ##
############################################################
with open("E:/AB104/AlgorithmTest/Jieba_Booking.json", 'r') as a:
    data = json.load(a)

data = DataFrame(data)
classifier = MultinomialNB()
X_train, X_test, y_train, y_test = train_test_split( data['comments'].values, data['mark'].values, test_size = 0)

targets = y_train
# print len(targets) #241221
count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(X_train)
# print len(X_train) #241221
classifier.fit(counts, targets)

############################################################
##                    進行檢測之結果儲存                     ##
############################################################
commList_Jieba_marked = []
for i in commList_Jieba:
    commList_Jieba_marked_dict = {}
    examples = [i["comments"]]
    # print i["comments"]
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)
    commList_Jieba_marked_dict["mark"] = predictions.tolist()
    # print predictions
    commList_Jieba_marked_dict["comments"] = [i["comments"]]
    commList_Jieba_marked_dict["hotel"] = [i["hotel"]]
    commList_Jieba_marked_dict["address"] = [i["address"]]
    commList_Jieba_marked_dict["noun"] = i["noun"]
    commList_Jieba_marked.append(commList_Jieba_marked_dict)

# print type(commList_Jieba_marked)
commList_Jieba_marked_json = json.dumps(commList_Jieba_marked, ensure_ascii=False)
# print type(commList_Jieba_marked_json)
with open("E:/Bayes_All_Comments_final.json","w") as w:
    w.write(commList_Jieba_marked_json.encode("utf-8"))

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 1:00:18.360000!!




