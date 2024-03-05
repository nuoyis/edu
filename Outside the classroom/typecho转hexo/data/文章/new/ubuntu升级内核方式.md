---
title: ubuntu升级内核方式
date: 2023-11-05 01:07:24
categories: uncategorized
tags: []
---
我的服务器和本地小主机都已经升级内核至6.5.7版本，内核升级对一些新的内容支持较好，下面开始如何升级内核
![2023-11-05T01:06:31.png][1]
1.内核手动升级
查询内核方式
```
uname -a
```
如果你的内核和官网出的一样就无需升级，如果闲麻烦请看下面脚本
首先执行日常两行命令
```
sudo apt update
sudo apt upgrade
```
搜索你想要的内核
```
apt search linux-image
```
推荐下载的是linux-image-*.*.*.*-generic（结尾是-generic就行）

安装方式
```
sudo apt install linux-image-*.*.*.*-generic
```
更新引导
```
sudo update-grub
```
查看其他内核
```
dpkg --list | grep linux-image
```
卸载掉多余的内核
```
sudo apt-get purge linux-image-*.*.*.*-*
sudo apt-get purge linux-headers-*.*.*.*-*
sudo apt-get purge linux-modules-*.*.*.*-*
```
更新引导
```
sudo apt-get purge
```
再次执行日常两行命令
```
sudo apt update
sudo apt upgrade
```
重启
```
reboot
```
重启完成后验证
```
dpkg --list | grep linux-image
```
2.脚本安装法(来自文章https://zhuanlan.zhihu.com/p/657036678)
原来下载地址:
```
https://raw.githubusercontent.com/pimlie/ubuntu-mainline-kernel.sh/master/ubuntu-mainline-kernel.sh
```
自有库加速下载地址:
```
https://static.nuoyis.net/lib/blog/download/ubuntu-mainline-kernel.sh
```
下载脚本
```
wget 上方地址
```
安装脚本
```
sudo install ubuntu-mainline-kernel.sh /usr/local/bin/
```
安装最新版内核
```
sudo ubuntu-mainline-kernel.sh -i
```
安装指定版本内核
```
sudo ubuntu-mainline-kernel.sh -i 内核版本号
```
重启
```
reboot
```
检查内核版本
```
uname -a
```
检查完后，如果你之前有安装几乎，请手动执行1的操作来清除显示的空内核。期间可能会报错，但不影响清理


  [1]: https://images.nuoyis.net/blog/typecho/uploads/2023/11/1255144267.png