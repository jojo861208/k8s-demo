#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

# csrftoken
client = requests.session()
csrftoken = client.get("http://127.0.0.1:8000/api-auth/login").cookies['csrftoken']


# read
data = {
    "username": "USER123", #APP使用者帳號
    "password": "password", #APP使用者密碼
    
    "csrftoken": csrftoken,
}

# 將帳密 POST 到 http://127.0.0.1:8000/api/user/can_login/ 查看是否有這筆帳密，並且是否能登入
r = requests.post("http://127.0.0.1:8000/api/user/can_login/", data=data, auth=('Lavender', 'password'))

print(r.text) # 回傳可以成功登入(DB有這組帳密的資料)或不能登入(DB沒有這筆帳密的資料)

"""
# create
# update
# delete
r = requests.delete("http://140.119.75.221:8000/api/game/2/", auth=('admin', 'admin'))
print r.text
"""

"""
# update
data = {
    "name": "ABC",
    "url": "https://stackoverflow.com/questions/53494112/i-am-getting-an-error-rest-framework-request-wrappedattributeerror-csrfcheck",
    "img": None,
    
    "csrftoken": csrftoken,
}

r = requests.put("http://127.0.0.1:8000/api/game/1/", data=data, auth=('Lavender', 'axd2684gold7'))
print r.text

# create
data = {
    "name": "ABC3",
    "url": "https://stackoverflow.com/questions/53494112/i-am-getting-an-error-rest-framework-request-wrappedattributeerror-csrfcheck",
    "img": None,
    
    "csrftoken": csrftoken,
}
r = requests.post("http://127.0.0.1:8000/api/game/", data=data, auth=('Lavender', 'axd2684gold7'))
print r.text

# delete
r = requests.delete("http://127.0.0.1:8000/api/game/1/", auth=('Lavender', 'axd2684gold7'))
print r.text
"""