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
cityName_Info = []
Hotels_Info = []
Hotel_Info = []
address_Info = []
url_base = 'https://www.hotelscombined.com.tw'
driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
driver1 = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
driver2 = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
driver.get(url_base+'/Place/Taiwan.htm')
soup = BeautifulSoup(driver.page_source)
block = soup.select('#hc_inAround > div > div.hc_m_content')[0].select('li')
# print type(block)
# print block
## 抓取地區名稱以及該區域網址 for 進入抓取資料用
for i in block:
    try:
        Block_dict = {}
        Block_dict['Block_Name'] = i.select('a')[0].text
        # print Block_dict['Block_Name']
        Block_dict['web'] = url_base + i.select_one('a')['href']
        # print Block_dict['web']
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

# 進入區域後先選定住宿飯店類型
    driver1.get(url)
    soup = BeautifulSoup(driver1.page_source)
    find = soup.select('#hc_popularHotels > div > div.hc_m_content > div.hc_sri')

    for i in find:
        try:
            typeCount_dict = {}
            typeCount_dict['hotelName'] = i.select_one("a").text  # .replace("\n","")
            typeCount_dict['web'] = url_base + i.select_one("a")['href']  # .replace("\n","")
        except Exception as e:
            print e
        typeCount_Info.append(typeCount_dict)

    # #========== 各縣市飯店類別與數量 ===========#
    # for i in typeCount_Info:
    #     print i
    # #=======================================#

    for i in typeCount_Info:
        cityName_dict = {}
        cityName_dict['cityName'] = i.get('web').split("/")[4].split(".")[0]
        # print cityName_dict['cityName']
        cityName_Info.append(cityName_dict)

    for i in typeCount_Info:
        cityName_dict = {}
        cityName_dict['cityName'] = i.get('web').split("/")[4].split(".")[0]
        cityName_Info.append(cityName_dict)

    for i in cityName_Info:
        url_detil = "https://www.hotelscombined.com.tw/Hotel/Search?fileName={}&checkin=2017-02-16&checkout=2017-02-17&rooms=1&adults_1=2"
        driver2.get(url_detil.format(i.get('cityName')))
        soup = BeautifulSoup(driver2.page_source)
        find = soup.select('#hc_htl_intro')
        # print find
        for i in find:
            address_dict = {}
            address_dict['Hotelname'] = i.select_one(".hc_htl_intro_name").text.split(",")[0].replace("\n", "").replace(" ", "")
            address_dict['addressRoadname'] = i.select_one(".hc_htl_intro_inner").text.split(",")[1].replace("\n",""
                          ).replace(" ","") + i.select_one(".hc_htl_intro_inner").text.split(",")[0].replace("\n", "").replace(" ", "")
            # print address_dict['Hotelname']
            # print address_dict['addressRoadname']
            address_Info.append(address_dict)
        # for i in find:
        #     price_dict = {}
        #     price_dict['Hotelname'] = i.select_one("#searchResultsHolder").text.split(",")[0].replace("\n", "").replace(" ", "")
        #     address_Info.append(price_dict)
    #========== 各縣市飯店類別與數量 ===========#
    for i in address_Info:
        print i
    #=======================================#




driver2.quit()
driver1.quit()
driver.quit()