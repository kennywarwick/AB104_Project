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

####   爬蟲程序
def crawler(url):
    URL = url + "/list-p{}.html"
    url_base = "http://you.ctrip.com/"
    sl = random.uniform(0.2, 0.9)
    time.sleep(sl)
    res_page = r.get(URL.format("1"))
    soup_page = BeautifulSoup(res_page.text)
    page = soup_page.select_one('div.hotel_screening > span.f_right > span.f_ff9100').text
    pageCount = int(math.ceil(int(page) / 20))
    for i in range(1,pageCount+1):
        if i == 51:
            break
        URL_each = url + "/list-p{}.html"
        sl = random.uniform(0.2, 0.9)
        time.sleep(sl)
        r.post(URL.format(i), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
        res = r.get(URL_each.format(i))
        soup = BeautifulSoup(res.text)
        webLink = soup.select('div.eachquarter.cf')
        for i in webLink:
            # print url_base + i.select_one('a')["href"]
            HotelWeb_dict = {}
            HotelWeb_dict["web"] = url_base + i.select_one('a')["href"]
            HotelWeb_List.append(HotelWeb_dict)
    # ==========================#
    contentjson = json.dumps(HotelWeb_List, ensure_ascii=False)
    with open('E:/AB104/Ctrip/20170104_Ctrip_HotelName_list.json', 'w') as f:
        f.write(contentjson.encode('utf-8'))
    # ==========================#

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
HotelWeb_List = []
URLS = []

#34
import json
with open("E:/AB104/Ctrip/ctrip_list.txt",'r') as a:
    data = a.read().splitlines()
    for item in data:
        try:
            URLS = item
            print item
        except Exception as e:
            print e
            print "抓取完畢!"
        crawler(URLS)

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 0:12:35.143000!!