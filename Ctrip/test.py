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

ipList = []
with open("E:/python/IP/ips.txt","r") as f:
    for item in f.readlines():
        ipList.append(item)
    f.close()
# lastPage = (int(baseSoup.select_one("div.search-count").select_one(".num").text) // 10) + 1

def sleeptime():
    sl = random.uniform(0.2, 0.9)
    time.sleep(sl)

####   爬蟲程序
def crawler(url):
    # Ctrip_Hotel_list = []
    nip = random.randint(0, len(ipList)-1)
    ip = ipList.__getitem__(nip).strip()
    proxy = {"http": "http://{}".format(ip)}
    n = 0
    ## IP測試是否可以使用
    while True:
        try:
            if n >= 5:
                print("http not found !!")
                return False
            res = requests.get(url, proxies=proxy, timeout=6)
            # if res.status_code==200:
                # print "res200"
            break
        except:
            n += 1
            nip = random.randint(0, len(ipList) - 1)
            ip = ipList.__getitem__(nip).strip()
            proxy = {"http": "http://{}".format(ip)}
            pass

    HotelDetail_dict = {}
    URL = url
    # print URL
    sleeptime()
    driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
    # driver = webdriver.PhantomJS(executable_path='E:/phantomjs/phantomjs')
    sleeptime()
    res = r.get(URL)
    soup = BeautifulSoup(res.text)
    res_tail = soup.select('.hdetail_title')
    try:
        HotelDetail_dict["hotel"] = res_tail[0].select_one("h1").text  #飯店名
    except Exception as e:
        print "hotel"
        print URL
    try:
        HotelDetail_dict["level"] = float(res_tail[0].select_one("span.score").text.encode("utf-8").split("/")[0])/5 ## 分數
    # print float(HotelDetail_dict["level"])/5
    except Exception as e:
        print "level"
        print URL
    try:
        com_Num = res_tail[0].select_one("p > a").text.encode("utf-8").split("条")[0] ## 評論數
        com_Num_page = float(math.ceil(float(com_Num)/5)) ## 評論頁數
    except Exception as e:
        print "com_Num_page"
        print URL
    sleeptime()
    try:
        res = soup.select('div.des_wide.f_left')
        HotelDetail_dict["address"] = res[0].select_one("div.hdetial_position > p.poi_text > span").text ## 地址
    except Exception as e:
        print "address"
        print URL
    try:
        HotelDetail_dict["feature"] = res[0].select_one("#CommentTag").text ## 優點集
    except Exception as e:
        HotelDetail_dict["feature"] = "None"
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
            try:
                HotelComm_dict["comment"] = i.select_one(".main_con").text.replace(" ","") ## 評論
            except Exception as e:
                HotelDetail_dict["comment"] = ""
            HotelComm_list.append(HotelComm_dict)
        try:
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight-2500);')
            time.sleep(2)
            driver.find_element_by_css_selector('a.nextpage').click()
            time.sleep(2)
            if count >= com_Num_page:
                break
            else:
                count = count + 50
        except Exception as e:
            break
    HotelDetail_dict["comment_collection"] = HotelComm_list
    # Ctrip_Hotel_list.append(HotelDetail_dict)
    # ==========================#
    ALL = []
    try:
        with open(SaveFile, 'r') as a:
            data = json.load(a)
            # print data
            for j in data:
                print j
                ALL.append(j)
    except Exception as e:
        print e
        print "It's first file!"
    # ==========================#
    ALL.append(HotelDetail_dict.copy())
    contentjson = json.dumps(ALL, ensure_ascii=False)
    with open(SaveFile, 'w') as f:
        f.write(contentjson.encode('utf-8'))
    # ==========================#
    print "Get " + URL
    driver.close()
    worker()

####   爬蟲實施抓取網頁
def worker():
    while not queue.empty():
        url = queue.get()
        crawler(url)

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
NUM_THREADS = 5
####   創建一個 Queue
queue = Queue()
SaveFile = "E:/AB104/Ctrip/test/20170107_Ctrip_Info_ALL.json"
#34
import json
for j in range(1,7):
    with open("E:/AB104/Ctrip/test/20170107_Ctrip_HotelName_list_{}.json".format(j),'r') as a:
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
    # # ==========================#
    # contentjson = json.dumps(Ctrip_Hotel_list, ensure_ascii=False)
    # with open('E:/AB104/Ctrip/20170107_Ctrip_Hotel_Info_{}.json'.format(j), 'w') as f:
    #     f.write(contentjson.encode('utf-8'))
    # # ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 0:03:48.180000!!