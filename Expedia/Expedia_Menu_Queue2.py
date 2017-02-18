#coding:UTF-8
# Expedia爬蟲
import math
import random
import sys
import time
from Queue import Queue
from datetime import datetime
from datetime import timedelta
from threading import Thread

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from Tool import geocoder

#得到遞迴的次數，要不然不停的自己調用自己會引起崩潰，設置遞迴的次數
sys.setrecursionlimit(10**6)

now = datetime.now()
aDay = timedelta(days=1)
Tomorrow = now + aDay
# now = now.strftime('%Y/%m/%d')
# Tomorrow = Tomorrow.strftime('%Y/%m/%d')
now = "2017/02/16"
Tomorrow = "2017/02/17"


ipList = []
with open("E:/python/IP/ips2.txt","r") as f:
    for item in f.readlines():
        ipList.append(item)
    f.close()

def sleeptime():
    sl = random.uniform(0.2, 1.2)
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
            res = requests.get(url, proxies=proxy, timeout=6)
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

    try:
        page = 1
        pageCount = 2
        # print now
        while page < pageCount:
        ########################################################################################
            driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
            countTimes = 0
            while countTimes < 3:
                try:
                    time.sleep(1)
                    driver.get(url.format( page, now, Tomorrow))
                    break
                except Exception as e:
                    countTimes = countTimes + 1
                    driver.get(url.format( page, now, Tomorrow)).refresh()
                    print "連線有問題!".encode("utf-8") , countTimes
            ######################################################################################
            if page == 1:
                # print driver.page_source
                # print type(driver.page_source)
                soup_page = BeautifulSoup(driver.page_source)
                # print soup_page
                pagetext = soup_page.select_one("#paginationContainer > div > nav > fieldset > p")
                # print pagetext
                pageCount = int(math.ceil(int(pagetext.text.split(" ")[6]) / 50))
                # print pageCount
            page = page + 1
            sleeptime()
            soup = BeautifulSoup(driver.page_source)
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            item_list = soup.select('.hotel.listing.col.organic')
            # print len(item_list)
            # print type(item_list)
            for item in item_list:
                HotelName_dict = {}
                HotelName_dict["hotel"] = item.select(".hotelName")[0].text.replace('\n'," ").rstrip().strip()
                # print HotelName_dict["hotelName"]
                HotelName_dict["url"] = item.select("div > div.flex-link-wrap > a")[0]['href']
                # print HotelName_dict["url"]
                #photo################################################
                try:
                    HotelName_dict["photo"] = item.select_one("div.hotel-thumbnail")['style'].split("//")[1].split('"')[0]
                except Exception as e:
                    HotelName_dict["photo"] = None
                    # print "photo's problem!"
                    # print HotelName_dict["url"]
                #actualPrice################################################
                try:
                    # print item.select(".actualPrice")[0]
                    HotelName_dict["Special_price"] = item.select(".actualPrice")[0].text.encode('utf-8').rstrip().strip().split("$")[1].decode('utf-8')
                except IndexError as IE:
                    HotelName_dict["Special_price"] = None
                    # print "actualPrice's problem!"
                    # print HotelName_dict["url"]
                #strickPrice################################################
                try:
                    HotelName_dict["Original_price"] = item.select(".strikePrice")[0].text.encode('utf-8').replace("\n", '').replace('"', '').replace(" ",'').split('此比較價格為這家飯店在Expedia智遊網於未來14天內，至少有一天有空房的最高價格。')[0].split("$")[1].split('劃掉')[0].decode('utf-8')
                except IndexError as IE:
                    HotelName_dict["Original_price"] = None
                    # print "strickPrice's problem!"
                    # print HotelName_dict["url"]
                #################################################
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
                    saddress = resAddress.select(".map-link")[0].select_one(".street-address").text
                    city = resAddress.select(".map-link")[0].select_one(".city").text
                    # province = resAddress.select(".map-link")[0].select_one(".province").text
                    Road = saddress + " " + city
                    print Road
                    # print "address"
                    HotelName_dict["address"] = Road

                except Exception as e:
                    HotelName_dict["address"] = None
                    print "address's problem!"
                    print HotelName_dict["url"]
                #################################################
                try:
                    # print Road.replace('\n'," ")
                    g = geocoder.google(Road.rstrip().strip())
                    time.sleep(0.5)
                    print g.latlng
                    HotelName_dict["longitude"] = g.latlng[1]
                    HotelName_dict["latitude"] = g.latlng[0]
                    print HotelName_dict["longitude"]
                    print HotelName_dict["latitude"]
                except Exception as a:
                    print "經緯度沒抓到"
                    print Road
                    print Road.replace('\n'," ").rstrip().strip()
                    print HotelName_dict["hotel"]
                HotelName_list.append(HotelName_dict.copy())
                print "Get this hotel_info!"
            # print "===="
            # print page
            # print pageCount
            # print "===="
            sleeptime()
            driver.close()
    except Exception as e:
        print e
        print "連結有問題..."
        queue.put(url)
        print "把url放回queue裡等待下次抓取"
        # driver.close()

    worker()

####   爬蟲實施抓取網頁
def worker():
    while not queue.empty():
        url = queue.get()
        crawler(url)

####   開啟瀏覽器
s1 = datetime.now()  ####### 起始時間
sleeptimes= 3
HotelName_list = []
HotelNameError_list = []
NUM_THREADS = 3
#12

urls = ["https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E5%8C%97&adults=2&regionId=3518&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E8%8A%B1%E8%93%AE&adults=2&regionId=1531&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%BE%85%E6%9D%B1&adults=2&regionId=6051185&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%81%86%E6%98%A5&adults=2&regionId=6047453&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E4%B8%AD&adults=2&regionId=3586&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%A4%81%E6%BA%AA&adults=2&regionId=6051183&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E9%AB%98%E9%9B%84&adults=2&regionId=1808&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%96%B0%E5%8C%97%E5%B8%82&adults=2&regionId=6178032&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E4%BB%81%E6%84%9B&adults=2&regionId=6141173&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E5%8D%97&adults=2&regionId=3499&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E6%9D%B1&adults=2&regionId=3558&sort=recommended&page={}&startDate={}&endDate={}",
        "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%A1%83%E5%9C%92&adults=2&regionId=177485&sort=recommended&page={}&startDate={}&endDate={}"]

# urls = ["https://www.expedia.com.tw/Hotel-Search?#destination=%E7%BE%85%E6%9D%B1&adults=2&regionId=6051185&sort=recommended&page={}&startDate={}&endDate={}",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%A1%83%E5%9C%92&adults=2&regionId=177485&sort=recommended&page={}&startDate={}&endDate={}"]
####   創建一個 Queue
queue = Queue()

for i in urls:
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
try:
    contentjson = json.dumps(HotelName_list, ensure_ascii=False)
    with open('E:/AB104/Expedia/last/Expedia_Menu_Queue_test_final11111.json', 'w') as f:  #' + str(now) + '
        f.write(contentjson.encode('utf-8'))
    f.close()
except Exception as e:
    print "無法存檔"
    print e
# ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 0:29:14.592000!!