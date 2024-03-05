---
title: Linux - 我的世界服务器搭建
date: 2023-07-15 10:23:28
categories: uncategorized
tags: []
---
下面环境基于Centos搭建，文章基于本子上内容恢复
#安装依赖包
```shell
sudo yum install git  //git安装
sudo yum group install "Development Tools" // 构建mcrcon
sudo yum install
```

#创建我的世界账户(不用root权限执行我的世界)
```shell
sudo useradd -r -m -u -d /opt/minecraft -s /bin/bash/minecraft
madir -P /opt/minecraft/{backups,tools,server}
```

#构建mcron软件包
```shell
cd /opt/minecraft/tools && git clone https://gitee.com/whtrys/mcron.git
gcc -std=gnull -pedantic -wall -wetra -O -S mcron /opt/minecraft/tools/mcrcon.c
```

#运行我的世界包
```shell
Java -Xmx1024M -Xms1024M -jar /opt/minecraft/server
```

注:1.内存和CPU建议在4GB以上(最新版可能需要16G以上)
2.需禁用一些容易卡BUG的物品，避免炸服