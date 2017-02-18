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


s1 = datetime.now()
path = "E:/AB104"#/AnaDB_version2.csv"

TaiwanCity = []
with open(path+"/TaiwanCity.txt",'r', encoding = 'utf-8-sig') as c:  #, encoding = 'utf-8-sig'
    data = c.readlines()
    for i in data:
        TaiwanCity.append(i.strip())
# print(TaiwanCity)
m = 0
for k in TaiwanCity:
    rRows = []
    document_list = []
    matrix = []
    m = m + 1
    with open(path+"/AnaDB_version2.csv",'r', encoding = 'utf-8-sig') as r:  #, encoding = 'utf-8-sig'
        readerObj = csv.reader(r)
        for i in r:
            dict = {}
            vec = []
            dict["Hotel"] = i.split(",")[0].strip()
            for j in range(9,18):
                vec.append(float(i.split(",")[j]))
            dict["vec"] = vec
            dict["cityMark"] = i.split(",")[1].strip()
            if dict["cityMark"] == k:
                matrix.append(vec)
            # matrix.append(vec)
            document_list.append(i)

    r.close()
    count = np.array(matrix)
    hotelName = []
    km = KMeans(n_clusters=6, init='k-means++', n_init=100, max_iter=300, tol=0.01, random_state=0)
    # km = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='complete')
    km.fit(count)
    y_km = km.fit_predict(count)
    y_label = []
    for i in y_km:
        y_label.append(i)
    # print(type(y_label))
    # print(y_label)

    # for i in y_label:
    #     with open("E:/AB104/{}.txt".format(m), 'a') as f:
    #         f.write(i)

    for i in document_list:
        hotelName.append(i["Hotel"])
    print(len(hotelName))
    dict1 = {}
    for i in range(len(hotelName)):
        print(hotelName[i])



    # ###Silhouette側影係數
    # cluster_labels = np.unique(y_km)
    # n_clusters = cluster_labels.shape[0]
    # silhouette_vals = silhouette_samples(count, y_km, metric='euclidean')
    # y_ax_lower, y_ax_upper = 0, 0
    # yticks = []
    # for i, c in enumerate(cluster_labels):
    #     c_silhouette_vals = silhouette_vals[y_km == c]
    #     c_silhouette_vals.sort()
    #     y_ax_upper += len(c_silhouette_vals)
    #     color = cm.jet(i / n_clusters)
    #     plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals, height=1.0,edgecolor='none', color=color)
    #     yticks.append((y_ax_lower + y_ax_upper) / 2)
    #     y_ax_lower += len(c_silhouette_vals)
    #
    # silhouette_avg = np.mean(silhouette_vals)
    #
    # plt.axvline(silhouette_avg, color="red", linestyle="--")
    #
    # plt.yticks(yticks, cluster_labels + 1)
    # plt.ylabel('Cluster')
    # plt.xlabel(str(m)+" " +'Silhouette coefficient')
    # plt.tight_layout()
    #
    # plt.savefig('E:/'+str(m)+' '+'silhouette.png', dpi=300)
    # plt.close()
    # plt.show()


s2 = datetime.now()
print("All  Finish "+str(s2-s1)+"!!")

