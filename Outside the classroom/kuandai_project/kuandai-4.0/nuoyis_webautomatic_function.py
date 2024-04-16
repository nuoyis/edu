import os
import requests
import time
import urllib3
import platform
from DrissionPage import ChromiumOptions, ChromiumPage


class lianwang:
    def login(self, xiaoyuanurl, xiaoyuanusername, xiaoyuanpassword, logout, login_user, login_password, login_check):
        print("正在静默登陆中，请稍后....")
        self.openurl(xiaoyuanurl)
        if self.find(logout):
            print("检测到登录，开始执行")
            self.shell("click", logout)
        else:
            print("未检测到登录，继续执行")
        time.sleep(10)
        # 用户名
        # self.shell("clear", login_user)
        self.shell("element", login_user, xiaoyuanusername)
        # 密码
        # self.shell("clear", login_password)
        self.shell("element", login_password, xiaoyuanpassword)
        self.shell("click", login_check)

        # 关闭浏览器内核
        self.closeurl()

    def geturl(self, url):
        try:
            http = urllib3.PoolManager()
            http.request('GET', url)
            return 1
        except Exception as e:
            return 0

    def touoptions(self):
        self.options.set_argument('--incognito')
        self.options.set_argument('--no-sandbox')
        self.options.headless(True)
        self.options.set_argument('--disable-gpu')
        self.options.set_argument('--ignore-certificate-errors')

    def openurl(self, url):
        """
        打开网页
        """
        try:
            self.options = ChromiumOptions()
            self.touoptions()
            self.page = ChromiumPage(self.options)
        except FileNotFoundError:
            sys = platform.system()
            if sys == "Windows":
                print("检测到你的系统是windows,未下载chrome,正在打开官网")
                os.system("start https://www.google.cn/chrome/")
                print("打开成功，请安装后重试")
            elif sys == "Linux":
                print("检测到你的系统是Linux,未下载chrome,正在自动安装")
                linuxsystem = int(input("请判断你的命令类型，apt请输入1，dnf输入2"))
                # https://cn.linux-console.net/?p=9940#:~:text=%E7%82%B9%E5%87%BB%20%E4%B8%8B%E8%BD%BD%20Chrome%20%E6%8C%89%E9%92%AE%E3%80%82%20%E5%9C%A8%E2%80%9C%E8%8E%B7%E5%8F%96%20Linux%20%E7%89%88%20Chrome%E2%80%9D%E9%A1%B5%E9%9D%A2%E4%B8%8A%EF%BC%8C%E9%80%89%E6%8B%A9%E4%B8%8E%E6%82%A8%E7%9A%84,%E5%92%8C%20Linux%20Mint%EF%BC%89%E4%B8%8A%E5%AE%89%E8%A3%85%20Google%20Chrome%E3%80%82%20%24%20wget%20https%3A%2F%2Fdl.google.com%2Flinux%2Fdirect%2Fgoogle-chrome-stable_current_amd64.deb
                if linuxsystem == 1:
                    os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
                    os.system("sudo apt install ./google-chrome-stable_current_amd64.deb")
                    os.system("sudo apt install google-chrome-stable")
                elif linuxsystem == 2:
                    os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm")
                    os.system("sudo dnf localinstall ./google-chrome-stable_current_x86_64.rpm")
                    os.system("sudo dnf install google-chrome-stable")
            exit(1)
        try:
            self.page.get(url)
        except Exception as e:
            print("网页打开失败，请重试")
            exit(1)

    def find(self, text):
        if self.page.ele(text):
            return True
        else:
            return False

    def shell(self, nuotype, text1, text2=''):
        # try:
        if nuotype == 'click':
            self.page.ele(text1).click()
        elif nuotype == 'element':
            self.page.ele(text1).input(text2)
        elif nuotype == 'clear':
            self.page.ele(text1).clear()
        # except Exception as e:
        #     print("执行过程中出现错误，请重试")
        #     exit(1)

    def closeurl(self):
        self.page.close()
