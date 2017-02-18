#coding:UTF-8
# Expedia爬蟲
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import requests as r
import math
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import random

# ipList = []
# with open("E:/python/IP/ips.txt","r") as f:
#     for item in f.readlines():
#         ipList.append(item)
#     f.close()
# lastPage = (int(baseSoup.select_one("div.search-count").select_one(".num").text) // 10) + 1

def sleeptime():
    sl = random.uniform(0.2, 0.9)
    time.sleep(sl)

####   爬蟲程序
def crawler(url):
    # nip = random.randint(0, len(ipList)-1)
    # ip = ipList.__getitem__(nip).strip()
    # proxy = {"http": "http://{}".format(ip)}
    # n = 0
    # while True:
    #     try:
    #         if n >= 5:
    #             print("http not found !!")
    #             return False
    #         res = requests.get(url, proxies=proxy, timeout=6)
    #         if res.status_code==200:
    #             print "XD"
    #         break
    #     except:
    #         n += 1
    #         nip = random.randint(0, len(ipList) - 1)
    #         ip = ipList.__getitem__(nip).strip()
    #         proxy = {"http": "http://{}".format(ip)}
    #         pass
    #

    HotelDetail_dict = {}
    URL = url
    sleeptime()
    driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
    sleeptime()
    res = r.get(URL)
    soup = BeautifulSoup(res.text)
    res_tail = soup.select('.hdetail_title')
    HotelDetail_dict["hotel"] = res_tail[0].select_one("h1").text  #飯店名
    #hdetail_title
    HotelDetail_dict["level"] = res_tail[0].select_one("span.score").text.encode("utf-8").split("/")[0] ## 分數
    # print float(HotelDetail_dict["level"])/5
    com_Num = res_tail[0].select_one("p > a").text.encode("utf-8").split("条")[0] ## 評論數
    com_Num_page = float(math.ceil(float(com_Num)/5))
    sleeptime()
    res = soup.select('div.des_wide.f_left')
    HotelDetail_dict["address"] = res[0].select_one("div.hdetial_position > p.poi_text > span").text ## 地址
    try:
        HotelDetail_dict["feature"] = res[0].select_one("#CommentTag").text ## 優點集
    except Exception as e:
        HotelDetail_dict["feature"] = "none"
    sleeptime()
    driver.get(URL)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight-2500);')

    HotelComm_list = []
    count = 1
    while True:
        sleeptime()
        soup = BeautifulSoup(driver.page_source)
        res_com = soup.select('div.comment_single')
        for i in res_com:
            HotelComm_dict = {}
            HotelComm_dict["comment"] = i.select_one(".main_con").text.replace(" ","") ## 評論
            HotelComm_list.append(HotelComm_dict)
        try:
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight-2500);')
            time.sleep(2)
            driver.find_element_by_css_selector('a.nextpage').click()
            time.sleep(2)
            if count >= com_Num_page:
                break
            else:
                count = count + 1
        except Exception as e:
            break
    HotelDetail_dict["comment_collection"] = HotelComm_list
    Ctrip_Hotel_list.append(HotelDetail_dict)
    driver.close()
    # worker()

# ####   爬蟲實施抓取網頁
# def worker():
#     while not queue.empty():
#         url = queue.get()
#         crawler(url)

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
sleeptimes= 2
Ctrip_Hotel_list = []
NUM_THREADS = 1
####   創建一個 Queue
queue = Queue()

#34
import json
with open("E:/AB104/20170103_Ctrip_HotelName_list.json",'r') as a:
    data = json.load(a)
    for item in data[0].values():
        try:
            queue.put(item)
        except Exception as e:
            print e
            print "抓取完畢!"
        crawler(item)

# ####   啟動THREAD
# threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
# map(lambda th: th.start(), threads)
# map(lambda th: th.join(), threads)
# time.strftime("%d/%m/%Y")
# # ==========================#
contentjson = json.dumps(Ctrip_Hotel_list, ensure_ascii=False)
with open('E:/AB104/20170103_Ctrip_Hotel_Info.json', 'w') as f:
    f.write(contentjson.encode('utf-8'))
# ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 0:03:48.180000!!(鎖 仁愛地區未拿到)