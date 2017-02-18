#coding:UTF-8

##  By python3
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import numpy as np
from sklearn.metrics import silhouette_samples
from matplotlib import cm
from sklearn.cluster import AgglomerativeClustering
from numpy.random import rand

s1 = datetime.now()
path = "E:/AB104/AnaDB_version2.csv"
rRows = []
document_list=[]
matrix = []
cp = 0
with open(path,'r') as r:  #, encoding = 'utf-8-sig'
    readerObj = csv.reader(r)
    for i in r:
        dict = {}
        vec = []
        for j in range(9,18):
            vec.append(float(i.split(",")[j]))
        dict["vec"] = vec
        dict["cityMark"] = i.split(",")[1].strip()
        # print (dict["Hotel"])
        # print(dict["cityMark"])
        # print(vec)
        # print(dict["cityMark"])
        if dict["cityMark"] == "花蓮縣":
            matrix.append(vec)
        # matrix.append(vec)
            document_list.append(dict)


r.close()
count = np.array(matrix)

hotelName = []
km = KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=0.0001, random_state=0)

# km = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='complete')
km.fit(count)
y_km = km.fit_predict(count)
y_label = []
for i in y_km:
    y_label.append(i)
print (len(km.fit_predict(count)))
print(len(y_km))
print(len(document_list))

dict1 = {}
for i in range(len(y_km)):
    print(y_km[i]+1)


###Silhouette側影係數
cluster_labels = np.unique(y_km)
n_clusters = cluster_labels.shape[0]
silhouette_vals = silhouette_samples(count, y_km, metric='euclidean')
y_ax_lower, y_ax_upper = 0, 0
yticks = []
for i, c in enumerate(cluster_labels):
    c_silhouette_vals = silhouette_vals[y_km == c]
    c_silhouette_vals.sort()
    y_ax_upper += len(c_silhouette_vals)
    color = cm.jet(i / float(n_clusters))
    # color = cm.jet(rand())
    plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals, height=1.0,edgecolor='none', color=color)
    yticks.append((y_ax_lower + y_ax_upper) / 2)
    y_ax_lower += len(c_silhouette_vals)

silhouette_avg = np.mean(silhouette_vals)
plt.axvline(silhouette_avg, color="r", linestyle="--")
plt.yticks(yticks, cluster_labels + 1)
plt.ylabel('Cluster')
plt.xlabel('Silhouette coefficient')


# plt.tight_layout()
# plt.savefig('E:/silhouette.png', dpi=300)
plt.show()

# ###Kmean++(graph)
# distortions = []
# for i in range(1,9):
#     kmG = KMeans(n_clusters=i, init='k-means++', n_init=100, max_iter=300, tol=0.0001, random_state=0)
#     kmG.fit(count)
#     distortions.append(kmG.inertia_)
# print(len(distortions))
# plt.plot(range(1,9),distortions,marker="o")
# plt.xlabel("Hualien County_ClustersNumber")
# plt.ylabel("Distirtion")
# plt.show()


s2 = datetime.now()
# print("All  Finish "+str(s2-s1)+"!!")

