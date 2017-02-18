#coding:UTF-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pymongo


from bs4 import BeautifulSoup
url_base = 'https://www.hotelscombined.com.tw'
url = 'https://www.hotelscombined.com.tw/Place/Taiwan_Taoyuan_International_Airport.htm'  ## For test
driver1 = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
driver2 = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
driver1.get(url)
typeCount_Info = []
cityName_Info = []
address_Info = []
soup = BeautifulSoup(driver1.page_source)
find = soup.select('#hc_popularHotels > div > div.hc_m_content > div.hc_sri')
for i in find:
    try:
        typeCount_dict = {}
        typeCount_dict['hotelName'] = i.select_one("a").text#.replace("\n","")
        typeCount_dict['web'] = url_base + i.select_one("a")['href']#.replace("\n","")
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
    cityName_Info.append(cityName_dict)

for i in cityName_Info:
    url_detil = "https://www.hotelscombined.com.tw/Hotel/Search?fileName={}&checkin=2017-02-16&checkout=2017-02-17&rooms=1&adults_1=2"
    driver2.get(url_detil.format(i.get('cityName')))
    soup = BeautifulSoup(driver2.page_source)
    find = soup.select('#hc_htl_intro')
    # print find
    for i in find:
        address_dict = {}
        address_dict['Hotelname'] =i.select_one(".hc_htl_intro_name").text.split(",")[0].replace("\n","").replace(" ","")
        address_dict['addressRoadname'] = i.select_one(".hc_htl_intro_inner").text.split(",")[1].replace("\n","").replace(" ",""
                                          "") + i.select_one(".hc_htl_intro_inner").text.split(",")[0].replace("\n","").replace(" ","")
        # print address_dict['Hotelname']
        # print address_dict['addressRoadname']
        address_Info.append(address_dict)
    # find1 = soup.select('#hc_htl_pm_rates_content')
    # for i in find:
    #     address_dict['School'] = i.select_one(".hc_tbl_col2").text
    #     print address_dict['School']

#========== 各縣市飯店類別與數量 ===========#
for i in address_Info:
    print i
#=======================================#


driver2.quit()
driver1.quit()

