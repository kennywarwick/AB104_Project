#coding:UTF-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import json
from datetime import datetime
import random

hotel_list = []
####   創建一個 Queue
queue = Queue()

def sleeptime():
    sl = random.uniform(0.2, 1)
    time.sleep(sl)

def worker():
    while not queue.empty():
        try:
            url = queue.get()
            crawler(url)
        except Exception as e:
            print e
            print "抓取錯誤"

def crawler(tmpurl1):
    try:
        racer = {}
        racer['hotel'] = None
        customer = []
        racer['address'] = None
        racer['level'] = None
        racer['comment_collection'] = None
        sleeptime()
        driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
        driver.get(tmpurl1)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        print "a"
        element = driver.find_element_by_xpath('//*[@id="hotelTmpl"]/div[8]/div[1]/div/a')
        #//*[@id="hotelTmpl"]/div[8]/div[1]/div/a
        print "b"
        time.sleep(2)
        element.click()
        print "c"
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source)
        # print soup.select('h1')[0].select('a')[0].text
        racer['hotel'] = soup.select('h1')[0].select('a')[0].text
        # print soup.select('#review_list_main_score')[0].text.strip('\n')
        racer['level'] = soup.select('#review_list_main_score')[0].text.strip('\n')
        # print soup.select('.hotel_address')[0].text
        racer['address'] = soup.select('.hotel_address')[0].text
        while True:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            item_list = soup.select('.review_item')
            for item in item_list:
                # print item.select('.review_item_reviewer')[0].select('h4')[0].text.strip('\n')
###############################
## 評論分好壞 (for NaiveBayes) ##
#############################################################################################################
#<p class="review_neg"><i class="review_item_icon">눉</i><span itemprop="reviewBody">嬰兒床太舊</span>        #
#</p><p class="review_pos"><i class="review_item_icon">눇</i><span itemprop="reviewBody">服務的態度很好        #
#</span></p>                                                                                                #
#############################################################################################################
                bin = str(item.select('.review_item_review_content')[0])
                try:
                    binMaker1 = bin.split('<i class="review_item_icon">')[1].split('</i><span itemprop="reviewBody">')[0]
                    if binMaker1 == "눉":
                        binMaker1 = 1
                        BadComm = bin.split('<span itemprop="reviewBody">')[1].split('</span>')[0]
                    else:
                        binMaker1 = 0
                        BadComm = "None"
                        GoodComm = bin.split('<span itemprop="reviewBody">')[1].split('</span>')[0]
                    try:
                        binMaker2 = bin.split('<i class="review_item_icon">')[2].split('</i><span itemprop="reviewBody">')[0]
                        if binMaker2 == "눇":
                            binMakerBad = 0
                            GoodComm = bin.split('<span itemprop="reviewBody">')[2].split('</span>')[0]
                    except Exception as e:
                        GoodComm = "None"
                        # print "僅有單一評比"
                except Exception as e:
                    BadComm = "None"
                    GoodComm = "None"
                # print item.select('.review_item_review_content')[0]
                # print item.select('.review_item_review_content')[0].select(".review_item_icon")[0].text.strip('\n').rstrip('\n')
                customer.append({"name": item.select('.review_item_reviewer')[0].select('h4')[0].text.strip('\n'),
                                 "1": BadComm,"0": GoodComm})
            try:
                element = driver.find_element_by_css_selector('#review_next_page_link')
                time.sleep(3)
                element.click()
            except Exception as e:
                # print e
                print "最後一頁"
                break
        #     break
        racer['comment_collection'] = customer
        # hotel_list.append(racer)
    except Exception as e:
        print e
        print tmpurl1
        print "抓取錯誤2"
    driver.close()
    # ==========================#
    ALL = []
    # try:
    #     with open(SaveFile, 'r') as a:
    #         data = json.load(a)
    #         for j in data:
    #             # print j
    #             ALL.append(j)
    # except Exception as e:
    #     print e
    #     print "It's first file!"
    # # ==========================#
    ALL.append(racer.copy())
    contentjson = json.dumps(ALL)#, ensure_ascii=False)
    try:
        nameMark = tmpurl1.split("tw/")[1].split(".zh-tw")[0]
    except Exception as e:
        nameMark = tmpurl1.split("tw/")[1].split("html")[0]
    with open("E:/AB104/Booking/test/20170107_Booking_Info_test{}.json".format(nameMark), 'w') as f:
        f.write(contentjson)

    # with open(SaveFile, 'r') as a:
    #     data = json.load(a)
    #     for j in data:
    #         print j
    # #==========================#
    worker()

s1 = datetime.now()  ####### 起始時間
NUM_THREADS = 4
####   創建一個 Queue
queue = Queue()
# SaveFile = "E:/AB104/Booking/test/20170107_Booking_Info_test{}.json"
s1 = datetime.now()  ####### 起始時間

for j in range(1,8):
    with open("E:/AB104/Booking/20170104_Booking_HotelName_list{}.json".format(j),'r') as a:
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
    # contentjson = json.dumps(hotel_list, ensure_ascii=False)
    # with open(SaveFile.format(j), 'w') as f:
    #     f.write(contentjson.encode('utf-8'))
    # # ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 8:47:14.394000!!
