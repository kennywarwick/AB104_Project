#coding:UTF-8

import json
ALL = []
for i in range(1,8):
    with open("E:/AB104/Expedia/20170104_Expedia_HotelName_list{}.json".format(i),'r') as a:
        data = json.load(a)
        # print data
        for j in data:
            # print j
            ALL.append(j)
contentjson = json.dumps(ALL, ensure_ascii=False)
with open('E:/AB104/Expedia/20170104_Expedia_HotelName_list_ALL.json', 'w') as f:
    f.write(contentjson.encode('utf-8'))







