#coding:UTF-8
# Expedia爬蟲
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from Queue import Queue
from threading import Thread
import random
import sys
from datetime import datetime
from datetime import timedelta
import math
import json

def sleeptime():
    sl = random.uniform(0.2, 1.2)
    time.sleep(sl)

####   爬蟲程序
def crawler(url):
    sleeptime()
    try:
        page = 1
        pageCount = 2
        # print now
        while page < pageCount:
        ########################################################################################
            # driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
            driver = webdriver.Chrome(executable_path="/opt/selenium/chromedriver-2.25")
            countTimes = 0
            while countTimes < 5:
                try:
                    driver.get(url.format( page, now, Tomorrow))
                    break
                except Exception as e:
                    countTimes = countTimes + 1
                    driver.get(url.format( page, now, Tomorrow)).refresh()
            ########################################################################################
            if page == 1:
                soup_page = BeautifulSoup(driver.page_source.encode("utf-8"))
                pagetext = soup_page.select_one("#paginationContainer > div > nav > fieldset > p")
                pageCount = int(math.ceil(int(pagetext.text.split(" ")[6]) / 50))
            page = page + 1
            sleeptime()
            soup = BeautifulSoup(driver.page_source.encode("utf-8"))
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            item_list = soup.select('.hotel.listing.col.organic')
            print len(item_list)
            for item in item_list:
                HotelName_dict = {}
                HotelName_dict["hotel"] = item.select(".hotelName")[0].text
                HotelName_dict["url"] = item.select("div > div.flex-link-wrap > a")[0]['href']
                #photo################################################
                try:
                    HotelName_dict["photo"] = item.select_one("div.hotel-thumbnail")['style'].split("//")[1].split('"')[0]
                except Exception as e:
                    HotelName_dict["photo"] = None
                #actualPrice################################################
                try:
                    HotelName_dict["Special_price"] = item.select(".actualPrice")[0].text.encode('utf-8').rstrip().strip().split("$")[1].decode('utf-8')
                except IndexError as IE:
                    HotelName_dict["Special_price"] = None
                #strickPrice################################################
                try:
                    HotelName_dict["Original_price"] = item.select(".strikePrice")[0].text.encode('utf-8').replace("\n", '').replace('"', '').replace(" ",'').split('此比較價格為這家飯店在Expedia智遊網於未來14天內，至少有一天有空房的最高價格。')[0].split("$")[1].decode('utf-8')
                except IndexError as IE:
                    HotelName_dict["Original_price"] = None

                ## 進入抓取地址 ######################
                sleeptime()
                res = requests.get(HotelName_dict["url"], verify=False)
                soup = BeautifulSoup(res.text)
                try:
                    resq = soup.select('#license-plate')[0]
                except Exception as e:
                    print "res's problem!"
                    print HotelName_dict["url"]
                try:
                    resAddress = soup.select('div.full-address')[0]
                    address = resAddress.select(".map-link")[0].text.strip()
                    HotelName_dict["address"] = address
                except Exception as e:
                    HotelName_dict["address"] = None
                    print "address's problem!"
                    print HotelName_dict["url"]
                #################################################
                HotelName_list.append(HotelName_dict.copy())
                print "============Get this hotel_info!============"
            sleeptime()
            driver.close()
    except Exception as e:
        print e
        queue.put(url)
        driver.close()

    worker()

####   爬蟲實施抓取網頁
def worker():
    while not queue.empty():
        url = queue.get()
        crawler(url)

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
sys.setrecursionlimit(10**6)
now = datetime.now()
aDay = timedelta(days=1)
Tomorrow = now + aDay
now = now.strftime('%Y/%m/%d')
Tomorrow = Tomorrow.strftime('%Y/%m/%d')
HotelName_list = []
HotelNameError_list = []
NUM_THREADS = 2
#12
# urls = ["https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E5%8C%97&adults=2&regionId=3518&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E8%8A%B1%E8%93%AE&adults=2&regionId=1531&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%BE%85%E6%9D%B1&adults=2&regionId=6051185&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%81%86%E6%98%A5&adults=2&regionId=6047453&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E4%B8%AD&adults=2&regionId=3586&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%A4%81%E6%BA%AA&adults=2&regionId=6051183&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E9%AB%98%E9%9B%84&adults=2&regionId=1808&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%96%B0%E5%8C%97%E5%B8%82&adults=2&regionId=6178032&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E4%BB%81%E6%84%9B&adults=2&regionId=6141173&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E5%8D%97&adults=2&regionId=3499&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E6%9D%B1&adults=2&regionId=3558&sort=recommended&page={}&startDate={}&endDate={}",
urls = ["https://www.expedia.com.tw/Hotel-Search?#destination=%E6%A1%83%E5%9C%92&adults=2&regionId=177485&sort=recommended&page={}&startDate={}&endDate={}"]

####   創建一個 Queue
queue = Queue()

for i in urls:
    ####  抓取每一頁 URL
    try:
        queue.put(i)
    except Exception as e:
        print e
        print "抓取完畢!"

####   啟動THREAD
threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
map(lambda th: th.start(), threads)
map(lambda th: th.join(), threads)
time.strftime("%d/%m/%Y")

#===========================#
try:
    contentjson = json.dumps(HotelName_list, ensure_ascii=False)
    with open('/home/ab104/ab104_g1/Expedia/專題/crawler/Expedia_Menu_Queue_test.json', 'w') as f:  #' + str(now) + '
        f.write(contentjson.encode('utf-8'))
    f.close()
except Exception as e:
    print e
#===========================#
s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 0:29:14.592000!!