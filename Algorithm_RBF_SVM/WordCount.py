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

corpus = ''
with open("E:/AB104/AlgorithmTest/Jieba_TestData_Ctrip.json", 'r') as input:
    data = json.load(input)
    for x,i in enumerate(data):
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
    # print hotel
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
with open("E:/AB104/AlgorithmTest/WordCount.json","w") as output:
    output.write(WordCountJson.encode("utf-8"))

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 0:00:00.135000!!