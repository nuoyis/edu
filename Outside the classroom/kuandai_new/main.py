# 第一次运行，需要把下方放开，或者手动终端执行`pip install -r requirements.txt`
# import os
# os.system("pip install -r requirements.txt")
import json
from time import sleep

from nuoyis_webautomatic_function import lianwang

with open("./config.json", 'r') as kuandai_config:
    nuoyis_kuandai_load = json.load(kuandai_config)
# 校园网定义
xiaoyuanurl = nuoyis_kuandai_load['xiaoyuanurl']
# 校园网账号
xiaoyuanusername = nuoyis_kuandai_load['xiaoyuanusername']
# 校园网密码
xiaoyuanpassword = nuoyis_kuandai_load['xiaoyuanpassword']


def login():
    print("正在静默登陆中，请稍后....")
    nuo.openurl(xiaoyuanurl)
    if nuo.find(nuoyis_kuandai_load['logout']):
        print("检测到登录，开始执行")
        nuo.shell("click", nuoyis_kuandai_load['logout'])
    else:
        print("未检测到登录，继续执行")
    sleep(10)
    # 用户名
    # nuo.shell("clear", nuoyis_kuandai_load['login_password'])
    nuo.shell("element", nuoyis_kuandai_load['login_user'], xiaoyuanusername)
    # 密码
    # nuo.shell("clear", nuoyis_kuandai_load['login_password'])
    nuo.shell("element", nuoyis_kuandai_load['login_password'], xiaoyuanpassword)
    nuo.shell("click", nuoyis_kuandai_load['login_check'])

    # 关闭浏览器内核
    nuo.closeurl()


if __name__ == "__main__":
    nuo = lianwang()
    print("正在检测浏览器是否正常,第一次如果异常需要连接互联网")
    nuo.openurl("http://localhost")
    nuo.closeurl()
    print("后台未报错，继续执行")
    # 校园网连接性检测
    if not (nuo.geturl(xiaoyuanurl)):
        print("网络异常或不是校园网，请检查")
        exit(1)
    login()
    print("未检测到报错，登录成功")

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
