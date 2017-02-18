#coding:UTF-8
# Expedia爬蟲
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests as r
import math
import re
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
    sl = random.uniform(0.5, 1.5)
    time.sleep(sl)
####   爬蟲程序
def crawler(url):
    nip = random.randint(0, len(ipList)-1)
    ip = ipList.__getitem__(nip).strip()
    proxy = {"http": "http://{}".format(ip)}
    n = 0
    while True:
        try:
            if n >= 5:
                print("http not found !!")
                return False
            res = r.get(url, proxies=proxy, timeout=6)
            # if res.status_code==200:
            #     print res.text
            break
        except:
            n += 1
            nip = random.randint(0, len(ipList) - 1)
            ip = ipList.__getitem__(nip).strip()
            proxy = {"http": "http://{}".format(ip)}
            pass

    global sleeptimes
    sleeptime()
    driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
    countTimes = 1

    #sr_header - -title
    res = r.get(url)
    soup_page = BeautifulSoup(res.text)
    page = soup_page.select_one("div.sr_header--title").select_one("h1").text.split(" ")[1]
    # print page
    sleeptime()
    driver.get(url)
    # print url
    count = 1
    for i in range(1,int(page)+1):
        sleeptime()
        print count
        soup = BeautifulSoup(driver.page_source)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight-1800);')
        item_list = soup.select_one('#ajaxsrwrap').select(".sr-hotel__title")
        # print item_list
        for item in item_list:
            HotelName_dict = {}
            # print item.select(".sr-hotel__title")[0].select("a")[0]['href']
            HotelName_dict["web"] = base_URL+item.select("a")[0]['href']
            # print HotelName_dict["web"]
            HotelWeb_List.append(HotelName_dict)
        sleeptime()
        try:
            time.sleep(1.5)
            driver.find_element_by_css_selector('#search_results_table > div.results-paging > a.paging-next').click()
            time.sleep(1.5)
            count = count+1
        except Exception as e:
            print url
            print e
            print "========== This is end of the page! =========="
            count = count + 1
            break

    driver.close()
    worker()

####   爬蟲實施抓取網頁
def worker():
    while not queue.empty():
        url = queue.get()
        crawler(url)

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
sleeptimes= 3
HotelWeb_List = []
NUM_THREADS = 2
#20
base_URL = "http://www.booking.com"
URL = "http://www.booking.com/searchresults.zh-tw.html?aid=304142;label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaOcBiAEBmAEwuAEGyAEM2AED6AEBqAID;sid=e89b0f5eb7660ade1650a2df5645f4af;city="
# URLS = [ URL + "-2637882&",URL + "-2631690&",URL + "-2637928&",URL + "-2632378&",URL + "-2635345&",URL + "-2632489&",URL + "-2637868&",URL + "-2640304&",URL + "-2637824&",URL + "-2629946&",URL + "-2633593&",URL + "-2628307&",URL + "-2626922&",URL + "-2634667&",URL + "900054432&",URL + "-2640880&",URL + "-2634978&",URL + "-2635904&",URL + "900039918&",URL + "900048295&"]
URLS = [URL + "900039918&",URL + "900048295&"]

####   創建一個 Queue
queue = Queue()

for i in URLS:
    ####  抓取每一頁 URL
    try:
        queue.put(i)
        # print type(i)
    except Exception as e:
        print e
        print "抓取完畢!"

####   啟動THREAD
threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
map(lambda th: th.start(), threads)
map(lambda th: th.join(), threads)
time.strftime("%d/%m/%Y")
# ==========================#
import json
contentjson = json.dumps(HotelWeb_List, ensure_ascii=False)
with open('E:/AB104/Booking/20170104_Booking_HotelName_list7.json', 'w') as f:
    f.write(contentjson.encode('utf-8'))
# ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 0:03:48.180000!!(鎖 仁愛地區未拿到)