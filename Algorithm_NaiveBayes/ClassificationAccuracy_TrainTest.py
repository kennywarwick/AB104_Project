#coding:UTF-8
## Step 3 ##  Fit Model & test Data
from datetime import datetime
from sklearn.naive_bayes import MultinomialNB
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


s1 = datetime.now()

with open("E:/AB104/AlgorithmTest/Jieba_Booking.json", 'r') as a:
    data = json.load(a)

data = DataFrame(data)
classifier = MultinomialNB(alpha=1, class_prior=None , fit_prior=True)
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

#=========================================================
## 混淆矩陣讀取
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

confmat = confusion_matrix(y_true = y_test, y_pred=y_pred)
print confmat

fig,ax = plt.subplots(figsize=(5,5)) ##plt視窗的size
ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.2) ##框內顏色，alphqa為深淺調整，越高越深
for i in range(confmat.shape[0]): ##數值給予
    for j in range(confmat.shape[1]):
        ax.text(x=j,y=i,s=confmat[i,j],va="center",ha="center")
plt.xlabel("predicted label") ##給予名稱
plt.ylabel("true label")
plt.show() ##show出plt圖


# data = DataFrame(data)
# classifier = MultinomialNB()
# targets = data['mark'].values
# print len(targets) #344602
# count_vectorizer = CountVectorizer()
# counts = count_vectorizer.fit_transform(data['comments'].values)
# print len(data['comments'].values) #344602
# classifier.fit(counts, targets)

# examples = ['自行車 不好']
# example_counts = count_vectorizer.transform(examples)
# predictions = classifier.predict(example_counts)
# print predictions

s2 = datetime.now()
print "All  Finish "+str(s2-s1)+"!!"
# All  Finish 0:00:32.367000!!

###############################################
# 70% data - 241,221
# Misclassified sample: 22,354
# Accuracy: 0.78
# All  Finish 0:00:03.564000!!
###############################################
# 80% data - 275,681
# Misclassified sample: 14,027
# Accuracy: 0.80
# All  Finish 0:00:03.526000!!
###############################################
# [[33349  1090]
#  [13786 20696]]
## 可知道相較之下，比較容易出現FP錯誤，偏屬於樂觀評論(實質為評價差卻判斷為評價好)




