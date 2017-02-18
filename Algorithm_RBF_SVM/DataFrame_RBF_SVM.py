#coding:UTF-8
## Step 1 ## DataFrame
import json
from datetime import datetime
from numpy import *

s1 = datetime.now()

commList = []
train_doc_list = []
train_doc_sent_vec = []
# 讀取寫入之Json檔，將評論分為"好""壞" mark
with open("E:/AB104/AlgorithmTest/20170111_Booking_AllComm.json", 'r') as a:
    data = json.load(a)
    for j in data:
        comm = j.get("comment_collection")
        try:
            for i in comm:
                dict = {}
                if i.get("comments") != "None":
                    dict["comments"] = i.get("1").strip('\n')
                    dict["mark"] = 1
                    commList.append(dict.copy())
        except Exception as e:
            print e
    for j in data:
        comm = j.get("comment_collection")
        try:
            for i in comm:
                dict = {}
                if i.get("comments") != "None":
                    dict["comments"] = i.get("0").strip('\n')
                    dict["mark"] = 0
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

comm = json.dumps(commList, ensure_ascii=False)
print type(comm)
with open("E:/AB104/AlgorithmTest/ALL_comms_0&1.json","w") as w:
    w.write(comm.encode("utf-8"))
print len(commList)

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 0:00:02.421000!!







