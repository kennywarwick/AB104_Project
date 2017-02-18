#coding:UTF-8
## Step 5 ## WordCount TestData
from datetime import datetime
import json
import operator
import itertools
import pprint     # pretty print the lists
from collections import Counter
import _uniout

s1 = datetime.now()

shouldReplaceList1 = []
shouldReplaceList2 = []
shouldReplaceList3 = []
shouldReplaceList4 = []
shouldReplaceList5 = []
shouldReplaceList6 = []
shouldReplaceList7 = []
shouldReplaceList8 = []
shouldReplaceList9 = []

##1
with open("E:/AB104/AB104/Group_Features/sim_sort_accommLevel.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList1.append(item.rstrip())
    f.close()
##2
with open("E:/AB104/AB104/Group_Features/sim_sort_CountyCity.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList2.append(item.strip())
    f.close()
##3
with open("E:/AB104/AB104/Group_Features/sim_sort_Expense.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList3.append(item.strip())
    f.close()
##4
with open("E:/AB104/AB104/Group_Features/sim_sort_Hardware.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList4.append(item.strip())
    f.close()
##5
with open("E:/AB104/AB104/Group_Features/sim_sort_insideRoom.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList5.append(item.strip())
    f.close()
##6
with open("E:/AB104/AB104/Group_Features/sim_sort_Meal.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList6.append(item.strip())
    f.close()
##7
with open("E:/AB104/AB104/Group_Features/sim_sort_Staff.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList7.append(item.strip())
    f.close()
##8
with open("E:/AB104/AB104/Group_Features/sim_sort_Transportation.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList8.append(item.strip())
    f.close()
##9
with open("E:/AB104/AB104/Group_Features/sim_sort_Venue.txt","r") as f:
    for item in f.readlines():
        shouldReplaceList9.append(item.strip())
    f.close()

###########################################################
corpus = ''
with open("E:/AB104/AlgorithmTest/Jieba_TestData_Ctrip.json", 'r') as input:
    data = json.load(input)
    for x,i in enumerate(data):
        ##1##
        # print i["noun"]
        for item in shouldReplaceList1:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'accommLevel')
        ##2##
        for item in shouldReplaceList2:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'CountyCity')

        ##3##
        for item in shouldReplaceList3:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'Expense')

        ##4##
        for item in shouldReplaceList4:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'Hardware')

        ##5##
        for item in shouldReplaceList5:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'insideRoom')

        ##6##
        for item in shouldReplaceList6:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'Meal')

        ##7##
        for item in shouldReplaceList7:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'Staff')

        ##8##
        for item in shouldReplaceList8:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'Transportation')

        ##9##
        for item in shouldReplaceList9:
            i["noun"] = i["noun"].replace(item.decode("utf-8"), 'Venue')

        # print type(i["noun"])
        corpus += (i["noun"])

### WordCounts(ALL)
for doc in [corpus]:
    tf = Counter()
    for word in doc.split():
        tf[word] += 1
    for x,i in enumerate(tf.items()):
        print x+1,_uniout.unescape(str(i), 'utf8')

### 對 Dict 某條件下分組
# print "Original list:"
# pprint.pprint(data)
data.sort(key=operator.itemgetter('hotel'))
# pprint.pprint(data)

### group the departments in lists
list1 = []
for key, items in itertools.groupby(data, operator.itemgetter('hotel')):
    list1.append(list(items))
# print "After grouping the list by department:"
# pprint.pprint(list1)

### create a list of department number and average age in each department
hotel_feature_WordCount = []
for item in list1:
    hotel_feature_dict = {}

    ### the hotel number
    hotel = item[0]["hotel"][0]
    hotel_feature_dict["hotel"] = hotel
    print hotel
    # print type(hotel)
    # print type(hotel[0].encode("utf-8"))

    ### the size of the hotel
    size = len(item)
    features = []
    for k in range(size):
        ###  the noun/mark of each hotel
        hotel_feature_mark_dict = {}
        hotel_feature_mark_dict["noun"] = item[k]['noun']
        hotel_feature_mark_dict["mark"] = int(item[k]['mark'][0])
        features.append(hotel_feature_mark_dict)
    hotel_feature_dict["features"] = features
    hotel_feature_WordCount.append(hotel_feature_dict)

# pprint.pprint(hotel_feature_WordCount)
### WordCounts
WordCount = []
for i in hotel_feature_WordCount:
    # print "============================="
    Dict ={}
    Dict["hotel"] = i["hotel"]
    # print i["hotel"]
    tf = Counter()
    for j in i["features"]:
        # print j
        if j["mark"] == 0:
            # print j["noun"]
            ### WordCounts(ALL)
            for doc in [j["noun"]]:
                # print len(doc.split()) ##此處可以限制單句
                for word in doc.split():
                    tf[word] += 1
        if j["mark"] == 1:
            # print j["noun"]
            ### WordCounts(ALL)
            for doc in [j["noun"]]:
                # print len(doc.split()) ##此處可以限制單句
                for word in doc.split():
                    tf[word] += -1
    ### SHOW DATA
    # print tf.items()
    # for x, i in enumerate(tf.items()):
    #     print x+1, _uniout.unescape(str(i), 'utf8')
    Dict["features"] = tf.items()
    WordCount.append(Dict)

WordCountJson = json.dumps(WordCount, ensure_ascii=False)
with open("E:/AB104/AlgorithmTest/WordCountFeature.json","w") as output:
    output.write(WordCountJson.encode("utf-8"))

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 0:00:00.135000!!