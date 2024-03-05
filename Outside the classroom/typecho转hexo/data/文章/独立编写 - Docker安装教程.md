---
title: 独立编写 - Docker安装教程
date: 2023-01-31 20:05:00
categories: 技术类
tags: []
---
#Linux安装教程
##Centos/Openanolis/OpenCloudOS适用以下代码
###万能脚本

```
curl -fsSL get.docker.com -o get-docker.sh
```
###手动执行首先运行

```
yum install docker-ce -y
```

如果出现未找到软件包先执行以下指令
```shell
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sed -i 's+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
yum makecache
```
##ubuntu/debian
```
apt update
apt upgrade -y
apt install curl vim wget gnupg dpkg apt-transport-https lsb-release ca-certificates
curl -sS
https://download.docker.com/linux/debian/gpg | gpg --dearmor > /usr/share/keyrings/docker-ce.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-ce.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian $(lsb_release -sc) stable" > /etc/apt/sources.list.d/docker.list
apt update
apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#Windows安装教程
windows请先准备Win10系统(不推荐win10以下系统使用docker),并开启Hyper-V功能    Hyper-V开启方法:    1.windows键右击,找到应用和功能,点击右上方程序和功能,找到Hyper-V全勾上    2.win+i键打开设置,点击应用,然后操作如上    开启后点击[这里][1]下载Docker desktop,下载完后一路next,再点击finish完成    如果桌面上没有docker图标,请在启动栏上进行搜索查找运行,并复制其快捷方式到桌面    然后打开cmd或者shell运行下docker run hello-world是否在下载docker镜像

[1]: https://hub.docker.com/?overlay=onboarding

```

```

