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
import requests
import math
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import signal
import random

def crawler(url):
    onehotel_list = []
    global n
    global s1
    URL = url+"#chkin=2017%2F02%2F16&chkout=2017%2F02%2F17&adults=2&children=0"
    partcomments_list = []
    ###### get website ######
    driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
            # driver = webdriver.PhantomJS("E:\phantomjs\phantomjs.exe")
    countTimes = 1
    ######### Get the url page #########
    while countTimes < 15:
        try:
            driver.get(URL)
            time.sleep(n)
            break
        except Exception as e:
            countTimes = countTimes + 1
            driver.get(URL).refresh()
            time.sleep(10)

    #### Click the comments button #####
    if  len(driver.find_element_by_css_selector('#tab-reviews').text) > 0:
        driver.find_element_by_css_selector('#tab-reviews').click()
        time.sleep(n)
        racer = {}
        ##### Get the hotel's Info ######
        soup = BeautifulSoup(driver.page_source)
        res = soup.select('body > div.site-content-wrap.hotelInformation > div.site-content.cols-row')[0]
        racer["hotel"] = res.select("#hotel-name")[0].text.replace(" ", "").replace("\n", "")
        # print res.select('#license-plate > div.address > div > a.map-link')[0]
        try:
            racer["level"] = res.select("div.summary-wrapper > article > div > div.cols-nested.aggregateRating > div.guest-rating")[0].text.split("Expedia")[0].replace(" ", "").replace("\n", "")
        except Exception as e:
            print "There is no guest-rating"
        try:
            res = soup.select('div.full-address')[0]
            Road = res.select(".map-link")[0].text
            Counties = res.select(".map-link")[0].text
            racer["address"] = Counties + Road
        except Exception as e:
            print "There is no address"

        count = 0
        ###### comments crawler ######
        while True:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            for rm_tag in soup.find_all(['button']):
                rm_tag.extract()  # 刪除button<tag>部分之文字
            res = soup.select('.segment.no-target.review.cf.translate-original')
            for i in res:
                partcomments_list.append({"name":i.select('div.user.cf')[0].text,"comment":i.select('div.details')[0].text.encode('utf-8').split("此")[0].replace("\n", "　").replace("\t", "　").decode('utf-8')})
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight-1450);')
            time.sleep(n)
            try:
                element =driver.find_element_by_css_selector('#reviews-pagination > fieldset > div > button.pagination-next > abbr')
                time.sleep(n)
                element.click()
            except Exception as e:
                break
            count = count + 1
            print count
        racer['comment_collection'] = partcomments_list
        onehotel_list.append(racer)

    hotel_list.append(racer)
    # ##############Save################
    # Partjson = json.dumps(onehotel_list, ensure_ascii=False)
    # with open('E:/AB104/Expedia/{}_comments.json'.format(URL.split("tw/")[1].split(".")[0]), 'w') as f:
    #     f.write(Partjson.encode('utf-8'))
    print URL.split("tw/")[1].split(".")[0] + " is crawled!"
    driver.close()
    worker()

####   爬蟲實施抓取網頁
def worker():
    while not queue.empty():
        url = queue.get()
        crawler(url)

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
hotel_list = []
partcomments_list = []
n=2
####   創建一個 Queue
queue = Queue()

#==========================#
import json
web_list = []
with open('E:/AB104/Expedia/20170104_ExpediaHotelName_web2.json') as data_file:
    data = json.load(data_file)
    for i in data:
        web_list.append(i["web"])

#==========================#
# count = 1
for i in web_list:
    URL = i
    try:
        queue.put(URL)
    except Exception as e:
        print e
        print "抓取完畢!"

    ####   啟動THREAD
threads = map(lambda i: Thread(target=worker), xrange(8))
map(lambda th: th.start(), threads)
map(lambda th: th.join(), threads)

# ==========================#
contentjson = json.dumps(hotel_list, ensure_ascii=False)
with open('E:/AB104/Expedia/20170104_Expedia_Hotel_Info.json', 'w') as f:
    f.write(contentjson.encode('utf-8'))
# ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間

#All  Finish 1 day, 22:00:58.516000!!
