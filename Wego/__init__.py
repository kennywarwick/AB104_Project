#coding:UTF-8

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import math

## 地區先以台灣為主，故須先行設定台灣範圍
Block_Info = []
typeCount_Info = []
Hotels_Info = []
Hotel_Info = []
url_base = 'https://www.wego.tw'
res = requests.get(url_base+'/hotels/taiwan',verify=False)
soup = BeautifulSoup(res.text)

## 抓取地區名稱以及該區域網址 for 進入抓取資料用
for i in soup.select('.medium-8'):
    try:
        Block_dict = {}
        Block_dict['Block_Name'] = i.select_one('a').text
        Block_dict['web'] = url_base + i.select_one('a')['href']
    except Exception as e:
        print e
    Block_Info.append(Block_dict)
# #========== 觀察抓取資訊 ===========#
# for i in Block_Info:
#     print i
# #=================================#
## 抓取 Block_dict 裡面 web 之部分
for i in Block_Info:
    url = i.get('web')
    # #========== 觀察抓取資訊 ===========#
    # print url
    # #=================================#
## 進入區域後先選定住宿飯店類型
url = 'https://www.wego.tw/hotels/taiwan/taipei/20161215/20161216/88892137'  ## For test
res = requests.get(url, verify=False)
soup = BeautifulSoup(res.text)
find = soup.select('.listing-container')
print find
for i in find:
    try:
        typeCount_dict = {}
        typeCount_dict['Block'] = url.split('-')[2]
        typeCount_dict['Type'] = i.select_one('.tab_label').text
        typeCount_dict['count'] = i.select_one('.tab_count').text.split('(')[1].split(')')[0]
    except Exception as e:
        print e
    typeCount_Info.append(typeCount_dict)

#========== 各縣市飯店類別與數量 ===========#
for i in typeCount_Info:
    print i
#=======================================#


