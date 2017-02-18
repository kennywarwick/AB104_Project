#coding:UTF-8
# Expedia爬蟲
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
import time
import re
import math
import requests
from bs4 import BeautifulSoup
from datetime import datetime

s1 = datetime.now()
n=5
hotel_list = []
URL='https://www.expedia.com.tw/Taipei-Hotels-Royal-Seasons-Hotel-Taipei.h2510620.Hotel-Information?rm1=a2&hwrqCacheKey=05f5e56a-df26-482f-b889-1ba9b3b26e14HWRQ1481006608216&c=cb9482ea-97e3-408b-96d6-356db32fd953&&exp_dp=1856.52&exp_ts=1481006608888&exp_curr=TWD&exp_pg=HSR'
driver1 = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
driver1.get(URL)
time.sleep(n)
element =WebDriverWait(driver1, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#modalCloseButton > span.icon.icon-close")))
# print element
time.sleep(n)
element.click()
driver1.execute_script('window.scrollTo(0, 1500);')
time.sleep(n)
driver1.find_element_by_css_selector('#tab-reviews').click()
soup_page = BeautifulSoup(driver1.page_source)
page = soup_page.select_one("#reviews-pagination > fieldset > p")
# print page #only for counting the page number
pageCount = int(math.ceil(int(page.text.split(" ")[6]) / 10))
for i in range(1,pageCount+2):
    hotel_dict = {}
    soup = BeautifulSoup(driver1.page_source,'lxml')
    for rm_tag in soup.find_all(['button']):
        rm_tag.extract()    #刪除button<tag>部分之文字
    res = soup.select('.segment.no-target.review.cf.translate-original')
    # print res
    for i in  res:
        # print i.select('div.details')[0].text.encode('utf-8').split("此")[0].replace("\n+",",").replace("\t+",",")
        hotel_dict['comment'] = i.select('div.details')[0].text.encode('utf-8').split("此")[0].replace("\n+",",").replace("\t+",",").decode('utf-8')
        hotel_list.append(hotel_dict.copy())
    time.sleep(n)
    driver1.execute_script('window.scrollTo(0, 1500);')
    try:
      driver1.find_element_by_css_selector('#reviews-pagination > fieldset > div > button.pagination-next > abbr').click()
    except Exception as e:
        print "This is end"
    time.sleep(n)
driver1.quit()
#==========================#
import json
contentjson = json.dumps(hotel_list, ensure_ascii=False)
with open('E:\AB104\Taipei-Hotels-Royal-Seasons-Hotel-Taipei_commend.json', 'w') as f:
    f.write(contentjson.encode('utf-8'))
#==========================#
s2 = datetime.now() ####### 結束時間
print "All  Finish "+str(s2-s1)+"!!" ####### 總共爬取資料耗費時間
#All  Finish 0:08:48.110000!!
