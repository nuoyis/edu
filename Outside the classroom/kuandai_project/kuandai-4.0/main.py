# 第一次运行，需要把下方放开，或者手动终端执行`pip install -r requirements.txt`
# import os
# os.system("pip install -r requirements.txt")
import json
import getpass
import time
from time import sleep
from subprocess import run, PIPE
from nuoyis_webautomatic_function import lianwang

if __name__ == "__main__":
    try:
        with open("config.json", 'r') as kuandai_config:
            nuoyis_kuandai_load = json.load(kuandai_config)
        # 校园网定义区域
        # if not len(nuoyis_kuandai_load): raise FileNotFoundError
        for nonull in nuoyis_kuandai_load:
            if not len(nuoyis_kuandai_load[nonull]):
                raise FileNotFoundError
        # 校园网地址
        xiaoyuanurl = nuoyis_kuandai_load['xiaoyuanurl']
        # 校园网账号
        xiaoyuanusername = nuoyis_kuandai_load['xiaoyuanusername']
        # 校园网密码
        xiaoyuanpassword = nuoyis_kuandai_load['xiaoyuanpassword']
        # 登出按钮
        logout = nuoyis_kuandai_load['logout']
        # 登录名
        login_user = nuoyis_kuandai_load['login_user']
        # 登录密码
        login_password = nuoyis_kuandai_load['login_password']
        # 登录按钮
        login_check = nuoyis_kuandai_load['login_check']
        # 是否循环检测
        loop = nuoyis_kuandai_load['loop']
    except Exception as e:
        print("未检测到config文件或缺少数据内容，正在为你重新生成，生成后请重新运行")
        xiaoyuanfile = {'xiaoyuanurl': input("请输入校园网登录地址:"),
                        'xiaoyuanusername': getpass.getpass("请输入账号:"),
                        'xiaoyuanpassword': getpass.getpass("请输入密码:"), 'logout': input("请输入登出按钮:"),
                        'login_user': input("请输入用户名xpath:(格式:xpath:/地址内容)"),
                        'login_password': input("请输入用户名密码xpath:(格式:xpath:/地址内容)"),
                        'login_check': input("请输入登录按钮xpath:(格式:xpath:/地址内容)"), 'loop': input("是否循环(填1或0)")}
        with open("config.json", 'w') as kuandai_config:
            kuandai_config.write(json.dumps(xiaoyuanfile, indent=2, sort_keys=True, ensure_ascii=False))
        print("写入成功，重新启动试试吧")
        exit(0)
    nuo = lianwang()
    print("正在检测浏览器是否正常,此次访问需要校园网能连通")
    nuo.openurl(xiaoyuanurl)
    nuo.closeurl()
    print("未检测到后台异常，继续执行")
    # 校园网连接性检测
    if not (nuo.geturl(xiaoyuanurl)):
        print("检测到后台异常：网络异常或不是校园网，请检查")
        exit(1)
    if loop == "1":
        cnt = 1
        while True:
            print(f"检测时间:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n", end='')
            r = run('ping www.baidu.com',
                    stdout=PIPE,
                    stderr=PIPE,
                    stdin=PIPE,
                    shell=True)
            if r.returncode:
                print('登录状态：异常 登录次数:{}次'.format(cnt), end='')
                nuo.login(xiaoyuanurl, xiaoyuanusername, xiaoyuanpassword, logout, login_user, login_password,
                          login_check)
                print('未检测到后台异常，登录请求:成功')
                cnt += 1
            else:
                print("登录状态:正常")
                print("十分钟后会自动更新", end='')
                sleep(60 * 10)  # 每十分钟检查一次
    else:
        nuo.login(xiaoyuanurl, xiaoyuanusername, xiaoyuanpassword, logout, login_user, login_password, login_check)
        print('未检测到后台异常，登录请求:成功')
