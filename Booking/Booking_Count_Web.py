#coding:UTF-8
# Expedia爬蟲
from datetime import datetime
import json
s1 = datetime.now()  ####### 起始時間
web_list = []
with open('E:/AB104/Booking/20170104_Booking_HotelName_list.json') as data_file:
    data = json.load(data_file)
    count = 1
    for i in data:
        web_list.append(i["web"])
        print count
        count =count +1
#==========================#
s2 = datetime.now() ####### 結束時間
print "All  Finish "+str(s2-s1)+"!!" ####### 總共爬取資料耗費時間
# 3535
#All  Finish 0:00:00.025000!!
