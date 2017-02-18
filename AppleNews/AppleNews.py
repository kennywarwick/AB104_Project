#coding:UTF-8
import requests as req
import time
from datetime import datetime
from bs4 import BeautifulSoup
from threading import Thread
import json
import math
from Queue import Queue
import os
import sys
sys.setrecursionlimit(10**6)

nameList = []

now = datetime.strftime(datetime.now(), '%Y-%m-%d')
startDate = "2016-02-17"    # 搜尋條件起始時間
startTime = datetime.now()  # 起始時間
NUM_THREADS = 5
APPLE_URL = "http://search.appledaily.com.tw/appledaily/search"
SaveFile = "E:/AB104/AppleNews_{}_" + str(now) +".json"

with open("E:/AB104/AB104/OpenData/hotelNametest.txt","r") as f:
    for item in f.readlines():
        # print item
        nameList.append(item.strip())
    f.close()

##############################################################################
def timeSpend(startTime,endTime):
    return (endTime - startTime).seconds

#POST DATA
def postData(news_page, querystr):
    global search_data

    search_data = {
        "searchMode": "Adv",
        "searchType": "text",
        "querystrA": querystr,
        "select": "AND",
        "source": "",
        "sdate": startDate,
        "edate": now,
        "page": news_page
    }
#First POST DATA
def FirstPostData(querystr):
    global searchFirst_data

    searchFirst_data = {
        "searchMode": "Adv",
        "searchType": "text",
        "querystrA": querystr,
        "select": "AND",
        "source": "",
        "sdate": startDate,
        "edate": now,
        "page": 1
    }

def main():
    while not queue.empty():
        querystr = queue.get()
        # print querystr
        getText(querystr)
        # print searchNumber

def getText(querystr):
    print "============================"
    print querystr
    articles = []
    FirstPostData(querystr)
    res = req.post(APPLE_URL, data=searchFirst_data)
    soup = BeautifulSoup(res.text, 'lxml')
    try:
        # print soup.select_one("#result_details")
        searchNumber = math.ceil(int(soup.select_one(".nus > span").text) / 10)+1.0
        # print searchNumber
        article_dict = {}
        article_dict["hotel"] = querystr.decode("utf-8")
        news = []
        for i in range(1,int(searchNumber)+1):
            print i
            postData(i, querystr)
            news_dict = {}
            res = req.post(APPLE_URL, data=search_data)
            soup = BeautifulSoup(res.text, 'lxml')
            soup = soup.select("#result > li")
            for item in soup:
                news_dict["href"] = item.select_one('a')['href'].split("applesearch/")[0].strip()
                news_dict["title"] = item.select_one('a').text.strip()
                # article_dict["content"] = i.select_one('p').text.strip()
                news_dict["datetime"] = item.select_one('time').text.strip()
                print news_dict["href"]
                news.append(news_dict.copy())
                time.sleep(0.00000001)
        article_dict["News"] = news
        articles.append(article_dict)
    except Exception as e:
        print querystr, ", there is no news!"
        print e

    encodedJson = json.dumps(articles, ensure_ascii=False)
    if os.path.isfile("E:/AB104/AppleNews_" + str(now) +".json"):# 如果不存在就返回False
        print "a"
        with open("E:/AB104/AppleNews_" + str(now) +".json", 'a') as f:
            f.write(encodedJson.encode('utf-8'))
    else:
        print "w"
        with open("E:/AB104/AppleNews_" + str(now) +".json", 'w') as f:
            f.write(encodedJson.encode('utf-8'))

    main()

##############################################################################
queue = Queue()

for querystr in nameList:
    try:
        queue.put(querystr)
    except Exception as e:
        print e
        print "抓取完畢!"

####   啟動THREAD
threads = map(lambda i: Thread(target=main), xrange(NUM_THREADS))
map(lambda th: th.start(), threads)
map(lambda th: th.join(), threads)

print "資料抓取完成總耗時：", datetime.now() - startTime
print "開始匯出檔案..."
print "匯出檔案完成 !!"
print "匯出檔案完成總耗時：", timeSpend(startTime, datetime.now())




