#coding:UTF-8
# Expedia爬蟲
from datetime import datetime
import json
s1 = datetime.now()  ####### 起始時間
web_list = []
with open('E:/AB104/Ctrip/20170104_Ctrip_HotelName_list1-1.json') as data_file:
    data = json.load(data_file)
    count = 1
    for i in data:
        web_list.append(i["web"])
        print count
        count =count +1
#==========================#
s2 = datetime.now() ####### 結束時間
print "All  Finish "+str(s2-s1)+"!!" ####### 總共爬取資料耗費時間
# 2431  #1
# 2687  #2
# 2881  #3
#All  Finish 0:00:00.056000!!

