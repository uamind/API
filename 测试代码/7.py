#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   7.py
@Time    :   2023/06/23 11:23:02
@Author  :   CryMang 
@Version :   1.0
@Contact :   uamind@foxmail.com

@License :   GPL v3.0 (https://www.gnu.org/licenses/gpl-3.0.html)

@Description :
该软件受GNU通用公共许可证（GPL）保护。

如果您使用本软件，则必须符合GPL下的条款，
可以在以下位置查看完整许可证文本：

    https://www.gnu.org/licenses/gpl-3.0.html

或者通过向Free Software Foundation, Inc.发送请求获得。
'''

# Here put the import libraries
import requests

SERVER_URL = 'http://127.0.0.1'

#抓包代理//不抓包可以注释代理代码并取消传递proxies变量
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}

json = {
    "id": 4,
    "名字": "赵六",
    "年龄": 22
}

response = requests.post(url=SERVER_URL + '/students', json=json, proxies=proxies)

print(f'状态码：{response.status_code}')
print(f'结果：{response.text}')