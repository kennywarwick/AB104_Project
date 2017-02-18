#coding:UTF-8


import requests
from bs4 import BeautifulSoup
import json
#
# URL="https://www.expedia.com.tw/ugc/urs/api/hotelreviews/hotel/10638096/?_type=json&start=40&items=10&categoryFilter=&languageFilter=&searchTerm=&sortBy=&languageSort=zh&expweb.activityId=d6116033-3a2a-4823-bf5f-d51d2e6dc271&pageName=page.Hotels.Infosite.Information&origin=Expedia&caller=Expedia&guid=d7cb0e5a-a2d7-45a5-a522-b4c03691f785&jsonpCallback=jQuery18209431802832869798_1481010146162&_=1481010378153"
# res=requests.get(URL)
# data =json.loads(res.text)

# print data

# import json
# URL="https://www.expedia.com.tw/ugc/urs/api/hotelreviews/hotel/10638096/?_type=json&start=40&items=10&categoryFilter=&languageFilter=&searchTerm=&sortBy=&languageSort=zh&expweb.activityId=d6116033-3a2a-4823-bf5f-d51d2e6dc271&pageName=page.Hotels.Infosite.Information&origin=Expedia&caller=Expedia&guid=d7cb0e5a-a2d7-45a5-a522-b4c03691f785&jsonpCallback=jQuery18209431802832869798_1481010146162&_=1481010378153"
# res=requests.get(URL)
# myjson = json.dumps(res.text, ensure_ascii=False) # This is a unicode string
# with open('articles.json', 'w') as f:
#     f.write(myjson.encode('utf-8'))
# from collections import OrderedDict

# with open('articles.json') as data_file:
#     data = json.load(data_file, object_pairs_hook=OrderedDict).split("(")[1]
#     print data
#     data_file.close()
# myjson = json.load('articles.json', ensure_ascii=False) # This is a unicode string
# print myjson
# print data.values()
# print repr(data)
# print repr(data)
# a = json.loads(open('articles.json').read()).split("(")[1]
# # a = open('articles.json').read().split("(")[1]
# # for keys in a:
# #     print keys
# print json.dumps(a,ensure_ascii=False, indent=4, sort_keys=True)



from pprint import pprint

with open('articles.json') as data_file:
    data = json.load(data_file)

pprint(data)


# a = open('articles.json').read()
# print json.dumps(a,ensure_ascii=False, indent=4, sort_keys=True)

