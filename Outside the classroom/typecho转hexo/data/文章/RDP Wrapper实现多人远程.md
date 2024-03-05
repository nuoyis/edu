---
title: RDP Wrapper实现多人远程
date: 2021-11-30 10:11:00
categories: 教程类
tags: []
---

>RDP Wrapper是个电脑上使用的多人远程连接软件，该软件破解了win10以上机型单人登录的问题。  
首先你的电脑支持远程开关，win10没有请先升级专业版  
进入官网下载RDP Wrapper ，地址:[](https://github.com/stascorp/rdpwrap)[](https://github.com/stascorp/rdpwrap)[https://github.com/stascorp/rdpwrap](https://github.com/stascorp/rdpwrap)  
下载完毕后，你的文件夹内有5个文件内容  
install.bat RDPcheck.exe RDPConf.exe RDPWlnst.exe update.exe  
运行install.bat(以管理方式运行)  
接着打开cmd(以管理方式运行),输入net stop termservice  
在资源管理器里,打开C:\\Program Files\\RDP Wrapper  
找到dll下的ini文件  
替换以下文件（解压后替换)  
资源下载链接:[](https://caiyun.139.com/m/i?135Ce8H2tpZTS)[https://caiyun.139.com/m/i?135Ce8H2tpZTS](https://caiyun.139.com/m/i?135Ce8H2tpZTS)  
提取码:qHeX  
(所有博客文件都在内)

替换完成后，继续打开cmd,输入代码net start termservice

大功告成，如果还没有绿色字体的内容请运行update
