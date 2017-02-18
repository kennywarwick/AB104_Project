#coding:UTF-8
import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
iris = datasets.load_iris()
X = iris.data[:,[2,3]]
y = iris.target
# X = np.array([[2,2,2],[1,1,1],[0,0,0]])
# # print X
# y = np.array([1,0,0])
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size = 0.9)#, random_state = 0) #random_state使用於隨機記憶位置

# 進行特徵標準化
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
print len(X_train_std)
print len(y_train)
ppn = Perceptron(n_iter = 100, eta0 = 0.2, random_state=0)
ppn.fit(X_train_std,y_train)

y_pred = ppn.predict(X_test_std)
print("Misclassified sample: %d" % (y_test != y_pred).sum())

print ("Accuracy: %.2f" % accuracy_score(y_test, y_pred))
