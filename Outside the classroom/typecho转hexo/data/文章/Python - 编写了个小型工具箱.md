---
title: Python - 编写了个小型工具箱
date: 2023-10-02 12:38:21
categories: uncategorized
tags: []
---
Python，一个大蟒蛇，上变成爬虫，再上是人工智能，下则是各种云服务云计算。这是我第一篇关于Python的文章。
这个工具箱，目前编写了两个实用的功能，以及其他废物功能(宣传功能和退出功能)
展示图片如下:
![屏幕截图 2023-10-02 202329.png][1]
![屏幕截图 2023-10-02 202401.png][2]
![屏幕截图 2023-10-02 202419.png][3]
![屏幕截图 2023-10-02 202442.png][4]
极域电子教室是我高中最痛恨的，因为我高中一直在撸代码，也有时候看些内卷的教程(当然云游戏也是在中午玩)
最痛恨的就是黑屏警告，本来机房课就没多少(恼)
于是那个时候C语言版本就出来了。直到今天，Python来解决了C语言的痛苦:不能获取管理员权限。
于是，系统账号管理就推出来了
全部代码如下:
```Python
from __future__ import print_function
import subprocess
import os
import time
import ctypes
import sys

def systemuser():
    print("---欢迎使用诺依阁工具箱---\n1.系统账号添加 2.删除系统账户 3.修改系统账户密码 4.查看用户列表 5.退出此功能")
    usernum = int(input("请输入序号:"))
    if usernum in [1, 2, 3, 4]:
        if usernum == 1:
            systemuseradd()
        elif usernum == 2:
            systemuserdel()
        elif usernum == 3:
            systemuserchangepassword()
        elif usernum == 4:
            os.system("net user")
            input("按 Enter 继续...")
        else:
            input("按 Enter 继续...")
    else:
        print("输入不正确，请重新输入")

def systemuseradd():
    # 系统账户创建
    sysuser = input("请输入用户名:")
    syspassword = input("请输入密码:")
    print("正在添加中,请稍后:")
    os.system("net user "+sysuser+" "+syspassword+" /add")
    if int(input("是否给予管理员权限，1是 ,2否定：")):
        os.system("net localgroup administrators "+sysuser+" /add")
        print("给予账户管理员权限成功")
    else:
        print("你未给予账户管理员权限")
    print("账户创建命令执行成功")
    input("按 Enter 继续...")

def systemuserdel():
    # 系统账户删除
    sysuser = input("请输入用户名:")
    print("正在删除中,请稍后:")
    os.system("net user "+sysuser+" /delete")
    print("账户删除命令执行成功")
    input("按 Enter 继续...")

def systemuserchangepassword():
    # 系统账户密码修改
    sysuser = input("请输入用户名:")
    print("正在修改中,请稍后:")
    os.system("net user " + sysuser + " *")
    print("账户修改命令执行成功")
    input("按 Enter 继续...")

def jiyukill():
    # 极域电子进程删除
    print("正在删除极域电子进程")
    os.system("@echo off")
    os.system("sc stop tdnetfilter")
    os.system("sc stop tdfilefilter")
    os.system("taskkill /im StudentMain.exe /f")
    os.system("taskkill /im StudentEX.exe  /f")
    os.system("taskkill /im MasterHelper.exe /f")
    print("删除进程完毕")
    input("按 Enter 继续...")

def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if admin():
        # 设置窗口标题
        os.system("title 诺依阁的工具箱 网站:<a href="https://blog.nuoyis.net")" title="https://blog.nuoyis.net")">https://blog.nuoyis.net")</a>
        os.environ['PYTHONIOENCODING'] = 'GBK'
        a = b = c = 0

        # 主菜单样式
        while (1):
            os.system('cls')
            print("---欢迎使用诺依阁工具箱---\n1.系统账号管理 2.删除极域电子 3.打开诺依阁的日记簿 4.关于工作箱 5.退出工具箱\n请注意:本软件仅供学习交流使用，任何违法违规行为自行承担")
            d = int(input("请输入1-5数字:"))

            if d == 5:
                exit()

            if d in [1, 2, 3, 4]:
                if d == 1:
                    systemuser()
                elif d == 2:
                    jiyukill()
                elif d == 3:
                    os.system("start <a href="https://blog.nuoyis.net")" title="https://blog.nuoyis.net")">https://blog.nuoyis.net")</a>
                elif d == 4:
                    print("此新版本为Python构建，原由C语言编写构建")
                    print("作者:诺依阁 新版编写时间:2023-09-30")
                    print("工具箱只是作者的学习内容，不为违法者任何行为买单")
                    input("按 Enter 继续...")
            else:
                print("输入错误，请重新输入")
        time.sleep(300)
    else:
        # 以管理员权限重新运行程序
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
```
如果您想加入功能，后续我将把最后一个序号改为else就可以完美解决
Python打包的是pyinstaller,如果未安装请按照下面指令安装:
```shell
 pip install pyinstaller
```

同时也写了个小cmd脚本，双击运行就可以直接生成
```cmd
@echo off
chcp 65001
pyinstaller -F -i main.ico main.py -n 诺依阁的工具箱
pause
```
放在主目录下，然后完成找到dist下的exe就行。
最后，放上成品各位体验
下载链接:https://static.nuoyis.net/lib/blog/download/%E8%AF%BA%E4%BE%9D%E9%98%81%E7%9A%84%E5%B7%A5%E5%85%B7%E7%AE%B1.exe

  [1]: https://io.nuoyis.net/typecho/uploads/2023/10/779419699.png
  [2]: https://io.nuoyis.net/typecho/uploads/2023/10/1709262822.png
  [3]: https://io.nuoyis.net/typecho/uploads/2023/10/3712880624.png
  [4]: https://io.nuoyis.net/typecho/uploads/2023/10/3509591716.png