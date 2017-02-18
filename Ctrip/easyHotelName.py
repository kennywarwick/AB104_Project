#coding:UTF-8
# Expedia爬蟲

import requests as r
import time
from datetime import datetime
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import random

def sleeptime():
    sl = random.uniform(0.8, 1.2)
    time.sleep(sl)

####   爬蟲程序
def crawler(url):
    sleeptime()
    HotelDetail_dict = {}
    res = r.get(url)
    soup = BeautifulSoup(res.text)
    sleeptime()
    res_tail = soup.select('.hdetail_title')
    try:
        h = res_tail[0].select_one("h1").text
        HotelDetail_dict["hotel"] = h
        Ctrip_Hotel_list.append(HotelDetail_dict["hotel"] )  #飯店名
    except Exception as e:
        print e
    print "Get the hotel's name!"
    worker()

####   爬蟲實施抓取網頁
def worker():
    while not queue.empty():
        url = queue.get()
        crawler(url)

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
Ctrip_Hotel_list = []
NUM_THREADS = 10
####   創建一個 Queue
queue = Queue()

#34
import json
for i in range(3,8):
    with open("E:/AB104/Ctrip/test/20170107_Ctrip_HotelName_list_{}.json".format(i),'r') as a:
        data = json.load(a)
    for item in data:
        try:
            queue.put(item.values()[0].encode("utf-8"))
        except Exception as e:
            print e
            print "抓取完畢!"
        # crawler(item)

    ####   啟動THREAD
    threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
    map(lambda th: th.start(), threads)
    map(lambda th: th.join(), threads)
    time.strftime("%d/%m/%Y")
    # ==========================#
    contentjson = json.dumps(Ctrip_Hotel_list, ensure_ascii=False)
    with open('E:/AB104/Ctrip/20170123_CtripHotelName{}.json'.format(i), 'w') as f:
        f.write(contentjson.encode('utf-8'))
    # ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 0:14:49.474000!!