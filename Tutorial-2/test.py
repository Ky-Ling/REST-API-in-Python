'''
Date: 2022-02-27 13:56:18
LastEditors: GC
LastEditTime: 2022-02-27 22:11:44
FilePath: \REST API\Tutorial-2\test.py
'''
import requests

BASE = "http://127.0.0.1:5000/"

# data = [
#     {"likes": 1223, "name": "Hello", "views": 1234},
#     {"likes": 123423, "name": "World", "views": 4551234},
#     {"likes": 12239876, "name": "Yeah", "views": 12342456}
# ]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())



input()
response = requests.patch(BASE + "video/2", {"views": 234567})
print(response.json())


