#coding:UTF-8

#listdir()
import os
import json

# 依檔案夾讀取出裡面所有資料
DATA_DIR = "E:/AB104/Booking/1"
file_data = []
for filename in os.listdir(DATA_DIR):
    print "Loading: %s" % filename
    with open(os.path.join(DATA_DIR, filename), 'rb')as a:
        data = json.load(a)
        # print type(data)
        file_data.append(data[0])

# 寫入同一Json檔
print len(file_data)
print type(file_data)

contentjson = json.dumps(file_data, encoding="UTF-8", ensure_ascii=False)
with open("E:/AB104/Booking/ALL_comm11111111.json", "w") as w:
    w.write(contentjson.encode('utf-8'))

# # 讀取寫入之Json檔
# with open("E:/AB104/Booking/ALL_comm.json", 'r') as a:
#     data = json.load(a)
#     for j in data:
#         print j

# # 也可用 os.walk()
# import os
#
# for root, dirs, files in os.walk("/tmp/"):
#     print root
#     for f in files:
#         print os.path.join(root, f)



