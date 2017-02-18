#coding:UTF-8
## Step 3 ##  Fit Model & test Data
from datetime import datetime
from sklearn.ensemble import AdaBoostClassifier
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

s1 = datetime.now()

with open("E:/AB104/AlgorithmTest/Jieba_Booking.json", 'r') as a:
    data = json.load(a)

data = DataFrame(data)
classifier = AdaBoostClassifier()
X_train, X_test, y_train, y_test = train_test_split( data['comments'].values, data['mark'].values, test_size = 0.2)

targets = y_train
# print len(targets) #241221
count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(X_train)
# print len(X_train) #241221
classifier.fit(counts, targets)

X_test = count_vectorizer.transform(X_test)
y_pred = classifier.predict(X_test)
print 'Misclassified sample: %d' % (y_test != y_pred).sum()
print 'Accuracy: %.2f' % accuracy_score(y_test, y_pred)

# #=========================================================
# ## 混淆矩陣讀取
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix
#
# confmat = confusion_matrix(y_true = y_test, y_pred=y_pred)
# print confmat
#
# fig,ax = plt.subplots(figsize=(5,5)) ##plt視窗的size
# ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.2) ##框內顏色，alphqa為深淺調整，越高越深
# for i in range(confmat.shape[0]): ##數值給予
#     for j in range(confmat.shape[1]):
#         ax.text(x=j,y=i,s=confmat[i,j],va="center",ha="center")
# plt.xlabel("predicted label") ##給予名稱
# plt.ylabel("true label")
# # plt.show() ##show出plt圖
# plt.savefig('C:/Users/BIG DATA/Desktop/AB104/AdaBoostClassifier_H0H1.png', dpi=300)
# plt.close()

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 0:00:32.367000!!

###############################################
# 70% data - 241,221
# Misclassified sample: 26360
# Accuracy: 0.75
# [[43748  8186]
#  [18174 33273]]
# All  Finish 0:00:23.893000!!
###############################################
# 80% data - 275,681
# Misclassified sample: 17711
# Accuracy: 0.74
# [[29071  5448]
#  [12263 22139]]
# All  Finish 0:00:17.144000!!
###############################################

## 可知道相較之下，比較容易出現FP錯誤，偏屬於樂觀評論(實質為評價差卻判斷為評價好)


# def plotROC(predStrengths, classLabels):
#     import matplotlib.pyplot as plt
#     from numpy import *
#     cur = (1.0,1.0) #cursor
#     ySum = 0.0 #variable to calculate AUC
#     numPosClas = sum(array(classLabels)==1.0)
#     yStep = 1/float(numPosClas); xStep = 1/float(len(classLabels)-numPosClas)
#     sortedIndicies = predStrengths.argsort()#get sorted index, it's reverse
#     fig = plt.figure()
#     fig.clf()
#     ax = plt.subplot(111)
#     #loop through all the values, drawing a line segment at each point
#     for index in sortedIndicies.tolist()[0]:
#         if classLabels[index] == 1.0:
#             delX = 0; delY = yStep;
#         else:
#             delX = xStep; delY = 0;
#             ySum += cur[1]
#         #draw line from cur to (cur[0]-delX,cur[1]-delY)
#         ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY], c='b')
#         cur = (cur[0]-delX,cur[1]-delY)
#     ax.plot([0,1],[0,1],'b--')
#     plt.xlabel('False positive rate'); plt.ylabel('True positive rate')
#     plt.title('ROC curve for AdaBoost horse colic detection system')
#     ax.axis([0,1,0,1])
#     plt.show()
#     print "the Area Under the Curve is: ",ySum*xStep

