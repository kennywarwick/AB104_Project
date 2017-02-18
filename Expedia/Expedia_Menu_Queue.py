#coding:UTF-8
# Expedia爬蟲
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import math
from datetime import datetime
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import random
import sys

sys.setrecursionlimit(10**6)
now = datetime.strftime(datetime.now(), '%Y-%m-%d')

ipList = []
with open("E:/python/IP/ips2.txt","r") as f:
    for item in f.readlines():
        ipList.append(item)
    f.close()

def sleeptime():
    sl = random.uniform(0.2, 0.7)
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
    driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
    try:
        driver.get(url)
        sleeptime()
        while True:
            try:
                element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#modalCloseButton > span.icon.icon-close")))
                # print element
                sleeptime()
                element.click()
                # driver.find_element_by_css_selector('#modalCloseButton > span.icon.icon-close').click()
                break
            except:
                driver.get(url).refresh()
                sleeptime()

        sleeptime()
        soup_page = BeautifulSoup(driver.page_source)
        page = soup_page.select_one("#paginationContainer > div > nav > fieldset > p")
        pageCount = int(math.ceil(int(page.text.split(" ")[6]) / 50))+1
        # print pageCount
        # 正在顯示第 1 - 50 筆搜尋結果 (共 741 筆)

        for i in range(1,pageCount+1):
            sleeptime()
            soup = BeautifulSoup(driver.page_source)
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            item_list = soup.select('.hotel.listing.col.organic')
            for item in item_list:
                HotelName_dict = {}
                HotelName_dict["hotelName"] = item.select(".hotelName")[0].text
                HotelName_dict["web"] = item.select("div > div.flex-link-wrap > a")[0]['href']
                print HotelName_dict["web"]
                ## 進入抓取地址 ######################
                sleeptime()
                res = requests.get(HotelName_dict["web"], verify=False)
                soup = BeautifulSoup(res.text)
                try:
                    res = soup.select('#license-plate')[0]
                except Exception as e:
                    print "res's problem!"
                    print HotelName_dict["web"]
                #################################################
                try:
                    res = soup.select('div.full-address')[0]
                    Road = res.select(".map-link")[0].text
                    Counties = res.select(".map-link")[0].text
                    HotelName_dict["address"] = Counties + Road
                    print "Get this address!"
                except Exception as e:
                    HotelName_dict["address"] = 'none'
                    print "address's problem!"
                    print HotelName_dict["web"]
                #################################################
                try:
                    HotelName_dict["photo"] = item.select_one("div.hotel-thumbnail")['style'].split("//")[1].split('"')[0]
                    print "Get this photo!"
                except Exception as e:
                    HotelName_dict["photo"] = 'none'
                    print "photo's problem!"
                    print HotelName_dict["web"]
                #################################################
                try:
                    HotelName_dict["actualPrice"] = item.select(".actualPrice")[0].text.encode('utf-8').rstrip().strip().split("$")[1].decode('utf-8')
                    print "Get this actualPrice!"
                except IndexError as IE:
                    HotelName_dict["actualPrice"] = 'none'
                    print "actualPrice's problem!"
                    print HotelName_dict["web"]
                #################################################
                try:
                    HotelName_dict["strickPrice"] = item.select(".strikePrice")[0].text.encode('utf-8').replace("\n", '').replace('"', '').replace(" ",'').split('此比較價格為這家飯店在Expedia智遊網於未來14天內，至少有一天有空房的最高價格。')[0].split("$")[1].decode('utf-8')
                    print "Get this strickPrice!"
                except IndexError as IE:
                    HotelName_dict["strickPrice"] = 'none'
                    print "strickPrice's problem!"
                    print HotelName_dict["web"]
                #################################################
                HotelName_list.append(HotelName_dict.copy())
                print "Get this hotel_info!"
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            sleeptime()
            try:
                driver.find_element_by_css_selector('#paginationContainer > div > nav > fieldset > div > button.pagination-next > abbr').click()
            except Exception as e:
                print "========== This is end of the page! =========="
            sleeptime()


        driver.close()
    except Exception as e:
        print e
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
NUM_THREADS = 1
#12
# urls = ["https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E5%8C%97&adults=2&regionId=3518&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E8%8A%B1%E8%93%AE&adults=2&regionId=1531&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%BE%85%E6%9D%B1&adults=2&regionId=6051185&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%81%86%E6%98%A5&adults=2&regionId=6047453&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E4%B8%AD&adults=2&regionId=3586&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%A4%81%E6%BA%AA&adults=2&regionId=6051183&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E9%AB%98%E9%9B%84&adults=2&regionId=1808&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%96%B0%E5%8C%97%E5%B8%82&adults=2&regionId=6178032&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E4%BB%81%E6%84%9B&adults=2&regionId=6141173&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E5%8D%97&adults=2&regionId=3499&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E5%8F%B0%E6%9D%B1&adults=2&regionId=3558&sort=recommended",
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E6%A1%83%E5%9C%92&adults=2&regionId=177485&sort=recommended"]

#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%BE%85%E6%9D%B1&adults=2&regionId=6051185&sort=recommended"]
#         "https://www.expedia.com.tw/Hotel-Search?#destination=%E7%BE%85%E6%9D%B1,+%E5%8F%B0%E7%81%A3&adults=2&regionId=6051185&sort=recommended    &page=1&startDate=2017/02/17&endDate=2017/02/18"]
urls = ["https://www.expedia.com.tw/Hotel-Search?#destination=%E7%BE%85%E6%9D%B1&adults=2&regionId=6051185&sort=recommended&page=1&startDate=2017/02/17&endDate=2017/02/18"]
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
contentjson = json.dumps(HotelName_list, ensure_ascii=False)
with open('E:/AB104/Expedia/last/Expedia_Menu_Queue' + str(now) + '.json', 'w') as f:
    f.write(contentjson.encode('utf-8'))
f.close()
# ==========================#

s2 = datetime.now()  ####### 結束時間
print "All  Finish " + str(s2 - s1) + "!!"  ####### 總共爬取資料耗費時間
#All  Finish 2:06:02.331000!!