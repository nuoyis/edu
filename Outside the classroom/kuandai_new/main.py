import os
import platform
from DrissionPage import ChromiumOptions, ChromiumPage

# 创建页面对象，并启动或接管浏览器
Options = ChromiumOptions()
Options.set_argument('--incognito')
Options.set_argument('--no-sandbox')
Options.set_argument('--headless')
Options.set_argument('--disable-gpu')
Options.set_argument('--ignore-certificate-errors')
try:
    page = ChromiumPage(Options)
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

# 跳转到登录页面
page.get('https://gitee.com/login')

# 定位到账号文本框，获取文本框元素
ele = page.ele('#user_login')
# 输入对文本框输入账号
ele.input('15802704408')
# 定位到密码文本框并输入密码
page.ele('#user_password').input('050331xWk')
# 点击登录按钮
page.ele('@value=登 录').click()