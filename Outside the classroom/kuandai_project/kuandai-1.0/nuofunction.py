# 部分写法借鉴 https://zhuanlan.zhihu.com/p/191566983
import os
import requests
import time
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class lianwang:
    def geturl(self, url):
        try:
            http = urllib3.PoolManager()
            http.request('GET', url)
            return 1
        except Exception as e:
            return 0

    def touoptions(self):
        # 头部设置
        self.options.add_argument("--incognito")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        return True

    def openurl(self, url):
        """
        打开网页
        :param url:
        :return: 返回 webdriver
        """
        # 谷歌浏览器判断
        try:
            print("正在使用谷歌浏览器")
            self.options = ChromeOptions()
            self.touoptions()
            # service = Service("./chromedriver.exe")
            # os.path.join(os.path.abspath("."), "chromedriver.exe"))
            # CHROMEDRIVER_PATH = "./chromedriver.exe"
            # service = Service(executable_path=CHROMEDRIVER_PATH)

            # self.driver = webdriver.Chrome(options=options)
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.get(url)
            return True
        except:
            print("谷歌浏览器调用失败，正在调用其他浏览器")

        # 火狐浏览器判断
        try:
            print("正在使用火狐浏览器")
            self.options = FirefoxOptions()
            self.touoptions()
            # service = Service("./chromedriver.exe")
            # os.path.join(os.path.abspath("."), "chromedriver.exe"))
            # CHROMEDRIVER_PATH = "./chromedriver.exe"
            # service = Service(executable_path=CHROMEDRIVER_PATH)

            # self.driver = webdriver.Firefox(options=options)
            self.driver = webdriver.Firefox(options=self.options)
            self.driver.get(url)
            return True
        except:
            print("火狐浏览器调用失败，正在调用其他浏览器")

        # Edge浏览器判断
        try:
            print("正在使用Edge浏览器")
            self.options = EdgeOptions()
            self.touoptions()
            # service = Service("./chromedriver.exe")
            # os.path.join(os.path.abspath("."), "chromedriver.exe"))
            # CHROMEDRIVER_PATH = "./chromedriver.exe"
            # service = Service(executable_path=CHROMEDRIVER_PATH)

            # self.driver = webdriver.Firefox(options=options)
            self.driver = webdriver.Edge(options=self.options)
            self.driver.get(url)
            return True
        except:
            print("Edge浏览器调用失败")

        return False

    def find(self, type, text):
        """
        查找网页元素
        """
        try:
            if type == 'id':
                elem = self.driver.find_element(By.ID, text)
            elif type == 'name':
                elem = self.driver.find_element(By.NAME, text)
            elif type == 'class':
                elem = self.driver.find_element(By.CLASS_NAME, text)
            elif type == 'xpath':
                elem = self.driver.find_element(By.XPATH, text)
            elif type == 'css':
                elem = self.driver.find_element(By.CSS_SELECTOR, text)
            else:
                return False, 0
        except Exception as e:
            return False, 0
        return True, elem

    def shell(self, type1, type2, text1, text2=''):
        """
        综合判断并执行区
        """
        _isOK, _strLOG = self.find(type1, text1)
        if not _isOK:  # 元素没找到，返回失败结果
            return False
        elem = _strLOG
        # 点击
        if type2 == "click":
            try:
                elem.click()
            except Exception:
                return False
            return True
        # 清除框中内容
        elif type2 == "clear":
            try:
                elem.clear()
            except Exception:
                return False
            return True
        # 输入
        elif type2 == "element":
            try:
                elem.send_keys(text2)
            except Exception:
                return False
            return True

    def closeurl(self):
        self.driver.quit()
