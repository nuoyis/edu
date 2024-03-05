---
title: python - 网页版校园宽带自动登录软件
date: 2023-11-04 02:51:07
categories: uncategorized
tags: []
---
自从来到了大学，我人变的比较懒，重复性的事情交给程序去做。
每次校园网输入和登录需要很久，有时候也会因为浏览器bug而卡壳。
展示效果
![网页捕获_4-11-2023_104219_172.17.1.2.jpeg][1]
![网页捕获_4-11-2023_104242_172.17.1.2.jpeg][2]
下面是做的简易代码
```
import time
import requests
import urllib3
import warnings
warnings.filterwarnings("ignore")

try:
    http = urllib3.PoolManager()
    http.request('GET', 'http://172.17.1.2')
except Exception as e:
    print("网络异常或不是校园网，请检查")
    time.sleep(2000)
    exit()

sslogin = input("请输入分配给的给予的安全密码")
if sslogin!="230908":
    print("密码错误")
    exit(0)
# response = requests.get("<a href="<a href="https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)"" title="https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)"">https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)"</a> title="<a href="https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)">https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)" title="https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)">https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)">https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)">https://blog.nuoyis.net/xiaoyuan/api.php?key="+sslogin)</a></a>
# if response.status_code == 200:
#     if(response.json().code!=200):
#         print("密码错误，请重启程序后登录")
# else:
#     print("请检查网络，并重新启动程序登录")
#     exit(0)
username = ""  # 请替换成你的用户名
password = ""  # 请替换成你的密码

import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--incognito")
options.add_argument('--headless')
driver = webdriver.Edge(options=options,)
driver.get("http://172.17.1.2")  # 打开网站

# # if(driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[1]
# try:
#     target = driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[1]')
# except exceptions.NoSuchElementException:
#     return False]').click())
print("正在静默登陆中，请稍后....")

try:
    driver.find_element(By.XPATH, "/html/body/div/div[1]/div[5]/input")
    print("检测到登录，开始执行")
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div[5]/input').click()
    time.sleep(10)
except:
    print("未检测到登录，继续执行")

#用户名框
driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[1]').click()  # 点击用户名输入框
driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[1]').clear()  # 清空输入框
driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[1]').send_keys(username)  # 自动敲入用户名

#密码框
driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[2]').click()  # 点击密码输入框
driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[2]').clear()  # 清空输入框
driver.find_element(By.XPATH, '/html/body/div/div[1]/form/input[2]').send_keys(password)  # 自动敲入密码

# 采用class定位登陆按钮
# driver.find_element_by_class_name('ant-btn').click() # 点击“登录”按钮
# 采用xpath定位登陆按钮，
driver.find_element(By.XPATH, '/html/body/div/div[1]/form/button').click()
print("登录完毕")
driver.quit()
```
py打包命令
```
pyinstaller -F main.py
```
没有pyinstaller就执行以下命令
```
pip install pyinstaller
```
注意事项：
1.172.17.1.2改成你们学校的网页登录地址
2.xpath获取方式：开发者模式->点击框元素->右键复制完整的xpath
![2023-11-04T02:47:56.png][3]
3.如果网页没加载好可能会引发python报错

  [1]: https://images.nuoyis.net/blog/typecho/uploads/2023/11/175824732.jpeg
  [2]: https://images.nuoyis.net/blog/typecho/uploads/2023/11/3429991873.jpeg
  [3]: https://images.nuoyis.net/blog/typecho/uploads/2023/11/657812672.png