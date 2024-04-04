# import os
# os.system("pip install -r requirements.txt")
import getpass
import sys
import time
import ctypes
from time import sleep
from subprocess import run, PIPE

from nuoyis_webautomatic_function import lianwang

# 校园网定义
xiaoyuanurl = ""

# 校园网账号
xiaoyuanusername = ""

# 校园网密码
xiaoyuanpassword = ""


def login():
    print("正在静默登陆中，请稍后....")

    if True in nuo.find("xpath://html/body/div/div[1]/div[3]/div[5]/input"):
        print("检测到登录，开始执行")
        nuo.shell("xpath", "click", "xpath://html/body/div/div[1]/div[3]/div[5]/input")
    else:
        print("未检测到登录，继续执行")
    sleep(10)
    # 用户名
    nuo.shell("click", "xpath://html/body/div/div[3]/form/input[1]")
    nuo.shell("clear", "xpath://html/body/div/div[3]/form/input[1]")
    nuo.shell("element", "xpath://html/body/div/div/div[3]/form/input[1]", xiaoyuanusername)

    # 密码
    nuo.shell("click", "xpath://html/body/div/div[3]/form/input[2]")
    nuo.shell("clear", "xpath://html/body/div/div[3]/form/input[2]")
    nuo.shell("element", "xpath://html/body/div/div/div[3]/form/input[2]", xiaoyuanpassword)
    nuo.shell("click", "xpath://html/body/div/div/div[3]/form/button")

    # 关闭浏览器内核
    nuo.closeurl()


if __name__ == "__main__":
    nuo = lianwang()
    print("正在检测浏览器是否正常,第一次如果异常需要连接互联网")
    nuo.openurl("https://www.baidu.com")
    nuo.closeurl()
    print("后台未报错，继续执行")
    # 校园网连接性检测
    if not (nuo.geturl(xiaoyuanurl)):
        print("网络异常或不是校园网，请检查")
        exit(1)
    login()



# # 跳转到登录页面
# page.get('https://gitee.com/login')
#
# # 定位到账号文本框，获取文本框元素
# ele = page.ele('#user_login')
# # 输入对文本框输入账号
# ele.input('15802704408')
# # 定位到密码文本框并输入密码
# page.ele('#user_password').input('050331xWk')
# # 点击登录按钮
# page.ele('@value=登 录').click()
